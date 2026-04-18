---
title: "LLM routing for quality, low-cost responses"
source: "https://research.ibm.com/blog/LLM-routers"
author:
  - "[[Kim Martineau]]"
published: 2024-10-10
created: 2026-04-13
description: "IBM researchers design an LLM router that analyzes incoming queries and hands them off in real time to the most cost-effective model."
tags:
  - "clippings"
---
## An air traffic controller for LLMs

IBM researchers have designed an LLM routing method that analyzes incoming queries and hands them off in real time to the model most likely to provide a cost-effective response.

![](https://research.ibm.com/_next/image?url=https%3A%2F%2Fresearch-website-prod-cms-uploads.s3.us.cloud-object-storage.appdomain.cloud%2FAn_air_traffic_controller_for_LL_Ms_4_122f876870.png&w=3840&q=85)

Just two years ago, a few proprietary, general-purpose large language models dominated the AI market. Today, there are [141,000 LLMs](https://huggingface.co/models?pipeline_tag=text-generation&sort=trending) open-sourced on Hugging Face alone — many of them relatively small and built for specialized tasks. Not only are these smaller, purpose-built models cheaper to serve, they run faster and often perform better than the proprietary models on individual queries.

In this new world of LLM abundance, you can now mix and match models based on your desired price, performance level, or inference speed thanks to a new technology called the LLM router.

Almost like an air traffic controller, the router evaluates your query and sends it to the LLM in your library that seems to offer the best value. Rather than route every query to a general-purpose model, routers let you pick and choose among a set of models by price, quality, latency, or any other criteria you might have.

“When ChatGPT was the only good model out there, there weren’t a lot of options,” said Mikhail Yurochkin, an IBM researcher working on AI-optimization strategies. “Now, we have the opportunity to consider price, performance, and other goals in deciding which model to use.”

Routers can cut inferencing costs by up to 85%, by [one estimate](https://lmsys.org/blog/2024-07-01-routellm/), by diverting a subset of queries to smaller, more efficient models. It may cost just a few cents for a company to run a model and answer one customer’s request, but scale that by thousands of queries a day, and those costs quickly add up. As LLMs break into the mainstream, the need to balance quality and cost has become more important than ever.

“Routing gives you the ability to finesse price and performance,” said Kate Soule, a generative AI program director at IBM Research. “Save the big models for the high value, complicated tasks, and use the smaller cheaper models for easy tasks that don’t require hundreds of billions of parameters.”

Routers can also help companies pick the most cost-effective LLMs for their libraries. “I’ve got 140,000 models to choose from, where do I start?” said Soule.

## Selection by audition or prediction

A variety of routing methods has evolved over the last year. One kind, called nonpredictive routers, call on multiple LLMs at once, in a kind of simultaneous mass audition, and pick the model that generates the best response. Closely related “cascading” routers call on the smallest, cheapest, models first, until a quality answer surfaces. The audition approach brings immediate feedback, but the downside is that running [inference](https://research.ibm.com/blog/AI-inference-explained) multiple times adds delay and cost.

Predictive routers can save time and money by skipping the audition and formulating a decision based on information gathered before inference time. At IBM, Yurochkin and his colleagues decided to use the mountains of LLM evaluation data now freely available on the web. They trained a routing algorithm on benchmark data to pick out the strengths and weaknesses of each model in their library so that it could, for any given query, identify the model with the best predicted accuracy and cost.

Testing the router on Stanford's [HELM](https://crfm.stanford.edu/helm/) benchmark, they found that several 13-billion parameter models could outperform Meta’s 70-billion parameter Llama-2 model by several percentage points. They describe their results in [a new study](https://research.ibm.com/publications/large-language-model-routing-with-benchmark-datasets--1) at the inaugural [Conference on Language Modeling](https://colmweb.org/) (COLM) this month.

In recent tests on [RouterBench](https://arxiv.org/abs/2403.12031), a framework for testing LLM routers on a library of LLMs, researchers found that 11 LLMs connected to the IBM router outperformed each of the 11 models doing the tasks on their own. The IBM router even did slightly better than the top model overall, OpenAI’s GPT-4, while saving 5 cents per query. RouterBench was launched earlier this year by Martian, one of several startups that have sprung up in the last year to offer LLM-routing services.

LLMs today are tested on hundreds of tasks representative of things they’re asked to do in real life, from summarizing documents to solving math problems. In the end, HELM and most other benchmarks rank models by their average performance. Lost in translation is how well they do on tasks requiring specialized knowledge or skills.

The value of this untapped data wasn’t lost on IBM researchers, who had been looking for creative ways to stretch limited computing resources. “We realized we could use this data to send questions on math or history to the models that do that best,” said Yurochkin, who was the senior author of the router study.

Researchers also confirmed that training a router on benchmark data that more closely resembles the target task produces better results. "Knowing how an LLM did on a similar task in the past gives you a good idea of how it will do in the future," said Tal Shnitzer, the study's lead author who worked on the project as an MIT postdoc.

The routing work grew out of an [MIT-IBM Watson AI Lab](https://mitibmwatsonailab.mit.edu/) project looking at the economics of [generative AI](https://research.ibm.com/blog/what-is-generative-AI) and what tasks are likely to be automated by LLMs. To understand the economic value of automating a task, said Soule, you need to understand, first, what the costs are and what level of performance to expect. Routers give you the ability to predict the right cost-performance trade-off for a given task.

And that goes for latency, too. Because smaller models are faster than bigger models, said Soule, “you can define your latency target, and predict how much performance you can achieve for that latency cutoff.”

## What’s next

In earlier work, IBM researchers developed a [“frugal” routing method](https://research.ibm.com/publications/fusing-models-with-complementary-expertise--1) that calls on smaller, specialized LLMs, one at a time, until it finds the best model for the task. Their idea was that a collection of specialists could outperform much larger, expensive models if their router could quickly identify the right expert for each query.

Nonpredictive routers allow you to immediately verify whether the right model was chosen and to use this feedback to improve the router. The predictive router, by contrast, is faster, but it may not be as accurate, especially when queries that don’t look anything like the router’s training data arise.

The ideal router could end up being a combination of both methods, and the team is now diving into what that possibility might look like.