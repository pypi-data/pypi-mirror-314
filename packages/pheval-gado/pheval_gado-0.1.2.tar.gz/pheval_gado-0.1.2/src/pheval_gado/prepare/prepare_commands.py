from dataclasses import dataclass
from pathlib import Path

from pheval_gado.constants import (
    INPUT_CASES_FILE_NAME,
    PRIORITISE_COMMAND_FILE,
    PROCESSED_COMMAND_FILE,
    PROCESSED_HPO_NAME,
)


@dataclass
class GADOProcessCLIArguments:
    """CLI arguments required to run the GADO process command."""

    input_output_dir: Path
    data_dir: Path
    gado_jar: Path
    hpo_ontology: Path
    hpo_predictions_info: Path


@dataclass
class GADOPrioritiseCLIArguments:
    """CLI arguments required to run the GADO prioritise command."""

    input_output_dir: Path
    data_dir: Path
    results_dir: Path
    gado_jar: Path
    genes: Path
    hpo_predictions: Path


class CommandWriter:
    def __init__(self, output_file: Path):
        self.file = open(output_file, "w")

    def write_process_command(self, command_arguments: GADOProcessCLIArguments) -> None:
        """Write GADO process command."""
        try:
            self.file.write(
                "java -jar "
                + str(command_arguments.data_dir.joinpath(command_arguments.gado_jar))
                + " --mode "
                + "PROCESS"
                + " --output "
                + f"{str(command_arguments.input_output_dir.joinpath(PROCESSED_HPO_NAME))}"
                + " --caseHpo "
                + str(command_arguments.input_output_dir.joinpath(INPUT_CASES_FILE_NAME))
                + " --hpoOntology "
                + str(command_arguments.data_dir.joinpath(command_arguments.hpo_ontology))
                + " --hpoPredictionsInfo "
                + str(command_arguments.data_dir.joinpath(command_arguments.hpo_predictions_info))
                + "\n"
            )
        except IOError:
            print("Error writing ", self.file)

    def write_prioritise_command(self, command_arguments: GADOPrioritiseCLIArguments) -> None:
        """Write GADO prioritise command."""
        try:
            self.file.write(
                "java -jar "
                + str(command_arguments.data_dir.joinpath(command_arguments.gado_jar))
                + " --mode "
                + "PRIORITIZE"
                + " --output "
                + f"{str(command_arguments.results_dir)}"
                + " --caseHpoProcessed "
                + str(command_arguments.input_output_dir.joinpath(PROCESSED_HPO_NAME))
                + " --genes "
                + str(command_arguments.data_dir.joinpath(command_arguments.genes))
                + " --hpoPredictions "
                + str(command_arguments.data_dir.joinpath(command_arguments.hpo_predictions))
                + "\n"
            )
        except IOError:
            print("Error writing ", self.file)

    def close(self) -> None:
        """Close file."""
        self.file.close()


def write_process_command(
    input_output_dir: Path,
    data_dir: Path,
    gado_jar: Path,
    hpo_ontology: Path,
    hpo_predictions_info: Path,
) -> None:
    """Write GADO process command to file."""
    command_file_path = input_output_dir.joinpath(PROCESSED_COMMAND_FILE)
    command_writer = CommandWriter(command_file_path)
    command_arguments = GADOProcessCLIArguments(
        input_output_dir=input_output_dir,
        gado_jar=gado_jar,
        hpo_ontology=hpo_ontology,
        hpo_predictions_info=hpo_predictions_info,
        data_dir=data_dir,
    )
    command_writer.write_process_command(command_arguments)
    command_writer.close()


def write_prioritise_command(
    input_output_dir: Path,
    results_dir: Path,
    data_dir: Path,
    output_dir: Path,
    gado_jar: Path,
    genes: Path,
    hpo_predictions: Path,
) -> None:
    """Write GADO prioritise command to file."""
    command_file_path = output_dir.joinpath(PRIORITISE_COMMAND_FILE)
    command_writer = CommandWriter(output_dir.joinpath(command_file_path))
    command_arguments = GADOPrioritiseCLIArguments(
        input_output_dir=input_output_dir,
        gado_jar=gado_jar,
        genes=genes,
        hpo_predictions=hpo_predictions,
        results_dir=results_dir,
        data_dir=data_dir,
    )
    command_writer.write_prioritise_command(command_arguments)
    command_writer.close()
