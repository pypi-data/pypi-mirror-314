import pandas as pd
import numpy as np
from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import List, Self
from .model_side_qre import SideQre



class SideQres(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    qres: List[SideQre] | None = Field(min_items=1, examples=[{'name': 'Q1'}, {'name': '$Q2'}])
    df_info: pd.DataFrame | None

    @model_validator(mode='after')
    def fill_side_qres(self) -> Self:

        if not self.qres:
            return self

        for qre in self.qres:

            if '$' in qre.name:
                str_query = f"var_name.str.contains(r'^{qre.name.replace('$', '')}_[0-9]{{1,2}}$')"
            else:
                str_query = f"var_name == '{qre.name}'"

            df_qre = self.df_info.query(str_query)

            if df_qre.empty:
                raise ValueError(f'{qre.name} is not found!!!')


            if qre.label is None:
                qre.label = df_qre['var_lbl'].values[0]

            elif '{lbl}' in qre.label:
                qre.label = qre.label.replace('{lbl}', df_qre['var_lbl'].values[0])


            qre.type = df_qre['var_type'].values[0]


            if qre.cats is None:
                qre.cats = df_qre['val_lbl'].values[0]


            qre.cols = df_qre['var_name'].values.tolist()


            if (qre.type not in [QreType.SA, QreType.SA_MTR]) and qre.mean_factor is not None:
                raise ValueError(f"Attribute 'mean_factor' only use for SA question!!!")


            if qre.type != QreType.NUM and qre.num_att is not None:
                raise ValueError(f"Attribute 'num_att' only use for NUM question!!!")

        return self











