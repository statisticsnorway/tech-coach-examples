import duckdb as db

navn = "eksempel"
db.sql(
    f"""select distinct {navn}, verdi as rente from r12_koblet2 where art in ('71','72')"""
).create_view("splitt_7172")
db.sql(
    f"""select distinct {navn}, verdi as belop_50 from r12_koblet2 where art in ('01','60')"""
).create_view("splitt_0160")

sp1=db.sql(f"""select a.*, b.belop_50 from splitt_7172 a full join splitt_0160 b 
on a.periode=b.periode and a.selskap=b.selskap and a.serienavn=b.serienavn and a.ltid=b.ltid and a.sek=b.sek
where a.rente is not null and b.belop_50 is not null""").df()