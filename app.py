from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
import mysql.connector
app = Flask(__name__)
app.secret_key = "super secret key"

def getMysqlConnection():
    return mysql.connector.connect(user='root', host='localhost', port='3306', password='', database='pa_web')


@app.route('/')
def index():
   return 'Hello, World!'

def getData(sqlstr):
       db = getMysqlConnection()
       cur = db.cursor()
       cur.execute(sqlstr)
       output_data = cur.fetchall()
       return output_data

def deleteData(id, value):
       db = getMysqlConnection()
       idString = str(id)
       sqlstr = "DELETE FROM user WHERE id_user="+idString+""
       cur = db.cursor()
       cur.execute(sqlstr)
       db.commit()
       return redirect(url_for(f"{value}"))

@app.route('/dashboardUser')
def dashboardUser():
       data = getData("SELECT * from user")
       return render_template('user.html', data=data)

@app.route('/deleteUser/<int:id>')
def deleteUser(id):
       value = 'dashboardUser'
       return deleteData(id, value)

@app.route('/updateUser/<int:id>', methods=['GET','POST'])
def updateUser(id):
       strid = str(id)
       
       db = getMysqlConnection()
       cur = db.cursor()
       strid = str(id)

       if request.method == 'POST':
             username = request.form['username']
             password = request.form['password']
             sqlstr = "UPDATE `user` SET `username` = '"+username+"', `password` = '"+password+"' WHERE `user`.`id_user` = '"+strid+"';"
             cur.execute(sqlstr)
             db.commit()
             cur.close()
             db.close()
             return redirect(url_for('dashboardUser'))


# @app.route('/dashboardReservasi')
# def dashboardReservasi():
#        data = getData("SELECT * from reservasi where status='Selesai' ")
#        return render_template('reservasi.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)