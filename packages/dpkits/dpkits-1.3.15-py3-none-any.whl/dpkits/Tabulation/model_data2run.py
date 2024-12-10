import pandas as pd
import numpy as np
from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Self
from ..logging import Logging

log = Logging()


class Data2Run(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    is_validated: bool = False
    is_md: bool = False
    df_data: pd.DataFrame = Field(min_items=1)
    df_info: pd.DataFrame = Field(min_items=1)


    @model_validator(mode='after')
    def valcheck_dfs(self) -> Self:

        if self.is_validated:
            log.print(f"Data2Run is already checked", log.clr_succ)
            return self

        log.print(f"Data2Run validating", log.clr_cyan)

        df_data = self.df_data
        df_info = self.df_info

        # # # COLUMNS CONSISTENCY-----------------------------------------------------------------------------------
        if df_data.shape[1] != df_info.shape[0]:
            raise ValueError("df_data's columns are not match with df_info's rows")

        log.print(" - Columns consistency")


        # # # CHECK & CONVERT 'val_lbl' to dict if it's a string----------------------------------------------------
        if df_info['val_lbl'].dtype in [str, object]:

            def convert_to_dict(row):

                if row == '{}':
                    return {}
                elif isinstance(row, dict):
                    return row
                else:
                    return eval(row)

            df_info['val_lbl'] = df_info['val_lbl'].apply(convert_to_dict)

            log.print(" - Check & Covert 'val_lbl' to dict if it is a string")


        # # # CONVERT TO MC-----------------------------------------------------------------------------------------
        if self.is_md:
            def recode_md_to_mc(row: pd.Series):
                lst_re = [i + 1 for i, v in enumerate(row.values.tolist()) if v == 1]
                return lst_re + ([np.nan] * (len(row.index) - len(lst_re)))

            def create_info_mc(row: pd.Series):
                lst_val = row.values.tolist()
                dict_re = {str(i + 1): v['1'] for i, v in enumerate(lst_val)}
                return [dict_re] * len(lst_val)

            for idx in df_info.query("var_type.isin(['MA', 'MA_mtr']) & var_name.str.contains(r'^\\w+\\d*_1$')").index:
                qre = df_info.at[idx, 'var_name'].rsplit('_', 1)[0]
                fil_idx = df_info.eval(f"var_name.str.contains('^{qre}_[0-9]+$')")
                cols = df_info.loc[fil_idx, 'var_name'].values.tolist()

                df_data[cols] = df_data[cols].apply(recode_md_to_mc, axis=1, result_type='expand')
                df_info.loc[fil_idx, ['val_lbl']] = df_info.loc[fil_idx, ['val_lbl']].apply(create_info_mc, result_type='expand')

            log.print(" - Convert to MC dataframe")


        # # # UNNETTED----------------------------------------------------------------------------------------------
        df_info['val_lbl_str'] = df_info['val_lbl'].astype(str)
        df_info['val_lbl_unnetted'] = df_info['val_lbl']

        for idx in df_info.query("val_lbl_str.str.contains('net_code')").index:

            dict_netted = df_info.at[idx, 'val_lbl_unnetted']
            dict_unnetted = dict()

            for key, val in dict_netted.items():

                if 'net_code' in key:
                    val_lbl_lv1 = dict_netted['net_code']

                    for net_key, net_val in val_lbl_lv1.items():

                        if isinstance(net_val, str):
                            dict_unnetted.update({str(net_key): net_val})
                        else:
                            dict_unnetted.update(net_val)

                else:
                    dict_unnetted.update({str(key): val})

            df_info.at[idx, 'val_lbl_unnetted'] = dict_unnetted

        df_info.drop(columns='val_lbl_str', inplace=True)

        log.print(" - Unnetted: 'val_lbl' in df_info")


        # # # CHECK UNIDENTIFIED VALUES-----------------------------------------------------------------------------
        df_data_check = df_data.copy()
        df_info_check = df_info.copy()

        df_info_check = df_info_check.loc[df_info_check.eval("~var_type.isin(['FT', 'FT_mtr', 'NUM']) | var_name == 'ID'"), :].drop(columns=['var_lbl', 'var_type', 'val_lbl'])
        df_data_check = df_data_check[df_info_check['var_name'].values.tolist()].dropna(axis=1, how='all').dropna(axis=0, how='all')
        df_info_check = df_info_check.set_index('var_name').loc[df_data_check.columns.tolist(), :]

        def convert_val_lbl(row):
            if row[0] != {}:
                row[0] = {int(k): np.nan for k in row[0].keys()}
            return row

        df_info_check = df_info_check.apply(convert_val_lbl, axis=1)
        dict_replace = df_info_check.to_dict()['val_lbl_unnetted']

        df_data_check = df_data_check.replace(dict_replace).dropna(axis=1, how='all')

        cols = df_data_check.columns.tolist()

        if 'ID' in cols:
            cols.remove('ID')

        df_data_check = df_data_check.dropna(subset=cols, how='all', axis=0)

        if not df_data_check.empty:
            df_data_check.reset_index(drop=True if 'ID' in df_data_check.columns else False, inplace=True)
            df_data_check = pd.melt(df_data_check, id_vars=df_data_check.columns[0], value_vars=df_data_check.columns[1:]).dropna()

            raise ValueError(f"Unidentified values are detected\n{df_data_check.to_string()}")

        log.print(" - Check unidentified values")


        # # # REMOVING DUPLICATED VALUES----------------------------------------------------------------------------
        str_query = "var_name.str.contains(r'^\\w+_1$') & var_type.str.contains('MA')"
        df_info_ma = df_info.query(str_query)

        def remove_dup(row: pd.Series):
            row_idx = row.index.values.tolist()
            lst_val = row.drop_duplicates(keep='first').values.tolist()
            return lst_val + ([np.nan] * (len(row_idx) - len(lst_val)))

        for qre_ma in df_info_ma['var_name'].values.tolist():
            prefix, suffix = qre_ma.rsplit('_', 1)
            cols = df_info.loc[df_info.eval(f"var_name.str.contains('^{prefix}_[0-9]{{1,2}}$')"), 'var_name'].values.tolist()
            df_data[cols] = df_data[cols].apply(remove_dup, axis=1, result_type='expand')

        log.print(" - Removing duplicated values")

        return self

