"""
Provides a `Workflow` class and a `@stage` decorator that allow to define workflows
in a declarative fashion.

A `Stage` object is responsible for creating Hail Batch jobs and declaring outputs
(files or metamist analysis objects) that are expected to be produced. Each stage
acts on a `Target`, which can be of the following:

    * SequencingGroup - an individual Sequencing Group (e.g. the CRAM of a single sample)
    * Dataset - a stratification of SGs in this analysis by Metamist Project (e.g. all SGs in acute-care)
    * Cohort - a stratification of SGs in this analysis by Metamist CustomCohort
    * MultiCohort - a union of all SGs in this analysis by Metamist CustomCohort

A `Workflow` object plugs stages together by resolving dependencies between different levels accordingly. Stages are
defined in this package, and chained into Workflows by their inter-Stages dependencies. Workflow names are defined in
main.py, which provides a way to choose a workflow using a CLI argument.
"""

import functools
import logging
from collections import defaultdict
from collections.abc import Callable
from enum import Enum
from typing import TYPE_CHECKING, Optional, Union

import networkx as nx

from cpg_flow.inputs import get_multicohort
from cpg_flow.status import MetamistStatusReporter
from cpg_flow.targets import Cohort, MultiCohort
from cpg_flow.utils import slugify, timestamp
from cpg_utils import Path
from cpg_utils.config import get_config
from cpg_utils.hail_batch import get_batch, reset_batch

if TYPE_CHECKING:
    from cpg_flow.stage import Stage, StageDecorator, StageOutput


def path_walk(expected, collected: set | None = None) -> set[Path]:
    """
    recursive walk of expected_out
    if the object is iterable, walk it
    this gets around the issue with nested lists and dicts
    mainly around the use of Array outputs from Cromwell

    Args:
        expected (Any): any type of object containing Paths
        collected (set): all collected paths so far

    Returns:
        a set of all collected Path nodes

    Examples:

    >>> path_walk({'a': {'b': {'c': Path('d')}}})
    {Path('d')}
    >>> path_walk({'a': {'b': {'c': [Path('d'), Path('e')]}}})
    {Path('d'), Path('e')}
    >>> path_walk({'a': Path('b'),'c': {'d': 'e'}, {'f': Path('g')}})
    {Path('b'), Path('g')}
    """
    if collected is None:
        collected = set()

    if expected is None:
        return collected
    if isinstance(expected, dict):
        for value in expected.values():
            collected.update(path_walk(value, collected))
    if isinstance(expected, list | set):
        for value in expected:
            collected.update(path_walk(value, collected))
    if isinstance(expected, str):
        return collected
    if isinstance(expected, Path):
        if expected in collected:
            raise ValueError(f'Duplicate path {expected} in expected_out')
        collected.add(expected)
    return collected


class WorkflowError(Exception):
    """
    Error raised by workflow and stage implementation.
    """


class Action(Enum):
    """
    Indicates what a stage should do with a specific target.
    """

    QUEUE = 1
    SKIP = 2
    REUSE = 3


# noinspection PyUnusedLocal
def skip(
    _fun: Optional['StageDecorator'] = None,
    *,
    reason: str | None = None,
    assume_outputs_exist: bool = False,
) -> Union['StageDecorator', Callable[..., 'StageDecorator']]:
    """
    Decorator on top of `@stage` that sets the `self.skipped` field to True.
    By default, expected outputs of a skipped stage will be checked,
    unless `assume_outputs_exist` is True.

    @skip
    @stage
    class MyStage1(SequencingGroupStage):
        ...

    @skip
    @stage(assume_outputs_exist=True)
    class MyStage2(SequencingGroupStage):
        ...
    """

    def decorator_stage(fun) -> 'StageDecorator':
        """Implements decorator."""

        @functools.wraps(fun)
        def wrapper_stage(*args, **kwargs) -> 'Stage':
            """Decorator helper function."""
            s = fun(*args, **kwargs)
            s.skipped = True
            s.assume_outputs_exist = assume_outputs_exist
            return s

        return wrapper_stage

    if _fun is None:
        return decorator_stage
    else:
        return decorator_stage(_fun)


_workflow: Optional['Workflow'] = None


def get_workflow(dry_run: bool = False) -> 'Workflow':
    global _workflow
    if _workflow is None:
        _workflow = Workflow(dry_run=dry_run)
    return _workflow


