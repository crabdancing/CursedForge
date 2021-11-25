#db = sqlite3.connect('cursedforge.db')
# db.enable_load_extension(True)
#db.load_extension('sqlite/fts5.so')
#db.execute('create table if not exists id_vs_name (id, name)')
#db.execute('create virtual table if not exists id_vs_name using fts5 (id, name)')
#db.commit()
    # https://stackoverflow.com/questions/60244988/how-can-i-use-the-fts5-extension-with-the-sqlite3-python-module-with-python-3-7
    # WHYYYYY???
    # sqlite3.OperationalError: unable to use function MATCH in the requested context
    # Every. Damn. Time. Have seen this NOT happen in console simplified case.
    # See:
    # >>> import sqlite3
    # >>>
    # >>> conn = sqlite3.connect(':memory:')
    # >>> conn.execute("""create virtual table fts5test using fts5 (data);""")
    # <sqlite3.Cursor object at 0x7f0923218650>
    # >>> conn.execute("""insert into fts5test (data)
    # ...                 values ('this is a test of full-text search');""")
    # <sqlite3.Cursor object at 0x7f0923218810>
    # >>> conn.execute("""select * from fts5test where data match 'full';""").fetchall()
    # for row in db.execute(f'select * from id_vs_name where   \'{url_stem}\' match name').fetchall():
    #    print(row)
# add_cmd = f'insert into id_vs_name (id, name) values ({project_id}, \'"{url_stem}"\')'
# db.execute(add_cmd)
# db.commit()