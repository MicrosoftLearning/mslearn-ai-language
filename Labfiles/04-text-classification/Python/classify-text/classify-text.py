from dotenv import load_dotenv
import os

# Import namespaces


def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')
        project_name = os.getenv('PROJECT')
        deployment_name = os.getenv('DEPLOYMENT')

        # Create client using endpoint and key


        # Read each text file in the articles folder
        batchedDocuments = []
        articles_folder = 'articles'
        files = os.listdir(articles_folder)
        for file_name in files:
            # Read the file contents
            text = open(os.path.join(articles_folder, file_name), encoding='utf8').read()
            batchedDocuments.append(text)

        # Get Classifications



    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()