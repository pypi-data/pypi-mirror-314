from pathlib import Path

import pandas as pd
from pheval.post_processing.post_processing import PhEvalGeneResult, generate_pheval_result
from pheval.utils.file_utils import all_files


def read_gado_result(gado_result: Path) -> pd.DataFrame:
    """Read GADO tab separated result output."""
    return pd.read_csv(gado_result, delimiter="\t")


class PhEvalGeneResultFromGADOCreator:
    def __init__(self, gado_result: pd.DataFrame):
        self.gado_result = gado_result

    @staticmethod
    def _find_gene_identifier(result_entry: pd.Series) -> str:
        """Return the gene identifier for a result entry."""
        return result_entry["Ensg"]

    @staticmethod
    def _find_gene_symbol(result_entry: pd.Series) -> str:
        """Return the gene symbol for a result entry."""
        return result_entry["Hgnc"]

    @staticmethod
    def _find_score(result_entry: pd.Series) -> float:
        """Return the score for a result entry."""
        return result_entry["Zscore"]

    def extract_pheval_gene_requirements(self) -> [PhEvalGeneResult]:
        """Extract data required to produce PhEval gene output."""
        simplified_phen2gene_result = []
        for _index, row in self.gado_result.iterrows():
            simplified_phen2gene_result.append(
                PhEvalGeneResult(
                    gene_symbol=self._find_gene_symbol(row),
                    gene_identifier=self._find_gene_identifier(row),
                    score=self._find_score(row),
                )
            )
        return simplified_phen2gene_result


def create_standardised_results(results_dir: Path, output_dir: Path) -> None:
    """Create PhEval gene results from GADO raw result directory."""
    for result in all_files(results_dir):
        gado_result = read_gado_result(result)
        try:
            pheval_gene_result = PhEvalGeneResultFromGADOCreator(
                gado_result
            ).extract_pheval_gene_requirements()
            generate_pheval_result(
                pheval_result=pheval_gene_result,
                sort_order_str="descending",
                output_dir=output_dir,
                tool_result_path=result,
            )
        except KeyError:
            pass
