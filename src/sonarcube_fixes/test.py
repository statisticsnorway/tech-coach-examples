import duckdb as db

navn = "eksempel"
db.sql(
    f"""select distinct {navn}, verdi as rente from r12_koblet2 where art in ('71','72')"""
).create_view("splitt_7172")
db.sql(
    f"""select distinct {navn}, verdi as belop_50 from r12_koblet2 where art in ('01','60')"""
).create_view("splitt_0160")
