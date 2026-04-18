---
title: "Unlocking Efficiency in Large Language Model Inference: A Comprehensive Survey of Speculative Decoding"
source: "https://arxiv.org/html/2401.07851v3"
author:
published:
created: 2026-04-15
description:
tags:
  - "clippings"
---
Heming Xia <sup>1</sup>, Zhe Yang <sup>2</sup>, Qingxiu Dong <sup>2</sup>, Peiyi Wang <sup>2</sup>,  
Yongqi Li <sup>1</sup>, Tao Ge <sup>3</sup>, Tianyu Liu <sup>4</sup>, Wenjie Li <sup>1</sup>, Zhifang Sui <sup>2</sup>  
<sup>1</sup> Department of Computing, The Hong Kong Polytechnic University  
<sup>2</sup> National Key Laboratory for Multimedia Information Processing, Peking University  
<sup>3</sup> Microsoft Research Asia  <sup>4</sup> Alibaba Group  
{he-ming.xia}@connect.polyu.hk; {yz\_young}@pku.edu.cn

###### Abstract

To mitigate the high inference latency stemming from autoregressive decoding in Large Language Models (LLMs), Speculative Decoding has emerged as a novel decoding paradigm for LLM inference. In each decoding step, this method first drafts several future tokens efficiently and then verifies them in parallel. Unlike autoregressive decoding, Speculative Decoding facilitates the simultaneous decoding of multiple tokens per step, thereby accelerating inference. This paper presents a comprehensive overview and analysis of this promising decoding paradigm. We begin by providing a formal definition and formulation of Speculative Decoding. Then, we organize in-depth discussions on its key facets, such as drafter selection and verification strategies. Furthermore, we present a comparative analysis of leading methods under third-party testing environments. We aim for this work to serve as a catalyst for further research on Speculative Decoding, ultimately contributing to more efficient LLM inference.<sup>1</sup>

Unlocking Efficiency in Large Language Model Inference:  
A Comprehensive Survey of Speculative Decoding

  

Heming Xia <sup>1</sup>, Zhe Yang <sup>2</sup>, Qingxiu Dong <sup>2</sup>, Peiyi Wang <sup>2</sup>, Yongqi Li <sup>1</sup>, Tao Ge <sup>3</sup>, Tianyu Liu <sup>4</sup>, Wenjie Li <sup>1</sup>, Zhifang Sui <sup>2</sup> <sup>1</sup> Department of Computing, The Hong Kong Polytechnic University <sup>2</sup> National Key Laboratory for Multimedia Information Processing, Peking University <sup>3</sup> Microsoft Research Asia  <sup>4</sup> Alibaba Group {he-ming.xia}@connect.polyu.hk; {yz\_young}@pku.edu.cn

  

## 1 Introduction

Large Language Models (LLMs) have achieved remarkable proficiency in a range of downstream tasks [^35] [^46] [^47] [^7] [^20]. They are progressively evolving as the cornerstone of comprehensive API interfaces (e.g., ChatGPT <sup>2</sup>), offering human life services and guidance through real-time human-machine interactions. However, the inference latency of these sizable models has emerged as a substantial obstacle restricting their broader applications. This latency primarily arises from the token-by-token generation necessitated by autoregressive decoding, resulting in an escalation of the inference latency with both the length of the generated sequence and the model’s scale.

![Refer to caption](https://arxiv.org/html/2401.07851v3/x1.png)

Figure 1: In contrast to autoregressive decoding ( left ) that generates sequentially, Speculative Decoding ( right ) first efficiently drafts multiple tokens and then verifies them in parallel using the target LLM. Drafted tokens after the bifurcation position ( e.g., ) will be discarded to guarantee the generation quality.

To accelerate LLM inference, an innovative inference paradigm, Speculative Decoding has been introduced [^42] [^49] [^28] [^5]. As shown in Figure 1, in each decoding step, Speculative Decoding first efficiently drafts multiple tokens as speculation of future decoding steps of the target LLM and then utilizes the LLM to verify all drafted tokens in parallel. Only those tokens that meet the LLM’s verification criterion are accepted as final outputs to guarantee generation quality.

![Refer to caption](https://arxiv.org/html/2401.07851v3/x2.png)

Figure 2: Timeline illustrating the evolution of Speculative Decoding. After 2022, Speculative Decoding was formally introduced as a general decoding paradigm to accelerate LLM inference and garnered widespread attention.

Speculative Decoding is founded upon two key observations about LLM inference: 1) many easy tokens can be predicted with less computational overhead (e.g., using a smaller model), and 2) LLM inference is highly memory bandwidth bound [^36] [^39] with the main latency bottleneck arising from memory reads/writes of LLM parameters rather than arithmetic computations. Drawing on these observations, Speculative Decoding adapts the concept of [^2] [^18] to focus LLMs’ efforts on the validation of pre-drafted tokens, substantially diminishing the need for frequent memory operations of LLM parameters, thereby improving inference efficiency.

While Speculative Decoding shows promise, it raises several critical questions that warrant further investigation. For instance, how to design an optimal drafter to strike a balance between speculation accuracy and drafting efficiency [^49] [^60] [^30]. Additionally, it is essential to assess whether the verification criterion can maintain both generation parallelism and output quality [^32] [^4]. Furthermore, since existing methods are evaluated under disparate testing conditions, a unified benchmark is needed to facilitate realistic speedup expectations within the research community.

Amid the rapid expansion of research in Speculative Decoding, this work makes the first attempt to present a survey of this field, aiming to raise awareness among academics about the latest advancements. We provide a systematic categorization of current research and an in-depth analysis of relevant studies. Moreover, we introduce Spec-Bench, a comprehensive benchmark to assess Speculative Decoding methods in diverse application scenarios. Our contributions can be summarized as follows:

1. First survey: To our knowledge, we are the first to present a comprehensive survey on Speculative Decoding;
2. Formal definition: We furnish a formal definition and formulation of Speculative Decoding, laying the groundwork for future research.
3. New taxonomy: We provide a systematic taxonomy for Speculative Decoding, offering an organized categorization of existing work.
4. Spec-Bench: We introduce Spec-Bench, an extensive benchmark designed for assessing Speculative Decoding, enabling a comparative evaluation of leading methodologies.

We hope that this work can serve as an essential guide for newcomers and motivate future research.

## 2 Overview

This paper offers a comprehensive survey of Speculative Decoding. We commence by introducing the early stages of Speculative Decoding research (§3), illustrated by a timeline of its evolution (as shown in Figure 2). This is followed by a formal definition and formulation of Speculative Decoding (§4). Then, we delve into a detailed discussion of leading techniques, including the selection of draft models (§5), verification strategies (§6), and alignment between the drafter and the target LLM (§7). Moreover, we introduce Spec-Bench, an extensive evaluation benchmark designed for assessing the acceleration effect of Speculative Decoding (§8).

## 3 Evolution of Speculative Decoding

This section discusses the motivation behind Speculative Decoding (§3.1) and then provides a detailed introduction to early attempts in this field (§3.2).

### 3.1 Motivation

The widespread adoption of LLMs has established autoregressive decoding as the de facto standard to LLM inference [^8] [^35] [^21]. However, autoregressive decoding is limited by its inference latency, which primarily stems from the memory-bound computation of LLMs [^36] [^39]. Specifically, the main latency bottleneck of each decoding step is not due to computational operations but arises from the necessity to transfer all LLM parameters from High-Bandwidth Memory (HBM) to the on-chip cache of modern accelerators like GPUs. This process, which generates only one token per step, leads to the underutilization of these accelerators and results in inefficiencies.

### 3.2 Pioneering Draft-then-Verify Efforts

To mitigate the above issue, an intuitive way involves leveraging idle computational resources to enhance parallelism in LLM inference. To this end, [^42] introduced Blockwise Decoding, an approach that incorporates extra feedforward neural (FFN) heads atop the Transformer decoder, enabling the simultaneous drafting of multiple tokens per step. These tokens are then verified by the original LLM in parallel, ensuring that the outputs align with those of the original LLM. As a pioneering work proposing the Draft-then-Verify paradigm, Blockwise Decoding effectively reduces the number of required LLM calls by increasing generation parallelism, thereby accelerating inference.

To further unleash the potential of this paradigm, [^49] introduced Speculative Decoding (SpecDec), which utilizes an independent drafter, notably a specialized Non-Autoregressive Transformer, to perform the drafting task both accurately and efficiently. Moreover, this method presented an innovative strategy that relaxes the rigid verification criterion, thereby increasing the acceptance rate of drafted tokens. Impressively, SpecDec achieves around 5 $\times$ speedup over autoregressive decoding with comparable quality, underscoring the substantial potential of Speculative Decoding.

Algorithm 1 Autoregressive Decoding

Language model $\mathcal{M}_{q}$, input sequence $x_{1},\dots,x_{t}$, and target sequence length $T$;

initialize $n\leftarrow t$

while $n<T$ do

Set $q_{n+1}\leftarrow\mathcal{M}_{q}\left(x\mid x_{<n+1}\right)$

Sample $x_{n+1}\sim q_{n+1}$

 $n\leftarrow n+1$

end while

Following SpecDec, [^28] and [^5] made concurrent contributions by proposing Speculative Sampling, expanding this paradigm to encompass the lossless acceleration of various sampling methods. These approaches employed smaller LMs from the same series (e.g., T5-small) to speed up the inference of their larger counterparts (e.g., T5-XXL). Unlike previous work, these off-the-shelf small LMs do not require additional training, enabling the rapid adoption of Speculative Decoding in LLM acceleration. This advancement has elevated Speculative Decoding to the forefront of LLM efficiency research, attracting widespread interest within the NLP community.

To sum up, these pioneering efforts in Speculative Decoding have gradually solidified the Draft-then-Verify paradigm, showcasing its promising potential in LLM acceleration. We provide a detailed categorization and discussion of these studies and subsequent research in the following sections.

## 4 Formulation and Definition

In this section, we first provide a concise overview of standard autoregressive decoding (§4.1). Then, we offer an in-depth exposition of Speculative Decoding (§4.2), which encompasses a formal definition, a comprehensive description of the methodology, and a detailed elaboration of the algorithm.

Algorithm 2 Speculative Decoding

Target language model $\mathcal{M}_{q}$, draft model $\mathcal{M}_{p}$, input sequence $x_{1},\dots,x_{t}$, block size $K$, target sequence length $T$, drafting strategy Draft, verification criterion Verify, and correction strategy Correct;

initialize $n\leftarrow t$

while $n<T$ do

// Drafting: obtain distributions from $\mathcal{M}_{p}$ efficiently

Set $p_{1},\dots,p_{K}\leftarrow\textsc{Draft}\left(x_{\leq n},\mathcal{M}_{p}\right)$

// Drafting: sample $K$ drafted tokens

