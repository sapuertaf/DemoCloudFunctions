"""
... 
"""
import os
import functions_framework
from google.cloud import dataproc_v1 as dataproc

# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def execute_workflow(cloud_event):
    # Agregando variables de entorno
    os.environ["PROJECT_ID"] = "datatest-347114"
    os.environ["REGION"] = "us-central1"
    os.environ["WORKFLOW_TEMPLATE"] = "mvp"

    # Configura el punto final antes de crear la instancia del cliente
    os.environ['DATAPROC_ENDPOINT'] = f'{os.environ["REGION"]}-dataproc.googleapis.com:443'

    dataproc_client = dataproc.WorkflowTemplateServiceClient(
        client_options={"api_endpoint":os.environ["DATAPROC_ENDPOINT"]}
    )

    workflow_template_name = f'projects/{os.environ["PROJECT_ID"]}/regions/{os.environ["REGION"]}/workflowTemplates/{os.environ["WORKFLOW_TEMPLATE"]}'

    file: dict = cloud_event.data

    input_bucket_uri = f"gs://{file['bucket']}/{file['name']}"

    try:
        response = dataproc_client.instantiate_workflow_template(
            name=workflow_template_name,
            parameters={"INPUT_BUCKET_URI": input_bucket_uri}
        )

        print("Launched workflow")
    except Exception as e:
        print(e)

