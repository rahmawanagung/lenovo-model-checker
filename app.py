from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor
import os
import pathlib

# Dapatkan path direktori saat ini menggunakan pathlib (lebih andal)
basedir = pathlib.Path(__file__).parent.resolve()

app = Flask(__name__)

# Buat path absolut untuk folder upload dan pastikan folder itu ada
UPLOAD_FOLDER = basedir / "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)

def get_model_info(serial_number):
    """
    Mengambil informasi Model Laptop untuk satu nomor seri.
    """
    url = f"https://pcsupport.lenovo.com/us/en/api/v4/mse/getproducts?productId={serial_number}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data and data[0].get('Name'):
            product_info = data[0]
            # HANYA MENGAMBIL MODEL LAPTOP
            return {
                "Model Laptop": product_info.get('Name', 'Tidak Ditemukan')
            }
        else:
            return {"Model Laptop": "Tidak Ditemukan"}
    except requests.exceptions.RequestException as e:
        print(f"Error pada SN {serial_number}: {e}")
        return {"Model Laptop": "Error"}

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            output_filename = f"result_model_{filename}"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            
            file.save(input_path)
            
            df_input = pd.read_excel(input_path)
            serial_numbers = df_input['SerialNumber'].tolist()

            with ThreadPoolExecutor(max_workers=10) as executor:
                results = list(executor.map(get_model_info, serial_numbers))

            result_df = pd.DataFrame(results)

            # Membuat DataFrame output yang bersih
            # Hanya berisi kolom SerialNumber dari file asli dan Model Laptop dari hasil proses
            df_output = pd.DataFrame({
                'SerialNumber': df_input['SerialNumber'],
                'Model Laptop': result_df['Model Laptop']
            })

            # Menyimpan DataFrame baru yang sudah bersih ke Excel
            df_output.to_excel(output_path, index=False)
            
            return send_from_directory(
                directory=app.config['UPLOAD_FOLDER'], 
                path=output_filename, 
                as_attachment=True
            )
    
    return render_template('index.html')