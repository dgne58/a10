---
title: "DeepSeek - Wikipedia"
source: "https://en.wikipedia.org/wiki/DeepSeek?utm_source=chatgpt.com"
author:
  - "[[Contributors to Wikimedia projects]]"
published: 2024-11-26
created: 2026-04-13
description:
tags:
  - "clippings"
---
**Hangzhou DeepSeek Artificial Intelligence Basic Technology Research Co., Ltd.**,[^9] [^10] [^11] [^1] [doing business as](https://en.wikipedia.org/wiki/Trade_name "Trade name") **DeepSeek**,[^2] is a Chinese [artificial intelligence](https://en.wikipedia.org/wiki/Artificial_intelligence "Artificial intelligence") (AI) company that develops [large language models](https://en.wikipedia.org/wiki/Large_language_model "Large language model") (LLMs). Based in [Hangzhou](https://en.wikipedia.org/wiki/Hangzhou "Hangzhou"), [Zhejiang](https://en.wikipedia.org/wiki/Zhejiang "Zhejiang"), DeepSeek is owned and funded by the Chinese [hedge fund](https://en.wikipedia.org/wiki/Hedge_fund "Hedge fund") [High-Flyer](https://en.wikipedia.org/wiki/High-Flyer "High-Flyer"). DeepSeek was founded in July 2023 by [Liang Wenfeng](https://en.wikipedia.org/wiki/Liang_Wenfeng "Liang Wenfeng"), the co-founder of High-Flyer, who also serves as the [CEO](https://en.wikipedia.org/wiki/Chief_executive_officer "Chief executive officer") for both of the companies.[^13] [^14] [^15] The company launched [an eponymous chatbot](https://en.wikipedia.org/wiki/DeepSeek_\(chatbot\) "DeepSeek (chatbot)") alongside its DeepSeek-R1 model in January 2025.

DeepSeek-R1 provided responses comparable to other contemporary large language models, such as [OpenAI](https://en.wikipedia.org/wiki/OpenAI "OpenAI") 's [GPT-4](https://en.wikipedia.org/wiki/GPT-4 "GPT-4") and [o1](https://en.wikipedia.org/wiki/OpenAI_o1 "OpenAI o1").[^16] Its training cost was reported to be significantly lower than other LLMs. The company claims that it trained its V3 model for US$6 million—far less than the US$100 million cost for OpenAI's [GPT-4](https://en.wikipedia.org/wiki/GPT-4 "GPT-4") in 2023 [^17] —and using approximately one-tenth the computing power consumed by [Meta](https://en.wikipedia.org/wiki/Meta_Platforms "Meta Platforms") 's comparable model, [Llama 3.1](https://en.wikipedia.org/wiki/Llama_3.1 "Llama 3.1").[^17] [^18] [^19] DeepSeek's success against larger and more established rivals has been described as "upending AI".[^20] [^21]

DeepSeek's models are described as "open-weight", meaning the exact parameters are openly shared, but the training data is not openly licensed.[^22] [^16] Since the January 2025 debut of DeepSeek-R1, the company has made its new models available under [free and open-source software licenses](https://en.wikipedia.org/wiki/Free_and_open-source_software_licenses "Free and open-source software licenses"), primarily the [MIT License](https://en.wikipedia.org/wiki/MIT_License "MIT License").[^23] The company reportedly recruits AI researchers from top Chinese universities [^20] and also hires from outside traditional [computer science](https://en.wikipedia.org/wiki/Computer_science "Computer science") fields to broaden its models' knowledge and capabilities.[^18]

DeepSeek significantly reduced training expenses for their R1 model by incorporating techniques such as [mixture of experts](https://en.wikipedia.org/wiki/Mixture_of_experts "Mixture of experts") (MoE) layers.[^24] The company also trained its models during ongoing trade restrictions on AI chip exports to China, using weaker AI chips intended for export and employing fewer units overall.[^19] [^25] Observers say this breakthrough sent "shock waves" through the industry which were described as triggering a " [Sputnik moment](https://en.wikipedia.org/wiki/Sputnik_moment "Sputnik moment") " for the US in the field of artificial intelligence, particularly due to its open-source, cost-effective, and high-performing AI models.[^26] [^27] [^28] This threatened established AI hardware leaders such as [Nvidia](https://en.wikipedia.org/wiki/Nvidia "Nvidia"); Nvidia's share price dropped sharply, losing US$600 billion in market value, the largest single-company decline in U.S. [stock market](https://en.wikipedia.org/wiki/Stock_market "Stock market") history.[^29] [^30]

## History

### Founding and early years (2016–2023)

In February 2016, High-Flyer was co-founded by AI enthusiast [Liang Wenfeng](https://en.wikipedia.org/wiki/Liang_Wenfeng "Liang Wenfeng"), who had been trading since the [2008 financial crisis](https://en.wikipedia.org/wiki/2008_financial_crisis "2008 financial crisis") while attending [Zhejiang University](https://en.wikipedia.org/wiki/Zhejiang_University "Zhejiang University").[^31] The company began stock trading using a [GPU](https://en.wikipedia.org/wiki/GPU "GPU") -dependent deep learning model on 21 October 2016; before then, it had used [CPU](https://en.wikipedia.org/wiki/CPU "CPU") -based linear models. By the end of 2017, most of its trading was driven by AI.[^32]

Liang established High-Flyer as a hedge fund focused on developing and using AI trading algorithms, and by 2021 the firm was using AI exclusively,[^33] often using [Nvidia](https://en.wikipedia.org/wiki/Nvidia "Nvidia") chips.[^34]

In 2019, the company began constructing its first [computing cluster](https://en.wikipedia.org/wiki/Computing_cluster "Computing cluster"), Fire-Flyer, at a cost of 200 million yuan; it contained 1,100 GPUs interconnected at 200 Gbit/s and was retired after 1.5 years in operation.[^32]

By 2021, Liang had started buying large quantities of Nvidia GPUs for an AI project,[^34] reportedly obtaining 10,000 [Nvidia A100](https://en.wikipedia.org/wiki/Ampere_\(microarchitecture\)#A100_accelerator_and_DGX_A100 "Ampere (microarchitecture)") GPUs [^35] before the United States restricted chip sales to China.[^33] Computing cluster Fire-Flyer 2 began construction in 2021 with a budget of 1 billion yuan.[^32]

It was reported that in 2022, Fire-Flyer 2's capacity had been used at over 96%, totaling 56.74 million GPU hours. 27% was used to support scientific computing outside the company.[^32]

During 2022, Fire-Flyer 2 had 5,000 [PCIe](https://en.wikipedia.org/wiki/PCI_Express "PCI Express") A100 GPUs in 625 nodes, each containing 8 GPUs. At the time, it exclusively used PCIe instead of the [DGX](https://en.wikipedia.org/wiki/Nvidia_DGX "Nvidia DGX") version of A100, since at the time the models it trained could fit within a single 40 GB GPU [VRAM](https://en.wikipedia.org/wiki/Video_random-access_memory "Video random-access memory") and so there was no need for the higher bandwidth of DGX (i.e., it required only data parallelism but not model parallelism).[^36] Later, it incorporated [NVLinks](https://en.wikipedia.org/wiki/NVLink "NVLink") and NCCL (Nvidia Collective Communications Library) to train larger models that required model parallelism.[^37] [^38]

On 14 April 2023,[^39] High-Flyer announced the launch of an [artificial general intelligence](https://en.wikipedia.org/wiki/Artificial_general_intelligence "Artificial general intelligence") (AGI) research lab, stating that the new lab would focus on developing AI tools unrelated to the firm's financial business.[^40] [^41] Two months later, on 17 July 2023,[^7] that lab was spun off into an independent company, DeepSeek, with High-Flyer as its principal investor and backer.[^33] [^42] [^41] [Venture capital](https://en.wikipedia.org/wiki/Venture_capital "Venture capital") investors were reluctant to provide funding, as they considered it unlikely that the venture would be able to quickly generate an " [exit](https://en.wiktionary.org/wiki/exit "wikt:exit") ".[^33]

### Model releases (2023–present)

DeepSeek released its first model, DeepSeek Coder, on 2 November 2023, followed by the DeepSeek-LLM series on 29 November 2023.[^43]<sup><span title="Location: section 5">: section 5</span> </sup> In January 2024, it released two DeepSeek-MoE models (Base and Chat),[^44] and in April 3 DeepSeek-Math models (Base, Instruct, and RL).[^45]

DeepSeek-V2 was released in May 2024, followed a month later by the DeepSeek-Coder V2 series.[^46] In September 2024, DeepSeek V2.5 was introduced and revised in December.[^47] On 20 November 2024, the preview of DeepSeek-R1-Lite became available via chat.[^48] [^49] In December, DeepSeek-V3-Base and DeepSeek-V3 (chat) were released.[^37]

![](https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Deepseek_login_error.png/250px-Deepseek_login_error.png)

The DeepSeek login page following a cyberattack around its 21 January 2025 launch

On 20 January 2025, DeepSeek launched the [DeepSeek chatbot](https://en.wikipedia.org/wiki/DeepSeek_\(chatbot\) "DeepSeek (chatbot)") —based on the DeepSeek-R1 model—free for [iOS](https://en.wikipedia.org/wiki/IOS "IOS") and [Android](https://en.wikipedia.org/wiki/Android_\(operating_system\) "Android (operating system)"). By 27 January, DeepSeek surpassed [ChatGPT](https://en.wikipedia.org/wiki/ChatGPT "ChatGPT") as the most downloaded freeware app on the [iOS App Store](https://en.wikipedia.org/wiki/App_Store_\(iOS\) "App Store (iOS)") in the United States,[^20] triggering an 18% drop in Nvidia's share price.[^50] [^51]

On 24 March 2025, DeepSeek released DeepSeek-V3-0324 under the MIT License.[^52] [^53]

On 28 May 2025, DeepSeek released DeepSeek-R1-0528 under the MIT License.[^54] The model has been noted for more tightly following official [Chinese Communist Party ideology](https://en.wikipedia.org/wiki/Ideology_of_the_Chinese_Communist_Party "Ideology of the Chinese Communist Party") and [censorship](https://en.wikipedia.org/wiki/Censorship_in_China "Censorship in China") in its answers to questions than prior models.[^55]

On 21 August 2025, DeepSeek released DeepSeek V3.1 under the MIT License.[^56] This model features a hybrid architecture with thinking and non-thinking modes. It also surpasses prior models like V3 and R1, by over 40% on certain benchmarks like SWE-bench and Terminal-bench.[^57] It was updated to V3.1-Terminus on 22 September 2025.[^58] V3.2-Exp was released on 29 September 2025. It uses DeepSeek Sparse Attention, a more efficient [attention mechanism](https://en.wikipedia.org/wiki/Transformer_\(deep_learning_architecture\)#Sub-quadratic_transformers "Transformer (deep learning architecture)") based on previous research published in February.[^59] [^60] DeepSeek-V3.2 was released on 1 December 2025, alongside a DeepSeek-V3.2-Speciale variant that focused on reasoning.[^61] [^62]

In February 2026, [Anthropic](https://en.wikipedia.org/wiki/Anthropic "Anthropic") accused DeepSeek of using thousands of fraudulent accounts to generate millions of conversations with [Claude](https://en.wikipedia.org/wiki/Claude_\(language_model\) "Claude (language model)") to train its own large language models.[^63]

It was announced in February 2026 that Deepseek will release its latest AI model which was trained on Nvidia’s most advanced AI chip as soon as March 2026.[^64]

## Company operation

DeepSeek is headquartered in Hangzhou, Zhejiang, and is owned and funded by [High-Flyer](https://en.wikipedia.org/wiki/High-Flyer "High-Flyer"). Its co-founder, [Liang Wenfeng](https://en.wikipedia.org/wiki/Liang_Wenfeng "Liang Wenfeng"), serves as CEO. As of May 2024, Liang personally held an 84% stake in DeepSeek through two [shell corporations](https://en.wikipedia.org/wiki/Shell_corporation "Shell corporation").[^3] [^65]

### Strategy

DeepSeek has stated that it focuses on research and does not have immediate plans for commercialization.[^66] This posture also means it can skirt certain provisions of China's AI regulations aimed at consumer-facing technologies.[^18]

DeepSeek's hiring approach emphasizes skills over lengthy work experience, resulting in many hires fresh out of university.[^41] [^18] The company likewise recruits individuals without computer science backgrounds to expand the range of expertise incorporated into the models, for instance in poetry or advanced mathematics.[^20] [^18] According to *[The New York Times](https://en.wikipedia.org/wiki/The_New_York_Times "The New York Times")*, dozens of DeepSeek researchers have or have previously had affiliations with [People's Liberation Army](https://en.wikipedia.org/wiki/People%27s_Liberation_Army "People's Liberation Army") laboratories and the [Seven Sons of National Defence](https://en.wikipedia.org/wiki/Seven_Sons_of_National_Defence "Seven Sons of National Defence").[^67]

Due to the impact of United States restrictions on chips, DeepSeek refined its algorithms to maximise computational efficiency and thereby leveraged older hardware and reduced energy consumption.[^68]<sup><span title="Page: 19">: 19</span></sup>

DeepSeek also expanded on the African continent as it offers more affordable and less power-hungry AI solutions. The company has bolstered African language models and generated a number of startups, for example in [Nairobi](https://en.wikipedia.org/wiki/Nairobi "Nairobi"). Along with [Huawei](https://en.wikipedia.org/wiki/Huawei "Huawei") 's storage and cloud computing services, the impact on the tech scene in sub-saharan Africa is considerable. DeepSeek offers local data sovereignty and more flexibility compared to Western AI platforms.[^69]

## Training framework

High-Flyer/DeepSeek had operated at least two primary computing clusters: Fire-Flyer (萤火一号) and Fire-Flyer 2 (萤火二号). Fire-Flyer 1 was constructed in 2019 and was retired after 1.5 years of operation. Fire-Flyer 2 is still in operation as of 2025. Fire-Flyer 2 consists of co-designed software and hardware architecture. On the hardware side, Nvidia GPUs use 200 [Gbps](https://en.wikipedia.org/wiki/Data-rate_units "Data-rate units") interconnects. The cluster is divided into two "zones", and the platform supports cross-zone tasks. The network topology was two [fat trees](https://en.wikipedia.org/wiki/Fat_tree "Fat tree"), chosen for high [bisection bandwidth](https://en.wikipedia.org/wiki/Bisection_bandwidth "Bisection bandwidth"). On the software side are:[^38] [^32]

- `3FS` (Fire-Flyer File System): A [distributed parallel file system](https://en.wikipedia.org/wiki/Clustered_file_system "Clustered file system"), specifically designed for asynchronous random reads. It uses Direct I/O and [RDMA Read](https://en.wikipedia.org/wiki/Remote_direct_memory_access "Remote direct memory access"). In contrast to standard Buffered I/O, Direct I/O does not cache data. Caching is useless in this case, since each piece of data read is random and is not reused.[^70] [^71]
- `hfreduce`: Library for asynchronous communication, originally designed to replace Nvidia Collective Communication Library (NCCL).[^36] It is mainly used for [allreduce](https://en.wikipedia.org/wiki/Allreduce "Allreduce"), especially of gradients during [backpropagation](https://en.wikipedia.org/wiki/Backpropagation "Backpropagation"). It is asynchronously run on the CPU to avoid blocking [kernels](https://en.wikipedia.org/wiki/Compute_kernel "Compute kernel") on the GPU.[^38] It uses [two-tree broadcast](https://en.wikipedia.org/wiki/Two-tree_broadcast "Two-tree broadcast") like NCCL.[^36]
- `hfai.nn`: Software library of commonly used operators for neural network training, similar to `torch.nn` in [PyTorch](https://en.wikipedia.org/wiki/PyTorch "PyTorch").
- `HaiScale Distributed Data Parallel` (DDP): Parallel training library that implements various forms of parallelism such as [Data Parallelism](https://en.wikipedia.org/wiki/Data_parallelism "Data parallelism") (DP), [Pipeline Parallelism](https://en.wikipedia.org/wiki/Pipeline_\(computing\) "Pipeline (computing)") (PP), Tensor Parallelism (TP), Experts Parallelism (EP), Fully Sharded Data Parallel (FSDP) and Zero Redundancy Optimizer (ZeRO). It is similar to PyTorch DDP, which uses NCCL on the backend.
- `HAI Platform`: Various applications such as task scheduling, fault handling, and disaster recovery.[^72]

As of 2022, Fire-Flyer 2 had 5,000 [PCIe](https://en.wikipedia.org/wiki/PCI_Express "PCI Express") A100 GPUs in 625 nodes, each containing 8 GPUs.[^36] It later incorporated NVLinks and NCCL to train larger models that required model parallelism.[^37] [^38]

## Development and release history

<table><caption>Major versions of DeepSeek models. SFT stands for supervised finetuning.</caption><tbody><tr><th>Major versions</th><th>Release date</th><th>Status</th><th>Major variants</th><th>License</th><th>Remarks</th></tr><tr><td>DeepSeek-Coder</td><td>November 2, 2023</td><td>Discontinued</td><td>Base (pretrained)<br>Instruct (with instruction-finetuned)</td><td rowspan="10"><a href="https://en.wikipedia.org/wiki/Source-available">Source-available</a> (DeepSeek)</td><td>The architecture is essentially the same as Llama.<sup><a href="#fn:73">73</a></sup></td></tr><tr><td>DeepSeek-LLM</td><td>November 29, 2023</td><td>Discontinued</td><td>Base<br>Chat (with SFT)</td><td>The architecture is essentially the same as Llama.<sup><a href="#fn:74">74</a></sup></td></tr><tr><td>DeepSeek-MoE</td><td>January 9, 2024</td><td>Discontinued</td><td>Base<br>Chat</td><td>Developed a variant of <a href="https://en.wikipedia.org/wiki/Mixture_of_experts">mixture of experts</a> (MoE).<sup><a href="#fn:75">75</a></sup></td></tr><tr><td rowspan="3">DeepSeek-Math</td><td rowspan="3">April 2024</td><td rowspan="3">Discontinued</td><td>Base</td><td>Initialized with DS-Coder-Base-v1.5 <sup><a href="#fn:76">76</a></sup></td></tr><tr><td>Instruct (with SFT)</td><td><sup><a href="#fn:77">77</a></sup></td></tr><tr><td>RL (using a process reward model)</td><td>Developed <a href="https://en.wikipedia.org/wiki/Group_Relative_Policy_Optimization">Group Relative Policy Optimization</a> (GRPO), a variant of <a href="https://en.wikipedia.org/wiki/Proximal_Policy_Optimization">Proximal Policy Optimization</a> (PPO).<sup><a href="#fn:78">78</a></sup></td></tr><tr><td>DeepSeek-V2</td><td>May 2024</td><td>Discontinued</td><td>DeepSeek-V2, DeepSeek-V2-Chat<br>DeepSeek-V2-Lite, DeepSeek-V2-Lite-Chat<br>DeepSeek-Coder-V2<br>DeepSeek-V2.5</td><td>Developed multi-head latent attention (MLA). Also used mixture of experts (MoE). Implemented KV caching.<sup><a href="#fn:79">79</a></sup></td></tr><tr><td>DeepSeek-V3</td><td>December 2024</td><td>Active</td><td>DeepSeek-V3-Base<br>DeepSeek-V3 (a chat model)</td><td>The architecture is essentially the same as V2. Updated on 2025-03-24.<sup><a href="#fn:80">80</a></sup></td></tr><tr><td>DeepSeek-Prover-V2</td><td>May 1, 2025</td><td>Active</td><td>DeepSeek-Prover-V2-671B<br>DeepSeek-Prover-V2-7B</td><td><sup><a href="#fn:81">81</a></sup></td></tr><tr><td>DeepSeek-VL2</td><td>December 13, 2024</td><td>Active</td><td></td><td><sup><a href="#fn:82">82</a></sup></td></tr><tr><td rowspan="4">DeepSeek-R1</td><td>November 20, 2024</td><td>Active</td><td>DeepSeek-R1-Lite-Preview</td><td><a href="https://en.wikipedia.org/wiki/Proprietary_software">Proprietary</a></td><td>Preview version, only accessed through API and a chat interface.</td></tr><tr><td rowspan="2">January 20, 2025</td><td rowspan="2">Active</td><td>DeepSeek-R1<br>DeepSeek-R1-Zero<br>DeepSeek-R1-0528</td><td rowspan="5"><a href="https://en.wikipedia.org/wiki/MIT_License">MIT</a></td><td>Initialized from DeepSeek-V3-Base and sharing the V3 architecture.<sup><a href="#fn:83">83</a></sup></td></tr><tr><td>Distilled models</td><td>Initialized from other models, such as Llama, Qwen, etc. Distilled from data synthesized by R1 and R1-Zero.<sup><a href="#fn:84">84</a></sup> <sup><a href="#fn:85">85</a></sup></td></tr><tr><td>May 28, 2025</td><td>Active</td><td>DeepSeek-R1-0528</td><td></td></tr><tr><td rowspan="2">DeepSeek-V3.1</td><td>August 21, 2025</td><td>Active</td><td>DeepSeek-V3.1-Base<br>DeepSeek-V3.1 (a chat model)</td><td>Hybrid architecture (thinking and non-thinking modes available). Trained on over 800B additional tokens on top of V3.<sup><a href="#fn:86">86</a></sup></td></tr><tr><td>September 22, 2025</td><td>Active</td><td>DeepSeek-V3.1-Terminus</td><td>Reducing instances of mixed Chinese-English text and occasional abnormal characters on top of V3.1.<sup><a href="#fn:87">87</a></sup></td></tr><tr><td>DeepSeek-Math-V2</td><td>November 27, 2025</td><td>Active</td><td></td><td><a href="https://en.wikipedia.org/wiki/Apache_2.0">Apache 2.0</a></td><td><sup><a href="#fn:88">88</a></sup></td></tr><tr><td>DeepSeek-V3.2</td><td>December 1, 2025</td><td>Active</td><td>DeepSeek-V3.2<br>DeepSeek-V3.2-Speciale</td><td><a href="https://en.wikipedia.org/wiki/MIT_License">MIT</a></td><td><sup><a href="#fn:61">61</a></sup> <sup><a href="#fn:62">62</a></sup> <sup><a href="#fn:89">89</a></sup></td></tr></tbody></table>

The first DeepSeek models were essentially the same as Llama,[^43] which were dense decoder-only [transformers](https://en.wikipedia.org/wiki/Transformer_\(deep_learning_architecture\) "Transformer (deep learning architecture)"). Later models incorporated the multi-head latent attention (MLA), Mixture of Experts (MoE), and KV caching.[^44] [^46]

A [decoder-only transformer](https://en.wikipedia.org/wiki/Transformer_\(deep_learning_architecture\)#decoder-only "Transformer (deep learning architecture)") consists of multiple identical decoder layers. Each of these layers features two main components: an attention layer and a [feedforward network](https://en.wikipedia.org/wiki/Feedforward_neural_network "Feedforward neural network") (FFN) layer.[^46] V2 replaced the standard [multi-head attention mechanism](https://en.wikipedia.org/wiki/Transformer_\(deep_learning_architecture\)#MHA "Transformer (deep learning architecture)") (MHA) with [multi-head latent attention](https://en.wikipedia.org/wiki/Transformer_\(deep_learning_architecture\)#MLA "Transformer (deep learning architecture)") (MLA). This introduces compressed latent vectors to reduce [KV (key–value) cache size](https://en.wikipedia.org/wiki/Transformer_\(deep_learning_architecture\)#KV_caching "Transformer (deep learning architecture)"), and thus memory usage.[^46]

A standard MoE Transformer generally use the [sparsely-gated MoE](https://en.wikipedia.org/wiki/Mixture_of_experts#Sparsely-gated_MoE_layer "Mixture of experts") layers in the FFN layers. In such an MoE layer, there are several FFN modules in parallel ("routed experts") and a small classifier ("gate") to compute a score for all these modules upon each token. Only the highest-scoring modules are activated. Starting with DeepSeekMoE, DeepSeek adopted a variant that adds "shared experts", which are always activated.[^44]

## Overview of models and technical specifications

DeepSeek's models are "open weight", which provides less freedom for modification than true [open source](https://en.wikipedia.org/wiki/Open_source "Open source") software.[^22] [^16]

### DeepSeek Coder

DeepSeek Coder is a series of eight models, four pretrained (`Base`) and four instruction-finetuned (`Instruct`). All have 16K context lengths. The model was made [source-available](https://en.wikipedia.org/wiki/Source-available "Source-available") under the DeepSeek License, which includes "open and responsible downstream usage" restrictions.[^90]

The [training](https://en.wikipedia.org/wiki/Training,_validation,_and_test_data_sets "Training, validation, and test data sets") program was:[^91] [^92] [^93]

1. Pretraining: 1.8T tokens (87% source code, 10% code-related English (GitHub markdown and [Stack Exchange](https://en.wikipedia.org/wiki/Stack_Exchange "Stack Exchange")), and 3% code-unrelated Chinese).
2. Long-context pretraining: 200B tokens. This extends the context length from 4K to 16K. This produced the `Base` models.
3. Supervised [finetuning](https://en.wikipedia.org/wiki/Fine-tuning_\(deep_learning\) "Fine-tuning (deep learning)") (SFT): 2B tokens of instruction data. This produced the `Instruct` models.

They were trained on clusters of A100 and [H800](https://en.wikipedia.org/wiki/Hopper_\(microarchitecture\) "Hopper (microarchitecture)") Nvidia GPUs, connected by [InfiniBand](https://en.wikipedia.org/wiki/InfiniBand "InfiniBand"), [NVLink](https://en.wikipedia.org/wiki/NVLink "NVLink"), [NVSwitch](https://en.wikipedia.org/wiki/NVSwitch "NVSwitch").[^91]

| Params. | # Layers | Model dim. | Intermediate dim. | \# Heads | \# Kv-heads |
| --- | --- | --- | --- | --- | --- |
| 1.3B | 24 | 2048 | 5504 | 16 | 16 |
| 5.7B | 32 | 4096 | 11008 | 32 | 1 [^4] |
| 6.7B | 32 | 4096 | 11008 | 32 | 32 |
| 33B | 62 | 7168 | 19200 | 56 | 7 [^4] |

### DeepSeek-LLM

The DeepSeek-LLM series was released in November 2023. It has 7B and 67B parameters in both Base and Chat forms. DeepSeek's accompanying paper claimed benchmark results higher than [Llama 2](https://en.wikipedia.org/wiki/Llama_2 "Llama 2") and most open-source LLMs at the time.[^43]<sup><span title="Location: section 5">: section 5</span> </sup> The model code is under the source-available DeepSeek License.[^95]

The architecture was essentially the same as the [Llama](https://en.wikipedia.org/wiki/Llama_\(language_model\) "Llama (language model)") series. They used the [pre-norm](https://en.wikipedia.org/wiki/Transformer_\(deep_learning_architecture\)#pre-LN "Transformer (deep learning architecture)") [decoder-only Transformer](https://en.wikipedia.org/wiki/Transformer_\(deep_learning_architecture\)#decoder-only "Transformer (deep learning architecture)") with [RMSNorm](https://en.wikipedia.org/wiki/RMSNorm "RMSNorm") as the normalization, [SwiGLU](https://en.wikipedia.org/wiki/SwiGLU "SwiGLU") in the feedforward layers, [rotary positional embedding](https://en.wikipedia.org/wiki/Rotary_positional_embedding "Rotary positional embedding") (RoPE), and [grouped-query attention](https://en.wikipedia.org/wiki/Grouped-query_attention "Grouped-query attention") (GQA). Both had vocabulary size 102,400 ([byte-level BPE](https://en.wikipedia.org/wiki/Byte_pair_encoding#Byte-level_BPE "Byte pair encoding")) and context length of 4096. They trained on 2 trillion tokens of English and Chinese text obtained by deduplicating the [Common Crawl](https://en.wikipedia.org/wiki/Common_Crawl "Common Crawl").[^43]

| Params. | \# Layers | Model dim. | Intermediate dim. | \# Heads | \# Kv-heads |
| --- | --- | --- | --- | --- | --- |
| 7B | 30 | 4096 | 11008 | 32 | 32 |
| 67B | 95 | 8192 | 22016 | 64 | 8 [^4] |

The Chat versions of the two Base models was released concurrently, obtained by training Base by [supervised finetuning (SFT) followed by direct policy optimization (DPO)](https://en.wikipedia.org/wiki/Reinforcement_learning_from_human_feedback "Reinforcement learning from human feedback").[^43]

#### MoE

DeepSeek-MoE models (Base and Chat), each have 16B parameters (2.7B activated per token, 4K context length). The training was essentially the same as DeepSeek-LLM 7B, and was trained on a part of its training dataset. They claimed performance comparable to a 16B MoE as a 7B non-MoE. It is a variant of the standard [sparsely-gated MoE](https://en.wikipedia.org/wiki/Mixture_of_experts#Sparsely-gated_MoE_layer "Mixture of experts"), with "shared experts" that are always queried, and "routed experts" that might not be. They found this to help with expert balancing. In standard MoE, some experts can become overused, while others are rarely used, wasting space. Attempting to balance expert usage causes experts to replicate the same capacity. They proposed the shared experts to learn core capacities that are often used, and let the routed experts learn peripheral capacities that are rarely used.[^44]

#### Math

DeepSeek-Math includes 3 models: Base, Instruct, and RL. Math was trained as follows:[^45]

1. Initialize with a previously pretrained DeepSeek-Coder Base v1.5 7B.
2. Further pretrain with 500B tokens (6% DeepSeekMath Corpus, 4% AlgebraicStack, 10% arXiv, 20% GitHub code, 10% Common Crawl). This produced Base.
3. Train an instruction-following model by SFT Base with 776K math problems and tool-use-integrated step-by-step solutions. This produced Instruct.
4. [Reinforcement learning](https://en.wikipedia.org/wiki/Reinforcement_learning "Reinforcement learning") (RL): The reward model was a [process reward model](https://en.wikipedia.org/wiki/Reasoning_language_model#PRM "Reasoning language model") (PRM) trained from Base according to the Math-Shepherd method.[^96] This reward model was then used to train Instruct using [Group Relative Policy Optimization](https://en.wikipedia.org/wiki/Group_Relative_Policy_Optimization "Group Relative Policy Optimization") (GRPO) on a dataset of 144K math questions "related to [GSM8K and MATH](https://en.wikipedia.org/wiki/Language_model_benchmark "Language model benchmark") ". The reward model was continuously updated during training to avoid reward hacking. This resulted in RL.

### V2

![](https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/DeepSeek_MoE_and_MLA_%28DeepSeek-V2%29.svg/500px-DeepSeek_MoE_and_MLA_%28DeepSeek-V2%29.svg.png)

The architecture of V2, showing both shared-routed MoE and MLA 97: Figure 2

In May 2024, DeepSeek released the DeepSeek-V2 series. The series includes 4 models, 2 base models (DeepSeek-V2, DeepSeek-V2 Lite) and 2 chatbots (Chat). The two larger models were trained as follows:[^97]

1. Pretrain on a dataset of 8.1T tokens, using 12% more Chinese tokens than English ones.
2. Extend context length from 4K to 128K using YaRN.[^98] This resulted in DeepSeek-V2.
3. SFT with 1.2M instances for helpfulness and 0.3M for safety. This resulted in Chat SFT, which was not released.
4. RL using GRPO in two stages. The first stage was trained to solve math and coding problems. This stage used 1 reward model, trained on compiler feedback (for coding) and ground-truth labels (for math). The second stage was trained to be helpful, safe, and follow rules. This stage used 3 reward models. The helpfulness and safety reward models were trained on human preference data. The rule-based reward model was manually programmed. All trained reward models were initialized from Chat (SFT). This resulted in the released version of Chat.

They opted for 2-staged RL, because they found that RL on reasoning data had "unique characteristics" different from RL on general data. For example, RL on reasoning could improve over more training steps.[^97]

The two V2-Lite models were smaller, and trained similarly. DeepSeek-V2 Lite-Chat underwent only SFT, not RL. They trained the Lite version to help "further research and development on MLA and DeepSeekMoE".[^97]

Architecturally, the V2 models were significantly different from the DeepSeek LLM series. They changed the standard attention mechanism by a [low-rank approximation](https://en.wikipedia.org/wiki/Low-rank_approximation "Low-rank approximation") called [multi-head latent attention](https://en.wikipedia.org/wiki/Transformer_\(deep_learning_architecture\)#MLA "Transformer (deep learning architecture)") (MLA), and used the previously published [mixture of experts](https://en.wikipedia.org/wiki/Mixture_of_experts "Mixture of experts") (MoE) variant.[^44]

| Name | Params. | Active params | \# Layers | Context length | \# Shared experts | \# Routed experts |
| --- | --- | --- | --- | --- | --- | --- |
| V2-Lite | 15.7B | 2.4B | 27 | 32K | 2 | 64 |
| V2 | 236B | 21B | 60 | 128K | 2 | 160 |

The *[Financial Times](https://en.wikipedia.org/wiki/Financial_Times "Financial Times")* reported that it was cheaper than its peers with a price of 2 [RMB](https://en.wikipedia.org/wiki/Renminbi "Renminbi") for every million output tokens. The [University of Waterloo](https://en.wikipedia.org/wiki/University_of_Waterloo "University of Waterloo") Tiger Lab's leaderboard ranked DeepSeek-V2 seventh on its LLM ranking.[^42]

The DeepSeek-Coder V2 series included V2-Base, V2-Lite-Base, V2-Instruct, and V20-Lite-Instruct.. Training:[^46] [^5]

1. Base models were initialized from corresponding intermediate checkpoints after pretraining on 4.2T tokens (not the version at the end of pretraining), then pretrained further for 6T tokens, then context-extended to 128K context length.
2. DeepSeek-Coder and DeepSeek-Math were used to generate 20K code-related and 30K math-related instruction data, then combined with an instruction dataset of 300M tokens. This was used for SFT.
3. RL with GRPO. The reward for math problems was computed by comparing with the ground-truth label. The reward for code problems was generated by a reward model trained to predict whether a program would pass the unit tests.

DeepSeek-V2.5 was made by combining DeepSeek-V2-Chat and DeepSeek-Coder-V2-Instruct.[^47]

### V3

![](https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Multi-Token_Prediction_%28DeepSeek%29_01.svg/500px-Multi-Token_Prediction_%28DeepSeek%29_01.svg.png)

Multi-token prediction

DeepSeek-V3-Base and DeepSeek-V3 (a chat model) use essentially the same architecture as V2 with the addition of [multi-token prediction](https://en.wikipedia.org/wiki/Transformer_\(deep_learning_architecture\)#Multi-Token_Prediction "Transformer (deep learning architecture)"), which (optionally) decodes extra tokens faster but less accurately. Training process:[^37]

1. Pretraining on 14.8T tokens of a multilingual corpus, mostly English and Chinese. It contained a higher ratio of math and programming than the pretraining dataset of V2.
2. Extend context length twice, from 4K to 32K and then to 128K, using YaRN.[^98] This produced DeepSeek-V3-Base.
3. SFT for 2 epochs on 1.5M samples of reasoning (math, programming, logic) and non-reasoning (creative writing, roleplay, simple question answering) data. Reasoning data was generated by "expert models". Non-reasoning data was generated by DeepSeek-V2.5 and checked by humans.
	- The "expert models" were trained by starting with an unspecified base model, then SFT on both <problem, original response> data, and synthetic <system prompt, prompt, problem, R1 response> data generated by an internal DeepSeek-R1-Lite model. The system prompt asked R1 to reflect and verify during thinking. Then the expert models were RL using an undisclosed reward function.
		- Each expert model was trained to generate just synthetic reasoning data in one specific domain (math, programming, logic).
		- Expert models were used instead of R1 itself, since the output from R1 itself suffered "overthinking, poor formatting, and excessive length".
4. Model-based reward models were made by starting with a SFT checkpoint of V3, then finetuning on human preference data containing both final reward and chain-of-thought leading to the final reward. The reward model produced reward signals for both questions with objective but free-form answers, and questions without objective answers (such as creative writing).
5. An SFT checkpoint of V3 was trained by GRPO using both reward models and rule-based reward. The rule-based reward was computed for math problems with a final answer (put in a box), and for programming problems by unit tests. This produced DeepSeek-V3.

DeepSeek released its DeepSeek-V3-0324 model, which used the same architecture as V3, on 24 March 2025 under the MIT License.[^101]

| Name | Params. | Active params | \# Layers | Context length | \# Shared experts | \# Routed experts |
| --- | --- | --- | --- | --- | --- | --- |
| V3 | 671B | 37B | 61 | 128K | 1 | 256 |

![](https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Mixed-precision_training_in_DeepSeek_V3.svg/500px-Mixed-precision_training_in_DeepSeek_V3.svg.png)

Mixed-precision framework for V3 37: Figure 6

The DeepSeek team performed extensive low-level engineering to improve efficiency. They used [mixed-precision arithmetic](https://en.wikipedia.org/wiki/Mixed-precision_arithmetic "Mixed-precision arithmetic"). Much of the forward pass was performed in [8-bit floating point numbers](https://en.wikipedia.org/wiki/Floating-point_arithmetic "Floating-point arithmetic") (5E2M: 5-bit exponent and 2-bit [mantissa](https://en.wikipedia.org/wiki/Mantissa_\(floating_point_number\) "Mantissa (floating point number)")) rather than the standard [32-bit](https://en.wikipedia.org/wiki/Single-precision_floating-point_format "Single-precision floating-point format"), requiring special [GEMM](https://en.wikipedia.org/wiki/General_matrix_multiply "General matrix multiply") routines to accumulate accurately. They used a custom 12-bit float (E5M6) only for the inputs to the linear layers after the attention modules. Optimizer states were in 16-bit ([BF16](https://en.wikipedia.org/wiki/Bfloat16_floating-point_format "Bfloat16 floating-point format")). They minimized communication latency by extensively overlapping computation and communication, such as dedicating 20 streaming multiprocessors out of 132 per H800 for only inter-GPU communication. They lowered communication by rearranging (every 10 minutes) the exact machine each expert was on so as to avoid querying certain machines more often than others, adding auxiliary load-balancing losses to the training loss function, and other load-balancing techniques.[^37]

After training, it was deployed on clusters of H800 GPUs. The 8 H800 GPUs within a cluster were connected by NVLink, and the clusters were connected by InfiniBand.[^37]

| Stage | Cost (in one thousand GPU hours) | Cost (in one million US$) |
| --- | --- | --- |
| Pre-training | 2,664 | 5.328 |
| Context extension | 119 | 0.24 |
| Fine-tuning | 5 | 0.01 |
| Total | 2,788 | 5.576 |

The cost has been discussed [^103] [^104] [^105] and called misleading, because it covers only parts of the true cost.[^106]

Benchmark tests show that V3 outperformed [Llama](https://en.wikipedia.org/wiki/Llama_\(language_model\) "Llama (language model)") 3.1 and [Qwen](https://en.wikipedia.org/wiki/Qwen "Qwen") 2.5 while matching [GPT-4o](https://en.wikipedia.org/wiki/GPT-4o "GPT-4o") and [Claude](https://en.wikipedia.org/wiki/Claude_\(language_model\) "Claude (language model)") 3.5 Sonnet.[^41] [^107] [^108] [^109]

### R1

![](https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/The_multistage_pipeline_of_DeepSeek-R1.png/250px-The_multistage_pipeline_of_DeepSeek-R1.png)

The multistage training pipeline of DeepSeek-R1

In January 2025, DeepSeek released the DeepSeek-R1 model under the [MIT License](https://en.wikipedia.org/wiki/MIT_License "MIT License").[^110]

DeepSeek-R1-Lite-Preview [^48] [^49] [^6] was trained for logical inference, mathematical reasoning, and real-time problem-solving. DeepSeek claimed that it exceeded performance of [OpenAI o1](https://en.wikipedia.org/wiki/OpenAI_o1 "OpenAI o1") on benchmarks such as [American Invitational Mathematics Examination](https://en.wikipedia.org/wiki/American_Invitational_Mathematics_Examination "American Invitational Mathematics Examination") (AIME) and MATH.[^111] However, *[The Wall Street Journal](https://en.wikipedia.org/wiki/The_Wall_Street_Journal "The Wall Street Journal")* reported that on 15 problems from the 2024 edition of AIME, the o1 model reached a solution faster.[^112]

DeepSeek-R1 and DeepSeek-R1-Zero [^113] were initialized from DeepSeek-V3-Base and share its architecture. DeepSeek-R1-Distill models were instead initialized from other pretrained open-weight models, including [LLaMA](https://en.wikipedia.org/wiki/Llama_\(language_model\) "Llama (language model)") and [Qwen](https://en.wikipedia.org/wiki/Qwen "Qwen"), then fine-tuned on [synthetic data](https://en.wikipedia.org/wiki/Synthetic_data "Synthetic data") generated by R1.[^84]

Template for `DeepSeek-R1-Zero`

> A conversation between User and Assistant. The user asks a question, and the Assistant solves it. The assistant first thinks about the reasoning process in the mind and then provides the user with the answer. The reasoning process and answer are enclosed within <think> </think> and <answer> </answer> tags, respectively, i.e., <think> reasoning process here </think> <answer> answer here </answer>. User: <prompt>. Assistant:

— <prompt> is replaced with the specific reasoning question during training.

DeepSeek-R1-Zero was trained exclusively using GRPO RL without SFT. Unlike previous versions, it used no model-based reward. All reward functions were rule-based, "mainly" of two types (other types were not specified): accuracy rewards and format rewards. Accuracy reward was checking whether a boxed answer is correct (for math) or whether a code passes tests (for programming). Format reward was checking whether the model puts its thinking trace within a <think>...</think> tag.[^84]

R1-Zero has issues with readability and mixing languages. R1 was trained to address these issues and further improve reasoning:[^84]

1. SFT DeepSeek-V3-Base on "thousands" of "cold-start" data all with the standard format of `|special_token|<reasoning_process>|special_token|<summary>`, designed to improve model output readability.
2. Apply the same GRPO RL process as R1-Zero, adding a "language consistency reward" to encourage it to respond monolingually. This produced an un released internal model.
3. Synthesize 600K reasoning data from the internal model, with rejection sampling (i.e. if the generated reasoning had a wrong final answer, then it is removed). Synthesize 200K non-reasoning data (writing, factual QA, self-cognition, translation) using DeepSeek-V3.
4. SFT DeepSeek-V3-Base on the 800K synthetic data for 2 epochs.
5. Apply the same GRPO RL process as R1-Zero with rule-based reward (for reasoning tasks), but also model-based reward (for non-reasoning tasks, helpfulness, and harmlessness). This produced DeepSeek-R1.

Distilled models were trained by SFT on 800K data synthesized from DeepSeek-R1, in a similar way as step 3. They were not trained with RL.[^84]

There were reports that R2, the intended successor to R1, was originally planned for release in early May 2025.[^114] However, on 28 May 2025, R1 was instead updated to version R1-0528.[^115] As of early July, R2 was not yet released, as Liang Wenfeng was not yet satisfied with its performance. Most Chinese cloud providers of R1 used [Nvidia H20](https://en.wikipedia.org/wiki/Nvidia_H20_GPU "Nvidia H20 GPU").[^116] As of August, R2 was not yet released. Sources cite slow data labelling and chip problems. Specifically, DeepSeek was encouraged by authorities to adopt Huawei's Ascend chips for training, but it had stability issues, slower inter-chip connectivity and inferior software. Consequently, it has opted to use Nvidia chips for training and Huawei chips for inference.[^117] It is also reported that the [Cyberspace Administration of China](https://en.wikipedia.org/wiki/Cyberspace_Administration_of_China "Cyberspace Administration of China") requested several large corporations to stop buying Nvidia H20 and buy from domestic suppliers instead.[^118]

With the release of R1 in January 2025, the DeepSeek team published a preprint on arXiv.[^84] Later, an updated version was published in *[Nature](https://en.wikipedia.org/wiki/Nature_\(journal\) "Nature (journal)")* in September 2025.[^119]

## Significance

DeepSeek's success against larger and more established rivals was a surprise to both the industry and to markets,[^20] [^120] and has been compared by investors and pundits to the " [Sputnik moment](https://en.wikipedia.org/wiki/Sputnik_crisis "Sputnik crisis") ".[^20] [^121] [^122] [^28] [^27] [^26]

The DeepSeek-R1 model provides responses comparable to other contemporary large language models, such as [OpenAI](https://en.wikipedia.org/wiki/OpenAI "OpenAI") 's [GPT-4o](https://en.wikipedia.org/wiki/GPT-4o "GPT-4o") and [o1](https://en.wikipedia.org/wiki/OpenAI_o1 "OpenAI o1").[^16] Its [training](https://en.wikipedia.org/wiki/Training,_validation,_and_test_data_sets "Training, validation, and test data sets") cost is reported to be significantly lower than other LLMs.[^123] [^124]

The company claims that it trained V3, a predecessor of R1, for US$6 million compared to US$100 million for OpenAI's [GPT-4](https://en.wikipedia.org/wiki/GPT-4 "GPT-4") in 2023,[^17] and approximately one tenth of the computing power used for [Meta](https://en.wikipedia.org/wiki/Meta_Platforms "Meta Platforms") 's comparable model, [LLaMA 3.1](https://en.wikipedia.org/wiki/Llama_\(language_model\) "Llama (language model)").[^17] [^18] [^19]

After the January 2025 release of the R1 model, which offered significantly lower costs than competing models, some investors anticipated a [price war](https://en.wikipedia.org/wiki/Price_war "Price war") in the American AI industry.[^125] It was dubbed the " [Pinduoduo](https://en.wikipedia.org/wiki/Pinduoduo "Pinduoduo") of AI", and other Chinese tech giants such as [ByteDance](https://en.wikipedia.org/wiki/ByteDance "ByteDance"), [Tencent](https://en.wikipedia.org/wiki/Tencent "Tencent"), [Baidu](https://en.wikipedia.org/wiki/Baidu "Baidu"), and [Alibaba](https://en.wikipedia.org/wiki/Alibaba_Group "Alibaba Group") cut the price of their AI models. Despite its low price, it was profitable compared to its money-losing rivals.[^66]

[^1]: :. Sometimes simply referred to in English as.[^12]

[^2]: [Chinese](https://en.wikipedia.org/wiki/Simplified_Chinese_characters "Simplified Chinese characters"): 深度求索; [pinyin](https://en.wikipedia.org/wiki/Pinyin "Pinyin"): *Shēndù Qiúsuǒ*

[^3]: 宁波程信柔兆企业管理咨询合伙企业（有限合伙） and 宁波程恩企业管理咨询合伙企业（有限合伙）

[^4]: The number of heads does not equal the number of KV heads, due to GQA.

[^5]: Inexplicably, the model named `DeepSeek-Coder-V2 Chat` in the paper was released as `DeepSeek-Coder-V2-Instruct` in HuggingFace.

[^6]: At that time, the `R1-Lite-Preview` required selecting "Deep Think enabled", and every user could use it only 50 times a day.

[^7]: ["DeepSeek突传消息"](https://finance.sina.com.cn/jjxw/2025-02-01/doc-inehyqcx9694053.shtml). [Sina Corporation](https://en.wikipedia.org/wiki/Sina_Corporation "Sina Corporation"). 1 February 2025. Retrieved 1 February 2025.

[^8]: Wu, Zijing (14 March 2025). ["DeepSeek focuses on research over revenue in contrast to Silicon Valley"](https://www.ft.com/content/fb5c11bb-1d4b-465f-8283-451a19a3d425). *[Financial Times](https://en.wikipedia.org/wiki/Financial_Times "Financial Times")*. Retrieved 14 March 2025.

[^9]: ["Hangzhou DeepSeek Artificial Intelligence Basic Technology Research Co., Ltd"](https://www.bloomberg.com/profile/company/2544189D:CH). *[Bloomberg L.P.](https://en.wikipedia.org/wiki/Bloomberg_L.P. "Bloomberg L.P.")*

[^10]: ["DeepSeek Coder Model Service Agreement"](https://chat.deepseek.com/downloads/DeepSeek%20Coder%20Model%20Service%20Agreement_1019.pdf) (PDF), *DeepSeek*, 19 October 2023, [archived](https://web.archive.org/web/20250221091648/https://chat.deepseek.com/downloads/DeepSeek%20Coder%20Model%20Service%20Agreement_1019.pdf) (PDF) from the original on 21 February 2025, retrieved 11 February 2025

[^11]: ["DeepSeek Coder Privacy Policy"](https://web.archive.org/web/20250708080741/https://chat.deepseek.com/downloads/DeepSeek%20Coder%20Privacy%20Policy_1019.pdf) (PDF). *DeepSeek*. Archived from [the original](https://chat.deepseek.com/downloads/DeepSeek%20Coder%20Privacy%20Policy_1019.pdf) (PDF) on 8 July 2025. Retrieved 19 February 2025.

[^12]: ["全国互联网安全管理平台"](https://beian.mps.gov.cn/#/query/webSearch?code=33010502011812). *beian.mps.gov.cn* (in Chinese (China)). [Ministry of Public Security of the People's Republic of China](https://en.wikipedia.org/wiki/Ministry_of_Public_Security_\(China\) "Ministry of Public Security (China)"). [Archived](https://web.archive.org/web/20250209181351/https://beian.mps.gov.cn/#/query/webSearch?code=33010502011812) from the original on 9 February 2025. Retrieved 9 February 2025.

[^13]: Jiang, Ben (21 January 2025). ["Beijing puts spotlight on China's new face of AI, DeepSeek's Liang Wenfeng"](https://www.scmp.com/tech/policy/article/3295662/beijing-meeting-puts-spotlight-chinas-new-face-ai-deepseek-founder-liang-wenfeng). *[South China Morning Post](https://en.wikipedia.org/wiki/South_China_Morning_Post "South China Morning Post")*. [Archived](https://web.archive.org/web/20250121221843/https://www.scmp.com/tech/policy/article/3295662/beijing-meeting-puts-spotlight-chinas-new-face-ai-deepseek-founder-liang-wenfeng) from the original on 21 January 2025. Retrieved 4 March 2025.

[^14]: Baptista, Eduardo (28 January 2025). ["Who is Liang Wenfeng, the founder of DeepSeek?"](https://www.reuters.com/technology/deepseek-founder-liang-wenfeng-puts-focus-chinese-innovation-2025-01-28/). *[Reuters](https://en.wikipedia.org/wiki/Reuters "Reuters")*. [Archived](https://web.archive.org/web/20250219122827/https://www.reuters.com/technology/deepseek-founder-liang-wenfeng-puts-focus-chinese-innovation-2025-01-28/) from the original on 19 February 2025. Retrieved 4 March 2025.

[^15]: ["Behind DeepSeek lies a dazzling Chinese university"](https://www.economist.com/china/2025/02/19/behind-deepseek-lies-a-dazzling-chinese-university). *[The Economist](https://en.wikipedia.org/wiki/The_Economist "The Economist")*. [ISSN](https://en.wikipedia.org/wiki/ISSN_\(identifier\) "ISSN (identifier)") [0013-0613](https://search.worldcat.org/issn/0013-0613). Retrieved 5 March 2025.

[^16]: Gibney, Elizabeth (23 January 2025). ["China's cheap, open AI model DeepSeek thrills scientists"](https://www.nature.com/articles/d41586-025-00229-6). *[Nature](https://en.wikipedia.org/wiki/Nature_\(journal\) "Nature (journal)")*. **638** (8049): 13–14. [Bibcode](https://en.wikipedia.org/wiki/Bibcode_\(identifier\) "Bibcode (identifier)"):[2025Natur.638...13G](https://ui.adsabs.harvard.edu/abs/2025Natur.638...13G). [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1038/d41586-025-00229-6](https://doi.org/10.1038%2Fd41586-025-00229-6). [PMID](https://en.wikipedia.org/wiki/PMID_\(identifier\) "PMID (identifier)") [39849139](https://pubmed.ncbi.nlm.nih.gov/39849139). [Archived](https://web.archive.org/web/20250129122940/https://www.nature.com/articles/d41586-025-00229-6) from the original on 29 January 2025. Retrieved 12 February 2025.

[^17]: Vincent, James (28 January 2025). ["The DeepSeek panic reveals an AI world ready to blow"](https://www.theguardian.com/commentisfree/2025/jan/28/deepseek-r1-ai-world-chinese-chatbot-tech-world-western). *[The Guardian](https://en.wikipedia.org/wiki/The_Guardian "The Guardian")*.

[^18]: Metz, Cade; Tobin, Meaghan (23 January 2025). ["How Chinese A.I. Start-Up DeepSeek Is Competing With Silicon Valley Giants"](https://www.nytimes.com/2025/01/23/technology/deepseek-china-ai-chips.html). *[The New York Times](https://en.wikipedia.org/wiki/The_New_York_Times "The New York Times")*. [ISSN](https://en.wikipedia.org/wiki/ISSN_\(identifier\) "ISSN (identifier)") [0362-4331](https://search.worldcat.org/issn/0362-4331). [Archived](https://web.archive.org/web/20250123102900/https://www.nytimes.com/2025/01/23/technology/deepseek-china-ai-chips.html) from the original on 23 January 2025. Retrieved 27 January 2025.

[^19]: Cosgrove, Emma (27 January 2025). ["DeepSeek's cheaper models and weaker chips call into question trillions in AI infrastructure spending"](https://www.businessinsider.com/explaining-deepseek-chinese-models-efficiency-scaring-markets-2025-1). *[Business Insider](https://en.wikipedia.org/wiki/Business_Insider "Business Insider")*. [Archived](https://web.archive.org/web/20250129043218/https://www.businessinsider.com/explaining-deepseek-chinese-models-efficiency-scaring-markets-2025-1) from the original on 29 January 2025. Retrieved 27 January 2025.

[^20]: Metz, Cade (27 January 2025). ["What is DeepSeek? And How Is It Upending A.I.?"](https://www.nytimes.com/2025/01/27/technology/what-is-deepseek-china-ai.html). *[The New York Times](https://en.wikipedia.org/wiki/The_New_York_Times "The New York Times")*. [ISSN](https://en.wikipedia.org/wiki/ISSN_\(identifier\) "ISSN (identifier)") [0362-4331](https://search.worldcat.org/issn/0362-4331). [Archived](https://web.archive.org/web/20250127211403/https://www.nytimes.com/2025/01/27/technology/what-is-deepseek-china-ai.html) from the original on 27 January 2025. Retrieved 27 January 2025.

[^21]: Roose, Kevin (28 January 2025). ["Why DeepSeek Could Change What Silicon Valley Believes About A.I."](https://www.nytimes.com/2025/01/28/technology/why-deepseek-could-change-what-silicon-valley-believes-about-ai.html) *[The New York Times](https://en.wikipedia.org/wiki/The_New_York_Times "The New York Times")*. [ISSN](https://en.wikipedia.org/wiki/ISSN_\(identifier\) "ISSN (identifier)") [0362-4331](https://search.worldcat.org/issn/0362-4331). [Archived](https://web.archive.org/web/20250128131926/https://www.nytimes.com/2025/01/28/technology/why-deepseek-could-change-what-silicon-valley-believes-about-ai.html) from the original on 28 January 2025. Retrieved 28 January 2025.

[^22]: Delbert, Caroline (31 January 2025). ["DeepSeek Is Cracking the 'Black Box' of Corporate AI Wide Open"](https://www.popularmechanics.com/science/a63633889/deepseek-open-weight/). *[Popular Mechanics](https://en.wikipedia.org/wiki/Popular_Mechanics "Popular Mechanics")*. [Archived](https://web.archive.org/web/20250213051908/https://www.popularmechanics.com/science/a63633889/deepseek-open-weight/) from the original on 13 February 2025. Retrieved 12 February 2025.

[^23]: Chen, Caiwei (12 February 2026). ["What's next for Chinese open-source AI"](https://www.technologyreview.com/2026/02/12/1132811/whats-next-for-chinese-open-source-ai/). *[MIT Technology Review](https://en.wikipedia.org/wiki/MIT_Technology_Review "MIT Technology Review")*. Retrieved 12 April 2026.

[^24]: Metz, Cade (12 February 2025). ["How Did DeepSeek Build Its A.I. With Less Money?"](https://www.nytimes.com/2025/02/12/technology/deepseek-ai-chip-costs.html). *[The New York Times](https://en.wikipedia.org/wiki/The_New_York_Times "The New York Times")*. [Archived](https://web.archive.org/web/20250319114813/https://www.nytimes.com/2025/02/12/technology/deepseek-ai-chip-costs.html) from the original on 19 March 2025. Retrieved 21 March 2025.

[^25]: Allen, Gregory C. (7 March 2025). ["DeepSeek, Huawei, Export Controls, and the Future of the U.S.-China AI Race"](https://www.csis.org/analysis/deepseek-huawei-export-controls-and-future-us-china-ai-race). *Center for Strategic and International Studies*.

[^26]: Hawkins, Amy (28 January 2025). ["Who is behind DeepSeek and how did it achieve its AI 'Sputnik moment'?"](https://www.theguardian.com/technology/2025/jan/28/who-is-behind-deepseek-and-how-did-it-achieve-its-ai-sputnik-moment). *The Guardian*.

[^27]: Cassidy, John (3 February 2025). ["Is DeepSeek China's Sputnik Moment?"](https://www.newyorker.com/news/the-financial-page/is-deepseek-chinas-sputnik-moment). *The New Yorker* – via www.newyorker.com.

[^28]: Ruwitch, John (28 January 2025). ["DeepSeek: Did a little-known Chinese startup cause a 'Sputnik moment' for AI?"](https://www.npr.org/2025/01/28/g-s1-45061/deepseek-did-a-little-known-chinese-startup-cause-a-sputnik-moment-for-ai). *NPR*. Retrieved 2 August 2025.

[^29]: Saah, Jasper (13 February 2025). ["DeepSeek sends shock waves across Silicon Valley"](https://liberationnews.org/deepseek-sends-shock-waves-across-silicon-valley/). *[Liberation News – The Newspaper of the Party for Socialism and Liberation](https://en.wikipedia.org/wiki/Party_for_Socialism_and_Liberation "Party for Socialism and Liberation")*. [Archived](https://web.archive.org/web/20250217044644/https://liberationnews.org/deepseek-sends-shock-waves-across-silicon-valley/) from the original on 17 February 2025. Retrieved 13 February 2025.

[^30]: Sillars, James (28 January 2025). ["DeepSeek: Tech firm suffers biggest drop in US stock market history as low-cost Chinese AI company bites Silicon Valley"](https://news.sky.com/story/deepseek-us-tech-stocks-tumble-on-fears-of-cheaper-chinese-ai-13297788). *[Sky News](https://en.wikipedia.org/wiki/Sky_News "Sky News")*. Retrieved 13 February 2025.

[^31]: Chen, Caiwei (24 January 2025). ["How a top Chinese AI model overcame US sanctions"](https://www.technologyreview.com/2025/01/24/1110526/china-deepseek-top-ai-despite-sanctions/). *[MIT Technology Review](https://en.wikipedia.org/wiki/MIT_Technology_Review "MIT Technology Review")*. [Archived](https://web.archive.org/web/20250125180427/https://www.technologyreview.com/2025/01/24/1110526/china-deepseek-top-ai-despite-sanctions/) from the original on 25 January 2025. Retrieved 25 January 2025.

[^32]: ["幻方 | 幻方历程"](https://www.high-flyer.cn/history/). *[High-Flyer](https://en.wikipedia.org/wiki/High-Flyer "High-Flyer")* (in Chinese (China)). [Archived](https://web.archive.org/web/20250203125004/https://www.high-flyer.cn/history/) from the original on 3 February 2025. Retrieved 2 February 2025.

[^33]: Ottinger, Lily (9 December 2024). ["Deepseek: From Hedge Fund to Frontier Model Maker"](https://www.chinatalk.media/p/deepseek-from-hedge-fund-to-frontier). *ChinaTalk*. [Archived](https://web.archive.org/web/20241228030725/https://www.chinatalk.media/p/deepseek-from-hedge-fund-to-frontier) from the original on 28 December 2024. Retrieved 28 December 2024.

[^34]: Olcott, Eleanor; Wu, Zijing (24 January 2025). ["How small Chinese AI start-up DeepSeek shocked Silicon Valley"](https://www.ft.com/content/747a7b11-dcba-4aa5-8d25-403f56216d7e). *[Financial Times](https://en.wikipedia.org/wiki/Financial_Times "Financial Times")*. [Archived](https://web.archive.org/web/20250125094520/https://www.ft.com/content/747a7b11-dcba-4aa5-8d25-403f56216d7e) from the original on 25 January 2025. Retrieved 31 January 2025.

[^35]: Leswing, Kif (23 February 2023). ["Meet the $10,000 Nvidia chip powering the race for A.I."](https://www.cnbc.com/2023/02/23/nvidias-a100-is-the-10000-chip-powering-the-race-for-ai-.html) *[CNBC](https://en.wikipedia.org/wiki/CNBC "CNBC")*. [Archived](https://web.archive.org/web/20250129054857/https://www.cnbc.com/2023/02/23/nvidias-a100-is-the-10000-chip-powering-the-race-for-ai-.html) from the original on 29 January 2025. Retrieved 30 January 2025.

[^36]: ["hfreduce | 高性能的多卡并行通信工具"](https://www.high-flyer.cn/blog/hf-reduce/). *[High-Flyer](https://en.wikipedia.org/wiki/High-Flyer "High-Flyer")*. 4 March 2020. [Archived](https://web.archive.org/web/20250128032837/https://www.high-flyer.cn/blog/hf-reduce/) from the original on 28 January 2025. Retrieved 3 February 2025.

[^37]: DeepSeek-AI; Liu, Aixin; Feng, Bei; Xue, Bing; Wang, Bingxuan; Wu, Bochao; Lu, Chengda; Zhao, Chenggang; Deng, Chengqi (27 December 2024), *DeepSeek-V3 Technical Report*, [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2412.19437](https://arxiv.org/abs/2412.19437)

[^38]: An, Wei; Bi, Xiao; Chen, Guanting; Chen, Shanhuang; Deng, Chengqi; Ding, Honghui; Dong, Kai; Du, Qiushi; Gao, Wenjun; Guan, Kang; Guo, Jianzhong; Guo, Yongqiang; Fu, Zhe; He, Ying; Huang, Panpan (17 November 2024). "Fire-Flyer AI-HPC: A Cost-Effective Software-Hardware Co-Design for Deep Learning". *SC24: International Conference for High Performance Computing, Networking, Storage and Analysis*. IEEE. pp. 1–23. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2408.14158](https://arxiv.org/abs/2408.14158). [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1109/SC41406.2024.00089](https://doi.org/10.1109%2FSC41406.2024.00089). [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [979-8-3503-5291-7](https://en.wikipedia.org/wiki/Special:BookSources/979-8-3503-5291-7 "Special:BookSources/979-8-3503-5291-7").

[^39]: ["独家|幻方量化回应市场关注：AGI不是用来炒股的，"和金融没关系""](https://www.yicai.com/news/101732215.html). *[Yicai](https://en.wikipedia.org/wiki/China_Business_Network "China Business Network")*. Retrieved 3 February 2025.

[^40]: Yu, Xu (17 April 2023). ["\[Exclusive\] Chinese Quant Hedge Fund High-Flyer Won't Use AGI to Trade Stocks, MD Says"](https://www.yicaiglobal.com/news/exclusive-chinese-quant-fund-high-flyer-will-not-use-agi-to-trade-stocks-managing-director-says). *[Yicai Global](https://en.wikipedia.org/wiki/China_Business_Network "China Business Network")*. [Archived](https://web.archive.org/web/20231231030712/https://www.yicaiglobal.com/news/exclusive-chinese-quant-fund-high-flyer-will-not-use-agi-to-trade-stocks-managing-director-says) from the original on 31 December 2023. Retrieved 28 December 2024.

[^41]: Jiang, Ben; Perezi, Bien (1 January 2025). ["Meet DeepSeek: the Chinese start-up that is changing how AI models are trained"](https://www.scmp.com/tech/tech-trends/article/3293050/meet-deepseek-chinese-start-changing-how-ai-models-are-trained). *[South China Morning Post](https://en.wikipedia.org/wiki/South_China_Morning_Post "South China Morning Post")*. [Archived](https://web.archive.org/web/20250122160046/https://www.scmp.com/tech/tech-trends/article/3293050/meet-deepseek-chinese-start-changing-how-ai-models-are-trained) from the original on 22 January 2025. Retrieved 1 January 2025.

[^42]: McMorrow, Ryan; Olcott, Eleanor (9 June 2024). ["The Chinese quant fund-turned-AI pioneer"](https://www.ft.com/content/357f3c68-b866-4c2e-b678-0d075051a260). *[Financial Times](https://en.wikipedia.org/wiki/Financial_Times "Financial Times")*. [Archived](https://web.archive.org/web/20240717030903/https://www.ft.com/content/357f3c68-b866-4c2e-b678-0d075051a260) from the original on 17 July 2024. Retrieved 28 December 2024.

[^43]: DeepSeek-AI; Bi, Xiao; Chen, Deli; Chen, Guanting; Chen, Shanhuang; Dai, Damai; Deng, Chengqi; Ding, Honghui; Dong, Kai (5 January 2024), *DeepSeek LLM: Scaling Open-Source Language Models with Longtermism*, [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2401.02954](https://arxiv.org/abs/2401.02954)

[^44]: Dai, Damai; Deng, Chengqi; Zhao, Chenggang; Xu, R. X.; Gao, Huazuo; Chen, Deli; Li, Jiashi; Zeng, Wangding; Yu, Xingkai (11 January 2024), *DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models*, [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2401.06066](https://arxiv.org/abs/2401.06066)

[^45]: Shao, Zhihong; Wang, Peiyi; Zhu, Qihao; Xu, Runxin; Song, Junxiao; Bi, Xiao; Zhang, Haowei; Zhang, Mingchuan; Li, Y. K. (27 April 2024), *DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models*, [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2402.03300](https://arxiv.org/abs/2402.03300).

[^46]: DeepSeek-AI; Zhu, Qihao; Guo, Daya; Shao, Zhihong; Yang, Dejian; Wang, Peiyi; Xu, Runxin; Wu, Y.; Li, Yukun (17 June 2024), *DeepSeek-Coder-V2: Breaking the Barrier of Closed-Source Models in Code Intelligence*, [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2406.11931](https://arxiv.org/abs/2406.11931)

[^47]: ["deepseek-ai/DeepSeek-V2.5 · Hugging Face"](https://huggingface.co/deepseek-ai/DeepSeek-V2.5). *[Hugging Face](https://en.wikipedia.org/wiki/Hugging_Face "Hugging Face")*. 3 January 2025. [Archived](https://web.archive.org/web/20250130091452/https://huggingface.co/deepseek-ai/DeepSeek-V2.5) from the original on 30 January 2025. Retrieved 28 January 2025.

[^48]: ["Deepseek Log in page"](https://chat.deepseek.com/sign_in). *DeepSeek*. Retrieved 30 January 2025.

[^49]: ["News | DeepSeek-R1-Lite Release 2024/11/20: 🚀 DeepSeek-R1-Lite-Preview is now live: unleashing supercharged reasoning power!"](https://web.archive.org/web/20241120141324/https://api-docs.deepseek.com/news/news1120). *DeepSeek API Docs*. Archived from [the original](https://api-docs.deepseek.com/news/news1120) on 20 November 2024. Retrieved 28 January 2025.

[^50]: Field, Hayden (27 January 2025). ["China's DeepSeek AI dethrones ChatGPT on App Store: Here's what you should know"](https://www.cnbc.com/2025/01/27/chinas-deepseek-ai-tops-chatgpt-app-store-what-you-should-know.html). *[CNBC](https://en.wikipedia.org/wiki/CNBC "CNBC")*. [Archived](https://web.archive.org/web/20250128201052/https://www.cnbc.com/2025/01/27/chinas-deepseek-ai-tops-chatgpt-app-store-what-you-should-know.html) from the original on 28 January 2025. Retrieved 27 January 2025.

[^51]: Picchi, Aimee (27 January 2025). ["What is DeepSeek, and why is it causing Nvidia and other stocks to slump?"](https://www.cbsnews.com/news/what-is-deepseek-ai-china-stock-nvidia-nvda-asml/). *[CBS News](https://en.wikipedia.org/wiki/CBS_News "CBS News")*. [Archived](https://web.archive.org/web/20250129002522/https://www.cbsnews.com/news/what-is-deepseek-ai-china-stock-nvidia-nvda-asml/) from the original on 29 January 2025. Retrieved 27 January 2025.

[^52]: Nuñez, Michael (24 March 2025). ["DeepSeek-V3 now runs at 20 tokens per second on Mac Studio, and that's a nightmare for OpenAI"](https://venturebeat.com/ai/deepseek-v3-now-runs-at-20-tokens-per-second-on-mac-studio-and-thats-a-nightmare-for-openai/). *[VentureBeat](https://en.wikipedia.org/wiki/VentureBeat "VentureBeat")*. Retrieved 24 March 2025.

[^53]: ["deepseek-ai/DeepSeek-V3-0324 · Hugging Face"](https://huggingface.co/deepseek-ai/DeepSeek-V3-0324). *[Hugging Face](https://en.wikipedia.org/wiki/Hugging_Face "Hugging Face")*. [Archived](https://web.archive.org/web/20250324193733/https://huggingface.co/deepseek-ai/DeepSeek-V3-0324) from the original on 24 March 2025. Retrieved 24 March 2025.

[^54]: ["deepseek-ai/DeepSeek-R1-0528 · Hugging Face"](https://huggingface.co/deepseek-ai/DeepSeek-R1-0528). *huggingface.co*. 28 May 2025. [Archived](https://web.archive.org/web/20250528192921/https://huggingface.co/deepseek-ai/DeepSeek-R1-0528) from the original on 28 May 2025. Retrieved 28 May 2025.

[^55]: Colville, Alex (12 June 2025). ["China's Global AI Firewall"](https://chinamediaproject.org/2025/06/12/chinas-global-ai-firewall/). *China Media Project*. Retrieved 30 June 2025.

[^56]: ["deepseek-ai/DeepSeek-V3.1 · Hugging Face"](https://huggingface.co/deepseek-ai/DeepSeek-V3.1). *huggingface.co*. 21 August 2025. Retrieved 25 August 2025.

[^57]: ["DeepSeek-V3.1 Release | DeepSeek API Docs"](https://api-docs.deepseek.com/news/news250821). *api-docs.deepseek.com*. Retrieved 25 August 2025.

[^58]: ["deepseek-ai/DeepSeek-V3.1-Terminus · Hugging Face"](https://huggingface.co/deepseek-ai/DeepSeek-V3.1-Terminus). *huggingface.co*. 22 September 2025. Retrieved 24 September 2025.

[^59]: Yuan, Jingyang; Gao, Huazuo; Dai, Damai; Luo, Junyu; Zhao, Liang; Zhang, Zhengyan; Xie, Zhenda; Wei, Y. X.; Wang, Lean (27 February 2025), *Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention*, [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2502.11089](https://arxiv.org/abs/2502.11089)

[^60]: ["deepseek-ai/DeepSeek-V3.2-Exp · Hugging Face"](https://huggingface.co/deepseek-ai/DeepSeek-V3.2-Exp). *huggingface.co*. 29 September 2025. Retrieved 2 October 2025.

[^61]: Binder, Matt (3 December 2025). ["DeepSeek v3.2: What it is, how it compares to ChatGPT, how to try it"](https://mashable.com/article/deepseek-v3-2-models-released). *[Mashable](https://en.wikipedia.org/wiki/Mashable "Mashable")*. Retrieved 12 April 2026.

[^62]: ["DeepSeek-V3.2 Release"](https://api-docs.deepseek.com/news/news251201). *DeepSeek API Docs*. 1 December 2025. Retrieved 12 April 2026.

[^63]: Metz, Cade (23 February 2026). ["Anthropic Accuses 3 Chinese Companies of Harvesting Its Data"](https://www.nytimes.com/2026/02/23/technology/anthropic-chinese-startups-distillation.html). *[The New York Times](https://en.wikipedia.org/wiki/The_New_York_Times "The New York Times")*. [ISSN](https://en.wikipedia.org/wiki/ISSN_\(identifier\) "ISSN (identifier)") [0362-4331](https://search.worldcat.org/issn/0362-4331). Retrieved 24 February 2026.

[^64]: ["China's DeepSeek trained its AI model on Nvidia's best chip despite US ban"](https://www.straitstimes.com/world/united-states/chinas-deepseek-trained-ai-model-on-nvidias-best-chip-despite-us-ban-official-says?ref=latest-headlines). *The Straits Times*. 24 February 2026. [ISSN](https://en.wikipedia.org/wiki/ISSN_\(identifier\) "ISSN (identifier)") [0585-3923](https://search.worldcat.org/issn/0585-3923). Retrieved 27 February 2026.

[^65]: ["大模型价格又砍一刀 这次"屠夫"竟是量化私募？"](https://www.cls.cn/detail/1672635). *www.cls.cn*. 10 May 2024. [Archived](https://web.archive.org/web/20241227042059/https://www.cls.cn/detail/1672635) from the original on 27 December 2024. Retrieved 3 February 2025.

[^66]: Schneider, Jordan (27 November 2024). ["Deepseek: The Quiet Giant Leading China's AI Race"](https://www.chinatalk.media/p/deepseek-ceo-interview-with-chinas). *ChinaTalk*. [Archived](https://web.archive.org/web/20241129213821/https://www.chinatalk.media/p/deepseek-ceo-interview-with-chinas) from the original on 29 November 2024. Retrieved 28 December 2024.

[^67]: Mickle, Tripp; Swanson, Ana; Tobin, Meaghan; Metz, Cade (16 April 2025). ["US Officials Target Nvidia and DeepSeek Amid Fears of China's A.I. Progress"](https://www.nytimes.com/2025/04/16/technology/nvidia-deepseek-china-ai-trump.html). *[The New York Times](https://en.wikipedia.org/wiki/The_New_York_Times "The New York Times")*. [ISSN](https://en.wikipedia.org/wiki/ISSN_\(identifier\) "ISSN (identifier)") [0362-4331](https://search.worldcat.org/issn/0362-4331). Retrieved 17 April 2025.

[^68]: Greenspan, Anna; Konior, Bogna (2025). "Introduction: Fleeting Forces and Clever Machinations". In Bratton, Benjamin; Greenspan, Anna; Ireland, Amy; Konior, Bogna (eds.). *Machine Decision is Not Final: China and the History and Future of Artificial Intelligence*. Urbanomic, [MIT Press](https://en.wikipedia.org/wiki/MIT_Press "MIT Press"). [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [9781913029999](https://en.wikipedia.org/wiki/Special:BookSources/9781913029999 "Special:BookSources/9781913029999").

[^69]: Rai, Saritha, Loni Prinsloo, and Helen Nyambura ["China's DeepSeek Is Beating Out OpenAI and Google in Africa"](https://www.bloomberg.com/news/features/2025-10-22/china-s-deepseek-pushes-into-africa-making-ai-accessible-to-millions?embedded-checkout=true) *Bloomberg Technology*. Accessed 27 Oct 2025.

[^70]: ["幻方力量 | 高速文件系统 3FS"](https://www.high-flyer.cn/blog/3fs/). *[High-Flyer](https://en.wikipedia.org/wiki/High-Flyer "High-Flyer")*. 13 June 2019. [Archived](https://web.archive.org/web/20250203011728/https://www.high-flyer.cn/blog/3fs/) from the original on 3 February 2025. Retrieved 3 February 2025.

[^71]: [*deepseek-ai/3FS*](https://github.com/deepseek-ai/3FS), DeepSeek, 28 February 2025, [archived](https://web.archive.org/web/20250228054402/https://github.com/deepseek-ai/3FS) from the original on 28 February 2025, retrieved 28 February 2025

[^72]: ["HFAiLab/hai-platform"](https://github.com/HFAiLab/hai-platform), *[High-Flyer](https://en.wikipedia.org/wiki/High-Flyer "High-Flyer")*, 2 February 2025, retrieved 3 February 2025

[^73]: ["LICENSE · deepseek-ai/deepseek-coder-33b-base"](https://huggingface.co/deepseek-ai/deepseek-coder-33b-base/blob/0b7a04d545e6e555c9149ea646d5884075321657/LICENSE). *[Hugging Face](https://en.wikipedia.org/wiki/Hugging_Face "Hugging Face")*. 28 October 2023. Retrieved 12 April 2026.

[^74]: ["DeepSeek-LLM/LICENSE-MODEL"](https://github.com/deepseek-ai/DeepSeek-LLM/blob/f8b3d77beb4449d77932eccc6abe08826ad3c608/LICENSE-MODEL). *[GitHub](https://en.wikipedia.org/wiki/GitHub "GitHub")*. 29 November 2023. Retrieved 12 April 2026.

[^75]: ["DeepSeek-MoE/LICENSE-MODEL"](https://github.com/deepseek-ai/DeepSeek-MoE/blob/1c8e7915f5f9aa7542ccad0571e0316e8f46ed56/LICENSE-MODEL). 11 January 2024. Retrieved 12 April 2026 – via [GitHub](https://en.wikipedia.org/wiki/GitHub "GitHub").

[^76]: ["LICENSE · deepseek-ai/deepseek-math-7b-base"](https://huggingface.co/deepseek-ai/deepseek-math-7b-base/blob/508a0dbe5467ae8a44aac7b0ad3868f12a87ba9e/LICENSE). *[Hugging Face](https://en.wikipedia.org/wiki/Hugging_Face "Hugging Face")*. 6 February 2024. Retrieved 12 April 2026.

[^77]: ["LICENSE · deepseek-ai/deepseek-math-7b-instruct"](https://huggingface.co/deepseek-ai/deepseek-math-7b-instruct/blob/4400d001099b793071767697fcd6f76989cb2e31/LICENSE). *[Hugging Face](https://en.wikipedia.org/wiki/Hugging_Face "Hugging Face")*. 6 February 2024. Retrieved 12 April 2026.

[^78]: ["LICENSE · deepseek-ai/deepseek-math-7b-rl"](https://huggingface.co/deepseek-ai/deepseek-math-7b-rl/blob/32acbd44180840b05306b3eda573f5ee3977369e/LICENSE). *[Hugging Face](https://en.wikipedia.org/wiki/Hugging_Face "Hugging Face")*. 6 February 2024. Retrieved 12 April 2026.

[^79]: ["LICENSE · deepseek-ai/DeepSeek-V2.5"](https://huggingface.co/deepseek-ai/DeepSeek-V2.5/blob/a05fd5f7de7b873944d01cb0270caedd53e07570/LICENSE). 5 September 2024. Retrieved 12 April 2026 – via [Hugging Face](https://en.wikipedia.org/wiki/Hugging_Face "Hugging Face").

[^80]: ["LICENSE-MODEL · deepseek-ai/DeepSeek-V3-Base"](https://huggingface.co/deepseek-ai/DeepSeek-V3-Base/blob/cc85cae8283f21e8970d6c3f95d9781242cff492/LICENSE-MODEL). 26 December 2024. Retrieved 12 April 2026 – via [Hugging Face](https://en.wikipedia.org/wiki/Hugging_Face "Hugging Face").

[^81]: ["DeepSeek-Prover-V2/LICENSE-MODEL"](https://github.com/deepseek-ai/DeepSeek-Prover-V2/blob/36acbf5d6d9f5cc2c3f2f6fa4fc6cf8a51dcf849/LICENSE-MODEL). 30 April 2025. Retrieved 12 April 2026 – via [GitHub](https://en.wikipedia.org/wiki/GitHub "GitHub").

[^82]: ["deepseek-ai/deepseek-vl2"](https://huggingface.co/deepseek-ai/deepseek-vl2). 27 November 2025. Retrieved 12 April 2026 – via [Hugging Face](https://en.wikipedia.org/wiki/Hugging_Face "Hugging Face").

[^83]: ["LICENSE · deepseek-ai/DeepSeek-R1-0528"](https://huggingface.co/deepseek-ai/DeepSeek-R1-0528/blob/11628360bdbb84a195bb216d98bc724f6af08d57/LICENSE). 28 May 2025. Retrieved 12 April 2026 – via [Hugging Face](https://en.wikipedia.org/wiki/Hugging_Face "Hugging Face").

[^84]: DeepSeek-AI; Guo, Daya; Yang, Dejian; Zhang, Haowei; Song, Junxiao; Zhang, Ruoyu; Xu, Runxin; Zhu, Qihao; Ma, Shirong (22 January 2025), *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*, [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2501.12948](https://arxiv.org/abs/2501.12948)

[^85]: ["LICENSE · deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B/blob/2a29ab14a7dcfb5132537e18050d0ebe5008f7fb/LICENSE). 20 January 2025. Retrieved 12 April 2026 – via [Hugging Face](https://en.wikipedia.org/wiki/Hugging_Face "Hugging Face").

[^86]: ["LICENSE · deepseek-ai/DeepSeek-V3.1-Base"](https://huggingface.co/deepseek-ai/DeepSeek-V3.1-Base/blob/4f0dbf5bdec43e980ff93ec4dd234f5150877543/LICENSE). 19 August 2025. Retrieved 12 April 2026 – via [Hugging Face](https://en.wikipedia.org/wiki/Hugging_Face "Hugging Face").

[^87]: ["LICENSE · deepseek-ai/DeepSeek-V3.1-Terminus"](https://huggingface.co/deepseek-ai/DeepSeek-V3.1-Terminus/blob/846b34eb0fdd68b57d255a31ddd1b4cb37fc601f/LICENSE). 22 September 2025. Retrieved 12 April 2026 – via [Hugging Face](https://en.wikipedia.org/wiki/Hugging_Face "Hugging Face").

[^88]: ["LICENSE · deepseek-ai/DeepSeek-Math-V2"](https://huggingface.co/deepseek-ai/DeepSeek-Math-V2/blob/9b04ba20f1f7ca1803b112cb2ad6410a143b262c/LICENSE). 27 November 2025. Retrieved 12 April 2026 – via [Hugging Face](https://en.wikipedia.org/wiki/Hugging_Face "Hugging Face").

[^89]: ["LICENSE · deepseek-ai/DeepSeek-V3.2"](https://huggingface.co/deepseek-ai/DeepSeek-V3.2/blob/a7e62ac04ecb2c0a54d736dc46601c5606cf10a6/LICENSE). 1 December 2025. Retrieved 12 April 2026 – via [Hugging Face](https://en.wikipedia.org/wiki/Hugging_Face "Hugging Face").

[^90]: ["DeepSeek-Coder/LICENSE-MODEL at main · deepseek-ai/DeepSeek-Coder"](https://github.com/deepseek-ai/DeepSeek-Coder/blob/main/LICENSE-MODEL). *[GitHub](https://en.wikipedia.org/wiki/GitHub "GitHub")*. [Archived](https://web.archive.org/web/20250122195853/https://github.com/deepseek-ai/deepseek-coder/blob/main/LICENSE-MODEL) from the original on 22 January 2025. Retrieved 24 January 2025.

[^91]: Guo, Daya; Zhu, Qihao; Yang, Dejian; Xie, Zhenda; Dong, Kai; Zhang, Wentao; Chen, Guanting; Bi, Xiao; Wu, Y. (26 January 2024), *DeepSeek-Coder: When the Large Language Model Meets Programming – The Rise of Code Intelligence*, [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2401.14196](https://arxiv.org/abs/2401.14196)

[^92]: ["DeepSeek Coder"](https://deepseekcoder.github.io/). *deepseekcoder.github.io*. [Archived](https://web.archive.org/web/20250127000632/https://deepseekcoder.github.io/) from the original on 27 January 2025. Retrieved 27 January 2025.

[^93]: [*deepseek-ai/DeepSeek-Coder*](https://github.com/deepseek-ai/deepseek-coder/), DeepSeek, 27 January 2025, [archived](https://web.archive.org/web/20250127054244/https://github.com/deepseek-ai/DeepSeek-Coder) from the original on 27 January 2025, retrieved 27 January 2025

[^94]: ["deepseek-ai/deepseek-coder-5.7bmqa-base · Hugging Face"](https://huggingface.co/deepseek-ai/deepseek-coder-5.7bmqa-base). *[Hugging Face](https://en.wikipedia.org/wiki/Hugging_Face "Hugging Face")*. Retrieved 27 January 2025.

[^95]: [*deepseek-ai/DeepSeek-LLM*](https://github.com/deepseek-ai/DeepSeek-LLM), DeepSeek, 27 January 2025, retrieved 27 January 2025

[^96]: Wang, Peiyi; Li, Lei; Shao, Zhihong; Xu, R. X.; Dai, Damai; Li, Yifei; Chen, Deli; Wu, Y.; Sui, Zhifang (19 February 2024), *Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations*, [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2312.08935](https://arxiv.org/abs/2312.08935).

[^97]: DeepSeek-AI; Liu, Aixin; Feng, Bei; Wang, Bin; Wang, Bingxuan; Liu, Bo; Zhao, Chenggang; Dengr, Chengqi; Ruan, Chong (19 June 2024), *DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model*, [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2405.04434](https://arxiv.org/abs/2405.04434).

[^98]: Peng, Bowen; Quesnelle, Jeffrey; Fan, Honglu; Shippole, Enrico (1 November 2023), *YaRN: Efficient Context Window Extension of Large Language Models*, [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2309.00071](https://arxiv.org/abs/2309.00071).

[^99]: ["config.json · deepseek-ai/DeepSeek-V2-Lite at main"](https://huggingface.co/deepseek-ai/DeepSeek-V2-Lite/blob/main/config.json). *[Hugging Face](https://en.wikipedia.org/wiki/Hugging_Face "Hugging Face")*. 15 May 2024. Retrieved 28 January 2025.

[^100]: ["config.json · deepseek-ai/DeepSeek-V2 at main"](https://huggingface.co/deepseek-ai/DeepSeek-V2/blob/main/config.json). *[Hugging Face](https://en.wikipedia.org/wiki/Hugging_Face "Hugging Face")*. 6 May 2024. Retrieved 28 January 2025.

[^101]: Feng, Coco (25 March 2025). ["DeepSeek wows coders with more powerful open-source V3 model"](https://www.scmp.com/tech/big-tech/article/3303798/deepseeks-upgraded-foundational-model-excels-coding-and-maths). *[South China Morning Post](https://en.wikipedia.org/wiki/South_China_Morning_Post "South China Morning Post")*. Retrieved 6 April 2025.

[^102]: ["config.json · deepseek-ai/DeepSeek-V3 at main"](https://huggingface.co/deepseek-ai/DeepSeek-V3/blob/main/config.json). *[Hugging Face](https://en.wikipedia.org/wiki/Hugging_Face "Hugging Face")*. 26 December 2024. [Archived](https://web.archive.org/web/20250126101005/https://huggingface.co/deepseek-ai/DeepSeek-V3/blob/main/config.json) from the original on 26 January 2025. Retrieved 28 January 2025.

[^103]: Patel, Dylan; Kourabi, AJ; O'Laughlin, Dylan; Knuhtsen, Doug (31 January 2025). ["DeepSeek Debates: Chinese Leadership On Cost, True Training Cost, Closed Model Margin Impacts"](https://semianalysis.com/2025/01/31/deepseek-debates/). *SemiAnalysis*. [Archived](https://web.archive.org/web/20250213182726/https://semianalysis.com/2025/01/31/deepseek-debates/) from the original on 13 February 2025. Retrieved 13 February 2025.

[^104]: Thubron, Rob (3 February 2025). ["DeepSeek's AI costs far exceed $5.5 million claim, may have reached $1.6 billion with 50,000 Nvidia GPUs"](https://www.techspot.com/news/106612-deepseek-ai-costs-far-exceed-55-million-claim.html). *TechSpot*. Retrieved 13 February 2025.

[^105]: Kajal, Kapil (31 January 2025). ["Research exposes DeepSeek's AI training cost is not $6M, it's a staggering $1.3B"](https://www.yahoo.com/news/research-exposes-deepseek-ai-training-165025904.html). *[Yahoo News](https://en.wikipedia.org/wiki/Yahoo_News "Yahoo News")*. [Archived](https://web.archive.org/web/20250213015354/https://www.yahoo.com/news/research-exposes-deepseek-ai-training-165025904.html) from the original on 13 February 2025. Retrieved 13 February 2025.

[^106]: ["Martin Vechev of INSAIT: "DeepSeek $6M Cost Of Training Is Misleading""](https://therecursive.com/martin-vechev-of-insait-deepseek-6m-cost-of-training-is-misleading/). *TheRecursive.com*. 28 January 2025. [Archived](https://web.archive.org/web/20250213130710/https://therecursive.com/martin-vechev-of-insait-deepseek-6m-cost-of-training-is-misleading/) from the original on 13 February 2025. Retrieved 13 February 2025.

[^107]: Jiang, Ben (27 December 2024). ["Chinese start-up DeepSeek's new AI model outperforms Meta, OpenAI products"](https://www.scmp.com/tech/tech-trends/article/3292507/chinese-start-deepseek-launches-ai-model-outperforms-meta-openai-products). *[South China Morning Post](https://en.wikipedia.org/wiki/South_China_Morning_Post "South China Morning Post")*. [Archived](https://web.archive.org/web/20241227191529/https://www.scmp.com/tech/tech-trends/article/3292507/chinese-start-deepseek-launches-ai-model-outperforms-meta-openai-products) from the original on 27 December 2024. Retrieved 28 December 2024.

[^108]: Sharma, Shubham (26 December 2024). ["DeepSeek-V3, ultra-large open-source AI, outperforms Llama and Qwen on launch"](https://venturebeat.com/ai/deepseek-v3-ultra-large-open-source-ai-outperforms-llama-and-qwen-on-launch/). *[VentureBeat](https://en.wikipedia.org/wiki/VentureBeat "VentureBeat")*. [Archived](https://web.archive.org/web/20241227195503/https://venturebeat.com/ai/deepseek-v3-ultra-large-open-source-ai-outperforms-llama-and-qwen-on-launch/) from the original on 27 December 2024. Retrieved 28 December 2024.

[^109]: Wiggers, Kyle (26 December 2024). ["DeepSeek's new AI model appears to be one of the best 'open' challengers yet"](https://techcrunch.com/2024/12/26/deepseeks-new-ai-model-appears-to-be-one-of-the-best-open-challengers-yet/). *[TechCrunch](https://en.wikipedia.org/wiki/TechCrunch "TechCrunch")*. [Archived](https://web.archive.org/web/20250102103526/https://techcrunch.com/2024/12/26/deepseeks-new-ai-model-appears-to-be-one-of-the-best-open-challengers-yet/) from the original on 2 January 2025. Retrieved 31 December 2024.

[^110]: Edwards, Benj (21 January 2025). ["Cutting-edge Chinese "reasoning" model rivals OpenAI o1—and it's free to download"](https://arstechnica.com/ai/2025/01/china-is-catching-up-with-americas-best-reasoning-ai-models/). *[Ars Technica](https://en.wikipedia.org/wiki/Ars_Technica "Ars Technica")*. Retrieved 16 February 2025.

[^111]: Franzen, Carl (20 November 2024). ["DeepSeek's first reasoning model R1-Lite-Preview turns heads, beating OpenAI o1 performance"](https://venturebeat.com/ai/deepseeks-first-reasoning-model-r1-lite-preview-turns-heads-beating-openai-o1-performance/). *[VentureBeat](https://en.wikipedia.org/wiki/VentureBeat "VentureBeat")*. [Archived](https://web.archive.org/web/20241122010413/https://venturebeat.com/ai/deepseeks-first-reasoning-model-r1-lite-preview-turns-heads-beating-openai-o1-performance/) from the original on 22 November 2024. Retrieved 28 December 2024.

[^112]: Huang, Raffaele (24 December 2024). ["Don't Look Now, but China's AI Is Catching Up Fast"](https://www.wsj.com/tech/ai/china-ai-advances-us-chips-7838fd20). *[The Wall Street Journal](https://en.wikipedia.org/wiki/The_Wall_Street_Journal "The Wall Street Journal")*. [Archived](https://web.archive.org/web/20241227183842/https://www.wsj.com/tech/ai/china-ai-advances-us-chips-7838fd20) from the original on 27 December 2024. Retrieved 28 December 2024.

[^113]: ["Release DeepSeek-R1 · deepseek-ai/DeepSeek-R1@23807ce"](https://github.com/deepseek-ai/DeepSeek-R1/commit/23807ced51627276434655dd9f27725354818974). *[GitHub](https://en.wikipedia.org/wiki/GitHub "GitHub")*. [Archived](https://web.archive.org/web/20250121104009/https://github.com/deepseek-ai/DeepSeek-R1/commit/23807ced51627276434655dd9f27725354818974) from the original on 21 January 2025. Retrieved 21 January 2025.

[^114]: Eduardo Baptista; Julie Zhu; Fanny Potkin (25 February 2025). ["DeepSeek rushes to launch new AI model as China goes all in"](https://www.reuters.com/technology/artificial-intelligence/deepseek-rushes-launch-new-ai-model-china-goes-all-2025-02-25/). *Reuters*. [Archived](https://web.archive.org/web/20250321225322/https://www.reuters.com/technology/artificial-intelligence/deepseek-rushes-launch-new-ai-model-china-goes-all-2025-02-25/) from the original on 21 March 2025. Retrieved 25 February 2025.

[^115]: Ding, Luz (29 May 2025). ["DeepSeek Says Upgraded Model Reasons Better, Hallucinates Less"](https://www.bloomberg.com/news/articles/2025-05-29/deepseek-says-upgraded-model-reasons-better-hallucinates-less). *Bloomberg*. Retrieved 9 June 2025.

[^116]: ["DeepSeek R2 launch stalled as CEO balks at progress, The Information reports"](https://www.reuters.com/world/china/deepseek-r2-launch-stalled-ceo-balks-progress-information-reports-2025-06-26/). *Reuters*. 26 June 2025. Retrieved 5 July 2025.

[^117]: Olcott, Eleanor; Wu, Zijing (14 August 2025). ["DeepSeek's next AI model delayed by attempt to use Chinese chips"](https://www.ft.com/content/eb984646-6320-4bfe-a78d-a1da2274b092). *[Financial Times](https://en.wikipedia.org/wiki/Financial_Times "Financial Times")*. Retrieved 13 November 2025.

[^118]: ["China cautions tech firms over Nvidia H20 AI chip purchases, sources say"](https://www.reuters.com/world/china/china-cautions-tech-firms-over-nvidia-h20-ai-chip-purchases-sources-say-2025-08-12/). *Reuters*. 12 August 2025.

[^119]: Guo, Daya; Yang, Dejian; Zhang, Haowei; Song, Junxiao; Wang, Peiyi; Zhu, Qihao; Xu, Runxin; Zhang, Ruoyu; Ma, Shirong; Bi, Xiao; Zhang, Xiaokang; Yu, Xingkai; Wu, Yu; Wu, Z. F.; Gou, Zhibin (September 2025). ["DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning"](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12443585). *Nature*. **645** (8081): 633–638. [Bibcode](https://en.wikipedia.org/wiki/Bibcode_\(identifier\) "Bibcode (identifier)"):[2025Natur.645..633G](https://ui.adsabs.harvard.edu/abs/2025Natur.645..633G). [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1038/s41586-025-09422-z](https://doi.org/10.1038%2Fs41586-025-09422-z). [ISSN](https://en.wikipedia.org/wiki/ISSN_\(identifier\) "ISSN (identifier)") [1476-4687](https://search.worldcat.org/issn/1476-4687). [PMC](https://en.wikipedia.org/wiki/PMC_\(identifier\) "PMC (identifier)") [12443585](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12443585). [PMID](https://en.wikipedia.org/wiki/PMID_\(identifier\) "PMID (identifier)") [40962978](https://pubmed.ncbi.nlm.nih.gov/40962978).

[^120]: Roose, Kevin (28 January 2025). ["Why DeepSeek Could Change What Silicon Valley Believe About A.I."](https://www.nytimes.com/2025/01/28/technology/why-deepseek-could-change-what-silicon-valley-believes-about-ai.html) *[The New York Times](https://en.wikipedia.org/wiki/The_New_York_Times "The New York Times")*. [ISSN](https://en.wikipedia.org/wiki/ISSN_\(identifier\) "ISSN (identifier)") [0362-4331](https://search.worldcat.org/issn/0362-4331). [Archived](https://web.archive.org/web/20250128131926/https://www.nytimes.com/2025/01/28/technology/why-deepseek-could-change-what-silicon-valley-believes-about-ai.html) from the original on 28 January 2025. Retrieved 28 January 2025.

[^121]: ["Beyond the Headlines on DeepSeek's Sputnik Moment: A Conversation with Jimmy Goodrich - IGCC"](https://ucigcc.org/interview/beyond-the-headlines-on-deepseeks-sputnik-moment-a-conversation-with-jimmy-goodrich/). *UC Institute on Global Conflict and Cooperation (IGCC)*. 12 February 2025.

[^122]: ["Is 'Sputnik Moment' an appropriate analogy for the launch of DeepSeek? - LCFI"](https://www.lcfi.ac.uk/news-events/blog/post/is-sputnik-moment-an-appropriate-analogy-for-the-launch-of-deepseek). *LCFI - Leverhulme Centre for the Future of Intelligence*. 2 February 2025.

[^123]: Roeloffs, Mary Whitfill. ["What Is DeepSeek? New Chinese Artificial Intelligence Rivals ChatGPT, OpenAI"](https://www.forbes.com/sites/maryroeloffs/2025/01/27/what-is-deepseek-new-chinese-ai-startup-rivals-openai-and-claims-its-far-cheaper/). *Forbes*. Retrieved 5 August 2025.

[^124]: DeepSeek-AI; et al. (2024). "DeepSeek-V3 Technical Report". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2412.19437](https://arxiv.org/abs/2412.19437) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^125]: Chow, Andrew R.; Perrigo, Billy (30 January 2025). ["Is the DeepSeek Panic Overblown?"](https://time.com/7211646/is-deepseek-panic-overblown/). *TIME*. [Archived](https://web.archive.org/web/20250317061531/https://time.com/7211646/is-deepseek-panic-overblown/) from the original on 17 March 2025. Retrieved 17 March 2025.