Sample $\widetilde{x}_{i}\sim p_{i},i=1,\dots,K$

// Verification: compute $K+1$ distributions in parallel

Set $q_{i}\leftarrow\mathcal{M}_{q}\left(x\mid x_{\leq n},\widetilde{x}_{<i}\right)%
,i=1,\dots,K+1$

// Verification: verify each drafted token

for $i=1:K$ do

if $\textsc{Verify}\left(\widetilde{x}_{i},p_{i},q_{i}\right)$ then

Set ${x}_{n+i}\leftarrow\widetilde{x}_{i}$ and $n\leftarrow n+1$

else

 ${x}_{n+i}\leftarrow\textsc{Correct}\left(p_{i},q_{i}\right)$

and Exit for loop.

end if

end for

If all drafted tokens are accepted, sample next token ${x}_{n+1}\sim q_{K+1}$ and set $n\leftarrow n+1$.

end while

forked edges, for tree= grow=east, reversed=true, anchor=base west, parent anchor=east, child anchor=west, base=center, font=, rectangle, draw=hidden-draw, rounded corners, align=left, text centered, minimum width=4em, edge+=darkgray, line width=1pt, s sep=3pt, inner xsep=2pt, inner ysep=3pt, line width=0.8pt, ver/.style=rotate=90, child anchor=north, parent anchor=south, anchor=center,, where level=1text width=7em,font=,, where level=2text width=8em,font=, where level=3text width=6em,font=,, where level=4text width=6em,font=,, \[ Speculative Decoding, ver \[ Drafting (§5), ver \[ Independent  
Drafting (§5.1) \[ Fine-tuned  
Drafter \[ SpecDec [^49], BiLD [^24], SpecInfer [^32],  
Online Speculative [^31], DistillSpec [^60], leaf, text width=35em \] \] \[ Tuning-free  
Drafter \[ Speculative Decoding [^28], StagedSpec [^40],  
SpS [^5], SpecTr [^45], REST [^17],  
CS. Drafting [^6], MCSD [^52], leaf, text width=35em \] \] \] \[ Self-Drafting (§5.2) \[ FFN Heads \[ Blockwise [^42], Medusa [^4], EAGLE [^30], leaf, text width=35em \] \] \[ Early Exiting \[ PPD [^53], Self-Speculative [^56],  
SPEED [^19], leaf, text width=35em \] \] \[ Mask-Predict \[ Parallel Decoding [^37], Lookahead Decoding [^15],  
PaSS [^33], leaf, text width=35em \] \] \] \] \[ Verification (§6), ver \[ Greedy  
Decoding (§6.1) \[ Lossless \[ Blockwise [^42], SpecDec [^49], Parallel Decoding  
[^37], PPD [^53], SPEED [^19],  
Self-Speculative [^56], Lookahead Decoding [^15], leaf, text width=35em \] \] \[ Approximate \[ Blockwise [^42], SpecDec [^49], BiLD [^24], leaf, text width=35em \] \] \] \[ Speculative  
Sampling (§6.2) \[ Lossless \[ Speculative Decoding [^28], DistillSpec [^60],  
Online Speculative [^31], SpS [^5], CS. Drafting  
[^6], PaSS [^33], MCSD [^52], leaf, text width=35em \] \] \[ Approximate \[ Speculative Decoding [^28], DistillSpec [^60], leaf, text width=35em \] \] \] \[ Token Tree  
Verification (§6.3) \[ SpecInfer [^32], StagedSpec [^40], SpecTr [^45],  
REST [^17], Medusa [^4], EAGLE [^30], leaf, text width=42.7em \] \] \] \]

Figure 3: Taxonomy of Speculative Decoding.

### 4.1 Autoregressive Decoding

Transformer-based LLMs typically make generations in an autoregressive manner. Given an input sequence $x_{1},\dots,x_{t}$, an autoregressive language model $\mathcal{M}_{q}$ generates the next token according to:

$$
x_{t+1}\sim q_{t+1}=\mathcal{M}_{q}\left(x\mid x_{<t+1}\right),
$$

where $q$ is the conditional probability distribution calculated by $\mathcal{M}_{q}$ and $x_{t+1}$ denotes the next token sampled from $q_{t+1}$. We illustrate a detailed process in Algorithm 1.

As discussed in Section 3, while the standard autoregressive decoding offers desirable generation quality, it is bounded by memory bandwidth, resulting in low utilization of modern accelerators. In this process, each memory-bound LLM call (i.e., an LLM forward step) produces merely a single token for the entire sequence, making the whole generation inefficient and time-consuming.

### 4.2 Speculative Decoding

Following [^49], [^28], and [^5], we here provide a formal definition of Speculative Decoding:

> Speculative Decoding is a Draft-then-Verify decoding paradigm in which, at each decoding step, it first efficiently drafts multiple future tokens and then verifies all these tokens in parallel using the target LLM to speed up inference.

We formulate a detailed Speculative Decoding process in Algorithm 2. Subsequently, we delve into the two fundamental substeps integral to this paradigm – drafting and verification:

#### Drafting

At each decoding step, Speculative Decoding first efficiently drafts multiple future tokens, as a speculation of the target LLM’s output. Formally, given an input sequence $x_{1},\dots,x_{t}$ and the target LLM $\mathcal{M}_{q}$, this paradigm employs an efficient draft model $\mathcal{M}_{p}$ (e.g., a smaller LM) to decode the next $K$ drafted tokens:

$$
\displaystyle p_{1},\dots,p_{K}
$$
 
$$
\displaystyle=\textsc{Draft}\left(x_{\leq t},\mathcal{M}_{p}\right),
$$
$$
\displaystyle\widetilde{x}_{i}
$$
 
$$
\displaystyle\sim p_{i},\quad i=1,\dots,K,
$$

where $\textsc{Draft}(\cdot)$ denotes various drafting strategies that we will discuss in Section 5, $p$ is the conditional probability distribution calculated by $\mathcal{M}_{p}$, and $\widetilde{x}_{i}$ denotes the drafted token sampled from $p_{i}$.

#### Verification

Subsequently, these drafted tokens are verified by the target LLM $\mathcal{M}_{q}$ in parallel. Formally, given the input sequence $x_{1},\dots,x_{t}$ and the draft $\widetilde{x}_{1},\dots,\widetilde{x}_{K}$, Speculative Decoding utilizes $\mathcal{M}_{q}$ to compute $K+1$ probability distributions simultaneously:

$$
\displaystyle q_{i}=\mathcal{M}_{q}\left(x\mid x_{\leq t},\widetilde{x}_{<i}%
\right),i=1,\dots,K+1.
$$

| Methods | $\textsc{Draft}\left(x_{\leq t},\mathcal{M}_{p}\right)$ | Drafter Type |
| --- | --- | --- |
| Parallel Drafting | $p_{1},\dots,p_{K}=\mathcal{M}_{p}\left(x\mid x_{\leq t}\right)$ | [^42] [^4] |
| Autoregressive Drafting | $p_{i}=\mathcal{M}_{p}\left(x\mid x_{\leq t},\widetilde{x}_{<i}\right),i=1,% \dots,K$ | [^28] [^5] |

Table 1: Summary of formulations for various drafting strategies in Speculative Decoding. We categorize these methods into two distinct groups based on their formulations: parallel drafting and autoregressive drafting.

Then, each drafted token $\widetilde{x}_{i}$ is verified by a specific criterion $\textsc{Verify}\left(\widetilde{x}_{i},p_{i},q_{i}\right)$. Only those tokens that meet the criterion are selected as final outputs, ensuring quality consistent with the target LLM’s standards. Otherwise, the first drafted token $\widetilde{x}_{c}$ that fails the verification will be corrected by the strategy $\textsc{Correct}\left(p_{c},q_{c}\right)$. All drafted tokens after position $c$ will be discarded, to guarantee the high quality of the final outputs. If all tokens pass verification, an additional token $x_{t+K+1}$ will be sampled from $q_{K+1}$ as Eq. (1).

The drafting and verification substeps will be iterated until the termination condition is met, i.e., the \[EOS\] token is decoded or the sentence reaches the maximal length.

Notably, the acceleration effect of Speculative Decoding primarily hinges on the acceptance rate of drafted tokens at each step. This rate is influenced by several factors, including the draft quality, verification criteria, and the behavior alignment between the drafter and the target LLM. Additionally, the intrinsic efficiency of the drafter itself also contributes to the overall speedup. In subsequent sections, we will delve into these pivotal components of Speculative Decoding, as depicted in Figure 3, to systematically categorize recent research trends within this promising paradigm.

## 5 Drafting

As a vital component of Speculative Decoding, the drafting process has a crucial impact on the speedup of the paradigm. The impact is determined by two key factors: the speculation accuracy of the drafter $\mathcal{M}_{p}$, measured by the average number of accepted tokens per step, and the drafting latency [^42] [^49]. How to trade off high speculation accuracy and low drafting latency presents a major challenge in this process. In this section, we classify various drafting strategies into two categories: independent drafting (§5.1) and self-drafting (§5.2), and summarize their formulations $\textsc{Draft}\left(x_{\leq t},\mathcal{M}_{p}\right)$ in Table 1.

### 5.1 Independent Drafting

To strike a balance between speculation accuracy and efficiency, SpecDec [^49] first proposed utilizing an independent model for drafting. Specifically, it employed a specialized Non-Autoregressive Transformer that drafts multiple tokens simultaneously per step. This model has a deep-shallow encoder-decoder architecture to run efficiently. Despite its strengths, SpecDec requires training a draft model from scratch, which demands an increased computational budget.

Considering the available models in existing LLM series (e.g., OPT [^57] and LLaMA [^46] [^47]), a more straightforward and efficient approach is directly employing a small LM from the same series as the drafter to accelerate the inference of its larger counterparts [^28] [^5] [^40] [^45] [^6]. For instance, [^28] utilized T5-small as the drafter, to accelerate the inference of T5-XXL. These off-the-shelf small LMs do not require additional training or any modification on model architectures, facilitating the quick adoption of Speculative Decoding. Moreover, since models in the same series share tokenizers, pretraining corpora, and similar training processes, they inherently have an alignment in prediction behaviors.

| Methods | $\textsc{Verify}\left(\widetilde{x}_{i},p_{i},q_{i}\right)$ | $\textsc{Correct}\left(p_{c},q_{c}\right)$ | Representative Work |
| --- | --- | --- | --- |
| Greedy Decoding | $\widetilde{x}_{i}=\arg\max q_{i}$ | ${x}_{t+c}\leftarrow\arg\max q_{c}$ | [^42] |
| Speculative Sampling | $r<\min\left(1,\frac{q_{i}(\widetilde{x}_{i})}{p_{i}(\widetilde{x}_{i})}\right)% ,r\sim U\left[0,1\right]$ | $x_{t+c}\sim\operatorname{norm}(\max\left(0,q_{c}-p_{c}\right))$ | [^28] |

