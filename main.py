# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import psycopg2

S = "dbname=nuit_info user=matteo password=dev"


def init(S):
    conn = psycopg2.connect(S)
    cur = conn.cursor()
    return cur


def recherche_name(name, year, cur):
    cur.execute("""SELECT * FROM users WHERE name LIKE %s AND year=%s""", (name, year))
    rows = cur.fetchall()
    for row in rows:
        print("ID = ", row[0], row[1], row[2])
    return rows;



if __name__ == '__main__':
    cur = init(S)
    name = input("Entrer votre nom :\n")
    year = input("Entrer votre année :\n")
    rows = recherche_name(name,year, cur)
