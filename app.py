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

def isAdmin():
       if 'isloggedin' not in session:
              return redirect(url_for('index'))
              

tampil=""
hidden="hidden"

# INDEX{{url_for('index')}}
@app.route('/')
def index():
       if 'loggedin' in session and session['id'] == 1:
              return render_template('index_admin.html')
       elif 'loggedin' in session:
              return render_template('index.html', hidden_login = hidden, hidden_logout=tampil, id_session=session['id'])

       return render_template('index.html', hidden_logout=hidden, id_session=0)

@app.route('/indexAdmin')
def indexAdmin():
       return render_template('index_admin.html')

@app.route('/antrian/<int:id>', methods=['GET', 'POST'])
def antrian(id):
       
       data = getData(f"SELECT * FROM reservasi where id_user = '{id}' ")
       username = session['username']
       return render_template('antrian.html', data=data, username=username)

@app.route('/daftarMenu')
def daftar_menu():
       hidden_logout = hidden

       if 'loggedin' in session:
              hidden_logout = tampil

       data = getData("SELECT * FROM daftar_menu")
       return render_template('daftar_menu.html', data=data, hidden_logout=hidden_logout)

@app.route('/daftarPesanan')
def daftar_pesanan():
       data = getData("SELECT * FROM reservasi WHERE status = 'Pending'")
       return render_template('pesanan.html', data=data)

@app.route('/deletePesanan/<int:id>', methods=['GET', 'POST'])
def deletePesanan(id):
       route = 'daftar_pesanan'

       db = getMysqlConnection()
       cur = db.cursor()

       data = getOneData(f"SELECT meja_no FROM reservasi WHERE id_pemesanan = {id} ")

       sqlstr = f"UPDATE `reservasi` SET `status` = 'Selesai' WHERE `reservasi`.`id_pemesanan` = {id}"
       editmeja = f"UPDATE `meja` SET `status_meja` = 'Kosong' WHERE `meja`.`no_meja` = {data};"
       cur.execute(editmeja)
       db.commit()
       return deleteData(sqlstr, route)
       


@app.route('/promo')
def promo():
       # SELECT * FROM promo WHERE tanggal = CURDATE();
       hidden_jika_admin = "hidden"
       hidden_logout = hidden
       id_session =""
       if 'loggedin' in session and session['id'] == 1:
              hidden_jika_admin = hidden
       elif 'loggedin' in session:
              id_session=session['id']
              hidden_logout = tampil
              hidden_jika_admin = tampil

       data = getData("SELECT * FROM promo WHERE tanggal >= CURDATE()")
       return render_template('promo_landing.html', data = data, hidden_logout=hidden_logout, hidden_jika_admin=hidden_jika_admin, id_session=id_session)

# DASHBOARD
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

       if 'loggedin' in session:
              if session['id'] != 1:
                     return redirect(url_for('index'))
       elif not 'loggedin' in session:
              return redirect(url_for('index'))

       data_user = getData("SELECT * FROM user")
       total_reservasi = getData("SELECT * FROM reservasi")
       reservasi_pending = getData("SELECT * FROM `reservasi` WHERE `status`= 'Pending'")
       reservasi_selesai = getData("SELECT * FROM `reservasi` WHERE `status`= 'Selesai'")
       return render_template('dashboard.html', data_user = data_user, total_reservasi = total_reservasi, reservasi_pending = reservasi_pending, reservasi_selesai = reservasi_selesai)

# DATABASE USER
@app.route('/dashboardUser')
def dashboardUser():
    
       if 'loggedin' in session:
              if session['id'] != 1:
                     return redirect(url_for('index'))
       elif not 'loggedin' in session:
              return redirect(url_for('index'))

       data = getData("SELECT * from user")
       return render_template('user.html', data=data)

@app.route('/deleteUser/<int:id>')
def deleteUser(id):
    
       if 'loggedin' in session:
              if session['id'] != 1:
                     return redirect(url_for('index'))
       elif not 'loggedin' in session:
              return redirect(url_for('index'))

       route = 'dashboardUser'
       idString = str(id)
       sqlstr = "DELETE FROM user WHERE id_user="+idString+""
       return deleteData(sqlstr, route)

@app.route('/updateUser/<int:id>', methods=['GET','POST'])
def updateUser(id):
    
       if 'loggedin' in session:
              if session['id'] != 1:
                     return redirect(url_for('index'))
       elif not 'loggedin' in session:
              return redirect(url_for('index'))

       
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
    
       if 'loggedin' in session:
              if session['id'] != 1:
                     return redirect(url_for('index'))
       elif not 'loggedin' in session:
              return redirect(url_for('index'))

       data = getData("SELECT * from reservasi")
       # data = getData("SELECT * from reservasi where status='Selesai' ")
       return render_template('reservasi.html', data=data)

