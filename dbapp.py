from flask import Flask, render_template, request
import datetime
import psycopg2

def get_db_connection(): #connect to our database
    conn = psycopg2.connect(
        host="localhost",
        port="5433",
        database= "phonedb",
        user="postgres",
        password="dagsattPlugga345")
    return conn

def read_phonelist():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonelist;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def insert_contact(name, phone):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO phonelist (name, phone) VALUES (?,?);",
                name, phone)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

simple = [
  ['alex', '013-131313'], ['benedict','01234'], ['christina','077-1212321']
]

app = Flask(__name__)

@app.route("/")
def start():
    now = datetime.datetime.now()
    D = [str(now.year%100), str(now.month), str(now.day)]
    if len(D[1])<2:
        D[1] = '0'+D[1]
    if len(D[2])<2:
        D[2] = '0'+D[2]
    return render_template('list.html', list=read_phonelist(), date=D)

@app.route("/insert", methods = ['POST', 'GET'])
def insert_page():
    if request.method == 'POST':
        name= request.form['name']
        phone= request.form['phone']
        return render_template('insert.html', req=insert_contact(
            name, phone, address, city, mail))
    else:
        return render_template('list.html', list=read_phonelist())
    

