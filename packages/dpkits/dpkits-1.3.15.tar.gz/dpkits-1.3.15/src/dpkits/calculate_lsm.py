import pandas as pd
import numpy as np


class LSMCalculation:

    @staticmethod
    def cal_lsm_6(df_data_output: pd.DataFrame, df_qres_info_output: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):

        lst_addin = ['CC1_Score', 'CC2_Score', 'CC3_Score', 'CC4_Score', 'CC5_Score', 'CC6_Score', 'LSM_Score', 'LSM']

        df_data_output.loc[:, lst_addin] = [[np.nan] * len(lst_addin)] * df_data_output.shape[0]

        df_data_output['CC1_Score'] = df_data_output['CC1']
        df_data_output['CC1_Score'].replace({1: 1, 2: 1, 3: 1, 4: 1, 5: 3, 6: 3, 7: 4, 8: 4, 9: 5, 10: 5, 11: 5, 12: 5}, inplace=True)

        lst_cc2 = [f'CC2_{i}' for i in range(1, 11)]
        df_data_output['CC2_Score'] = df_data_output.loc[:, lst_cc2].sum(axis=1, numeric_only=True)
        df_data_output['CC2_Score'].replace({1: 2, 2: 2, 3: 3, 4: 3, 5: 4, 6: 4, 7: 5, 8: 6, 9: 7, 10: 8, 11: 8}, inplace=True)
        df_data_output.loc[df_data_output['CC2_Score'] >= 12, ['CC2_Score']] = [9]

        lst_cc3 = [f'CC3_{i}' for i in range(1, 8)]
        df_cc3_score = df_data_output.loc[:, lst_cc3].copy()
        df_cc3_score.replace({1: 9, 2: 4, 3: 4, 4: 4, 5: 5, 6: 0, 7: -3}, inplace=True)
        df_data_output['CC3_Score'] = df_cc3_score.sum(axis=1, numeric_only=True)

        lst_cc4 = [f'CC4_{i}' for i in range(1, 25)]
        df_cc4_score = df_data_output.loc[:, lst_cc4].copy()
        df_cc4_score.replace({1: 4, 2: 3, 3: -3, 4: 1, 5: 3, 6: 4, 7: 2, 8: 3, 9: 2, 10: 4, 11: 3, 12: 4, 13: 4, 14: 3, 15: 2, 16: 2, 17: 3, 18: 3, 19: 4, 20: 3, 21: 3, 22: 3, 23: 5, 24: 5, 25: 4}, inplace=True)
        df_data_output['CC4_Score'] = df_cc4_score.sum(axis=1, numeric_only=True)

        dict_cc5_score = {
            'CC5_1': [['qre == 0', 1000], ['qre == 1', 1003], ['qre == 2', 1005], ['qre == 3', 1006], ['qre == 4', 1006], ['((qre >= 5) & (qre < 1000))', 1006]],
            'CC5_2': [['qre == 0', 1000], ['qre == 1', 1000], ['qre == 2', 1002], ['qre == 3', 1003], ['qre == 4', 1004], ['((qre >= 5) & (qre < 1000))', 1005]],
            'CC5_3': [['qre == 0', 1000], ['qre == 1', 1001], ['qre == 2', 1004], ['qre == 3', 1005], ['qre == 4', 1005], ['((qre >= 5) & (qre < 1000))', 1005]],
            'CC5_4': [['qre == 0', 1000], ['qre == 1', 1003], ['qre == 2', 1005], ['qre == 3', 1007], ['qre == 4', 1007], ['((qre >= 5) & (qre < 1000))', 1007]],
            'CC5_5': [['qre == 0', 1000], ['qre == 1', 1004], ['qre == 2', 1008], ['qre == 3', 1008], ['qre == 4', 1008], ['((qre >= 5) & (qre < 1000))', 1008]],
            'CC5_6': [['qre == 0', 1000], ['qre == 1', 1004], ['qre == 2', 1007], ['qre == 3', 1007], ['qre == 4', 1007], ['((qre >= 5) & (qre < 1000))', 1007]],
            'CC5_7': [['qre == 0', 1000], ['qre == 1', 1002], ['qre == 2', 1005], ['qre == 3', 1005], ['qre == 4', 1005], ['((qre >= 5) & (qre < 1000))', 1005]],
            'CC5_8': [['qre == 0', 1000], ['qre == 1', 1004], ['qre == 2', 1007], ['qre == 3', 1007], ['qre == 4', 1007], ['((qre >= 5) & (qre < 1000))', 1007]],
            'CC5_9': [['qre == 0', 1000], ['qre == 1', 1004], ['qre == 2', 1008], ['qre == 3', 1008], ['qre == 4', 1008], ['((qre >= 5) & (qre < 1000))', 1008]],
            'CC5_10': [['qre == 0', 1000], ['qre == 1', 1004], ['qre == 2', 1009], ['qre == 3', 1009], ['qre == 4', 1009], ['((qre >= 5) & (qre < 1000))', 1009]],
            'CC5_11': [['qre == 0', 1000], ['qre == 1', 1003], ['qre == 2', 1005], ['qre == 3', 1005], ['qre == 4', 1005], ['((qre >= 5) & (qre < 1000))', 1005]],
            'CC5_12': [['qre == 0', 1000], ['qre == 1', 1003], ['qre == 2', 1005], ['qre == 3', 1006], ['qre == 4', 1006], ['((qre >= 5) & (qre < 1000))', 1006]],
            'CC5_13': [['qre == 0', 1000], ['qre == 1', 1000], ['qre == 2', 1001], ['qre == 3', 1002], ['qre == 4', 1003], ['((qre >= 5) & (qre < 1000))', 1004]],
            'CC5_14': [['qre == 0', 1000], ['qre == 1', 1002], ['qre == 2', 1003], ['qre == 3', 1004], ['qre == 4', 1004], ['((qre >= 5) & (qre < 1000))', 1004]],
            'CC5_15': [['qre == 0', 1000], ['qre == 1', 1003], ['qre == 2', 1005], ['qre == 3', 1005], ['qre == 4', 1005], ['((qre >= 5) & (qre < 1000))', 1005]],
            'CC5_16': [['qre == 0', 1000], ['qre == 1', 1000], ['qre == 2', 1000], ['qre == 3', 1000], ['qre == 4', 1000], ['((qre >= 5) & (qre < 1000))', 1000]],
            'CC5_17': [],
            'CC5_18': [],
        }

        df_cc5_score = df_data_output.loc[:, list(dict_cc5_score.keys())].copy()
        df_cc5_score = df_cc5_score.replace(to_replace=r'[^0-9.]*', value=0, regex=True)

        for key, val in dict_cc5_score.items():
            if val:
                for pair in val:
                    if not df_cc5_score.query(pair[0].replace("qre", key)).empty:
                        qre_rep = pair[0].replace("qre", f"df_cc5_score['{key}']")
                        str_re_score = f"df_cc5_score.loc[{qre_rep}, ['{key}']] = [{pair[1]}]"
                        exec(str_re_score)

        df_cc5_score['CC5_17_18'] = [0] * df_cc5_score.shape[0]

        for idx in df_cc5_score.index:

            if df_cc5_score.at[idx, 'CC5_18'] >= 1 and df_cc5_score.at[idx, 'CC5_17'] + df_cc5_score.at[idx, 'CC5_18'] >= 2:
                df_cc5_score.at[idx, 'CC5_17_18'] = 1006

            elif df_cc5_score.at[idx, 'CC5_18'] == 1 or (df_cc5_score.at[idx, 'CC5_17'] >= 2 and df_cc5_score.at[idx, 'CC5_18'] == 0):
                df_cc5_score.at[idx, 'CC5_17_18'] = 1004

            elif df_cc5_score.at[idx, 'CC5_18'] == 0 and df_cc5_score.at[idx, 'CC5_17'] == 1:
                df_cc5_score.at[idx, 'CC5_17_18'] = 1002

            else:
                df_cc5_score.at[idx, 'CC5_17_18'] = 1000

        df_cc5_score.drop(['CC5_17', 'CC5_18'], inplace=True, axis=1)
        df_data_output['CC5_Score'] = df_cc5_score.sum(axis=1, numeric_only=True) - (len(list(df_cc5_score.columns)) * 1000)

        # lst_cc6 = [f'CC6']
        lst_cc6 = [f'CC6_{i}' for i in range(1, 11)]
        df_cc6_score = df_data_output.loc[:, lst_cc6].copy()
        df_cc6_score.replace({1: 5, 2: 0, 3: 6, 4: 0, 5: 6, 6: 15, 7: 10, 8: 5, 9: 0, 10: 0}, inplace=True)
        df_data_output['CC6_Score'] = df_cc6_score.sum(axis=1, numeric_only=True)


        df_lsm_score = df_data_output.loc[:, ['CC1_Score', 'CC2_Score', 'CC3_Score', 'CC4_Score', 'CC5_Score', 'CC6_Score']].copy()
        df_lsm_score['LSM_Score'] = df_lsm_score.sum(axis=1, numeric_only=True) * 10
        df_lsm_score['LSM'] = [np.nan] * df_lsm_score.shape[0]

        for idx in df_lsm_score.index:
            int_score = df_lsm_score.at[idx, 'LSM_Score']

            if 1 <= int_score <= 75:
                df_lsm_score.at[idx, 'LSM'] = 0
            elif 76 <= int_score <= 130:
                df_lsm_score.at[idx, 'LSM'] = 1
            elif 131 <= int_score <= 175:
                df_lsm_score.at[idx, 'LSM'] = 2
            elif 176 <= int_score <= 215:
                df_lsm_score.at[idx, 'LSM'] = 3
            elif 216 <= int_score <= 260:
                df_lsm_score.at[idx, 'LSM'] = 4
            elif 261 <= int_score <= 305:
                df_lsm_score.at[idx, 'LSM'] = 5
            elif 306 <= int_score <= 350:
                df_lsm_score.at[idx, 'LSM'] = 6
            elif 351 <= int_score <= 400:
                df_lsm_score.at[idx, 'LSM'] = 7
            elif 401 <= int_score <= 455:
                df_lsm_score.at[idx, 'LSM'] = 8
            elif 456 <= int_score <= 520:
                df_lsm_score.at[idx, 'LSM'] = 9
            elif 521 <= int_score <= 595:
                df_lsm_score.at[idx, 'LSM'] = 10
            elif 596 <= int_score <= 675:
                df_lsm_score.at[idx, 'LSM'] = 11
            elif 676 <= int_score <= 770:
                df_lsm_score.at[idx, 'LSM'] = 12
            elif 771 <= int_score <= 875:
                df_lsm_score.at[idx, 'LSM'] = 13
            elif 876 <= int_score <= 990:
                df_lsm_score.at[idx, 'LSM'] = 14
            elif 991 <= int_score <= 1125:
                df_lsm_score.at[idx, 'LSM'] = 15
            elif 1126 <= int_score <= 1275:
                df_lsm_score.at[idx, 'LSM'] = 16
            elif 1276 <= int_score <= 1445:
                df_lsm_score.at[idx, 'LSM'] = 17
            elif 1446 <= int_score <= 1850:
                df_lsm_score.at[idx, 'LSM'] = 18
            elif int_score >= 1851:
                df_lsm_score.at[idx, 'LSM'] = 19
            else:
                df_lsm_score.at[idx, 'LSM'] = np.nan

        df_data_output['LSM_Score'] = df_lsm_score['LSM_Score']
        df_data_output['LSM'] = df_lsm_score['LSM']

        df_qres_info_output = pd.concat([df_qres_info_output,
                                         pd.DataFrame(
                                             columns=['var_name', 'var_lbl', 'var_type', 'val_lbl'],
                                             data=[
                                                 ['CC1_Score', 'CC1_Score', 'NUM', {}],
                                                 ['CC2_Score', 'CC2_Score', 'NUM', {}],
                                                 ['CC3_Score', 'CC3_Score', 'NUM', {}],
                                                 ['CC4_Score', 'CC4_Score', 'NUM', {}],
                                                 ['CC5_Score', 'CC5_Score', 'NUM', {}],
                                                 ['CC6_Score', 'CC6_Score', 'NUM', {}],
                                                 ['LSM_Score', 'LSM_Score', 'NUM', {}],
                                                 ['LSM', 'LSM', 'NUM', {}],
                                             ])],
                                        axis=0)

        df_data_output.reset_index(drop=True, inplace=True)
        df_qres_info_output.reset_index(drop=True, inplace=True)

        return df_data_output, df_qres_info_output
