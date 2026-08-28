from ssb_parquedit import ParquEdit

con = ParquEdit()

print(con.list_tables())

table = "skjemadata"

view = con.view(table, where="skjema = 'RA-0530' AND refnr = '7fe33c89f117' AND feltnavn = 'haddeVarenJaNei'")
# con.drop_table(table)
print(view)