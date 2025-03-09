import os
from dotenv import load_dotenv
from haystack import Pipeline
from haystack.utils import Secret
from haystack.components.writers import DocumentWriter
from haystack.document_stores.types import DuplicatePolicy
from haystack.components.generators import OpenAIGenerator
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.embedders import (
    SentenceTransformersTextEmbedder,
    SentenceTransformersDocumentEmbedder,
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
regulations_document_store = MongoDBAtlasDocumentStore(
    database_name="dermatitis_db",
    collection_name="regulations",
    vector_search_index="vector_index",
)


def create_storing_regulation_pipe():
    storing_regulations_pipe = Pipeline()
    storing_regulations_pipe.add_component(
        "splitter", DocumentSplitter(split_by="word", split_length=50, split_overlap=10)
    )
    storing_regulations_pipe.add_component(
        "embedder", SentenceTransformersDocumentEmbedder()
    )
    storing_regulations_pipe.add_component(
        "writer",
        DocumentWriter(
            document_store=regulations_document_store, policy=DuplicatePolicy.OVERWRITE
        ),
    )
    storing_regulations_pipe.connect("splitter", "embedder")
    storing_regulations_pipe.connect("embedder", "writer")

    return storing_regulations_pipe


def create_storing_pipe():
    storing_pipe = Pipeline()
    storing_pipe.add_component(
        instance=SentenceTransformersDocumentEmbedder(), name="doc_embedder"
    )
    storing_pipe.add_component(
        instance=DocumentWriter(
            document_store=document_store, policy=DuplicatePolicy.OVERWRITE
        ),
        name="doc_writer",
    )

    storing_pipe.connect("doc_embedder.documents", "doc_writer.documents")

    return storing_pipe


def create_prediction_pipe():
    prompt_template = """
    Given these documents, answer whether it is classified as 'dermatitis atopic' or 'non dermatitis atopic' based on the given documents. Also give explanation about the symtomps mentioned that related to the dermatitis. if the question does not related to dermatitis, give explanation about what is dermatitis atopic and non atopic, and ask for more description related to the disease. answer with the same language as the language used in the question.
    \nDocuments:
    {% for doc in documents %}
        {{ doc.content }}
    {% endfor %}
    \nQuestion: {{question}}
    \nAnswer:
    """

    prediction_pipe = Pipeline()
    prediction_pipe.add_component(
        instance=SentenceTransformersTextEmbedder(), name="query_embedder"
    )
    prediction_pipe.add_component(
        instance=MongoDBAtlasEmbeddingRetriever(document_store=document_store, top_k=5),
        name="retriever",
    )
    prediction_pipe.add_component(
        instance=PromptBuilder(template=prompt_template), name="prompt_builder"
    )
    prediction_pipe.add_component(
        instance=OpenAIGenerator(
            model="gpt-4o-mini",
            api_key=Secret.from_token(os.getenv("OPENAI_API_KEY")),
        ),
        name="llm",
    )
    prediction_pipe.connect("query_embedder", "retriever")
    prediction_pipe.connect("retriever", "prompt_builder.documents")
    prediction_pipe.connect("prompt_builder", "llm")

    return prediction_pipe


def create_anamnesis_extractor_pipe():
    prompt_template = """"
    Given this patient's description, extract information according to these parameters. Also follow the answer format\n
    Patient Description: {{prompt}}\n
    Parameters: main_complaint, patient_age, contact_history, infection_source, other_source, trigger_factors, illness_duration, past_history, family_history\n
    Answer Format: main_complaint\n patient_age\n contact_history\n infection_source\n other_source\n trigger_factors\n illness_duration\n past_history\n family_history\n
    For each parameter, give 'Unknown' if the information is not mentioned or unsure. And give 'None' if the given information for the parameter is negative.
    """
    anamnesis_pipe = Pipeline()
    anamnesis_pipe.add_component(
        instance=PromptBuilder(template=prompt_template), name="prompt_builder"
    )
    anamnesis_pipe.add_component(
        instance=OpenAIGenerator(
            model="gpt-4o-mini",
            api_key=Secret.from_token(os.getenv("OPENAI_API_KEY")),
        ),
        name="llm",
    )

    anamnesis_pipe.connect("prompt_builder", "llm")

    return anamnesis_pipe


def create_anamnesis_followup_pipe():
    prompt_template = """"
    Given this patient's description, extract information according to these unprovided parameters. Also follow the answer format\n
    Patient Description: {{prompt}}\n
    Unprovided Parameters: {% for param in unprovided_params %}{{param}}, {% endfor %}\n
    Answer Format: {% for param in unprovided_params %}{{param}}\n {% endfor %}
    For each parameter, give 'Unknown' if the information is not mentioned or unsure. And give 'None' if the given information for the parameter is negative.
    """
    followup_pipe = Pipeline()
    followup_pipe.add_component(
        instance=PromptBuilder(template=prompt_template), name="prompt_builder"
    )
    followup_pipe.add_component(
        instance=OpenAIGenerator(
            model="gpt-4o-mini",
            api_key=Secret.from_token(os.getenv("OPENAI_API_KEY")),
        ),
        name="llm",
    )

    followup_pipe.connect("prompt_builder", "llm")

    return followup_pipe


def create_followup_pipe():
    prompt_template = """"
    Create question to ask the user to provide more information about the unprovided parameters.\n
    Previous Question: {{previous_question}}\n
    Unprovided Parameters: {% for param in unprovided_params %}{{param}}, {% endfor %}\n
    Use the same language as the language used in the previous question.
    """
    followup_pipe = Pipeline()
    followup_pipe.add_component(
        instance=PromptBuilder(template=prompt_template), name="prompt_builder"
    )
    followup_pipe.add_component(
        instance=OpenAIGenerator(
            model="gpt-4o-mini",
            api_key=Secret.from_token(os.getenv("OPENAI_API_KEY")),
        ),
        name="llm",
    )

    followup_pipe.connect("prompt_builder", "llm")

    return followup_pipe
