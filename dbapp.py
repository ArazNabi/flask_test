from flask import Flask, render_template, request, redirect, url_for
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

def insert_contact(name, phone, address, city, mail):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO phonelist (name, phone, address, city, email) VALUES (%s, %s, %s, %s, %s);",
        (name, phone, address, city, mail))
    cur.execute("COMMIT;")
    cur.close()
    conn.close()
    return "Contact added"

def delete_contact(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM phonelist WHERE id = %s;", (id))
    cur.execute("COMMIT;")
    cur.close()
    conn.close()
    return "Contact removed"


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
        address= request.form['address']
        city= request.form['city']
        mail= request.form['mail']
        return render_template('insert.html', req=insert_contact(name, phone, address, city, mail))
    else:
        return render_template('list.html', list=read_phonelist())
    
@app.route("/delete", methods = ['POST', 'GET'])
def delete_page():
    if request.method == 'POST':
        c_id= request.form['id']
        return render_template('delete.html', req=delete_contact(c_id))
    else:
        return render_template('list.html', list=read_phonelist())