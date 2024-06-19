# Syncing SharePoint Library with Azure AI Studio Indexes

## Project Overview

This project aims to synchronize a SharePoint library with Azure AI Studio indexes. Each root-level folder in the SharePoint library will correspond to its own index in Azure AI Studio. We will detect file additions in SharePoint using Power Automate, which will trigger an Azure Function to update the respective indexes.

## Architectural Components

1. **SharePoint Online**
   - Stores documents in libraries and folders.
   
2. **Power Automate**
   - Detects changes in SharePoint and triggers Azure Functions.

3. **Azure AI Studio**
   - Hosts the indexes corresponding to SharePoint folders.

4. **Azure Functions**
   - Acts as the glue between SharePoint and Azure AI Studio.
   - Handles events from Power Automate and updates the respective indexes.

5. **Managed Identities**
   - Securely manage credentials for accessing Azure resources.

## Steps and Documentation

### Step 1: Set Up SharePoint Library

1. Create a SharePoint site and document library.
2. Organize the root-level folders.

### Step 2: Configure Power Automate Flow

1. **Create a Power Automate Flow**:
   - Set up a trigger for file additions in the SharePoint document library.
   - [Create a flow in Power Automate](https://docs.microsoft.com/en-us/power-automate/get-started-logic-flow)

2. **Trigger Azure Function**:
   - Configure the flow to call an HTTP-triggered Azure Function, passing the file data in Base64 format.
   - [HTTP action in Power Automate](https://docs.microsoft.com/en-us/power-automate/logic-apps-http-endpoint)

### Step 3: Create Azure Functions

1. **Set Up Azure Functions**:
   - Create a new Azure Functions project using Python.
   - [Create your first function in the Azure portal](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python)

2. **Implement Functions**:
   - Create an HTTP-triggered function to handle file data and update indexes.
   - Example function code:
     ```python
     import logging
     import base64
     import os
     from azure.identity import ManagedIdentityCredential
     from azure.search.documents import SearchClient
     from azure.search.documents.models import IndexDocumentsBatch, IndexAction

     import azure.functions as func

     def main(req: func.HttpRequest) -> func.HttpResponse:
         logging.info('Python HTTP trigger function processed a request.')

         try:
             file_data = req.get_json()
             file_content = base64.b64decode(file_data['file_content'])
             file_name = file_data['file_name']
             folder_name = file_data['folder_name']

             # Set up managed identity credential
             credential = ManagedIdentityCredential()

             # Connect to the appropriate Azure AI Studio index
             index_name = f"{folder_name}-index"
             search_client = SearchClient(endpoint=os.environ["SEARCH_ENDPOINT"],
                                          index_name=index_name,
                                          credential=credential)

             # Update the index
             actions = IndexDocumentsBatch(actions=[
                 IndexAction.upload(
                     {
                         "id": file_name,
                         "content": file_content.decode('utf-8')
                     }
                 )
             ])
             search_client.index_documents(actions)

             return func.HttpResponse("Index updated successfully.", status_code=200)

         except Exception as e:
             logging.error(f"Error processing request: {e}")
             return func.HttpResponse(f"Error: {str(e)}", status_code=500)
     ```

3. **Configure Managed Identity**:
   - Enable Managed Identity for the Azure Functions app.
   - [How to use managed identities for Azure resources](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview)

4. **Access Azure AI Studio**:
   - Use Managed Identity to securely call Azure AI Studio.
   - [Authenticate with Managed Identity](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/how-to-use-vm-token)

### Step 4: Index Management in Azure AI Studio

1. **Create Indexes**:
   - Define and create indexes for each root folder.
   - [Azure AI Studio documentation](https://learn.microsoft.com/en-us/azure/cognitive-search/)

2. **Update Indexes**:
   - Implement logic to update indexes when new files are detected.
   - [Push data into an Azure Cognitive Search index](https://docs.microsoft.com/en-us/azure/search/search-howto-indexing-portal)

## Summary of Documentation Links

- [Create a flow in Power Automate](https://docs.microsoft.com/en-us/power-automate/get-started-logic-flow)
- [HTTP action in Power Automate](https://docs.microsoft.com/en-us/power-automate/logic-apps-http-endpoint)
- [Create your first function in the Azure portal](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python)
- [Azure Functions Python developer guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python)
- [How to use managed identities for Azure resources](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview)
- [Authenticate with Managed Identity](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/how-to-use-vm-token)
- [Azure AI Studio documentation](https://learn.microsoft.com/en-us/azure/cognitive-search/)
- [Push data into an Azure Cognitive Search index](https://docs.microsoft.com/en-us/azure/search/search-howto-indexing-portal)

## Conclusion

By following this architecture and utilizing the provided documentation, you can build a robust solution to sync a SharePoint library with Azure AI Studio indexes using Power Automate and Azure Functions.
