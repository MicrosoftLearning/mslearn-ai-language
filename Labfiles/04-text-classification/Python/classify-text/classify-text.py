from dotenv import load_dotenv
import os

# Import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')
        project_name = os.getenv('PROJECT')
        deployment_name = os.getenv('DEPLOYMENT')

        # Create client using endpoint and key
        credential = AzureKeyCredential(ai_key)
        ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)

        # Analyze each text file in the reviews folder
        batchedDocuments = []
        articles_folder = 'articles'
        for file_name in os.listdir(articles_folder):
            # Read the file contents
            print('\n-------------\n' + file_name)
            text = open(os.path.join(articles_folder, file_name), encoding='utf8').read()
            batchedDocuments.append(text)

            # Get Classification
            operation = ai_client.begin_single_label_classify(
                batchedDocuments,
                project_name=project_name,
                deployment_name=deployment_name
            )

            document_results = operation.result()
            for doc, classification_result in zip(document, document_results):
                if classification_result.kind == "CustomDocumentClassification":
                    classification = classification_result.classifications[0]
                    print("The document text '{}' was classified as '{}' with confidence score {}.".format(
                        doc, classification.category, classification.confidence_score)
                    )
                elif classification_result.is_error is True:
                    print("Document text '{}' has an error with code '{}' and message '{}'".format(
                        doc, classification_result.error.code, classification_result.error.message
            ))


    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()