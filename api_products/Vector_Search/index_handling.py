from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, edm
from azure.search.documents import SearchClient
from azure.search.documents.models import IndexDocumentsBatch, IndexAction

def create_index(client: SearchIndexClient, index_name: str):
    # Define the schema for the index
    index = SearchIndex(
        name=index_name,
        fields=[
            SimpleField(name="id", type=edm.String, key=True),
            SimpleField(name="content", type=edm.String)
        ]
    )
    client.create_index(index)

def update_index(client: SearchClient, file_name: str, file_content: str):
    actions = IndexDocumentsBatch(actions=[
        IndexAction.upload(
            {
                "id": file_name,
                "content": file_content
            }
        )
    ])
    client.index_documents(actions)

def index_exists(client: SearchIndexClient, index_name: str) -> bool:
    indexes = client.list_index_names()
    return index_name in indexes