@app.route('/deleteReservasi/<int:id>')
def deleteReservasi(id):
    
       if 'loggedin' in session:
              if session['id'] != 1:
                     return redirect(url_for('index'))
       elif not 'loggedin' in session:
              return redirect(url_for('index'))

       route = 'dashboardReservasi'
       idString = str(id)
       sqlstr = "DELETE FROM reservasi WHERE id_pemesanan="+idString+""
       return deleteData(sqlstr, route)
       

@app.route('/updateReservasi/<int:id>', methods=['GET','POST'])
def updateReservasi(id):
    
       if 'loggedin' in session:
              if session['id'] != 1:
                     return redirect(url_for('index'))
       elif not 'loggedin' in session:
              return redirect(url_for('index'))

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
    
       if 'loggedin' in session:
              if session['id'] != 1:
                     return redirect(url_for('index'))
       elif not 'loggedin' in session:
              return redirect(url_for('index'))

       data = getData("SELECT * from meja")
       return render_template('meja.html', data=data)

@app.route('/createMeja', methods=['GET', 'POST'])
def createMeja():
    
       if 'loggedin' in session:
              if session['id'] != 1:
                     return redirect(url_for('index'))
       elif not 'loggedin' in session:
              return redirect(url_for('index'))

       meja = request.form['meja']
       keterangan = request.form['keterangan']
       route = 'dashboardMeja'
       sqlstr = "INSERT INTO meja (`no_meja`, `keterangan`) routeS ('"+meja+"', '"+keterangan+"')"
       return createData(sqlstr, route)

@app.route('/deleteMeja/<int:id>')
def deleteMeja(id):
    
       if 'loggedin' in session:
              if session['id'] != 1:
                     return redirect(url_for('index'))
       elif not 'loggedin' in session:
              return redirect(url_for('index'))

       route = 'dashboardMeja'
       idString = str(id)
       sqlstr = "DELETE FROM meja WHERE no_meja="+idString+""
       return deleteData(sqlstr, route)

@app.route('/updateMeja/<int:id>', methods=['GET','POST'])
def updateMeja(id):
    
       if 'loggedin' in session:
              if session['id'] != 1:
                     return redirect(url_for('index'))
       elif not 'loggedin' in session:
              return redirect(url_for('index'))

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
    
       if 'loggedin' in session:
              if session['id'] != 1:
                     return redirect(url_for('index'))
       elif not 'loggedin' in session:
              return redirect(url_for('index'))

       data = getData("SELECT * from promo")
       return render_template('promo.html', data=data)

@app.route('/createPromo', methods=['GET', 'POST'])
def createPromo():
    
       if 'loggedin' in session:
              if session['id'] != 1:
                     return redirect(url_for('index'))
       elif not 'loggedin' in session:
              return redirect(url_for('index'))


       if request.method == 'GET' :
              data_menu = getData("SELECT * from daftar_menu")
              return render_template('promo_create.html', data_menu=data_menu)
       
       if request.method == 'POST' :
           
              id_menu = request.form['menu']
              harga_promo = request.form['harga_akhir']
              tanggal = request.form['tanggal']
              
              harga_awal = getOneData("SELECT harga from daftar_menu where id_menu='"+id_menu+"'")
              nama_menu = getOneData("SELECT menu from daftar_menu where id_menu='"+id_menu+"'")
              route = 'dashboardPromo'
              sqlstr = "INSERT INTO `promo` (`id_promo`, `menu`, `harga_awal`, `harga_promo`, `tanggal`) VALUES (NULL, '"+nama_menu+"', '"+str(harga_awal)+"', '"+harga_promo+"', '"+tanggal+"')"
              return createData(sqlstr, route)

@app.route('/deletePromo/<int:id>')
def deletePromo(id):
    
       if 'loggedin' in session:
              if session['id'] != 1:
                     return redirect(url_for('index'))
       elif not 'loggedin' in session:
              return redirect(url_for('index'))

       route = 'dashboardPromo'
       idString = str(id)
       sqlstr = "DELETE FROM promo WHERE id_promo="+idString+""
       return deleteData(sqlstr, route)

@app.route('/updatePromo/<int:id>', methods=['GET','POST'])
def updatePromo(id):
    
       if 'loggedin' in session:
              if session['id'] != 1:
                     return redirect(url_for('index'))
       elif not 'loggedin' in session:
              return redirect(url_for('index'))

       db = getMysqlConnection()
       cur = db.cursor()

       data = getUpdateData(f"SELECT * FROM promo WHERE id_promo='{id}'", cur)

       if request.method == 'POST':
             harga_akhir = request.form['harga_akhir']
             tanggal = request.form['tanggal']
             sqlstr = f"UPDATE `promo` SET `harga_promo` = '{harga_akhir}', `tanggal` = '{tanggal}' WHERE `promo`.`id_promo` = {id}"
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
    
       if 'loggedin' in session:
              if session['id'] != 1:
                     return redirect(url_for('index'))
       elif not 'loggedin' in session:
              return redirect(url_for('index'))

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
    
       if 'loggedin' in session:
              if session['id'] != 1:
                     return redirect(url_for('index'))
       elif not 'loggedin' in session:
              return redirect(url_for('index'))

       data = getData("SELECT * FROM daftar_menu")
       return render_template('menu.html', data=data)

