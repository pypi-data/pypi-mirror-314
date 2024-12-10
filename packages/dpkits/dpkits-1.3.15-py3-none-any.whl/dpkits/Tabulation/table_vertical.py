import pandas as pd
import numpy as np
from ..logging import Logging





class TabulationVertical(Logging):


    def __init__(self, *, obj_table):
        super().__init__()
        self.obj_table = obj_table



    def generate_df_vertical(self):

        lst_col = ['name', 'label', 'type', 'cat_code', 'cat_label', 'cols', 'factor', 'filter', 'sort', 'calculation']


        for item in self.obj_table.tbl_side:

            print(item.name, item.label, item.type)



        # here:



        a = 1




        return self.obj_table












