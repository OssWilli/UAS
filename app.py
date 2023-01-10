from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
Flask
import mysql.connector
from flask_wtf import FlaskForm
from wtforms import StringField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from filepath import BASE_PATH

app = Flask(__name__)
app.secret_key = "super secret key"

def getMysqlConnection():
    return mysql.connector.connect(user='root', host='localhost', port='3306', password='', database='pa_web')

class MyForm(FlaskForm):
    file = FileField('File', validators=[FileAllowed(['txt', 'pdf', 'jpg', 'jpeg', 'png'])])

def getData(sqlstr):
       db = getMysqlConnection()
       cur = db.cursor()
       cur.execute(sqlstr)
       output_data = cur.fetchall()
       return output_data

def deleteData(sqlstr, route):
       db = getMysqlConnection()
       cur = db.cursor()
       cur.execute(sqlstr)
       db.commit()
       return redirect(url_for(f"{route}"))

def createData(sqlstr, route):
       db = getMysqlConnection()
       cur = db.cursor()
       cur.execute(sqlstr)
       db.commit()
       return redirect(url_for(f"{route}"))

def getOneData(sqlstr):
       db = getMysqlConnection()
       cur = db.cursor()
       cur.execute(sqlstr)
       string_data = cur.fetchone()[0]
       return string_data

def getUpdateData(sqlstr, cur):
       cur.execute(sqlstr)
       data = cur.fetchone()
       return data

# INDEX
@app.route('/')
def index():
   return render_template('index.html', hidden="hidden")

@app.route('/indexAdmin')
def indexAdmin():
       return render_template('index_admin.html')

@app.route('/antrian')
def antrian():
       return render_template('antrian.html')

@app.route('/daftarMenu')
def daftar_menu():
       return render_template('daftar_menu.html')

@app.route('/daftarPesanan')
def daftar_pesanan():
       return render_template('pesanan.html')

@app.route('/promo')
def promo():
       return render_template('promo.html')

@app.route('/signUp')
def signUp():
       return render_template('signup.html')

# DASHBOARD
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
       data_user = getData("SELECT * FROM user")
       total_reservasi = getData("SELECT * FROM reservasi")
       reservasi_pending = getData("SELECT * FROM `reservasi` WHERE `status`= 'Pending'")
       reservasi_selesai = getData("SELECT * FROM `reservasi` WHERE `status`= 'Selesai'")
       return render_template('dashboard.html', data_user = data_user, total_reservasi = total_reservasi, reservasi_pending = reservasi_pending, reservasi_selesai = reservasi_selesai)

# DATABASE USER
@app.route('/dashboardUser')
def dashboardUser():
       data = getData("SELECT * from user")
       return render_template('user.html', data=data)

@app.route('/deleteUser/<int:id>')
def deleteUser(id):
       route = 'dashboardUser'
       idString = str(id)
       sqlstr = "DELETE FROM user WHERE id_user="+idString+""
       return deleteData(sqlstr, route)

@app.route('/updateUser/<int:id>', methods=['GET','POST'])
def updateUser(id):
       
       db = getMysqlConnection()
       cur = db.cursor()
       strid = str(id)

       data = getUpdateData(f"SELECT * FROM user WHERE id_user ='{strid}'", cur)

       if request.method == 'POST':
             username = request.form['username']
             password = request.form['password']
             sqlstr = "UPDATE `user` SET `username` = '"+username+"', `password` = '"+password+"' WHERE `user`.`id_user` = '"+strid+"';"
             cur.execute(sqlstr)
             db.commit()
             cur.close()
             db.close()
             return render_template('user_update.html', data=data, disabled='disabled')
       
       else :
             cur.close()
             db.close()
             return render_template('user_update.html', data=data, disabled='') 

# DATABASE RESERVASI
@app.route('/dashboardReservasi')
def dashboardReservasi():
       data = getData("SELECT * from reservasi where status='Selesai' ")
       return render_template('reservasi.html', data=data)

@app.route('/deleteReservasi/<int:id>')
def deleteReservasi(id):
       route = 'dashboardReservasi'
       idString = str(id)
       sqlstr = "DELETE FROM reservasi WHERE id_pemesanan="+idString+""
       return deleteData(sqlstr, route)
       

