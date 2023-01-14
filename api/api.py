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


#BASE MODELS
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
    execute(insertQuery.format(
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
        reservasi.status))

    return {"message":"success"}


@app.post("/api/updateReservasi/{id}")
async def updateReservasi(id: int, reservasi: Reservasi):
    updateQuery = """
    UPDATE reservasi SET 
    id_pemesanan = '{0}', nama = '{1}', email = '{2}', telp = '{3}', jum_tamu = '{4}', 
    tanggal = '{5}', jam = '{6}', tambahan = '{7}', id_user = '{8}', meja_no = '{9}', 
    ket_meja = '{10}', status = '{11}' WHERE reservasi.id_pemesanan = {12}
    """
    execute(updateQuery.format(
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
        id))

    return {"message":"success"}

@app.delete("/api/deleteReservasi/{id}")
def deleteReservasi(id):
    execute("DELETE FROM reservasi WHERE id_pemesanan='{}'".format(id))

    return{"message":"success"}

@app.get("/api/get")
async def get_():

    return {}


@app.get("/api/get")
async def get_():

    return {}


@app.get("/api/get")
async def get_():

    return {}
