from waitress import serve
from app import app  # Mengimpor object 'app' dari file app.py

# Menjalankan server produksi Waitress
# Host '0.0.0.0' berarti server bisa diakses dari luar localhost
# Port 8080 adalah port umum untuk aplikasi web
if __name__ == '__main__':
    print("Server produksi dijalankan pada http://localhost:8080/")
    serve(app, host='localhost', port=8080)