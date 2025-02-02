from dotenv import load_dotenv
import os
from haystack import Pipeline
from haystack.utils import Secret
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.embedders import (
    SentenceTransformersTextEmbedder,
)
from haystack_integrations.document_stores.mongodb_atlas import (
    MongoDBAtlasDocumentStore,
)
from haystack_integrations.components.retrievers.mongodb_atlas import (
    MongoDBAtlasEmbeddingRetriever,
)

load_dotenv()

document_store = MongoDBAtlasDocumentStore(
    database_name="dermatitis_db",
    collection_name="raw_collections",
    vector_search_index="vector_index",
)

prompt_template = """
Given these documents, answer whether it is classified as 'dermatitis atopik' or 'non dermatitis atopik' based on the given documents. and also give explanation about the disease. answer with the same language as the language used in the question.
\nDocuments:
{% for doc in documents %}
    {{ doc.content }}

{% endfor %}

\nQuestion: {{question}}
\nAnswer:
"""

rag_pipeline = Pipeline()
rag_pipeline.add_component(
    instance=SentenceTransformersTextEmbedder(), name="query_embedder"
)
rag_pipeline.add_component(
    instance=MongoDBAtlasEmbeddingRetriever(document_store=document_store, top_k=1),
    name="retriever",
)
rag_pipeline.add_component(
    instance=PromptBuilder(template=prompt_template), name="prompt_builder"
)
rag_pipeline.add_component(
    instance=OpenAIGenerator(
        model="gpt-4o-mini",
        api_key=Secret.from_token(os.getenv("OPENAI_API_KEY")),
    ),
    name="llm",
)
rag_pipeline.connect("query_embedder", "retriever")
rag_pipeline.connect("retriever", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder", "llm")


# result = rag_pipeline.run(
#     {
#         "query_embedder": {"text": question},
#         "prompt_builder": {"question": question},
#     }
# )
# print(result)
