import numpy
import pandas as pd
import numpy as np
from colorama import Fore



class CodeframeReader:

    def __init__(self, cf_file_name: str):
        self.cf_file_name = cf_file_name

        self.dict_add_new_qres_oe = dict()
        self.df_full_oe_coding = pd.DataFrame


    def to_dataframe_file(self):

        file_name = self.cf_file_name
        output_file_name = f'{file_name}_output.xlsx'

        print(Fore.BLUE, f"\nREAD '{file_name}' -> CREATE '{output_file_name}' -> RUN OE\n", Fore.RESET)

        dict_df_ws = pd.read_excel(file_name, sheet_name=None, header=None)
        dict_df_coding = dict()
        dict_df_codelist = dict()

        df_rid = pd.DataFrame(data=[], columns=['RESPONDENTID'])
        for ws_name, df_ws in dict_df_ws.items():

            if ws_name in ['RAWDATA', 'DATABASE', 'VERBATIM']:
                continue

            if '-CODE' in ws_name:
                df_ws.columns = df_ws.iloc[1].tolist()
                df_ws = df_ws.query("index >= 2").copy()
                df_ws.reset_index(drop=True, inplace=True)
                df_rid = pd.concat([df_rid, df_ws.loc[:, ['RESPONDENTID']]], axis=0)
                dict_df_coding.update({ws_name: df_ws})
            else:
                qre_lbl = df_ws.at[0, 1]
                df_ws.columns = df_ws.iloc[2].tolist()
                df_ws = df_ws.query("index >= 3 & RECODE.isnull()").copy()
                df_ws.drop(columns=['RECODE', 'LABEL ENG'], inplace=True)
                df_ws.reset_index(drop=True, inplace=True)

                dict_df_codelist.update({
                    ws_name: {
                        'qre_lbl': qre_lbl,
                        'df_colname': pd.DataFrame(),
                        'df_codelist': df_ws
                    }
                })


        print('EXPORT CODING FILE')
        df_rid.drop_duplicates(subset=['RESPONDENTID'], inplace=True)

        try:
            df_rid.sort_values(by=['RESPONDENTID'], inplace=True)
        except TypeError:
            pass

        lst_rid = df_rid['RESPONDENTID'].values.tolist()

        lst_ws_col = ['Unnamed: 0', 'RESPONDENTID', 'COLUMN_NAME', 'VERBATIM', 'CODING', 'FW_CHECK']

        df_full_oe = pd.DataFrame()

        for ws_name, df_ws in dict_df_coding.items():

            print(ws_name)

            df_ws.rename(columns={'COLUMN NAME': 'COLUMN_NAME', 'FW CHECK': 'FW_CHECK'}, inplace=True)

            lst_qre_comb = list(dict.fromkeys([a.replace('Y1_', 'Y1|').replace('Y2_', 'Y2|').rsplit('|', 1)[0] for a in df_ws['COLUMN_NAME'].values.tolist()]))

            df_ws['RESPONDENTID'] = df_ws['RESPONDENTID'].astype(str)
            df_ws['VERBATIM'] = df_ws['VERBATIM'].astype(str)
            df_ws['CODING'] = df_ws['CODING'].astype(str)

            df_ws_new = pd.DataFrame(columns=lst_ws_col, data=[])
            for rid in lst_rid:
                for qre in lst_qre_comb:

                    df_fil = df_ws.query(f"RESPONDENTID.str.contains('{rid}') & COLUMN_NAME.str.contains('{qre}')")

                    verbatim = '|'.join(df_fil['VERBATIM'].values.tolist())
                    coding = '\\'.join(df_fil['CODING'].values.tolist())
                    lst_coding = list(dict.fromkeys(coding.split('\\')))

                    if lst_coding[0] == '' and 'THICHHON' not in str(ws_name).upper() and 'THICH_HON' not in str(ws_name).upper():
                        lst_coding[0] = '99999'

                    if len(lst_coding) > 1 and '99999' in lst_coding:
                        lst_coding.remove('99999')

                    df_check = df_ws_new.query(f"RESPONDENTID == '{rid}' & COLUMN_NAME == '{qre}'")

                    if not df_check.empty:
                        df_ws_new.loc[((df_ws_new['RESPONDENTID'] == rid) & (df_ws_new['COLUMN_NAME'] == qre)), :] = [f"{rid}@_@{qre}", rid, qre, verbatim, lst_coding, np.nan]
                    else:
                        df_ws_new = pd.concat([df_ws_new, pd.DataFrame(
                            columns=lst_ws_col,
                            data=[[f"{rid}@_@{qre}", rid, qre, verbatim, lst_coding, np.nan]])], axis=0)


            df_ws_new['VERBATIM'].replace({'': 'NONE'}, inplace=True)

            df_ws_new.reset_index(drop=True, inplace=True)

            for rid in lst_rid:
                df_fil = df_ws_new.query(f"RESPONDENTID == '{rid}' & COLUMN_NAME.isin({lst_qre_comb})")
                qre_total_name = lst_qre_comb[0].replace('_Y1', '_Total')

                if not df_fil['VERBATIM'].values.tolist():
                    continue

                verbatim = '|'.join(df_fil['VERBATIM'].values.tolist())

                lst_coding = list()
                for item in df_fil['CODING'].values.tolist():
                    lst_coding.extend(item)

                lst_coding = list(dict.fromkeys(lst_coding))

                if len(lst_coding) > 1 and '99999' in lst_coding:
                    lst_coding.remove('99999')

                lst_total_row = [f"{rid}@_@{qre_total_name}", rid, qre_total_name, verbatim, lst_coding, np.nan]

                df_ws_new = pd.concat([df_ws_new, pd.DataFrame(columns=lst_ws_col, data=[lst_total_row])], axis=0)

            df_ws_new.sort_values(by=['RESPONDENTID', 'COLUMN_NAME'], inplace=True)
            df_ws_new.reset_index(drop=True, inplace=True)

            df_ws_new['CODING_LEN'] = [len(a) for a in df_ws_new['CODING']]
            df_ws_new['CODING'] = ['\\'.join(a) for a in df_ws_new['CODING']]
            max_len = df_ws_new['CODING_LEN'].max()
            arr_max_len = [a for a in range(1, max_len + 1)]

            df_ws_new[arr_max_len] = df_ws_new['CODING'].str.split('\\', expand=True)

            df_ws_new = pd.melt(df_ws_new, id_vars=['RESPONDENTID', 'COLUMN_NAME'], value_vars=arr_max_len)
            df_ws_new.sort_values(by=['RESPONDENTID', 'COLUMN_NAME'], inplace=True)
            df_ws_new.reset_index(drop=True, inplace=True)

            # df_ws_new['value'].replace({None: np.nan}, inplace=True)
            df_ws_new = df_ws_new.loc[df_ws_new.eval("value != ''"), :].copy()
            df_ws_new['value'] = df_ws_new['value'].astype(float)

            df_ws_new['COLUMN_NAME'] = [f"{a1}_OE_{a2}" for a1, a2 in zip(df_ws_new['COLUMN_NAME'], df_ws_new['variable'])]

            lst_qre_name = df_ws_new['COLUMN_NAME'].copy().drop_duplicates(keep='first').values.tolist()

            df_ws_new.drop_duplicates(subset=['RESPONDENTID', 'COLUMN_NAME', 'variable'], inplace=True)

            df_ws_new = df_ws_new.set_index(['RESPONDENTID', 'COLUMN_NAME'])['value'].unstack().reset_index()

            df_ws_new = df_ws_new.reindex(columns=['RESPONDENTID'] + lst_qre_name)

            print(f'ADD columns to dict_df_codelist[{ws_name.replace("-CODE", "")}]')
            lst_qre = list(df_ws_new.columns)
            lst_qre.remove('RESPONDENTID')
            df_colname = pd.DataFrame(columns=['COL_NAME'], data=lst_qre)
            df_colname[['COL_NAME', 'stt']] = df_colname['COL_NAME'].str.rsplit('_', n=1, expand=True)
            df_colname.drop_duplicates(subset=['COL_NAME'], keep='last', inplace=True)
            df_colname['COL_NAME'] = df_colname['COL_NAME'] + '|' + df_colname['stt'].astype(str)
            df_colname.drop(columns='stt', inplace=True)
            df_colname.reset_index(drop=True, inplace=True)
            df_colname = pd.concat([df_colname, pd.DataFrame(columns=['SEC', 'LABEL', 'TYPE', 'CODELIST'], data=[['PRODUCT|FORCE_CHOICE|NORMAL_OE', '', 'MA', {}]] * df_colname.shape[0])], axis=1)
            df_colname['LABEL'] = dict_df_codelist[ws_name.replace('-CODE', '')]['qre_lbl']
            dict_df_codelist[ws_name.replace('-CODE', '')].update({'df_colname': df_colname})

            if df_full_oe.empty:
                df_full_oe = df_ws_new.copy()
            else:
                df_full_oe = df_full_oe.merge(df_ws_new, how='left', on='RESPONDENTID')


        # df_full_oe.to_csv(f"{file_name}_CODING.csv", index=False)

        print('EXPORT CODELIST FILE')
        df_full_codelist = pd.DataFrame()
        for ws_name, val in dict_df_codelist.items():
            print(ws_name)
            dict_codelist = dict()
            net_count = 900001
            df_codelist = val['df_codelist']
            cur_net_key = str()
            for idx in df_codelist.index:
                code = df_codelist.at[idx, 'CODE']
                label = df_codelist.at[idx, 'LABEL VNI']

                if pd.isnull(df_codelist.at[idx, 'CODE']):
                    notes = df_codelist.at[idx, 'NOTES']
                    cur_net_key = f"{net_count}|{notes}|{label}"
                    dict_codelist.update({cur_net_key: {}})
                    net_count += 1
                else:
                    if cur_net_key:
                        dict_codelist[cur_net_key].update({str(int(code)): label})
                    else:
                        dict_codelist.update({str(int(code)): label})

            df_colname = val['df_colname']
            df_colname['CODELIST'] = [{'net_code': dict_codelist}] * df_colname.shape[0]

            if df_full_codelist.empty:
                df_full_codelist = df_colname.copy()
            else:
                df_full_codelist = pd.concat([df_full_codelist, df_colname], axis=0)

        df_full_codelist.reset_index(drop=True, inplace=True)
        # df_full_codelist.to_csv(f"{file_name}_CODELIST.csv", index=False, encoding='utf-8-sig')

        df_full_codelist.drop(columns=['SEC'], inplace=True)

        with pd.ExcelWriter(output_file_name, engine="openpyxl") as writer:
            df_full_codelist.to_excel(writer, sheet_name='codelist')
            df_full_oe.to_excel(writer, sheet_name='coding')

        df_full_codelist.set_index('COL_NAME', drop=True, inplace=True)
        df_full_codelist.loc[:, 'VALUES'] = np.nan

        dict_add_new_qres_oe = df_full_codelist.to_dict('index')

        for k, v in dict_add_new_qres_oe.items():
            self.dict_add_new_qres_oe.update({k: list(v.values())})

        self.df_full_oe_coding = df_full_oe

        print('\n')



    def read_dataframe_output_file(self):

        output_file_name = f'{self.cf_file_name}_output.xlsx'

        print(Fore.BLUE, f"\nREAD '{output_file_name}' -> RUN OE\n", Fore.RESET)

        df_codelist = pd.read_excel(output_file_name, sheet_name='codelist', index_col=0)
        df_codelist.set_index('COL_NAME', inplace=True)
        df_codelist.loc[:, 'VALUES'] = np.nan

        dict_add_new_qres_oe = dict()
        for k, v in df_codelist.to_dict(orient='index').items():
            v['CODELIST'] = eval(v['CODELIST'])

            dict_add_new_qres_oe.update({k: list(v.values())})

        self.df_full_oe_coding = pd.read_excel(output_file_name, sheet_name='coding', index_col=0)
        self.dict_add_new_qres_oe = dict_add_new_qres_oe