Table 2: Summary of formulations for various verification strategies in Speculative Decoding.

### 5.2 Self-Drafting

While leveraging an external draft model offers considerable advantages, this approach necessitates extra effort to either train or identify a draft model that closely aligns with the target LLM. This challenge is intensified when no smaller counterparts of the LLM are available, e.g., LLaMA-7B [^46] [^47]. Furthermore, integrating two distinct models within a single system introduces additional computational complexity, particularly in distributed settings [^4].

To address the above issues, numerous studies have suggested leveraging the target LLM itself for efficient drafting [^42] [^37] [^19] [^4] [^15] [^12]. Particularly, Blockwise Decoding [^42] and Medusa [^4] incorporated FFN heads atop the Transformer decoder, enabling the parallel token generation per step. Compared with external drafters, these lightweight heads reduce extra computational overhead and are friendly to distributed inference. Another line of research has explored the potential of early exiting and layer skipping within the target LLM for drafting [^53] [^56] [^19]. For instance, [^53] introduced additional subprocesses that exit early during the current decoding step, thereby initiating the drafting of future tokens in advance. Similarly, Self-Speculative [^56] proposed to adaptively skip several intermediate layers during inference to draft efficiently.

In contrast to prior work that focused on extending model architectures or altering the inference process, [^37] introduced a simple drafting strategy that directly appends multiple \[PAD\] tokens to the end of the input prompt to enable parallel generation. However, this approach deviates from LLMs’ autoregressive pretraining pattern, leading to suboptimal drafting quality. To tackle this, [^15] proposed transforming low-quality drafts into multiple n-grams to improve the speculation accuracy; [^33] introduced multiple learnable \[LA\] tokens and finetuned these token embeddings on a small training dataset to enhance the parallel decoding performance.

## 6 Verification

In each decoding step, the drafted tokens are verified in parallel to ensure the outputs align with the target LLM. This process also determines the number of tokens accepted per step, a vital factor impacting the speedup. This section summarizes various verification criteria $\textsc{Verify}\left(\widetilde{x}_{i},p_{i},q_{i}\right)$ (as shown in Table 2), encompassing those supporting greedy decoding (§6.1) and speculative sampling (§6.2) in LLM inference. Besides, we introduce token tree verification (§6.3), an effective strategy to increase the token acceptance rate.

<table><thead><tr><th colspan="2" rowspan="2">Methods</th><th colspan="3">Drafting</th><th colspan="3">Verification</th><th rowspan="2">Target LLM</th><th rowspan="2">Speedup (reported)</th></tr><tr><th>Approach</th><th>Alignment</th><th>Tuning-free</th><th>Greedy</th><th>Sampling</th><th>Token Tree</th></tr></thead><tbody><tr><td rowspan="7">Independent-D</td><td>SpecDec <sup><a href="#fn:49">49</a></sup></td><td>Non-Auto LM</td><td>Seq-KD</td><td>✗</td><td>✓</td><td>✗</td><td>✗</td><td>Transformer-base (65M)</td><td><math><semantics><mrow><mn>3.9</mn> <mo>×</mo> <mo>∼</mo> <mn>5.1</mn> <mo>×</mo></mrow> <annotation>3.9\times\sim 5.1\times</annotation> <annotation>3.9 × ∼ 5.1 ×</annotation></semantics></math></td></tr><tr><td>SpS <sup><a href="#fn:5">5</a></sup></td><td>Small LM</td><td>-</td><td>✓</td><td>✓</td><td>✓</td><td>✗</td><td>Chinchilla (70B)</td><td><math><semantics><mrow><mn>1.9</mn> <mo>×</mo> <mo>∼</mo> <mn>2.5</mn> <mo>×</mo></mrow> <annotation>1.9\times\sim 2.5\times</annotation> <annotation>1.9 × ∼ 2.5 ×</annotation></semantics></math></td></tr><tr><td>SpecInfer <sup><a href="#fn:32">32</a></sup></td><td>Boost-tuned LMs</td><td>Col-BT</td><td>✗</td><td>✓</td><td>✓</td><td>✓</td><td>LLaMA (30B-65B)</td><td><math><semantics><mrow><mn>2.0</mn> <mo>×</mo> <mo>∼</mo> <mn>2.4</mn> <mo>×</mo></mrow> <annotation>2.0\times\sim 2.4\times</annotation> <annotation>2.0 × ∼ 2.4 ×</annotation></semantics></math></td></tr><tr><td>DistillSpec <sup><a href="#fn:60">60</a></sup></td><td>Small LM</td><td>KD</td><td>✗</td><td>✓</td><td>✓</td><td>✗</td><td>T5-XL (3B)</td><td>-</td></tr><tr><td>Online Speculative <sup><a href="#fn:31">31</a></sup></td><td>Small LM</td><td>Online-KD</td><td>✗</td><td>✓</td><td>✓</td><td>✗</td><td>Vicuna (7B)</td><td>-</td></tr><tr><td>CS. Drafting <sup><a href="#fn:6">6</a></sup></td><td>Cascaded LMs</td><td>-</td><td>✓</td><td>✓</td><td>✓</td><td>✗</td><td>FLAN-T5-xxl (11B)</td><td>-</td></tr><tr><td>REST <sup><a href="#fn:17">17</a></sup></td><td>Context Retrieval</td><td>-</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td><td>Vicuna (7B-13B)</td><td><math><semantics><mrow><mn>1.6</mn> <mo>×</mo> <mo>∼</mo> <mn>1.8</mn> <mo>×</mo></mrow> <annotation>1.6\times\sim 1.8\times</annotation> <annotation>1.6 × ∼ 1.8 ×</annotation></semantics></math></td></tr><tr><td rowspan="7">Self-D</td><td>Blockwise Decoding <sup><a href="#fn:42">42</a></sup></td><td>FFN Heads</td><td>Seq-KD</td><td>✗</td><td>✓</td><td>✗</td><td>✗</td><td>Transformer-big (213M)</td><td><math><semantics><mrow><mn>1.7</mn> <mo>×</mo> <mo>∼</mo> <mn>3.0</mn> <mo>×</mo></mrow> <annotation>1.7\times\sim 3.0\times</annotation> <annotation>1.7 × ∼ 3.0 ×</annotation></semantics></math></td></tr><tr><td>Medusa <sup><a href="#fn:4">4</a></sup></td><td>FFN Heads</td><td>Seq-KD</td><td>✗</td><td>✓</td><td>✓</td><td>✓</td><td>Vicuna (7B-13B)</td><td><math><semantics><mrow><mn>2.2</mn> <mo>×</mo> <mo>∼</mo> <mn>2.3</mn> <mo>×</mo></mrow> <annotation>2.2\times\sim 2.3\times</annotation> <annotation>2.2 × ∼ 2.3 ×</annotation></semantics></math></td></tr><tr><td>PPD <sup><a href="#fn:53">53</a></sup></td><td>Early Exiting</td><td>-</td><td>✗</td><td>✓</td><td>✗</td><td>✗</td><td>Vicuna (13B)</td><td><math><semantics><mrow><mn>1.1</mn> <mo>×</mo> <mo>∼</mo> <mn>1.5</mn> <mo>×</mo></mrow> <annotation>1.1\times\sim 1.5\times</annotation> <annotation>1.1 × ∼ 1.5 ×</annotation></semantics></math></td></tr><tr><td>Self-Speculative <sup><a href="#fn:56">56</a></sup></td><td>Layer Skipping</td><td>-</td><td>✓</td><td>✓</td><td>✓</td><td>✗</td><td>LLaMA-2 (13B-70B)</td><td><math><semantics><mrow><mn>1.4</mn> <mo>×</mo> <mo>∼</mo> <mn>1.7</mn> <mo>×</mo></mrow> <annotation>1.4\times\sim 1.7\times</annotation> <annotation>1.4 × ∼ 1.7 ×</annotation></semantics></math></td></tr><tr><td>Parallel Decoding <sup><a href="#fn:37">37</a></sup></td><td>Mask-Predict</td><td>-</td><td>✓</td><td>✓</td><td>✗</td><td>✗</td><td>MBart50 (610M)</td><td><math><semantics><mrow><mn>1.0</mn> <mo>×</mo> <mo>∼</mo> <mn>1.1</mn> <mo>×</mo></mrow> <annotation>1.0\times\sim 1.1\times</annotation> <annotation>1.0 × ∼ 1.1 ×</annotation></semantics></math></td></tr><tr><td>Lookahead Decoding <sup><a href="#fn:15">15</a></sup></td><td>Mask-P & N-grams</td><td>-</td><td>✓</td><td>✓</td><td>✗</td><td>✗</td><td>LLaMA-2 (7B-70B)</td><td><math><semantics><mrow><mn>1.5</mn> <mo>×</mo> <mo>∼</mo> <mn>2.3</mn> <mo>×</mo></mrow> <annotation>1.5\times\sim 2.3\times</annotation> <annotation>1.5 × ∼ 2.3 ×</annotation></semantics></math></td></tr><tr><td>EAGLE <sup><a href="#fn:30">30</a></sup></td><td>Auto-regression Head</td><td>KD</td><td>✗</td><td>✓</td><td>✓</td><td>✓</td><td>Vicuna (7B-33B)</td><td><math><semantics><mrow><mn>2.9</mn> <mo>×</mo> <mo>∼</mo> <mn>3.1</mn> <mo>×</mo></mrow> <annotation>2.9\times\sim 3.1\times</annotation> <annotation>2.9 × ∼ 3.1 ×</annotation></semantics></math></td></tr></tbody></table>

Table 3: Summary of Speculative Decoding methods. “Independent-D” and “Self-D” denote independent drafting and self-drafting, respectively. “Greedy”, “Sampling”, and “Token Tree” denote whether the method supports greedy decoding, speculative sampling, and token tree verification, respectively. We list the most representative target LLMs for each method and the speedups in the original paper (if reported), which is obtained with a batch size of 1.

### 6.1 Greedy Decoding

Early attempts at Speculative Decoding focused on the verification criterion supporting greedy decoding, which guarantees that the outputs are exactly the same as the greedy decoding results of the target LLM [^41] [^44] [^49]. Formally, given the input sequence $x_{1},\dots,x_{t}$, the drafted tokens $\widetilde{x}_{1},\dots,\widetilde{x}_{K}$, and the computed probability distributions $p_{1},\dots,p_{K}$, $q_{1},\dots,q_{K}$ as obtained from Eq. (2) and (3), respectively, the verification criterion on the $i_{th}$ drafted token is formulated as

$$
\widetilde{x}_{i}=\arg\max q_{i},
$$

where $i=1,\dots,K$. The first position $c$ that the drafted token $\widetilde{x}_{c}$ fails the verification denotes the bifurcation position. The output token at this position ${x}_{t+c}$ will be adjusted by the correction strategy, which simply replaces the drafted token with the LLM’s top-1 prediction:

