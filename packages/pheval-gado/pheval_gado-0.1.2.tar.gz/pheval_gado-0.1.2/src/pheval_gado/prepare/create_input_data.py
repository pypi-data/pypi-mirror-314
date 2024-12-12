import csv
from pathlib import Path

from phenopackets import Phenopacket
from pheval.utils.file_utils import all_files
from pheval.utils.phenopacket_utils import PhenopacketUtil, phenopacket_reader

from pheval_gado.constants import INPUT_CASES_FILE_NAME


def get_list_of_phenotypic_features(phenopacket_util: PhenopacketUtil) -> [str]:
    """Return list of all HPO IDs describing a phenotypic profile in a phenopacket."""
    return [hpo.type.id for hpo in phenopacket_util.observed_phenotypic_features()]


def create_case_id_from_phenopacket(phenopacket_path: Path) -> str:
    """Create a case ID from the phenopacket file name."""
    return phenopacket_path.stem


def create_entry_for_phenopacket(phenopacket_path: Path, phenopacket: Phenopacket) -> [str]:
    """Create an entry for a phenopacket, with the sample ID and all observed HPO ids."""
    case_id = create_case_id_from_phenopacket(phenopacket_path)
    phenotypic_features = get_list_of_phenotypic_features(PhenopacketUtil(phenopacket))
    phenotypic_features.insert(0, case_id)
    return phenotypic_features


def create_all_entries(phenopacket_dir: Path) -> [str]:
    """Create all entries for a corpus of phenopackets."""
    entries = []
    for phenopacket_path in all_files(Path(phenopacket_dir)):
        phenopacket = phenopacket_reader(phenopacket_path)
        entries.append(create_entry_for_phenopacket(phenopacket_path, phenopacket))
    return entries


def write_input_file(entries: [str], output_dir: Path) -> None:
    """Write the input file for GADO."""
    with open(output_dir.joinpath(INPUT_CASES_FILE_NAME), "w", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerows(entries)
    f.close()


def create_input_file(phenopacket_dir: Path, output_dir: Path) -> None:
    """Create the input file for GADO given a corpus of phenopackets."""
    entries = create_all_entries(phenopacket_dir)
    write_input_file(entries, output_dir)
