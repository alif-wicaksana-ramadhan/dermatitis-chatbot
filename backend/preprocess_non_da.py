import pandas as pd
import re
from sklearn.model_selection import train_test_split


def to_snake_case(name):
    name = re.sub(
        r"(?<!^)(?=[A-Z])", "_", name
    )  # Add underscore before capital letters
    name = re.sub(r"[\s]+", "_", name)  # Replace spaces with underscores
    name = re.sub(
        r"[^\w]", "_", name
    )  # Replace non-alphanumeric characters with underscores
    return name.lower()  # Convert to lowercase


# Path ke file Excel
file_path = "dataset/data_non_da.xlsx"
output_path = "dataset/data_non_da_cleaned.csv"

# Membaca ulang data dari file
df = pd.read_excel(file_path, sheet_name="Form Responses 1")

# Memilih hanya kolom tertentu
selected_columns = [
    df.columns[4],  # Kolom ke-1
    df.columns[5],  # Kolom ke-2
    df.columns[6],  # Kolom ke-3
    df.columns[7],  # Kolom ke-4
    df.columns[8],  # Kolom ke-5
    df.columns[9],  # Kolom ke-6
    df.columns[11],  # Kolom ke-7
    df.columns[13],  # Kolom ke-12
    df.columns[14],  # Kolom ke-13
]

column_renaming = {
    "usia__pasien": "patient_age",
    "keluhan__utama_dan__onset": "main_complaint",
    "riwayat__kontak_dengan__bahan__alergen_atau__iritan_": "contact_history",
    "sumber__infeksi": "infection_source",
    "apabila_memilih___lain___lain__pada_pertanyaan_sebelumnya__harap_sebutkan_sumber_infeksinya": "other_source",
    "faktor__pencetus__penyakit__sekarang_": "trigger_factors",
    "lama__sakit": "illness_duration",
    "riwayat__penyakit__dahulu": "past_history",
    "riwayat__penyakit__keluarga": "family_history",
}

# Membuat subset data dengan kolom yang dipilih
df_selected = df[selected_columns]
data_cleaned = df_selected.drop_duplicates()
data_cleaned.columns = [to_snake_case(col) for col in data_cleaned.columns]
# data_cleaned["class"] = "non dermatitis atopic"
data_cleaned = data_cleaned.rename(columns=column_renaming)
data_cleaned.loc[:, "classname"] = "non dermatitis atopic"
# print(len(data_cleaned.index))

train_df, test_df = train_test_split(data_cleaned, test_size=0.2, random_state=42)

train_df.to_csv("dataset/data_non_da_train_cleaned.csv", index=False)
test_df.to_csv("dataset/data_non_da_test_cleaned.csv", index=False)

data_cleaned.to_csv(output_path, index=False)