@app.route('/updateReservasi/<int:id>', methods=['GET','POST'])
def updateReservasi(id):
       db = getMysqlConnection()
       cur = db.cursor()

       data = getUpdateData(f"SELECT * FROM reservasi WHERE id_pemesanan='{id}'", cur)
       data_meja = getData(f"SELECT * FROM meja")
       strid = str(id)
       if request.method == 'POST':
             nama = request.form['nama']
             email = request.form['email']
             telepon = request.form['telepon']
             jml_tamu = request.form['jml_tamu']
             tanggal = request.form['tanggal']
             jam = request.form['jam']
             meja = request.form['meja']
             layanan = request.form['layanan']
             status = request.form['status']

             separate_meja = meja.split(',')
             strmeja = separate_meja[0]
             keterangan_meja = separate_meja[1]
             sqlstr = "UPDATE `reservasi` SET `nama` = '"+nama+"', `email` = '"+email+"', `telp` = '"+telepon+"', `jum_tamu` = '"+jml_tamu+"', `tanggal` = '"+tanggal+"', `jam` = '"+jam+"', `meja_no` = '"+strmeja+"', `ket_meja` = '"+keterangan_meja+"', `tambahan` = '"+layanan+"', `status` = '"+status+"' WHERE `reservasi`.`id_pemesanan` = '"+strid+"'"
             cur.execute(sqlstr)
             db.commit()
             cur.close()
             db.close()
             return render_template('reservasi_update.html', data=data, data_meja=data_meja, disabled='disabled') 
       else:
             cur.close()
             db.close()
             return render_template('reservasi_update.html', data=data, data_meja=data_meja, disabled='') 


# DATABASE MEJA
@app.route('/dashboardMeja')
def dashboardMeja():
       data = getData("SELECT * from meja")
       return render_template('meja.html', data=data)

@app.route('/createMeja', methods=['GET', 'POST'])
def createMeja():
       meja = request.form['meja']
       keterangan = request.form['keterangan']
       route = 'dashboardMeja'
       sqlstr = "INSERT INTO meja (`no_meja`, `keterangan`) routeS ('"+meja+"', '"+keterangan+"')"
       return createData(sqlstr, route)

@app.route('/deleteMeja/<int:id>')
def deleteMeja(id):
       route = 'dashboardMeja'
       idString = str(id)
       sqlstr = "DELETE FROM meja WHERE no_meja="+idString+""
       return deleteData(sqlstr, route)

@app.route('/updateMeja/<int:id>', methods=['GET','POST'])
def updateMeja(id):
       db = getMysqlConnection()
       cur = db.cursor()

       data = getUpdateData(f"SELECT * FROM meja WHERE no_meja ='{id}'", cur)

       if request.method == 'POST':
             no_meja = request.form['no_meja']
             keterangan = request.form['keterangan']
             sqlstr = f"UPDATE `meja` SET `no_meja` = '{no_meja}', `keterangan` = '{keterangan}' WHERE `meja`.`no_meja` = {id}"
             cur.execute(sqlstr)
             db.commit()
             cur.close()
             db.close()
             return render_template('meja_update.html', data=data, disabled='disabled') 
       else:
             cur.close()
             db.close()
             return render_template('meja_update.html', data=data, disabled='') 

# DATABASE PROMO
@app.route('/dashboardPromo')
def dashboardPromo():
       data = getData("SELECT * from promo")
       return render_template('promo.html', data=data)

@app.route('/createPromo', methods=['GET', 'POST'])
def createPromo():

       if request.method == 'GET' :
              data_menu = getData("SELECT * from daftar_menu")
              return render_template('promo_create.html', data_menu=data_menu)
       
       if request.method == 'POST' :
           
              id_menu = request.form['menu']
              harga_promo = request.form['harga_akhir']
              
              harga_awal = getOneData("SELECT harga from daftar_menu where id_menu='"+id_menu+"'")
              nama_menu = getOneData("SELECT menu from daftar_menu where id_menu='"+id_menu+"'")
              route = 'dashboardPromo'
              sqlstr = "INSERT INTO `promo` (`id_promo`, `menu`, `harga_awal`, `harga_promo`) VALUES (NULL, '"+nama_menu+"', '"+str(harga_awal)+"', '"+harga_promo+"')"
              return createData(sqlstr, route)

