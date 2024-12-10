import pandas as pd
import numpy as np
from .logging import Logging


class DataProcessing(Logging):

    def __init__(self, *, df_data: pd.DataFrame, df_info: pd.DataFrame):
        super().__init__()
        self.df_data: pd.DataFrame = df_data
        self.df_info: pd.DataFrame = df_info



    def add_qres(self, dict_add_new_qres: dict, is_add_oe_col: bool = False) -> (pd.DataFrame, pd.DataFrame):
        """
        :param dict_add_new_qres:
            'var_name': ['var_lbl', 'var_type', val_lbl, default value],
            var_name: str
            var_lbl: str
            var_type: str ['SA', 'SA_mtr', 'MA', 'MA_mtr', 'NUM', 'FT']
        :param is_add_oe_col: bool
        :return: df_data, df_info
        """

        info_col_name = ['var_name', 'var_lbl', 'var_type', 'val_lbl']
        lst_keys = list(dict_add_new_qres.keys())

        lst_data_addin = list()
        lst_info_addin = list()
        lst_colname = list()
        int_max_row = self.df_data.shape[0]

        for key, val in dict_add_new_qres.items():
            self.print(f'Add new variables to df_data & df_info: {key}', end="" if key != lst_keys[-1] else "\n")

            if val[1] in ['MA']:
                qre_ma_name, max_col = str(key).rsplit('|', 1)

                for i in range(1, int(max_col) + 1):

                    lst_info_addin.append([f'{qre_ma_name}_{i}', val[0], val[1], val[2]])

                    if '_OE' not in key or is_add_oe_col is True:
                        lst_colname.append(f'{qre_ma_name}_{i}')
                        lst_data_addin.append([val[-1]] * int_max_row)

            else:

                lst_info_addin.append([key, val[0], val[1], val[2]])

                if '_OE' not in key or is_add_oe_col is True:
                    lst_colname.append(key)
                    lst_data_addin.append([val[-1]] * int_max_row)


        self.df_info = pd.concat([self.df_info, pd.DataFrame(columns=info_col_name, data=lst_info_addin)], axis=0, ignore_index=True)

        if len(lst_colname) > 0:
            self.df_data = pd.concat([self.df_data, pd.DataFrame(columns=lst_colname, data=np.array(lst_data_addin).transpose())], axis=1)

        self.df_data.reset_index(drop=True, inplace=True)
        self.df_info.reset_index(drop=True, inplace=True)

        return self.df_data, self.df_info



    def align_ma_values_to_left(self, qre_name: str | list, fillna_val: float = None) -> pd.DataFrame:
        """
        :param qre_name: MA likes 'Q1|8'
        :param fillna_val: fil nan with float value
        :return: df_data
        """
        lst_qre_name = [qre_name] if isinstance(qre_name, str) else qre_name

        for qre_item in lst_qre_name:

            qre, max_col = qre_item.rsplit('|', 1)

            lst_qre = [f'{qre}_{i}' for i in range(1, int(max_col) + 1)]

            df_fil = self.df_data.loc[:, lst_qre].copy()
            df_fil = df_fil.T
            df_sort = pd.DataFrame(np.sort(df_fil.values, axis=0), index=df_fil.index, columns=df_fil.columns)
            df_sort = df_sort.T
            self.df_data[lst_qre] = df_sort[lst_qre]

            del df_fil, df_sort

            if fillna_val:
                self.df_data.loc[self.df_data.eval(f"{qre}_1.isnull()"), f'{qre}_1'] = fillna_val

        return self.df_data



    def remove_qres(self, lst_col: list) -> (pd.DataFrame, pd.DataFrame):
        """
        :param lst_col: columns to remove
        :return: df_data, df_info
        """
        self.df_data.drop(columns=lst_col, inplace=True)
        self.df_info = self.df_info.loc[self.df_info.eval(f"~var_name.isin({lst_col})"), :].copy()

        self.df_data.reset_index(drop=True, inplace=True)
        self.df_info.reset_index(drop=True, inplace=True)

        return self.df_data, self.df_info



    def merge_qres(self, *, lst_merge: list, lst_to_merge: list, dk_code: int) -> pd.DataFrame:
        """
        :param lst_merge: output columns
        :param lst_to_merge: input columns
        :param dk_code:
        :return: df_data
        """

        codelist = self.df_info.loc[self.df_info.eval("var_name == @lst_merge[0]"), 'val_lbl'].values.tolist()[0]

        if len(lst_merge) < len(codelist.keys()):
            self.print(f"Merge_qres(error): Length of lst_merge should be greater than or equal length of codelist!!!\nlst_merge = {lst_merge}\ncodelist = {codelist}\nProcessing terminated!!!", self.err)
            exit()


        def merge_row(sr_row: pd.Series, lst_col_name: list, dk: int) -> pd.Series:

            lst_output = sr_row.reset_index(drop=True).drop_duplicates(keep='first').dropna().sort_values().values.tolist()
            output_len = len(lst_col_name)

            if len(lst_output) > 1 and dk in lst_output:
                lst_output.remove(dk)

            if len(lst_output) < output_len:
                lst_output.extend([np.nan] * (output_len - len(lst_output)))

            return pd.Series(data=lst_output, index=lst_col_name)

        self.df_data[lst_merge] = self.df_data[lst_to_merge].apply(merge_row, lst_col_name=lst_merge, dk=dk_code, axis=1)

        return self.df_data



    def convert_percentage(self, lst_qres: list[str], fil_nan: float, is_check_sum: bool) -> (pd.DataFrame, pd.DataFrame):
        """
        :param lst_qres: MA likes 'Q1|8'
        :param fil_nan: fill nan value with float
        :param is_check_sum: check sum for share question (these should be 100%)
        :return: df_data, df_info
        """

        df_check_sum = self.df_data['ID']

        for qre in lst_qres:
            self.print(f"Convert percentage: {qre}")
            lst_qre = self.convert_ma_pattern(qre) if '|' in qre else [qre]

            self.df_info.loc[self.df_info.eval("var_name.isin(@lst_qre)"), 'var_type'] = 'NUM'
            self.df_data[lst_qre] = self.df_data[lst_qre].replace(' %', '', regex=True).astype(float)

            if fil_nan is not None:
                self.df_data[lst_qre] = self.df_data[lst_qre].fillna(fil_nan)

            if is_check_sum:
                df_check_sum = pd.concat([df_check_sum, self.df_data[lst_qre].sum(axis=1)], axis=1)
                df_check_sum.rename(columns={0: f'{qre.rsplit('|', 1)[0]}_Sum'}, inplace=True)


        if is_check_sum:
            df_check_sum = df_check_sum.melt(id_vars=['ID']).query("value != 100")

            if not df_check_sum.empty:
                df_check_sum.to_csv('df_check_sum.csv')
                self.print(f"Please check the percentage of ID: \n{df_check_sum} \n saved with 'df_check_sum.csv'", self.clr_err)

        return self.df_data, self.df_info



    @staticmethod
    def convert_ma_pattern(str_ma: str) -> list:
        ma_prefix, ma_suffix = str_ma.rsplit('|', 1)
        return [f'{ma_prefix}_{i}' for i in range(1, int(ma_suffix) + 1)]



    @staticmethod
    def update_append_remove(row, method, lst_val_update) -> pd.Series:

        max_len = row.shape[0]
        lst_val = list()

        match method:

            case 'a':
                lst_val = row.dropna().values.tolist()
                lst_val.extend(lst_val_update)
                lst_val = list(dict.fromkeys(lst_val))

            case 'r':
                update_row = row.replace(lst_val_update, np.nan)
                lst_val = update_row.dropna().values.tolist()


        if len(lst_val) != max_len:
            lst_val = lst_val + [np.nan] * (max_len - len(lst_val))

        update_row = pd.Series(index=row.index, data=lst_val)

        return update_row



    def update_qres_data(self, *, query_fil: str, qre_name: str, lst_val_update: list[int | float], method: str) -> pd.DataFrame:
        """
        :param query_fil:
        :param qre_name: MA likes 'Q1|8'
        :param lst_val_update: list[int | float]
        :param method: 'a' = append, 'r' = remove, 'o' = overlay
        :return: df_data
        """

        lst_qre_update = self.convert_ma_pattern(qre_name) if '|' in qre_name else [qre_name]

        match method:

            case 'a' | 'r':
                self.df_data.loc[self.df_data.eval(query_fil), lst_qre_update] = self.df_data.loc[self.df_data.eval(query_fil), lst_qre_update].apply(self.update_append_remove, method=method, lst_val_update=lst_val_update, axis=1)

            case 'o':

                if len(lst_qre_update) != len(lst_val_update):
                    self.print("Length of update columns must equal update values!!!!", self.clr_err)
                    return pd.DataFrame()

                else:
                    self.df_data.loc[self.df_data.eval(query_fil), lst_qre_update] = lst_val_update

            case _:
                self.print(f'Please check param method - {method}', self.clr_err)
                return pd.DataFrame()

        return self.df_data



    def create_count_ma_ranking(self, *, act: str, lst_qre: list) -> (dict, dict):

        dict_add_new_qres = dict()
        dict_data_new_qres = dict()

        def re_ranking(row, ranking_range: int):

            lst_result = [np.nan] * ranking_range

            df = row.to_frame(name='val')
            df['score'] = list(range(1, df.shape[0] + 1)[::-1])

            for k, v in df.set_index('val', drop=True).to_dict()['score'].items():
                lst_result[k - 1] = v

            return lst_result


        for qre in lst_qre:

            match act.upper():

                case 'MA':
                    lst_col_qre = self.df_info.loc[self.df_info.eval(f"var_name.str.contains(r'^{qre}_[\\d]{{1,2}}$') & var_type.isin(['MA', 'MA_mtr'])"), 'var_name'].values.tolist()

                    if not len(lst_col_qre):
                        self.print(f"{qre} is not {act.upper()} questions!!!", self.clr_err)
                        continue

                    new_num_qre = f'{qre}_Count'
                    dict_add_new_qres.update({new_num_qre: [new_num_qre, 'NUM', {}, np.nan]})
                    dict_data_new_qres.update({new_num_qre: self.df_data[lst_col_qre].count(axis=1).values.tolist()})

                case 'RANKING':
                    lst_col_qre = self.df_info.loc[self.df_info.eval(f"var_name.str.contains(r'^{qre}_Rank[\\d]{{1,2}}$') & var_type.isin(['RANKING'])"), 'var_name'].values.tolist()

                    if not len(lst_col_qre):
                        self.print(f"{qre} is not {act.upper()} questions!!!", self.clr_err)
                        continue

                    dict_codelist = self.df_info.loc[self.df_info.eval("var_name == @lst_col_qre[0]"), 'val_lbl'].values[0]
                    new_num_qre = f'{qre}_ScoreOfAtt'
                    dict_add_new_qres.update(
                        {f"{new_num_qre}_{k}": [f"{k}. {v}", 'NUM', {}, np.nan] for k, v in dict_codelist.items()}
                    )

                    df_ranking: pd.DataFrame = self.df_data[lst_col_qre].apply(re_ranking, ranking_range=len(list(dict_add_new_qres.keys())), axis=1, result_type='expand')
                    df_ranking.columns = list(dict_add_new_qres.keys())
                    dict_data_new_qres = {k: list(v.values()) for k, v in df_ranking.to_dict().items()}

                case _:
                    self.print(f"{act} is not in [MA, RANKING]!!!", self.clr_err)
                    continue


        return dict_add_new_qres, dict_data_new_qres



    def count_ma_choice(self, *, lst_ma_qre: list, dict_replace: dict = None) -> (pd.DataFrame, pd.DataFrame):

        dict_add_new_qres, dict_data_new_qres = self.create_count_ma_ranking(act='MA', lst_qre=lst_ma_qre)

        self.add_qres(dict_add_new_qres)
        self.df_data[list(dict_data_new_qres.keys())] = pd.DataFrame.from_dict(dict_data_new_qres).replace(dict_replace) if dict_replace else pd.DataFrame.from_dict(dict_data_new_qres)

        return self.df_data, self.df_info



    def calculate_ranking_score(self, *, lst_ranking_qre: list) -> (pd.DataFrame, pd.DataFrame):

        dict_add_new_qres, dict_data_new_qres = self.create_count_ma_ranking(act='RANKING', lst_qre=lst_ranking_qre)

        self.add_qres(dict_add_new_qres)
        self.df_data[list(dict_data_new_qres.keys())] = pd.DataFrame.from_dict(dict_data_new_qres)

        return self.df_data, self.df_info





    # @staticmethod
    # def concept_evaluate(cpt_filename: str, ) -> (pd.DataFrame, dict):
    #     # Here: May 16
    #     # 1. clean inputted concept
    #     # 2. create codeframe for each word for concept
    #     # 3. match verbatim to concept codeframe
    #     # 4. return dataframe with codes of the words in concept
    #
    #     return pd.DataFrame(), dict()  # dataframe & codelíst




