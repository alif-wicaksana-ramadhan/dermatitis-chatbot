import os
from haystack import Pipeline
from haystack.components.converters import TextFileToDocument
from haystack.components.preprocessors import DocumentCleaner
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack_integrations.document_stores.mongodb_atlas import (
    MongoDBAtlasDocumentStore,
)
from haystack.document_stores.types import DuplicatePolicy
from haystack.components.writers import DocumentWriter


os.environ["MONGO_CONNECTION_STRING"] = (
    "mongodb+srv://iros:riset1231@cluster0.pkadj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

document_store = MongoDBAtlasDocumentStore(
    database_name="test_db",
    collection_name="test_collections",
    vector_search_index="vector_index",
)

pipeline_storing_mongodb = Pipeline()
pipeline_storing_mongodb.add_component("converter", TextFileToDocument())
pipeline_storing_mongodb.add_component("cleaner", DocumentCleaner())
pipeline_storing_mongodb.add_component(
    "splitter", DocumentSplitter(split_by="word", split_length=256, split_overlap=100)
)
pipeline_storing_mongodb.add_component(
    "embedder", SentenceTransformersDocumentEmbedder()
)
pipeline_storing_mongodb.add_component(
    "writer", DocumentWriter(document_store=document_store, policy=DuplicatePolicy.SKIP)
)

pipeline_storing_mongodb.connect("converter", "cleaner")
pipeline_storing_mongodb.connect("cleaner", "splitter")
pipeline_storing_mongodb.connect("splitter", "embedder")
pipeline_storing_mongodb.connect("embedder", "writer")

pipeline_storing_mongodb.run({"converter": {"sources": ["starwars.txt"]}})
