---
lab:
    title: 'Task 2 – Translate guest feedback'
    description: 'Use Azure Translator in Foundry Tools to translate guest feedback into any supported language, detecting the source language automatically.'
    level: 200
    concepts: 'text translation, language detection, supported languages'
    islab: true
    status: 'draft'
---

# Task 2 — Translate guest feedback

*Part of the **Analyze and translate guest feedback** lab. New here? Start with [Getting started](A0-getting-started.md).*

> **Set up (start here):** This task needs a Foundry project and the starter code. If you
> haven't already, complete [Getting started](A0-getting-started.md) to create your project,
> clone the code, and set `TRANSLATOR_ENDPOINT` in `Python/.env`. Then verify you're ready:

```
python setup/check_env.py --task 2
```

> **Continuing from a previous task?** If you just finished Task 1 in the same `Python`
> folder, your project, virtual environment, and Azure sign-in are already set. You only
> need to confirm that `TRANSLATOR_ENDPOINT` is filled in - it's a *different* endpoint
> format from the one Task 1 used - then go straight to **Explore the playground** below.

---

**Goal**: Translate guest feedback from any language into a target language of your choice,
without having to tell the service what language the input was in.

**Concept reinforced**: translation and language detection are the same call. You supply
the target language; Azure Translator works out the source.

## Explore Azure Translator in the portal

Before writing code, it's worth seeing the service work interactively.

1. In the [Microsoft Foundry portal](https://ai.azure.com), open your project. Select
    **Explore playgrounds** (or on the **Build** page, select the **Models** tab).

1. Select the **AI services** tab to view the list of Azure services in Foundry Tools.

1. In the list of tools, select **Azure Translator - Text translation**.

1. In the Text translator playground, in the **Source text** area, enter a line of guest
    feedback such as `The lodge was spotless and the staff were wonderful.`. Then, in the
    **Translation** area, select any language and use the **Translate** button.

1. Try a few more languages. Then paste in the French review text from Task 1 and note that
    you never had to tell it the input was French.

1. Select the **Code** tab to view sample code, and note the **ENDPOINT** variable used for
    the REST API. It should look like `https://{your-resource}.cognitiveservices.azure.com/` -
    the same value you put in `TRANSLATOR_ENDPOINT`.

    This endpoint uses the older format for Azure AI services, but it is still how you
    connect to Azure Translator in a Foundry resource. The Azure Speech tools use it too.

## Connect to Azure Translator in Foundry Tools

1. In the `Labfiles/A-analyze-and-translate-text/Python` folder, open **translate-feedback.py**
    and review the existing code.

    > **Tip**: As you add code to the code file, be sure to maintain the correct indentation.

1. At the top of the code file, find the comment **Import namespaces** and add the code to
    import the namespaces you need:

    ```python
    # Import namespaces
    from azure.identity import DefaultAzureCredential
    from azure.ai.translation.text import TextTranslationClient
    from azure.ai.translation.text.models import InputTextItem
    ```

1. In the **main** function, find the comment **Create client using endpoint and credential**
    and add the code to create a client:

    ```python
    # Create client using endpoint and credential
    credential = DefaultAzureCredential()
    client = TextTranslationClient(credential=credential, endpoint=translator_endpoint)
    ```

## Ask the service which languages it supports

Rather than hard-coding a list of languages, ask the service. This also gives you a way to
validate whatever the user types.

> **Try it first**: `get_supported_languages(scope="translation")` returns an object whose
> `translation` attribute is a dictionary keyed by language code. Write the prompt-and-validate
> loop before revealing the solution.

<details markdown="1">
<summary>Show a solution</summary>

Find the comment **Choose target language** and add the following code, which returns the
list of supported languages and prompts the user to select a target language code:

```python
# Choose target language
languagesResponse = client.get_supported_languages(scope="translation")
print("{} languages supported.".format(len(languagesResponse.translation)))
print("(See https://learn.microsoft.com/azure/ai-services/translator/language-support#translation)")
print("Enter a target language code for translation (for example, 'en'):")
targetLanguage = "xx"
supportedLanguage = False
while supportedLanguage == False:
    targetLanguage = input()
    if targetLanguage in languagesResponse.translation.keys():
        supportedLanguage = True
    else:
        print("{} is not a supported language.".format(targetLanguage))
```

</details>

## Translate the feedback

> **Try it first**: `client.translate()` takes a `body` of `InputTextItem` objects and a
> `to_language` list. Each result carries both a `detected_language` and a `translations`
> collection. Write the loop that prints where the text came from and what it became.

<details markdown="1">
<summary>Show a solution</summary>

Find the comment **Translate text** and add the following code, which repeatedly prompts for
feedback to translate, translates it to the target language (detecting the source language
automatically), and displays the results until the user enters *quit*:

```python
# Translate text
inputText = ""
while inputText.lower() != "quit":
    inputText = input("Enter guest feedback to translate ('quit' to exit):")
    if inputText != "quit":
        input_text_elements = [InputTextItem(text=inputText)]
        translationResponse = client.translate(body=input_text_elements, to_language=[targetLanguage])
        translation = translationResponse[0] if translationResponse else None
        if translation:
            sourceLanguage = translation.detected_language
            for translated_text in translation.translations:
                print(f"'{inputText}' was translated from {sourceLanguage.language} to {translated_text.to} as '{translated_text.text}'.")
```

Save your changes and run the application:

```
python translate-feedback.py
```

When prompted, enter a valid target language code. Then enter some guest feedback and view
the results, which should detect the source language and translate the text. Try:

```
J'adore ce chalet. Le personnel est tres amical.
```

The service reports the source as `fr` without you telling it. When you're done, enter
`quit`. You can run the application again and choose a different target language.

</details>

<details markdown="1" class="concept">
<summary>When should I translate, and when should I not?</summary>
<div class="concept-body" markdown="1">

Translation is cheap and fast, so the temptation is to translate everything into one
language and analyze that. Resist it for analysis: translating first throws away signal.
Sentiment, entity names, and especially PII are all more reliably detected in the
*original* language, because that's what the specialist models were trained on.

The pattern that works well is the one this lab builds: **analyze in the source language,
translate for humans**. Task 1 finds the entities and the PII; Task 2 makes the result
readable to a team that doesn't speak French.

</div>
</details>

**Stretch**: `translate()` accepts more than one target language at a time. Change
`to_language=[targetLanguage]` to a list of three codes and adjust the output loop so a
single call produces all three translations.

---

**Next (optional):** [Task 3 — Hand the job to an agent](A3-build-a-guest-feedback-agent.md)
