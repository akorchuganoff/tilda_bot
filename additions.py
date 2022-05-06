import sqlite3

DATABASE_PATH = 'D:\\projects\\Личные проекты\\tilda_telegram_bot\\leads.db'
conn = sqlite3.connect(DATABASE_PATH)
cur = conn.cursor()


def add_lead_to_db(date, time, error, phone, name, guest_data):
    # conn = sqlite3.connect(DATABASE_PATH)
    # cur = conn.cursor()
    request = f"""INSERT INTO leads (date, time, error, phone, name, guest_data) VALUES ({date}, {time}, {error}, {phone}, {name}, {guest_data});"""
    print(request)
    cur.execute(request)
    conn.commit()
    return True


def check_lead(phone, date, time):
    request = f"""SELECT * FROM leads WHERE phone == {phone} and date == {date} and time == {time};"""
    print(request)
    data = cur.execute(request).fetchall()
    if len(data) == 0:
        return True
    return False


def get_active_leads():
    request = f"""SELECT * FROM leads WHERE status == 'NEW';"""
    print(request)
    data = cur.execute(request).fetchall()
    return data


def remove_lead_by_id(id):
    try:
        request = f"""UPDATE leads SET status = 'PROCESSED' WHERE id == {id};"""
        print(request)
        cur.execute(request)
        conn.commit()
        return True
    except Exception:
        return False
