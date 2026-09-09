"""
Timed queries + update examples for the prodtil_* tables created by ParquEdit,
built from the actual Landbruksdirektoratet "produksjon-og-avlosertilskudd"
columns (soeknads_aar, orgnr, orgnavn, kommunenr, arealer, pNNN livestock/crop
codes, and the tilskudd/subsidy amount columns).

Tables:
    prodtil_bulk          - wide format, single bulk insert (fill=True)
    prodtil_split_bulk    - wide format, inserted year-by-year
    prodtil_single_row    - wide format, inserted row-by-row
    prodtil_single_row_l  - LONG/melted format (soeknads_aar, orgnr, variable, value),
                             inserted row-by-row

Run this after the table-creation script in your question.
"""

import time
from contextlib import contextmanager

from ssb_parquedit import ParquEdit

con = ParquEdit()

TABLES = [
    "prodtil_bulk",
    "prodtil_split_bulk",
    "prodtil_single_row",
    "prodtil_single_row_l",
]


@contextmanager
def timed(label: str):
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    print(f"{label:<60} {elapsed:8.3f}s")


# ---------------------------------------------------------------------------
# 1. TIMED QUERIES - run the same battery of queries against each table
# ---------------------------------------------------------------------------

def run_query_battery(table: str) -> None:
    print(f"\n=== {table} ===")

    is_long = table == "prodtil_single_row_l"

    with timed(f"[{table}] count(*)"):
        n = con.count(table_name=table)
    print(f"  rows: {n}")

    with timed(f"[{table}] view() - full table"):
        _ = con.view(table_name=table)

    with timed(f"[{table}] view() - filter on soeknads_aar"):
        _ = con.view(table_name=table, where="soeknads_aar = 2024")

    with timed(f"[{table}] count() - filter on soeknads_aar"):
        _ = con.count(table_name=table, where="soeknads_aar = 2024")

    with timed(f"[{table}] view() - filter on a single orgnr"):
        _ = con.view(table_name=table, where="orgnr = 969111098")

    with timed(f"[{table}] view() - filter on kommunenr"):
        _ = con.view(table_name=table, where="kommunenr = 3434")

    with timed(f"[{table}] view() - limit/offset (pagination)"):
        _ = con.view(table_name=table, limit=500, offset=1000)

    with timed(f"[{table}] view() - order_by"):
        _ = con.view(table_name=table, order_by="soeknads_aar DESC, orgnr ASC")

    if not is_long:
        with timed(f"[{table}] view() - column selection"):
            _ = con.view(
                table_name=table,
                columns=["soeknads_aar", "orgnr", "orgnavn", "sum_produksjons_og_avloesertilskudd"],
            )
        with timed(f"[{table}] view() - filter on subsidy amount"):
            _ = con.view(
                table_name=table,
                where="soeknads_aar = 2024 AND cast(sum_produksjons_og_avloesertilskudd AS int) > 500000",
            )
        with timed(f"[{table}] view() - filter on total area"):
            _ = con.view(table_name=table, where="totalareal > 100")
    else:
        with timed(f"[{table}] view() - filter on variable + non-null value"):
            _ = con.view(
                table_name=table,
                where="variable = 'sum_produksjons_og_avloesertilskudd' AND value IS NOT NULL",
            )
        with timed(f"[{table}] view() - column selection (long format)"):
            _ = con.view(table_name=table, columns=["orgnr", "variable", "value"])
        with timed(f"[{table}] view() - filter on husdyrtilskudd rows"):
            _ = con.view(table_name=table, where="variable = 'husdyrtilskudd'")

    with timed(f"[{table}] view() - output_format='polars'"):
        _ = con.view(table_name=table, output_format="polars")

    with timed(f"[{table}] view() - output_format='pyarrow'"):
        _ = con.view(table_name=table, output_format="pyarrow")

    with timed(f"[{table}] exists()"):
        _ = con.exists(table_name=table)

    # with timed(f"[{table}] get_edits()"):
    #     _ = con.get_edits(table_name=table)


