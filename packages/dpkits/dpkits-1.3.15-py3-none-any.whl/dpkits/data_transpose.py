import pandas as pd
from colorama import Fore


class DataTranspose:

    @staticmethod
    def to_stack(df_data: pd.DataFrame, df_info: pd.DataFrame, dict_data_structure: dict) -> (pd.DataFrame, pd.DataFrame):

        """
        :param df_data: dataframe
        :param df_info: dataframe
        :param dict_data_structure: dict = {
            'id_col': str,
            'sp_col': str,
            'lst_scr': list,
            'dict_sp': dict = {
                1: {
                    'Ma_SP1': 'Ma_SP',
                    'Q1_SP1': 'Q1',
                    'Q2_SP1': 'Q2',
                    'Q3_SP1': 'Q3',
                },
                2: {
                    'Ma_SP2': 'Ma_SP',
                    'Q1_SP2': 'Q1',
                    'Q2_SP2': 'Q2',
                    'Q3_SP2': 'Q3',
                 },
            },
            'lst_fc': list
        }
        :return: df_data_stack, df_info_stack both as dataframe type
        """
        
        id_col = dict_data_structure['id_col']
        sp_col = dict_data_structure['sp_col']
        lst_scr = dict_data_structure['lst_scr']
        dict_sp = dict_data_structure['dict_sp']
        lst_fc = dict_data_structure['lst_fc']

        # check duplicate in id col
        df_dup_id = df_data.loc[df_data.duplicated(subset=id_col), [id_col]].copy()
        df_dup_id[id_col] = df_dup_id[id_col].astype(str)

        if not df_dup_id.empty:
            print(Fore.RED, f"Please check {df_dup_id.shape[0]} duplicated ID:\n{'\n'.join(df_dup_id[id_col].values.tolist())}", Fore.RESET)
            exit()

        # df_data_stack generate
        df_data_scr = df_data.loc[:, [id_col] + lst_scr].copy()

        df_data_df = pd.DataFrame()
        if lst_fc:
            df_data_df = df_data.loc[:, [id_col] + lst_fc].copy()

        lst_df_data_sp = [df_data.loc[:, [id_col] + list(val.keys())].copy() for val in dict_sp.values()]

        for i, df in enumerate(lst_df_data_sp):
            df.rename(columns=dict_sp[i + 1], inplace=True)

        df_data_stack = pd.concat(lst_df_data_sp, axis=0, ignore_index=True)

        df_data_stack = df_data_scr.merge(df_data_stack, how='left', on=[id_col])

        if lst_fc:
            df_data_stack = df_data_stack.merge(df_data_df, how='left', on=[id_col])

        df_data_stack.reset_index(drop=True, inplace=True)

        df_data_stack.sort_values(by=[id_col, sp_col], inplace=True)
        df_data_stack.reset_index(drop=True, inplace=True)

        df_info_stack = df_info.copy()

        for key, val in dict_sp[1].items():
            df_info_stack.loc[df_info_stack['var_name'] == key, ['var_name']] = [val]

        df_info_stack.drop_duplicates(subset=['var_name'], keep='first', inplace=True)

        # Reset df_info_stack index
        df_info_stack['idx_var_name'] = df_info_stack['var_name']
        df_info_stack.set_index('idx_var_name', inplace=True)
        df_info_stack = df_info_stack.loc[list(df_data_stack.columns), :]
        df_info_stack.reindex(list(df_data_stack.columns))
        df_info_stack.reset_index(drop=True, inplace=True)

        return df_data_stack, df_info_stack



    @staticmethod
    def to_unstack(df_data_stack: pd.DataFrame, df_info_stack: pd.DataFrame, dict_unstack_structure: dict) -> (pd.DataFrame, pd.DataFrame):

        """
        :param df_data_stack: dataframe
        :param df_info_stack: dataframe
        :param dict_unstack_structure: dict = {
            'id_col': str,
            'sp_col': str,
            'lst_col_part_head': list,
            'lst_col_part_body': list,
            'lst_col_part_tail': list
        }
        :return: df_data_unstack, df_info_unstack both as dataframe type
        """

        id_col = dict_unstack_structure['id_col']
        sp_col = dict_unstack_structure['sp_col']

        dict_sp_val = df_info_stack.query(f"var_name == '{sp_col}'")['val_lbl'].values[0]

        df_part_head = df_data_stack.query(f"{sp_col} == {list(dict_sp_val.keys())[0]}")[[id_col] + dict_unstack_structure['lst_col_part_head']].copy()
        df_part_tail = df_data_stack.query(f"{sp_col} == {list(dict_sp_val.keys())[0]}")[[id_col] + dict_unstack_structure['lst_col_part_tail']].copy()

        df_part_body = pd.DataFrame()
        df_info_part_body = pd.DataFrame()

        dict_sort_col = dict()
        for k, v in dict_sp_val.items():

            sp_lbl = str(v).replace(' ', '_')

            df_info_by_k = df_info_stack.query(f"var_name.isin({dict_unstack_structure['lst_col_part_body']})").copy()
            df_data_by_k = df_data_stack.query(f"{sp_col} == {k}")[[id_col] + dict_unstack_structure['lst_col_part_body']].copy()

            dict_rename_col = dict()
            dict_rename_var_lbl = dict()
            for idx in df_info_by_k.index:

                var_name = df_info_by_k.at[idx, 'var_name']
                var_lbl = df_info_by_k.at[idx, 'var_lbl']
                var_type = df_info_by_k.at[idx, 'var_type']

                str_ma_name = str()

                if var_type in ['MA']:
                    str_ma_name, str_ma_cat = var_name.rsplit('_', 1)
                    str_var_name_new = f"{str_ma_name}_{sp_lbl}_{str_ma_cat}"
                else:
                    str_var_name_new = f"{var_name}_{sp_lbl}"

                dict_rename_col.update({var_name: str_var_name_new})
                dict_rename_var_lbl.update({var_lbl: f"{var_lbl}_{sp_lbl}"})

                if var_type in ['MA']:
                    if str_ma_name in dict_sort_col.keys():
                        dict_sort_col[str_ma_name].append(str_var_name_new)
                    else:
                        dict_sort_col.update({str_ma_name: [str_var_name_new]})
                else:
                    if var_name in dict_sort_col.keys():
                        dict_sort_col[var_name].append(str_var_name_new)
                    else:
                        dict_sort_col.update({var_name: [str_var_name_new]})

            df_data_by_k.rename(columns=dict_rename_col, inplace=True)
            # df_info_by_k['var_name'].replace(dict_rename_col, inplace=True)
            # df_info_by_k['var_lbl'].replace(dict_rename_var_lbl, inplace=True)
            df_info_by_k.replace({'var_name': dict_rename_col}, inplace=True)
            df_info_by_k.replace({'var_lbl': dict_rename_var_lbl}, inplace=True)

            if df_part_body.empty:
                df_part_body = df_data_by_k.copy()
                df_info_part_body = df_info_by_k.copy()
            else:
                df_part_body = df_part_body.merge(df_data_by_k, how='left', on=id_col)
                df_info_part_body = pd.concat([df_info_part_body, df_info_by_k], ignore_index=True)

        # Need to sort vars
        lst_sort_col = list()
        for v in dict_sort_col.values():
            lst_sort_col.extend(v)

        df_part_body = df_part_body.reindex(columns=[id_col] + lst_sort_col)

        df_info_part_body['idx_by_var_name'] = df_info_part_body['var_name']
        df_info_part_body.set_index('idx_by_var_name', inplace=True)
        df_info_part_body = df_info_part_body.reindex(lst_sort_col)
        df_info_part_body.reset_index(drop=True, inplace=True)
        # Need to sort vars

        df_data_unstack = df_part_head.copy()
        df_data_unstack = df_data_unstack.merge(df_part_body, how='left', on=id_col)
        df_data_unstack = df_data_unstack.merge(df_part_tail, how='left', on=id_col)

        df_info_unstack = df_info_stack.query(
            f"var_name.isin({[id_col] + dict_unstack_structure['lst_col_part_head']})").copy()
        df_info_unstack = pd.concat([df_info_unstack, df_info_part_body], ignore_index=True)
        df_info_unstack = pd.concat([df_info_unstack, df_info_stack.query(
            f"var_name.isin({dict_unstack_structure['lst_col_part_tail']})").copy()], ignore_index=True)

        df_data_unstack.reset_index(drop=True, inplace=True)
        df_info_unstack.reset_index(drop=True, inplace=True)

        return df_data_unstack, df_info_unstack