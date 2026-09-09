from ssb_parquedit import ParquEdit
import pandas as pd
from _duckdb import CatalogException

con = ParquEdit()

for table in [
    "prodtil_bulk",
    "prodtil_split_bulk",
    "prodtil_single_row",
    "prodtil_single_row_l",
]:
    try:
        con.drop_table(table_name=table, cleanup=True)
    except CatalogException:
        print(f"Already deleted {table}")


df = pd.DataFrame()
for i in range(2017, 2026):
    df = pd.concat(
        [
            df,
            pd.read_csv(
                f"https://raw.githubusercontent.com/LandbruksdirektoratetGIT/opendata/refs/heads/main/datasets/produksjon-og-avlosertilskudd/{i}/dataset.csv",
                sep=";",
            ),
        ]
    )
df = df.reset_index(drop=True)
df.columns = [
    str(col)
    .replace(" ", "")
    .replace("(", "")
    .replace(")", "")
    .replace("-", "")
    .replace(",", "")
    .replace(".", "")
    .lower()
    for col in df.columns
]
df.columns = df.columns.str[:55]

df = df.loc[:, ~df.columns.duplicated()].copy()
print("Starting create")
print(df)
con.create_table(
    table_name="prodtil_bulk",
    product_name="Testing med prodtil data",
    source=df,
    fill=True,
    user_defined_id=["soeknads_aar", "orgnr"],
)

view = con.view("prodtil_bulk")

print(view)

con.create_table(table_name="prodtil_split_bulk", product_name="Testing med prodtil data",source=df, fill=False, user_defined_id=["soeknads_aar", "orgnr"])
for year in range(2017, 2026):
    con.insert_data(table_name="prodtil_split_bulk",source=df[df["soeknads_aar"] == year])

con.create_table(table_name="prodtil_single_row", product_name="Testing med prodtil data",source=df, fill=False, user_defined_id=["soeknads_aar", "orgnr"])
print("prodtil_single_row")
for row_no in range(len(df)):
    row = df.iloc[[row_no]]

    con.insert_data(
        table_name="prodtil_single_row",
        source=row
    )

df = df.melt(id_vars=["soeknads_aar", "orgnr"])

con.create_table(table_name="prodtil_single_row_l", product_name="Testing med prodtil data",source=df, fill=False, user_defined_id=["soeknads_aar", "orgnr"])
print("prodtil_single_row_l")
for row_no in range(len(df)):
    row = df.iloc[[row_no]]

    con.insert_data(
        table_name="prodtil_single_row_l",
        source=row
    )


print("Done")
