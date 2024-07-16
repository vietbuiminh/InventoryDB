import re
import pandas as pd
from thefuzz import fuzz
import numpy as np


def processPasteBOM(text):
    text_ls = re.split(r'\t|\r\n', text)
    column_ls = []
    data_ls = []
    df = pd.DataFrame()
    # print(text_ls[0])
    # print("Fuzz: ", fuzz.partial_ratio(text_ls[0], "Bill of Material"))
    alike = fuzz.partial_ratio(text_ls[0], "Bill of Materials")
    if alike <= 100 and alike >= 98:
        # print("Pass")
        column_ls = column_ls = ['Bill of Materials', 'qty']
        data_ls = text_ls[2:]
        if len(data_ls) % 2 != 0 and fuzz.partial_ratio(data_ls[-1],
                                                        "") != 100:
            data_ls.append("")
        else:
            data_ls.pop()
            print(data_ls)
        reshaped_ls = np.array(data_ls).reshape(int(len(data_ls) // 2), 2)
        print(column_ls, reshaped_ls, "asdasd")
        df = pd.DataFrame(reshaped_ls, columns=column_ls)
    else:
        try:
            if int(text_ls[1]) >= 0:
                column_ls = ['Bill of Materials', 'qty']
                data_ls = text_ls[0:]
                if len(data_ls) % 2 != 0 and fuzz.partial_ratio(
                        data_ls[-1], "") != 100:
                    data_ls.append("")
                else:
                    data_ls.pop()
                reshaped_ls = np.array(data_ls).reshape(
                    int(len(data_ls) // 2), 2)
                print(column_ls, reshaped_ls, "asdasd")
                df = pd.DataFrame(reshaped_ls, columns=column_ls)
        except Exception as e:
            print(e)
    return df


# def test():
#     text = """Bill of Materials	qty
#     End Clamp (30mm)	46
#     Mid Clamp 	37
#     Bonded Mid Clamp 	22
#     3/8" Hardware 	228
#     Ridge Brackets (twisted both sides)	5
#     Ridge Brackets (straight, both sides)	7
#     3/8" Hardware (ridge bracket centers) 	24
#     3/8" Hardware (long)	28
#     Rail (19')*	40
#     Splice	28
#     """
#     processPasteBOM(text)
