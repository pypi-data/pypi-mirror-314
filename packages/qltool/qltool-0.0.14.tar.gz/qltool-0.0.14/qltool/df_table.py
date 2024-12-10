#!/usr/bin/env python3

# to override print <= can be a big problem with exceptions
# from __future__ import print_function # must be 1st
# import builtins

# import sys

from fire import Fire

# from qltool.version import __version__
# from qltool import unitname
# from qltool import config

# import time
# import datetime as dt
from console import fg, bg

# import os

import pandas as pd
import numpy as np
from terminaltables import SingleTable


def create_dummy_df():
    """
    Args:
    None
    Returns:
    dataframe
"""
    columns = ["a", "b", "c", "_fg", "_bg"]
    # columns1=[x for x in columns if x[0]!="_"]
    df = pd.DataFrame(np.random.randint(0, 9, size=(11, len(columns))),
                      columns=columns)
    df["_fg"] = fg.lightgray  # fg.default
    df["_bg"] = bg.default

    # --------------------------- default pattern ------------
    for i, row in df.iterrows():
        if i % 3 == 0:
            df.loc[i, ["_bg"]] = bg.darkslategray  # bg.dimgray#bg.darkslategray
        else:
            df.loc[i, ["_bg"]] = bg.default  # bg.black

        if i % 5 == 0:
            df.loc[i, ["_fg"]] = fg.lightgreen  # lightyellow

    return df


def inc_dummy_df(df):
    """
    increase df cells by unit
    """
    for i, row in df.iterrows():
        df.iloc[i, :-2] = df.iloc[i, :-2] + 1  # loc doesnt work, iloc is ok
    return df


# ======================================================
def show_table(df, selection="123"):
    """
    test.
    Idea: take df source...   Get those selected... df info on color???
    I need to solve colors
    """

    row_n = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]

    dfpure = df.copy()
    dfpure.drop(columns=["_fg", "_bg"], inplace=True)

    rows = dfpure.values.tolist()
    rows = [[str(el) for el in row] for row in rows]
    # columns = df.columns.tolist()

    columns2 = [x for x in list(df.columns) if x[0] != "_"]
    tab_header = [["n"] + columns2]  #
    # tab_header = [  f"{fg.white}{x}{fg.default}" for x in tab_header] # NOTW
    # data = [['a','b'], ['ca','cb']]
    tab_src = tab_header.copy()

    # nn=0  #I use index
    padding = "  "  # nicer bars
    for index, row in df.iterrows():
        # i take row from pure
        row = list(dfpure.loc[index, :])
        fgcol = fg.white
        fgcol = df.loc[index, ["_fg"]][0]
        bgcol = df.loc[index, ["_bg"]][0]
        if selection is not None and row_n[index] in list(selection):
            # print(index, selection)
            bgcol = bg.yellow4  # df.loc[index,['_fg']][0]

        # print(bgcol)
        # print(index, row ) # list of pure df cols for row
        row = [row_n[index]] + row

        for j in range(len(row)):  # change color
            row[j] = (
                fgcol
                + bgcol
                + padding
                + str(row[j])
                + padding
                + bg.default
                + fg.default
            )

        tab_src.append(row)  # prepend to list
        # nn+=1

    table = SingleTable(tab_src)
    table.padding_left = 0
    table.padding_right = 0
    # blessings terminal() t.clear()

    # --------- if too wide - i think
    if not table.ok:
        table.padding_left = 0
    if not table.ok:
        table.padding_right = 0
    while not table.ok:
        j = 0
        # remove columns here
        # table = SingleTable()
        table.padding_left = 0
        table.padding_right = 0

    print(table.table)




def main():
    """
    Show table
    """
    df = create_dummy_df()
    df = inc_dummy_df(df)
    move_cursor(15, 4)
    show_table(df)


if __name__ == "__main__":
    Fire(main)
