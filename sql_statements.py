def insert_db_row():
    insert_query = """INSERT INTO Vault (URL, Username, Password) VALUES (%s, %s, %s)"""
    return insert_query

def delete_db_row():
    sql_delete_query = """DELETE FROM Vault WHERE URL = %s"""
    return sql_delete_query

def update_db_url():
    update_query_url = """UPDATE Vault SET URL = %s WHERE URL = %s"""
    return update_query_url

def update_db_usrname():
    update_query_usrname = """UPDATE Vault SET Username = %s WHERE URL = %s"""
    return update_query_usrname

def update_db_passwd():
    update_query_passwd = """UPDATE Vault SET Password = %s WHERE URL = %s"""
    return update_query_passwd

def select_db_entry():
    select_query = """SELECT * FROM Vault WHERE URL = %s"""
    return select_query

def update_db():
    update_db = """UPDATE Vault SET Password = %s"""
    return update_db


