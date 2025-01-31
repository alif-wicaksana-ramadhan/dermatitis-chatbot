import os
import pandas as pd
from haystack import Pipeline, Document
from haystack.utils import Secret
from haystack.document_stores.types import DuplicatePolicy
from haystack.components.writers import DocumentWriter
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.embedders import (
    SentenceTransformersDocumentEmbedder,
    SentenceTransformersTextEmbedder,
)
from haystack_integrations.document_stores.mongodb_atlas import (
    MongoDBAtlasDocumentStore,
)
from haystack_integrations.components.retrievers.mongodb_atlas import (
    MongoDBAtlasEmbeddingRetriever,
)

os.environ["MONGO_CONNECTION_STRING"] = (
    "mongodb+srv://iros:riset1231@cluster0.pkadj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

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
    content += f"\ndisease type: {row['classname']}\n\n"

    documents.append(Document(content=content, meta={"class": row["classname"]}))

    # documents.append(
    #     Document(
    #         content=row["main_complaint"],
    #         meta={
    #             "patient_age": row["patient_age"],
    #             "contact_history": row["contact_history"],
    #             "infection_source": row["infection_source"],
    #             "other_source": row["other_source"],
    #             "trigger_factors": row["trigger_factors"],
    #             "illness_duration": row["illness_duration"],
    #             "past_history": row["past_history"],
    #             "family_history": row["family_history"],
    #             "class": row["class"],
    #         },
    #     )
    # )


document_store = MongoDBAtlasDocumentStore(
    database_name="dermatitis_db",
    collection_name="raw_collections",
    vector_search_index="vector_index",
)
doc_writer = DocumentWriter(document_store=document_store, policy=DuplicatePolicy.SKIP)
doc_embedder = SentenceTransformersDocumentEmbedder()
query_embedder = SentenceTransformersTextEmbedder()

storing_pipe = Pipeline()
storing_pipe.add_component(instance=doc_embedder, name="doc_embedder")
storing_pipe.add_component(instance=doc_writer, name="doc_writer")

storing_pipe.connect("doc_embedder.documents", "doc_writer.documents")
storing_pipe.run({"doc_embedder": {"documents": documents}})

# prompt_template = """
# Given these documents, answer whether it is classified as 'dermatitis atopik' or 'non dermatitis atopik' based on the given documents. answer with the same language as the language used in the question.
# \nDocuments:
# {% for doc in documents %}
#     {{ doc.content }}

# {% endfor %}

# \nQuestion: {{question}}
# \nAnswer:
# """

prompt_template = """
{% for doc in documents %}
    {{ doc.meta.class }}
{% endfor %}
"""

rag_pipeline = Pipeline()
rag_pipeline.add_component(instance=query_embedder, name="query_embedder")
rag_pipeline.add_component(
    instance=MongoDBAtlasEmbeddingRetriever(document_store=document_store, top_k=1),
    name="retriever",
)
rag_pipeline.add_component(
    instance=PromptBuilder(template=prompt_template), name="prompt_builder"
)
# rag_pipeline.add_component(
#     instance=OpenAIGenerator(
#         model="gpt-4o-mini",
#         api_key=Secret.from_token(),
#     ),
#     name="llm",
# )
rag_pipeline.connect("query_embedder", "retriever")
rag_pipeline.connect("retriever", "prompt_builder.documents")
# rag_pipeline.connect("prompt_builder", "llm")


test_da = pd.read_csv("dataset/data_da_test_cleaned.csv")
test_non_da = pd.read_csv("dataset/data_non_da_test_cleaned.csv")

n_true = 0
n_total = 0

for _, row in test_da.iterrows():
    question = f"main complaint: {row['main_complaint']}"
    question += f"\npatient age: {row['patient_age']}"
    question += f"\ncontact history: {row['contact_history']}"
    question += f"\ninfection source: {row['infection_source']}"
    question += f"\nother source: {row['other_source']}"
    question += f"\ntrigger factors: {row['trigger_factors']}"
    question += f"\nillness duration: {row['illness_duration']}"
    question += f"\npast history: {row['past_history']}"
    question += f"\nfamily history: {row['family_history']}"

    label = row["classname"]

    result = rag_pipeline.run(
        {
            "query_embedder": {"text": question},
            # "prompt_builder": {"question": question},
        }
    )

    result = (
        result["prompt_builder"]["prompt"]
        .replace("\n    ", "")
        .replace("\n", ",")
        .split(",")[1:-1]
    )

    n_total += 1

    if label == result[0]:
        n_true += 1

acc = n_true / n_total
print("ACC:", acc)
# # Ask a question on the data you just added.
# question = """Kontrol 1 bulan. Kunjungan pertama kali tgl 19/5/2022 dengan keluhan telapak tangan dan kaki terasa kering dan gatal jika terkena air sejak 2 tahun lalu dan hilang timbul"""

# result = rag_pipeline.run(
#     {
#         "query_embedder": {"text": question},
#         "prompt_builder": {"question": question},
#     }
# )
# print(result)
