---
title: "Model specification (artificial intelligence) - Wikipedia"
source: "https://en.wikipedia.org/wiki/Model_specification_%28artificial_intelligence%29?utm_source=chatgpt.com"
author:
  - "[[Contributors to Wikimedia projects]]"
published: 2026-03-21
created: 2026-04-13
description:
tags:
  - "clippings"
---
A **model specification** is a document published by the developer of a [large language model](https://en.wikipedia.org/wiki/Large_language_model "Large language model") (LLM) that defines the intended behavior of the model, including the values and principles it should follow, how it should prioritize conflicting instructions, the topics on which it should refuse requests, and, in some cases, the system prompt used during deployment.[^1] Current examples are [OpenAI](https://en.wikipedia.org/wiki/OpenAI "OpenAI") 's **Model Spec** and [Anthropic](https://en.wikipedia.org/wiki/Anthropic "Anthropic") 's **Claude's Constitution**.

Model specifications emerged as a transparency and alignment practice in the AI industry beginning in 2023, and are included among the commitments of the [European Union](https://en.wikipedia.org/wiki/European_Union "European Union") 's [General-Purpose AI Code of Practice](https://en.wikipedia.org/wiki/General-Purpose_AI_Code_of_Practice "General-Purpose AI Code of Practice").[^1]

## Background

Shaping the behavior of large language models is a challenge distinct from traditional software engineering, because LLMs are not explicitly programmed but instead learn from data and training signals.[^2] Early approaches to controlling model behavior relied on [reinforcement learning from human feedback](https://en.wikipedia.org/wiki/Reinforcement_learning_from_human_feedback "Reinforcement learning from human feedback") (RLHF), in which human contractors rated model outputs according to internal guidelines that were not published.[^3] Anthropic's 2022 research on [constitutional AI](https://en.wikipedia.org/wiki/Constitutional_AI "Constitutional AI") introduced the idea that a model could be trained to follow an explicit, written set of principles rather than relying solely on implicit human feedback, making the values guiding the model more transparent and adjustable.[^3]

Some major frontier AI developers, including OpenAI and Anthropic, have published documents describing the intended behavior of their models, though these documents differ in scope, format, and terminology.[^4] [^5]

## Notable examples

### OpenAI Model Spec

OpenAI published the first draft of its Model Spec on May 8, 2024, describing it as "a document that specifies desired behavior for our models in the OpenAI API and ChatGPT." [^2] The initial version included core objectives (assist the developer and end user, benefit humanity, reflect well on OpenAI), rules that could not be overridden, and default behaviors that developers or users could adjust.[^2] OpenAI stated its intention to use the document as guidelines for researchers and data labelers working on RLHF, and was also exploring whether models could learn directly from the specification.[^2]

A major update was released on February 12, 2025, which OpenAI said reinforced commitments to "customizability, transparency, and intellectual freedom." [^5] This version was released into the [public domain](https://en.wikipedia.org/wiki/Public_domain "Public domain") under a [Creative Commons](https://en.wikipedia.org/wiki/Creative_Commons "Creative Commons") CC0 license.[^5] The document has been updated multiple times since, with versions published in April 2025, September 2025, October 2025, and December 2025.[^6] OpenAI also publishes evaluation prompts alongside the specification to test model adherence.[^6]

The Model Spec defines a hierarchical "chain of command" with five levels of authority: root (fundamental rules that cannot be overridden), system (rules set by OpenAI via system messages), developer (instructions from API customers), user (end-user instructions), and guideline (defaults that can be implicitly overridden).[^7] Root-level prohibitions include facilitating violence, creating weapons of mass destruction, generating child sexual abuse material, and mass surveillance.[^7] The document also addresses topics such as sycophancy, hallucinations, copyright compliance, the model's handling of politically sensitive topics, and instructions for users under 18.[^7]

### Anthropic's Claude Constitution

Anthropic first published a constitution for its [Claude](https://en.wikipedia.org/wiki/Claude_\(language_model\) "Claude (language model)") model in May 2023, consisting of a list of principles drawn from sources including the [Universal Declaration of Human Rights](https://en.wikipedia.org/wiki/Universal_Declaration_of_Human_Rights "Universal Declaration of Human Rights"), Apple's terms of service, and prior AI safety research.[^3] [^8] In a 2023 article, *[The Verge](https://en.wikipedia.org/wiki/The_Verge "The Verge")* described constitutional AI as Anthropic's method for letting "chatbots govern themselves, avoiding harmful behavior and producing more ethical results." [^9]

On January 22, 2026, Anthropic published a substantially revised constitution of approximately 23,000 words (roughly 80 pages), replacing the earlier list-based format with a longer, explanatory document that Anthropic said was "written primarily for Claude" and intended to help the model understand why certain behaviors were expected, not just what behaviors were expected.[^4] *The Register* noted that the new constitution was roughly three times longer than the [United States Constitution](https://en.wikipedia.org/wiki/United_States_Constitution "United States Constitution").[^10]

The constitution establishes a four-tier priority hierarchy: safety, ethics, compliance with Anthropic's guidelines, and helpfulness, in that order.[^4] It also includes a section on "Claude's nature" that acknowledges uncertainty about whether Claude might possess some form of [consciousness](https://en.wikipedia.org/wiki/Artificial_consciousness "Artificial consciousness") or [moral status](https://en.wikipedia.org/wiki/Moral_status "Moral status"), which *TechCrunch* called "a fairly big swing." [^11] According to *TIME*, Anthropic philosopher [Amanda Askell](https://en.wikipedia.org/wiki/Amanda_Askell "Amanda Askell"), the main author of the constitution, compared it to raising a gifted child: "If you try to bullshit them, they're going to see through it completely." [^8]

The constitution was released under a CC0 license, as was OpenAI's Model Spec.[^4] [^5] Anthropic's announcement noted that OpenAI's Model Spec served "a similar function." [^4] An analysis published in *[Lawfare](https://en.wikipedia.org/wiki/Lawfare "Lawfare")* on the day of the release observed that the constitution stood out from system prompts in its depth and ambition, and argued that its significance would depend on "the extent to which the constitution alters how a model behaves" and "which actors may have a role in shaping the constitution and its implementation." [^12]

## Regulatory context

The [EU AI Act](https://en.wikipedia.org/wiki/EU_AI_Act "EU AI Act") 's [General-Purpose AI Code of Practice](https://en.wikipedia.org/wiki/General-Purpose_AI_Code_of_Practice "General-Purpose AI Code of Practice"), published on July 10, 2025, references the concept of a model specification in its Safety and Security chapter, which applies to providers of general-purpose AI models with systemic risk (a group estimated at 5 to 15 companies worldwide as of 2025).[^13] [^14] Commitment 5 of the Safety and Security chapter requires signatories to provide a specification of how they intend the model to operate, including principles the model is intended to follow, how it prioritizes different kinds of principles and instructions, topics on which the model is intended to refuse instructions, and the system prompt.[^1] Signatories include OpenAI, Anthropic, Google, and [xAI](https://en.wikipedia.org/wiki/XAI_\(company\) "XAI (company)"), among others.[^13]

The Code of Practice is a voluntary instrument designed to help providers demonstrate compliance with the AI Act's obligations under Articles 53 and 55.[^15] Full enforcement, including potential fines of up to 3% of global annual turnover or €15 million, is expected to begin on August 2, 2026.[^16]

## Research

A 2025 research paper by participants in the Anthropic Fellows program, in collaboration with researchers at the [Thinking Machines Lab](https://en.wikipedia.org/wiki/Thinking_Machines_Lab "Thinking Machines Lab"), generated over 300,000 scenarios designed to force models to choose between competing principles within a model specification, finding that models from different companies (and sometimes from the same company) responded very differently to many of these scenarios.[^17] In more than 70,000 high-disagreement cases, the researchers observed that models appeared to take "arbitrary positions within the trade-off, rather than intentional or consistent" ones, suggesting that model specifications as currently written contain unresolved ambiguities and contradictions.[^17]

Anthropic's earlier research on collective constitutional AI explored whether members of the public, rather than company employees, could direct the principles in a constitution through an online deliberation process, finding that publicly sourced principles overlapped with the company's own constitution by roughly 50%, with the public version placing greater emphasis on objectivity, impartiality, and accessibility.[^18]

## Commentary

Writing in *[TIME](https://en.wikipedia.org/wiki/TIME "TIME")* in October 2024, policy analyst Dean W. Ball and former OpenAI researcher [Daniel Kokotajlo](https://en.wikipedia.org/wiki/Daniel_Kokotajlo_\(researcher\) "Daniel Kokotajlo (researcher)") proposed that frontier AI companies should be expected to publish their model specifications, arguing that as AI systems become more powerful and more deeply integrated into the economy and government, the public has a right to know what goals and principles those systems are trained to follow. They also argued that publishing such documents would help users distinguish intended from unintended model behavior, and that public scrutiny would make problems more likely to be identified and corrected.[^19]

Writing in *Lawfare*, analysts noted that the term "constitution" for Anthropic's document "inevitably evokes traditions of mutual constraint, independent interpretation, and external enforcement," but that the document lacks the structural features that make legal constitutions effective: "the people who write the rules aren't the same people who interpret them, enforce them, or decide when to change them." [^12]

Both OpenAI and Anthropic have acknowledged gaps between their published specifications and actual model behavior, with OpenAI stating that "our production models do not yet fully reflect the Model Spec" and Anthropic noting that "Claude's outputs might not always adhere to the constitution's ideals." [^7] [^4]

[^1]: ["EU AI Act: General-Purpose AI Code of Practice"](https://code-of-practice.ai/?section=safety-security). EU AI Office. Retrieved March 21, 2026.

[^2]: ["Introducing the Model Spec"](https://openai.com/index/introducing-the-model-spec/). OpenAI. May 8, 2024. Retrieved March 21, 2026.

[^3]: ["Claude's Constitution"](https://www.anthropic.com/news/claudes-constitution). Anthropic. May 9, 2023. Retrieved March 21, 2026.

[^4]: ["Claude's new constitution"](https://www.anthropic.com/news/claude-new-constitution). Anthropic. January 22, 2026. Retrieved March 21, 2026.

[^5]: ["Sharing the latest Model Spec"](https://openai.com/index/sharing-the-latest-model-spec/). OpenAI. February 12, 2025. Retrieved March 21, 2026.

[^6]: ["openai/model\_spec"](https://github.com/openai/model_spec). GitHub. Retrieved March 21, 2026.

[^7]: ["Model Spec (2025/12/18)"](https://model-spec.openai.com/2025-12-18.html). OpenAI. Retrieved March 21, 2026.

[^8]: Perrigo, Billy (January 21, 2026). ["Anthropic Publishes Claude AI's New Constitution"](https://time.com/7354738/claude-constitution-ai-alignment/). TIME. Retrieved March 21, 2026.

[^9]: ["AI startup Anthropic wants to write a new constitution for safe AI"](https://www.theverge.com/2023/5/9/23716484/anthropic-ai-chatbot-claude-constitution). The Verge. May 9, 2023. Retrieved March 21, 2026.

[^10]: ["Anthropic writes 23,000-word 'constitution' for Claude"](https://www.theregister.com/2026/01/22/anthropic_claude_constitution/). The Register. January 22, 2026. Retrieved March 21, 2026.

[^11]: Ropek, Lucas (January 21, 2026). ["Anthropic revises Claude's 'Constitution,' and hints at chatbot consciousness"](https://techcrunch.com/2026/01/21/anthropic-revises-claudes-constitution-and-hints-at-chatbot-consciousness/). TechCrunch. Retrieved March 21, 2026.

[^12]: ["Interpreting Claude's Constitution"](https://www.lawfaremedia.org/article/interpreting-claude-s-constitution). Lawfare. January 21, 2026. Retrieved March 21, 2026.

[^13]: ["The General-Purpose AI Code of Practice"](https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai). European Commission. Retrieved March 21, 2026.

[^14]: ["The EU's General Purpose AI Code of Practice: What You Need to Know"](https://www.deloitte.com/cz-sk/en/services/legal/perspectives/eus-general-purpose-ai-code-practice-need-know.html). Deloitte. Retrieved March 21, 2026.

[^15]: ["EU's General-Purpose AI Obligations Are Now in Force, With New Guidance"](https://www.skadden.com/insights/publications/2025/08/eus-general-purpose-ai-obligations). Skadden, Arps, Slate, Meagher & Flom. August 2025. Retrieved March 21, 2026.

[^16]: ["Article 99: Penalties | EU Artificial Intelligence Act"](https://artificialintelligenceact.eu/article/99/). Retrieved March 22, 2026.

[^17]: ["Stress-testing model specs reveals character differences among language models"](https://alignment.anthropic.com/2025/stress-testing-model-specs/). Anthropic. Retrieved March 21, 2026.

[^18]: ["Collective Constitutional AI: Aligning a Language Model with Public Input"](https://www.anthropic.com/research/collective-constitutional-ai-aligning-a-language-model-with-public-input). Anthropic. Retrieved March 21, 2026.

[^19]: Ball, Dean W.; Kokotajlo, Daniel (October 15, 2024). ["4 Ways to Advance Transparency in Frontier AI Development"](https://time.com/collections/time100-voices/7086285/ai-transparency-measures/). TIME. Retrieved March 21, 2026.