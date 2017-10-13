from flask import Flask
from flask import render_template
from flask_mysqldb import MySQL
from flask_prometheus import monitor 
mysql = MySQL()
app = Flask(__name__)
# My SQL Instance configurations 
# Change the HOST IP and Password to match your instance configurations
 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'P@ssw0rd'
app.config['MYSQL_DB'] = 'studentbook'
app.config['MYSQL_HOST'] = '35.195.195.114'
mysql.init_app(app)

@app.route('/')
@app.route('/<name>')
def statichtml(name=None):
    return render_template('index.html', name=name)

# The first route to access the webservice from http://35.190.217.3:5000/ 
#@pp.route("/add") this will create a new endpoints that can be accessed using http://external-ip:5000/add
@app.route("/list")
def hello(): # Name of the method
    cur = mysql.connection.cursor() #create a connection to the SQL instance
    cur.execute('''SELECT * FROM students''') # execute an SQL statment
    rv = cur.fetchall() #Retreive all rows returend by the SQL statment
    return render_template('index.html', name=str(rv))     #Return the data in a string format

@app.route("/add/<name>/<email>")
def add(name=None, email=None):
    cur= mysql.connection.cursor()
    insert_stmt = (
                 "INSERT INTO students (studentName, email) "
                 "VALUES (%s, %s)")
    data=(name,email)
    cur.execute(insert_stmt, data)
    mysql.connection.commit()
    return render_template('index.html', name="New Record is added to the database")  

@app.route("/update/<name>/<email>")
def update(name=None, email=None):
    cur=mysql.connection.cursor()
    update_stmt = (
        "UPDATE students SET studentName = %s " 
        "WHERE email = %s")
    data=(name,email)
    cur.execute(update_stmt, data)
    mysql.connection.commit()
    return render_template('index.html', name="User recored was updated")      #Return the data in a string format

@app.route("/delete/<name>")
def delete(name=None):
    cur=mysql.connection.cursor()
    delstatmt = "DELETE FROM students WHERE studentName = ' {} ' ".format(name)
    print(delstatmt)                
   
    cur.execute(delstatmt)
    mysql.connection.commit()
    return render_template('index.html', name="User recored was deleted")      #Return the data in a string format

if __name__ == "__main__":
        monitor(app, port=8000)
        app.run(host='0.0.0.0', port='5000')