$$
{x}_{t+c}\leftarrow\arg\max q_{c}.
$$

The verification criterion of greedy decoding is straightforward and clear. Thus, multiple subsequent studies have adopted this criterion to demonstrate the efficacy of their methodologies [^37] [^53] [^19] [^56] [^15]. However, the strict matching requirement of this criterion often results in the rejection of high-quality drafted tokens, simply because they differ from the top-1 predictions of the target LLM, thereby constraining the speedup of the paradigm.

To tackle this problem, multiple studies have proposed various approximate verification criteria [^42] [^49] [^24]. Compared with the lossless criterion, these methods slightly relax the matching requirement to trust the drafts more, leading to higher acceptance of drafted tokens. For instance, SpecDec [^49] only requires the drafted tokens to fall in top-k candidates of the target LLM; BiLD [^24] proposed a rollback criterion that only rejects drafted tokens when the number of consecutive mismatch tokens exceeds a fixed threshold.

### 6.2 Speculative Sampling

Following [^41], subsequent work extended Speculative Decoding to support various sampling methods [^28] [^5], accelerating the target LLM’s inference without changing its output distribution. Formally, given the initial sequence $x_{1},\dots,x_{t}$, the drafted tokens $\widetilde{x}_{1},\dots,\widetilde{x}_{K}$ and the computed distributions $p_{1},\dots,p_{K}$, $q_{1},\dots,q_{K}$, the verification criterion on the $i_{th}$ drafted token is

$$
\displaystyle r<\min\left(1,\frac{q_{i}(\widetilde{x}_{i})}{p_{i}(\widetilde{x%
}_{i})}\right),r\sim U\left[0,1\right],
$$

where $r$ denotes a random number drawn from a uniform distribution $U\left[0,1\right]$; $q_{i}(\widetilde{x}_{i})$ and $p_{i}(\widetilde{x}_{i})$ are the probability of $\widetilde{x}_{i}$ according to $\mathcal{M}_{q}$ and $\mathcal{M}_{p}$, respectively; and $i=1,\dots,K$. In other words, this criterion accepts the token $\widetilde{x}_{i}$ if $q_{i}(\widetilde{x}_{i})\geq p_{i}(\widetilde{x}_{i})$, and in case $q_{i}(\widetilde{x}_{i})<p_{i}(\widetilde{x}_{i})$ it rejects the token with probability $1-\frac{q_{i}(\widetilde{x}_{i})}{p_{i}(\widetilde{x}_{i})}$. The correction strategy resamples the output token at the bifurcation position $c$ from an adjusted distribution:

$$
x_{t+c}\sim\operatorname{norm}(\max\left(0,q_{c}-p_{c}\right)).
$$

[^28] and [^5] have theoretically proved that this criterion maintains identical output distributions to the target LLM. Thus, it has been widely adopted in subsequent research [^31] [^60] [^33] [^6]. In addition to the strict requirement, some work has also explored approximate strategies to improve the token acceptance rate [^28] [^60]. For instance, [^28] proposed multiplying $p_{i}(\widetilde{x}_{i})$ in Eq. (6) by a lenience parameter $l\in[0,1]$ to slightly relax the criterion.

### 6.3 Token Tree Verification

Contrary to prior verification strategies that focused on a single draft sequence, SpecInfer [^32] proposed token tree verification, an effective strategy enabling the target LLM to verify multiple draft sequences in parallel. As illustrated in Figure 4, this method first merges multiple candidate draft sequences into a token tree by sharing prefixes. It then utilizes a specially designed tree attention mask to facilitate the LLM verifying the whole structure in parallel. Recent research has explored various approaches to obtain these candidate draft sequences [^32] [^4] [^17] [^30]. For instance, [^32] generated diverse draft sequences from different boost-tuned LMs; [^4] considered the top-k predictions from each FFN head to obtain multiple candidate sequences.

![Refer to caption](https://arxiv.org/html/2401.07851v3/x3.png)

Figure 4: Illustration of the token tree sequences ( left ) and tree attention mask ( right ). For simplicity, we only visualize the attention mask of tokens in white colors.

## 7 Alignment

As illustrated in Section 5, the speedup of Speculative Decoding primarily depends on the speculation accuracy, which in turn is influenced by the behavior similarity between the drafter and the target LLM. To enhance this, existing research has explored various knowledge distillation (KD) strategies to align the drafter’s outputs with those of the target LLM [^42] [^49] [^32] [^31] [^24] [^60]. Particularly, Blockwise Decoding adopted sequence-level knowledge distillation (Seq-KD) [^25] for alignment, which trained the drafter on the sentences generated by the target LLM. [^32] proposed a collective boost-tuning (Col-BT) strategy, applying Seq-KD to finetune multiple small LMs on the training data and utilizing their aggregated output as drafts to improve the speculation accuracy.

Although Seq-KD is effective, it ignores the probability distributions of the target LLM, leading to performance degradation with sampling methods. To rectify this, recent studies have explored other KD strategies for Speculative Decoding [^60] [^31]. Notably, DistillSpec [^60] conducted a comprehensive comparison of different KD strategies on Speculative Decoding across various downstream tasks. [^31] proposed an online KD strategy that dynamically aligns the drafter with the target LLM on the fly using the query data.

We summarize the main features of existing Speculative Decoding methods in Table 3, including the drafter type or the drafting strategy, the alignment approach, supported verification strategies, and the reported speedup, etc.

## 8 Spec-Bench

With the rapid research progress in Speculative Decoding, there is an increasing demand for comparative analysis of leading methods. However, existing approaches are tested using disparate benchmarks, devices, and environments, making fair comparisons impractical. To address this gap, we introduce Spec-Bench – a comprehensive benchmark for Speculative Decoding covering diverse application scenarios. Based on Spec-Bench, we present a systematic comparison of open-source approaches under third-party testing conditions. Experiments were executed on the same device and testing environment to ensure a fair comparison.

### 8.1 Benchmark Construction

To assess Speculative Decoding methods across various scenarios, Spec-Bench encompasses six distinct subtasks: multi-turn conversation, translation, summarization, question answering, mathematical reasoning, and retrieval-augmented generation. We composed Spec-Bench by randomly selecting 80 instances from each of six widely used datasets, including MT-bench [^59], WMT14 DE-EN, CNN/Daily Mail [^34], Natural Questions [^26], GSM8K [^9], and DPR [^23]. For details on Spec-Bench and the specific experimental setup, please refer to Appendix B.

![Refer to caption](https://arxiv.org/html/2401.07851v3/x4.png)

Figure 5: Speedup comparison of various Speculative Decoding methods on Spec-Bench with greedy settings ( T = 0 𝑇 T=0 italic\_T = 0 ). Evaluations were conducted on Vicuna-7B with a batch size of 1. We present the mean speedup over 3 runs. The detailed results are shown in Appendix C.

### 8.2 Comparative Evaluation

Our main evaluations were conducted on Vicuna-7B at FP16 precision using a single consumer-grade 3090 GPU <sup>4</sup>. As depicted in Figure 5, under greedy settings, EAGLE [^30] achieves the highest speedup ratio (1.8 $\times$ $\sim$ 2.4 $\times$) over autoregressive decoding across most subtasks, especially in mathematical reasoning (with a $\sim$ 2.4 $\times$ speedup). EAGLE’s success is mainly due to two factors: 1) it reuses the KV cache of LLMs to predict drafted tokens, substantially reducing the drafting computational overhead; 2) compared with Medusa [^4], EAGLE drafts in an autoregressive way, providing more stable and accurate speculation results. PLD [^38] excels in subtasks with high similarities between input and output, such as summarization (with a $\sim$ 2.4 $\times$ speedup). However, its performance diminishes in other subtasks like translation and question answering, with speedup ratios falling between 1.1 $\times$ $\sim$ 1.3 $\times$.

