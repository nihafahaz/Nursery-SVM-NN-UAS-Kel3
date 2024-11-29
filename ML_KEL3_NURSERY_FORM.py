# import required library
import streamlit as st
import pickle
import json
import os  # Import os to check if file exists

# loading the model to predict on the data
try:
    model = pickle.load(open('rbf_model.pkl', 'rb'))
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
    data = {
        "email": email,
        "name": name,
        "tempat_lahir": tempat,
        "tanggal_lahir": tanggal_lahir.strftime('%Y-%m-%d'),  # Convert date to string
        "jenis_kelamin": jnsKelamin,
        "keuangan": finance,
        "kehidupan_sosial": social,
        "kesehatan": health,
        "result": result
    }

    file_name = 'data_anak_lolos.json'

    # Check if the file exists
    if os.path.exists(file_name):
        # Read existing data
        with open(file_name, 'r') as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    # Append new data
    existing_data.append(data)

    # Save updated data
    with open(file_name, 'w') as file:
        json.dump(existing_data, file, indent=4)

def main():
    # judul program
    st.title('Pendaftaran Anak PAUD')
    st.write('By Kelompok 3')
    long_text = ">>> Isi formulir ini dengan sepenuh hati. Pastikan semua informasi yang Anda berikan adalah yang sebenarnya. <<<"
    st.markdown(f'<div style="white-space: pre-wrap;">{long_text}</div>', unsafe_allow_html=True)

    #input data by user
    email = st.text_input("Masukkan alamat email Anda: ")
    name = st.text_input("Masukkan nama putra/i Anda: ")
    tempat = st.text_input("Tempat lahir putra/i Anda:")
    tanggal_lahir = st.date_input("Tanggal lahir:")
    jnsKelamin = st.radio("Pilih jenis kelamin", ("Laki-laki", "Perempuan"))

    # input data yang akan dimasukkan ke model
    finance_opt = ['Stabil', 'Tidak/Kurang Stabil']
    finance = st.selectbox("Keuangan Orang Tua", finance_opt)

    social_opt = ['Dapat bersosialisasi dengan baik', 'Sedikit bermasalah, perlu perhatian khusus', 'Bermasalah, sulit bersosialisasi']
    social = st.selectbox("Kehidupan Sosial Anak", social_opt)

    health_opt = ['Sehat jasmani-rohani', 'Sehat (secara umum)', 'Kurang sehat/kondisi fisik-rohani lemah']
    health = st.selectbox("Kesehatan Anak", health_opt)

    # inisialisasi variabel result
    result=""

    # predict button
    if st.button("Submit"):
        result = prediction(social, finance, health)
        print(result)

        if result == 1:
            output_message = "Selamat! Anak Anda diterima di PAUD. Kami sangat senang menyambutnya di keluarga kami. Informasi lebih lanjut akan dikirim ke email yang terdaftar dalam formulir."
            save_data_to_json(email, name, tempat, tanggal_lahir, jnsKelamin, finance, social, health, result)
        elif result == 2:
            output_message = "Selamat! Kami dengan penuh sukacita mengumumkan bahwa anak Anda telah diterima di PAUD. Betapa senangnya kami menyambutnya sebagai bagian dari keluarga besar kami! Informasi lebih lanjut akan segera dikirimkan ke email yang terdaftar pada formulir."
            save_data_to_json(email, name, tempat, tanggal_lahir, jnsKelamin, finance, social, health, result)
        elif result == 0:
            output_message = "Maaf, anak Anda tidak diterima di PAUD kali ini. Kami mengucapkan terima kasih atas partisipasi Anda dan semoga sukses di masa depan!"

        st.success(output_message)

if __name__=='__main__':
    main()