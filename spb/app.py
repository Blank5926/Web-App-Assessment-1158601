from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

@app.route("/")
def home():
    return redirect("/currentjobs")

@app.route("/currentjobs")
def currentjobs():
    connection = getCursor()
    connection.execute("SELECT a.job_id,a.customer,concat(ifnull(b.first_name,''),' ',ifnull(b.family_name,'')) customer_name,a.job_date FROM job a, customer b where a.completed=0 and a.customer=b.customer_id;")
    jobList = connection.fetchall()
    return render_template("currentjoblist.html", job_list = jobList)    

if __name__ == '__main__':
    app.run()

