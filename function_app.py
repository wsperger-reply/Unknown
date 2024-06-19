import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="SharepointSync")
def SharepointSync(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        file_content = base64.b64decode(req_body['file_content'])
        file_name = req_body['file_name']
        folder_name = req_body['folder_name']

        # Set up managed identity credential
        credential = ManagedIdentityCredential()

        # Connect to the Search Index client
        index_client = SearchIndexClient(endpoint=SEARCH_ENDPOINT, credential=credential)

        # Check if the index already exists
        try:
            index_client.get_index(folder_name)
        except:
            create_index(index_client, folder_name)

        # Connect to the Search Client for the specific index
        search_client = SearchClient(endpoint=SEARCH_ENDPOINT, index_name=folder_name, credential=credential)

        # Update the index with the new file
        update_index(search_client, file_name, file_content.decode('utf-8'))

        return func.HttpResponse("Index updated successfully.", status_code=200)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)



@app.route(route="SharepointSearch", auth_level=func.AuthLevel.FUNCTION)
def SharepointSearch(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )