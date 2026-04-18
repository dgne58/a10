---
title: "LLM alignment techniques: 4 post-training approaches"
source: "https://snorkel.ai/blog/llm-alignment-techniques-4-post-training-approaches/"
author:
  - "[[Matthew Casey]]"
published: 2025-03-04
created: 2026-04-13
description: "Ensure your LLMs align with your values and goals using LLM alignment techniques. Learn how to mitigate risks and optimize performance."
tags:
  - "clippings"
---
Large language models (LLMs) have revolutionized how we interact with technology, enabling everything from AI-powered customer service to advanced research tools. However, as these models grow more powerful, they also become more unpredictable. Misaligned LLMs can generate harmful, unhelpful, or downright nonsensical responses—posing risks to both users and organizations. This is where **LLM alignment** techniques come in.

Alignment ensures that an AI model’s outputs align with specific values, principles, or goals, such as generating polite, safe, and accurate responses or adhering to a company’s ethical guidelines.

[LLM alignment](https://snorkel.ai/blog/what-is-large-language-model-llm-alignment/) techniques come in three major varieties:

1. **Prompt engineering** that explicitly tells the model how to behave.
2. **Supervised fine-tuning** with targeted and curated prompts and responses.
3. **Post-training preference optimization,** which takes feedback from both desirable and undesirable responses and adjusts the model accordingly.

This piece will focus on four post-training techniques worth knowing.

While alignment techniques vary, their shared goal is to shape LLM behavior to better meet human needs and expectations. Below, we’ll explore several popular methods for LLM alignment, breaking down how they work, their strengths, and their challenges.

![4 Ways to Align LLMs: RLHF, DPO, KTO, and ORPO](https://i.ytimg.com/vi/lBzw9ku86dg/hqdefault.jpg)

4 Ways to Align LLMs: RLHF, DPO, KTO, and ORPO

## Reinforcement Learning from Human Feedback (RLHF)

[Reinforcement Learning from Human Feedback](https://en.wikipedia.org/wiki/Reinforcement_learning_from_human_feedback) (RLHF) is one of the most widely used techniques for aligning [large language models](https://snorkel.ai/large-language-models/).

After pretraining a model on large datasets, RLHF adds a post-training phase. In this phase, human annotators review the model’s outputs, identifying which ones are preferred. These preferences are then used to train a **reward model**, which predicts the quality of new outputs. The reward model is usually smaller than the target LLM, but can be any size. Finally, the reward model guides the LLM’s behavior using reinforcement learning algorithms, such as [Proximal Policy Optimization](https://spinningup.openai.com/en/latest/algorithms/ppo.html) (PPO).

### How RLHF works (in simple terms)

1. Humans compare different responses from the model and either pick the better ones or rank responses from best to worst.
2. A reward model learns to predict these human preferences.
3. The LLM is fine-tuned to produce responses that the reward model rates as “good.”

### RLHF’s advantages

- **Proven success:** Used by OpenAI for ChatGPT, RLHF is a tried-and-true method for improving model alignment.
- **Handles complex goals:** By encoding nuanced human preferences into the reward model, RLHF can optimize for multiple criteria (e.g., helpfulness, safety, and politeness).

### RLHF’s disadvantages

- **Complex and expensive:** RLHF requires training a separate reward model and running reinforcement learning, which can be computationally intensive.
- **Risk of overfitting:** The model may over-optimize for specific reward metrics, leading to unintended behaviors.
- **Scaling challenges:** Reliance on human annotations makes RLHF difficult to scale across niche use cases.

## Direct Preference Optimization (DPO)

[Direct Preference Optimization](https://snorkel.ai/blog/how-snorkel-topped-the-alpacaeval-leaderboard-and-why-we-re-not-there-anymore/) (DPO) simplifies the alignment process by skipping the separate reward model altogether. Instead, DPO trains the LLM directly on human preference data. Researchers at Stanford demonstrated that LLMs inherently encode information that can approximate human preferences, which can be leveraged for alignment without explicitly training a separate reward model. By optimizing the likelihood of human-preferred responses, DPO fine-tunes the LLM without the added complexity of reinforcement learning.

### How DPO works (in simple terms)

1. Collect data showing which responses are “good” or “bad.”
2. Fine-tune the LLM directly on this data, increasing the likelihood of good responses and decreasing the likelihood of bad ones.

### DPO’s advantages

- **Simplicity:** DPO requires no separate reward model or reinforcement learning algorithm, making it easier to implement.
- **Stability:** DPO avoids some of the instability issues associated with reinforcement learning.
- **Efficiency:** Computationally cheaper than RLHF, DPO stands as a better option for smaller teams or less resource-intensive applications.

### DPO’s disadvantages

- **Limited flexibility:** While simpler, DPO may not handle highly complex alignment goals as well as RLHF.
- **Data quality dependency:** Success depends heavily on having high-quality preference data.

## Odds Ratio Preference Optimization (ORPO)

[Odds Ratio Preference Optimization (ORPO)](https://arxiv.org/abs/2403.07691) builds on ideas from RLHF and DPO but combines multiple steps into a single process. Instead of training a reward model and fine-tuning the LLM separately, ORPO uses a unified loss function to balance task-specific objectives with human preference alignment, streamlining the training process. This approach combines supervised fine-tuning with preference optimization in a mathematically integrated manner.

![Orpo—one of many LLM alignment techniques available to data scientists](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%200%200'%3E%3C/svg%3E)

Orpo—one of many LLM alignment techniques available to data scientists

## How ORPO works (in simple terms)

1. Use labeled preference data to calculate a combined loss for both task accuracy and preference alignment.
2. [Fine-tune the LLM](https://snorkel.ai/blog/how-to-fine-tune-large-language-models-for-enterprise-use-cases/) using this single loss function.

### ORPO’s advantages

- **Efficiency:** By merging two steps, ORPO reduces the overall training time and computational cost.
- **Improved performance:** Studies show that ORPO can outperform RLHF and DPO on some benchmarks.

### ORPO’s disadvantages

- **Implementation complexity:** Designing a combined loss function requires careful calibration to avoid one objective dominating the other.
- **Niche use:** ORPO is relatively new and less widely adopted, so best practices are still emerging.

## Kahneman-Tversky optimization (KTO)

[Kahneman-Tversky optimization (KTO)](https://arxiv.org/abs/2402.01306) is inspired by economics and focuses on how humans perceive utility. Much like the formulation for SFT, this can be done using prompt-response pairs that have been labeled as “good” or “bad,” optimizing the model to favor responses rated as good while being robust to label noise.

![KTO—one of many LLM alignment techniques available to data scientists.](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%200%200'%3E%3C/svg%3E)

KTO—one of many LLM alignment techniques available to data scientists.

### How KTO works (in simple terms):

1. Label responses as either good or bad.
2. Use these labels to train the LLM to favor good responses while ignoring occasional inconsistencies in the labels.

### KTO’s advantages:

- **Robust to noisy data:** KTO is less affected by imperfect or inconsistent labeling compared to other methods.
- **Simple labeling:** Requires only binary labels, which are easier to collect than detailed rankings or scores.

### KTO’s disadvantages:

- **Limited granularity:** Binary labels lack the nuance of other methods, which may limit performance for complex alignment goals.
- **Less established:** Like ORPO, KTO is relatively new and still under active research.

## Key Takeaways

- **Alignment is crucial** for ensuring that LLMs generate safe, helpful, and context-appropriate responses.
- **RLHF** holds a vital place in alignment pipelines but can be complex and costly.
- **DPO** simplifies the process and reduces computational overhead, making it ideal for resource-constrained teams.
- **ORPO and KTO** are emerging methods offering promising alternatives to traditional alignment techniques, with unique strengths in efficiency and robustness.
- Translating abstract human values, ethics, and context-specific goals into measurable metrics remains a significant challenge across all alignment methods.

When choosing an alignment method, organizations must weigh trade-offs like complexity, computational cost, and data quality requirements. Ultimately, the right approach depends on the specific use case, resources, and alignment goals.