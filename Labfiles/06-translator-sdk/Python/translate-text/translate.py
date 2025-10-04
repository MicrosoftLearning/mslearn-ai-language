from dotenv import load_dotenv
import os

# import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import *
from azure.ai.translation.text.models import InputTextItem


def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        translatorRegion = os.getenv('TRANSLATOR_REGION')
        translatorKey = os.getenv('TRANSLATOR_KEY')

        # Create client using endpoint and key
        credential = AzureKeyCredential(translatorKey)
        client = TextTranslationClient(credential=credential, region=translatorRegion)


        ## Choose target language
        languagesResponse = client.get_supported_languages(scope="translation")
        print("{} languages supported.".format(len(languagesResponse.translation)))
        print("(See https://learn.microsoft.com/azure/ai-services/translator/language-support#translation)")
        print("Enter a target language code for translation (for example, 'en'):")
        targetLanguage = "xx"
        supportedLanguage = False
        while supportedLanguage == False:
            targetLanguage = input()
            if  targetLanguage in languagesResponse.translation.keys():
                supportedLanguage = True
            else:
                print("{} is not a supported language.".format(targetLanguage))


        # Translate text
        inputText = ""
        while inputText.lower() != "quit":
            inputText = input("Enter text to translate ('quit' to exit):")
            if inputText != "quit":
                input_text_elements = [InputTextItem(text=inputText)]
                translationResponse = client.translate(body=input_text_elements, to_language=[targetLanguage])
                translation = translationResponse[0] if translationResponse else None
                if translation:
                    sourceLanguage = translation.detected_language
                    for translated_text in translation.translations:
                        print(f"'{inputText}' was translated from {sourceLanguage.language} to {translated_text.to} as '{translated_text.text}'.")


    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()