def run_workflow(
    stages: list['StageDecorator'] | None = None,
    wait: bool | None = False,
    dry_run: bool = False,
) -> 'Workflow':
    wfl = get_workflow(dry_run=dry_run)
    wfl.run(stages=stages, wait=wait)
    return wfl


class Workflow:
    """
    Encapsulates a Hail Batch object, stages, and a cohort of datasets of sequencing groups.
    Responsible for orchestrating stages.
    """

    def __init__(
        self,
        stages: list['StageDecorator'] | None = None,
        dry_run: bool | None = None,
    ):
        if _workflow is not None:
            raise ValueError(
                'Workflow already initialised. Use get_workflow() to get the instance',
            )

        self.dry_run = dry_run or get_config(True)['workflow'].get('dry_run')

        # TODO: should the ['dataset'] be a get? should we rename it to analysis dataset?
        analysis_dataset = get_config(True)['workflow']['dataset']
        name = get_config()['workflow'].get('name', analysis_dataset)
        description = get_config()['workflow'].get('description', name)
        self.name = slugify(name)

        self._output_version: str | None = None
        if output_version := get_config()['workflow'].get('output_version'):
            self._output_version = slugify(output_version)

        self.run_timestamp: str = get_config()['workflow'].get('run_timestamp') or timestamp()

        # Description
        if self._output_version:
            description += f': output_version={self._output_version}'
        description += f': run_timestamp={self.run_timestamp}'
        if sequencing_type := get_config()['workflow'].get('sequencing_type'):
            description += f' [{sequencing_type}]'
        if not self.dry_run:
            if ds_set := set(d.name for d in get_multicohort().get_datasets()):
                description += ' ' + ', '.join(sorted(ds_set))
            reset_batch()
            get_batch().name = description

        self.status_reporter = None
        if get_config()['workflow'].get('status_reporter') == 'metamist':
            self.status_reporter = MetamistStatusReporter()
        self._stages: list[StageDecorator] | None = stages
        self.queued_stages: list[Stage] = []

    @property
    def output_version(self) -> str:
        return self._output_version or get_multicohort().alignment_inputs_hash()

    @property
    def analysis_prefix(self) -> Path:
        return self._prefix(category='analysis')

    @property
    def tmp_prefix(self) -> Path:
        return self._prefix(category='tmp')

    @property
    def web_prefix(self) -> Path:
        return self._prefix(category='web')

    @property
    def prefix(self) -> Path:
        return self._prefix()

    def _prefix(self, category: str | None = None) -> Path:
        """
        Prepare a unique path for the workflow with this name and this input data.
        """
        return get_multicohort().analysis_dataset.prefix(category=category) / self.name / self.output_version

    def cohort_prefix(self, cohort: Cohort, category: str | None = None) -> Path:
        """
        Takes a cohort and category as an argument, calls through to the Workflow cohort_prefix method
        Result in the form PROJECT_BUCKET / WORKFLOW_NAME / COHORT_ID
        e.g. "gs://cpg-project-main/seqr_loader/COH123", or "gs://cpg-project-main-analysis/seqr_loader/COH123"

        Args:
            cohort (Cohort): we pull the analysis dataset and name from this Cohort
            category (str | None): sub-bucket for this project

        Returns:
            Path
        """
        return cohort.analysis_dataset.prefix(category=category) / self.name / cohort.name

    def run(
        self,
        stages: list['StageDecorator'] | None = None,
        wait: bool | None = False,
    ):
        """
        Resolve stages, add and submit Hail Batch jobs.
        When `run_all_implicit_stages` is set, all required stages that were not defined
        explicitly would still be executed.
        """
        _stages = stages or self._stages
        if not _stages:
            raise WorkflowError('No stages added')
        self.set_stages(_stages)

        if not self.dry_run:
            get_batch().run(wait=wait)

    @staticmethod
    def _process_first_last_stages(
        stages: list['Stage'],
        graph: nx.DiGraph,
        first_stages: list[str],
        last_stages: list[str],
    ):
        """
        Applying first_stages and last_stages config options. Would skip all stages
        before first_stages, and all stages after last_stages (i.e. descendants and
        ancestors on the stages DAG.)
        """
        stages_d = {s.name: s for s in stages}
        stage_names = list(stg.name for stg in stages)
        lower_names = {s.lower() for s in stage_names}

        for param, _stage_list in [
            ('first_stages', first_stages),
            ('last_stages', last_stages),
        ]:
            for _s_name in _stage_list:
                if _s_name.lower() not in lower_names:
                    raise WorkflowError(
                        f'Value in workflow/{param} "{_s_name}" must be a stage name '
                        f"or a subset of stages from the available list: "
                        f'{", ".join(stage_names)}',
                    )

        if not (last_stages or first_stages):
            return

        # E.g. if our last_stages is CramQc, MtToEs would still run because it's in
        # a different branch. So we want to collect all stages after first_stages
        # and before last_stages in their respective branches, and mark as skipped
        # everything in other branches.
        first_stages_keeps: list[str] = first_stages[:]
        last_stages_keeps: list[str] = last_stages[:]

        for fs in first_stages:
            for descendant in nx.descendants(graph, fs):
                if not stages_d[descendant].skipped:
                    logging.info(
                        f'Skipping stage {descendant} (precedes {fs} listed in first_stages)',
                    )
                    stages_d[descendant].skipped = True
                for grand_descendant in nx.descendants(graph, descendant):
                    if not stages_d[grand_descendant].assume_outputs_exist:
                        logging.info(
                            f'Not checking expected outputs of not immediately '
                            f'required stage {grand_descendant} (< {descendant} < {fs})',
                        )
                        stages_d[grand_descendant].assume_outputs_exist = True

            for ancestor in nx.ancestors(graph, fs):
                first_stages_keeps.append(ancestor)

        for ls in last_stages:
            # ancestors of this last_stage
            ancestors = nx.ancestors(graph, ls)
            if any(anc in last_stages for anc in ancestors):
                # a downstream stage is also in last_stages, so this is not yet
                # a "real" last stage that we want to run
                continue
            for ancestor in ancestors:
                if stages_d[ancestor].skipped:
                    continue  # already skipped
                logging.info(f'Skipping stage {ancestor} (after last {ls})')
                stages_d[ancestor].skipped = True
                stages_d[ancestor].assume_outputs_exist = True

            for ancestor in nx.descendants(graph, ls):
                last_stages_keeps.append(ancestor)

        for _stage in stages:
            if _stage.name not in last_stages_keeps + first_stages_keeps:
                _stage.skipped = True
                _stage.assume_outputs_exist = True

    @staticmethod
    def _process_only_stages(
        stages: list['Stage'],
        graph: nx.DiGraph,
        only_stages: list[str],
    ):
        if not only_stages:
            return

        stages_d = {s.name: s for s in stages}
        stage_names = list(stg.name for stg in stages)
        lower_names = {s.lower() for s in stage_names}

        for s_name in only_stages:
            if s_name.lower() not in lower_names:
                raise WorkflowError(
                    f'Value in workflow/only_stages "{s_name}" must be a stage '
                    f"name or a subset of stages from the available list: "
                    f'{", ".join(stage_names)}',
                )

        # We want to run stages only appearing in only_stages, and check outputs of
        # imediate predecessor stages, but skip everything else.
        required_stages: set[str] = set()
        for os in only_stages:
            rs = nx.descendants_at_distance(graph, os, 1)
            required_stages |= set(rs)

        for stage in stages:
            # Skip stage not in only_stages, and assume outputs exist...
            if stage.name not in only_stages:
                stage.skipped = True
                stage.assume_outputs_exist = True

        # ...unless stage is directly required by any stage in only_stages
        for stage_name in required_stages:
            stages_d[stage_name].assume_outputs_exist = False

    def set_stages(
        self,
        requested_stages: list['StageDecorator'],
    ):
        """
        Iterate over stages and call their queue_for_cohort(cohort) methods;
        through that, creates all Hail Batch jobs through Stage.queue_jobs().
        """
        # TOML options to configure stages:
        skip_stages = get_config()['workflow'].get('skip_stages', [])
        only_stages = get_config()['workflow'].get('only_stages', [])
        first_stages = get_config()['workflow'].get('first_stages', [])
        last_stages = get_config()['workflow'].get('last_stages', [])

        # Only allow one of only_stages or first_stages/last_stages as they seem
        # to be mutually exclusive.
        if only_stages and (first_stages or last_stages or skip_stages):
            raise WorkflowError(
                "Workflow config parameter 'only_stages' is incompatible with "
                + "'first_stages', 'last_stages' and/or 'skip_stages'",
            )

        logging.info(
            f'End stages for the workflow "{self.name}": {[cls.__name__ for cls in requested_stages]}',
        )
        logging.info('Stages additional configuration:')
        logging.info(f'  workflow/skip_stages: {skip_stages}')
        logging.info(f'  workflow/only_stages: {only_stages}')
        logging.info(f'  workflow/first_stages: {first_stages}')
        logging.info(f'  workflow/last_stages: {last_stages}')

        # Round 1: initialising stage objects.
        _stages_d: dict[str, Stage] = {}
        for cls in requested_stages:
            if cls.__name__ in _stages_d:
                continue
            _stages_d[cls.__name__] = cls()

        # Round 2: depth search to find implicit stages.
        depth = 0
        while True:  # might require few iterations to resolve dependencies recursively
            depth += 1
            newly_implicitly_added_d = dict()
            for stg in _stages_d.values():
                if stg.name in skip_stages:
                    stg.skipped = True
                    continue  # not searching deeper

                if only_stages and stg.name not in only_stages:
                    stg.skipped = True

                # Iterate dependencies:
                for reqcls in stg.required_stages_classes:
                    if reqcls.__name__ in _stages_d:  # already added
                        continue
                    # Initialising and adding as explicit.
                    reqstg = reqcls()
                    newly_implicitly_added_d[reqstg.name] = reqstg

            if newly_implicitly_added_d:
                logging.info(
                    f'Additional implicit stages: {list(newly_implicitly_added_d.keys())}',
                )
                _stages_d |= newly_implicitly_added_d
            else:
                # No new implicit stages added, so can stop the depth-search here
                break

        # Round 3: set "stage.required_stages" fields to each stage.
        for stg in _stages_d.values():
            stg.required_stages = [
                _stages_d[cls.__name__] for cls in stg.required_stages_classes if cls.__name__ in _stages_d
            ]

        # Round 4: determining order of execution.
        dag_node2nodes = dict()  # building a DAG
        for stg in _stages_d.values():
            dag_node2nodes[stg.name] = set(dep.name for dep in stg.required_stages)
        dag = nx.DiGraph(dag_node2nodes)
        try:
            stage_names = list(reversed(list(nx.topological_sort(dag))))
        except nx.NetworkXUnfeasible:
            logging.error('Circular dependencies found between stages')
            raise

        logging.info(f'Stages in order of execution:\n{stage_names}')
        stages = [_stages_d[name] for name in stage_names]

        # Round 5: applying workflow options first_stages and last_stages.
        if first_stages or last_stages:
            logging.info('Applying workflow/first_stages and workflow/last_stages')
            self._process_first_last_stages(stages, dag, first_stages, last_stages)
        elif only_stages:
            logging.info('Applying workflow/only_stages')
            self._process_only_stages(stages, dag, only_stages)

        if not (final_set_of_stages := [s.name for s in stages if not s.skipped]):
            raise WorkflowError('No stages to run')

        logging.info(
            f'Final list of stages after applying stage configuration options:\n{final_set_of_stages}',
        )

        required_skipped_stages = [s for s in stages if s.skipped]
        if required_skipped_stages:
            logging.info(
                f'Skipped stages: {", ".join(s.name for s in required_skipped_stages)}',
            )

        # Round 6: actually adding jobs from the stages.
        if not self.dry_run:
            inputs = get_multicohort()  # Would communicate with metamist.
            for i, stg in enumerate(stages):
                logging.info('*' * 60)
                logging.info(f'Stage #{i + 1}: {stg}')
                # pipeline setup is now done in MultiCohort only
                # the legacy version (input_datasets) is still supported
                # that will create a MultiCohort with a single Cohort
                if isinstance(inputs, MultiCohort):
                    stg.output_by_target = stg.queue_for_multicohort(inputs)
                else:
                    raise WorkflowError(f'Unsupported input type: {inputs}')
                if errors := self._process_stage_errors(stg.output_by_target):
                    raise WorkflowError(
                        f'Stage {stg} failed to queue jobs with errors: ' + '\n'.join(errors),
                    )

                logging.info('')

        else:
            self.queued_stages = [stg for stg in _stages_d.values() if not stg.skipped]
            logging.info(f'Queued stages: {self.queued_stages}')

    @staticmethod
    def _process_stage_errors(
        output_by_target: dict[str, Union['StageOutput', None]],
    ) -> list[str]:
        targets_by_error = defaultdict(list)
        for target, output in output_by_target.items():
            if output and output.error_msg:
                targets_by_error[output.error_msg].append(target)
        return [f'{error}: {", ".join(target_ids)}' for error, target_ids in targets_by_error.items()]
