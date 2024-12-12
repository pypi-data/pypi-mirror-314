from pathlib import Path

from pheval_gado.post_process.post_process_results_format import create_standardised_results


def post_process_results_format(raw_results_dir: Path, output_dir: Path) -> None:
    """Post-process GADO result to PhEval gene results."""
    print("...creating pheval gene results format...")
    create_standardised_results(
        results_dir=raw_results_dir,
        output_dir=output_dir,
    )
    print("done")
