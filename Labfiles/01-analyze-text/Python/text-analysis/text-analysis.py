from dotenv import load_dotenv
import os
import json


# Import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Create client using endpoint and key
        credential = AzureKeyCredential(ai_key)
        ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)

        # Analyze each text file in the reviews folder
        reviews_folder = 'reviews'
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            print('\n-------------\n' + file_name)
            text = open(os.path.join(reviews_folder, file_name), encoding='utf8').read()
            print('\n' + text)

            # Get language
            detectedLanguage = ai_client.detect_language(documents=[text])[0]
            print("\nRaw response: {}".format(detectedLanguage))
            print('\nLanguage: {}'.format(detectedLanguage.primary_language.name))

            # Get sentiment
            sentimentAnalysis = ai_client.analyze_sentiment(documents=[text])[0]
            sentiment = sentimentAnalysis  # just to shorten the name

            formatted = {
                "id": sentiment.id,
                "sentiment": sentiment.sentiment,
                "warnings": sentiment.warnings,
                "statistics": sentiment.statistics,  # drop this if you don’t need it
                "confidence_scores": {
                    "positive": sentiment.confidence_scores.positive,
                    "neutral": sentiment.confidence_scores.neutral,
                    "negative": sentiment.confidence_scores.negative,
                },
                "sentences": [
                    {
                        "text": s.text,
                        "sentiment": s.sentiment,
                        "confidence_scores": {
                            "positive": s.confidence_scores.positive,
                            "neutral": s.confidence_scores.neutral,
                            "negative": s.confidence_scores.negative,
                        },
                        "length": s.length,
                        "offset": s.offset,
                    }
                    for s in sentiment.sentences
                ],
            }

            #print("\nRaw response:")
           # print(json.dumps(formatted, indent=2, ensure_ascii=False))

            print('\nOverall sentiment: {}'.format(sentimentAnalysis.sentiment))

            # Get key phrases
            phrases = ai_client.extract_key_phrases(documents=[text])[0].key_phrases
            if len(phrases) > 0:
                print("\nKey Phrases:")
                for phrase in phrases:
                    print('\t{}'.format(phrase))

            # Get entities
            entities = ai_client.recognize_entities(documents=[text])[0].entities
            if len(entities) > 0:
                print("\nEntities")
                for entity in entities:
                    print('\t{} ({})'.format(entity.text, entity.category))

            # Get linked entities
            entities = ai_client.recognize_linked_entities(documents=[text])[0].entities
            if len(entities) > 0:
                print("\nLinks")
                for linked_entity in entities:
                    print('\t{} ({})'.format(linked_entity.name, linked_entity.url))


    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()