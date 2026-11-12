---
lab:
    title: 'Build speech-enabled apps and agents'
    description: 'Build the Alpine Ski House guest services voice line: synthesize greetings, transcribe voicemail, generate speech with AI models, translate spoken requests, and finish with a real-time voice concierge. A modular lab you can complete end to end or one task at a time.'
    level: 400
    concepts: 'speech synthesis, speech recognition, generative AI audio models, speech translation, voice agents'
    duration: 50
    islab: true
    status: 'draft'
---

# Build speech-enabled apps and agents

**Difficulty** ▰▰▰▰▱ **L400**  (filled bars out of 5; **L100** beginner → **L500** expert)

Speech is the interface people reach for when their hands are full and their gloves are on.
In this lab you'll build the Alpine Ski House guest services voice line, starting with a
simple recorded greeting and ending with an agent you can genuinely hold a conversation with.

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
<summary>Speech service or speech-capable model?</summary>
<div class="concept-body" markdown="1">

Both convert between audio and text, and this lab uses both - deliberately.

**Azure Speech in Foundry Tools** is a specialist service. You pick a named voice, point it
at a file or a microphone, and get back a deterministic result. It handles the awkward parts
of real audio - streaming, microphones, speakers, long recordings - and it's what you want
for a voicemail system.

**Speech-capable generative AI models** treat audio as just another modality. You can tell a
text-to-speech model *how* to say something ("speak in a warm, welcoming tone") in plain
language, which the specialist service expresses through voice selection and markup instead.

Rule of thumb: reach for the service when you need reliable audio plumbing, and for a model
when you need expressive control or you're already in a model-based pipeline.

</div>
</details>

**Your scenario:** you work at **Alpine Ski House**, a group of mountain resorts with lodges
in Zermatt, Whistler, and Chamonix. The guest services desk is buried in voicemail, guests
call from all over the world in every language, and nobody can answer the phone while riding
a chairlift. Across this lab you'll build the voice tooling that fixes that, adding one
capability per task.

You'll start with the **Core** tasks that get you to a working voice application as quickly
as possible. From there, a set of **Optional** tasks lets you go deeper into the areas that
interest you most.

> **Note**: Some of the technologies used in this exercise are in preview or in active
> development. You may experience some unexpected behavior, warnings, or errors.

## What you'll learn

By completing the **Core** tasks of this exercise, you'll be able to:

- **Synthesize and recognize speech** with Azure Speech in Foundry Tools - generating a
  spoken greeting as an audio file, and transcribing recorded guest voicemail.
- **Use speech-capable generative AI models** for both text-to-speech and speech-to-text,
  and steer the delivery with natural-language instructions.

The **Optional** tasks let you additionally:

- **Translate spoken requests in real time**, transcribing what a guest says and speaking the
  translation back in three languages.
- **Give an agent speech skills** by connecting the Azure Speech in Foundry Tools MCP server,
  then calling that agent from your own client application.
- **Build a real-time voice concierge** with Azure Speech Voice Live, including barge-in,
  echo cancellation, and noise suppression.

## How this lab is organized

This lab is **modular**. Each task is written to be completed **on its own, starting fresh** -
so you can pick a single task and do just that one. Every task also shares one starter folder,
one virtual environment, and one `.env`, so if you'd rather work straight through, you can.

1. **Start with [Getting started](B0-getting-started.md)** - create your Microsoft Foundry
   project, deploy the models you need, get the starter code, and set up your `.env`. Every
   task begins from here; if you're doing the whole lab in one sitting, you only need to do
   this once.
2. **Do any task.** Each task lists the setup it needs so you can start it independently. If
   you're moving straight from the previous task, a short *"Continuing from a previous task?"*
   note at the top lets you skip the repeated setup and keep going.

## Lab at a glance

Complete the **Core** tasks first (about **50 minutes**) - they end with a working voice
application built two different ways. Then expand any **Optional** tasks that interest you.
The full lab, including all optional tasks, takes about **2 hours 20 minutes**.

| Section | Task | Difficulty | Time |
| --- | --- | --- | --- |
| **Core** | [Task 1 – Build the guest services line](B1-build-the-guest-services-line.md) | ▰▰▱▱▱ L200 | ~25 min |
| **Core** | [Task 2 – Use speech-capable AI models](B2-use-speech-capable-ai-models.md) | ▰▰▰▱▱ L300 | ~25 min |
| *Optional* | [Task 3 – Translate spoken requests](B3-translate-spoken-requests.md) | ▰▰▰▱▱ L300 | ~20 min |
| *Optional* | [Task 4 – Give an agent speech skills](B4-give-an-agent-speech-skills.md) | ▰▰▰▱▱ L300 | ~30 min |
| *Optional* | [Task 5 – Build a real-time voice concierge](B5-build-a-real-time-voice-concierge.md) | ▰▰▰▰▱ L400 | ~30 min |

**Choosing your path** - pick the tasks that fit the time you have:

- **Core only (~50 min):** do Tasks 1-2. You'll have used both approaches to speech.
- **Core + recommended (~1h 50m):** also do **Task 3** and **Task 4**.
- **Everything (~2h 20m):** add **Task 5**, the real-time voice concierge. It's the most
  involved task in the lab and works best with a headset.

> **A note on hardware**: Tasks 3 and 5 use your **microphone and speakers**. Task 5 in
> particular works best with a headset - with open speakers there's a risk the agent "hears"
> its own responses and treats them as new input. Tasks 1, 2, and 4 work with audio files
> only, so they're fine on any machine.

## Two ways to give something a voice

This lab deliberately shows you the same capability at two levels of abstraction:

- **You write the audio handling** - Tasks 1, 2, and 3. You create a config, attach an audio
  source or sink, call recognize or synthesize, and check a result reason. You can see every
  moving part, which is what makes the next approach meaningful.
- **The agent handles it** - Tasks 4 and 5. In Task 4 the agent calls speech operations
  through an MCP server; in Task 5 the Voice Live SDK manages an entire duplex conversation,
  including deciding when the guest has stopped speaking. Your code shrinks to configuration
  and event handling.

Neither is "more correct". Task 1's approach is exactly right for batch-transcribing a
voicemail box; Task 5's is the only sane way to build a conversation.

## Summary

Across this lab you:

- Built the **guest services line**, synthesizing a spoken greeting and transcribing recorded
  voicemail with the Azure Speech SDK.
- Used **speech-capable generative AI models** to generate and transcribe speech, steering
  delivery with plain-language instructions.
- (Optionally) **translated spoken requests** into three languages and spoke each translation
  back in a native voice.
- (Optionally) **connected the Azure Speech MCP server to an agent** and drove it from a
  client app.
- (Optionally) built a **real-time voice concierge** with Azure Speech Voice Live, handling
  interruptions, echo, and background noise.

Together these show the range of speech on Azure: from a single deterministic API call, all
the way to a live conversation you can interrupt.

## Clean up

If you're finished, delete the resources you created to avoid unnecessary Azure costs.

1. In the [Azure portal](https://portal.azure.com), navigate to the resource group that contains your Foundry resource.
1. On the toolbar, select **Delete resource group**, enter the resource group name, and confirm.

> If you completed Task 4, remember that it also created an **Azure storage account** for the
> generated audio files. Delete that too if it's in a different resource group.
