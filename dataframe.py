import numpy as np
import pandas as pd
# df_bt = pd.read_csv("./biteca.csv")
df_pb = pd.read_csv("./bio_grouped_new.csv")
df_fg = pd.read_csv("fgquery.csv")
# matching.mymatch(df_fg, df_fg, "personLabel", "NAME_FIRST", )
df_pb = pd.read_csv("./bio_grouped_new.csv")
df_fg = pd.read_csv("./fgquery.csv")
df_pb["name"] = df_pb["NAME_FIRST"] + " " + df_pb["NAME_LAST"]
print(df_fg.head())