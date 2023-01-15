from fastapi import FastAPI
from pydantic import BaseModel
from api.db import *


app = FastAPI(title="Mie Ayam bang Willi - API Services", version="1.0.0")


async def convert_timedelta(waktu):
    detik = waktu.seconds
    jam = detik // 3600
    menit = (detik % 3600) // 60
    detik = detik % 60
    return "{0}:{1}:{2}".format(jam, menit, detik)


# BASE MODELS
class Reservasi(BaseModel):
    id_pemesanan: int
    nama: str
    email: str
    telp: str
    jum_tamu: int
    tanggal: str
    jam: str
    tambahan: str
    id_user: int
    meja_no: int
    ket_meja: str
    status: str

class Promo(BaseModel):
    id_promo: int
    menu: str
    harga_awal: int
    harga_promo: int
    tanggal: str

class Meja(BaseModel):
    no_meja: int
    keterangan: str
    status_meja: str

class User(BaseModel):
    id_user: int
    username: str
    password: str

class DaftarMenu(BaseModel):
    id_menu: int
    menu: str
    harga: int
    path: str

# INDEX API
@app.get("/api/")
async def index():
    return {
        "description": "Mie Ayam Bang Willi's API, created and developed by Kelompok 4"
    }


# API RESERVASI
@app.get("/api/getReservasi")
async def getReservasi():
    content = {}
    content["data_reservasi"] = []
    data = getData("SELECT * FROM reservasi")

    for i in data:
        jam = convert_timedelta(i[6])

        content["data_reservasi"].append(
            {
                "id_pemesanan": i[0],
                "nama": i[1],
                "email": i[2],
                "telepon": i[3],
                "jumlah_tamu": i[4],
                "tanggal": i[5],
                "jam": jam,
                "tambahan": i[7],
                "id_user": i[8],
                "no_meja": i[9],
                "ket_meja": i[10],
                "status": i[11],
            }
        )

    return content


@app.get("/api/getReservasiById/{id_pemesanan}")
async def getReservasiById(id_pemesanan: int):
    content = {}
    content["data_reservasi"] = []
    data = getData(
        "SELECT * FROM reservasi WHERE id_pemesanan='{}'".format(id_pemesanan)
    )

    for i in data:
        jam = convert_timedelta(i[6])

        content["data_reservasi"].append(
            {
                "id_pemesanan": i[0],
                "nama": i[1],
                "email": i[2],
                "telepon": i[3],
                "jumlah_tamu": i[4],
                "tanggal": i[5],
                "jam": jam,
                "tambahan": i[7],
                "id_user": i[8],
                "no_meja": i[9],
                "ket_meja": i[10],
                "status": i[11],
            }
        )

    return content


@app.post("/api/createReservasi/")
async def createReservasi(reservasi: Reservasi):
    insertQuery = """
    INSERT INTO reservasi(id_pemesanan, nama, email, telp, jum_tamu, tanggal, jam, tambahan, id_user, meja_no, ket_meja, status) 
    VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}')
    """
    execute(
        insertQuery.format(
            reservasi.id_pemesanan,
            reservasi.nama,
            reservasi.email,
            reservasi.telp,
            reservasi.jum_tamu,
            reservasi.tanggal,
            reservasi.jam,
            reservasi.tambahan,
            reservasi.id_user,
            reservasi.meja_no,
            reservasi.ket_meja,
            reservasi.status,
        )
    )

    return {"message": "success"}


@app.post("/api/updateReservasi/{id}")
async def updateReservasi(id: int, reservasi: Reservasi):
    updateQuery = """
    UPDATE reservasi SET 
    id_pemesanan = '{0}', nama = '{1}', email = '{2}', telp = '{3}', jum_tamu = '{4}', 
    tanggal = '{5}', jam = '{6}', tambahan = '{7}', id_user = '{8}', meja_no = '{9}', 
    ket_meja = '{10}', status = '{11}' WHERE reservasi.id_pemesanan = {12}
    """
    execute(
        updateQuery.format(
            reservasi.id_pemesanan,
            reservasi.nama,
            reservasi.email,
            reservasi.telp,
            reservasi.jum_tamu,
            reservasi.tanggal,
            reservasi.jam,
            reservasi.tambahan,
            reservasi.id_user,
            reservasi.meja_no,
            reservasi.ket_meja,
            reservasi.status,
            id,
        )
    )

    return {"message": "success"}


@app.delete("/api/deleteReservasi/{id}")
def deleteReservasi(id):
    execute("DELETE FROM reservasi WHERE id_pemesanan='{}'".format(id))

    return {"message": "success"}


# API PROMO
@app.get("/api/getPromo")
async def getPromo():
    content = {}
    content["data_promo"] = []
    data = getData("SELECT * FROM promo")

    for i in data:

        content["data_promo"].append(
            {
                "id_promo": i[0],
                "menu": i[1],
                "harga_awal": i[2],
                "harga_promo": i[3],
                "tanggal": i[4]
            }
        )

    return content


@app.get("/api/getPromoById/{id_promo}")
async def getPromoById(id_promo: int):
    content = {}
    content["data_promo"] = []
    data = getData(
        "SELECT * FROM promo WHERE id_promo='{}'".format(id_promo)
    )

    for i in data:

        content["data_promo"].append(
            {
                "id_promo": i[0],
                "menu": i[1],
                "harga_awal": i[2],
                "harga_promo": i[3],
                "tanggal": i[4]
            }
        )

    return content


@app.post("/api/createPromo/")
async def createPromo(promo: Promo):
    insertQuery = """
    INSERT INTO promo(id_promo, menu, harga_awal, harga_promo, tanggal) VALUES ('{0}','{1}','{2}','{3}','{4}')
    """
    execute(
        insertQuery.format(
            promo.id_promo,
            promo.menu,
            promo.harga_awal,
            promo.harga_promo,
            promo.tanggal
        )
    )

    return {"message": "success"}


@app.post("/api/updatePromo/{id}")
async def updatePromo(id: int, promo: Promo):
    updateQuery = """
    UPDATE promo SET 
    id_promo = '{0}', menu = '{1}', harga_awal = '{2}', harga_promo = '{3}', tanggal = '{4}' WHERE promo.id_promo = {5}
    """
    execute(
        updateQuery.format(
            promo.id_promo,
            promo.menu,
            promo.harga_awal,
            promo.harga_promo,
            promo.tanggal,
            id
        )
    )

    return {"message": "success"}


@app.delete("/api/deletePromo/{id}")
def deletePromo(id):
    execute("DELETE FROM promo WHERE id_promo='{}'".format(id))

    return {"message": "success"}


# API MEJA


# API DAFTAR MENU
@app.get("/api/get")
async def get_():

    return {}

# API USER
@app.get("/api/get")
async def get_():

    return {}
