from pipelines import create_anamnesis_pipe, create_followup_pipe

anamnesis_pipe = create_anamnesis_pipe()
followup_pipe = create_followup_pipe()

prompt = "Pasien laki-laki berusia 59 tahun datang dengan keluhan bercak merah kehitaman disertai rasa gatal yang telah dirasakan sejak 4 tahun yang lalu, awalnya muncul di siku kanan lalu menyebar ke siku kiri, kedua tungkai bawah, kedua lengan, dan punggung. Pasien mengeluhkan gatal yang memburuk saat berkeringat dan memiliki kulit yang cenderung kering (xerosis), dengan perjalanan penyakit yang dipengaruhi oleh faktor lingkungan dan emosi. Pasien memiliki riwayat diabetes melitus, riwayat penyakit serupa sebelumnya, serta riwayat asma bronkial yang mengindikasikan adanya faktor atopi, didukung pula dengan riwayat atopi dalam keluarga seperti asma bronkial, rinitis alergi, dan dermatitis atopik. Selain itu, pasien melaporkan adanya keringat berlebih pada suhu panas maupun dingin yang turut memperberat rasa gatal, dengan bercak merah kehitaman ditemukan pada pipi, leher, punggung kaki, tungkai, pelipis, dan tangan. Keluhan ini telah berlangsung lebih dari 4 minggu tanpa perbaikan yang signifikan."

response = anamnesis_pipe.run({"prompt": prompt})
response = response["llm"]["replies"][0]
parsed_response = response.split("\n")
data_dict = dict(item.strip().split(": ", 1) for item in parsed_response)
print(data_dict)
unprovided_params = [key for key, value in data_dict.items() if value == "None"]

response = followup_pipe.run(
    {"unprovided_params": unprovided_params, "previous_question": prompt}
)
response = response["llm"]["replies"][0]
print(response)
