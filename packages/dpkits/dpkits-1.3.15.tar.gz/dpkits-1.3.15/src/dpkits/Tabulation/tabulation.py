import pandas as pd
import numpy as np
from ..logging import Logging
from .model_table import Table




class Tabulation(Logging):


    def __init__(self, *, tbl_file_name: str, grp_tbl_info: dict[dict]):
        """
        :param tbl_file_name: output xlsx file name
        :param grp_tbl_info: all tables information for processing
        """

        super().__init__()

        # --------------------------------------------------------------------------------------------------------------
        self.tbl_file_name = tbl_file_name.rsplit('/', 1)[-1] if '/' in tbl_file_name else tbl_file_name

        try:
            with open(self.tbl_file_name):
                self.print(f'File: "{self.tbl_file_name}" is accessed >>> Completed', self.clr_succ)

        except PermissionError:
            raise PermissionError(f'Permission Error when access file: "{self.tbl_file_name}" Processing terminated.')

        except FileNotFoundError:
            pass


        # --------------------------------------------------------------------------------------------------------------
        self.grp_tbl_info = grp_tbl_info
        self.lst_model_tables: list[TableInformation] = list()


        # on hold
        # TableFormatter.__init__(self, self.tbl_file_name)

        # is developing
        # TabulationVertical.__init__(self, dict_tbl_info)







    def tabulate_tables(self, *, lst_running_tables_group: list[str]):

        s_err_tbl = set(lst_running_tables_group).difference(set(self.grp_tbl_info.keys()))

        if s_err_tbl:
            raise ValueError(f"Undefined tables: {s_err_tbl}")


        for grp_tbl_name, tbl_info in self.grp_tbl_info.items():

            if grp_tbl_name not in lst_running_tables_group:
                self.print(f"Skip group tables {grp_tbl_name}", self.clr_warn)
                continue

            self.print(f"Process group tables {grp_tbl_name}", self.clr_magenta)

            dict_data_to_run = dict(tbl_info['data_to_run'])

            for tbl_name, tbl_format in tbl_info['tables_format'].items():

                if tbl_name not in tbl_info['tables_to_run']:
                    self.print(f"Skip {tbl_name}", self.clr_warn)
                    continue
                
                self.print(f"Process {tbl_name}", self.clr_blue)

                tbl_format.update({'data_to_run': dict_data_to_run})
                obj_table = Table.from_orm(tbl_format)

                # For checking
                obj_table.df_horizontal.to_csv(f'tbl_format.df_horizontal_{tbl_name}.csv')


                self.lst_model_tables.append(obj_table)

                dict_data_to_run.update({'is_validated': True})








        del self.grp_tbl_info





    # Note:
    #     - fix sig test, do not sig total with other code
    #     - fix sort method


