from dotenv import load_dotenv
import os

# Import namespaces
from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient

def main():
    try:
        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear')

        # Get Configuration Settings
        load_dotenv()
        foundry_endpoint = os.getenv('FOUNDRY_ENDPOINT')


        # Create client using endpoint
        credential = DefaultAzureCredential()
        ai_client = TextAnalyticsClient(endpoint=foundry_endpoint, credential=credential)


        # Analyze each text file in the reviews folder
        reviews_folder = 'reviews'
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            print('\n-------------\n' + file_name)
            text = open(os.path.join(reviews_folder, file_name), encoding='utf8').read()
            print('\n' + text)

            # Get language
            detectedLanguage = ai_client.detect_language(documents=[text])[0]
            print('\nLanguage: {}'.format(detectedLanguage.primary_language.name))


            # Get entities
            entities = ai_client.recognize_entities(documents=[text])[0].entities
            if len(entities) > 0:
                print("\nEntities")
                for entity in entities:
                    print('\t{} ({})'.format(entity.text, entity.category))

            # Get PII
            # Get PII
            pii_result = ai_client.recognize_pii_entities(documents=[text])[0]
            pii_entities = pii_result.entities
            if len(pii_entities) > 0:
                print("\nPII Entities")
                for pii_entity in pii_entities:
                    print('\t{} ({})'.format(pii_entity.text, pii_entity.category)) 
                print("Redacted Text:\n {}".format(pii_result.redacted_text))
            
            
                except Exception as ex:
                    print(ex)


if __name__ == "__main__":
    main()
