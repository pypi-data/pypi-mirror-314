import pandas as pd
import numpy as np
from pydantic import BaseModel, Field, ConfigDict, PositiveInt, field_validator, model_validator
from typing import List, Dict, Any, Self
from enum import Enum
from .model_data2run import Data2Run, log
from .model_question import *
from .table_horizontal import TableHorizontal
from .table_vertical import TabulationVertical



class CellContent(str, Enum):
    C0 = 'c'
    P0 = 'p'
    P1 = '%'



class SigTestType(str, Enum):
    NON = 'non'
    IND = 'ind'
    REL = 'rel'



class SigTest(BaseModel):
    type: SigTestType = Field(min_length=3, max_length=3, default='non')
    lvl: List[PositiveInt] = Field(min_items=0, max_items=2)
    cols: List[str] = Field(min_items=0, max_items=24)

    @field_validator('lvl')
    @classmethod
    def valcheck_lvl(cls, lvl) -> List[PositiveInt]:

        lst_err = list()
        for i in lvl:
            if not 0 < i < 100:
                lst_err.extend([i])

        if lst_err:
            raise ValueError(f"significant test lvl should in range (0 < i < 100) instead of {lst_err}")

        log.print(f"SigTest validating", log.clr_cyan)
        log.print(f" - Attribute 'lvl'")

        return lvl


    @field_validator('cols')
    @classmethod
    def valcheck_cols(cls, cols) -> List[str]:

        lst_err = list()
        for i in cols:
            x = re.match(r'^[A-Z]$', i)

            if not x:
                lst_err.extend([i])

        if lst_err:
            raise ValueError(f"significant test cols should in range [A-Z] instead of {lst_err}")


        log.print(f" - Attribute 'cols'")

        return cols



class Table(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)

    # INPUT
    tbl_name: str = Field(min_length=1, max_length=30, frozen=True)
    tbl_filter: str = Field(min_length=0, frozen=True)
    tbl_cell_content: List[CellContent] = Field(min_items=1, max_items=3, frozen=True)
    sig_test: SigTest

    is_hide_zero_cats: bool = False
    is_hide_zero_cols: bool = False
    weight_var: str = Field(min_length=0, frozen=True)

    tbl_header: Dict[str, Any]
    tbl_side: List[Question] = Field(min_items=1, examples=[{'name': 'Q1'}, {'name': '$Q2'}])

    data_to_run: Data2Run

    # OUTPUT
    df_horizontal: pd.DataFrame = pd.DataFrame()
    df_vertical: pd.DataFrame = pd.DataFrame()





    @model_validator(mode='after')
    def valcheck_tbl_infor(self) -> Self:

        # # # Check tbl_header -----------------------------------------------------------------------------------------
        lst_err = list()
        df_info = self.data_to_run.df_info
        dict_header_val = self.tbl_header

        for key_hd_grp, val_hd_grp in dict_header_val.items():
            for hd_grp_idx, hd_grp_item in enumerate(val_hd_grp):

                if len(hd_grp_item) == 0:
                    lst_err.extend([f" - Length of {item} @ {key_hd_grp} @ index[{hd_grp_idx}] equals zero"])
                    continue

                for qre in hd_grp_item:

                    qre_name = qre['qre_name']

                    match qre_name:

                        case qre_name if '@' in qre_name:
                            qre.update({'type': 'QUERY'})
                            continue

                        case qre_name if '$' in qre_name:
                            df_qre = df_info.query(f"var_name.str.contains('^{qre_name[1:]}_[0-9]{{1,2}}$')")

                        case _:
                            df_qre = df_info.query(f"var_name == '{qre_name}'")

                    if df_qre.empty:
                        lst_err.extend(
                            [f" - Question {item} @ {key_hd_grp} @ index[{hd_grp_idx}] @ {qre_name} is not found."])
                        continue

                    if qre['cats'] != {}:
                        s_diff = set(qre['cats'].keys()).difference(df_qre.iloc[0, -1].keys())

                        if s_diff.issuperset({'-1'}):
                            s_diff.remove('-1')

                        if len(s_diff) > 0:
                            lst_err.extend([
                                               f" - {item} @ {key_hd_grp} @ index[{hd_grp_idx}] @ {qre_name} @ {s_diff} is not in {df_qre.iloc[0, -1]}"])
                            continue

                    df_qre = df_qre.reset_index(drop=True)
                    dict_update_qre = {
                        'cats': df_qre.at[0, 'val_lbl_unnetted'] if qre['cats'] == {} else qre['cats'],
                        'type': df_qre.at[0, 'var_type'],
                        'lst_col': df_qre['var_name'].values.tolist(),
                    }

                    if len(qre['qre_lbl']) == 0:
                        dict_update_qre.update({'qre_lbl': df_qre.at[0, 'var_lbl']})

                    qre.update(dict_update_qre)

        arr_header_len = np.array([len(i) for i in list(dict_header_val.values())])

        if arr_header_len.min() != arr_header_len.max() != arr_header_len.mean():
            lst_err.extend([f" - Level {item} got an error: {arr_header_len}"])


        if len(lst_err):
            raise AttributeError(f"Invalid dict_header: \n{'\n'.join(lst_err)}")

        log.print(f"Table {self.tbl_name}'s header is checked", log.clr_succ)



        # # # Fill Question Attribute-----------------------------------------------------------------------------------
        for qre in self.tbl_side:

            if '$' in qre.name:
                str_query = f"var_name.str.contains(r'^{qre.name.replace('$', '')}_[0-9]{{1,2}}$')"
            else:
                str_query = f"var_name == '{qre.name}'"

            df_qre = self.data_to_run.df_info.query(str_query)

            if df_qre.empty:
                raise ValueError(f'{qre.name} is not found!!!')

            qre.fill_question(df_qre)

        log.print(f"Table {self.tbl_name}'s tbl_side[question] is filled successfully", log.clr_succ)



        # # # Generate df_horizontal------------------------------------------------------------------------------------
        tbl_hrz = TableHorizontal(obj_table=self)
        tbl_hrz.generate_df_horizontal()
        log.print(f"Table {self.tbl_name}'s df_horizontal is generated successfully", log.clr_succ)



        # # # Generate df_vertical--------------------------------------------------------------------------------------
        tbl_ver = TabulationVertical(obj_table=self)
        tbl_ver.generate_df_vertical()

        here = 1

        log.print(f"Table {self.tbl_name}'s df_vertical is generated successfully", log.clr_succ)












        return self