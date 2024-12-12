from pathlib import Path

from pydantic import BaseModel, Field


class GADOToolSpecificConfigurations(BaseModel):
    gado_jar: Path = Field(...)
    hpo_ontology: Path = Field(...)
    hpo_predictions_info: Path = Field(...)
    genes: Path = Field(...)
    hpo_predictions: Path = Field(...)
