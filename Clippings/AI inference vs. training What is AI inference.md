---
title: "AI inference vs. training: What is AI inference?"
source: "https://www.cloudflare.com/learning/ai/inference-vs-training/"
author:
published:
created: 2026-04-15
description: "AI inference is the process that a trained machine learning model uses to draw conclusions from brand-new data. Learn how AI inference and training differ."
tags:
  - "clippings"
---
Preview Mode

[Documentation](https://staging.mrk.cfdata.org/mrk/redwood-blade-repository/)

AI inference is when an AI model produces predictions or conclusions. AI training is the process that enables AI models to make accurate inferences.

#### Learning Objectives

After reading this article you will be able to:

- Define and explain AI inference
- Distinguish between AI training and AI inference
- Compare the amount of compute power used by AI inference vs. training

Copy article link

## What is AI inference?

In the field of [artificial intelligence (AI)](https://www.cloudflare.com/learning/ai/what-is-artificial-intelligence/), inference is the process that a trained [machine learning](https://www.cloudflare.com/learning/ai/what-is-machine-learning/) model\* uses to draw conclusions from brand-new data. An AI model capable of making inferences can do so without examples of the desired result. In other words, inference is an AI model in action.

An example of AI inference would be a self-driving car that is capable of recognizing a stop sign, even on a road it has never driven on before. The process of identifying this stop sign in a new context is inference.

Another example: A machine learning model trained on the past performance of professional sports players may be able to make predictions about the future performance of a given sports player before they are signed to a contract. Such a prediction is an inference.

\* *Machine learning is a type of AI.*

#### AI inference vs. training

- **Training** is the first phase for an AI model. Training may involve a process of trial and error, or a process of showing the model examples of the desired inputs and outputs, or both.
- **Inference** is the process that follows AI training. The better trained a model is, and the more fine-tuned it is, the better its inferences will be — although they are never guaranteed to be perfect.

To get to the point of being able to identify stop signs in new locations (or predict a professional athlete's performance), machine learning models go through a process of training. For the autonomous vehicle, its developers showed the model thousands or millions of images of stop signs. A vehicle running the model may have even been driven on roads (with a human driver as backup), enabling it to learn from trial and error. Eventually, after enough training, the model was able to identify stop signs on its own.

## What are some use cases for AI inference?

Almost any real-world application of AI relies on AI inference. Some of the most commonly used examples include:

- **[Large language models (LLMs):](https://www.cloudflare.com/learning/ai/what-is-large-language-model/)** A model trained on sample text can parse and interpret texts it has never seen before
- **[Predictive analytics:](https://www.cloudflare.com/learning/ai/what-is-predictive-ai/)** Once a model has been trained on past data and reaches the inference stage, it can make predictions based on incoming data
- **[Email security:](https://www.cloudflare.com/learning/email-security/what-is-email-security/)** A machine learning model can be trained to [recognize spam emails](https://www.cloudflare.com/learning/email-security/how-to-stop-spam-emails/) or [business email compromise](https://www.cloudflare.com/learning/email-security/business-email-compromise-bec/) attacks, then make inferences about incoming email messages, allowing email security filters to block malicious ones
- **Driverless cars:** As described in the above example, inference is hugely important for autonomous vehicles
- **Research:** Scientific and medical research depends on interpreting data, and AI inference can be used to draw conclusions from that data
- **Finance:** A model trained on past market performance can make (non-guaranteed) inferences about future market performance

## How does AI training work?

At its essence, AI training involves feeding AI models large data sets. Those data sets can be structured or unstructured, labeled or unlabeled. Some types of models may need specific examples of inputs and their desired outputs. Other models — such as [deep learning](https://www.cloudflare.com/learning/ai/what-is-deep-learning/) models — may only need raw data. Eventually the models learn to recognize patterns or correlations, and they can then make inferences based on new inputs.

As training progresses, developers may need to fine-tune the models. They have it provide some inferences right after the initial training process, then correct the outputs. Imagine an AI model has been tasked to identify the photos of dogs from a data set of pet photographs. If the model instead identifies photos of cats, it needs some tuning.

## How does AI compute power usage compare for inference vs. training?

AI programs extend the capabilities of computers to far beyond what they were able to do previously. But this comes at the cost of using much more processing power than traditional computer programs — just as, for a person, solving a complex mathematical equation requires more focus and concentration than solving "2 + 2."

Training an AI model can be very expensive in terms of compute power. But it is more or less a one-time expense. Once a model is properly trained, it ideally does not need to be trained further. If the model does need to be adapted to a new use case, developers can use less-intensive techniques like [low-rank adaption (LoRA)](https://www.cloudflare.com/learning/ai/what-is-lora/) instead of retraining the model from scratch.

Inference, however, is ongoing. If a model is actively in use, it is constantly applying its training to new data and making additional inferences. This takes quite a bit of compute power and can be very expensive.

## How does Cloudflare allow developers to run AI inference?

[Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/) offers developers access to GPUs all over the globe for running AI tasks. This pairs with [Vectorize](https://developers.cloudflare.com/vectorize/), a service for generating and storing embeddings for machine learning models. Cloudflare also offers cost-effective [object storage](https://www.cloudflare.com/learning/cloud/what-is-object-storage/) for maintaining collections of training data — [R2](https://www.cloudflare.com/developer-platform/products/r2/), a zero- [egress-fee](https://www.cloudflare.com/learning/cloud/what-are-data-egress-fees/) storage platform.

Learn more about [how Cloudflare enables developers to run AI inference at the edge](https://ai.cloudflare.com/).

## FAQs

#### What is the difference between AI training and AI inference?

AI training is the initial phase of AI development, when a model learns; while AI inference is the subsequent phase where the trained model applies its knowledge to new data to make predictions or draw conclusions.

#### How does AI training work?

AI training involves feeding a model large datasets, which can be structured or unstructured. The model learns to recognize patterns and correlations within this data. Developers might also fine-tune the model by correcting its initial outputs, a process similar to teaching through trial and error.

#### What is an example of AI inference?

A self-driving car recognizing a stop sign on a new road is an example of inference. The model controlling the car is applying its training to a situation it has not experienced before to make a correct identification.

#### Which process uses more computing power, training or inference?

Training an AI model can be very expensive in terms of computing power, but it is generally a one-time expense. Inference, on the other hand, is an ongoing process that uses a significant amount of computing power as the model is actively applied to new data.

#### What are some common use cases for AI inference?

Almost any real-world application of AI relies on inference. Common examples include large language models (LLMs) replying to new prompts, developers using "vibe coding" to build apps, predictive analytics making forecasts, cyber security products identifying new strains of malware, and financial models predicting market performance.

Navigated to AI inference vs. training: What is AI inference?