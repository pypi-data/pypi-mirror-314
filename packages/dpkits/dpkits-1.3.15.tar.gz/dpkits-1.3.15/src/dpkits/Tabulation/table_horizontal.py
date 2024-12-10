import pandas as pd
import numpy as np
from ..logging import Logging


class TableHorizontal(Logging):


    def __init__(self, *, obj_table):
        super().__init__()
        self.obj_table = obj_table



    def generate_df_horizontal(self):

        obj_table = self.obj_table
        lst_idx_qre = list()
        count = 0
        last_lvl = 0

        for key, val in obj_table.tbl_header.items():

            if obj_table.df_horizontal.empty:
                obj_table.df_horizontal = self.header_lst_qre_to_dataframe(hd_grp=key, lst_tbl_val=val)
            else:
                obj_table.df_horizontal = pd.concat([obj_table.df_horizontal, self.header_lst_qre_to_dataframe(hd_grp=key, lst_tbl_val=val)], axis=0, ignore_index=True)

            # generate idx_qre------------------------------------------------------------------------------------------
            step = 0
            for i in val[-1]:
                step += len(i['cats'].keys())


            for v in range(len(lst_idx_qre), obj_table.df_horizontal.index[-1], step):

                lst_idx_qre.extend([count] * step)

                count += len(val[-1])

            last_lvl = len(val) - 1
            # End of generate idx_qre-----------------------------------------------------------------------------------

        obj_table.df_horizontal['query_combine'] = obj_table.df_horizontal.filter(regex='^query_lvl_[0-9]{1,2}$').agg('&'.join, axis=1)
        obj_table.df_horizontal['idx_qre'] = obj_table.df_horizontal[f'qre_grp_lvl_{last_lvl}'] + lst_idx_qre


        # Add sig test header dataframe (Not yet)


        return self.obj_table



    def header_lst_qre_to_dataframe(self, *, hd_grp: str, lst_tbl_val: list) -> pd.DataFrame:

        df_comb_hd_data = pd.DataFrame()

        self.print(f"Header group name: {hd_grp}", self.clr_cyan_light)

        lst_cols = ['hd_grp', 'hd_lvl', 'qre_grp', 'qre', 'cols', 'type', 'lbl', 'cat_code', 'cat_lbl', 'query']

        for hd_lvl, lst_qre in enumerate(lst_tbl_val):

            self.print(f"Header group level: {hd_lvl}", self.clr_cyan)

            lst_data = self.header_lst_qre_to_dataframe_data(lst_qre=lst_qre, hd_grp=hd_grp, hd_lvl=hd_lvl)

            df_hd_data = pd.DataFrame(columns=lst_cols, data=lst_data)

            df_hd_data.columns = df_hd_data.columns + f'_lvl_{hd_lvl}'

            match hd_lvl:
                case 0:
                    df_comb_hd_data = df_hd_data
                case _:
                    df_comb_hd_data = self.combine_df_header_by_level(df_a=df_comb_hd_data, df_b=df_hd_data)


        return df_comb_hd_data



    def header_lst_qre_to_dataframe_data(self, *, lst_qre: list, hd_grp: str, hd_lvl: int) -> list[list]:

        lst_data = list()

        for i, qre in enumerate(lst_qre):

            self.print(f"Header group question: {i} - {qre}", self.clr_magenta if i % 2 == 0 else self.clr_magenta_light)

            for cat_key, cat_val in qre['cats'].items():

                str_query = str()
                lst_col = list()

                match qre['type']:

                    case 'QUERY':
                        str_query = f"({cat_key})"

                    case 'MA' | 'SA':
                        str_query = '(' + '|'.join([f"{col}=={int(cat_key)}" if int(cat_key) > 0 else f"{col}>{int(cat_key)}" for col in qre['lst_col']]) + ')'
                        lst_col = qre['lst_col']

                    case _:
                        self.print(f"{qre} has invalid type >>> terminated", self.clr_err)

                lst_row = [hd_grp, hd_lvl, i, qre['qre_name'], lst_col, qre['type'], qre['qre_lbl'], cat_key, cat_val, str_query]
                lst_data.append(lst_row)

        return lst_data



    @staticmethod
    def combine_df_header_by_level(df_a: pd.DataFrame, df_b: pd.DataFrame) -> pd.DataFrame:

        # self.print(f"Run 'combine_df_header_by_level'")

        df_a_repeat = pd.DataFrame(np.repeat(df_a.values, df_b.shape[0], axis=0), columns=df_a.columns)
        df_b_repeat = pd.DataFrame(np.repeat(df_b.values, df_a.shape[0], axis=0), columns=df_b.columns)

        df_b_repeat['idx1'] = df_b_repeat.index % df_a.shape[0]
        df_b_repeat['idx2'] = df_b_repeat.index
        df_b_repeat = df_b_repeat.sort_values(by=['idx1', 'idx2']).reset_index(drop=True).drop(columns=['idx1', 'idx2'])

        df_combine = pd.concat([df_a_repeat, df_b_repeat], axis=1)

        return df_combine















