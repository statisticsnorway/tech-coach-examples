import duckdb as db

navn = "eksempel"
splitt_7172 = db.sql(
    f"""select distinct {navn}, verdi as rente from r12_koblet2 where art in ('71','72')"""
)
splitt_0160 = db.sql(
    f"""select distinct {navn}, verdi as belop_50 from r12_koblet2 where art in ('01','60')"""
)
