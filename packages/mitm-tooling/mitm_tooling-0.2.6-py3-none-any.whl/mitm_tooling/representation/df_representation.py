import pandas as pd
import pydantic

from mitm_tooling.definition import ConceptName
from .intermediate_representation import Header


class MITMDataset(pydantic.BaseModel):
    header: Header
    dfs: dict[ConceptName, dict[str, pd.DataFrame]]
