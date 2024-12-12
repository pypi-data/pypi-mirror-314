from pathlib import Path

from pheval_gado.prepare.create_input_data import create_input_file


def prepare_input_file(testdata_dir: Path, tool_input_commands_dir: Path) -> None:
    """Prepare the input data file for a corpus of phenopackets."""
    create_input_file(testdata_dir.joinpath("phenopackets"), tool_input_commands_dir)
