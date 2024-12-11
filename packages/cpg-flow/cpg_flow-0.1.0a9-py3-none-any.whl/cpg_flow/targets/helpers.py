"""
This module provides helper functions for handling sequencing type subdirectories.

Functions:
    seq_type_subdir: Returns a subdirectory name based on the sequencing type from the configuration.

"""

from cpg_utils.config import get_config


def seq_type_subdir() -> str:
    """
    Subdirectory parametrised by sequencing type. For genomes, we don't prefix at all.
    """
    seq_type = get_config()["workflow"].get("sequencing_type")
    return "" if not seq_type or seq_type == "genome" else seq_type
