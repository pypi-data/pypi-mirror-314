"""GADO Runner"""

from dataclasses import dataclass
from pathlib import Path

from pheval.runners.runner import PhEvalRunner

from pheval_gado.post_process.post_process import post_process_results_format
from pheval_gado.prepare.prepare import prepare_input_file
from pheval_gado.run.run import prioritise_input, process_input
from pheval_gado.tool_specific_configuration_parser import GADOToolSpecificConfigurations


@dataclass
class GADOPhEvalRunner(PhEvalRunner):
    """_summary_"""

    input_dir: Path
    testdata_dir: Path
    tmp_dir: Path
    output_dir: Path
    config_file: Path
    version: str

    def prepare(self):
        """prepare"""
        print("preparing")
        prepare_input_file(self.testdata_dir, self.tool_input_commands_dir)

    def run(self):
        """run"""
        print("running with GADO")
        tool_specific_configurations = GADOToolSpecificConfigurations.parse_obj(
            self.input_dir_config.tool_specific_configuration_options
        )
        process_input(
            tool_input_commands_dir=self.tool_input_commands_dir,
            input_dir=self.input_dir,
            tool_specific_configurations=tool_specific_configurations,
        )
        prioritise_input(
            input_dir=self.input_dir,
            tool_input_commands_dir=self.tool_input_commands_dir,
            output_dir=self.raw_results_dir,
            tool_specific_configurations=tool_specific_configurations,
        )

    def post_process(self):
        """post_process"""
        print("post processing")
        post_process_results_format(
            raw_results_dir=self.raw_results_dir, output_dir=self.output_dir
        )
