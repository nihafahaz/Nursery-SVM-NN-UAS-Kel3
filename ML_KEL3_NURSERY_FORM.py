# import required libraries
import streamlit as st
import os
import json
import pickle

# loading the model to predict on the data
try:
    model = pickle.load(open('rbf_model', 'rb'))
except Exception as e:
    st.error(f"Error loading model: {e}")

# Encoding mappings
finance_mapping = {'Stabil': 0, 'Tidak/Kurang Stabil': 1}
social_mapping = {'Dapat bersosialisasi dengan baik': 0, 'Bermasalah, sulit bersosialisasi': 1, 'Sedikit bermasalah, perlu perhatian khusus': 2}
health_mapping = {'Kurang sehat/kondisi fisik-rohani lemah': 0, 'Sehat jasmani-rohani': 1, 'Sehat (secara umum)': 2}

# fungsi untuk mengambil inputan user
def prediction(social, finance, health):
    # map inputs to encoded value
    finance_encoded = finance_mapping[finance]
    social_encoded = social_mapping[social]
    health_encoded = health_mapping[health]

    # cek kesesuaian
    print(f"Encoded values: Finance: {finance_encoded}, Social: {social_encoded}, Health: {health_encoded}")

    # membuat prediksi model 
    prediction = model.predict(
        [[social_encoded, finance_encoded, health_encoded]]
    )

    return prediction[0]


def save_data_to_json(email, name, tempat, tanggal_lahir, jnsKelamin, finance, social, health, result):
    # Validasi input yang harus diisi
    if not email or not name or not tempat:
        st.error("Email, Nama, dan Tempat Lahir harus diisi! (disarankan ketik manual)")
        return False  # Menghentikan fungsi jika ada input yang kosong
    
    data = {
        "email": email,
        "name": name,
        "tempat_lahir": tempat,
        "tanggal_lahir": tanggal_lahir.strftime('%Y-%m-%d'),  # Convert date to string
        "jenis_kelamin": jnsKelamin,
        "keuangan": finance,
        "kehidupan_sosial": social,
        "kesehatan": health,
        "result": int(result)  # Convert result to int to make it JSON serializable
    }

    file_name = 'data_anak_lolos.json'

    # Check if the file exists and is not empty
    if os.path.exists(file_name):
        try:
            with open(file_name, 'r') as file:
                existing_data = json.load(file)
        except json.JSONDecodeError:  # Handle the case of an empty or invalid JSON file
            existing_data = []
    else:
        existing_data = []

    # Append new data
    existing_data.append(data)

    # Save updated data back to the file
    try:
        with open(file_name, 'w') as file:
            json.dump(existing_data, file, indent=4)
        st.success("Data berhasil disimpan!")
        return True  # Mengembalikan True jika data berhasil disimpan
    except Exception as e:
        st.error(f"Error while saving data: {e}")
        return False

def main():
    # Title and intro text
    st.title('Pendaftaran Anak PAUD')
    st.write('By Kelompok 3')
    long_text = ">>> Isi formulir ini dengan sepenuh hati. Pastikan semua informasi yang Anda berikan adalah yang sebenarnya. <<<"
    st.markdown(f'<div style="white-space: pre-wrap;">{long_text}</div>', unsafe_allow_html=True)

    # User input fields
    email = st.text_input("Masukkan alamat email Anda: ")
    name = st.text_input("Masukkan nama putra/i Anda: ")
    tempat = st.text_input("Tempat lahir putra/i Anda:")
    tanggal_lahir = st.date_input("Tanggal lahir:")
    jnsKelamin = st.radio("Pilih jenis kelamin", ("Laki-laki", "Perempuan"))

    # Input data atribut yang dimasukkan ke model
    finance_opt = ['Stabil', 'Tidak/Kurang Stabil']
    finance = st.selectbox("Keuangan Orang Tua", finance_opt)

    social_opt = ['Dapat bersosialisasi dengan baik', 'Sedikit bermasalah, perlu perhatian khusus', 'Bermasalah, sulit bersosialisasi']
    social = st.selectbox("Kehidupan Sosial Anak", social_opt)

    health_opt = ['Sehat jasmani-rohani', 'Sehat (secara umum)', 'Kurang sehat/kondisi fisik-rohani lemah']
    health = st.selectbox("Kesehatan Anak", health_opt)

    # Initialize result
    result = ""

    # Check if the necessary inputs are filled
    if not email or not name or not tempat:
        st.error("Email, Nama, dan Tempat Lahir harus diisi!")
    else:
        # Prediction button
        if st.button("Submit"):
            result = prediction(social, finance, health)  # Only predict if inputs are valid
            print("result kelas", result)

            if result == 1:
                output_message = "Selamat! Kami dengan penuh sukacita mengumumkan bahwa anak Anda telah diterima di PAUD."
                if save_data_to_json(email, name, tempat, tanggal_lahir, jnsKelamin, finance, social, health, result):
                    st.success(output_message)
            elif result == 2:
                output_message = "Selamat! Anak Anda diterima di PAUD. Kami sangat senang menyambutnya di keluarga kami."
                if save_data_to_json(email, name, tempat, tanggal_lahir, jnsKelamin, finance, social, health, result):
                    st.success(output_message)
            elif result == 0:
                output_message = "Maaf, anak Anda tidak diterima di PAUD kali ini. Terima kasih atas partisipasi Anda!"
                st.success(output_message)



if __name__ == '__main__':
    main()