@app.route('/deletePromo/<int:id>')
def deletePromo(id):
       route = 'dashboardPromo'
       idString = str(id)
       sqlstr = "DELETE FROM promo WHERE id_promo="+idString+""
       return deleteData(sqlstr, route)

@app.route('/updatePromo/<int:id>', methods=['GET','POST'])
def updatePromo(id):
       db = getMysqlConnection()
       cur = db.cursor()

       data = getUpdateData(f"SELECT * FROM promo WHERE id_promo='{id}'", cur)

       if request.method == 'POST':
             harga_akhir = request.form['harga_akhir']
             sqlstr = f"UPDATE `promo` SET `harga_promo` = '{harga_akhir}' WHERE `promo`.`id_promo` = {id}"
             cur.execute(sqlstr)
             db.commit()
             cur.close()
             db.close()
             return render_template('promo_update.html', data=data, disabled='disabled') 
       else:
             cur.close()
             db.close()
             return render_template('promo_update.html', data=data, disabled='') 

path = "../static/img/"

@app.route('/createMenu', methods=['GET','POST'])
def createMenu():
       form = MyForm()
       if request.method == 'POST':
              file = request.files['files']
              nama = request.form['nama_makanan']
              harga = request.form['harga']

              # Sanitize the file name
              filename = secure_filename(file.filename)

              # Save the file to the filesystem
              file.save(BASE_PATH + filename)

              filepath = path + filename

              route = 'dashboardMenu'
              sqlstr = f"INSERT INTO `daftar_menu` (`id_menu`, `menu`, `harga`, `path`) VALUES (NULL, '{nama}', '{harga}', '{filepath}')"
              return createData(sqlstr, route)

       return render_template('menu_create.html', form=form)

@app.route('/dashboardMenu', methods=['GET','POST'])
def dashboardMenu():
       data = getData("SELECT * FROM daftar_menu")
       return render_template('menu.html', data=data)

@app.route('/deleteMenu/<int:id>', methods=['GET', 'POST'])
def deleteMenu(id):
       route = 'dashboardMenu'
       sqlstr = f"DELETE FROM daftar_menu WHERE id_menu={id}"
       return deleteData(sqlstr, route)


@app.route('/updateMenu/<int:id>', methods=['GET','POST'])
def updateMenu(id):
       db = getMysqlConnection()
       cur = db.cursor()

       data = getUpdateData(f"SELECT * FROM daftar_menu WHERE id_menu='{id}'", cur)

       if request.method == 'POST':
               file = request.files['files']
               nama = request.form['nama_menu']
               harga = request.form['harga']
               # Sanitize the file name
               filename = secure_filename(file.filename)

               # Save the file to the filesystem
               file.save(BASE_PATH + filename)

               filepath = path + filename
               sqlstr = f"UPDATE `daftar_menu` SET `menu` = '{nama}', `harga` = '{harga}', `path` = '{filepath}' WHERE `daftar_menu`.`id_menu` = {id}"
               cur.execute(sqlstr)
               db.commit()
               cur.close()
               db.close()
               return render_template('promo_update.html', data=data, disabled='disabled') 
       else:
             cur.close()
             db.close()
             return render_template('menu_update.html', data=data, disabled='') 


@app.route('/cek')
def cek():
       return render_template('reservasi_user.html')

#LOGIN
@app.route('/login', methods=['GET','POST'])
def login():
       db = getMysqlConnection()
       cur = db.cursor()
       
       if request.method == 'POST':
              user = request.form['user']
              password = request.form['password']

              data = getUpdateData("SELECT * FROM user WHERE username='"+user+"'", cur)
              print(data)
              if data != None:
                     if data[1] == 'admin':
                            if password == data[2]:
                                   return redirect(url_for("indexAdmin"))
                            else:
                                   return "Password yang Anda masukkan salah!"
                     else:
                            if password == data[2]:
                                   return redirect(url_for("antrian"))
                            else:
                                   return "Password yang Anda masukkan salah!"
              else:
                     return ("Username tidak ditemukan!")

       return render_template('signin.html')




if __name__ == '__main__':
    app.run(debug=True)
