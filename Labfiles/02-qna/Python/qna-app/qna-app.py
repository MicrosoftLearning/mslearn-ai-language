from dotenv import load_dotenv
import os

# Import namespaces


def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Create client using endpoint and key


        # Submit a question and display the answer



    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()