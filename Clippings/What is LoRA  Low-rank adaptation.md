---
title: "What is LoRA? | Low-rank adaptation"
source: "https://www.cloudflare.com/learning/ai/what-is-lora/"
author:
published:
created: 2026-04-15
description: "Low-rank adaptation, or LoRA, is a less expensive, more efficient method for adapting large machine learning models to specific uses. Learn how LoRA works."
tags:
  - "clippings"
---
Preview Mode

[Documentation](https://staging.mrk.cfdata.org/mrk/redwood-blade-repository/)

## What is low-rank adaptation (LoRA)?

Low-rank adaptation (LoRA) is a way to adapt a large machine learning model for specific uses without retraining the entire model.

#### Learning Objectives

After reading this article you will be able to:

Related Content

---

#### Want to keep learning?

Subscribe to theNET, Cloudflare's monthly recap of the Internet's most popular insights!

Copy article link

## What is low-rank adaptation (LoRA)?

Low-rank adaptation (LoRA) is a technique for quickly adapting [machine learning](https://www.cloudflare.com/learning/ai/what-is-machine-learning/) models to new contexts. LoRA helps make huge and complicated machine learning models much more suited for specific uses. It works by adding lightweight pieces to the original model, as opposed to changing the entire model. LoRA helps developers quickly expand the use cases for the machine learning models they build.

## What does LoRA do?

Large and complex machine learning models, such as those used for [large language models (LLMs)](https://www.cloudflare.com/learning/ai/what-is-large-language-model/) like ChatGPT, take a long time and a lot of resources to set up. They may have trillions of parameters that are set to specific values. Once this process is complete, the model may be powerful and accurate in general, but it is not necessarily fine-tuned to carry out specific tasks.

Getting a model to work in specific contexts can require a great deal of retraining, changing all its parameters. With the amount of parameters in such models, this retraining is expensive and time-consuming. LoRA provides a quick way to adapt the model without retraining it.

Imagine Jim moves from Europe to North America and all his appliances (microwave, hot water pot, and so on) do not fit the outlets in his new house, since these two regions follow different standards for electric plugs. Jim has two options. He could rip out and replace all the outlets in his home so that they fit the plugs on his appliances. Or, he could simply purchase a few cheap outlet adapters and plug in his appliances that way.

LoRA is like Jim's second option. Instead of completely retraining a model from start to finish, LoRA adds a lightweight, changeable part to the model so that it fits the new context. For AI developers, this is much faster and less resource intensive, just as purchasing a few adapters at the hardware store is cheaper for Jim than hiring a contractor to go into his walls and replace the electrical outlets.

## How does low-rank adaptation impact a machine learning model?

A machine learning model is the combination of a machine learning algorithm with a data set. The result of this combination is a computer program that can identify patterns, find objects, or draw relationships between items even in data sets it has not seen before.

For complex tasks like [generating text](https://www.cloudflare.com/learning/ai/what-is-generative-ai/), producing images, or carrying out other modern-day applications of machine learning, the models draw from a lot of data and use highly complex algorithms. Slight changes to the algorithms or the data set mean that the model will produce different results. However, getting the kinds of results that are needed in a specific context can take a lot of training.

Instead of re-doing the whole model, LoRA freezes the weights\* and parameters of the model as they are. Then on top of this original model, it adds a lightweight addition called a low-rank matrix, which is then applied to new inputs to get results specific to the context. The low-rank matrix adjusts for the weights of the original model so that outputs match the desired use case.

\* *In machine learning models, a "weight" is a mathematical value that helps determine how important different types of inputs are.*

## What is a low-rank matrix in LoRA?

A matrix, in mathematics, is an array or collection of numbers, like:

![Low-Rank Matrix Example: First column 2 4 6, second column 4 8 12, third column 6 12 18](https://cf-assets.www.cloudflare.com/slt3lc6tev37/VVNsQ2Ah92NypTI4c0MO5/087a575ef69de9941b1e407bad8798b1/low-rank-matrix.png "Low-Rank Matrix Example")

Matrices are an important part of how machine learning models and [neural networks](https://www.cloudflare.com/learning/ai/what-is-neural-network/) work. For such uses, they can be much larger than the example above. For LoRA, the important thing to understand is that low-rank matrices are smaller and have many fewer values than larger matrices. They do not take up much memory and require fewer steps to add or multiply together. This makes them faster for computers to process.

LoRA adds low-rank matrices to the frozen original machine learning model. These matrices contain new weights to apply to the model when generating results. This process alters the outputs that the model produces with minimal computing power and training time.

In the analogy used above, Jim bought cheap adapters to plug his appliances into the wall. Low-rank matrices are like those cheap adapters, with the outlets being the original machine learning models.

## How does machine learning work?

[Machine learning](https://www.cloudflare.com/learning/ai/what-is-machine-learning/) is a term that refers to a type of statistical algorithm that can learn to find patterns in data, without receiving specific instructions from a human. Machine learning can generalize from examples to classify data it has never seen before. It is foundational for many types of [artificial intelligence (AI)](https://www.cloudflare.com/learning/ai/what-is-artificial-intelligence/) applications.

Cloudflare enables developers to quickly integrate popular machine learning models through services such as:

- [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/), a global network of GPUs available to developers
- [Cloudflare Vectorize](https://developers.cloudflare.com/vectorize/), a globally distributed [vector database](https://www.cloudflare.com/learning/ai/what-is-vector-database/)
- [Cloudflare AI Gateway](https://developers.cloudflare.com/ai-gateway/), which allows developers to gain visibility and control over their AI apps
- [Cloudflare R2](https://www.cloudflare.com/developer-platform/products/r2/), [object storage](https://www.cloudflare.com/learning/cloud/what-is-object-storage/) with no [egress fees](https://www.cloudflare.com/learning/cloud/what-are-data-egress-fees/), which allows developers to store and access training data sets in a cost-effective way

Learn more about the full [Cloudflare for AI platform](https://ai.cloudflare.com/).

## FAQs

#### What is low-rank adaptation (LoRA)?

Low-rank adaptation (LoRA) is a method for rapidly adapting machine learning models to new use cases without retraining them. It enables developers to customize models for specific contexts. LoRA works by appending a lightweight addition, called a low-rank matrix, to the original model. This matrix tweaks the outputs of the model, similar to how a piece of colored translucent plastic can quickly shift the color of a spotlight.

#### What is a low-rank matrix in LoRA?

In low-rank adaptation (LoRA), a low-rank matrix is a small, computationally efficient matrix (or array of numbers) added to a machine learning model. It allows for targeted adaptation of the model’s outputs.

#### What is lightweight model modification in LoRA?

Lightweight model modification means adding small, changeable components to an existing machine learning model. This makes updates faster and uses far fewer computational resources compared to retraining the whole model.

#### Why is machine learning adaptability important, and how does LoRA help?

Machine learning adaptability is important for quickly and cost-effectively updating models for new tasks. LoRA helps by letting developers make targeted changes without the need for expensive, time-consuming retraining.

#### What are model weights in machine learning?

Model weights are mathematical values in a machine learning model that determine the importance of different types of inputs. Adjusting these weights changes how the model interprets and processes data.

#### How does LoRA relate to neural network optimization?

LoRA is a neural network optimization technique that improves model performance for specific tasks by adding low-rank matrices, enhancing adaptability without the need for extensive retraining of the neural network.

Navigated to What is low-rank adaptation (LoRA)?