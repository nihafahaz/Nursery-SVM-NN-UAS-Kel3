# import required library
import streamlit as st
import pickle
import json
import os  # Import os to check if file exists

# loading the model to predict on the data
try:
    model = tf.keras.models.load_model('modelANN2.h5')
except Exception as e:
    st.error(f"Error loading model: {e}")

# Encoding mappings
finance_mapping = {'Stabil': 0, 'Tidak/Kurang Stabil': 1}
social_mapping = {'Dapat bersosialisasi dengan baik': 0, 'Bermasalah, sulit bersosialisasi': 1, 'Sedikit bermasalah, perlu perhatian khusus': 2}
health_mapping = {'Kurang sehat/kondisi fisik-rohani lemah': 0, 'Sehat jasmani-rohani': 1, 'Sehat (secara umum)': 2}
parents_mapping = {'Great Pretentious': 0, 'Pretentious': 1, 'Kalangan Umum': 2}
has_nurs_mapping = {'Critical': 0, 'Tidak Proper': 1, 'Kurang Proper/Baik': 2, 'Sangat Baik': 3}
form_mapping = {'Lengkap': 0, 'Terpenuhi': 1, 'Keluarga Asuh': 2, 'Tidak Lengkap': 3}
children_mapping = {'1': 0, '2': 1, '3': 2, 'Lebih dari 3': 3}
housing_mapping = {'Baik': 0, 'Critical': 1, 'Kurang baik': 2}

# PCA initialization
pca = PCA(n_components=6)  # Since PCA is reducing to 6 components

# Load your PCA transformation matrix
pca_components = np.array([[-1.25718073e-03, 9.99897781e-01, 1.25525987e-02, 2.96572896e-03,
                            -2.40280869e-03, -3.91688915e-03, 3.91249057e-03, 2.44537557e-04],
                           [2.21585840e-03, -9.18134006e-03, 8.54527864e-01, -5.19246423e-01,
                            -6.28324991e-03, 5.07124132e-03, 1.39635763e-04, 3.29530429e-03],
                           [-4.40129123e-05, -9.03556312e-03, 5.19173591e-01, 8.54504377e-01,
                            -1.97623026e-05, 2.53699465e-03, -8.54116394e-04, -1.38651731e-02],
                           [6.18842968e-01, 1.11388862e-03, -1.18795885e-03, 9.22394965e-03,
                            -4.22222560e-01, 8.31146001e-03, -3.74139514e-01, 5.46465280e-01],
                           [8.48987463e-04, 3.40603544e-03, 6.04562430e-03, 2.05762678e-03,
                            8.37927230e-01, 3.31868171e-03, -3.96649672e-01, 3.74810455e-01],
                           [-3.12073689e-02, -3.08388408e-03, 3.48332682e-03, 8.82976970e-03,
                            8.41964853e-02, -4.52705656e-04, 7.72182926e-01, 6.28944169e-01]])

pca.fit(pca_components)  # Fit your PCA model based on your data

# Function to take user input and transform it for PCA
def prediction(parents, has_nurs, form, children, housing, finance, social, health):
    # Encoding the user input
    parents_encoded = parents_mapping[parents]
    has_nurs_encoded = has_nurs_mapping[has_nurs]
    form_encoded = form_mapping[form]
    children_encoded = children_mapping[str(children)]
    housing_encoded = housing_mapping[housing]
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

def save_data_to_json(email, name, tempat, tanggal_lahir, jnsKelamin, parents, has_nurs, form, children, housing, finance, social, health, result):
    data = {
        "email": email,
        "name": name,
        "tempat_lahir": tempat,
        "tanggal_lahir": tanggal_lahir.strftime('%Y-%m-%d'),  # Convert date to string
        "jenis_kelamin": jnsKelamin,
        "status_ortu": parents,
        "kamar_anak": has_nurs,
        "kelengkapan_keluarga": form,
        "jumlah_anak": children,
        "kondisi_tmpt_tinggal": housing,
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

    # Inputs for PCA
    parents_opt = ['Great Pretentious', 'Pretentious', 'Kalangan Umum']
    parents = st.selectbox("Status Orang Tua", parents_opt)

    has_nurs_opt = ['Critical', 'Tidak Proper', 'Kurang Proper/Baik', 'Sangat Baik']
    has_nurs = st.selectbox("Kondisi kamar anak", has_nurs_opt)

    form_opt = ['Lengkap', 'Terpenuhi', 'Keluarga Asuh', 'Tidak Lengkap']
    form = st.selectbox("Kelengkapan keluarga", form_opt)

    children_opt = ['1', '2', '3', 'Lebih dari 3']
    children = st.selectbox("Jumlah anak", form_opt)

    housing_opt = ['Baik', 'Critical', 'Kurang baik']
    housing = st.selectbox("Kondisi tempat tinggal", housing_opt)

    finance_opt = ['Stabil', 'Tidak/Kurang Stabil']
    finance = st.selectbox("Keuangan Orang Tua", finance_opt)

    social_opt = ['Dapat bersosialisasi dengan baik', 'Sedikit bermasalah, perlu perhatian khusus', 'Bermasalah, sulit bersosialisasi']
    social = st.selectbox("Kehidupan Sosial Anak", social_opt)

    health_opt = ['Sehat jasmani-rohani', 'Sehat (secara umum)', 'Kurang sehat/kondisi fisik-rohani lemah']
    health = st.selectbox("Kesehatan Anak", health_opt)

    # Initialize result
    result = ""

    # predict button
    if st.button("Submit"):
        result = prediction(social, finance, health)
        print(result)

        if result == 1 or result == 3:
            output_message = "Selamat! Kami dengan penuh sukacita mengumumkan bahwa anak Anda telah diterima di PAUD."
            save_data_to_json(email, name, tempat, tanggal_lahir, jnsKelamin, parents, has_nurs, form, children, housing, finance, social, health, result)
        elif result == 2 or result == 4:
            output_message = "Selamat! Anak Anda diterima di PAUD. Kami sangat senang menyambutnya di keluarga kami."
            save_data_to_json(email, name, tempat, tanggal_lahir, jnsKelamin, parents, has_nurs, form, children, housing, finance, social, health, result)
        elif result == 0:
            output_message = "Maaf, anak Anda tidak diterima di PAUD kali ini. Kami mengucapkan terima kasih atas partisipasi Anda dan semoga sukses di masa depan!"

        st.success(output_message)

if __name__=='__main__':
    main()