for t in TABLES:
    run_query_battery(t)


# ---------------------------------------------------------------------------
# 2. UPDATES - single cell
# ---------------------------------------------------------------------------
# edit() always targets exactly one rowid. To touch a single cell, pass a
# `changes` dict with just that one column. Example: fixing a misspelled
# company name for one applicant/year.

def update_single_cell():
    table = "prodtil_bulk"
    row = con.view(table_name=table, where="soeknads_aar = 2025 AND orgnr = 969111098")
    if row.empty:
        print("No matching row found for single-cell example")
        return
    rowid = row["rowid"].iloc[0]

    con.edit(
        table_name=table,
        rowid=rowid,
        changes={"orgnavn": "ØVERLIS LANDBRUKSSERVICE AS"},  # <- single column
        change_event_reason="REVIEW",
        change_comment="Corrected company name to match Brønnøysundregistrene",
    )


# ---------------------------------------------------------------------------
# 3. UPDATES - a group of cells in one row
# ---------------------------------------------------------------------------
# Still one edit() call, one rowid, but `changes` has several key/value pairs.
# This is atomic and produces one changelog entry covering all the columns.
# Example: correcting the land-use areas together, since fulldyrket +
# overflatedyrket + innmarksbeite should sum to totalareal.

def update_group_of_cells():
    table = "prodtil_bulk"
    row = con.view(table_name=table, where="soeknads_aar = 2025 AND orgnr = 969111098")
    if row.empty:
        print("No matching row found for multi-cell example")
        return
    rowid = row["rowid"].iloc[0]

    con.edit(
        table_name=table,
        rowid=rowid,
        changes={
            "fulldyrket": 62,
            "overflatedyrket": 0,
            "innmarksbeite": 7,
            "totalareal": 69,
        },
        change_event_reason="OWNER",
        change_comment="Owner-reported correction to fulldyrket/totalareal after resurvey",
    )


# ---------------------------------------------------------------------------
# 4a. UPDATES - batch, audited (loop of edit() calls)
# ---------------------------------------------------------------------------
# Slower, but every row-change is logged individually to get_edits(). Good
# when you need per-row traceability, e.g. reassigning a set of orgnr to a
# new kommunenr after a municipality merger/boundary change.

def batch_update_audited(year: int, org_list: list[int], new_kommunenr: int):
    table = "prodtil_bulk"
    matches = con.view(
        table_name=table,
        where=f"soeknads_aar = {year} AND orgnr IN ({','.join(map(str, org_list))})",
    )

    with timed(f"[{table}] batch update via edit() loop, n={len(matches)}"):
        for _, r in matches.iterrows():
            con.edit(
                table_name=table,
                rowid=r["rowid"],
                changes={"kommunenr": new_kommunenr},
                change_event_reason="OTHER_SOURCE",
                change_comment=f"Reassigned kommunenr to {new_kommunenr} after municipality reform",
            )


# ---------------------------------------------------------------------------
# 4b. UPDATES - batch, fast (raw DuckDB UPDATE, bypasses changelog)
# ---------------------------------------------------------------------------
# Much faster for large batches, but does NOT show up in con.get_edits(),
# since it writes directly to the underlying table rather than going through
# ParquEdit's edit() logging path. Use only when you don't need an audit
# trail, e.g. recomputing bunnfradrag for a whole year after a rule change.

def batch_update_fast(year: int, new_bunnfradrag: int):
    table = "prodtil_bulk"
    raw = con._get_connection().raw  # duckdb.DuckDBPyConnection

    with timed(f"[{table}] batch update via raw SQL UPDATE"):
        raw.execute(
            f"""
            UPDATE {table}
            SET bunnfradrag = {new_bunnfradrag}
            WHERE soeknads_aar = {year}
            """
        )


# Example calls (uncomment / adjust orgnr, years, kommunenr as needed):
# update_single_cell()
# update_group_of_cells()
# batch_update_audited(2025, [969111098, 969111233], new_kommunenr=3436)
# batch_update_fast(2025, new_bunnfradrag=6200)