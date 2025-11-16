import os
import sys
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchableField

service_endpoint = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")
api_key = os.getenv("AZURE_SEARCH_API_KEY")
index_name = "sample-index"

if not service_endpoint or not api_key:
    print("Missing AZURE_SEARCH_SERVICE_ENDPOINT or AZURE_SEARCH_API_KEY. Set them before running createindex.py.")
    sys.exit(0)

credential = AzureKeyCredential(api_key)
index_client = SearchIndexClient(service_endpoint, credential)

fields = [
    SimpleField(name="id", type="Edm.String", key=True),
    SearchableField(name="content", type="Edm.String"),
]

index = SearchIndex(name=index_name, fields=fields)

try:
    index_client.create_index(index)
    print(f"Index '{index_name}' created or updated successfully.")
except Exception as e:
    print(f"Failed to create index: {e}")

search_client = SearchClient(service_endpoint, index_name, credential)

documents = [
    {"id": "1", "content": "Hello world"},
    {"id": "2", "content": "Azure Cognitive Search"}
]

try:
    result = search_client.upload_documents(documents)
    print(f"Upload result: {result}")
except Exception as e:
    print(f"Failed to upload documents: {e}")
