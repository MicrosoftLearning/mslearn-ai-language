# Notes: `text-analysis.py`

**Exercise:** [Instructions/Exercises/01-analyze-text.md](../../../../Instructions/Exercises/01-analyze-text.md), *Analyze Text*

**Approach used in this lab:** call **Azure Language in Foundry Tools** directly with the `azure-ai-textanalytics` SDK. These are deterministic, task-specific NLP operations (language detection, NER, PII) on each hotel review.

**The other approach:** a **Foundry agent** with the **Azure Language MCP server** as a tool. That's exactly what the next lab ([02-language-agent](../../../02-language-agent/Python/text-agent/NOTES.md)) builds. Alternatively, an LLM can be *prompted* to extract entities or redact PII and return JSON.

> 🎯 marks an item that maps to the **AI-103** skills outline ([study guide, skills measured as of April 16, 2026](https://learn.microsoft.com/credentials/certifications/resources/study-guides/ai-103)).

---

## 1. Client: `TextAnalyticsClient(endpoint, credential=DefaultAzureCredential())`

| | |
|---|---|
| **Library** | `azure-ai-textanalytics==5.3.0` (the Language service's text analysis SDK) |
| **`endpoint`** | The Foundry resource endpoint, `https://<resource>.services.ai.azure.com` (or `*.cognitiveservices.azure.com`). |
| **`credential`** | `DefaultAzureCredential()`, which is **keyless** Entra ID auth. The identity needs a role such as *Cognitive Services User* (or *Cognitive Services Language Reader*). `AzureKeyCredential(key)` is the key-based alternative. |
| **Why** | One client covers all the prebuilt text features: language, entities, PII, sentiment, key phrases, summarization, and so on. |
| **REST equivalent** | No client. Send `Authorization: Bearer <token>` (scope `https://cognitiveservices.azure.com/.default`) or `Ocp-Apim-Subscription-Key` with each call. |
| **Agent equivalent** | `AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=...)`. The Language credentials live in a **project connection** that the MCP tool uses. |

🎯 *Manage, monitor, and secure → "Configure security, including managed identity… **keyless credentials**, and role policies"*

---

## 2. Language detection: `ai_client.detect_language(documents=[text])[0]`

| | |
|---|---|
| **Parameters** | `documents` is a list of strings or dicts (`{"id", "text", "country_hint"}`). The SDK batches up to the service limit. Optional: `country_hint`, `model_version`. |
| **Returns** | A list of `DetectLanguageResult` (or `DocumentError`). The code uses `.primary_language.name`; `.iso6391_name` and `.confidence_score` are also available. |
| **Why** | Route each review to language-specific processing (translation, or a model for that language) before analysis. |
| **REST equivalent** | `POST {endpoint}/language/:analyze-text?api-version=2023-04-01` with body `{"kind": "LanguageDetection", "analysisInput": {"documents": [{"id": "1", "text": "..."}]}}` |

🎯 *Text analysis → "Implement solutions to extract entities, topics, summaries, and structured JSON outputs by using generative prompting and **Foundry Tools**"*

## 3. Named entity recognition: `ai_client.recognize_entities(documents=[text])[0].entities`

| | |
|---|---|
| **Returns** | `CategorizedEntity` items with `.text`, `.category` (Person, Location, DateTime, Organization…), `.subcategory`, `.confidence_score` and `.offset`. |
| **Why** | Pull structured facts (places, dates, people) out of free text for search facets or analytics. |
| **REST equivalent** | Same endpoint with `"kind": "EntityRecognition"` |

🎯 *Text analysis → "…extract **entities**…"*

## 4. PII detection and redaction: `ai_client.recognize_pii_entities(documents=[text])[0]`

| | |
|---|---|
| **Returns** | `.entities` (PII items with category, such as PhoneNumber, Email or Person) and **`.redacted_text`**, which is the input with PII replaced by `*`. |
| **Optional parameters** | `categories_filter=[PiiEntityCategory.EMAIL, ...]` to limit categories, `domain_filter="phi"` for health data |
| **Why** | Remove personal data **before** storing reviews, logging prompts, or sending text to an LLM. |
| **REST equivalent** | Same endpoint with `"kind": "PiiEntityRecognition"` (and `"parameters": {"piiCategories": [...]}`) |

🎯 *Text analysis → "Configure detection of sentiment, tone, safety issues, and **sensitive content**"*
🎯 *Plan and manage → Responsible AI → "Configure safety filters, guardrails…"*. PII redaction before an LLM sees the text is a guardrail.

---

## 5. Direct SDK vs agent + MCP vs LLM prompting

| | Direct SDK (this lab) | Agent + Azure Language MCP (lab 02) | LLM prompt only |
|---|---|---|---|
| Call | `detect_language`, `recognize_entities`, `recognize_pii_entities` | Agent picks the Language MCP tool (`server_url=https://<resource>.cognitiveservices.azure.com/language/mcp?api-version=...`) | `responses.create(instructions="Return JSON with entities and redacted text", input=text)` |
| Output | Typed, deterministic, with confidence scores | Tool output, which the LLM then summarizes | Free-form or JSON; can vary or hallucinate |
| Best for | Batch pipelines, compliance-grade PII | Conversational, ad-hoc analysis | Custom domain extraction, tone, summaries |

🎯 *Text analysis → "**Customize language model outputs** for domain tasks, such as compliance summarization and domain extraction"*. This is the LLM column.
🎯 *Plan and manage → "Choose an appropriate model for each task, including LLMs, SLMs, multimodal models, and **Foundry Tools**"*. This table is that decision.

## References

- [Azure Language overview](https://learn.microsoft.com/azure/ai-services/language-service/overview)
- [Azure Language tools and agents (MCP server)](https://learn.microsoft.com/azure/ai-services/language-service/concepts/foundry-tools-agents)
- [AI-103 study guide](https://learn.microsoft.com/credentials/certifications/resources/study-guides/ai-103)
