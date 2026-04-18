---
title: "What is an LLM (large language model)?"
source: "https://www.cloudflare.com/learning/ai/what-is-large-language-model/"
author:
published:
created: 2026-04-15
description: "An LLM, or large language model, is a machine learning model that can comprehend and generate human language. Learn how LLM models work."
tags:
  - "clippings"
---
Preview Mode

[Documentation](https://staging.mrk.cfdata.org/mrk/redwood-blade-repository/)

## What is a large language model (LLM)?

Large language models (LLMs) are machine learning models that can comprehend and generate human language text. They work by analyzing massive data sets of language.

#### Learning Objectives

After reading this article you will be able to:

Copy article link

## What is a large language model (LLM)?

A large language model (LLM) is a type of [artificial intelligence (AI)](https://www.cloudflare.com/learning/ai/what-is-artificial-intelligence/) program that can recognize and generate text, among other tasks. LLMs are trained on [huge sets of data](https://www.cloudflare.com/learning/ai/big-data/) — hence the name "large." LLMs are built on [machine learning](https://www.cloudflare.com/learning/ai/what-is-machine-learning/): specifically, a type of [neural network](https://www.cloudflare.com/learning/ai/what-is-neural-network/) called a transformer model.

In simpler terms, an LLM is a computer program that has been fed enough examples to be able to recognize and interpret human language or other types of complex data. Many LLMs are trained on data that has been gathered from the Internet — thousands or millions of gigabytes' worth of text. Some LLMs continue to [crawl the web](https://www.cloudflare.com/learning/bots/what-is-a-web-crawler/) for more content after they are initially trained. But the quality of the samples impacts how well LLMs will learn natural language, so an LLM's programmers may use a more curated data set, at least at first.

LLMs use a type of machine learning called [deep learning](https://www.cloudflare.com/learning/ai/what-is-deep-learning/) in order to understand how characters, words, and sentences function together. Deep learning involves the probabilistic analysis of unstructured data, which eventually enables the deep learning model to recognize distinctions between pieces of content without human intervention.

LLMs are then further trained via tuning: they are fine-tuned or prompt-tuned to the particular task that the programmer wants them to do, such as interpreting questions and generating responses, or translating text from one language to another.

## What are LLMs used for?

LLMs can be trained to do a number of tasks. One of the most well-known uses is their application as [generative AI](https://www.cloudflare.com/learning/ai/what-is-generative-ai/): when given a prompt or asked a question, they can produce text in reply. The publicly available LLM ChatGPT, for instance, can generate essays, poems, and other textual forms in response to user inputs.

Any large, complex data set can be used to train LLMs, including programming languages. Some LLMs can help programmers write code. They can write functions upon request — or, given some code as a starting point, they can finish writing a program. LLMs may also be used in:

- Sentiment analysis
- DNA research
- Customer service
- [Chatbots](https://www.cloudflare.com/learning/bots/what-is-a-chatbot/)
- Online search

Examples of real-world LLMs include ChatGPT (from OpenAI), Bard (Google), Llama (Meta), and Bing Chat (Microsoft). GitHub's Copilot is another example, but for coding instead of natural human language.

## How do large language models work?

#### Machine learning and deep learning

At a basic level, LLMs are built on machine learning. Machine learning is a subset of AI, and it refers to the practice of feeding a program large amounts of data in order to train the program how to identify features of that data without human intervention.

LLMs use a type of machine learning called deep learning. Deep learning models can essentially train themselves to recognize distinctions without human intervention, although some human fine-tuning is typically necessary.

Deep learning uses probability in order to "learn." For instance, in the sentence "The quick brown fox jumped over the lazy dog," the letters "e" and "o" are the most common, appearing four times each. From this, a deep learning model could conclude (correctly) that these characters are among the most likely to appear in English-language text.

Realistically, a deep learning model cannot actually conclude anything from a single sentence. But after analyzing trillions of sentences, it could learn enough to predict how to logically finish an incomplete sentence, or even generate its own sentences.

#### LLM neural networks

In order to enable this type of deep learning, LLMs are built on neural networks. Just as the human brain is constructed of neurons that connect and send signals to each other, an artificial neural network (typically shortened to "neural network") is constructed of network nodes that connect with each other. They are composed of several "layers”: an input layer, an output layer, and one or more layers in between. The layers only pass information to each other if their own outputs cross a certain threshold.

#### LLM transformer models

The specific kind of neural networks used for LLMs are called transformer models. Transformer models are able to learn context — especially important for human language, which is highly context-dependent. Transformer models use a mathematical technique called self-attention to detect subtle ways that elements in a sequence relate to each other. This makes them better at understanding context than other types of machine learning. It enables them to understand, for instance, how the end of a sentence connects to the beginning, and how the sentences in a paragraph relate to each other.

This enables LLMs to interpret human language, even when that language is vague or poorly defined, arranged in combinations they have not encountered before, or contextualized in new ways. On some level they "understand" semantics in that they can associate words and concepts by their meaning, having seen them grouped together in that way millions or billions of times.

## What are some advantages and limitations of LLMs?

A key characteristic of LLMs is their ability to respond to unpredictable queries. A traditional computer program receives commands in its accepted syntax, or from a certain set of inputs from the user. A video game has a finite set of buttons, an application has a finite set of things a user can click or type, and a programming language is composed of precise if/then statements.

By contrast, an LLM can respond to natural human language and use data analysis to answer an unstructured question or prompt in a way that makes sense. Whereas a typical computer program would not recognize a prompt like "What are the four greatest funk bands in history?", an LLM might reply with a list of four such bands, and a reasonably cogent defense of why they are the best.

In terms of the information they provide, however, LLMs can only be as reliable as the data they ingest. If fed false information, they will give false information in response to user queries. LLMs also sometimes " [hallucinate](https://www.cloudflare.com/learning/ai/what-are-ai-hallucinations/) ": they create fake information when they are unable to produce an accurate answer. For example, in 2022 news outlet Fast Company [asked](https://www.fastcompany.com/90819887/how-to-trick-openai-chat-gpt) ChatGPT about the company Tesla's previous financial quarter; while ChatGPT provided a coherent news article in response, much of the information within was invented.

In terms of [security](https://www.cloudflare.com/the-net/ai-secure/), user-facing applications based on LLMs are as prone to bugs as any other application. LLMs can also be manipulated via malicious inputs to provide certain types of responses over others — including responses that are dangerous or unethical. Finally, one of the [security problems with LLMs](https://www.cloudflare.com/the-net/vulnerable-llm-ai/) is that users may upload secure, confidential data into them in order to increase their own productivity. But LLMs use the inputs they receive to further train their models, and they are not designed to be secure vaults; they may expose confidential data in response to queries from other users. Learn more about the [best ways to secure LLMs.](https://www.cloudflare.com/learning/ai/what-is-ai-security/)

## How developers can quickly start building their own LLMs

To build LLM applications, developers need easy access to multiple data sets, and they need places for those data sets to live. Both cloud storage and on-premises storage for these purposes may involve infrastructure investments outside the reach of developers' budgets. Additionally, training data sets are typically stored in multiple places, but [moving that data](https://www.cloudflare.com/the-net/cloud-egress-fees-challenge-future-ai/) to a central location may result in massive [egress fees](https://www.cloudflare.com/learning/cloud/what-are-data-egress-fees/).

Fortunately, Cloudflare offers several services to allow developers to quickly start spinning up LLM applications, and other types of AI. Vectorize is a globally distributed vector database for querying data stored in no-egress-fee object storage ([R2](https://www.cloudflare.com/developer-platform/products/r2/)) or documents stored in [Workers Key Value](https://www.cloudflare.com/developer-platform/workers-kv/). Combined with the development platform [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/), developers can use Cloudflare to quickly start experimenting with their own LLMs.

## FAQs

#### What is a large language model (LLM)?

A large language model is an AI model that is trained on huge sets of data to recognize, interpret, and generate text. When prompted, large language models can produce text or blocks of code within seconds. Users can prompt large language models using natural language, instead of through a predefined user interface or via programming languages.

#### How do large language models work?

LLMs use a process called deep learning to analyze vast amounts of unstructured data and learn from it. They are built on artificial neural networks — specifically, transformer models — that use a technique called self-attention that allows the model to learn and understand context, which is crucial for interpreting human language.

#### What are LLMs used for?

LLMs can be trained for many tasks. One of the most popular uses is generative AI, where they create text in response to a user's prompt. They are also used in sentiment analysis, customer service chatbots, online search, and even to help programmers write code.

#### What are some examples of real-world LLMs?

Well-known examples include ChatGPT from OpenAI, Gemini from Google, Llama from Meta, and Bing Chat from Microsoft. For programming, GitHub's Copilot is a prominent example.

#### What is a key advantage of LLMs compared to other applications?

A major advantage of LLMs is their ability to respond to unpredictable and unstructured queries. Unlike a traditional computer program that requires specific commands, an LLM can understand and respond to natural human language, even if the question is vague or phrased in a way it has never seen before. Users may need to refine their prompts somewhat to get the exact result they want, but even unclear prompts typically result in intelligible responses.

#### What are the limitations or risks associated with LLMs?

LLMs are only as reliable as the data they are trained on and can provide false information if fed incorrect data. They are also known to "hallucinate" or invent information. From a security perspective, they can be manipulated with malicious inputs and are not designed to be secure vaults, meaning users risk exposing confidential data via their inputs.