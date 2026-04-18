---
title: "Reasoning model - Wikipedia"
source: "https://en.wikipedia.org/wiki/Reasoning_model?utm_source=chatgpt.com"
author:
  - "[[Contributors to Wikimedia projects]]"
published: 2025-01-26
created: 2026-04-13
description:
tags:
  - "clippings"
---
A **reasoning model**, also known as a **reasoning language model** (**RLM**) or **large reasoning model** (**LRM**), is a type of [large language model](https://en.wikipedia.org/wiki/Large_language_model "Large language model") (LLM) that has been specifically trained to solve complex tasks requiring multiple steps of logical.[^1] These models demonstrate superior performance on logic, mathematics, and programming tasks compared to standard LLMs. They possess the ability to [revisit and revise](https://en.wikipedia.org/wiki/Backtracking "Backtracking") earlier reasoning steps and utilize additional computation during inference as a method to [scale performance](https://en.wikipedia.org/wiki/Neural_scaling_law "Neural scaling law"), complementing traditional scaling approaches based on training data size, model parameters, and training compute.[^2]

## Overview

Unlike traditional language models that generate responses immediately, reasoning models allocate additional compute, or thinking, time before producing an answer to solve multi-step problems. [OpenAI](https://en.wikipedia.org/wiki/OpenAI "OpenAI") introduced this terminology in September 2024 when it released the [o1 series](https://en.wikipedia.org/wiki/OpenAI_o1 "OpenAI o1"), describing the models as designed to "spend more time thinking" before responding. The company framed o1 as a reset in model naming that targets complex tasks in science, coding, and mathematics, and it contrasted o1's performance with [GPT-4o](https://en.wikipedia.org/wiki/GPT-4o "GPT-4o") on benchmarks such as [AIME](https://en.wikipedia.org/wiki/American_Invitational_Mathematics_Examination "American Invitational Mathematics Examination") and [Codeforces](https://en.wikipedia.org/wiki/Codeforces "Codeforces"). Independent reporting the same week summarized the launch and highlighted OpenAI's claim that o1 automates [chain-of-thought](https://en.wikipedia.org/wiki/Chain-of-thought_prompting "Chain-of-thought prompting") style reasoning to achieve large gains on difficult exams.[^3] [^4] [^5]

In operation, reasoning models generate internal chains of intermediate steps, then select and refine a final answer. [OpenAI](https://en.wikipedia.org/wiki/OpenAI "OpenAI") reported that o1's accuracy improves as the model is given more [reinforcement learning](https://en.wikipedia.org/wiki/Reinforcement_learning "Reinforcement learning") during training and more test-time compute at inference. The company initially chose to hide raw chains and instead return a model-written summary, stating that it "decided not to show" the underlying thoughts so researchers could monitor them without exposing unaligned content to end users. Commercial deployments document separate "reasoning tokens" that meter hidden thinking and a control for "reasoning effort" that tunes how much compute the model uses. These features make the models slower than ordinary chat systems while enabling stronger performance on difficult problems.[^4] [^6]

## History

The research trajectory toward reasoning models combined advances in [supervision](https://en.wikipedia.org/wiki/Supervised_learning "Supervised learning"), [prompting](https://en.wikipedia.org/wiki/Prompt_engineering "Prompt engineering"), and [search-style inference](https://en.wikipedia.org/wiki/Search_tree "Search tree").

Early [alignment work](https://en.wikipedia.org/wiki/AI_alignment "AI alignment") on [reinforcement learning from human feedback](https://en.wikipedia.org/wiki/Reinforcement_learning_from_human_feedback "Reinforcement learning from human feedback") showed that models can be fine-tuned to follow instructions with "human feedback" and preference-based rewards.[^7] [^8] In 2022, [Google](https://en.wikipedia.org/wiki/Google "Google") Research scientists Jason Wei and Denny Zhou showed that [chain-of-thought](https://en.wikipedia.org/wiki/Chain-of-thought_prompting "Chain-of-thought prompting") prompting "significantly improves the ability" of large models on complex reasoning tasks.[^9]

$$
{\displaystyle {\text{Input}}\rightarrow \underbrace {{\text{Step}}_{1}\rightarrow {\text{Step}}_{2}\rightarrow \cdots \rightarrow {\text{Step}}_{n}} _{\text{Reasoning chain}}\rightarrow {\text{Answer}}}
$$

A companion result demonstrated that the simple instruction "Let's think step by step" can elicit zero-shot reasoning.[^10] Follow-up work introduced self-consistency decoding, which "boosts the performance" of chain-of-thought by sampling diverse solution paths and choosing the consensus, and tool-augmented methods such as *ReAct*, a portmanteau of Reason and Act, that prompt models to "generate both reasoning traces" and actions.[^11] [^12] Research then generalized chain-of-thought into search over multiple candidate plans. The [Tree-of-Thoughts](https://en.wikipedia.org/wiki/Prompt_engineering#Tree-of-thought "Prompt engineering") framework from [Princeton](https://en.wikipedia.org/wiki/Princeton_University "Princeton University") computer scientist Shunyu Yao proposes that models "perform deliberate decision making" by exploring and backtracking over a tree of intermediate thoughts.[^13]

[OpenAI](https://en.wikipedia.org/wiki/OpenAI "OpenAI") 's reported breakthrough focused on supervising reasoning processes rather than only outcomes, with Lightman et al.'s "Let's Verify Step by Step" reporting that rewarding each correct step "significantly outperforms outcome supervision" on challenging math problems and improves interpretability by aligning the chain-of-thought with human judgment.[^14] [^15] OpenAI's [o1](https://en.wikipedia.org/wiki/OpenAI_o1 "OpenAI o1") announcement ties these strands together with a large-scale [reinforcement learning](https://en.wikipedia.org/wiki/Reinforcement_learning "Reinforcement learning") algorithm that trains the model to refine its own chain of thought, and it reports that accuracy rises with more training compute and more time spent thinking at inference.[^4]

Together, these developments define the core of reasoning models. They use supervision signals that evaluate the quality of intermediate steps, they exploit inference-time exploration such as consensus or [tree search](https://en.wikipedia.org/wiki/Tree_search "Tree search"), and they expose controls for how much internal thinking compute to allocate. OpenAI's o1 family made this approach available at scale in September 2024 and popularized the label "reasoning model" for LLMs that deliberately think before they answer.[^3] [^6]

The development of reasoning models illustrates [Richard S. Sutton](https://en.wikipedia.org/wiki/Richard_S._Sutton "Richard S. Sutton") 's "bitter lesson" that scaling compute typically outperforms methods based on human-designed insights.[^16] This principle was demonstrated by researchers at the Generative AI Research Lab (GAIR), who initially attempted to replicate o1's capabilities using sophisticated methods including tree search and reinforcement learning in late 2024. Their findings, published in the "o1 Replication Journey" series, revealed that [knowledge distillation](https://en.wikipedia.org/wiki/Knowledge_distillation "Knowledge distillation"), a comparatively straightforward technique that trains a smaller model to mimic o1's outputs, produced unexpectedly strong performance. This outcome illustrated how direct scaling approaches can, at times, outperform more complex engineering solutions.[^17] [^18]

### Drawbacks

Reasoning models require significantly more computational resources during inference compared to non-reasoning models. Research on the [American Invitational Mathematics Examination](https://en.wikipedia.org/wiki/American_Invitational_Mathematics_Examination "American Invitational Mathematics Examination") (AIME) benchmark found that reasoning models were 10 to 74 times more expensive to operate than their non-reasoning counterparts.[^19] The extended inference time is attributed to the detailed, step-by-step reasoning outputs that these models generate, which are typically much longer than responses from standard [large language models](https://en.wikipedia.org/wiki/Large_language_model "Large language model") that provide direct answers without showing their reasoning process.

One researcher in early 2025 argued that these models may face potential additional denial-of-service concerns with "overthinking attacks." [^20]

### Releases

#### 2024

In September 2024, [OpenAI](https://en.wikipedia.org/wiki/OpenAI "OpenAI") released [o1-preview](https://en.wikipedia.org/wiki/OpenAI_o1#release "OpenAI o1"), a large language model with enhanced reasoning capabilities.[^21] The full version, [o1](https://en.wikipedia.org/wiki/OpenAI_o1 "OpenAI o1"), was released in December 2024. OpenAI initially shared preliminary results on its successor model, [o3](https://en.wikipedia.org/wiki/OpenAI_o3 "OpenAI o3"), in December 2024,[^22] [^23] [^24] with the full o3 model becoming available in 2025.[^25]

[Alibaba](https://en.wikipedia.org/wiki/Alibaba_Group "Alibaba Group") released reasoning versions of its [Qwen](https://en.wikipedia.org/wiki/Qwen "Qwen") large language models in November 2024.[^26] In December 2024, the company introduced QvQ-72B-Preview, an experimental visual reasoning model.[^27]

In December 2024, [Google](https://en.wikipedia.org/wiki/Google "Google") introduced [Deep Research](https://en.wikipedia.org/wiki/Gemini_Deep_Research "Gemini Deep Research") in [Gemini](https://en.wikipedia.org/wiki/Gemini_\(chatbot\) "Gemini (chatbot)"), a feature designed to conduct multi-step research tasks.[^28] [^29]

On December 16, 2024, researchers demonstrated that by scaling test-time compute, a relatively small [Llama](https://en.wikipedia.org/wiki/Llama_\(language_model\) "Llama (language model)") 3B model could outperform a much larger Llama 70B model on challenging reasoning tasks. This experiment suggested that improved inference strategies can unlock reasoning capabilities even in smaller models.[^30] [^31]

#### 2025

In January 2025, [DeepSeek](https://en.wikipedia.org/wiki/DeepSeek "DeepSeek") released [R1](https://en.wikipedia.org/wiki/DeepSeek_\(chatbot\) "DeepSeek (chatbot)"), a reasoning model that achieved performance comparable to OpenAI's o1 at significantly lower computational cost. The release demonstrated the effectiveness of [Group Relative Policy Optimization](https://en.wikipedia.org/wiki/Group_Relative_Policy_Optimization "Group Relative Policy Optimization") (GRPO), a reinforcement learning technique used to train the model.[^32] [^33]

On January 25, 2025, DeepSeek enhanced R1 with web search capabilities, allowing the model to retrieve information from the internet while performing reasoning tasks.[^34]

Research during this period further validated the effectiveness of [knowledge distillation](https://en.wikipedia.org/wiki/Knowledge_distillation "Knowledge distillation") for creating reasoning models. The s1-32B model achieved strong performance through budget forcing and scaling methods, reinforcing findings that simpler training approaches can be highly effective for reasoning capabilities.[^35] [^18]

On February 2, 2025, OpenAI released [Deep Research](https://en.wikipedia.org/wiki/ChatGPT_Deep_Research "ChatGPT Deep Research"), a feature powered by their [o3](https://en.wikipedia.org/wiki/OpenAI_o3 "OpenAI o3") model that enables users to conduct comprehensive research tasks.[^36] The system generates detailed reports by automatically gathering and synthesizing information from multiple web sources.[^36]

OpenAI called [GPT-4.5](https://en.wikipedia.org/wiki/GPT-4.5 "GPT-4.5") its "last non-chain-of-thought model",[^37] and implemented with [GPT-5](https://en.wikipedia.org/wiki/GPT-5 "GPT-5") a router model that selects a model based on the difficulty of the task.[^38]

#### 2026

In January 2026, [Moonshot AI](https://en.wikipedia.org/wiki/Moonshot_AI "Moonshot AI") released Kimi K2.5, an open-source 1 trillion parameter [MoE](https://en.wikipedia.org/wiki/Mixture_of_experts "Mixture of experts") model with 32 billion active parameters. It uses an “ [Agent](https://en.wikipedia.org/wiki/AI_agent "AI agent") Swarm” system that dynamically decomposes tasks into sub-agents for reasoning and execution, enabling more scalable multi-step problem solving than a single sequential reasoning chain.[^39]

## Training

Reasoning models follow the familiar large-scale pretraining used for frontier language models, then diverge in the post-training and optimization. [OpenAI](https://en.wikipedia.org/wiki/OpenAI "OpenAI") reports that [o1](https://en.wikipedia.org/wiki/OpenAI_o1 "OpenAI o1") is trained with a large-scale [reinforcement learning](https://en.wikipedia.org/wiki/Reinforcement_learning "Reinforcement learning") algorithm that teaches the model to use and refine a [chain of thought](https://en.wikipedia.org/wiki/Chain-of-thought_prompting "Chain-of-thought prompting") before answering. The company emphasizes two coupled levers, more reinforcement learning during training and more time spent thinking at inference, and it documents smooth gains as each increases. OpenAI also states that it decided not to show raw chains to end users and instead returns a model-written summary, a product choice tied to safety monitoring and competitive concerns.[^4]

A central ingredient is [process supervision](https://en.wikipedia.org/wiki/Process_supervision "Process supervision"), which rewards intermediate steps rather than only the final answer. OpenAI's study introduced a process reward model trained on step-level labels and found that process supervision significantly outperforms outcome-only supervision on challenging math problems. The project also released the PRM800K step-level feedback dataset and argued that process-level rewards improve interpretability because humans can check each step. These results supplied a practical recipe for supervising chains of thought that was later scaled into production training.[^15]

This training differs in important ways from traditional frontier models that do not target reasoning. Standard systems are pretrained on internet-scale corpora with a next-token prediction objective, then aligned through [instruction tuning](https://en.wikipedia.org/wiki/Instruction_tuning "Instruction tuning") and preference optimization. The canonical [InstructGPT](https://en.wikipedia.org/wiki/InstructGPT "InstructGPT") recipe first uses [supervised fine-tuning](https://en.wikipedia.org/wiki/Fine-tuning_\(deep_learning\) "Fine-tuning (deep learning)") on human demonstrations, then trains a reward model from pairwise preferences, and finally optimizes the policy with reinforcement learning, typically [PPO](https://en.wikipedia.org/wiki/Proximal_Policy_Optimization "Proximal Policy Optimization") with a [KL penalty](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence "Kullback–Leibler divergence").[^8] [^40] Variants such as [direct preference optimization](https://en.wikipedia.org/wiki/Direct_preference_optimization "Direct preference optimization") remove the explicit RL step and optimize the model directly on preference data, but the supervision target is still the final outcome judged by raters rather than the quality of internal steps.[^41] Technical reports for [GPT-4](https://en.wikipedia.org/wiki/GPT-4 "GPT-4") summarize this conventional pipeline as next-token pretraining followed by [RLHF](https://en.wikipedia.org/wiki/Reinforcement_learning_from_human_feedback "Reinforcement learning from human feedback") -style post-training to shape behavior.[^42]

In contrast, reasoning models are optimized to produce, critique, and revise multi-step chains during training. OpenAI states that reinforcement learning is applied to the chain itself, which teaches the model to recognize mistakes, break problems into simpler steps, and switch strategies when the current approach fails. OpenAI also documents that it hides chains at inference and returns an answer that summarizes useful ideas from the internal trace. These design choices reflect the model's training objective and its intended monitoring.[^4]

Zelikman et al. introduced STaR (Self-Taught Reasoner), which explored bootstrapping rationales by iteratively generating and filtering chains, then fine-tuning on those traces, and they reported gains over outcome-only fine-tuning. One variant of this method supplied additional mechanisms for producing training signals that speak to intermediate reasoning, not only final answers.[^43]

[DeepSeek](https://en.wikipedia.org/wiki/DeepSeek "DeepSeek") reported [R1](https://en.wikipedia.org/wiki/DeepSeek_\(chatbot\) "DeepSeek (chatbot)") and R1-Zero systems trained with pure RL to elicit long chains, self-verification, and reflection, arguing that explicit chain-level rewards can induce general reasoning behaviors. These results indicate that post-training focused on chain quality has become a distinct regime separate from outcome-only alignment.[^44]

### Supervised fine-tuning

A [large language model](https://en.wikipedia.org/wiki/Large_language_model "Large language model") (LLM) can be fine-tuned on datasets of reasoning tasks paired with step-by-step solution traces. The fine-tuned model learns to produce its own reasoning chains for new problems.[^45] [^46]

Since human-written traces are expensive to collect, researchers use *rejection sampling fine-tuning* (RFT) to build datasets automatically. This method generates multiple reasoning traces for each prompt, then filters out traces with incorrect final answers using a verifier.[^47]

### Reinforcement learning

A pretrained language model can be further trained with RL. In the RL formalism, a generative language model is a **policy** ${\displaystyle \pi }$. A task prompt is an environmental **state** ${\displaystyle x}$, and the model's response is an **action** ${\displaystyle y}$. The probability that the model responds ${\displaystyle x}$ with ${\displaystyle y}$ is ${\displaystyle \pi (y|x)}$.

Training a reasoning language model with RL means constructing a **reward model** ${\displaystyle r(x,y)}$ to guide the RL process. Intuitively, the reward says how good a response is for a prompt. For a reasoning task, the reward is high if the response solves the task and low if it does not.

A response ${\displaystyle y}$ may be broken-down into multiple steps, written ${\displaystyle y_{1},y_{2},\dots ,y_{n}}$.

Most recent systems use policy-gradient methods such as [Proximal Policy Optimization](https://en.wikipedia.org/wiki/Proximal_Policy_Optimization "Proximal Policy Optimization") (PPO) because PPO constrains each policy update with a clipped objective, which stabilises training for very large policies.[^48]

#### Outcome reward model

An outcome reward model, or outcome-supervised RM (ORM),[^45] gives the reward for a step ${\displaystyle r(x,y_{1},\dots ,y_{i})}$ based on the final answer: ${\displaystyle r(x,y_{1},\dots ,y_{i})=r(x,y_{n})}$. Such models are often called "verifiers".

For tasks with answers that are easy to verify, such as [math word problems](https://en.wikipedia.org/wiki/Word_problem_\(mathematics_education\) "Word problem (mathematics education)"), the outcome reward can be binary: 1 if the final answer is correct, 0 otherwise.[^45] If automatic verification is hard, humans can label answers as correct or not, and those labels can be used to finetune a base model that predicts the human label.[^46] For tasks like creative writing, where quality is not simply true or false, one can train a reward model on human [ranked preference](https://en.wikipedia.org/wiki/Ranking_\(statistics\) "Ranking (statistics)") data, as in [reinforcement learning from human feedback](https://en.wikipedia.org/wiki/Reinforcement_learning_from_human_feedback "Reinforcement learning from human feedback").[^19] A base model can also be fine-tuned to predict, from a partial thinking trace ${\displaystyle x,y_{1},\dots ,y_{m}}$, whether the final answer will be correct, and this prediction can serve as a binary reward.[^45]

The ORM is usually trained with [logistic regression](https://en.wikipedia.org/wiki/Logistic_regression "Logistic regression"), i.e. by minimizing [cross-entropy loss](https://en.wikipedia.org/wiki/Cross-entropy "Cross-entropy").[^49]

Given a PRM, an ORM can be constructed by multiplying the total process reward during the reasoning trace,[^19] by taking the minimum,[^49] or by other ways of aggregating process rewards. DeepSeek used a simple ORM to train the [R1 model](https://en.wikipedia.org/wiki/DeepSeek_\(chatbot\) "DeepSeek (chatbot)").[^33]

#### Process reward model

A process reward model, or process-supervised RM (PRM),[^45] gives the reward for a step ${\displaystyle r(x,y_{1},\dots ,y_{i})}$ based only on the steps so far: ${\displaystyle (x,y_{1},\dots ,y_{i})}$.

Given a partial thinking trace ${\displaystyle x,y_{1},\dots ,y_{m}}$, a human can judge whether the steps so far are correct, without looking at the final answer. This yields a binary reward. Because human labels are costly, a base model can be fine-tuned to predict them.[^45] The PRM is usually trained with [logistic regression](https://en.wikipedia.org/wiki/Logistic_regression "Logistic regression") on the human labels, i.e. by minimizing the [cross-entropy loss](https://en.wikipedia.org/wiki/Cross-entropy "Cross-entropy") between true and predicted labels.[^49]

As an example, a 2023 OpenAI paper collected 800K process labels for 75K thinking traces. A labeler saw a trace and marked each step as "positive" if it moved toward a solution, "neutral" if it was not wrong but did not help, and "negative" if it was a mistake. After the first "negative" label, the labeler stopped on that trace and moved to another. The authors argued that labeling up to the first error was enough to train a capable PRM, even though labeling later steps could give richer signals.[^19] [^50]

To avoid human labels, researchers have proposed methods to create PRM without human labels on the processes. Inspired by [Monte Carlo tree search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search "Monte Carlo tree search") (MCTS), the Math-Shepherd method samples multiple continuations until the end, starting at each reasoning step ${\displaystyle y_{i}}$, and set the reward at that step to be either ${\displaystyle {\frac {\#{\text{(correct answers)}}}{\#{\text{(total answers)}}}}}$ in the case of "soft estimation", or ${\displaystyle {\begin{cases}1&{\text{if one of the answers is correct}}\\0&{\text{else}}\end{cases}}}$ in the case of "hard estimation". This creates process rewards from an ORM, which is often easier or cheaper to construct. A PRM can then be trained on these labels.[^49] Some work has tried a fully MCTS approach.[^51]

One can also use an ORM to implicitly construct a PRM, similar to [direct preference optimization](https://en.wikipedia.org/wiki/Direct_preference_optimization "Direct preference optimization").[^52]

#### Guided sampling

A trained ORM can be used to pick the best response. The policy generates several responses, and the ORM selects the best one. This implements a simple form of [test-time compute scaling](https://en.wikipedia.org/wiki/Neural_scaling_law "Neural scaling law") ("best-of-N").[^46] [^53]

A trained PRM can guide reasoning by a greedy [tree search](https://en.wikipedia.org/wiki/Tree_traversal "Tree traversal"): the policy proposes several next steps, the PRM picks one, and the process repeats. This mirrors using an ORM to pick a whole response.[^54] [Beam search](https://en.wikipedia.org/wiki/Beam_search "Beam search") performs better than greedy search.

*Lookahead search* is another tree search method. The policy proposes several next steps, then makes a short rollout for each. If a solution is found during rollout, the search stops early. Otherwise, the PRM scores each rollout, and the step with the highest score is chosen.[^31]

*Self-consistency* can be combined with an ORM. The model generates multiple answers, and the answers are clustered so that each cluster has the same final answer. The ORM scores each answer, scores in each cluster are summed, and the answer from the highest-scoring cluster is returned.[^49]

## Benchmarks

Reasoning models generally achieve higher scores than non-reasoning models on many benchmarks, particularly on tasks requiring multi-step reasoning.[^55] [^56] [^57] [^58] [^59] [^60] [^61]

The [Humanity's Last Exam](https://en.wikipedia.org/wiki/Humanity%27s_Last_Exam "Humanity's Last Exam") (HLE) benchmark evaluates expert-level reasoning across mathematics, humanities, and natural sciences, revealing significant performance gaps between models. Current state-of-the-art reasoning models achieve relatively low scores on HLE, indicating substantial room for improvement. For example, the full reasoning model [o3](https://en.wikipedia.org/wiki/OpenAI_o3 "OpenAI o3") achieved 26.6%,[^36] while the lighter o3-mini-high (on text-only questions) achieved 13%.[^62]

On the [American Invitational Mathematics Examination](https://en.wikipedia.org/wiki/American_Invitational_Mathematics_Examination "American Invitational Mathematics Examination") (AIME), a challenging mathematics competition, non-reasoning models typically solve fewer than 30% of problems. In contrast, models employing reasoning methods achieve success rates between 50% and 80%.[^2] [^33] [^35] While [OpenAI's o1](https://en.wikipedia.org/wiki/OpenAI_o1 "OpenAI o1") maintained or slightly improved its accuracy from reported 2024 results to 2025 AIME results, o3-mini-high achieved 80% accuracy at significantly lower cost, approximately 12 times cheaper.[^63]

Some minority or independent benchmarks exclude reasoning models due to their longer response times and higher inference costs, including benchmarks for online complex event detection in cyber-physical systems, general inference-time compute evaluation, Verilog engineering tasks, and network security assessments.[^64] [^65] [^66] [^67]

## Models

<table><tbody><tr><th>Company</th><th>Model</th><th>Release Date</th></tr><tr><td rowspan="6"><a href="https://en.wikipedia.org/wiki/OpenAI">OpenAI</a></td><td><a href="https://en.wikipedia.org/wiki/GPT-5">GPT-5</a> (o3.1)</td><td>August 2025</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/Products_and_applications_of_OpenAI#GPT-OSS">GPT-OSS</a></td><td>August 2025 <sup><a href="#fn:68">68</a></sup></td></tr><tr><td><a href="https://en.wikipedia.org/wiki/OpenAI_o3">o3 and o4-mini</a></td><td>April 2025</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/OpenAI_o3">o3-mini</a></td><td>January 2025</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/OpenAI_o1">o1</a></td><td>December 2024</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/OpenAI_o1">o1-preview</a></td><td>September 2024</td></tr><tr><td rowspan="6"><a href="https://en.wikipedia.org/wiki/Google_Gemini">Google Gemini</a></td><td><a href="https://en.wikipedia.org/wiki/Gemini_(language_model)">3 Flash</a></td><td>December 2025</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/Gemini_(language_model)">3 Pro</a></td><td>November 2025</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/Gemini_(language_model)">2.5 Computer Use</a></td><td>October 2025</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/Gemini_(language_model)">2.5 Flash</a></td><td>April 2025</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/Gemini_(language_model)">2.5 Pro</a></td><td>March 2025</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/Gemini_(language_model)">2.0 Flash Thinking</a></td><td>December 2024</td></tr><tr><td rowspan="5"><a href="https://en.wikipedia.org/wiki/DeepSeek">DeepSeek</a></td><td>V3.2-Exp</td><td>September 2025</td></tr><tr><td>V3.1</td><td>August 2025</td></tr><tr><td>R1-0528</td><td>May 2025</td></tr><tr><td>V3-0324</td><td>March 2025</td></tr><tr><td>R1 and R1-Lite-Preview</td><td>January 2025</td></tr><tr><td rowspan="3"><a href="https://en.wikipedia.org/wiki/Alibaba_Group">Alibaba Group</a></td><td><a href="https://en.wikipedia.org/wiki/Qwen">QwQ-32B</a></td><td>March 2025</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/Qwen">QvQ-72B-Preview</a></td><td>December 2024</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/Qwen">QwQ-32B-Preview</a></td><td>November 2024</td></tr><tr><td rowspan="4"><a href="https://en.wikipedia.org/wiki/Anthropic">Anthropic</a></td><td><a href="https://en.wikipedia.org/wiki/Claude_(language_model)">Claude Opus 4.5</a></td><td>November 2025</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/Claude_(language_model)">Claude Haiku 4.5</a></td><td>October 2025</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/Claude_(language_model)">Claude Sonnet 4.5</a></td><td>September 2025</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/Claude_(language_model)">Claude Sonnet 3.7</a></td><td>February 2025</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/Mistral_AI">Mistral AI</a></td><td>Magistral Medium / Small</td><td>June 2025</td></tr><tr><td rowspan="2"><a href="https://en.wikipedia.org/wiki/XAI_(company)">xAI</a></td><td><a href="https://en.wikipedia.org/wiki/Grok_(chatbot)">Grok 4</a></td><td>July 2025</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/Grok_(chatbot)">Grok 3</a></td><td>February 2025</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/Hugging_Face">Hugging Face</a></td><td>OlympicCoder-7B & 32B</td><td>February 2025</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/NVIDIA">NVIDIA</a></td><td>Llama <a href="https://en.wikipedia.org/wiki/Nemotron">Nemotron</a></td><td>March 2025</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/Tencent">Tencent</a></td><td>Hunyuan T1</td><td>March 2025</td></tr><tr><td rowspan="2"><a href="https://en.wikipedia.org/wiki/Moonshot_AI">Moonshot AI</a></td><td><a href="https://en.wikipedia.org/wiki/Kimi_(chatbot)">Kimi K2 Thinking</a></td><td>November 2025</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/Kimi_(chatbot)">Kimi K2.5</a></td><td>January 2026</td></tr></tbody></table>

[^1]: Besta, Maciej; Barth, Julia; Schreiber, Eric; Kubicek, Ales; Catarino, Afonso; Gerstenberger, Robert; Nyczyk, Piotr; Iff, Patrick; Li, Yueling (2025-01-23). "Reasoning Language Models: A Blueprint". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2501.11223](https://arxiv.org/abs/2501.11223) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^2]: ["Learning to reason with LLMs"](https://openai.com/index/learning-to-reason-with-llms/). *OpenAI*. 2024-09-12. Retrieved 2025-07-26.

[^3]: [*Introducing OpenAI o1-preview*](https://openai.com/index/introducing-openai-o1-preview/), OpenAI, 2024-09-12

[^4]: [*Learning to reason with LLMs*](https://openai.com/index/learning-to-reason-with-llms/), OpenAI, 2024-09-12

[^5]: [*OpenAI launches new series of AI models with reasoning abilities*](https://www.reuters.com/technology/artificial-intelligence/openai-launches-new-series-ai-models-solve-hard-problems-2024-09-12/), Reuters, 2024-09-12

[^6]: [*Azure OpenAI reasoning models*](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/reasoning), Microsoft Learn, 2025-10-11

[^7]: Christiano, Paul; Leike, Jan; Brown, Tom B.; Martic, Miljan; Legg, Shane; Amodei, Dario (2017). "Deep reinforcement learning from human preferences". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[1706.03741](https://arxiv.org/abs/1706.03741) \[[stat.ML](https://arxiv.org/archive/stat.ML)\].

[^8]: Ouyang, Long; Wu, Jeff; Jiang, Xu; Dinan, Emily; Bansal, Prafulla; Wainwright, Sam; Xu, Chong; Schulman, John (2022). "Training language models to follow instructions with human feedback". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2203.02155](https://arxiv.org/abs/2203.02155) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^9]: Wei, Jason; Wang, Xuezhi; Schuurmans, Dale; Saxton, David; Prenger, Ryan; Ren, Shuohui; Liu, Yang; Zhou, Denny (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2201.11903](https://arxiv.org/abs/2201.11903) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^10]: Kojima, Takeshi; Gu, Shixiang; Reid, Machel; Matsuo, Yutaka; Iwasawa, Yusuke (2022). "Large Language Models are Zero-Shot Reasoners". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2205.11916](https://arxiv.org/abs/2205.11916) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^11]: Wang, Xuezhi; Wei, Jason; Schuurmans, Dale; Le, Quoc; Chi, Ed; Zhou, Denny (2022). "Self-Consistency Improves Chain of Thought Reasoning in Language Models". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2203.11171](https://arxiv.org/abs/2203.11171) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^12]: Yao, Shunyu; Zhao, Jeffrey; Yu, Dian; Du, Nan; Shafran, Izhak; Narasimhan, Karthik; Cao, Yuan (2022). "ReAct: Synergizing Reasoning and Acting in Language Models". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2210.03629](https://arxiv.org/abs/2210.03629) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^13]: Yao, Shunyu; Yu, Dian; Zhao, Jeffrey; Shafran, Izhak; Griffiths, Thomas L.; Cao, Yuan; Narasimhan, Karthik (2023). "Tree of Thoughts: Deliberate Problem Solving with Large Language Models". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2305.10601](https://arxiv.org/abs/2305.10601) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^14]: Lightman, Hunter; Kosaraju, Vineet; Burda, Yura; Edwards, Harri; Baker, Bowen; Lee, Teddy; Leike, Jan; Schulman, John; Sutskever, Ilya (2023). "Let's Verify Step by Step". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2305.20050](https://arxiv.org/abs/2305.20050) \[[cs.LG](https://arxiv.org/archive/cs.LG)\].

[^15]: [*Improving mathematical reasoning with process supervision*](https://openai.com/index/improving-mathematical-reasoning-with-process-supervision/), OpenAI, 2023-05-31

[^16]: Sutton, Richard S. ["The Bitter Lesson"](http://www.incompleteideas.net/IncIdeas/BitterLesson.html). *Incomplete Ideas*. Retrieved 2025-02-27.

[^17]: Huang, Zhen; Zou, Haoyang; Li, Xuefeng; Liu, Yixiu; Zheng, Yuxiang; Chern, Ethan; Xia, Shijie; Qin, Yiwei; Yuan, Weizhe (2024-11-25). "O1 Replication Journey — Part 2: Surpassing O1-preview through Simple Distillation, Big Progress or Bitter Lesson?". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2411.16489](https://arxiv.org/abs/2411.16489) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^18]: Zeff, Maxwell (2025-02-05). ["Researchers created an open rival to OpenAI's o1 'reasoning' model for under $50"](https://techcrunch.com/2025/02/05/researchers-created-an-open-rival-to-openais-o1-reasoning-model-for-under-50/). *TechCrunch*. Retrieved 2025-07-26.

[^19]: Lightman, Hunter; Kosaraju, Vineet; Burda, Yura; Edwards, Harri; Baker, Bowen; Lee, Teddy; Leike, Jan; Schulman, John; Sutskever, Ilya (2024). ["Let's Verify Step by Step"](https://openreview.net/forum?id=dKDGgN0eTg). *International Conference on Learning Representations (ICLR 2024)*. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2305.20050](https://arxiv.org/abs/2305.20050). Retrieved 2025-07-26.

[^21]: Edwards, Benj (2024-09-12). ["OpenAI's new "reasoning" AI models are here: o1-preview and o1-mini"](https://arstechnica.com/information-technology/2024/09/openais-new-reasoning-ai-models-are-here-o1-preview-and-o1-mini/). *Ars Technica*. Retrieved 2025-02-06.

[^22]: ["OpenAI o1 System Card"](https://cdn.openai.com/o1-system-card.pdf) (PDF). *OpenAI*. 2024-12-05. Retrieved 2025-07-26.

[^23]: Robison, Kylie (2024-12-05). ["OpenAI launches ChatGPT Pro, a $200/month plan with unlimited access to o1, GPT-4o, and more"](https://www.theverge.com/2024/12/5/24314147/openai-reasoning-model-o1-strawberry-chatgpt-pro-new-tier). *The Verge*. Retrieved 2025-07-26.

[^24]: Singh, Jaspreet (2024-12-20). ["OpenAI unveils 'o3' model, touting advances in reasoning"](https://www.reuters.com/technology/artificial-intelligence/openai-unveils-o3-model-touting-advances-reasoning-2024-12-20/). *Reuters*. Retrieved 2025-07-26.

[^25]: ["Introducing OpenAI o3 and o4-mini"](https://openai.com/index/introducing-o3-and-o4-mini/). *OpenAI*. 2025-04-16. Retrieved 2025-07-26.

[^26]: Team, Qwen (2024-11-28). ["QwQ-32B-Preview: Reflect Deeply on the Boundaries of the Unknown"](https://qwenlm.github.io/blog/qwq-32b-preview/). *Qwen (Alibaba Cloud)*. Retrieved 2025-07-26.

[^27]: Team, Qwen (2024-12-25). ["QVQ: To See the World with Wisdom"](https://qwenlm.github.io/blog/qvq-72b-preview/). *Qwen*. Alibaba Cloud. Retrieved 2025-07-26.

[^28]: ["Try Deep Research and our new experimental model in Gemini, your AI assistant"](https://blog.google/products/gemini/google-gemini-deep-research/). *Google*. 2024-12-11. Retrieved 2025-02-05.

[^29]: Roth, Emma (2024-12-11). ["Google built an AI tool that can do research for you"](https://www.theverge.com/2024/12/11/24318217/google-gemini-advanced-deep-research-launch). *The Verge*. Retrieved 2025-07-26.

[^30]: ["Scaling test-time compute"](https://huggingface.co/blog/h4-scaling-test-time-compute). *Hugging Face*. 2024-12-16. Retrieved 2025-07-26.

[^31]: Snell, Charlie; Lee, Jaehoon; Xu, Kelvin; Kumar, Aviral (2025). ["Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters"](https://openreview.net/forum?id=t4s3hJY9dH). *International Conference on Learning Representations (ICLR 2025)*. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2408.03314](https://arxiv.org/abs/2408.03314). Retrieved 2025-07-26.

[^32]: Orland, Kyle (2025-01-28). ["How does DeepSeek R1 really fare against OpenAI's best reasoning models?"](https://arstechnica.com/ai/2025/01/how-does-deepseek-r1-really-fare-against-openais-best-reasoning-models/). *Ars Technica*. Retrieved 2025-02-06.

[^33]: DeepSeek-AI; Guo, Daya; Yang, Dejian; Zhang, Haowei; Song, Junxiao; Zhang, Ruoyu; Xu, Runxin; Zhu, Qihao; Ma, Shirong (2025-01-22). "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2501.12948](https://arxiv.org/abs/2501.12948) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^34]: [DeepSeek 支持"深度思考+联网检索"能力](http://tech.people.com.cn/n1/2025/0129/c1007-40386565.html) \[DeepSeek adds a search feature supporting simultaneous deep thinking and web search\]. *People's Daily Online* (in Chinese). 2025-01-29. Retrieved 2025-07-26.

[^35]: Muennighoff, Niklas; Yang, Zitong; Shi, Weijia; Li, Xiang Lisa; Fei-Fei, Li; [Hajishirzi, Hannaneh](https://en.wikipedia.org/wiki/Hanna_Hajishirzi "Hanna Hajishirzi"); Zettlemoyer, Luke; [Liang, Percy](https://en.wikipedia.org/wiki/Percy_Liang "Percy Liang"); Candès, Emmanuel (2025-02-03). "s1: Simple test-time scaling". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2501.19393](https://arxiv.org/abs/2501.19393) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^36]: ["Introducing deep research"](https://openai.com/index/introducing-deep-research/). *OpenAI*. 2025-02-02. Retrieved 2025-02-05.

[^37]: Fried, Ina (2025-02-28). ["OpenAI's GPT-4.5 release underscores AI's next challenge"](https://www.axios.com/2025/02/28/openai-gpt-ai-reasoning). *Axios*. Retrieved 2026-01-20.

[^38]: Goldman, Sharon. ["GPT-5's model router ignited a user backlash against OpenAI—but it might be the future of AI"](https://fortune.com/2025/08/12/openai-gpt-5-model-router-backlash-ai-future/). *Fortune*. Retrieved 2026-01-20.

[^39]: ["Kimi K2.5 Tech Blog: Visual Agentic Intelligence"](https://www.kimi.com/blog/kimi-k2-5). *www.kimi.com*. Retrieved 2026-02-25.

[^40]: Ziegler, Daniel M.; Stiennon, Nisan; Wu, Jeffrey; Brown, Tom B.; Radford, Alec; Amodei, Dario; Christiano, Paul; Irving, Geoffrey (2019). "Fine-Tuning Language Models from Human Preferences". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[1909.08593](https://arxiv.org/abs/1909.08593) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^41]: Rafailov, Rafael; Sharma, Kushal; Mitchell, Eric; Manning, Christopher D.; Ermon, Stefano; Finn, Chelsea (2023). "Direct Preference Optimization: Your Language Model is Secretly a Reward Model". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2305.18290](https://arxiv.org/abs/2305.18290) \[[cs.LG](https://arxiv.org/archive/cs.LG)\].

[^42]: Achiam, Josh; Adler, Steven; Agarwal, Sandhini (2023). "GPT-4 Technical Report". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2303.08774](https://arxiv.org/abs/2303.08774) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^43]: Zelikman, Eric; Wu, Yuhuai; Mu, Jesse; Goodman, Noah D. (2022). "STaR: Bootstrapping Reasoning With Reasoning". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2203.14465](https://arxiv.org/abs/2203.14465) \[[cs.LG](https://arxiv.org/archive/cs.LG)\].

[^44]: Guo, Dan (2025). "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2501.12948](https://arxiv.org/abs/2501.12948) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^45]: Uesato, Jonathan; Kushman, Nate; Kumar, Ramana; Song, Francis; Siegel, Noah; Wang, Lisa; Creswell, Antonia; Irving, Geoffrey; Higgins, Irina (2022-11-25). "Solving math word problems with process- and outcome-based feedback". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2211.14275](https://arxiv.org/abs/2211.14275) \[[cs.LG](https://arxiv.org/archive/cs.LG)\].

[^46]: Cobbe, Karl; Kosaraju, Vineet; Bavarian, Mohammad; Chen, Mark; Jun, Heewoo; Kaiser, Lukasz; Plappert, Matthias; Tworek, Jerry; Hilton, Jacob (2021-11-18). "Training Verifiers to Solve Math Word Problems". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2110.14168](https://arxiv.org/abs/2110.14168) \[[cs.LG](https://arxiv.org/archive/cs.LG)\].

[^47]: Yuan, Zheng; Yuan, Hongyi; Li, Chengpeng; Dong, Guanting; Lu, Keming; Tan, Chuanqi; Zhou, Chang; Zhou, Jingren (2023-09-13). "Scaling Relationship on Learning Mathematical Reasoning with Large Language Models". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2308.01825](https://arxiv.org/abs/2308.01825) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^48]: ["Aligning language models to follow instructions"](https://openai.com/blog/instruction-following/). *OpenAI Blog*. 2022-01-27. Retrieved 2025-05-04.

[^49]: Wang, Peiyi; Li, Lei; Shao, Zhihong; Xu, Runxin; Dai, Damai; Li, Yifei; Chen, Deli; Wu, Yu; Sui, Zhifang (August 2024). Ku, Lun-Wei; Martins, Andre; Srikumar, Vivek (eds.). "Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations". *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*. Bangkok, Thailand: Association for Computational Linguistics: 9426–9439. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2312.08935](https://arxiv.org/abs/2312.08935). [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.18653/v1/2024.acl-long.510](https://doi.org/10.18653%2Fv1%2F2024.acl-long.510).

[^50]: ["prm800k"](https://github.com/openai/prm800k). *GitHub*. OpenAI. 2025-01-27. Retrieved 2025-01-27.

[^51]: Chen, Guoxin; Liao, Minpeng; Li, Chengxi; Fan, Kai (2024-09-27). "AlphaMath Almost Zero: Process Supervision without Process". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2405.03553](https://arxiv.org/abs/2405.03553) \[[cs.LG](https://arxiv.org/archive/cs.LG)\].

[^52]: Yuan, Lifan; Li, Wendi; Chen, Huayu; Cui, Ganqu; Ding, Ning; Zhang, Kaiyan; Zhou, Bowen; [Liu, Zhiyuan](https://en.wikipedia.org/wiki/ModelBest "ModelBest"); Peng, Hao (2024-12-02). "Free Process Rewards without Process Labels". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2412.01981](https://arxiv.org/abs/2412.01981) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^53]: Zhang, Di; Wu, Jianbo; Lei, Jingdi; Che, Tong; Li, Jiatong; Xie, Tong; Huang, Xiaoshui; Zhang, Shufei; Pavone, Marco (2024-11-21). "LLaMA-Berry: Pairwise Optimization for O1-like Olympiad-Level Mathematical Reasoning". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2410.02884](https://arxiv.org/abs/2410.02884) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^54]: Ma, Qianli; Zhou, Haotian; Liu, Tingkai; Yuan, Jianbo; Liu, Pengfei; You, Yang; Yang, Hongxia (2023-10-16). "Let's reward step by step: Step-Level reward model as the Navigators for Reasoning". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2310.10080](https://arxiv.org/abs/2310.10080) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^55]: Wei, Jason; Wang, Xuezhi; Schuurmans, Dale; Bosma, Maarten; Ichter, Brian; Xia, Fei; Chi, Ed; Le, Quoc; Zhou, Denny (2023-01-10). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2201.11903](https://arxiv.org/abs/2201.11903) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^56]: Wang, Xuezhi; Wei, Jason; Schuurmans, Dale; Le, Quoc; Chi, Ed; Narang, Sharan; Chowdhery, Aakanksha; Zhou, Denny (2023-03-07). "Self-Consistency Improves Chain of Thought Reasoning in Language Models". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2203.11171](https://arxiv.org/abs/2203.11171) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^57]: Yao, Shunyu; Yu, Dian; Zhao, Jeffrey; Shafran, Izhak; Griffiths, Thomas L.; Cao, Yuan; Narasimhan, Karthik (2023). "Tree of Thoughts: Deliberate Problem Solving with Large Language Models". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2305.10601](https://arxiv.org/abs/2305.10601) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^58]: Cui, Dong-Xu; Long, Shi-Yu; Tang, Yi-Xuan; Zhao, Yue; Li, Qiao (2025-08-25). ["Can Reasoning Power Significantly Improve the Knowledge of Large Language Models for Chemistry?─Based on Conversations with LLMs"](https://doi.org/10.1021/acs.jcim.5c01265). *Journal of Chemical Information and Modeling*. **65** (18) acs.jcim.5c01265. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1021/acs.jcim.5c01265](https://doi.org/10.1021%2Facs.jcim.5c01265). [ISSN](https://en.wikipedia.org/wiki/ISSN_\(identifier\) "ISSN (identifier)") [1549-9596](https://search.worldcat.org/issn/1549-9596). [PMID](https://en.wikipedia.org/wiki/PMID_\(identifier\) "PMID (identifier)") [40854079](https://pubmed.ncbi.nlm.nih.gov/40854079).

[^59]: Qwen; Yang, An; Yang, Baosong; Zhang, Beichen; Hui, Binyuan; Zheng, Bo; Yu, Bowen; Li, Chengyuan; Liu, Dayiheng (2024). "Qwen2.5 Technical Report". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2412.15115](https://arxiv.org/abs/2412.15115) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^60]: Comanici, Gheorghe; Bieber, Eric; Schaekermann, Mike; Pasupat, Ice; Sachdeva, Noveen; Dhillon, Inderjit; Blistein, Marcel; Ram, Ori; Zhang, Dan (2025-07-22). "Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next Generation Agentic Capabilities". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2507.06261](https://arxiv.org/abs/2507.06261) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^61]: Mirza, Adrian; Alampara, Nawaf; Kunchapu, Sreekanth; Ríos-García, Martiño; Emoekabu, Benedict; Krishnan, Aswanth; Gupta, Tanya; Schilling-Wilhelmi, Mara; Okereke, Macjonathan; Aneesh, Anagha; Asgari, Mehrdad; Eberhardt, Juliane; Elahi, Amir Mohammad; Elbeheiry, Hani M.; Gil, María Victoria (July 2025). ["A framework for evaluating the chemical knowledge and reasoning abilities of large language models against the expertise of chemists"](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12226332). *Nature Chemistry*. **17** (7): 1027–1034. [Bibcode](https://en.wikipedia.org/wiki/Bibcode_\(identifier\) "Bibcode (identifier)"):[2025NatCh..17.1027M](https://ui.adsabs.harvard.edu/abs/2025NatCh..17.1027M). [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1038/s41557-025-01815-x](https://doi.org/10.1038%2Fs41557-025-01815-x). [ISSN](https://en.wikipedia.org/wiki/ISSN_\(identifier\) "ISSN (identifier)") [1755-4349](https://search.worldcat.org/issn/1755-4349). [PMC](https://en.wikipedia.org/wiki/PMC_\(identifier\) "PMC (identifier)") [12226332](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12226332). [PMID](https://en.wikipedia.org/wiki/PMID_\(identifier\) "PMID (identifier)") [40394186](https://pubmed.ncbi.nlm.nih.gov/40394186).

[^62]: ["Humanity's Last Exam leaderboard"](https://agi.safe.ai/benchmarks/hle). *Safe.ai*. Center for AI Safety. Retrieved 2025-07-26.

[^63]: ["OpenAI o3-mini"](https://openai.com/index/openai-o3-mini/). *OpenAI*. 2025-01-31. Retrieved 2025-02-09.

[^64]: Huang, Yuting; Zois, Christos; Wang, Yue; Zhang, Yue; Mavromatis, Christos; Zeng, Jiachen; Yin, Shihao; Voulkidis, Antonios; Shepard, Daniel (2025). "Toward Foundation Models for Online Complex Event Detection in CPS-IoT: A Case Study". *Proceedings of the 2nd International Workshop on Foundation Models for Cyber-Physical Systems & Internet of Things*. ACM. pp. 1–6. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2503.12282](https://arxiv.org/abs/2503.12282). [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1145/3722565.3727198](https://doi.org/10.1145%2F3722565.3727198). [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [979-8-4007-1608-9](https://en.wikipedia.org/wiki/Special:BookSources/979-8-4007-1608-9 "Special:BookSources/979-8-4007-1608-9"). Although we did not evaluate o1 and o3 models... their high cost and inference time make them impractical for online CED, which requires frequent, low-latency API requests.

[^65]: Hu, Zihao; Wang, Yuqing; Sun, Rui; Lu, Haoran; Gong, Qian; Wang, Jinshuai; Gong, Yunlong; Huang, Yiming; He, Peng (2025-02-13). "Inference-Time Compute: More Faithful? A Research Note". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2502.09673](https://arxiv.org/abs/2502.09673) \[[cs.CL](https://arxiv.org/archive/cs.CL)\]. we were unable to evaluate O1 and R1 …

[^66]: Chen, Guoliang; Zhu, Zhiyao; Meng, Qinxiang; Liang, Weilin; Ji, Zijie; Liu, Jiangning; Zeng, Jie (2025-03-07). "RealBench: Evaluating LLMs as Verilog Engineers". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2503.04914](https://arxiv.org/abs/2503.04914) \[[cs.AI](https://arxiv.org/archive/cs.AI)\]. For O1-preview, we sample only once due to high cost.

[^67]: Gupta, Arpit; Schapira, Michael; Gill, Phillipa; Seetharaman, Srinivasan (2025-01-30). "On the Feasibility of Using LLMs to Execute Multistage Network Attacks". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2501.16466](https://arxiv.org/abs/2501.16466) \[[cs.CR](https://arxiv.org/archive/cs.CR)\]. We were unable to evaluate o1 … the public API has a safeguard that prevents o1 from executing attacks.

[^68]: Heath, Alex (2025-08-05). ["OpenAI releases a free GPT model that can run on your laptop"](https://www.theverge.com/openai/718785/openai-gpt-oss-open-model-release). *The Verge*. Retrieved 2026-03-07.