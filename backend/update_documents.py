from haystack import Document
import pandas as pd

from pipelines import create_storing_pipe

storing_pipe = create_storing_pipe()

# Prepare the documents
data_da = pd.read_csv("dataset/data_da_train_cleaned.csv")
data_non_da = pd.read_csv("dataset/data_non_da_train_cleaned.csv")
combined_df = pd.concat([data_da, data_non_da], ignore_index=True)

# Create some example documents
documents = []
for _, row in combined_df.iterrows():
    content = f"main complaint: {row['main_complaint']}"
    content += f"\npatient age: {row['patient_age']}"
    content += f"\ncontact history: {row['contact_history']}"
    content += f"\ninfection source: {row['infection_source']}"
    content += f"\nother source: {row['other_source']}"
    content += f"\ntrigger factors: {row['trigger_factors']}"
    content += f"\nillness duration: {row['illness_duration']}"
    content += f"\npast history: {row['past_history']}"
    content += f"\nfamily history: {row['family_history']}"
    # content += f"\ndisease type: {row['classname']}\n\n"

    documents.append(Document(content=content, meta={"class": row["classname"]}))

storing_pipe.run({"doc_embedder": {"documents": documents}})