![Refer to caption](https://arxiv.org/html/2401.07851v3/x5.png)

Figure 6: Speedup comparison of various methods on Spec-Bench at different temperatures. The speedup effect diminishes as the sampling temperature increases.

We also compare the speedups of Speculative Decoding methods at different sampling temperatures. As illustrated in Figure 6, EAGLE consistently outperforms other methods across various settings, achieving a speedup ratio ranging from 1.7 $\times$ to 2.1 $\times$. Besides, it is observed that the acceleration effect of all methods decreases with an increase in sampling temperature. This is attributed to the increased computational complexity of the speculative sampling criterion at higher temperatures, as revealed in prior research [^22] [^40].

## 9 Challenges and Future Directions

#### How to trade off speculation accuracy and drafting efficiency?

As discussed in Sections 5, scaling up the drafter can effectively enhance speculation accuracy, yet it largely reduces the drafting efficiency and even the overall speedup. Therefore, it is essential to strike a balance between speculation accuracy and drafting latency. Among existing strategies, behavior alignment is a promising approach to address this issue, as it improves speculation accuracy without increasing latency. However, despite recent advancements [^32] [^60] [^31], there is still considerable room for improvement to align the drafter with the target LLM. For example, given that the drafted tokens after the bifurcation position are all discarded, one potential direction could involve encouraging the drafter to prioritize the generation quality of early-position tokens. Beyond alignment, other factors such as the quality of drafting [^15] and the determination of speculation length [^43] also influence speculation accuracy and merit further exploration.

#### How to apply Speculative Decoding in batched inference scenarios?

Currently, only a few Speculative Decoding implementations have supported batched inference, such as EAGLE <sup>5</sup> and SpS <sup>6</sup>. However, batched inference is a crucial technique for efficiently managing user inputs in LLM real-time services. The primary challenges in batched Speculative Decoding lie in two aspects: (1) Each decoded sentence in Speculative Decoding varies in decoding steps due to different speculation accuracy. Thus, the inference latency of a batch depends on the slowest sample in the batch; (2) The extra computational complexity introduced by Speculative Decoding, especially in sampling settings, increases with larger batch sizes. How to maintain a promising speedup of Speculative Decoding in batched inference, and combine it with advanced techniques such as continuous batching [^54], warrants further investigation.

#### How to integrate Speculative Decoding with other leading techniques?

As a general decoding paradigm, Speculative Decoding has already demonstrated its potential in conjunction with other advanced techniques [^51] [^58] [^29]. For instance, [^55] combined Speculative Decoding with Contrastive Decoding [^29], which not only speeds up the inference but also substantially improves the generation quality. In addition to the acceleration of text-only LLMs, applying Speculative Decoding in multimodal inference, such as image synthesis, text-to-speech synthesis, and video generation, is also an intriguing and valuable direction for future research. Another promising research direction is to integrate Speculative Decoding with other efficient methods such as vLLM [^27], Non-Auregressive Generation [^13] [^14] and Flash-Attention [^11] [^10], further boosting the inference efficiency of LLM services.

## 10 Conclusion

This paper presents a comprehensive survey of Speculative Decoding, including the evolution of this promising paradigm, its formal definition and formulation, a systematic categorization of existing methods, and an in-depth review of leading techniques. Moreover, we introduce Spec-Bench, an extensive evaluation benchmark for Speculative Decoding methods, and present a comparative evaluation of prominent methods. To our knowledge, this is the first survey dedicated to Speculative Decoding. Our aim for this paper is to clarify the current research landscape and provide insights into future research directions.

## Limitations

This paper provides a thorough examination and categorization of current methodologies and emerging trends in Speculative Decoding. We have also conducted a comparative analysis of leading open-source methods to offer researchers deeper insights into the advantages and limitations of different models. Beyond Speculative Decoding, we acknowledge additional efficient NLP strategies such as vLLM [^27] and continuous batching [^54]. In the future, we intend to expand the discussion to encompass the integration of Speculative Decoding with these advanced techniques. Moreover, due to the absence of an available implementation of batched Speculative Decoding, our evaluations could not cover this aspect. We plan to undertake subsequent experiments to assess the speedup of Speculative Decoding methods across various batch sizes.

## Ethics Statement

The datasets used in our experiment are publicly released and labeled through interaction with humans in English. In this process, user privacy is protected, and no personal information is contained in the dataset. The scientific artifacts that we used are available for research with permissive licenses. And the use of these artifacts in this paper is consistent with their intended use. Therefore, we believe that our research work meets the ethics of ACL.

## Acknowledgements

We thank all anonymous reviewers for their valuable comments during the review process. This work is partially supported by Research Grants Council of Hong Kong (15207122 and 15213323).

## References

## Appendix

## Appendix A Applications

In addition to serving as a general paradigm, recent work has revealed that some variants of Speculative Decoding demonstrate extraordinary effectiveness in specific tasks. Furthermore, other research has applied this paradigm to address latency issues unique to certain application scenarios, achieving inference acceleration. Below, we will provide a detailed introduction to these promising works.

Recent studies have highlighted Speculative Decoding is particularly well suited for tasks where model inputs and outputs are highly similar [^44] [^16] [^51], such as Grammatical Error Correction [^48] [^1] and Retrieval-augmented Generation [^3]. These methods introduced a specialized form of Speculative Decoding, where the initial user input or the retrieved context is directly employed as drafts. For instance, SAD [^44], an early attempt at Speculative Decoding on Grammatical Error Correction, utilized the input sentence with grammatical errors as a draft and leveraged the LLM to verify the whole sentence in parallel, achieving a $9\times$ $\sim$ $12\times$ speedup. Similarly, LLMA [^51] selected text spans from the reference as drafts, demonstrating a $2\times$ $\sim$ $3\times$ speedup across various practical application scenarios including Retrieval-augmented Generation, Cache-assisted Generation, and Multi-turn Conversations.

Beyond these works, RaLMSpec [^58] adopted Speculative Decoding to accelerate retrieval-augmented language models (RaLMs). It pointed out that the main latency bottleneck of iterative RaLMs is the frequent retrieval from a vast knowledge base. To accelerate inference, this method proposed to maintain a local cache for speculative retrieval, achieving around $2\times$ speedup with identical model outputs. LLMCad [^50] applied Speculative Decoding to on-device LLM inference. Concretely, it proposed to generate drafts with a smaller real-time LM that can be hosted in device memory, and only utilize the target LLM for parallel verification. This approach effectively reduces repetitive releasing and loading of model weights, achieving a $9.3\times$ speedup compared to existing inference engines.

## Appendix B Experimental Details

### B.1 Details of Spec-Bench

To assess the acceleration performance of Speculative Decoding methods in various scenarios, we developed Spec-Bench, a comprehensive benchmark encompassing six distinct tasks. Spec-Bench integrates MT-bench [^59], a multi-turn conversation benchmark previously adopted in research [^4] [^30], to provide a basis for comparison with earlier studies. Additionally, it includes two input-guided tasks: summarization and retrieval-augmented generation (RAG), both of which exhibit a significant overlap between the input prompts and the target outputs. We selected CNN/Daily Mail [^34] and Natural Questions [^26] as the dataset for these two tasks, respectively. Specifically, in the RAG subtask, the top-5 documents retrieved from DPR [^23] were concatenated with each question to construct the input prompt.

Moreover, Spec-Bench incorporates three further subtasks – translation, question answering, and mathematical reasoning – to provide a thorough evaluation of Speculative Decoding’s speedup capabilities in diverse contexts. We utilized WMT14 DE-EN, Natural Questions, and GSM8K [^9] as the primary datasets for these tasks, respectively. We randomly selected 80 instances from each subtask’s test set for evaluation. The detailed composition is summarized in Table 4.

| Subtask | Dataset | #Samples |
| --- | --- | --- |
| Multi-turn Conversation | MT-bench | 80 |
| Retrieval-aug. Generation | Natural Questions | 80 |
| Summarization | CNN/Daily Mail | 80 |
| Translation | WMT14 DE-EN | 80 |
| Question Answering | Natural Questions | 80 |
| Mathematical Reasoning | GSM8K | 80 |
| Overall | \- | 480 |

Table 4: Detailed Composition of Spec-Bench. Spec-Bench includes 6 distinct subtasks to encompass diverse application scenarios.

<table><tbody><tr><td colspan="2">Models</td><td>Multi-turnConversation</td><td>Translation</td><td>Summarization</td><td>QuestionAnswering</td><td>MathematicalReasoning</td><td>Retrieval-aug.Generation</td><td>#tokens/s</td><td>Avg.</td></tr><tr><td rowspan="7"><math><semantics><mrow><mi>T</mi> <mo>=</mo> <mn>0</mn></mrow> <annotation-xml><apply><ci>𝑇</ci> <cn>0</cn></apply></annotation-xml> <annotation>T=0</annotation> <annotation>italic_T = 0</annotation></semantics></math></td><td>Autoregressive Decoding</td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>36.74 <sub>±0.31</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>Lookahead <sup><a href="#fn:15">15</a></sup></td><td>1.15 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>0.98 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.07 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.06 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.32 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.03 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>40.64 <sub>±0.26</sub></td><td>1.11 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>REST <sup><a href="#fn:17">17</a></sup></td><td>1.49 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.23 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.04</sub></td><td>1.26 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>1.39 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.04</sub></td><td>1.34 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>1.71 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.05</sub></td><td>51.12 <sub>±0.78</sub></td><td>1.39 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>PLD <sup><a href="#fn:38">38</a></sup></td><td>1.63 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.11 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>2.41 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.04</sub></td><td>1.27 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>1.70 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>1.66 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.04</sub></td><td>59.42 <sub>±0.55</sub></td><td>1.62 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>SpS <sup><a href="#fn:28">28</a></sup></td><td>1.92 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.04</sub></td><td>1.33 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.93 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>1.81 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.04</sub></td><td>1.84 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.76 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>64.85 <sub>±0.70</sub></td><td>1.77 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>Medusa <sup><a href="#fn:4">4</a></sup></td><td>1.65 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>1.41 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.33 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>1.44 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>1.69 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>1.29 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>54.30 <sub>±0.34</sub></td><td>1.48 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>EAGLE <sup><a href="#fn:30">30</a></sup></td><td>2.35 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>1.79 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>2.04 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.96 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>2.44 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.80 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>76.30 <sub>±0.36</sub></td><td>2.08 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td rowspan="4"><math><semantics><mrow><mi>T</mi> <mo>=</mo> <mn>1</mn></mrow> <annotation-xml><apply><ci>𝑇</ci> <cn>1</cn></apply></annotation-xml> <annotation>T=1</annotation> <annotation>italic_T = 1</annotation></semantics></math></td><td>Autoregressive Decoding</td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>36.24 <sub>±0.43</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>REST <sup><a href="#fn:17">17</a></sup></td><td>1.43 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>1.19 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.24 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.36 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.34 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.61 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>49.04 <sub>±0.30</sub></td><td>1.35 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>SpS <sup><a href="#fn:28">28</a></sup></td><td>1.55 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>1.20 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>1.57 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>1.54 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>1.56 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>1.52 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>53.94 <sub>±0.43</sub></td><td>1.49 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>EAGLE <sup><a href="#fn:30">30</a></sup></td><td>1.79 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.61 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>1.74 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>1.66 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.04</sub></td><td>1.95 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.06</sub></td><td>1.63 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>62.88 <sub>±0.54</sub></td><td>1.74 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr></tbody></table>

Table 5: Speedup comparison of various Speculative Decoding methods on Spec-Bench. The results were obtained using Vicuna-7B-v1.3 at FP16 precision. Evaluations were conducted on a single NVIDIA 3090 GPU with a batch size of 1. We report the mean speedup ratio over 3 different runs. We show the best results in boldface.

### B.2 Implementation Details

We have selected six representative Speculative Decoding methods for our comparative analysis on Spec-Bench. These methods are open-source and free of bugs. Specifically, SpS [^5] stands as the pioneering work in this field, utilizing a smaller LM from the same model series as the drafter to accelerate LLM inference. Medusa [^4] and EAGLE [^30] integrate additional lightweight heads into the target LLM to facilitate efficient drafting. Lookahead [^15] introduces multiple special tokens to the end of the input prompt for parallel drafting and transforms the drafts into n-gram candidates. PLD [^38] is the code implementation <sup>7</sup> of LLMA [^51], which selects text spans from the input as drafts. REST [^17] retrieves relevant drafts from text corpora based on the input prompt.

We conducted our experimental evaluations using the Vicuna-v1.3 model series [^59]. For SpS, we employed the Huggingface implementation <sup>8</sup> and utilized the vicuna-68m-v1.3 model provided by [^52] as the drafter. We followed the default parameters of Lookahead <sup>9</sup> and PLD for our evaluations. The main experiments were conducted using Pytorch 2.0.1 with a single consumer-grade NVIDIA GeForce RTX 3090 GPU (24GB) of 12 CPU cores under CUDA 11.8. Further analysis was performed on a more powerful NVIDIA A100 GPU (80GB) of 64 CPU cores under CUDA 11.4.

## Appendix C Details of Main Experimental Results

The detailed results of our main analysis are shown in Table 5, including the experimental settings of greedy decoding ($T=0$) and speculative sampling ($T=1$). The findings indicate that EAGLE [^30] excels across various Spec-Bench subtasks, achieving an overall speedup ranging from 1.6 $\times$ to 2.4 $\times$. PLD [^38] shows notable efficiency in scenarios where the input and output have a significant overlap. For instance, the speedup ratio of PLD increases from 1.27 $\times$ in the question answering subtask to 1.66 $\times$ in the retrieval-augmented generation subtask, highlighting its effectiveness when the input includes relevant documents. Notably, most methods achieve a suboptimal speedup on the translation subtask. We suspect that it is due to the potential lack of multilingual data in the pretraining corpora.

![Refer to caption](https://arxiv.org/html/2401.07851v3/x6.png)

Figure 7: Speedup comparison of various methods on Spec-Bench with different computational devices.

<table><thead><tr><th colspan="2">Models</th><th>Multi-turnConversation</th><th>Translation</th><th>Summarization</th><th>QuestionAnswering</th><th>MathematicalReasoning</th><th>Retrieval-aug.Generation</th><th>#tokens/s</th><th>Avg.</th></tr></thead><tbody><tr><td rowspan="7">Vicuna-7B</td><td>Autoregressive Decoding</td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>40.24 <sub>±0.30</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>Lookahead <sup><a href="#fn:15">15</a></sup></td><td>1.95 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>1.61 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.05</sub></td><td>1.63 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.73 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.04</sub></td><td>2.16 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.04</sub></td><td>1.50 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>71.20 <sub>±1.30</sub></td><td>1.77 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>REST <sup><a href="#fn:17">17</a></sup></td><td>1.72 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.06</sub></td><td>1.38 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.05</sub></td><td>1.46 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.04</sub></td><td>1.80 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.04</sub></td><td>1.31 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>1.87 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.06</sub></td><td>63.81 <sub>±1.00</sub></td><td>1.59 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>PLD <sup><a href="#fn:38">38</a></sup></td><td>1.67 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>1.06 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>2.59 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.06</sub></td><td>1.16 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>1.63 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>1.83 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>66.61 <sub>±1.15</sub></td><td>1.66 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>SpS <sup><a href="#fn:28">28</a></sup></td><td>1.78 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>1.19 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.78 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>1.58 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>1.54 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.69 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>64.07 <sub>±0.41</sub></td><td>1.59 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>Medusa <sup><a href="#fn:4">4</a></sup></td><td>2.79 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.07</sub></td><td>2.36 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.07</sub></td><td>2.14 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.04</sub></td><td>2.36 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.08</sub></td><td>2.77 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.08</sub></td><td>2.05 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>97.27 <sub>±2.04</sub></td><td>2.42 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>EAGLE <sup><a href="#fn:30">30</a></sup></td><td>2.75 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.05</sub></td><td>2.08 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.05</sub></td><td>2.32 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.05</sub></td><td>2.23 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>2.79 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.04</sub></td><td>2.15 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>96.23 <sub>±1.15</sub></td><td>2.39 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td rowspan="7">Vicuna-13B</td><td>Autoregressive Decoding</td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>31.38 <sub>±0.22</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>Lookahead <sup><a href="#fn:15">15</a></sup></td><td>1.57 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>1.34 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>1.39 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.40 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>1.82 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.32 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>46.42 <sub>±0.12</sub></td><td>1.48 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>REST <sup><a href="#fn:17">17</a></sup></td><td>1.68 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>1.31 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.05</sub></td><td>1.51 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>1.67 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.29 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.96 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>48.89 <sub>±0.26</sub></td><td>1.56 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>PLD <sup><a href="#fn:38">38</a></sup></td><td>1.53 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.08 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>2.25 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.09 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.65 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>1.72 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>48.42 <sub>±0.17</sub></td><td>1.54 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>SpS <sup><a href="#fn:28">28</a></sup></td><td>1.73 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.25 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.76 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.53 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>1.68 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.73 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>50.48 <sub>±0.28</sub></td><td>1.61 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>Medusa <sup><a href="#fn:4">4</a></sup></td><td>2.39 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>2.12 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.92 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>2.07 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>2.49 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.02</sub></td><td>1.88 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>67.64 <sub>±0.07</sub></td><td>2.16 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>EAGLE <sup><a href="#fn:30">30</a></sup></td><td>2.88 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.05</sub></td><td>2.24 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.04</sub></td><td>2.52 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>2.24 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.04</sub></td><td>2.90 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.03</sub></td><td>2.34 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>79.35 <sub>±1.18</sub></td><td>2.53 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td rowspan="7">Vicuna-33B</td><td>Autoregressive Decoding</td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>16.34 <sub>±0.01</sub></td><td>1.00 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>Lookahead <sup><a href="#fn:15">15</a></sup></td><td>1.46 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.21 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.32 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.29 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.71 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.28 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>22.58 <sub>±0.08</sub></td><td>1.38 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>REST <sup><a href="#fn:17">17</a></sup></td><td>1.71 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>1.39 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.57 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.69 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>1.34 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>1.89 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>25.98 <sub>±0.07</sub></td><td>1.59 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>PLD <sup><a href="#fn:38">38</a></sup></td><td>1.45 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.06 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.98 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.07 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.54 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.43 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>23.07 <sub>±0.01</sub></td><td>1.41 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>SpS <sup><a href="#fn:28">28</a></sup></td><td>1.79 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.31 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.80 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.57 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.73 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.69 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>26.89 <sub>±0.03</sub></td><td>1.65 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>Medusa <sup><a href="#fn:4">4</a></sup></td><td>2.22 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.95 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.85 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>1.87 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>2.32 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.01</sub></td><td>1.84 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>32.92 <sub>±0.06</sub></td><td>2.01 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr><tr><td>EAGLE <sup><a href="#fn:30">30</a></sup></td><td>2.81 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>2.14 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>2.53 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>2.19 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>3.01 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>2.31 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> <sub>±0.00</sub></td><td>40.91 <sub>±0.03</sub></td><td>2.50 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math></td></tr></tbody></table>

Table 6: Speedup comparison of Speculative Decoding methods across various model scales on Spec-Bench. The results were obtained using Vicuna-v1.3 at FP16 precision with greedy settings ($T=0$). Evaluations were conducted on a single NVIDIA A100 GPU with a batch size of 1. We report the mean speedup over 3 different runs.

## Appendix D Further Analysis on A100

This section presents a comprehensive analysis of leading Speculative Decoding methods on Spec-Bench, utilizing a single NVIDIA A100 GPU. The discussion delves into the influence of computational hardware, model scale, and computational precision on the performance of Speculative Decoding. All experiments were performed on the same device and environment to ensure fair comparison.

![Refer to caption](https://arxiv.org/html/2401.07851v3/x7.png)

Figure 8: Speedup comparison of various Speculative Decoding methods on a single A100 GPU with greedy settings ( T = 0 𝑇 T=0 italic\_T = 0 ). Evaluations were conducted on Spec-Bench using Vicuna-7B at FP16 precision.

### D.1 Computational Devices

We first discuss the impact of evolving computational devices on Speculative Decoding. As depicted in Figure 7, the acceleration effect of most Speculative Decoding methods is notably enhanced when employed on high-performance GPUs, such as NVIDIA A100s. This enhancement is primarily due to the increased availability of idle computational resources on more advanced computational devices, which Speculative Decoding can leverage to accelerate inference processes. Among the methods evaluated, Medusa [^4] and Lookahead [^15] demonstrate the most significant improvements. Specifically, the speedup ratio for Medusa escalates from 1.48 $\times$ to 2.42 $\times$, and for Lookahead, it rises from 1.11 $\times$ to 1.77 $\times$. This finding underscores that Speculative Decoding methods will benefit more from evolving computational hardware, such as H100 GPUs.

We illustrate the comparison of various Speculative Decoding methods evaluated with a single A100 GPU in Figure 8. The detailed experimental results are shown in Table 6. The results indicate that Medusa [^4] and EAGLE [^30] excel in this experimental setting, achieving an overall speedup of 2.4 $\times$. These two methods perform particularly well on the multi-turn conversation and mathematical reasoning subtasks, with a $\sim$ 2.8 $\times$ speedup.

![Refer to caption](https://arxiv.org/html/2401.07851v3/x8.png)

Figure 9: Speedup comparison of various methods on Spec-Bench at different model scales.

### D.2 Model Scale

We present the speedup comparison of Speculative Decoding methods across various model scales in Figure 9. The detailed experimental results are shown in Table 6. Among all the evaluated methods, EAGLE [^30] maintains a high speedup ratio over autoregressive decoding across all model scales, achieving a speedup ratio ranging from 2.4 $\times$ to 2.5 $\times$. While Medusa [^4] demonstrates superior acceleration performance on Vicuna-7B, its speedup ratio degrades from 2.4 $\times$ to 2.0 $\times$ as the model scale increases.

### D.3 Computational Precision

It is noteworthy that most Speculative Decoding approaches are predominantly evaluated using FP16 precision [^15] [^4] [^30] [^17]. However, it is critical to underscore that the outputs generated by Speculative Decoding in FP16 precision may not consistently align with those derived from autoregressive decoding. This divergence stems from the accumulation of floating-point errors inherent in FP16 computations, which can result in discrepancies between the outputs of the two decoding methods, particularly in the context of longer sequences. In FP32 precision, the outputs of Speculative Decoding are guaranteed to be exactly the same as autoregressive decoding.

![Refer to caption](https://arxiv.org/html/2401.07851v3/x9.png)

Figure 10: Speedup comparison of various methods on Spec-Bench with different computational precision.

We compare the speedup performance of Speculative Decoding methods with FP16/FP32 precision in Figure 10. The experimental results reveal a noticeable reduction in speedup for all methods under FP32 precision. Specifically, PLD [^38] achieves merely 1.01 $\times$ speedup in FP32 precision, and the acceleration effect of EAGLE [^30] also diminishes, with its speedup falling from 2.39 $\times$ to 1.74 $\times$. To furnish the research community with a comprehensive understanding of the acceleration impact, we advocate for future studies to report speedup metrics across both precision settings.

[^1]: Christopher Bryant, Zheng Yuan, Muhammad Reza Qorib, Hannan Cao, Hwee Tou Ng, and Ted Briscoe. 2023. [Grammatical error correction: A survey of the state of the art](https://doi.org/10.1162/COLI_A_00478). *Comput. Linguistics*, 49(3):643–701.

[^2]: F. Warren Burton. 1985. [Speculative computation, parallelism, and functional programming](https://doi.org/10.1109/TC.1985.6312218). *IEEE Trans. Computers*, 34(12):1190–1193.

[^3]: Deng Cai, Yan Wang, Lemao Liu, and Shuming Shi. 2022. [Recent advances in retrieval-augmented text generation](https://doi.org/10.1145/3477495.3532682). In *SIGIR ’22: The 45th International ACM SIGIR Conference on Research and Development in Information Retrieval, Madrid, Spain, July 11 - 15, 2022*, pages 3417–3419. ACM.

[^4]: Tianle Cai, Yuhong Li, Zhengyang Geng, Hongwu Peng, Jason D. Lee, Deming Chen, and Tri Dao. 2024. [Medusa: Simple LLM inference acceleration framework with multiple decoding heads](https://doi.org/10.48550/ARXIV.2401.10774). *CoRR*, abs/2401.10774.

[^5]: Charlie Chen, Sebastian Borgeaud, Geoffrey Irving, Jean-Baptiste Lespiau, Laurent Sifre, and John Jumper. 2023a. [Accelerating large language model decoding with speculative sampling](https://doi.org/10.48550/arXiv.2302.01318). *CoRR*, abs/2302.01318.

[^6]: Ziyi Chen, Xiaocong Yang, Jiacheng Lin, Chenkai Sun, Jie Huang, and Kevin Chen-Chuan Chang. 2023b. [Cascade speculative drafting for even faster llm inference](http://arxiv.org/abs/2312.11462).

[^7]: Wei-Lin Chiang, Zhuohan Li, Zi Lin, Ying Sheng, Zhanghao Wu, Hao Zhang, Lianmin Zheng, Siyuan Zhuang, Yonghao Zhuang, Joseph E. Gonzalez, Ion Stoica, and Eric P. Xing. 2023. [Vicuna: An open-source chatbot impressing gpt-4 with 90%\* chatgpt quality](https://lmsys.org/blog/2023-03-30-vicuna/).

[^8]: Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian Gehrmann, Parker Schuh, Kensen Shi, Sasha Tsvyashchenko, Joshua Maynez, Abhishek Rao, Parker Barnes, Yi Tay, Noam Shazeer, Vinodkumar Prabhakaran, Emily Reif, Nan Du, Ben Hutchinson, Reiner Pope, James Bradbury, Jacob Austin, Michael Isard, Guy Gur-Ari, Pengcheng Yin, Toju Duke, Anselm Levskaya, Sanjay Ghemawat, Sunipa Dev, Henryk Michalewski, Xavier Garcia, Vedant Misra, Kevin Robinson, Liam Fedus, Denny Zhou, Daphne Ippolito, David Luan, Hyeontaek Lim, Barret Zoph, Alexander Spiridonov, Ryan Sepassi, David Dohan, Shivani Agrawal, Mark Omernick, Andrew M. Dai, Thanumalayan Sankaranarayana Pillai, Marie Pellat, Aitor Lewkowycz, Erica Moreira, Rewon Child, Oleksandr Polozov, Katherine Lee, Zongwei Zhou, Xuezhi Wang, Brennan Saeta, Mark Diaz, Orhan Firat, Michele Catasta, Jason Wei, Kathy Meier-Hellstern, Douglas Eck, Jeff Dean, Slav Petrov, and Noah Fiedel. 2023. [Palm: Scaling language modeling with pathways](http://jmlr.org/papers/v24/22-1144.html). *J. Mach. Learn. Res.*, 24:240:1–240:113.

[^9]: Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman. 2021. [Training verifiers to solve math word problems](http://arxiv.org/abs/2110.14168). *CoRR*, abs/2110.14168.

[^10]: Tri Dao. 2023. [Flashattention-2: Faster attention with better parallelism and work partitioning](https://doi.org/10.48550/ARXIV.2307.08691). *CoRR*, abs/2307.08691.

[^11]: Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, and Christopher Ré. 2022. [Flashattention: Fast and memory-efficient exact attention with io-awareness](http://papers.nips.cc/paper_files/paper/2022/hash/67d57c32e20fd0a7a302cb81d36e40d5-Abstract-Conference.html). In *Advances in Neural Information Processing Systems 35: Annual Conference on Neural Information Processing Systems 2022, NeurIPS 2022, New Orleans, LA, USA, November 28 - December 9, 2022*.

[^12]: Cunxiao Du, Jing Jiang, Yuanchen Xu, Jiawei Wu, Sicheng Yu, Yongqi Li, Shenggui Li, Kai Xu, Liqiang Nie, Zhaopeng Tu, and Yang You. 2024. [Glide with a cape: A low-hassle method to accelerate speculative decoding](https://doi.org/10.48550/ARXIV.2402.02082). *CoRR*, abs/2402.02082.

[^13]: Cunxiao Du, Zhaopeng Tu, and Jing Jiang. 2021. [Order-agnostic cross entropy for non-autoregressive machine translation](http://proceedings.mlr.press/v139/du21c.html). In *Proceedings of the 38th International Conference on Machine Learning, ICML 2021, 18-24 July 2021, Virtual Event*, volume 139 of *Proceedings of Machine Learning Research*, pages 2849–2859. PMLR.

[^14]: Cunxiao Du, Zhaopeng Tu, Longyue Wang, and Jing Jiang. 2022. [ngram-oaxe: Phrase-based order-agnostic cross entropy for non-autoregressive machine translation](https://aclanthology.org/2022.coling-1.446). In *Proceedings of the 29th International Conference on Computational Linguistics, COLING 2022, Gyeongju, Republic of Korea, October 12-17, 2022*, pages 5035–5045. International Committee on Computational Linguistics.

[^15]: Yichao Fu, Peter Bailis, Ion Stoica, and Hao Zhang. 2024. [Break the sequential dependency of llm inference using lookahead decoding](http://arxiv.org/abs/2402.02057).

[^16]: Tao Ge, Heming Xia, Xin Sun, Si-Qing Chen, and Furu Wei. 2022. [Lossless acceleration for seq2seq generation with aggressive decoding](https://doi.org/10.48550/ARXIV.2205.10350). *CoRR*, abs/2205.10350.

[^17]: Zhenyu He, Zexuan Zhong, Tianle Cai, Jason D. Lee, and Di He. 2023. [REST: retrieval-based speculative decoding](https://doi.org/10.48550/ARXIV.2311.08252). *CoRR*, abs/2311.08252.

[^18]: John L. Hennessy and David A. Patterson. 2012. *Computer Architecture - A Quantitative Approach, 5th Edition*. Morgan Kaufmann.

[^19]: Coleman Hooper, Sehoon Kim, Hiva Mohammadzadeh, Hasan Genc, Kurt Keutzer, Amir Gholami, and Yakun Sophia Shao. 2023. [SPEED: speculative pipelined execution for efficient decoding](https://doi.org/10.48550/ARXIV.2310.12072). *CoRR*, abs/2310.12072.

[^20]: Albert Q. Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh Chaplot, Diego de Las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile Saulnier, Lélio Renard Lavaud, Marie-Anne Lachaux, Pierre Stock, Teven Le Scao, Thibaut Lavril, Thomas Wang, Timothée Lacroix, and William El Sayed. 2023. [Mistral 7b](https://doi.org/10.48550/ARXIV.2310.06825). *CoRR*, abs/2310.06825.

[^21]: Albert Q. Jiang, Alexandre Sablayrolles, Antoine Roux, Arthur Mensch, Blanche Savary, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Emma Bou Hanna, Florian Bressand, Gianna Lengyel, Guillaume Bour, Guillaume Lample, Lélio Renard Lavaud, Lucile Saulnier, Marie-Anne Lachaux, Pierre Stock, Sandeep Subramanian, Sophia Yang, Szymon Antoniak, Teven Le Scao, Théophile Gervet, Thibaut Lavril, Thomas Wang, Timothée Lacroix, and William El Sayed. 2024. [Mixtral of experts](http://arxiv.org/abs/2401.04088).

[^22]: Joao Gante. 2023. [Assisted generation: a new direction toward low-latency text generation](https://doi.org/10.57967/hf/0638).

[^23]: Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick S. H. Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and Wen-tau Yih. 2020. [Dense passage retrieval for open-domain question answering](https://doi.org/10.18653/V1/2020.EMNLP-MAIN.550). In *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing, EMNLP 2020, Online, November 16-20, 2020*, pages 6769–6781. Association for Computational Linguistics.

[^24]: Sehoon Kim, Karttikeya Mangalam, Suhong Moon, Jitendra Malik, Michael W. Mahoney, Amir Gholami, and Kurt Keutzer. 2023. [Speculative decoding with big little decoder](http://papers.nips.cc/paper_files/paper/2023/hash/7b97adeafa1c51cf65263459ca9d0d7c-Abstract-Conference.html). In *Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023*.

[^25]: Yoon Kim and Alexander M. Rush. 2016. [Sequence-level knowledge distillation](https://doi.org/10.18653/V1/D16-1139). In *Proceedings of the 2016 Conference on Empirical Methods in Natural Language Processing, EMNLP 2016, Austin, Texas, USA, November 1-4, 2016*, pages 1317–1327. The Association for Computational Linguistics.

[^26]: Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris Alberti, Danielle Epstein, Illia Polosukhin, Jacob Devlin, Kenton Lee, Kristina Toutanova, Llion Jones, Matthew Kelcey, Ming-Wei Chang, Andrew M. Dai, Jakob Uszkoreit, Quoc Le, and Slav Petrov. 2019. [Natural questions: A benchmark for question answering research](https://doi.org/10.1162/tacl_a_00276). *Transactions of the Association for Computational Linguistics*, 7:452–466.

[^27]: Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph Gonzalez, Hao Zhang, and Ion Stoica. 2023. [Efficient memory management for large language model serving with pagedattention](https://doi.org/10.1145/3600006.3613165). In *Proceedings of the 29th Symposium on Operating Systems Principles, SOSP 2023, Koblenz, Germany, October 23-26, 2023*, pages 611–626. ACM.

[^28]: Yaniv Leviathan, Matan Kalman, and Yossi Matias. 2023. [Fast inference from transformers via speculative decoding](https://proceedings.mlr.press/v202/leviathan23a.html). In *International Conference on Machine Learning, ICML 2023, 23-29 July 2023, Honolulu, Hawaii, USA*, volume 202 of *Proceedings of Machine Learning Research*, pages 19274–19286. PMLR.

[^29]: Xiang Lisa Li, Ari Holtzman, Daniel Fried, Percy Liang, Jason Eisner, Tatsunori Hashimoto, Luke Zettlemoyer, and Mike Lewis. 2023. [Contrastive decoding: Open-ended text generation as optimization](https://doi.org/10.18653/V1/2023.ACL-LONG.687). In *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2023, Toronto, Canada, July 9-14, 2023*, pages 12286–12312. Association for Computational Linguistics.

[^30]: Yuhui Li, Fangyun Wei, Chao Zhang, and Hongyang Zhang. 2024. [Eagle: Speculative sampling requires rethinking feature uncertainty](http://arxiv.org/abs/2401.15077).

[^31]: Xiaoxuan Liu, Lanxiang Hu, Peter Bailis, Ion Stoica, Zhijie Deng, Alvin Cheung, and Hao Zhang. 2023. [Online speculative decoding](https://doi.org/10.48550/ARXIV.2310.07177). *CoRR*, abs/2310.07177.

[^32]: Xupeng Miao, Gabriele Oliaro, Zhihao Zhang, Xinhao Cheng, Zeyu Wang, Zhengxin Zhang, Rae Ying Yee Wong, Alan Zhu, Lijie Yang, Xiaoxiang Shi, Chunan Shi, Zhuoming Chen, Daiyaan Arfeen, Reyna Abhyankar, and Zhihao Jia. 2024. [Specinfer: Accelerating large language model serving with tree-based speculative inference and verification](https://doi.org/10.1145/3620666.3651335). In *Proceedings of the 29th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, Volume 3*, ASPLOS ’24, page 932–949, New York, NY, USA. Association for Computing Machinery.

[^33]: Giovanni Monea, Armand Joulin, and Edouard Grave. 2023. [Pass: Parallel speculative sampling](https://doi.org/10.48550/ARXIV.2311.13581). *CoRR*, abs/2311.13581.

[^34]: Ramesh Nallapati, Bowen Zhou, Cícero Nogueira dos Santos, Çaglar Gülçehre, and Bing Xiang. 2016. [Abstractive text summarization using sequence-to-sequence rnns and beyond](https://doi.org/10.18653/V1/K16-1028). In *Proceedings of the 20th SIGNLL Conference on Computational Natural Language Learning, CoNLL 2016, Berlin, Germany, August 11-12, 2016*, pages 280–290. ACL.

[^35]: OpenAI. 2023. [GPT-4 technical report](https://doi.org/10.48550/ARXIV.2303.08774). *CoRR*, abs/2303.08774.

[^36]: David A. Patterson. 2004. [Latency lags bandwith](https://doi.org/10.1145/1022594.1022596). *Commun. ACM*, 47(10):71–75.

[^37]: Andrea Santilli, Silvio Severino, Emilian Postolache, Valentino Maiorca, Michele Mancusi, Riccardo Marin, and Emanuele Rodolà. 2023. [Accelerating transformer inference for translation via parallel decoding](https://doi.org/10.18653/v1/2023.acl-long.689). In *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2023, Toronto, Canada, July 9-14, 2023*, pages 12336–12355. Association for Computational Linguistics.

[^38]: Apoorv Saxena. 2023. [Prompt lookup decoding](https://github.com/apoorvumang/prompt-lookup-decoding/).

[^39]: Noam Shazeer. 2019. [Fast transformer decoding: One write-head is all you need](http://arxiv.org/abs/1911.02150). *CoRR*, abs/1911.02150.

[^40]: Benjamin Spector and Chris Re. 2023. [Accelerating LLM inference with staged speculative decoding](https://doi.org/10.48550/arXiv.2308.04623). *CoRR*, abs/2308.04623.

[^41]: Mitchell Stern, William Chan, Jamie Kiros, and Jakob Uszkoreit. 2019. [Insertion transformer: Flexible sequence generation via insertion operations](http://proceedings.mlr.press/v97/stern19a.html). In *Proceedings of the 36th International Conference on Machine Learning, ICML 2019, 9-15 June 2019, Long Beach, California, USA*, volume 97 of *Proceedings of Machine Learning Research*, pages 5976–5985. PMLR.

[^42]: Mitchell Stern, Noam Shazeer, and Jakob Uszkoreit. 2018. [Blockwise parallel decoding for deep autoregressive models](https://proceedings.neurips.cc/paper/2018/hash/c4127b9194fe8562c64dc0f5bf2c93bc-Abstract.html). In *Advances in Neural Information Processing Systems 31: Annual Conference on Neural Information Processing Systems 2018, NeurIPS 2018, December 3-8, 2018, Montréal, Canada*, pages 10107–10116.

[^43]: Qidong Su, Christina Giannoula, and Gennady Pekhimenko. 2023. [The synergy of speculative decoding and batching in serving large language models](https://doi.org/10.48550/ARXIV.2310.18813). *CoRR*, abs/2310.18813.

[^44]: Xin Sun, Tao Ge, Furu Wei, and Houfeng Wang. 2021. [Instantaneous grammatical error correction with shallow aggressive decoding](https://doi.org/10.18653/v1/2021.acl-long.462). In *Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing, ACL/IJCNLP 2021, (Volume 1: Long Papers), Virtual Event, August 1-6, 2021*, pages 5937–5947. Association for Computational Linguistics.

[^45]: Ziteng Sun, Ananda Theertha Suresh, Jae Hun Ro, Ahmad Beirami, Himanshu Jain, and Felix X. Yu. 2023. [Spectr: Fast speculative decoding via optimal transport](http://papers.nips.cc/paper_files/paper/2023/hash/6034a661584af6c28fd97a6f23e56c0a-Abstract-Conference.html). In *Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023*.

[^46]: Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, Aurélien Rodriguez, Armand Joulin, Edouard Grave, and Guillaume Lample. 2023a. [Llama: Open and efficient foundation language models](https://doi.org/10.48550/arXiv.2302.13971). *CoRR*, abs/2302.13971.

[^47]: Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, Dan Bikel, Lukas Blecher, Cristian Canton-Ferrer, Moya Chen, Guillem Cucurull, David Esiobu, Jude Fernandes, Jeremy Fu, Wenyin Fu, Brian Fuller, Cynthia Gao, Vedanuj Goswami, Naman Goyal, Anthony Hartshorn, Saghar Hosseini, Rui Hou, Hakan Inan, Marcin Kardas, Viktor Kerkez, Madian Khabsa, Isabel Kloumann, Artem Korenev, Punit Singh Koura, Marie-Anne Lachaux, Thibaut Lavril, Jenya Lee, Diana Liskovich, Yinghai Lu, Yuning Mao, Xavier Martinet, Todor Mihaylov, Pushkar Mishra, Igor Molybog, Yixin Nie, Andrew Poulton, Jeremy Reizenstein, Rashi Rungta, Kalyan Saladi, Alan Schelten, Ruan Silva, Eric Michael Smith, Ranjan Subramanian, Xiaoqing Ellen Tan, Binh Tang, Ross Taylor, Adina Williams, Jian Xiang Kuan, Puxin Xu, Zheng Yan, Iliyan Zarov, Yuchen Zhang, Angela Fan, Melanie Kambadur, Sharan Narang, Aurélien Rodriguez, Robert Stojnic, Sergey Edunov, and Thomas Scialom. 2023b. [Llama 2: Open foundation and fine-tuned chat models](https://doi.org/10.48550/ARXIV.2307.09288). *CoRR*, abs/2307.09288.

[^48]: Yu Wang, Yuelin Wang, Kai Dang, Jie Liu, and Zhuo Liu. 2021. [A comprehensive survey of grammatical error correction](https://doi.org/10.1145/3474840). *ACM Trans. Intell. Syst. Technol.*, 12(5):65:1–65:51.

[^49]: Heming Xia, Tao Ge, Peiyi Wang, Si-Qing Chen, Furu Wei, and Zhifang Sui. 2023. [Speculative decoding: Exploiting speculative execution for accelerating seq2seq generation](https://doi.org/10.18653/V1/2023.FINDINGS-EMNLP.257). In *Findings of the Association for Computational Linguistics: EMNLP 2023, Singapore, December 6-10, 2023*, pages 3909–3925. Association for Computational Linguistics.

[^50]: Daliang Xu, Wangsong Yin, Xin Jin, Ying Zhang, Shiyun Wei, Mengwei Xu, and Xuanzhe Liu. 2023. [Llmcad: Fast and scalable on-device large language model inference](https://doi.org/10.48550/ARXIV.2309.04255). *CoRR*, abs/2309.04255.

[^51]: Nan Yang, Tao Ge, Liang Wang, Binxing Jiao, Daxin Jiang, Linjun Yang, Rangan Majumder, and Furu Wei. 2023a. Inference with reference: Lossless acceleration of large language models. *arXiv preprint arXiv:2304.04487*.

[^52]: Sen Yang, Shujian Huang, Xinyu Dai, and Jiajun Chen. 2024. [Multi-candidate speculative decoding](https://doi.org/10.48550/ARXIV.2401.06706). *CoRR*, abs/2401.06706.

[^53]: Seongjun Yang, Gibbeum Lee, Jaewoong Cho, Dimitris S. Papailiopoulos, and Kangwook Lee. 2023b. [Predictive pipelined decoding: A compute-latency trade-off for exact LLM decoding](https://doi.org/10.48550/ARXIV.2307.05908). *CoRR*, abs/2307.05908.

[^54]: Gyeong-In Yu, Joo Seong Jeong, Geon-Woo Kim, Soojeong Kim, and Byung-Gon Chun. 2022. [Orca: A distributed serving system for transformer-based generative models](https://www.usenix.org/conference/osdi22/presentation/yu). In *16th USENIX Symposium on Operating Systems Design and Implementation, OSDI 2022, Carlsbad, CA, USA, July 11-13, 2022*, pages 521–538. USENIX Association.

[^55]: Hongyi Yuan, Keming Lu, Fei Huang, Zheng Yuan, and Chang Zhou. 2023. [Speculative contrastive decoding](https://doi.org/10.48550/ARXIV.2311.08981). *CoRR*, abs/2311.08981.

[^56]: Jun Zhang, Jue Wang, Huan Li, Lidan Shou, Ke Chen, Gang Chen, and Sharad Mehrotra. 2023a. [Draft & verify: Lossless large language model acceleration via self-speculative decoding](https://doi.org/10.48550/arXiv.2309.08168). *CoRR*, abs/2309.08168.

[^57]: Susan Zhang, Stephen Roller, Naman Goyal, Mikel Artetxe, Moya Chen, Shuohui Chen, Christopher Dewan, Mona T. Diab, Xian Li, Xi Victoria Lin, Todor Mihaylov, Myle Ott, Sam Shleifer, Kurt Shuster, Daniel Simig, Punit Singh Koura, Anjali Sridhar, Tianlu Wang, and Luke Zettlemoyer. 2022. [OPT: open pre-trained transformer language models](https://doi.org/10.48550/arXiv.2205.01068). *CoRR*, abs/2205.01068.

[^58]: Zhihao Zhang, Alan Zhu, Lijie Yang, Yihua Xu, Lanting Li, Phitchaya Mangpo Phothilimthana, and Zhihao Jia. 2023b. [Accelerating retrieval-augmented language model serving with speculation](https://openreview.net/forum?id=vkzPuZJ80a). In *Submitted to The Twelfth International Conference on Learning Representations*. Under review.

[^59]: Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric Xing, Hao Zhang, Joseph E. Gonzalez, and Ion Stoica. 2023. [Judging LLM-as-a-judge with MT-bench and chatbot arena](https://openreview.net/forum?id=uccHPGDlao). In *Thirty-seventh Conference on Neural Information Processing Systems Datasets and Benchmarks Track*.

[^60]: Yongchao Zhou, Kaifeng Lyu, Ankit Singh Rawat, Aditya Krishna Menon, Afshin Rostamizadeh, Sanjiv Kumar, Jean-François Kagy, and Rishabh Agarwal. 2023. [Distillspec: Improving speculative decoding via knowledge distillation](http://arxiv.org/abs/2310.08461).