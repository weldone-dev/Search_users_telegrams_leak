import sqlite3

def get_connection_db():
    return sqlite3.connect('users.db')


def init_db():
    conn = get_connection_db()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users( 
        userid INTEGER(24) PRIMARY KEY NOT NULL,
        user_status VARCHAR(65) DEFAULT 'user',
        username VARCHAR(65) NULL,
        balance INTEGER(24) DEFAULT 0,
        coupon_money INTEGER(24) DEFAULT 0,
        state VARCHAR(256) NULL,
        text VARCHAR(256) NULL
    )
    """)
    c.execute("CREATE INDEX user_status_idx ON users(user_status)")

    c.execute("""
       CREATE TABLE IF NOT EXISTS coupons(
           text VARCHAR(32) PRIMARY KEY NOT NULL,
           count_activation INTEGER(6)
       )
    """)
    conn.commit()
#####USERS########
def add_user(userid, username=""):
    if not(there_user(userid)):
        conn = get_connection_db()
        c = conn.cursor()
        c.execute("INSERT INTO users (userid, username) SELECT ?, ?", (userid, username))
        conn.commit()
def del_user(userid):
    conn = get_connection_db()
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE userid=?", (userid,))
    conn.commit()
def update_username(userid, username):
    conn = get_connection_db()
    c = conn.cursor()
    c.execute("UPDATE users SET username=? WHERE userid=?", (username,user_id))
    conn.commit()
def get_user(userid):
    conn = get_connection_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE userid=?", (userid,))
    conn.commit()
    return c.fetchone()
def get_count_usesrs():
    conn = get_connection_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(userid) FROM users",)
    conn.commit()
    return c.fetchone()[0]
def there_user(userid):
    conn = get_connection_db()
    c = conn.cursor()
    c.execute("SELECT userid FROM users WHERE userid=?", (userid,))
    conn.commit()
    if c.fetchone():
        return True
    else:
        return False
def get_all_admins():
    conn = get_connection_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_status='admin'")
    conn.commit()
    all_admin = ""
    for i in c.fetchall():
        all_admin+=f"@{i[2]}, "
    
    return all_admin[:-2]
#####BALANCE#######
def add_to_balance(userid, money): #Добавить к баланку  
    conn = get_connection_db()
    c = conn.cursor()
    c.execute("UPDATE users SET balance=balance+? WHERE userid=?", (money,userid))
    conn.commit()
def deduct_from_balance(userid, money): #Вычесть из баланса
    conn = get_connection_db()
    c = conn.cursor()
    c.execute("UPDATE users SET balance=balance-? WHERE userid=?", (money,userid))
    conn.commit()
def get_balance(userid):
    conn = get_connection_db()
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE userid=?", (userid,))
    conn.commit()
    return c.fetchone()[0]
def all_sum_balacne():
    conn = get_connection_db()
    c = conn.cursor()
    c.execute("SELECT SUM(balance) FROM users")
    conn.commit()
    return c.fetchone()[0]
#####STATUS#########
def update_status(userid, status): 
    conn = get_connection_db()
    c = conn.cursor()
    c.execute("UPDATE users SET user_status=? WHERE userid=?", (status,userid))
    conn.commit()
def get_status(userid):
    conn = get_connection_db()
    c = conn.cursor()
    c.execute("SELECT user_status FROM users WHERE userid=?", (userid,))
    conn.commit()
    return c.fetchone()[0]
#####STATE##########
def update_state(userid, state): 
    conn = get_connection_db()
    c = conn.cursor()
    c.execute("UPDATE users SET state=? WHERE userid=?", (state, userid))
    conn.commit()
def get_state(userid):
    conn = get_connection_db()
    c = conn.cursor()
    c.execute("SELECT state FROM users WHERE userid=?", (userid,))
    conn.commit()
    
    return c.fetchone()[0]
#Cleae all state
def clear_all_state():
    conn = get_connection_db()
    c = conn.cursor()
    c.execute("UPDATE users SET state=?", ("NULL", ))
    conn.commit()
#Print all
def print_users():
    conn = get_connection_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    conn.commit()
    for i in c.fetchall():
        print(i)
if __name__ == "__main__":
    init_db()
    print_users()
   