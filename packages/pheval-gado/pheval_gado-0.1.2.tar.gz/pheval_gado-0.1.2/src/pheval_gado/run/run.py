import subprocess
from pathlib import Path

from pheval_gado.constants import PRIORITISE_COMMAND_FILE, PROCESSED_COMMAND_FILE
from pheval_gado.prepare.prepare_commands import write_prioritise_command, write_process_command
from pheval_gado.tool_specific_configuration_parser import GADOToolSpecificConfigurations


def process_input(
    tool_input_commands_dir: Path,
    input_dir: Path,
    tool_specific_configurations: GADOToolSpecificConfigurations,
) -> None:
    """Process the input data with GADO."""
    write_process_command(
        input_output_dir=tool_input_commands_dir,
        data_dir=input_dir,
        gado_jar=tool_specific_configurations.gado_jar,
        hpo_ontology=tool_specific_configurations.hpo_ontology,
        hpo_predictions_info=tool_specific_configurations.hpo_predictions_info,
    )
    print("processing")
    subprocess.run(
        ["bash", str(tool_input_commands_dir.joinpath(PROCESSED_COMMAND_FILE))], shell=False
    )


def prioritise_input(
    input_dir: Path,
    tool_input_commands_dir: Path,
    output_dir: Path,
    tool_specific_configurations: GADOToolSpecificConfigurations,
) -> None:
    """Prioritise the data with GADO."""
    write_prioritise_command(
        input_output_dir=tool_input_commands_dir,
        gado_jar=tool_specific_configurations.gado_jar,
        genes=tool_specific_configurations.genes,
        hpo_predictions=tool_specific_configurations.hpo_predictions,
        output_dir=tool_input_commands_dir,
        data_dir=input_dir,
        results_dir=output_dir,
    )
    print("prioritising")
    subprocess.run(
        ["bash", str(tool_input_commands_dir.joinpath(PRIORITISE_COMMAND_FILE))], shell=False
    )
