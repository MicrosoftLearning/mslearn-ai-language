---
lab:
    title: 'Analyze and translate guest feedback'
    description: 'Build the Alpine Ski House guest feedback pipeline: detect the language of each review, extract entities, redact PII, translate feedback into any language, and hand the whole job to an agent. A modular lab you can complete end to end or one task at a time.'
    level: 300
    concepts: 'language detection, entity recognition, PII redaction, text translation, MCP tools'
    duration: 35
    islab: true
    status: 'draft'
---

# Analyze and translate guest feedback

**Difficulty** ▰▰▰▱▱ **L300**  (filled bars out of 5; **L100** beginner → **L500** expert)

Guest feedback arrives as unstructured text, in whatever language the guest happens to
speak. Turning that into something a business can act on means answering three questions
about every review: *what language is this*, *what is it about*, and *what in it must not
be published*. In this lab you'll build that pipeline, then hand the whole job to an agent.

<style>
/* "Ask Freya" just-in-time concept blocks */
details.concept { margin:.6rem 0 1rem; }
details.concept > summary { display:inline-block; cursor:pointer; list-style:none;
  font-size:.85em; font-weight:600; color:#1b6ec2; background:#1b6ec212;
  border:1px solid #1b6ec233; border-radius:999px; padding:.2em .7em; }
details.concept > summary::-webkit-details-marker { display:none; }
details.concept > summary::before { content:"Ask Freya: "; font-weight:700; }
details.concept > summary:hover { background:#1b6ec2; color:#fff; border-color:#1b6ec2; }
details.concept[open] > summary { border-bottom-left-radius:0; border-bottom-right-radius:0; }
details.concept .concept-body { border:1px solid #1b6ec233; border-top:none;
  border-radius:0 8px 8px 8px; padding:.6rem .9rem; background:#1b6ec208; font-size:.95em; }
</style>

<details markdown="1" class="concept">
<summary>Why not just ask a language model?</summary>
<div class="concept-body" markdown="1">

You could. But Azure Language in Foundry Tools gives you *specialist* models for a small
set of well-defined jobs - language detection, entity recognition, PII redaction - and
they return **structured** results with categories and confidence scores, not prose you
have to parse. They're cheaper and faster per document, and the PII redaction returns the
redacted text for you rather than trusting a model to remember the rules.

The interesting twist, which you'll see in Task 3, is that you don't have to choose: an
agent can call these same specialist tools on your behalf.

</div>
</details>

**Your scenario:** you work at **Alpine Ski House**, a group of mountain resorts with
lodges in Zermatt, Whistler, and Chamonix. Guests leave reviews in a dozen languages, and
the guest experience team needs to publish the useful ones without publishing anyone's
email address. Across this lab you'll build the tooling that makes that possible.

You'll start with the **Core** tasks that get you to a working analysis and translation
pipeline as quickly as possible. From there, an **Optional** task lets you go further and
put an agent in charge.

> **Note**: Some of the technologies used in this exercise are in preview or in active
> development. You may experience some unexpected behavior, warnings, or errors.

## What you'll learn

By completing the **Core** tasks of this exercise, you'll be able to:

- **Analyze text** with Azure Language in Foundry Tools - detecting the language a review
  is written in, extracting the entities it mentions, and redacting personally
  identifiable information before publication.
- **Translate text** with Azure Translator in Foundry Tools, detecting the source language
  automatically and translating into any supported target language.

The **Optional** task lets you additionally:

- **Give an agent the same capabilities** by connecting the Azure Language in Foundry
  Tools MCP server, then calling that agent from your own client application - and see how
  much code disappears when the agent picks the tools for you.

## How this lab is organized

This lab is **modular**. Each task is written to be completed **on its own, starting fresh** -
so you can pick a single task and do just that one. Every task also shares one starter folder,
one virtual environment, and one `.env`, so if you'd rather work straight through, you can.

1. **Start with [Getting started](A0-getting-started.md)** - create your Microsoft Foundry
   project, get the starter code, and set up your `.env`. Every task begins from here; if
   you're doing the whole lab in one sitting, you only need to do this once.
2. **Do any task.** Each task lists the setup it needs so you can start it independently. If
   you're moving straight from the previous task, a short *"Continuing from a previous task?"*
   note at the top lets you skip the repeated setup and keep going.

## Lab at a glance

Complete the **Core** tasks first (about **35 minutes**) - they end with a working analysis
and translation pipeline. Then expand the **Optional** task if it interests you. The full
lab takes about **1 hour 5 minutes**.

| Section | Task | Difficulty | Time |
| --- | --- | --- | --- |
| **Core** | [Task 1 – Analyze guest reviews](A1-analyze-guest-reviews.md) | ▰▰▱▱▱ L200 | ~20 min |
| **Core** | [Task 2 – Translate guest feedback](A2-translate-guest-feedback.md) | ▰▰▱▱▱ L200 | ~15 min |
| *Optional* | [Task 3 – Hand the job to an agent](A3-build-a-guest-feedback-agent.md) | ▰▰▰▱▱ L300 | ~30 min |

**Choosing your path** - pick the tasks that fit the time you have:

- **Core only (~35 min):** do Tasks 1-2. You'll have a working feedback pipeline.
- **Everything (~1h 5m):** add **Task 3** to see the same capabilities delivered through an
  agent and an MCP server instead of direct SDK calls.

> **One scenario, one resource**: every task in this lab talks to the same Microsoft
> Foundry resource. Azure Language, Azure Translator, and the agent runtime are all
> capabilities of that single resource - you just reach them through different endpoints
> and SDKs. The `.env` you build in Getting started holds all of them.

## Two ways to reach the same capability

There's more than one way to use Azure Language in Foundry Tools, and this lab shows you
**two**:

- **The SDK, called directly** - the approach you'll write in Tasks 1 and 2. You choose
  the operation (`detect_language`, `recognize_entities`, `recognize_pii_entities`), you
  send the document, and you handle the structured result. Deterministic, cheap, and
  completely under your control.
- **An agent calling the MCP server** - the approach in Task 3. You describe what you want
  in natural language and the agent decides which Language operations to call and in what
  order. Far less code, and it handles requests you didn't anticipate.

Neither is "more correct". Direct SDK calls are the right answer for a known, repeated
pipeline; an agent is the right answer for open-ended requests. Writing the pipeline by
hand first is what makes it obvious what the agent is doing for you in Task 3.

## Summary

Across this lab you:

- **Analyzed guest reviews** with Azure Language in Foundry Tools - detecting language,
  extracting entities, and producing a redacted version of each review safe to publish.
- **Translated guest feedback** with Azure Translator in Foundry Tools, letting the service
  detect the source language for you.
- (Optionally) **connected the Azure Language MCP server to an agent** and called that agent
  from your own client app, comparing the code you wrote by hand with the code the agent
  made unnecessary.

Together these show the two levers for working with unstructured text: calling **specialist
models** directly when you know exactly what you need, and delegating to an **agent** when
you don't.

## Clean up

If you're finished, delete the resources you created to avoid unnecessary Azure costs.

1. In the [Azure portal](https://portal.azure.com), navigate to the resource group that contains your Foundry resource.
1. On the toolbar, select **Delete resource group**, enter the resource group name, and confirm.
