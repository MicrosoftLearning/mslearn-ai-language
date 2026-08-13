---
lab:
    title: 'Task 1 – Analyze guest reviews'
    description: 'Use Azure Language in Foundry Tools to detect the language of each guest review, extract the entities it mentions, and redact personally identifiable information.'
    level: 200
    concepts: 'language detection, entity recognition, PII redaction'
    islab: true
    status: 'draft'
---

# Task 1 — Analyze guest reviews

*Part of the **Analyze and translate guest feedback** lab. New here? Start with [Getting started](A0-getting-started.md).*

> **Set up (start here):** This task needs a Foundry project and the starter code. If you
> haven't already, complete [Getting started](A0-getting-started.md) to create your project,
> clone the code, and set `FOUNDRY_ENDPOINT` in `Python/.env`. The sample reviews are already
> in the starter folder. Then verify you're ready:

```
python setup/check_env.py --task 1
```

---

**Goal**: Take a folder of raw guest reviews and, for each one, work out what language it's
in, what it mentions, and what has to be removed before you publish it.

**Concept reinforced**: specialist models return **structured** results. You don't parse
prose - you get categories, confidence scores, and a redacted string you can use directly.

**Set up:**

1. In the `Labfiles/A-analyze-and-translate-text/Python` folder, activate the virtual
    environment (`.\labenv\Scripts\Activate.ps1`) and confirm `FOUNDRY_ENDPOINT` is set in
    **.env** (see [Getting started](A0-getting-started.md)).

1. Open the **reviews** subfolder and read a couple of the files. Note that they cover two
    lodges, and that **review5.txt** isn't in English. Note also that **review1.txt**
    contains an email address and **review2.txt** names a colleague - those are the details
    you'll be redacting.

1. Open **analyze-reviews.py** and review the existing code. The loop that reads each review
    file and prints it is already written; you'll add the analysis.

    > **Tip**: As you add code to the code file, be sure to maintain the correct indentation.

## Connect to Azure Language in Foundry Tools

1. At the top of the code file, find the comment **Import namespaces** and add the code to
    import the namespaces you need:

    ```python
    # Import namespaces
    from azure.identity import DefaultAzureCredential
    from azure.ai.textanalytics import TextAnalyticsClient
    ```

1. In the **main** function, code to load the endpoint from the configuration file has
    already been provided. Find the comment **Create client using endpoint** and add the
    code to create a client:

    ```python
    # Create client using endpoint
    credential = DefaultAzureCredential()
    ai_client = TextAnalyticsClient(endpoint=foundry_endpoint, credential=credential)
    ```

1. Save the file and run the application:

    ```
    python analyze-reviews.py
    ```

1. Observe the output. The code runs without error and displays the contents of each review
    file. It successfully creates a client but doesn't use it yet - you'll fix that next.

## Detect the language of each review

> **Try it first**: The client exposes one method per capability. Before revealing the
> solution, look at the `detect_language` documentation and work out what it returns for a
> single document, and why the code below indexes `[0]`.

<details markdown="1">
<summary>Show a solution</summary>

Find the comment **Get language** and add the code to detect the language of each review:

```python
# Get language
detectedLanguage = ai_client.detect_language(documents=[text])[0]
print('\nLanguage: {}'.format(detectedLanguage.primary_language.name))
```

> **Note**: *In this example, each review is analyzed individually, resulting in a separate
> call to the service for each file. An alternative approach is to create a collection of
> documents and pass them to the service in a single call. In both approaches, the response
> from the service consists of a collection of documents; which is why in the Python code
> above, the index of the first (and only) document in the response ([0]) is specified.*

Save your changes and re-run the program. This time the language for each review is
identified - and **review5.txt** is correctly reported as French.

</details>

<details markdown="1" class="concept">
<summary>What does "confidence" mean here?</summary>
<div class="concept-body" markdown="1">

Language detection returns a `confidence_score` alongside the language name. Short
documents are genuinely ambiguous - a three-word review could plausibly be several
languages - so the service tells you how sure it is rather than pretending to be certain.

In a production pipeline you'd typically route low-confidence documents to a human, or fall
back to treating them as your default language. Try printing
`detectedLanguage.primary_language.confidence_score` and compare the long English reviews
with the short French one.

</div>
</details>

## Extract the entities mentioned in a review

Reviews mention places, landmarks, dates, and people. Entity recognition finds them and
tells you what category each belongs to.

> **Try it first**: `recognize_entities` returns an object with an `entities` collection,
> and each entity has `text` and `category` attributes. Write the loop that prints them
> before revealing the solution.

<details markdown="1">
<summary>Show a solution</summary>

Find the comment **Get entities** and add the code to identify the entities in each review:

```python
# Get entities
entities = ai_client.recognize_entities(documents=[text])[0].entities
if len(entities) > 0:
    print("\nEntities")
    for entity in entities:
        print('\t{} ({})'.format(entity.text, entity.category))
```

Save your changes and re-run the program. Observe the entities detected in each review -
you should see locations such as Zermatt and Whistler, landmarks, and dates.

</details>

## Redact personally identifiable information

Privacy policies and legislation often require that personally identifiable information
(PII) - names, addresses, phone numbers, email addresses - be redacted from documents
before they're published.

> **Try it first**: PII redaction returns *two* useful things: the list of entities it
> found, and a version of the whole document with them masked out. Find the attribute that
> holds the masked text before revealing the solution.

<details markdown="1">
<summary>Show a solution</summary>

Find the comment **Get PII** and add the code to identify and redact PII entities:

```python
# Get PII
pii_result = ai_client.recognize_pii_entities(documents=[text])[0]
pii_entities = pii_result.entities
if len(pii_entities) > 0:
    print("\nPII Entities")
    for pii_entity in pii_entities:
        print('\t{} ({})'.format(pii_entity.text, pii_entity.category))
    print("Redacted Text:\n {}".format(pii_result.redacted_text))
```

Save your changes and re-run the program. Observe the PII entities identified - the email
address in **review1.txt** and the person named in **review2.txt** - and review the redacted
version of each document that is produced.

That `redacted_text` string is what the guest experience team would publish.

</details>

**Stretch**: the reviews contain a rating implied by their tone but never stated as a number.
Look up `analyze_sentiment` in the Azure Language SDK and add a fourth analysis step that
prints the overall sentiment of each review.

---

**Next:** [Task 2 — Translate guest feedback](A2-translate-guest-feedback.md)