@app.route('/deleteMenu/<int:id>', methods=['GET', 'POST'])
def deleteMenu(id):
    
       if 'loggedin' in session:
              if session['id'] != 1:
                     return redirect(url_for('index'))
       elif not 'loggedin' in session:
              return redirect(url_for('index'))

       route = 'dashboardMenu'
       sqlstr = f"DELETE FROM daftar_menu WHERE id_menu={id}"
       return deleteData(sqlstr, route)


@app.route('/updateMenu/<int:id>', methods=['GET','POST'])
def updateMenu(id):
    
       if 'loggedin' in session:
              if session['id'] != 1:
                     return redirect(url_for('index'))
       elif not 'loggedin' in session:
              return redirect(url_for('index'))

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


@app.route('/userReservasi', methods=['GET', 'POST'])
def userReservasi():
       if not 'loggedin' in session:
              return render_template('signin.html')
       
       db = getMysqlConnection()
       cur = db.cursor()

       data_meja = getData(f"SELECT * FROM meja WHERE status_meja = 'Kosong' ")
       
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
             id_user = session['id']
             sqlstr = f"INSERT INTO `reservasi` (`id_pemesanan`, `nama`, `email`, `telp`, `jum_tamu`, `tanggal`, `jam`, `tambahan`, `id_user`, `meja_no`, `ket_meja`, `status`) VALUES (NULL, '{nama}', '{email}', '{telepon}', '{jml_tamu}', '{tanggal}', '{jam}', '{layanan}', '{id_user}', '{strmeja}', '{keterangan_meja}', '{status}')"
             cur.execute(sqlstr)
             db.commit()

             editmeja = f"UPDATE `meja` SET `status_meja` = 'Terisi' WHERE `meja`.`no_meja` = {strmeja};"
             cur.execute(editmeja)
             db.commit()

             cur.close()
             db.close()
             return redirect(url_for('promo'))
       else:
             cur.close()
             db.close()
             return render_template('reservasi_user.html', data_meja=data_meja, disabled='') 

#LOGIN
@app.route('/login', methods=['GET','POST'])
def login():
       
       if 'loggedin' in session and session['id'] == 1:
              return redirect(url_for('indexAdmin'))
       
       elif 'loggedin' in session:
              return render_template('index.html', hidden_login = hidden, hidden_logout=tampil, id_session=session['id'])

       db = getMysqlConnection()
       cur = db.cursor()
       # Memeriksa apakah "username" dan "password" POST telah di isi (input pengguna)
       if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
              username = request.form['username']
              password = request.form['password']

              data = getUpdateData(f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}';",cur)
              # jika datanya true (ada pada database)
              if data:
                     # membuat data sesi, data ini akan diakses route lain
                     session['loggedin'] = True
                     session['id'] = data[0]
                     session['username'] = data[1]
                     
                     if 'loggedin' in session and session['id'] == 1:
                            return render_template('index_admin.html')

                     return render_template('index.html', hidden_login=hidden, hidden_logout=tampil, id_session=session['id'])
              else:
                     # jika data username dan password salah
                     gagal = "username atau password anda salah"
                     gagal_hidden = ""
                     return render_template('signin.html', gagal=gagal, gagal_hidden=gagal_hidden)
       return render_template('signin.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    # cek apakah username,password, password2 sudah dikirim melalui POST (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'password2' in request.form:
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']

        db = getMysqlConnection()
        cur = db.cursor()
        cur.execute('SELECT * FROM user WHERE username = %s', (username,))
        account = cur.fetchone()
        # Jika username sudah ada pada database
        if account:
            msg = 'Account already exists!'
        # Jika terdapat kesalahan pada re-type password
        elif password != password2:
            msg = 'Invalid password!'
        # Jika pengguna belum mengisi form username ataupun password
        elif not username or not password:
            msg = 'Please fill out the form!'
        else:
            # jika semua ketentuan sudah terpenuhi
            cur.execute(f"INSERT INTO `user` (`id_user`, `username`, `password`) VALUES (NULL, '{username}', '{password}')")
            db.commit()
            msg = 'You have successfully registered!'  
        
    # Pemberitahuan keterangan 
    return render_template('signup.html', msg=msg)

@app.route('/logout')
def logout():
       # Remove session data, this will log the user out
       session.pop('loggedin', None)
       session.pop('id', None)
       session.pop('username', None)
       # Redirect to login page
       return render_template('index.html', hidden_logout=hidden, hidden_login=tampil, id_session=0)





if __name__ == '__main__':
    app.run(debug=True)
