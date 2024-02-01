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

def generate_href(field_value):
    # Your logic to generate the href based on field_value
    # For example, let's say you want to link to Google search using the field value
    return f'/job/{field_value}'

@app.route("/currentjobs")
def currentjobs():
    connection = getCursor()
    # add customers' name combine togther, add customer table for query
    connection.execute("SELECT a.job_id,a.customer,concat(ifnull(b.first_name,''),' ',ifnull(b.family_name,'')) customer_name,a.job_date FROM job a, customer b where a.completed=0 and a.customer=b.customer_id;")
    jobList = connection.fetchall()
    return render_template("currentjoblist.html", job_list=jobList, generate_href=generate_href)

@app.route("/job/<int:job_id>")
def job_detail(job_id):
    connection = getCursor()

    # Fetch job details
    connection.execute("SELECT * FROM job WHERE job_id = %s", (job_id,))
    job = connection.fetchone()

    # From job_part, job and part table query the part usage of this job
    connection.execute("SELECT a.*, b.qty FROM part a JOIN job_part b ON a.part_id = b.part_id WHERE b.job_id = %s;", (job_id,))
    parts = connection.fetchall()

    # From job_service, service and job table query the service usage of this job
    connection.execute("SELECT a.*, b.qty FROM service a JOIN job_service b ON a.service_id = b.service_id WHERE b.job_id = %s", (job_id,))
    services = connection.fetchall()

    # Fetch lists of all available services and parts for adding to the job
    connection.execute("SELECT * FROM service")
    all_services = connection.fetchall()
    connection.execute("SELECT * FROM part")
    all_parts = connection.fetchall()

    return render_template("job_detail.html", job=job, services=services, parts=parts, all_services=all_services, all_parts=all_parts)


if __name__ == '__main__':
    app.run()
