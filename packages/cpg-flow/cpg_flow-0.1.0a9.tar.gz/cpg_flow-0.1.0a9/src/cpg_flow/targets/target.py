"""

This module defines the `Target` class, which represents a target that a stage can act upon.
The `Target` class includes methods to retrieve sequencing groups and their IDs, compute a hash
for alignment inputs, and provide job attributes and prefixes. It also includes a property to
retrieve a unique target ID and a method to map internal IDs to participant or external IDs.

Classes:
    Target: Defines a target that a stage can act upon.

Methods:
    get_sequencing_groups(only_active: bool = True) -> list["SequencingGroup"]:
        Get a flat list of all sequencing groups corresponding to this target.

    get_sequencing_group_ids(only_active: bool = True) -> list[str]:
        Get a flat list of all sequencing group IDs corresponding to this target.

    alignment_inputs_hash() -> str:
        Compute a hash for the alignment inputs of the sequencing groups.

    target_id() -> str:
        Property to retrieve a unique target ID.

    get_job_attrs() -> dict:
        Retrieve attributes for Hail Batch job.

    get_job_prefix() -> str:
        Retrieve prefix for job names.

    rich_id_map() -> dict[str, str]:
        Map internal IDs to participant or external IDs, if the latter is provided.

Targets for workflow stages: SequencingGroup, Dataset, Cohort.

"""

import hashlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cpg_flow.targets import SequencingGroup


class Target:
    """
    Defines a target that a stage can act upon.
    """

    def __init__(self) -> None:
        # Whether to process even if outputs exist:
        self.forced: bool = False
        # If not set, exclude from the workflow:
        self.active: bool = True

    def get_sequencing_groups(
        self,
        only_active: bool = True,
    ) -> list['SequencingGroup']:
        """
        Get flat list of all sequencing groups corresponding to this target.
        """
        raise NotImplementedError

    def get_sequencing_group_ids(self, only_active: bool = True) -> list[str]:
        """
        Get flat list of all sequencing group IDs corresponding to this target.
        """
        return [s.id for s in self.get_sequencing_groups(only_active=only_active)]

    def alignment_inputs_hash(self) -> str:
        s = ' '.join(
            sorted(' '.join(str(s.alignment_input)) for s in self.get_sequencing_groups() if s.alignment_input),
        )
        h = hashlib.sha256(s.encode()).hexdigest()[:38]
        return f'{h}_{len(self.get_sequencing_group_ids())}'

    @property
    def target_id(self) -> str:
        """
        ID should be unique across target of all levels.

        We are raising NotImplementedError instead of making it an abstract class,
        because mypy is not happy about binding TypeVar to abstract classes, see:
        https://stackoverflow.com/questions/48349054/how-do-you-annotate-the-type-of
        -an-abstract-class-with-mypy

        Specifically,
        ```
        TypeVar('TargetT', bound=Target)
        ```
        Will raise:
        ```
        Only concrete class can be given where "Type[Target]" is expected
        ```
        """
        raise NotImplementedError

    def get_job_attrs(self) -> dict:
        """
        Attributes for Hail Batch job.
        """
        raise NotImplementedError

    def get_job_prefix(self) -> str:
        """
        Prefix job names.
        """
        raise NotImplementedError

    def rich_id_map(self) -> dict[str, str]:
        """
        Map if internal IDs to participant or external IDs, if the latter is provided.
        """
        return {s.id: s.rich_id for s in self.get_sequencing_groups() if s.participant_id != s.id}
