---
title: "Attacks in Adversarial Machine Learning: A Systematic Survey from the Life-cycle Perspective"
source: "https://arxiv.org/html/2302.09457v2"
author:
published:
created: 2026-04-15
description:
tags:
  - "clippings"
---
Baoyuan Wu, Zihao Zhu, Li Liu, Qingshan Liu, Zhaofeng He, Siwei Lyu Baoyuan Wu and Zihao Zhu are with the School of Data Science, The Chinese University of Hong Kong, Shenzhen, China, email: wubaoyuan@cuhk.edu.cn, zihaozhu@link.cuhk.edu.cn. Li Liu is with the Hong Kong University of Science and Technology (Guangzhou), China, email: avrillliu@hkust-gz.edu.cn. Qingshan Liu, email: qsliu@nuist.edu.cn. Zhaofeng He is with the School of Artificial Intelligence, Beijing University of Posts and Telecommunications, Beijing, China, email: zhaofenghe@bupt.edu.cn. Siwei Lyu is with the Department of Computer Science and Engineering, University at Buffalo, State University of New York (SUNY), Buffalo, NY 14260 USA, email: siweilyu@buffalo.edu. Corresponding author: Baoyuan Wu (wubaoyuan@cuhk.edu.cn).

###### Abstract

Adversarial machine learning (AML) studies the adversarial phenomenon of machine learning, which may make inconsistent or unexpected predictions with humans. Some paradigms have been recently developed to explore this adversarial phenomenon occurring at different stages of a machine learning system, such as backdoor attack occurring at the pre-training, in-training and inference stage; weight attack occurring at the post-training, deployment and inference stage; adversarial attack occurring at the inference stage. However, although these adversarial paradigms share a common goal, their developments are almost independent, and there is still no big picture of AML. In this work, we aim to provide a unified perspective to the AML community to systematically review the overall progress of this field. We firstly provide a general definition about AML, and then propose a unified mathematical framework to covering existing attack paradigms. According to the proposed unified framework, we build a full taxonomy to systematically categorize and review existing representative methods for each paradigm. Besides, using this unified framework, it is easy to figure out the connections and differences among different attack paradigms, which may inspire future researchers to develop more advanced attack paradigms. Finally, to facilitate the viewing of the built taxonomy and the related literature in adversarial machine learning, we further provide a website, $i.e.$, [http://adversarial-ml.com](http://adversarial-ml.com/), where the taxonomies and literature will be continuously updated.

## I Introduction

Machine learning (ML) aims to learn a machine/model from the data, such that it can act like humans when handling new data. It has achieved huge progress on lots of important applications in the last decade, especially with the rise of deep learning from 2006, such as computer vision, natural language processing, speech recognition, $etc.$ It seems that ML has been powerful enough to satisfy humans’ expectations in practice. However, a disturbing phenomenon found in recent years shows that sometimes ML models may make abnormal predictions that are inconsistent with humans. For example, the model could give totally different predictions on two visually similar images, as one of them is perturbed by imperceptible and malicious noises [^86], while human’s prediction will not be influenced by such noises. We call this phenomenon as adversarial phenomenon, indicating the adversary between ML models and humans. Unlike regular machine learning which focuses on improving the consistency between ML models and humans, adversarial machine learning (AML) focuses on exploring the adversarial phenomenon. Unfortunately, due to the black-box mechanism of modern ML models (especially deep neural networks), it is difficult to provide human-understandable explanations for their decisions, neither the consistency nor the inconsistency with humans. Consequently, the existence of the adversarial phenomenon in ML becomes one of the main obstacles to obtain the trust of humans. Meanwhile, due to the importance and challenges of the adversarial phenomenon, it has attracted many researchers’ attention, and AML has become an emerging topic in the ML community.

As shown in Figure 1, we divide the full life-cycle of the machine learning system into five stages, $i.e.$pre-training stage, training stage, post-training, deployment stage, and inference stage. In the literature of AML, several different paradigms have been developed to explore the adversarial phenomenon at different stages, mainly including backdoor attacks occurring at the pre-training, training, and inference stage, weight attacks occurring at the post-training, deployment, and inference stage, and adversarial examples occurring at the inference stage <sup>1</sup>. Although with the same goal, the developments of these attack paradigms are almost independent. Without a comprehensive development of different paradigms, we believe that it will be difficult to comprehensively and deeply understand the adversarial phenomenon of ML, making it difficult to truly improve the adversarial robustness of ML. In this survey, we attempt to provide a unified perspective on the attack aspect of AML on the image classification task, based on the life-cycle of the machine learning system.

Our Goal and Contributions. After years of prosperous but isolated development with a bottom-up manner ($i.e.$, from different perspectives to the same destination), we believe it is important to make a comprehensive top-down review of current progress in the AML area. To achieve this goal, we firstly provide a general definition of AML, and then present a unified mathematical framework to cover diverse formulations of existing branches. Moreover, according to the unified framework, we build systematic categorizations of existing diverse works. Although there been several surveys about adversarial examples ($e.g.$, [^290] [^5]) or backdoor learning ($e.g.$, [^80] [^247]), the main point that distinguishes our survey from existing surveys is the unified definition and mathematical framework of AML, which could bring in two main contributions to the community. 1) The systematic perspective provided by the unified framework could help us to quickly overview the big picture of AML, to avoid one-sided or biased understanding of AML. 2) According to the unified framework, the intrinsic connections among different AML branches are built to provide a broader view for researchers in each individual branch, such that the developments of different branches could be calibrated to accelerate the overall progress of AML.

Organization. The remaining contents are organized as follows: Section II introduces the general definition, unified mathematical formulation, and three learning paradigms of AML. Section III reviews adversarial attacks occurring at the pre-training stage, mainly including data-poisoning based backdoor attacks. Section IV covers adversarial attacks occurring at the training stage, mainly including training-controllable based backdoor attacks. In section V, we investigate adversarial attacks occurring at the post-training stage, mainly including weight attacks via parameter-modification. Section V reviews adversarial attacks occurring at the deployment stage, mainly including weight attacks via bit-flip. Section VII reviews adversarial attacks occurring at the deployment stage, mainly including adversarial examples. Except for image classification, we also review adversarial attacks in other scenarios ($e.g.$, diffusion models and large language models) in Section VIII. Section IX and X present the applications and further discussions of adversarial attacks respectively, followed by the summary in Section XI. This survey only covers the attack part of AML. For the defense part, the readers can refer to our other survey [^249].

## II What is Adversarial Machine Learning

![Refer to caption](https://arxiv.org/html/2302.09457v2/x1.png)

Figure 1: The full life-cycle of Adversarial Machine Leaning

TABLE I: Basic notations.

| Notation | Name and Description |
| --- | --- |
| $D_{0}$ | Benign dataset, $i.e.$, $\{(\mathbf{x}_{0}^{(i)},y_{0}^{(i)})\}_{i=1}^{N_{0}}$, where $(\mathbf{x}_{0}^{(i)},y_{0}^{(i)})$ is called a benign data (BD), with $\mathbf{x}_{0}^{(i)}$ being a benign sample (BS) and $y_{0}^{(i)}$ being a benign label. |
| $D_{\varepsilon}$ | Adversarial dataset, $i.e.$, $\{(\mathbf{x}_{\varepsilon}^{(i)},y_{\varepsilon}^{(i)})\}_{i=1}^{N_{% \varepsilon}}$, where $(\mathbf{x}_{\varepsilon}^{(i)},y_{\varepsilon}^{(i)})$ is called an adversarial data (AD), with $\mathbf{x}_{\varepsilon}^{(i)}$ being an adversarial sample (AS) and $y_{\varepsilon}^{(i)}$ being an adversarial label. |
| $f_{\mathbf{w}_{0}}(\cdot)$ | Benign model (BM): if one model is regularly trained based on $D_{0}$, then it is called BM, with the weight $\mathbf{w}_{0}$ |
| $f_{\mathbf{w}_{\varepsilon}}(\cdot)$ | Adversarial model (AM): If one benign model (BM) $f_{\mathbf{w}_{0}}(\cdot)$ is maliciously modified, or one model is trained based on $D_{\varepsilon}$ (or mixture of $D_{\varepsilon}$ and $D_{0}$), then the modified/trained model is called AM, with the weight $\mathbf{w}_{\varepsilon}$ |

### II-A General Definition and Formulation

Notations. We denote a machine learning model as $f_{\mathbf{w}}:\mathcal{X}\rightarrow\mathcal{Y}$, with $\mathbf{w}$ indicating model weight, $\mathcal{X}\subset\mathcal{R}^{d}$ the input space ($d$ indicating the input dimension), and $\mathcal{Y}\subset\mathcal{R}$ the output space, respectively. A data pair is denoted as $(\mathbf{x},y)$, with $\mathbf{x}\in\mathcal{X}$ being the input sample and $y\in\mathcal{Y}$ being the corresponding label. Furthermore, for clarity, we introduce subscripts $00$ and $\varepsilon$ to indicate benign and adversarial data/model, respectively. The detailed notations are summarized in Table I.

###### Definition 1 (Adversarial Machine Learning (AML)).

AML is an emerging sub-area of machine learning to study the adversarial phenomenon of machine learning. AML is defined upon three basic conditions, including stealthiness $\mathcal{S}$, benign consistency $\mathcal{C}$ and adversarial inconsistency $\mathcal{I}$, as follows:

1. Stealthiness $\mathcal{S}(\mathbf{x}_{0},\mathbf{x}_{\varepsilon};\mathbf{w}_{0},\mathbf{w}_%
	{\varepsilon})$: It captures the condition that the change between benign and adversarial samples, or that between benign and adversarial weights should be stealthy, while the specific definition and formulation of stealthiness will lead to different variants.
2. Benign consistency $\mathcal{C}(\mathbf{x}_{0},y_{0};\mathbf{w}_{0},\mathbf{w}_{\varepsilon})$: It captures the condition of prediction consistency on the benign data pair $(\mathbf{x}_{0},y_{0})$ between human and benign or adversarial models.
3. Adversarial inconsistency $\mathcal{I}(\mathbf{x}_{\varepsilon},y_{\varepsilon};\mathbf{w}_{0},\mathbf{w}%
	_{\varepsilon})$: It captures the condition of prediction inconsistency on the adversarial data pair $(\mathbf{x}_{\varepsilon},y_{\varepsilon})$ between human and benign or adversarial models, which reflects the goal of adversarial machine learning.

General formulation. Based on Definition 1, a general formulation of AML could be written as follows:

$$
\displaystyle\underset{\mathbf{x}_{\varepsilon},\mathbf{w}_{\varepsilon}}{\arg%
\min}~{}
$$
 
$$
\displaystyle\mathcal{S}(\mathbf{x}_{0},\mathbf{x}_{\varepsilon};\mathbf{w}_{0%
},\mathbf{w}_{\varepsilon})+\mathcal{C}(\mathbf{x}_{0},y_{0};\mathbf{w}_{0},%
\mathbf{w}_{\varepsilon})+
$$
 
$$
\displaystyle\mathcal{I}(\mathbf{x}_{\varepsilon},y_{\varepsilon};\mathbf{w}_{%
0},\mathbf{w}_{\varepsilon}).
$$

Specification of each term will lead to different AML paradigms.

### II-B Three Attack Paradigms at Different Stages of AML

TABLE II: Summary of all specified formulations in three attack paradigms of AML.

<table><tbody><tr><td><p>Condition</p></td><td>Specifications</td><td>Description</td></tr><tr><td rowspan="2"><p><math><semantics><mrow><mi>𝒮</mi> <mo>⁢</mo> <mrow><mo>(</mo><msub><mi>𝐱</mi> <mn>0</mn></msub><mo>,</mo><msub><mi>𝐱</mi> <mi>ε</mi></msub><mo>;</mo><msub><mi>𝐰</mi> <mn>0</mn></msub><mo>,</mo><msub><mi>𝐰</mi> <mi>ε</mi></msub><mo>)</mo></mrow></mrow> <annotation-xml><apply><ci>𝒮</ci> <vector><apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <ci>𝜀</ci></apply> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <cn>0</cn></apply> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></vector></apply></annotation-xml> <annotation>\mathcal{S}(\mathbf{x}_{0},\mathbf{x}_{\varepsilon};\mathbf{w}_{0},\mathbf{w}_% {\varepsilon})</annotation> <annotation>caligraphic_S ( bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT, bold_x start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT; bold_w start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT, bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT )</annotation></semantics></math></p></td><td><p>AML.<math><semantics><msub><mi>𝒮</mi> <mi>𝐱</mi></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>𝒮</ci> <ci>𝐱</ci></apply></annotation-xml> <annotation>\mathcal{S}_{\mathbf{x}}</annotation> <annotation>caligraphic_S start_POSTSUBSCRIPT bold_x end_POSTSUBSCRIPT</annotation></semantics></math>: <math><semantics><mrow><msub><mi>𝒟</mi> <mi>𝐱</mi></msub> <mo>⁢</mo> <mrow><mo>(</mo><msub><mi>𝐱</mi> <mn>0</mn></msub><mo>,</mo><msub><mi>𝐱</mi> <mi>ε</mi></msub><mo>)</mo></mrow></mrow> <annotation-xml><apply><apply><csymbol>subscript</csymbol> <ci>𝒟</ci> <ci>𝐱</ci></apply> <interval><apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <ci>𝜀</ci></apply></interval></apply></annotation-xml> <annotation>\mathcal{D}_{\mathbf{x}}(\mathbf{x}_{0},\mathbf{x}_{\varepsilon})</annotation> <annotation>caligraphic_D start_POSTSUBSCRIPT bold_x end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT, bold_x start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT )</annotation></semantics></math></p></td><td><p>Stealthiness of sample perturbation: encouraging small difference between <math><semantics><msub><mi>𝐱</mi> <mn>0</mn></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply></annotation-xml> <annotation>\mathbf{x}_{0}</annotation> <annotation>bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT</annotation></semantics></math> and <math><semantics><msub><mi>𝐱</mi> <mi>ε</mi></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <ci>𝜀</ci></apply></annotation-xml> <annotation>\mathbf{x}_{\varepsilon}</annotation> <annotation>bold_x start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT</annotation></semantics></math></p></td></tr><tr><td><p>AML.<math><semantics><msub><mi>𝒮</mi> <mi>𝐰</mi></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>𝒮</ci> <ci>𝐰</ci></apply></annotation-xml> <annotation>\mathcal{S}_{\mathbf{w}}</annotation> <annotation>caligraphic_S start_POSTSUBSCRIPT bold_w end_POSTSUBSCRIPT</annotation></semantics></math>: <math><semantics><mrow><msub><mi>𝒟</mi> <mi>𝐰</mi></msub> <mo>⁢</mo> <mrow><mo>(</mo><msub><mi>𝐰</mi> <mn>0</mn></msub><mo>,</mo><msub><mi>𝐰</mi> <mi>ε</mi></msub><mo>)</mo></mrow></mrow> <annotation-xml><apply><apply><csymbol>subscript</csymbol> <ci>𝒟</ci> <ci>𝐰</ci></apply> <interval><apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <cn>0</cn></apply> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></interval></apply></annotation-xml> <annotation>\mathcal{D}_{\mathbf{w}}(\mathbf{w}_{0},\mathbf{w}_{\varepsilon})</annotation> <annotation>caligraphic_D start_POSTSUBSCRIPT bold_w end_POSTSUBSCRIPT ( bold_w start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT, bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT )</annotation></semantics></math></p></td><td><p>Stealthiness of weight perturbation: encouraging small difference between <math><semantics><msub><mi>𝐰</mi> <mn>0</mn></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <cn>0</cn></apply></annotation-xml> <annotation>\mathbf{w}_{0}</annotation> <annotation>bold_w start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT</annotation></semantics></math> and <math><semantics><msub><mi>𝐰</mi> <mi>ε</mi></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></annotation-xml> <annotation>\mathbf{w}_{\varepsilon}</annotation> <annotation>bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT</annotation></semantics></math></p></td></tr><tr><td rowspan="2"><p><math><semantics><mrow><mi>𝒞</mi> <mo>⁢</mo> <mrow><mo>(</mo><msub><mi>𝐱</mi> <mn>0</mn></msub><mo>,</mo><msub><mi>y</mi> <mn>0</mn></msub><mo>;</mo><msub><mi>𝐰</mi> <mn>0</mn></msub><mo>,</mo><msub><mi>𝐰</mi> <mi>ε</mi></msub><mo>)</mo></mrow></mrow> <annotation-xml><apply><ci>𝒞</ci> <vector><apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply> <apply><csymbol>subscript</csymbol> <ci>𝑦</ci> <cn>0</cn></apply> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <cn>0</cn></apply> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></vector></apply></annotation-xml> <annotation>\mathcal{C}(\mathbf{x}_{0},y_{0};\mathbf{w}_{0},\mathbf{w}_{\varepsilon})</annotation> <annotation>caligraphic_C ( bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT, italic_y start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT; bold_w start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT, bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT )</annotation></semantics></math></p></td><td><p>AML.<math><semantics><msub><mi>𝒞</mi> <mi>A</mi></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>𝒞</ci> <ci>𝐴</ci></apply></annotation-xml> <annotation>\mathcal{C}_{A}</annotation> <annotation>caligraphic_C start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT</annotation></semantics></math>: <math><semantics><mrow><msub><mi>ℒ</mi> <msub><mi>𝒞</mi> <mi>A</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mi>ε</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msub><mi>𝐱</mi> <mn>0</mn></msub><mo>)</mo></mrow></mrow><mo>,</mo><msub><mi>y</mi> <mn>0</mn></msub><mo>)</mo></mrow></mrow> <annotation-xml><apply><apply><csymbol>subscript</csymbol> <ci>ℒ</ci> <apply><csymbol>subscript</csymbol> <ci>𝒞</ci> <ci>𝐴</ci></apply></apply> <interval><apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply></apply> <apply><csymbol>subscript</csymbol> <ci>𝑦</ci> <cn>0</cn></apply></interval></apply></annotation-xml> <annotation>\mathcal{L}_{\mathcal{C}_{A}}(f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{0}),y_{% 0})</annotation> <annotation>caligraphic_L start_POSTSUBSCRIPT caligraphic_C start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT ), italic_y start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT )</annotation></semantics></math></p></td><td><p>Benign consistency 1: prediction consistency on BS between AM and human, which encourages <math><semantics><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mi>ε</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msub><mi>𝐱</mi> <mn>0</mn></msub><mo>)</mo></mrow></mrow> <annotation-xml><apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply></apply></annotation-xml> <annotation>f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{0})</annotation> <annotation>italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT )</annotation></semantics></math> to be <math><semantics><msub><mi>y</mi> <mn>0</mn></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>𝑦</ci> <cn>0</cn></apply></annotation-xml> <annotation>y_{0}</annotation> <annotation>italic_y start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT</annotation></semantics></math></p></td></tr><tr><td><p>AML.<math><semantics><msub><mi>𝒞</mi> <mi>B</mi></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>𝒞</ci> <ci>𝐵</ci></apply></annotation-xml> <annotation>\mathcal{C}_{B}</annotation> <annotation>caligraphic_C start_POSTSUBSCRIPT italic_B end_POSTSUBSCRIPT</annotation></semantics></math>: <math><semantics><mrow><msub><mi>ℒ</mi> <msub><mi>𝒞</mi> <mi>B</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mn>0</mn></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msub><mi>𝐱</mi> <mn>0</mn></msub><mo>)</mo></mrow></mrow><mo>,</mo><msub><mi>y</mi> <mn>0</mn></msub><mo>)</mo></mrow></mrow> <annotation-xml><apply><apply><csymbol>subscript</csymbol> <ci>ℒ</ci> <apply><csymbol>subscript</csymbol> <ci>𝒞</ci> <ci>𝐵</ci></apply></apply> <interval><apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <cn>0</cn></apply></apply> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply></apply> <apply><csymbol>subscript</csymbol> <ci>𝑦</ci> <cn>0</cn></apply></interval></apply></annotation-xml> <annotation>\mathcal{L}_{\mathcal{C}_{B}}(f_{\mathbf{w}_{0}}(\mathbf{x}_{0}),y_{0})</annotation> <annotation>caligraphic_L start_POSTSUBSCRIPT caligraphic_C start_POSTSUBSCRIPT italic_B end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT ), italic_y start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT )</annotation></semantics></math></p></td><td><p>Benign consistency 2: prediction consistency on BS between BM and human, which encourages <math><semantics><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mn>0</mn></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msub><mi>𝐱</mi> <mn>0</mn></msub><mo>)</mo></mrow></mrow> <annotation-xml><apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <cn>0</cn></apply></apply> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply></apply></annotation-xml> <annotation>f_{\mathbf{w}_{0}}(\mathbf{x}_{0})</annotation> <annotation>italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT )</annotation></semantics></math> to be <math><semantics><msub><mi>y</mi> <mn>0</mn></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>𝑦</ci> <cn>0</cn></apply></annotation-xml> <annotation>y_{0}</annotation> <annotation>italic_y start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT</annotation></semantics></math></p></td></tr><tr><td rowspan="2"><p><math><semantics><mrow><mi>ℐ</mi> <mo>⁢</mo> <mrow><mo>(</mo><msub><mi>𝐱</mi> <mi>ε</mi></msub><mo>,</mo><msub><mi>y</mi> <mi>ε</mi></msub><mo>;</mo><msub><mi>𝐰</mi> <mn>0</mn></msub><mo>,</mo><msub><mi>𝐰</mi> <mi>ε</mi></msub><mo>)</mo></mrow></mrow> <annotation-xml><apply><ci>ℐ</ci> <vector><apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <ci>𝜀</ci></apply> <apply><csymbol>subscript</csymbol> <ci>𝑦</ci> <ci>𝜀</ci></apply> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <cn>0</cn></apply> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></vector></apply></annotation-xml> <annotation>\mathcal{I}(\mathbf{x}_{\varepsilon},y_{\varepsilon};\mathbf{w}_{0},\mathbf{w}% _{\varepsilon})</annotation> <annotation>caligraphic_I ( bold_x start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT, italic_y start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT; bold_w start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT, bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT )</annotation></semantics></math></p></td><td><p>AML.<math><semantics><msub><mi>ℐ</mi> <mi>A</mi></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>ℐ</ci> <ci>𝐴</ci></apply></annotation-xml> <annotation>\mathcal{I}_{A}</annotation> <annotation>caligraphic_I start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT</annotation></semantics></math>: <math><semantics><mrow><msub><mi>ℒ</mi> <msub><mi>ℐ</mi> <mi>A</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mi>ε</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msub><mi>𝐱</mi> <mi>ε</mi></msub><mo>)</mo></mrow></mrow><mo>,</mo><msub><mi>y</mi> <mi>ε</mi></msub><mo>)</mo></mrow></mrow> <annotation-xml><apply><apply><csymbol>subscript</csymbol> <ci>ℒ</ci> <apply><csymbol>subscript</csymbol> <ci>ℐ</ci> <ci>𝐴</ci></apply></apply> <interval><apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <ci>𝜀</ci></apply></apply> <apply><csymbol>subscript</csymbol> <ci>𝑦</ci> <ci>𝜀</ci></apply></interval></apply></annotation-xml> <annotation>\mathcal{L}_{\mathcal{I}_{A}}(f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{% \varepsilon}),y_{\varepsilon})</annotation> <annotation>caligraphic_L start_POSTSUBSCRIPT caligraphic_I start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT ), italic_y start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT )</annotation></semantics></math></p></td><td><p>Adversarial inconsistency 1: prediction inconsistency on AS between AM and human, which encourages <math><semantics><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mi>ε</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msub><mi>𝐱</mi> <mi>ε</mi></msub><mo>)</mo></mrow></mrow> <annotation-xml><apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <ci>𝜀</ci></apply></apply></annotation-xml> <annotation>f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{\varepsilon})</annotation> <annotation>italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT )</annotation></semantics></math> to be the target label <math><semantics><msub><mi>y</mi> <mi>ε</mi></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>𝑦</ci> <ci>𝜀</ci></apply></annotation-xml> <annotation>y_{\varepsilon}</annotation> <annotation>italic_y start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT</annotation></semantics></math></p></td></tr><tr><td><p>AML.<math><semantics><msub><mi>ℐ</mi> <mi>B</mi></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>ℐ</ci> <ci>𝐵</ci></apply></annotation-xml> <annotation>\mathcal{I}_{B}</annotation> <annotation>caligraphic_I start_POSTSUBSCRIPT italic_B end_POSTSUBSCRIPT</annotation></semantics></math>: <math><semantics><mrow><msub><mi>ℒ</mi> <msub><mi>ℐ</mi> <mi>B</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mn>0</mn></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msub><mi>𝐱</mi> <mi>ε</mi></msub><mo>)</mo></mrow></mrow><mo>,</mo><msub><mi>y</mi> <mi>ε</mi></msub><mo>)</mo></mrow></mrow> <annotation-xml><apply><apply><csymbol>subscript</csymbol> <ci>ℒ</ci> <apply><csymbol>subscript</csymbol> <ci>ℐ</ci> <ci>𝐵</ci></apply></apply> <interval><apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <cn>0</cn></apply></apply> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <ci>𝜀</ci></apply></apply> <apply><csymbol>subscript</csymbol> <ci>𝑦</ci> <ci>𝜀</ci></apply></interval></apply></annotation-xml> <annotation>\mathcal{L}_{\mathcal{I}_{B}}(f_{\mathbf{w}_{0}}(\mathbf{x}_{\varepsilon}),y_{% \varepsilon})</annotation> <annotation>caligraphic_L start_POSTSUBSCRIPT caligraphic_I start_POSTSUBSCRIPT italic_B end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT ), italic_y start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT )</annotation></semantics></math></p></td><td><p>Adversarial inconsistency 2: prediction inconsistency on AS between BM and human, which encourages <math><semantics><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mn>0</mn></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msub><mi>𝐱</mi> <mi>ε</mi></msub><mo>)</mo></mrow></mrow> <annotation-xml><apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <cn>0</cn></apply></apply> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <ci>𝜀</ci></apply></apply></annotation-xml> <annotation>f_{\mathbf{w}_{0}}(\mathbf{x}_{\varepsilon})</annotation> <annotation>italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT )</annotation></semantics></math> to be the target label <math><semantics><msub><mi>y</mi> <mi>ε</mi></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>𝑦</ci> <ci>𝜀</ci></apply></annotation-xml> <annotation>y_{\varepsilon}</annotation> <annotation>italic_y start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT</annotation></semantics></math></p></td></tr><tr><td rowspan="5"><p>Others</p></td><td><p><math><semantics><mrow><msub><mi>ℛ</mi> <mn>1</mn></msub> <mo>⁢</mo> <mrow><mo>(</mo><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mn>0</mn></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msub><mi>𝐱</mi> <mn>0</mn></msub><mo>)</mo></mrow></mrow><mo>,</mo><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mn>0</mn></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msub><mi>𝐱</mi> <mi>ε</mi></msub><mo>)</mo></mrow></mrow><mo>)</mo></mrow></mrow> <annotation-xml><apply><apply><csymbol>subscript</csymbol> <ci>ℛ</ci> <cn>1</cn></apply> <interval><apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <cn>0</cn></apply></apply> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply></apply> <apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <cn>0</cn></apply></apply> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <ci>𝜀</ci></apply></apply></interval></apply></annotation-xml> <annotation>\mathcal{R}_{1}(f_{\mathbf{w}_{0}}(\mathbf{x}_{0}),f_{\mathbf{w}_{0}}(\mathbf{% x}_{\varepsilon}))</annotation> <annotation>caligraphic_R start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT ( italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT ), italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT ) )</annotation></semantics></math></p></td><td><p>Regularization for encouraging some kinds of similarity between BS and AS according to BM</p></td></tr><tr><td><p><math><semantics><mrow><msub><mi>ℛ</mi> <mn>2</mn></msub> <mo>⁢</mo> <mrow><mo>(</mo><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mi>ε</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msub><mi>𝐱</mi> <mn>0</mn></msub><mo>)</mo></mrow></mrow><mo>,</mo><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mi>ε</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msub><mi>𝐱</mi> <mi>ε</mi></msub><mo>)</mo></mrow></mrow><mo>)</mo></mrow></mrow> <annotation-xml><apply><apply><csymbol>subscript</csymbol> <ci>ℛ</ci> <cn>2</cn></apply> <interval><apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply></apply> <apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <ci>𝜀</ci></apply></apply></interval></apply></annotation-xml> <annotation>\mathcal{R}_{2}(f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{0}),f_{\mathbf{w}_{% \varepsilon}}(\mathbf{x}_{\varepsilon}))</annotation> <annotation>caligraphic_R start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT ( italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT ), italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT ) )</annotation></semantics></math></p></td><td><p>Regularization for encouraging some kinds of similarity between BS and AS according to AM</p></td></tr><tr><td><p><math><semantics><mrow><msub><mi>ℛ</mi> <mn>3</mn></msub> <mo>⁢</mo> <mrow><mo>(</mo><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mi>ε</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msub><mi>𝐱</mi> <mn>0</mn></msub><mo>)</mo></mrow></mrow><mo>,</mo><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mn>0</mn></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msub><mi>𝐱</mi> <mn>0</mn></msub><mo>)</mo></mrow></mrow><mo>)</mo></mrow></mrow> <annotation-xml><apply><apply><csymbol>subscript</csymbol> <ci>ℛ</ci> <cn>3</cn></apply> <interval><apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply></apply> <apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <cn>0</cn></apply></apply> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply></apply></interval></apply></annotation-xml> <annotation>\mathcal{R}_{3}(f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{0}),f_{\mathbf{w}_{0}% }(\mathbf{x}_{0}))</annotation> <annotation>caligraphic_R start_POSTSUBSCRIPT 3 end_POSTSUBSCRIPT ( italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT ), italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT ) )</annotation></semantics></math></p></td><td><p>Regularization for encouraging some kinds of similarity between BM and AM on BS</p></td></tr><tr><td><p><math><semantics><mrow><msub><mi>𝒵</mi> <mi>𝐱</mi></msub> <mo>⁢</mo> <mrow><mo>(</mo><msub><mi>𝐱</mi> <mi>ε</mi></msub><mo>)</mo></mrow></mrow> <annotation-xml><apply><apply><csymbol>subscript</csymbol> <ci>𝒵</ci> <ci>𝐱</ci></apply> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <ci>𝜀</ci></apply></apply></annotation-xml> <annotation>\mathcal{Z}_{\mathbf{x}}(\mathbf{x}_{\varepsilon})</annotation> <annotation>caligraphic_Z start_POSTSUBSCRIPT bold_x end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT )</annotation></semantics></math></p></td><td><p>Constraint on <math><semantics><msub><mi>𝐱</mi> <mi>ε</mi></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <ci>𝜀</ci></apply></annotation-xml> <annotation>\mathbf{x}_{\varepsilon}</annotation> <annotation>bold_x start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT</annotation></semantics></math>, such as the representation domain</p></td></tr><tr><td><p><math><semantics><mrow><msub><mi>𝒵</mi> <mi>𝐰</mi></msub> <mo>⁢</mo> <mrow><mo>(</mo><msub><mi>𝐰</mi> <mi>ε</mi></msub><mo>)</mo></mrow></mrow> <annotation-xml><apply><apply><csymbol>subscript</csymbol> <ci>𝒵</ci> <ci>𝐰</ci></apply> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply></annotation-xml> <annotation>\mathcal{Z}_{\mathbf{w}}(\mathbf{w}_{\varepsilon})</annotation> <annotation>caligraphic_Z start_POSTSUBSCRIPT bold_w end_POSTSUBSCRIPT ( bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT )</annotation></semantics></math></p></td><td><p>Constraint on <math><semantics><msub><mi>𝐰</mi> <mi>ε</mi></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></annotation-xml> <annotation>\mathbf{w}_{\varepsilon}</annotation> <annotation>bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT</annotation></semantics></math>, such as sparsity or bounded</p></td></tr></tbody></table>

The life-cycle of a machine learning system mainly consists of five stages, including pre-training, training, post-training, deployment, and inference stage. According to the stages at which the adversarial phenomenon exists, AML can be categorized to three attack paradigms, as shown in Figure 1:  

1) Backdoor attacks: It aims to generate an adversarial model $f_{\mathbf{w}_{\varepsilon}}(\cdot)$ (also called backdoored model), such that at the inference stage, it performs well on benign data $\mathbf{x}_{0}$, while predicts the adversarial sample $\mathbf{x}_{\varepsilon}$ as the target label $y_{\varepsilon}$. It is implemented by manipulating the training dataset or the training procedure by the attacker. According to whether the attacker has control over the training process, the backdoor attack can further be divided into data-poisoning based backdoor attack and training-controllable based backdoor attack. The former mainly focuses on the poisoned sample injection at the pre-training stage, while the latter mainly focuses on the training-controllable based backdoor injection at the training stage. Both these attacks include backdoor activation at the inference stage. Its formulation is derived by specifying the general formulation (1) as follows:

$$
\displaystyle\left\{\begin{aligned} \mathcal{S}(\mathbf{x}_{0},\mathbf{x}_{%
\varepsilon};\mathbf{w}_{0},\mathbf{w}_{\varepsilon})&=&\mathcal{D}_{\mathbf{x%
}}(\mathbf{x}_{0},\mathbf{x}_{\varepsilon}),\\
\mathcal{C}(\mathbf{x}_{0},y_{0};\mathbf{w}_{0},\mathbf{w}_{\varepsilon})&=&%
\mathcal{L}_{\mathcal{C}_{A}}(f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{0}),y_{%
0}),\\
\mathcal{I}(\mathbf{x}_{\varepsilon},y_{\varepsilon};\mathbf{w}_{0},\mathbf{w}%
_{\varepsilon})&=&\mathcal{L}_{\mathcal{I}_{A}}(f_{\mathbf{w}_{\varepsilon}}(%
\mathbf{x}_{\varepsilon}),y_{\varepsilon}).\end{aligned}\right.
$$

$\mathcal{D}_{\mathbf{x}}(\mathbf{x}_{0},\mathbf{x}_{\varepsilon})$ encourages the stealthiness that the poisoned sample $\mathbf{x}_{\varepsilon}$ should be similar with the benign sample $\mathbf{x}_{0}$. $\mathcal{L}_{\mathcal{C}_{A}}(f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{0}),y_{%
0})$ ensures that the prediction on $\mathbf{x}_{0}$ by $f_{\mathbf{w}_{\varepsilon}}(\cdot)$ should be consistent with the ground-truth label $y_{0}$ which is annotated by humans. $\mathcal{L}_{\mathcal{I}_{A}}(f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{%
\varepsilon}),y_{\varepsilon})$ ensures that the prediction on $\mathbf{x}_{\varepsilon}$ by $f_{\mathbf{w}_{\varepsilon}}(\cdot)$ should be the adversarial label $y_{\varepsilon}$, which is inconsistent with $y_{0}$. Since the backdoor attack doesn’t require a benign model $f_{\mathbf{w}_{0}}(\cdot)$ as input, the benign model weight $\mathbf{w}_{0}$ doesn’t occur in the above equations.

2) Weight attacks: It describes that given the benign model $f_{\mathbf{w}_{0}}(\cdot)$ trained on the benign dataset $D_{0}$, the attacker aims at slightly modifying the model parameters to obtain an adversarial model $f_{\mathbf{w}_{\varepsilon}}(\cdot)$. Consequently, at the inference stage, its predictions on adversarial inputs or target benign inputs become the target label $y_{\varepsilon}$, while the predictions on other benign inputs are still their ground-truth labels. Weight attacks can occur both at the post-training and deployment stages. At the post-training stage, the attacker has the authority to directly modify the parameters of benign model in the continuous space, dubbed as weight attack injection via parameter-modification. At the deployment stage, the benign model is deployed in the hardware device ($e.g.$, intelligent mobile or camera). In this case, the attack can modify the model parameters in the memory by flipping bit values in the discrete space, dubbed as weight attack injection via bit-flip. Both these attacks include weight attack activation at the inference stage. Its formulation could be obtained by specifying the general formulation (1) of AML as follows:

$$
\displaystyle\left\{\begin{aligned} \mathcal{S}(\mathbf{x}_{0},\mathbf{x}_{%
\varepsilon};\mathbf{w}_{0},\mathbf{w}_{\varepsilon})&=&\mathcal{D}_{\mathbf{x%
}}(\mathbf{x}_{0},\mathbf{x}_{\varepsilon})+\mathcal{D}_{\mathbf{w}}(\mathbf{w%
}_{0},\mathbf{w}_{\varepsilon}),\\
\mathcal{C}(\mathbf{x}_{0},y_{0};\mathbf{w}_{0},\mathbf{w}_{\varepsilon})&=&%
\mathcal{L}_{\mathcal{C}_{B}}(f_{\mathbf{w}_{0}}(\mathbf{x}_{0}),y_{0})+%
\mathcal{L}_{\mathcal{C}_{A}}(f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{0}),y_{%
0}),\\
\mathcal{I}(\mathbf{x}_{\varepsilon},y_{\varepsilon};\mathbf{w}_{0},\mathbf{w}%
_{\varepsilon})&=&\mathcal{L}_{\mathcal{I}_{A}}(f_{\mathbf{w}_{\varepsilon}}(%
\mathbf{x}_{\varepsilon}),y_{\varepsilon}).\end{aligned}\right.
$$

Since the weight attacks require both the benign model $f_{\mathbf{w}_{\varepsilon}}(\cdot)$ and the benign data $(\mathbf{x}_{0},y_{0})$ as inputs, and outputs the adversarial model $f_{\mathbf{w}_{\varepsilon}}(\cdot)$ or the adversarial sample $\mathbf{x}_{\varepsilon}$, both $\mathbf{w}_{\varepsilon}$ and $\mathbf{w}_{0}$ occur in above equations. Similar to $\mathcal{D}_{\mathbf{x}}(\mathbf{x}_{0},\mathbf{x}_{\varepsilon})$, $\mathcal{D}_{2}(\mathbf{w}_{0},\mathbf{w}_{\varepsilon})$ encourages the stealthiness that the adversarial model weight $\mathbf{w}_{\varepsilon}$ should be close to the benign model weight $\mathbf{w}_{0}$. $\mathcal{L}_{\mathcal{C}_{B}}(f_{\mathbf{w}_{0}}(\mathbf{x}_{0}),y_{0})$ ensures that the attacked model $f_{\mathbf{w}_{0}}(\cdot)$ must perform normally on benign data $(\mathbf{x}_{0},y_{0})$, which is a hard constraint. The effects of $\mathcal{L}_{\mathcal{C}_{A}}(f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{0}),y_{%
0})$ and $\mathcal{L}_{\mathcal{I}_{A}}(f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{%
\varepsilon}),y_{\varepsilon})$ have been described in the above paragraph.

3) Adversarial examples: It describes that given a benign model $f_{\mathbf{w}_{0}}(\cdot)$, the attacker aims at slightly modifying one benign sample $\mathbf{x}_{0}$ to obtain a corresponding adversarial sample $\mathbf{x}_{\varepsilon}$, such that the prediction $f_{\mathbf{w}_{0}}(\mathbf{x}_{\varepsilon})$ is different with the ground-truth label $y_{0}$ or same with the adversarial label $y_{\varepsilon}$. Different from backdoor attacks and weight attacks, adversarial examples only happen at the inference stage. Its formulation could be obtained by specifying the general formulation (1) of AML as follows:

$$
\displaystyle\left\{\begin{aligned} \mathcal{S}(\mathbf{x}_{0},\mathbf{x}_{%
\varepsilon};\mathbf{w}_{0},\mathbf{w}_{\varepsilon})&=&\mathcal{D}_{\mathbf{x%
}}(\mathbf{x}_{0},\mathbf{x}_{\varepsilon}),\\
\mathcal{C}(\mathbf{x}_{0},y_{0};\mathbf{w}_{0},\mathbf{w}_{\varepsilon})&=&%
\mathcal{L}_{\mathcal{C}_{B}}(f_{\mathbf{w}_{0}}(\mathbf{x}_{0}),y_{0}),\\
\mathcal{I}(\mathbf{x}_{\varepsilon},y_{\varepsilon};\mathbf{w}_{0},\mathbf{w}%
_{\varepsilon})&=&\mathcal{L}_{\mathcal{I}_{B}}(f_{\mathbf{w}_{0}}(\mathbf{x}_%
{\varepsilon}),y_{\varepsilon}).\end{aligned}\right.
$$

Since the inference-time adversarial example is conducted only on the benign model, the adversarial model weight $\mathbf{w}_{\varepsilon}$ doesn’t occur in above equations. $\mathcal{L}_{\mathcal{I}_{B}}(f_{\mathbf{w}_{0}}(\mathbf{x}_{\varepsilon}),y_{%
\varepsilon})$ encourages that the prediction on $\mathbf{x}_{\varepsilon}$ by $f_{\mathbf{w}_{0}}(\cdot)$ should be the adversarial label $y_{\varepsilon}$, which is inconsistent with $y_{0}$.

For clarity, we summarize all specified formulations presented in Eqs. (2), (3), (4) in Table II, as well as some additional regularization or constraints.

![Refer to caption](https://arxiv.org/html/2302.09457v2/extracted/5330208/imgs/backdoor-taxonomy.png)

Refer to caption

## III Attack at the Pre-training Stage

Before training large-scale deep models, $i.e.$, pre-training stage, it is necessary to collect the training dataset and then preprocess the dataset to adapt the model. In practice, the user may download an open-sourced dataset from an unverified source or buy data from an untrustworthy third-party data supplier. Considering the data scale, it is difficult to thoroughly check the data quality, or distinguish malicious noises from random noises. In this scenario, the attacker has the chance to manipulate partial data to generate poisoned samples to achieve the malicious goal. After training with the poisoned dataset, the backdoor can be injected into the trained model. We refer to this type of attack as data-poisoning based backdoor attack.

Data-poisoning based backdoor attacks can be separated into two independent tasks: malicious data poisoning ($i.e.$, generating poisoned samples) and normal model training respectively. Since the attacker can only access and manipulate the training dataset, while the training process is out of control, we mainly focus on the former task (dubbed poisoned data injection) in this section.

### III-A Formulation and Categorization

Formulation. Data-poisoning based backdoor generation focuses on generating poisoned samples $D_{\varepsilon}=\{(\mathbf{x}_{\varepsilon},y_{\varepsilon})\}$, which can be formulated as follows:

$$
\displaystyle\mathbf{x}_{\varepsilon}=g_{3}\big{(}g_{1}(\varepsilon),g_{2}(D_{%
0})\big{)},\quad y_{\varepsilon}=g_{4}(y_{0})
$$

where $g_{1}(\cdot)$ denotes the generation of triggers, $g_{2}(\cdot)$ denotes the selection of benign samples to be poisoned, $g_{3}(\cdot)$ denotes the fusion of triggers and selected samples, $g_{4}(\cdot)$ denotes the generation of target labels of poisoned samples.

Categorization. As shown in Figure 2, according to the specifications of $(g_{1},g_{2},g_{3},g_{4})$, we categorize existing works of data-poisoning based backdoor attacks into the following four sub-branches:

1. Backdoor attacks with different triggers according to $g_{1}(\cdot)$, which will be introduced in Section III-B;
2. Backdoor attacks with different selection strategies according to $g_{2}(\cdot)$, which will be introduced in Section III-C;
3. Backdoor attacks with different fusion strategies according to $g_{3}(\cdot,\cdot)$, which will be introduced in Section III-D;
4. Backdoor attacks with different target classes according to $g_{4}(\cdot)$, which will be introduced in Section III-E.

### III-B Trigger Generation

Trigger generation aims to generate triggers ($i.e.$, $g_{1}(\cdot)$ in Eq. (5) that are used to fuse with the benign samples. According to the characteristics of triggers, existing works can be categorized from the following perspectives.

#### III-B1 Visible v.s. Invisible Trigger

According to the trigger visibility with respect to human’s visual perception, the trigger can be categorized into visible and invisible trigger.

##### Visible trigger

Visible trigger means that the modification of the original sample $\mathbf{x}_{\varepsilon}-\mathbf{x}_{0}$ can be realized by human visual perception, but it will not interfere with human’s prediction, $i.e.$, a human can always predict the correct label regardless of whether there is a trigger or not. The first visible trigger is adopted by BadNets [^88] designed, which generates poisoned image $\mathbf{x}_{\varepsilon}$ by stamping a small visible grid patch or a sticker ($e.g.$, yellow square, bomb, flower) on the benign image $\mathbf{x}_{0}$. Since that, the triggers with similar visible patterns have been widely used in many subsequent works [^196] [^173] [^141]. Besides, in the backdoor attacks against the 3D cloud point classification task, the visible additional 3D points are adopted as the backdoor trigger in a few existing works [^129] [^257].

##### Invisible trigger

Although the visible trigger seems to be harmless from a human’s perspective, its high-frequency presence in multiple samples with the same label may still raise human suspicion. Therefore, some invisible triggers have been developed to make backdoor attacks less detectable by human inspection, while maintaining the high attack success rate. There are four main strategies to achieve trigger invisibility.

- Alpha blending: Blended [^41] firstly adopts the alpha blending strategy to fuse the trigger into the benign image. Specifically, the $g_{1}$ function in Eq. (5) is specified as the $\alpha$ -blending function, $i.e.$, $\mathbf{x}_{\varepsilon}=\alpha\mathbf{x}_{0}+(1-\alpha)$, with $\alpha\in[0,1]$, and the trigger visibility is negatively correlated with $\alpha$.
- Digital steganography: [^8] [^13]: it is the technology of concealing secret information into some digital media ($e.g.$, image, video), while avoiding obvious changes in the media. By treating the trigger as secret information, digital steganography is a perfect tool to generate an invisible trigger. For example, Li $et~{}al.$ [^126] utilize the widely used steganography algorithm, $i.e.$, the least significant bit (LSB) substitution [^27], to insert the trigger information into the least significant bit of one pixel to avoid the visible change in the RGB space. The sample-specific backdoor attack (SSBA) method [^134] adopts a double-loop auto-encoder [^220] that is firstly proposed for digital steganography, to merge the trigger information into the benign image, such that invisible and sample-specific triggers could be generated.
- Adversarial perturbation: since most types of adversarial perturbations are imperceptible to humans, they can be used as effective tools to generate invisible triggers. One typical example is AdvDoor [^293], which adopts the targeted universal adversarial perturbation (TUAP) [^162] as the trigger. The invisibility and the stable mapping from the TUAP to the target class satisfied the requirement of the backdoor attack with invisible triggers. Besides, adversarial perturbation is a commonly used technique in label-consistent backdoor attacks ($e.g.$, [^200] [^176]). The general idea is that the original feature of a target image is erased by invisible adversarial perturbation, while the feature of a source image with trigger is inserted. Consequently, the generated poisoned image has a similar visual appearance to the target image, but a similar feature to source image with trigger, and is labeled as the target class.
- Slight transformation: as human eyes are insensitive to slight spatial or color distortion, some slight transformations are adopted as triggers, such as the image warping in [^174], or style transfer in [^45].

#### III-B2 Non-semantic v.s. Semantic Trigger

According to whether the trigger has semantic meaning, the trigger can be categorized into non-semantic and semantic trigger.

##### Non-semantic trigger

Non-semantic trigger means that the trigger has no semantic meaning, such as a small checkerboard grid or random noise. Since most of the existing backdoor attacks adopt non-semantic triggers, here we don’t expand the descriptions.

##### Semantic trigger

Semantic trigger means that the trigger corresponds to some semantic objects with particular attributes contained in the benign sample, such as the red car in one image, or a particular word in one sentence. This kind of semantic trigger is first adopted in backdoor attacks against several security-critical natural language processing (NLP) tasks ($e.g.$, sentiment analysis [^26] or text classification [^26], toxic comment detection [^294], neural machine translation (NMT), and [^42], where a particular word or a particular sentence was used as the trigger. Then, the semantic trigger was extended into the computer vision tasks, where some particular semantic objects in the benign image were treated as the trigger, such as “cars with racing stripe” [^10]. VSSC [^230] first proposes to edit the source image by image editing methods to generate semantic triggers that are in harmony with the remaining visual content in the image to ensure visual stealthiness. Since the semantic trigger is chosen among the objects that already exist in the benign image, a unique feature of this kind of backdoor attack is that the input image is not modified, while only the label is changed to the target class, which increases the stealthiness, compared to backdoor attacks with non-semantic triggers.

#### III-B3 Manually designed Trigger v.s. Learnable Trigger

According to how triggers are generated, we categorize existing works into manually designed and learnable trigger.

##### Manually designed trigger

: Manually designed trigger means that the trigger is manually specified by the attacker, such as grid square trigger [^88], cartoon pattern [^41], random noise [^196], ramp signal [^14], 3D binary pattern [^237], $etc.$ When designing these triggers, the attacker often doesn’t take into account the benign training dataset to be poisoned or any particular model, thus there is no guarantee about the stealthiness or effectiveness of these triggers.

##### Learnable trigger

Learnable trigger also called optimization-based trigger, denotes that the trigger is generated through optimizing an objective function that is related to the benign sample or a model, to achieve some particular goals ($e.g.$, enhancing the stealthiness or attack success rate). For example, in label-consistent attacks [^200], the trigger is often generated by minimizing the distance between the poisoned sample and the target benign sample in the original input space, and the distance between the poisoned sample and the benign source sample in the feature space of a pre-trained model. Besides, another typical optimized trigger is the universal adversarial perturbation $w.r.t.$ the target class ($e.g.$, [^293], [^306], [^301]), which is optimized based on a set of benign samples and a pre-trained model.

#### III-B4 Digital v.s. Physical Trigger

According to the scenario in which the trigger works, existing works can be categorized to digital and physical trigger.

##### Digital trigger

Most existing backdoor attack works only consider the digital trigger, $i.e.$, the trigger in both training and inference stages only exist in digital space.

##### Physical trigger

In contrast, the physical backdoor attack where some physical objects are used as the trigger at the inference stage has been rarely studied. There are a few attempts focusing on some particular tasks, such as face recognition or autonomous driving. For example, the work [^243] presents a detailed empirical study of the backdoor attack against the face recognition model in the physical scenario. Seven physical objects at different facial locations are used as triggers, and the studies reveal that the trigger location is critical to the attack performance. The physical transformations for backdoors (PTB) method [^272] also studies the physical backdoor attack against face recognition, and introduces diverse transformations ($e.g.$, distance, rotation, angle, brightness, and Gaussian noise) on poisoned facial images, to enhance the robustness to distortions in the physical scenario. Besides, the work [^92] explores physical backdoor attacks against lane-detection models. It designed a set of two traffic cones with specific shapes and positions as the trigger and changed the output lane in poisoned samples. VSSC [^230] achieves physical attack by automatically editing original images in the digital space.

### III-C Sample Selection Strategy

This part focuses on selecting appropriate samples to be poisoned from the benign dataset $D_{0}$, $i.e.$, $g_{2}(D_{0})$ in Eq. (5). There are two types of strategies adopted by existing works: random selection and non-random selection strategies.

#### III-C1 Random Selection Strategy

Random selection is the most widely adopted strategy in the field of backdoor attacks. Just as its name implies, the attacker often randomly selects samples to be poisoned, disregarding the varying importance of each poisoned sample in terms of backdoor injection. The proportion of poisoned samples to all training samples, $i.e.$, $|D_{\varepsilon}|/|D_{0}|$, is called the poisoning ratio. Since most existing backdoor attacks adopted this strategy, we don’t expand the details.

#### III-C2 Non-random Selection Strategy

Recent studies have started to explore the importance of different samples for backdoor attacks and propose different non-random selection strategies to select samples to be poisoned instead of selecting randomly. Filtering-and-updating strategy (FUS) [^255] adopts forgetting events [^223] to indicate the contribution of each poisoned sample and iteratively filters and updates a sample pool. Learnable poisoning sample selection strategy (LPS) [^313] learns the mask through a min-max optimization, where the inner problem maximizes loss w.r.t. the mask to identify hard poisoned samples by impeding the training objective, while the outer problem minimizes the loss w.r.t. the model parameters. An improved filtering and updating strategy (FUS++) [^138] combines the forgetting events and curvature of different samples to conduct a simple yet efficient sample selection strategy. The representation distance (RD) score is proposed in [^253] to identify the poisoning samples that are more crucial to the success of backdoor attacks. Wu $et~{}al.$ [^253] propose a confidence-based scoring methodology to measure the contribution of each poisoned sample based on the distance posteriors and proposed a greedy search algorithm to find the most informative samples for backdoor injection. Proxy-Free Strategy (PFS) [^137] utilizes a pre-trained feature extractor to compute the cosine similarity between clean and corresponding poisoned samples and then selects poisoned samples with high similarity and diversity.

### III-D Trigger Fusion Strategy

According to different fusion strategies that fuse the triggers and selected samples, $i.e.$, $g_{3}(\cdot,\cdot)$ in Eq. (5), we can categorize existing works from the following perspectives.

#### III-D1 Additive v.s. Non-additive Trigger

According to the fusion method of trigger and image, the trigger can be categorized into additive and non-additive trigger.

##### Additive trigger

Additive trigger means that the poisoned image is the additive fusion of the benign image and trigger. Specifically, the fusion function $g_{2}$ in Eq. (5) is specified as an additive function, $i.e.$, $\mathbf{x}_{\varepsilon}=\alpha g_{0}(\mathbf{x}_{0})+(1-\alpha)g_{1}(%
\boldsymbol{\varepsilon})$ with $\alpha\in(0,1)$. Since most existing triggers belong to this type, and there is no much variation of $g_{1}$, here we don’t expand the details.

##### Non-additive trigger

Non-additive trigger denotes that the poisoned image is not the direct additive fusion of the trigger and the input image, but is generated by some types of non-additive transformation function. There are two types of transformations in existing works, including the color/style/attribute transformation, and the spatial transformation. In terms of the former type, FaceHack [^197] utilizes a particular facial attribute as the trigger in the face recognition task, such as the age, expression or makeup; DFTS [^45] uses a particular image style as the trigger. In terms of the latter type, WaNet [^174] utilizes image warping as the trigger based on a warping function and a pre-defined warping field.

#### III-D2 Sample-agnostic v.s. Sample-specific Trigger

According to whether the trigger is dependent on the image, the trigger can be categorized into sample-agnostic and sample-specific trigger.

##### Sample-agnostic trigger

Sample-agnostic trigger means that the trigger $\mathbf{x}_{\varepsilon}-\mathbf{x}_{0}$ is independent with the benign sample $\mathbf{x}_{0}$, $i.e.$, $\mathbf{x}_{\varepsilon}^{(i)}-\mathbf{x}_{0}^{(i)}=\mathbf{x}_{\varepsilon}^{%
(j)}-\mathbf{x}_{0}^{(j)},\forall i\neq j$. It could be implemented by setting the fusion function $g_{2}$ as a linear function. Since most existing backdoor attacks adopted this type, here we don’t expand the details.

##### Sample-specific trigger

Sample-specific trigger means that the trigger $\mathbf{x}_{\varepsilon}-\mathbf{x}_{0}$ is related to the benign sample $\mathbf{x}_{0}$, $i.e.$, $\mathbf{x}_{\varepsilon}^{(i)}-\mathbf{x}_{0}^{(i)}\neq\mathbf{x}_{\varepsilon%
}^{(j)}-\mathbf{x}_{0}^{(j)},\forall i\neq j$. It could be implemented by designing a particular fusion function $g_{2}$, or trigger generation function $g_{1}$. In terms of the fusion function, one typical choice is utilizing the image steganography technique. For example, Li $et~{}al.$ [^126] adopt the least significant bit (LSB) steganography technique [^27] to insert the binary code of the trigger into the benign image. Since the least significant bits vary in different benign images, $\mathbf{x}_{\varepsilon}-\mathbf{x}_{0}$ is specific to each $\mathbf{x}_{0}$. The SSBA attack [^134] adopts a double-loop auto-encoder [^220] based steganography technique, to merge the trigger information into the benign image to obtain specific $\mathbf{x}_{\varepsilon}-\mathbf{x}_{0}$ for each $\mathbf{x}_{0}$. Another technique is transformation, where each benign sample after a particular transformation is treated as one poisoned sample ($e.g.$, [^174], [^45]), such that $\mathbf{x}_{\varepsilon}-\mathbf{x}_{0}$ is dependent with $\mathbf{x}_{0}$. In terms of the trigger generation function, $g_{1}$ could take the benign sample $\mathbf{x}_{0}$ as one of the input arguments to generate sample-specific trigger. For example, Poison ink [^289] extracts a black and white edge image from one benign image, then colorizes the edge image with a particular color as the trigger. Since the edge image is specific in each benign image, the trigger is also sample-specific.

#### III-D3 Static v.s. Dynamic Trigger

According to whether the trigger changes across different samples, the trigger can be categorized into static and dynamic trigger.

##### Static trigger

Static triggerdenotes that the trigger is fixed across the training samples, including the pattern and location. Most early backdoor attacks, such as BadNets [^88], Blended [^41], SIG [^14], adopt static triggers. However, poisoned samples with static triggers are likely to show very stable and discriminative characteristics compared to benign samples. Consequently, these characteristics could be easily identified and utilized by the defender.

##### Dynamic trigger

Dynamic trigger assumes that there is variation or randomness of the trigger across the poisoned samples, which could be implemented by adding randomness into the fusion function $g_{2}$ or the trigger transformation $g_{1}$. Compared with the static trigger, it may be more difficult to form stable mapping from the dynamic trigger to the target class, but it will be more stealthy to evade the defense. For example, the random backdoor attack [^196] randomly samples the trigger pattern from a uniform distribution and the trigger location from a pre-defined set for each poisoned sample. The DeHiB method [^274] which attacks the semi-supervised learning models also poisons the unlabeled data by inserting triggers at a random location. In Refool [^149], some hyper-parameters for generating the reflection trigger are randomly sampled from some uniform distributions. The composite attack [^141] defines the trigger as the composition of two existing objects in benign images, without restrictions on the objects’ appearances or locations.

### III-E Target Label Generation

According to different target classes of poisoned samples, $i.e.$, $g_{4}(\cdot)$ in Eq. (5), we can categorize existing works from the following perspectives.

#### III-E1 Single-target v.s. Multi-target

##### Single-target class

Single-target class describes that all poisoned training samples are labeled as one single target class at the training stage, and all poisoned samples are expected to be predicted as that target class at the inference stage. It is also called all-to-one setting. Most existing backdoor attacks adopt this setting, thus we don’t expand the details.

##### Multi-target classes

means that there are multiple target classes. Furthermore, according to the number of triggers, there are two sub-settings. One is all-to-all setting [^88], where with the same trigger, samples from different source classes will be predicted as different target classes. The other setting is multiple target classes together with multiple triggers. It could be achieved by simply extending one single trigger in the single-target class setting to multiple triggers. Besides, the conditional backdoor generating network (c-BaN) method [^196] and the Marksman attack [^58] propose to learn a class conditional trigger generator, such that the attacker could generate a class conditional trigger to fool the model to any arbitrary target class, rather than a pre-defined target class.

#### III-E2 Label-consistent v.s. Label-inconsistent

##### Label-inconsistent

Label-inconsistent denotes that the poisoned sample is generated based on benign samples from other classes ($i.e.$, not target class), but its label is changed to the target class, such that the visual content is inconsistent with its label. Since most existing backdoor attacks adopted this setting, here we don’t present more details.

##### Label-consistent

Label-consistent (also called clean-label attack) means that the poisoned sample is generated based on benign samples from the target class, and the original label is not changed, such that the visual content of the poisoned sample is consistent with its label. Consequently, it is more stealthy than the label-inconsistent poisoned sample under human inspection. Zhao $et~{}al.$ [^301] evaluate the label-consistent attack against video recognition tasks. The benign target video is first attacked by adversarial attacks, and the universal adversarial perturbation $w.r.t.$ the target class is generated based on several benign videos as the trigger, then the attacked target video and the trigger are combined to obtain the poisoned video. Refool [^149] generates the reflection image as the trigger, then combines it with one benign target image to obtain one poisoned image. Due to the transparency of the reflection image, the poisoned image has a similar visual appearance to the original benign image. The hidden trigger attack [^195] fuses one benign target image and one source image with trigger through a strategy like adversarial attack: given a pre-trained model, enforcing the feature representation of the combined image ($i.e.$, the poisoned image) to be close to that of the source image with trigger, while encouraging that the combined image and the benign target image look similar in the original RGB space. Consequently, the model could learn the mapping from the source image with the trigger to the target class based on the generated poisoned images, and it is likely to predict any image from the source class with the trigger as the target class. The invisible poison attack [^176] firstly transforms a visible trigger image to a noise image with limited magnitude through a pre-trained auto-encoder, then inserts the noised trigger into one benign target image to obtain one poisoned image with a similar appearance. The sleeper agent attack [^213] proposes a new setting that given a fixed trigger, the attacker aims to learn a perturbation on the training set, such that for any model trained on this perturbed training set, the label-consistent backdoor from the source class to the target class can be activated by the trigger. It is formulated as a bi-level minimization problem $w.r.t.$ the data perturbation and the parameters of the surrogate model.

## IV Attack at the Training Stage

The training stage involves the training loss, training algorithm and executing the training procedure. In practice, due to the lack of the computational resource, the user usually outsources the training process to a third-party training platform, or downloads a pretrained model from unverified sources, or cannot control the whole training process ($e.g.$, federated learning [^114]). These situations leave the attacker a chance to inject backdoor at the training stage. In addition to manipulating the triggers or labels as did in data-poisoning based backdoor attacks, this threat model assumes that the attacker has the total control over the whole training process and outputs a backdoored model, dubbed as training-controllable based backdoor attack.

### IV-A Formulation and Categorization

Formulation. According to Eq. (2), the general formulation of training-controllable based backdoor attack, is as follows:

$$
\displaystyle\underset{\{\mathbf{x}_{\varepsilon}^{(i)}\}_{i=1}^{N_{\epsilon}}%
\in\mathcal{Z}_{\mathbf{x}},\mathbf{w}_{\varepsilon}\in\mathcal{Z}_{\mathbf{w}%
}}{\arg\min}~{}\frac{1}{N_{0}}\sum\nolimits_{i=1}^{N_{0}}\lambda_{\mathcal{C}_%
{A}}\mathcal{L}_{\mathcal{C}_{A}}\big{(}f_{\mathbf{w}_{\varepsilon}}(\mathbf{x%
}_{0}^{(i)}),y_{0}^{(i)}\big{)}
$$
 
$$
\displaystyle+\frac{1}{N_{\varepsilon}}\sum\nolimits_{i=1}^{N_{\varepsilon}}%
\big{[}\mathcal{D}_{\mathbf{x}}\big{(}\mathbf{x}_{0}^{(i)},\mathbf{x}_{%
\varepsilon}^{(i)}\big{)}+\lambda_{\mathcal{I}_{A}}\mathcal{L}_{\mathcal{I}_{A%
}}\big{(}f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{\varepsilon}^{(i)}),y_{%
\varepsilon}^{(i)}\big{)}
$$
 
$$
\displaystyle+\lambda_{r_{2}}\mathcal{R}_{2}\big{(}f_{\mathbf{w}_{\varepsilon}%
}(\mathbf{x}_{0}^{(i)}),f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{\varepsilon}^%
{(i)})\big{)}\big{]},
$$

where $\lambda_{\mathcal{C}_{A}},\lambda_{\mathcal{I}_{A}},\lambda_{r_{2}}\geq 0$ are trade-off hyper-parameters. Since the attacker needs to poison the dataset and control the training process, we treat both $\mathbf{x}_{\varepsilon}$ and $\mathbf{w}_{\varepsilon}$ as optimized variables.

Categorization. We categorize existing works from the following four perspectives, including the number of attack stages, whether the full training data can be accessed, whether the full training process is controlled, and the controlled components of the training procedure by the attacker.

### IV-B One-stage v.s. Two-stage Training

In this threat model, the attacker will conduct two tasks, including generating poisoned samples $\mathbf{x}_{\boldsymbol{\epsilon}}$, and training the model ($i.e.$, learning $\mathbf{w}_{\boldsymbol{\epsilon}}$).

#### IV-B1 Two-stage training

If this two tasks are conducted sequentially ($i.e.$, separating the problem (6) into two sub-problems $w.r.t.$ $\mathbf{x}_{\boldsymbol{\epsilon}}$ and $\mathbf{w}_{\boldsymbol{\epsilon}}$, respectively), then we call it two-stage training backdoor attack. In this case, any off-the-shelf data-poisoning based backdoor attack strategy could be adopted to finish the first task, while the attacker mainly focuses on the manipulation of the training process, of which the details we will leave to Section IV-E.

#### IV-B2 One-stage training

In contrast, if these two tasks are conducted jointly ($i.e.$, optimizing $\mathbf{x}_{\boldsymbol{\epsilon}}$ and $\mathbf{w}_{\boldsymbol{\epsilon}}$ jointly through solving the problem (6)), then we call it one-stage training backdoor attack. Compared to the two-stage training attack, it is expected to couple the trigger and the model parameters more tightly in the final backdoored model of the one-stage training attack. The input-aware backdoor attack [^173] proposes to jointly learn the model parameters and a generative model that generates the trigger for each training sample. It also controls the training process that if adding Gaussian noise onto the poisoned samples, then their labels are corrected back to the ground-truth labels in the loss function. LIRA [^57] and WB [^56] propose a bi-level minimization problem to jointly learn the trigger generation network and the backdoored model, with the only difference that LIRA adopts the $\ell_{\infty}$ norm while WB utilized the Wasserstein distance to ensure the stealthiness of triggers, respectively. Zhong $et~{}al.$ [^307] designs a sequential structure with a trigger generator ($e.g.$, a U-Net based network) and the victim model, and they are trained jointly. The trigger generator learns a multinomial distribution with three states $\{0,-1,+1\}$ indicating the intensity modification on each pixel, and then a trigger is sampled from this distribution. The attacker also controls the loss to achieve two goals: encouraging the feature representation of poisoned samples to be close to the average feature representation of the benign samples of the target class; and encouraging the sparsity of the trigger. The BaN attack [^196] also adopts such a sequential structure, but the trigger generator maps the random noise to the trigger. Its extension, $i.e.$, c-BaN, adopts a class conditional generator, such that the trigger generator would be specific to each target class in the setting of multi-target classes.

### IV-C Full access v.s. Partial access of training data

#### IV-C1 Full access of training data

Most existing backdoor attacks focus on centralized learning, $i.e.$, the attacker has full access of training data, such that any training data could be manipulated.

#### IV-C2 Partial access of training data

In contrast, in the scenario of distributed learning or federated learning (FL) [^114], which is designed for accelerating the training process or protecting data privacy, the participation of multiple clients means a higher risk of backdoor attack, though the attacker can only access partial training data. In the following, we mainly review the works of backdoor attacks against federated learning. For example, [^15] and [^10] propose a strategy that the malicious agents scaled up the local model updates which contained backdoor information, to dominate the global model update, such that the backdoor could be injected into the global model. The distributed backdoor attack (DBA) [^260] designs a distributed backdoor attack mechanism that multiple attackers insert backdoor into the global model with different local triggers, and shows that the backdoor activated by the global trigger ($i.e.$, the combination of all local triggers) has very high attack success rate in the final trained model. Wang $et~{}al.$ [^229] propose a new backdoor attack paradigm in the FL scenario, called edge-case backdoor attack, which focuses on predicting the data points sampled from the tail of the input data distribution to a target label, without any modification of the input features. Chen $et~{}al.$ [^29] demonstrates the effectiveness of vanilla backdoor attacks against federated meta-learning. Fung $et~{}al.$ [^78] conducts the backdoor attack against federated learning in the sybil setting [^63], where the adversary achieves the malicious goal by joining the federated learning using multiple colluding aliases. It demonstrates that the attack success rate increased with the number of sybils ($i.e.$, malicious clients with poisoned samples). The Neurotoxin attack method [^297] aims to improve the duration of backdoor effect during the federated learning procedure, by restricting the gradients of poisoned samples to ensure that the coordinates of large gradient norms between poisoned gradients and benign gradients (sent from the server) are not overlapped, such that the backdoor effect would not be erased.

### IV-D Full control v.s. Partial control of training process

#### IV-D1 Full control of training process

In the conventional training paradigm, the training process is often finished at one stage by one trainer, and then the trained model is directed deployed. In this case, the attacker has the chance to fully control the training process. Since most training-controllable backdoor attacks belong to this case, here we don’t repeat their details.

#### IV-D2 Partial control of training process

However, sometimes the training process is separated to several stages by different trainers. Consequently, the attacker can only control a partial training process. One typical training paradigm that emerges in recent years is firstly pre-training on a large-scale dataset, and then fine-tuning on a small dataset for different downstream tasks, especially in the natural language processing field. In this case, the attacker controls the pre-training process and aims to train a backdoored pre-trained model. However, the main challenge is how to maintain the backdoor effect after the possible fine-tuning for different downstream tasks. Along with the popularity of the pre-training and then fine-tuning paradigm, the backdoor inserted in a popular pre-trained model will cause long-term and widespread threats. There have been a few attempts. For example, Shen $et~{}al.$ [^203] propose to map some particular tokens ($e.g.$, the classification token in BERT [^111]) to a target output representation in the pre-trained NLP model for the poisoned text with trigger, such that the backdoor could be activated in downstream tasks through the token representation. The poisoned prompt tuning attack [^65] proposes to learn a poisoned soft prompt for a specific downstream task based on a fixed pre-trained model, and when the user uses the pre-trained model and the poisoned prompt together, then the backdoor would be activated by the trigger in the corresponding downstream task. The layer-wise weight poisoning (LWP) attack [^123] studies the setting that the backdoored pre-trained model is obtained by retraining a benign pre-trained model based on the poisoned dataset and the benign training dataset of the downstream task. To enhance the backdoor resistance to fine-tuning for downstream tasks, LWP defines the backdoor loss of each layer, such that the backdoor effect is injected in both lower and higher layers. Another one common training paradigm is firstly training a large model, then conducting model compression to obtain a lightweight model via model quantization [^153] or model pruning [^127]. The work [^222] presents a new threat model in which the attacker controls the training of the large model, and produces a benign large model, but the model after compression became a backdoored model that could be activated by the trigger. It is implemented by jointly taking the uncompressed and possible compressed models into account during the training.

### IV-E Controlling different components of the training procedure

Existing training-controllable backdoor attacks could also be categorized according to the controlled training component during the training procedure, such as training loss, training algorithm, order of poisoned samples.

#### IV-E1 Control training loss

For example, the work [^307] adds two terms into the training loss function to ensure stealthiness, including the number of perturbed pixels in poisoned image, and the intermediate layer’s activation difference between benign and poisoned samples, while the original trigger is sampled from a multinomial distribution, of which the parameters are generated by a generator.

#### IV-E2 Control training algorithm

The bit-per-pixel attack (BppAttack) [^239] firstly adopts image quantization and dithering to generate stealthy triggers, then utilizes the contrastive supervised learning to train the backdoored model, with the modification that the adversarial example (using any adversarial attack method) of each benign training example is also selected as its negative sample. The deep feature space trojan (DFST) attack [^45] designs an iterative attack process between data poisoning and a controlled detoxication step. The detoxication step mitigates the backdoor effect of the simple features of the trigger, such that the model is enforced to learn more subtle and complex features of the trigger in the next round data-poisoning based training. In both WaNet [^174] and Input-Aware [^173], a cross-trigger training mode is adopted in the training procedure: if adding a trigger onto the training sample, then its label is changed to the target class; if further adding a random noise onto the poisoned sample with the trigger, then its label is changed back to the correct label; the probability of adding trigger and random noise is controlled by the attacker. It is claimed in [^174] [^173] that this training mode could enforce trigger nonreusablity and help to evade the defense like Neural Cleanse [^228].

#### IV-E3 Control indices or order of poisoned samples

The data-efficient backdoor attack [^256] controls the choice of which samples to poison according to a filtering-and-updating strategy, which shows improved attack performance compared to the random selection strategy. The batch ordering backdoor (BOB) attack [^209] only controls the batch orders in each epoch during the SGD training process to inject the backdoor, without any manipulations on the features or labels. The key idea is choosing training samples to mimic the gradients of a jointly trained surrogate model based on a poisoned dataset.

## V Attack at the Post-training Stage

After training the model at the training stage, a benign trained model will be obtained at the post-training stage. In this scenario, the attacker can directly modify the parameters of the benign model to inject trojan, dubbed weight attack injection via parameter-modification.

### V-A Formulation and Categorization

Formulation. According to Eq. (3), the general formulation of weight attack injection via parameter-modification, is

$$
\displaystyle\underset{\mathbf{x}_{\varepsilon}\in\mathcal{Z}_{\mathbf{x}},%
\mathbf{w}_{\varepsilon}\in\mathcal{Z}_{\mathbf{w}}}{\arg\min}~{}\mathcal{D}_{%
\mathbf{w}}(\mathbf{w}_{0},\mathbf{w}_{\varepsilon})+\frac{1}{N_{0}}\sum%
\nolimits_{i=1}^{N_{0}}\big{[}\lambda_{\mathcal{C}_{B}}\mathcal{L}_{\mathcal{C%
}_{B}}\big{(}f_{\mathbf{w}_{0}}(\mathbf{x}_{0}^{(i)}),
$$
$$
\displaystyle y_{0}^{(i)}\big{)}+\lambda_{\mathcal{C}_{A}}\mathcal{L}_{%
\mathcal{C}_{A}}\big{(}f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{0}^{(i)}),y_{0%
}^{(i)}\big{)}\big{]}+\frac{1}{N_{\varepsilon}}\sum\nolimits_{i=1}^{N_{%
\varepsilon}}\big{[}\mathcal{D}_{\mathbf{x}}\big{(}\mathbf{x}_{0}^{(i)},%
\mathbf{x}_{\varepsilon}^{(i)}\big{)}
$$
 
$$
\displaystyle+\lambda_{\mathcal{I}_{A}}\mathcal{L}_{\mathcal{I}_{A}}\big{(}f_{%
\mathbf{w}_{\varepsilon}}(\mathbf{x}_{\varepsilon}^{(i)}),y_{\varepsilon}^{(i)%
}\big{)}+\lambda_{r_{2}}\mathcal{R}_{2}\big{(}f_{\mathbf{w}_{\varepsilon}}(%
\mathbf{x}_{0}^{(i)}),f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{\varepsilon}^{(%
i)})\big{)}
$$
 
$$
\displaystyle+\lambda_{r_{3}}\mathcal{R}_{3}\big{(}f_{\mathbf{w}_{\varepsilon}%
}(\mathbf{x}_{0}^{(i)}),f_{\mathbf{w}_{0}}(\mathbf{x}_{0}^{(i)})\big{)}\big{]},
$$

where $\lambda_{\mathcal{C}_{A}},\lambda_{\mathcal{C}_{B}},\lambda_{\mathcal{I}_{A}},%
\lambda_{r_{2}},\lambda_{r_{3}}\geq 0$ are trade-off hyper-parameters. The second term is often specified as a hard constraint to ensure the consistency condition AML.$\mathcal{C}_{B}$, $i.e.$, $\mathcal{L}_{\mathcal{C}_{B}}\big{(}f_{\mathbf{w}_{0}}(\mathbf{x}_{0}),y_{0}%
\big{)}=\delta(\arg\max f_{\mathbf{w}_{0}}(\mathbf{x}_{0})=y_{0})$, where $\delta(a)=0$ if $a$ is true, otherwise $\delta(a)=\infty$. It is a default requirement in weight attack, thus it is omitted hereafter in this section.

Categorization. According to whether the attacker has knowledge of parameter values of the model, we can categorize existing works into white-box and black-box weight attack injection.

### V-B White-box Weight Attack Injection

White-box weight attack injection means that the attacker has access to the parameter values of the bengin model. Liu $et~{}al.$ [^151] observe that the outputs of DNN model with ReLU functions are linearly related to some parameters. Based on this observation, two simple weight attack methods were proposed to achieve targeted predictions of some selected benign samples: the single bias attack (SBA) simply enlarges one bias parameter that is related to the output corresponding to the target class; the gradient descent attack (GDA) modifies some weights using gradient descent algorithm. Zhao $et~{}al.$ [^300] propose an ADMM based framework for solving the optimization problem of weight attack with two constraints: 1) the classification of the other images should be unchanged and 2) the parameter modifications should be minimized.

### V-C Black-box Weight Attack Injection

In contrast to white-box setting, black-box weight attack injection assumes that the attacker does not have any knowledge of parameter values. Subnet Replacement Attack (SRA) method [^187] generates a very narrow subnet given the architecture information of the target model, where the subnet is explicitly trained to be sensitive to trigger only, and then replaces the corresponding parts of the target model with the generated subnet.

## VI Attack at the Deployment Stage

The deployment stage of machine learning life-cycle means that the trained model is deployed in the hardware device ($e.g.$, smartphone, server), where the model weight is stored in the memory with a binary form. In this scenario, the attacker can flip the bits of the model weights in the memory space via physical fault injection techniques to obtain an adversarial model, dubbed weight attack injection via bit-flip.

### VI-A Formulation and Categorization

Formulation. The general formulation of weight attack injection via bit-flip has the same form as parameter-modification, $i.e.$, Eq. (7), with one main difference that there is binary constraint $w.r.t.$  $\mathbf{w}_{\varepsilon}$.

Categorization. According to whether the benign sample is modified by adding a trigger or not, existing weight attacks can be generally partitioned into two categories, including: 1) weight bit-flip without trigger, where $\mathbf{x}_{\varepsilon}=\mathbf{x}_{0}$, with the goal that $f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{\varepsilon})=y_{\epsilon}\neq y_{0}$; 2) weight bit-flip with trigger, where $\mathbf{x}_{\epsilon}\neq\mathbf{x}_{0}$, with the goal that $f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{\varepsilon})=y_{\epsilon}\neq y_{0}$ and $f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{0})=y_{0}$.

### VI-B Weight Bit-flip without Trigger

Weight Bit-Flip without trigger aims to change the predictions of one particular benign sample or a set of benign samples through only manipulating the model weights from $\mathbf{w}_{0}$ to $\mathbf{w}_{\varepsilon}$, while the predictions of other benign samples should not be influenced. The targeted bit-flip attack (T-BFA) method [^193] aims to predict some selected samples as the target class through flipping a few weight bits, and models this task as a binary optimization problem, which is solved by a searching algorithm. The targeted attack with limited bit-flips (TA-LBF) method [^12] uses the similar formulation with T-BFA, but could attack one single selected sample, and utilized a powerful integer programming method called $\ell_{p}$ -Box ADMM [^248] to achieve successful targeted attack with only a few bits flipped.

### VI-C Weight Bit-flip with Trigger

The weight attack with trigger aims to obtain an adversarial model $f_{\mathbf{w}_{\varepsilon}}$ through slightly perturbing the benign model weights $\mathbf{w}_{0}$, such that $f_{\mathbf{w}_{\varepsilon}}(\cdot)$ will be activated by any sample with a particular trigger that is designed by attacker or optimized together with $\mathbf{w}_{\varepsilon}$, while $f_{\mathbf{w}_{\varepsilon}}(\cdot)$ performs normally on benign samples. This type of weight attacks seems to be similar to backdoor attacks, but with the main difference that $\mathbf{w}_{\varepsilon}$ is obtained through manipulating $\mathbf{w}_{0}$, while backdoor attack trains $\mathbf{w}_{\varepsilon}$ from scratch. For example, the Trojaning attack [^148] designs a sequential weight attack method with 3 stages: firstly generates the trigger through maximizing its activation on some selected neurons related to the target class; then recovers some training data through reverse engineering; finally retrains the model based on the recovered training data and its poisoned version with the generated trigger to achieve the targeted attack. It is very practical since no training data is required. The targeted bit trojan (TBT) attack [^192] relaxs the above setting to that some training data points are accessed, but restricts the weight modifications from continuous to bit flip. TBT also adopts a sequential attack procedure with 3 steps: firstly identifying the significant neurons corresponding to the target class according to the gradient magnitude; then generating triggers through maximizing the activation of the identified significant neurons; finally searching and flipping a few critical bits to inject the backdoor with the generated trigger, while keeping the accuracy on some benign samples. The ProFlip attack [^30] adopts the same 3-step procedure with TBT, with different algorithm for each individual stage. The adversarial weight perturbation (AWP) method [^81] proposes to slightly perturb the weights of a trained benign model to inject backdoor through enforcing the prediction of the poisoned sample by the perturbed model to the target class, and encouraging the consistency between the prediction of the benign sample by the benign model and that by the perturbed model. The anchoring attack [^296] has the same goal with AWP, but with a different objective function that enforcing the prediction of the poisoned sample by the perturbed model to the target class and that of the benign sample to the ground-truth class, as well as encouraging the logit consistency between the benign and perturbed models on the benign sample. The handcrafted backdoor attack [^94] proposes a layer-by-layer weight modification procedure from the bottom to top layer, following the rules that there is a negligible clean accuracy drop, and the activation separation between benign and poisoned samples is increased. The initial trigger could also be adjusted to increase the activation separation during the modification procedure. Note that although it is named as backdoor, but it actually is the weight bit flip with trigger. The subnet replacement attack (SRA) [^186] firstly trains a backdoor subnet, which shows high activation for poisoned samples with triggers while low activation for benign samples, then randomly replaces one subnet in the benign model by the backdoor subset and cut off the connection to the remaining part of the model. SRA only needs to know the victim model architecture, rather than model weights required in other weight attacks.

## VII Attack at the Inference Stage

The inference stage is the last stage in the life cycle of machine learning system. Normally, at this stage, test samples are queried through the deployed model to get the predictions. Like other stages, several adversarial phenomena can occur at this stage to achieve malicious goals. First, to accomplish the whole attack process of backdoor attacks, the attackers need to generate poisoned test samples to activate the backdoor injected into the backdoored model, dubbed backdoor attack activation. Similarly, weight attackers also need to activate the effectiveness of weight attacks by specific samples, dubbed weight attack activation. Another scenario is after obtaining a benign model, the attacker has access to modify any benign sample slightly to mislead the model into predicting wrong labels, called adversarial example. Since the core technical of backdoor attacks and weight attacks have been discussed in Sections III - VI, we just detail adversarial examples in this section.

![Refer to caption](https://arxiv.org/html/2302.09457v2/extracted/5330208/imgs/adversarial-taxonomy.png)

Refer to caption

### VII-A Formulation and Categorization

Formulation. According to Eq. (4), the general formulation of adversarial examples at the inference stage is as follows:

$$
\displaystyle\underset{\mathbf{x}_{\varepsilon}\in\mathcal{Z}_{\mathbf{x}}}{%
\arg\min}~{}
$$
 
$$
\displaystyle\mathcal{D}_{\mathbf{w}}(\mathbf{x},\mathbf{x}_{\varepsilon})+%
\lambda_{\mathcal{C}_{B}}\mathcal{L}_{\mathcal{C}_{B}}(f_{\mathbf{w}_{0}}(%
\mathbf{x}_{0}),y_{0})+
$$
 
$$
\displaystyle\lambda_{\mathcal{I}_{B}}\mathcal{L}_{\mathcal{I}_{B}}(f_{\mathbf%
{w}_{0}}(\mathbf{x}_{\varepsilon}),y_{\varepsilon})+\lambda_{r_{1}}\mathcal{R}%
_{1}(f_{\mathbf{w}_{0}}(\mathbf{x}_{0}),f_{\mathbf{w}_{0}}(\mathbf{x}_{%
\varepsilon})),
$$

where $\lambda_{\mathcal{C}_{B}},\lambda_{\mathcal{I}_{B}},\lambda_{r_{1}}\geq 0$ are trade-off hyper-parameters. The second term $\mathcal{L}_{\mathcal{C}_{B}}(f_{\mathbf{w}_{0}}(\mathbf{x}_{0}),y_{0})$ is also specified as a hard constraint, thus it is omitted hereafter in this section.

Categorization. As shown in Figure 3, we present a hierarchical taxonomy of existing inference-time adversarial examples. Specifically, according to the accessed information of the attacker, there are three categories at the first level, as follows:

- White-box adversarial examples: the attacker has sufficient information about the victim model, including architecture and weights, such that the attacker can easily generate adversarial perturbations to cross the decision boundary (see Section VII-B).
- Black-box adversarial examples: the attacker can only access the query feedback returned by the victim model, such that the attacker has to gradually adjust the perturbation to cross the invisible decision boundary (see Section VII-C).
- Transfer-based adversarial examples: the generated adversarial perturbation is not designed for any specific victim model, and the goal is to enhance the probability of directly fooling other unknown models without repeated queries (see Section VII-D).

### VII-B White-Box Adversarial Examples

In this section, we categorize white-box adversarial examples from two different perspectives, including perturbation types and output types. According to different perturbation types, we can categorize white-box adversarial examples into the following five types.

#### VII-B1 Optimization-based vs. Learning-based Perturbation

##### Optimization-based perturbation

Early works in this field mainly focused on directly optimizing the problem (8) to generate one adversarial example $\mathbf{x}_{\varepsilon}$ or adversarial perturbation $\boldsymbol{\varepsilon}$ for each individual benign sample $\mathbf{x}_{0}$. According to different specifications of $\mathcal{D}_{\mathbf{w}}(\mathbf{x},\mathbf{x}_{\varepsilon})$, existing optimization-based works could be partitioned into two categories:

- $\ell_{\infty}$ -norm and gradient sign based methods. Specifically, the attacker set $\mathcal{D}_{\mathbf{w}}(\mathbf{x},\mathbf{x}_{\varepsilon})=\|\mathbf{x}-%
	\mathbf{x}_{\varepsilon}\|_{\infty}$ to restrict the upper bound of the perturbations to ensure the stealthiness. However, since the $\ell_{\infty}$ -norm is non-differentiable, it is infeasible to solve the optimization problem using the widely used gradient-based methods. To tackle this difficulty, the $\ell_{\infty}$ -norm could be moved from the objective function to be a constraint, as follows:
	$$
	\displaystyle\underset{\mathbf{x}_{\varepsilon}\in\mathcal{Z}_{\mathbf{x}}}{%
	\arg\min}~{}\mathcal{L}_{\mathcal{I}_{B}}(f_{\mathbf{w}_{0}}(\mathbf{x}_{%
	\varepsilon}),y_{\varepsilon}),~{}\text{s.t.}~{}\|\mathbf{x}-\mathbf{x}_{%
	\varepsilon}\|_{\infty}\leq\epsilon,
	$$
	where $\epsilon>0$ is an attacker-determined upper bound of the perturbation, which is also called perturbation budget. A series of gradient sign-based methods are proposed to solve the above problem (9). The first attempt is fast gradient sign method (FSGM) [^86], where only one step is moved from $\mathbf{x}_{0}$ following the sign of gradient with the step size $\epsilon$ to obtain $\mathbf{x}_{\varepsilon}$. Consequently, the magnitude of each entry in the adversarial perturbation is $\epsilon$, $i.e.$, the perturbation budget is fully utilized. However, due to the likely non-smoothness of the decision boundary of $f_{\mathbf{w}_{0}}(\cdot)$, the one-step gradient sign direction might be inaccurate to reduce the value of $\mathcal{L}_{\mathcal{I}_{B}}(f_{\mathbf{w}_{0}}(\mathbf{x}_{\varepsilon}),y_{%
	\varepsilon})$. Thus, it is extended to iterative FSGM (I-FGSM) [^116], where there are multiple updating steps with smaller step size, such that the gradient sign direction of each step is more accurate. Note that I-FGSM is renamed as another famous name by [^158]), called projected gradient descent (PGD). Then, several extensions of I-FGSM are proposed to improve attack performance or adversarial transferability, such as momentum iterative FSGM (MI-FGSM) [^60], Nesterov accelerates gradient (NI-FGSM) [^140], Auto-PGD [^50], $etc.$
- $\ell_{2}$ -norm and gradient based methods. Another widely adopted specification of $\mathcal{D}_{\mathbf{w}}(\mathbf{x},\mathbf{x}_{\varepsilon})$ is $\ell_{2}$ norm, $i.e.$, $\mathcal{D}_{\mathbf{w}}(\mathbf{x},\mathbf{x}_{\varepsilon})=\|\mathbf{x}-%
	\mathbf{x}_{\varepsilon}\|_{2}^{2}$. For example, in the DeepFool method [^163], it adopts the $\ell_{2}$ norm, but transforms the loss function $\mathcal{L}_{\mathcal{I}_{B}}(f_{\mathbf{w}_{0}}(\mathbf{x}_{\varepsilon}),y_{%
	\varepsilon})$ to a hard constraint that $\arg\max f_{\mathbf{w}_{0}}(\mathbf{x}_{\varepsilon})\neq y_{0}$. It designs an iterative algorithm to minimize the $\ell_{2}$ distance while moving towards the decision boundary of the benign class $y_{0}$, where in each step the distance between the current solution and the decision boundary has to be approximated. In the C&W- $\ell_{2}$ method [^23], $\mathcal{L}_{\mathcal{I}_{B}}(f_{\mathbf{w}_{0}}(\mathbf{x}_{\varepsilon}),y_{%
	\varepsilon})$ is specified as a differentiable loss function ($e.g.$, cross entropy loss or hinge loss). Consequently, the problem (8) could be directly solved by any off-the-shelf gradient-based method, together with the projection to the constraint space $\mathcal{Z}_{\mathbf{x}}$.

##### Learning-based perturbation

In addition to directly optimizing the problem (8), some methods attempt to utilize the learning-based method to generate adversarial samples or perturbations. Specifically, it is assumed that $\mathbf{x}_{\varepsilon}$ or $\bm{\varepsilon}$ is generated by a parametric model with $\mathbf{x}_{0}$ as the input, $i.e.$,

$$
\displaystyle\mathbf{x}_{\varepsilon}=g_{\boldsymbol{\bm{\theta}}}(\mathbf{x}_%
{0}),~{}\text{or}~{}\mathbf{x}_{\varepsilon}=\mathbf{x}_{0}+g_{\boldsymbol{\bm%
{\theta}}}(\mathbf{x}_{0}).
$$

Then, the task becomes to learn the parameter $\boldsymbol{\bm{\theta}}$, which can be formulated as follows:

$$
\displaystyle\underset{\boldsymbol{\bm{\theta}}}{\arg\min}~{}\frac{1}{n}\sum%
\nolimits_{i=1}^{n}\big{[}
$$
 
$$
\displaystyle\mathcal{D}_{\mathbf{w}}(\mathbf{x}_{0}^{(i)},g_{\boldsymbol{\bm{%
\theta}}}(\mathbf{x}_{0}^{(i)}))+
$$
 
$$
\displaystyle\lambda_{\mathcal{I}_{B}}\mathcal{L}_{\mathcal{I}_{B}}(f_{\mathbf%
{w}_{0}}(g_{\boldsymbol{\bm{\theta}}}(\mathbf{x}_{0}^{(i)})),y_{\varepsilon}^{%
(i)})\big{]},
$$

where $\mathcal{L}_{\mathcal{I}_{B}}$ is often set as the GAN (generative adversarial network) loss or its variants, such as advGAN [^258], PhysGAN [^115], CGAN-Adv [^281], AP-GAN [^298], AC-GAN [^212], MAG-GAN [^34], LG-GAN [^308], AdvFaces [^53], $etc.$

#### VII-B2 Digital v.s. Physical Perturbation

##### Digital perturbation

Digital perturbation means that the whole attack procedure, including perturbation generation and attacking the victim model, is conducted in the digital space. Since there is no perturbation distortion, the attacker can precisely manipulate the perturbation value and only needs to pay attention to generating better perturbations with higher stealthiness and attack success rate.

##### Physical perturbation

Physical perturbation is firstly studied in [^116], aims to attack against the model deployed in the physical scenario ($e.g.$, the face recognition model in mobile phone, or the human detection model in video surveillance system). The whole attack procedure consists of 3 stages, including: a)generating perturbation in digital space; b) transforming the digital perturbation to a physical perturbation ($e.g.$, poster or sticker); c) digitizing the physical perturbation back into the digital space via camera or scanner, and then fooling the attack model. In short, there are two transformations between the initial digital perturbation at the first stage and the final digital perturbation fed into the attacked model, including digital-to-physical (D2P) and physical-to-digital (P2D) transformations. Consequently, some distortions will be introduced on the perturbation, which may cause the attack failure. To achieve a successful physical attack, the attacker has to encourage the generated perturbation to be robust to distortions. Besides, due to these distortions, it is difficult to require the invisibility of perturbation by restricting the $\ell_{p}$ -norm of perturbation as did in most digital attacks. Instead, it is often required that the adversarial examples should look natural or realistic in the physical world. Since most existing works belong to digital attack, in the following we only introduce existing physical attacks. As the special requirement in physical attack is the robustness to the distortions from D2P and P2D transformations, we categorize existing physical attacks into two types: According to the robustness type, we categorize existing physical attacks into two types:

- Robustness to the D2P distortion. It is observed in [^201] that the digital-to-physical distortion is partially caused by the insufficient color space of the printer, and RGB values out of the color space are clipped to bring in color distortion. To tackle it, the concept of non-printability score (NPS) is produced in [^201] to encourage adversarial perturbations to be in the printable color space. Similarly, the adversarial generative nets (AGNs) [^202] trains a generative model using GANs to generate adversarial textures on an eyeglass frame, and restricts the texture within the printable color space to resist color distortion. The method SLAP [^155] adopts the projector to project the digital adversarial perturbation onto real-world objects to get physical adversarial examples. It extends the NPS concept to the projectable colors, by considering the factors of projector distance, ambient light, camera exposure, as well as color and material properties of the projection surface. The work [^245] adopts a conditional variational autoencoder (CVAE) to learn adversarial perturbation sets based on the pair of benign and adversarial images. Based on the multi-illumination dataset of scenes captured in the wild, the CVAE can generate adversarial perturbations that are robust to different color distortions. The work [^104] utilized the generative adversarial network (GAN) [^85] to simulate the color distortion between the original digital image and the corresponding physical image obtained through the D2P and P2D transformations and without spatial transformations. Consequently, the trained GAN model can generate images with similar color distortion in physical scenario. Then, the generated color-distorted image is used as the input to generate adversarial perturbations. However, due to the time cost of manually preparing the physical images through printing and scanning, the training set of GAN cannot be too large, likely causing the overfitting to the attacked image, the printing and scanning devices and the attacked model. The class-agnostic and model-agnostic meta learning (CMML) method [^75] adopts a GAN model to simulate the color distortion, and trains the GAN model based on limited training physical images to improve the generalization to different classes and different attacked models. The curriculum adversarial attack (CAA) method [^305] designs a D2P module based on a multi-layer perception model, to simulate two types of chromatic aberration of stickers, including the fabrication error induced by printers and the photographing error caused by cameras.
- Robustness to the physical-to-digital (P2D) distortion. Two major sources of the P2D distortion include the relative location variation between the physical perturbation and the digitizing device ($e.g.$, camera or phone), and the environmental variations ($e.g.$, ambient or camera light). The formal variation can be modeled as spatial transformations, and the expectation over transformation (EOT) $w.r.t.$ the original adversarial loss is proposed in [^9] to encourage the robustness to different spatial P2D distortions. Then, EOT loss is extended in several subsequent works with different transformations. For example, RP2 [^70] extends EOT loss by adding physical images to the transformation sets. The RP2 is further extended in [^69] from the classification to the detection task by adding more constraints on object positions. The work [^265] aims to attack human detectors in the physical world. It enriches EOT loss by utilizing the thin plate spline (TPS) transformation to model non-rigid object deformation ($e.g.$, the T-shirt), as well as color transformation. The universal physical camouflage attack (UPC) [^97] models the non-rigid deformation by a series of geometric transformations ($i.e.$, cropping, resizing, affine tomography). The ShapeShifter method [^37] adds the masking operation into the EOT loss. The work [^254] proposes a randomized rendering function to model the scaling, translating, and augmentation transformations together. The work [^67] attacks the road sign in the physical world by simultaneously considering rotation, scaling, and color shift in the EOT loss, as well as a random background sampled in the physical world. The ERCG method [^302] designs rescaling and perspective transformations based on the estimated location and perspective of the target object in the image into EOT loss. In [^198], instead of printing adversarial perturbations on a sticker as did in most other physical attack works, the adversarial light signal that illuminates the objects is generated to achieve physical attacks, implemented by LEDs. To improve the robustness to environmental and camera imaging conditions, a set of experimentally determined affine or polynomial transformations applied per color channel is adopted in the EOT loss. AdvPattern [^240] transforms the original image by changing the position, brightness, or blurring to improve the robustness to environmental distortions in person re-ID tasks. AdvHat [^113] attacks face recognition by pasting a printed adversarial sticker on the hat. It simulates the spatial distortion from the off-plane bending of the hat by a parabolic transformation in 3D space. The curriculum adversarial attack (CAA) [^305] pastes a printed adversarial sticker on the forehead. It designs a sticker transformation module to simulate sticker deformation ($e.g.$, off-plane bending and 3D rotations) and sticker position disturbance, and a face transformation module to simulate the variations of poses, lighting conditions, and internal facial variations. PhysGAN [^115] aims to attack the autonomous driving system by taking a small slice of video as the input, rather than 2D individual images, such that the generated adversarial road sign could continuously fool the moving vehicle. The EOT loss is extended to attack the automatic speech recognition in the physical world. In [^188], the expectation loss is defined over different kinds of reverberations that are generated by an acoustic room simulator. In [^273], the expectation loss is defined over impulse responses recorded in diverse environments to resist environmental reverberations, and the Gaussian noise is also considered to simulate the thermal noise caused in both the playback and recording devices.

#### VII-B3 Sample-Specific vs. Sample-Agnostic Perturbation

According to the perspective that the adversarial perturbation is specific or agnostic to the benign sample, existing attack methods could be partitioned to the following two categories:

$$
\begin{cases}\text{Sample-specific perturbation:}&\mathbf{x}_{\varepsilon}^{(i%
)}-\mathbf{x}_{0}^{(i)}\neq\mathbf{x}_{\varepsilon}^{(j)}-\mathbf{x}_{0}^{(j)}%
;\\
\text{Sample-agnostic perturbation:}&\mathbf{x}_{\varepsilon}^{(i)}-\mathbf{x}%
_{0}^{(i)}=\mathbf{x}_{\varepsilon}^{(j)}-\mathbf{x}_{0}^{(j)},\end{cases}
$$

where $i\neq j$ are the indices of two different samples. While most existing works belong to the sample-specific type, here we mainly review the works of sample-agnostic perturbation, which is also called universal adversarial perturbation (UAP). According to whether some benign samples are utilized or not, existing UAP methods can be categorized to the following two types: data-dependent and data-free methods.

##### Data-dependent UAP

The existence of UAP is firstly discovered by [^162] in the CNN-based image classification task, which extends the general formulation (8) from one individual benign sample to a set of benign samples, as follows:

$$
\displaystyle\underset{\bm{\varepsilon}}{\arg\min}~{}\|\bm{\varepsilon}\|_{2}^%
{2}+\frac{\lambda_{\mathcal{C}_{B}}}{m}\sum_{i=1}^{n}\mathcal{L}_{\mathcal{C}_%
{B}}(f_{\mathbf{w}_{0}}(\mathbf{x}_{0}^{(i)}+\bm{\varepsilon}),y_{0}^{(i)}).
$$

One variant of UAP, called class discriminative UAP (CD-UAP) [^287], aims to find a common perturbation that is adversarial for benign samples from some particular target classes, while ineffective for benign samples from other classes.

##### Data-free UAP

To improve the generalization of UAP to new benign samples, some works attempt to generate UAP without utilizing any benign sample, $i.e.$, data-free. For example, the Fast Feature Fool method [^164] shows that the perturbation with higher activation at all the convolution layers in the attacked model could fool multiple benign samples simultaneously. The generalizable data-free UAP (GD-UAP) [^165] proposes to generate UAP by searching the perturbation with the maximal activation norms of all layers in the attacked model. The prior driven uncertainty approximation (PD-UA) method [^144] proposes to generate UAP by maximizing the model uncertainty, including the Epistemic uncertainty and the Aleatoric uncertainty, based on the assumption that larger model uncertainty corresponded to stronger attack performance. In addition to the image-classification task, UAP has also studied in many other applications, such as image retrieval [^121], object detection [^118] [^97], face recognition [^2], and speech recognition [^170] [^262], $etc.$

#### VII-B4 Additive vs. Non-Additive Perturbation

According to the relationship between $\mathbf{x}_{\varepsilon}$ and $\mathbf{x}_{0}$, existing attack methods could be partitioned into the following two categories:

$$
\begin{cases}\text{Additive perturbation:}&\mathbf{x}_{\varepsilon}=\mathbf{x}%
_{0}+\boldsymbol{\varepsilon};\\
\text{Non-additive perturbation:}&\mathbf{x}_{\varepsilon}=h(\mathbf{x}_{0}),%
\end{cases}
$$

where $h(\cdot)$ denotes a non-additive transformation function. While most existing works adopted additive perturbation, here we mainly review the works of non-additive perturbation. Note that since the non-additive transformation causes the global distortion compared to the benign sample $\mathbf{x}_{0}$, the $\ell_{p}$ -norm is often no longer adopted to specify the distance metric $\mathcal{D}_{1}(\mathbf{x}_{0},\mathbf{x}_{\varepsilon})$, instead by other forms, such as the style loss in AdvCam [^67], or the geodesic distance in Manifool [^109], $etc.$ Existing non-additive methods mainly adopt two types of transformations, $i.e.$, geometric (or spatial) and style transformations.

##### Geometric transformations

Geometric transformations mainly include rotation, translation, and affine transformations. The fact that small rotations and translations on images can change the predictions of convolutional neural networks (CNNs) is firstly observed in [^72]. However, it focuses on measuring the invariance of CNNs to any geometric transformation, rather than designing inconspicuous adversarial transformations. Some later works pay more attention to ensure the inconspicuousness of the generated geometric transformations. For example, the Manifool method [^109] generates adversarial geometric transformations by perturbing the original image towards the decision boundary ($i.e.$, increasing the classification loss), while keeping the perturbed image on a transformation manifold, to ensure the inconspicuousness of the generated transformation. The stAdv method [^259] proposes to minimize the local spatial distortion that is defined based on the flow vector between the benign and adversarial images. The work [^68] empirically investigates the vulnerability of neural network–based classifiers to geometric transformations, using the gradient-based attack method or grid search to find the adversarial transformation. Two suggestions for improving the robustness are also provided, including inserting the adversarial transformation into the adversarial training process [^158], and the majority vote with multiple random geometric transformations at inference. The generalized universal adversarial perturbations (GUAP) method [^295] utilizes the learning-based attack method to generate the universal spatial transformation. The work \[wong2019isserstein\] adopts the isserstein distance \[isserstein-distance-1974\] to measure the cost of moving pixel mass between images, rather than the widely used $\ell_{p}$ distance. It can cover multiple geometric transformations, such as scaling, rotation, and translation.

##### Style transformations

Style transformations mean to change the style or color of the global or local region of the image. The ReColorAdv method [^117] proposes to globally change the color of the benign image to achieve the attack goal, in both RGB and CIELUV color spaces. The adversarial camouflage (AdvCam) method [^67] combines the style loss that is firstly used on image style transfer [^82] with the adversarial loss, to generate adversarial image with natural styles that looks legitimate to human eyes.

#### VII-B5 Dense vs. Sparse Perturbation

According to perturbation cardinality, each attack method belongs to one of the following types:

$$
\begin{cases}\text{Dense perturbation:}&\|\mathbf{x}_{\varepsilon}-\mathbf{x}_%
{0}\|_{0}=|\mathbf{x}_{0}|;\\
\text{Sparse perturbation:}&\|\mathbf{x}_{\varepsilon}-\mathbf{x}_{0}\|_{0}<|%
\mathbf{x}_{0}|.\end{cases}
$$

For example, if all pixels in one image are perturbed, then the perturbation is dense. While most existing attack methods adopt the setting of dense perturbation (or called dense attack), some works find that perturbing partial entries of one benign sample ($e.g.$, partial pixels in one image) could also achieve the attack goal, which is called sparse perturbation or sparse attack. Compared with dense perturbation where the attacker only needs to determine the perturbation magnitude of each entry, the sparse attacker should also determine the perturbation positions. According to the strategy of determining perturbation positions, existing sparse attack methods are partitioned into three categories, including: manual, heuristic search and optimization-based strategies.

##### Manual strategy

Manual strategy means that the attacker manually specifies the perturbed positions. For example, LaVAN [^110] experimentally demonstrates that an adversarial and visible local patch located in the background in one image could also fool the model. This manual strategy qualitatively demonstrates that the background pixels are also important for the prediction, but cannot provide more exact and quantitative analysis of the sensitivity of each pixel.

##### Heuristic search strategy

Heuristic search strategy means that the perturbed entries are gradually determined according to some heuristic criterion. For example, the Jacobian-based saliency map attack (JSMA) [^180] and its extensions [^23] perturb the pixels corresponding to large values in the saliency map. The CornerSearch method [^49] firstly sorts all candidate pixels according to their changes to the model output, then iteratively samples perturbed pixels following a probability distribution related to the sorted index. The LocSearchAdv algorithm [^167] conducts sparse attack in a black-box setting. It designs a greedy local search strategy that given the current perturbed pixels, then new candidate pixels are searched from a small square centered at each perturbed pixel, according to black-box attack performance.

##### Optimization-based strategy

Optimization-based strategy aims at optimizing the magnitudes and positions of perturbations simultaneously. For example, the One-Pixel attack [^216] tries to perturb only one pixel to achieve the attack goal. The pixel coordinates and the RGB values are concatenated to form a vector that needs to be optimized. Then, the differential evolution (DE) algorithm [^25] is adopted to search for a good concatenate vector that achieves the attack goal. In [^299], the sparsity of perturbations is encouraged by the $\ell_{0}$ norm, along with the adversarial loss. The alternating direction method of multipliers (ADMM) algorithm [^18] is then adopted to optimize this problem. However, there is no constraint on perturbation magnitudes, causing the learned perturbation might be visible. The Pointwise attack method [^199] extends the Boundary attack method [^19] (a dense black-box attack) from $\ell_{2}$ norm to $\ell_{0}$ norm to enforce sparsity. It firstly adds a salt-and-pepper noise that could fool the model, then repeatedly removes the noise of one pixel if the model is still fooled. The GreedyFool method [^145] develops a two-stage algorithm to minimize the $\ell_{0}$ norm. The first stage increases the perturbed pixels according to the distortion map, and the second stage gradually reduces the perturbed pixels according to the attack performance with different perturbation magnitudes on these pixels. The SparseFool method [^159] adopts the $\ell_{1}$ norm to encourage sparsity, and develops an iterative algorithm that picks one coordinate ($i.e.$, one pixel) to perturb based on the linear approximation of the decision boundary. Moreover, [^264] explores the group-wise sparsity in adversarial examples, encouraged by the $\ell_{2,1}$ norm [^284]. The learned perturbations gathered together to the local regions that are highly related to discriminative regions. The $\ell_{2,1}$ norm is also used in [^241] to enforce the temporal sparsity for attacking the model for the video-based task, $i.e.$, only partial frames are perturbed. The sparse adversarial attack via perturbation factorization (SAPF) method [^71] provides a new perspective that the perturbation on each pixel is factorized to the product of the perturbation magnitude and a binary selection factor. If the binary factor is $1$, then the corresponding pixel is perturbed, otherwise not. Then, the sparse attack is formulated as a mixed integer programming (MIP), and the sparsity degree is exactly controlled via the cardinality constraint on selection factors. This MIP problem is efficiently solved by the $\ell_{p}$ -Box ADMM algorithm [^248].

According to different output types, we can further categorize white-box adversarial examples into the following two types.

#### VII-B6 Untargeted vs. Targeted Attack

Untargeted attack aims to fool the model to give an incorrect prediction ($i.e.$, different with $y_{0}$) on $\mathbf{x}_{\varepsilon}$, while targeted attack aims to fool the model to predict $\mathbf{x}_{\varepsilon}$ as a target class $y_{\varepsilon}$. Their difference could be reflected by the specification of $\mathcal{L}_{\mathcal{I}_{B}}(f_{\mathbf{w}_{0}}(\mathbf{x}_{\varepsilon}),y_{%
\varepsilon})$ in the general formulation (8), as follows:

$$
\begin{cases}\text{Untargeted attack:}&\mathcal{L}_{\mathcal{I}_{B}}(f_{%
\mathbf{w}_{0}}(\mathbf{x}_{\varepsilon}),y_{\varepsilon})=-\mathcal{L}(f_{%
\mathbf{w}_{0}}(\mathbf{x}_{\varepsilon}),y_{0});\\
\text{Targeted attack:}&\mathcal{L}_{\mathcal{I}_{B}}(f_{\mathbf{w}_{0}}(%
\mathbf{x}_{\varepsilon}),y_{\varepsilon})=\mathcal{L}(f_{\mathbf{w}_{0}}(%
\mathbf{x}_{\varepsilon}),y_{\varepsilon}),\end{cases}
$$

where $\mathcal{L}(\cdot,\cdot)$ could be any widely used loss function, such as cross-entropy loss or hinge loss. The difference between the above two loss specifications doesn’t influence the choice of the adopted optimization algorithm. Thus, in most adversarial example works, experiments of both untargeted and targeted attacks are conducted simultaneously to verify the effectiveness of the proposed objective function or the proposed algorithm. However, according to the reported results in existing works, there is a remarkable gap in the attack performance between these two attacks. Especially in black-box and transfer-based attacks, the targeted attack is often much more challenging than the untargeted attack, as the adversarial region of a particular target class is much narrower than that of all incorrect classes. Thus, a few recent attempts focus on improving the targeted attack performance in black-box and transfer-based attack scenarios. For example, the work [^124] replaces the cross entropy loss by the Poincare distance metric to obtain the self-adaptive gradient magnitude during iterative attack to alleviate noise curing, and adds a triplet loss to enforce adversarial example away from the original class, leading to more transferable targeted adversarial examples. The transferable targeted perturbation (TTP) [^168] designs a generative adversarial network $w.r.t.$ the target class, which can produce highly transferable targeted perturbation. The work [^304] find that existing iterative transfer attacks ($e.g.$, MI-FSGM [^60], DI-FSGM [^261]) could give much better targeted transfer attack results with sufficient iterations, and proposed to adopt the logit loss to further improve the attack performance.

#### VII-B7 Factorized vs. Structured Output

Most existing attacks are evaluated on tasks with factorized outputs ($e.g.$, the discrete label in DNN-based image classification task), such that it is easy to compute (for white-box attacks) or estimate (for black-box attacks) the gradients $w.r.t.$ the input. However, there are also some DNN-based tasks with structured outputs ($e.g.$, image captioning, scene text recognition), which predict a sequential label for each input (image or audio). The dependency among outputs may bring in additional challenge for adversarial examples. According to the type of target outputs, existing attacks against tasks with structured outputs are partitioned into the following two categories:

##### Attack with complete target outputs

where a complete sentence is set as the target output. In this case, the gradient $w.r.t.$ the input can be easily computed as did in the regular learning of the attacked model, and the attack methods designed for models with factorized outputs can be naturally applied. For example, [^269] sets a complete and irrelevant caption as the target caption to attack the dense captioning model, and directly uses the Adam-based attack method proposed in [^23]. [^204] proposes to construct the complete target caption by replacing noun, numeral, or relation words in the original caption with other words of the same type. Then, the visual-semantic embedding based image captioning model is attacked by minimizing the hinge loss defined based on the constructed target caption. [^24] attacked the audio-to-text model by setting complete target sentences, and generated the adversarial audio input by the fast gradient sign attack method [^86] and its iterative variant [^116]. The works [^267] and [^268] also change some words in the output sequence to set a complete target output, and utilize the sequential factorization of the posterior probability $w.r.t.$ the target sequence to simplify the optimization of adversarial loss.

##### Attack with partial target outputs

where only partial outputs in the target output sequence is set as the target. The work [^31] firstly proposed the target keyword attack by requiring some keywords to appear in the output sequence, while not restricting their specific locations. It is implemented by the hinge loss to maximize the probability of the target keywords. The work [^270] proposed exact structured attack by requiring some specific keywords to appear at specific locations in the output sequence. It is more strict than the target keyword attack, and the complete target output could be seen as a special case of it. It is implemented by treating the attack as a structured output prediction problem with hidden variables, where the targeted words are treated as observed random variables, while the output words of other unrestricted locations are treated as hidden variables. Then, two structured output learning methods, including generalized expectation maximization [^16] and structured SVM with latent variables [^280], are adopted to generate the adversarial examples.

### VII-C Black-Box Adversarial Examples

According to the type of query feedback returned by the attacked model, existing black-box adversarial examples could be further partitioned into two categories, including score-based adversarial examples with continuous feedback ($e.g.$, the posterior probability in $[0,1]$), and decision-based adversarial examples with discrete feedback ($e.g.$, the discrete label).

#### VII-C1 Score-based Adversarial Examples

For this category, the general formulation (8) is specified as follows

$$
\displaystyle\min_{\mathbf{x}_{\varepsilon}\in\mathcal{Z}_{\mathbf{x}}}\delta%
\big{(}\mathbf{x}_{\varepsilon}\in\mathbb{B}_{\mathbf{x}_{0},\epsilon}\big{)}+%
\max\big{(}0,\triangle\big{)},
$$

where $\mathbb{B}_{\mathbf{x}_{0},\epsilon}=\{\mathbf{x}^{\prime}|\|\mathbf{x}^{%
\prime}-\mathbf{x}_{0}\|_{p}\leq\epsilon\}$ defines a neighborhood set around $\mathbf{x}_{0}$, with $\epsilon>0$ and the norm $p$ being attacker determined scalars. The distance function $\mathcal{D}_{\mathbf{x}}$ is specified as $\delta\big{(}\mathbf{x}_{\varepsilon}\in\mathbb{B}_{\mathbf{x},\epsilon}\big{)}$, and $\delta(a)=0$ if $a$ is true, otherwise $\delta(a)=\infty$. It serves as a hard constraint to limit adversarial perturbation, and the attacker has to minimize the hinge loss through searching within $\mathbb{B}_{\mathbf{x},\epsilon}$. The hinge loss $\max\big{(}0,\triangle\big{)}$ is specified as follows:

$$
\begin{cases}\text{Untargeted:}&\triangle=f(\mathbf{x}_{\varepsilon},y_{0})-%
\max\limits_{j\neq y_{0}}f(\mathbf{x}_{\varepsilon},j);\\
\text{Targeted:}&\triangle=\max\limits_{j\neq y_{\varepsilon}}f(\mathbf{x}_{%
\varepsilon},j)-f(\mathbf{x}_{\varepsilon},y_{\varepsilon}),\end{cases}
$$

with $y_{\varepsilon}\in\mathcal{Y}$ being the target label. Note that the hinge loss is non-negative, and $00$ is the minimal value, corresponding to a successful adversarial perturbation. Thus, once a successful adversarial perturbation is obtained, the attack could stop. In the following, according to the information utilized by the attacker, we summarize existing score-based adversarial examples from two categories, including query-based and combination-based adversarial examples.

##### Query-based adversarial examples

Query-based methods treat the attack task as a black-box optimization problem, such that many black-box optimization approaches can be applied. Accordingly, existing query-based attack methods can be further partitioned into two categories, including random search and gradient-estimation-based methods.

- Random search methods update the adversarial perturbation based on some random search strategies. SimBA [^89] randomly picks one direction to add or subtract the perturbation at each step, from a set of orthonormal basis vectors, which is specified as the Cartesian basis or discrete cosine basis. The ECO attack [^161] proposes to determine the perturbation among the vertices of the $\ell_{\infty}$ version of the neighborhood set $\mathbb{B}_{\mathbf{x},\epsilon}$, leading to a discrete set maximization problem, which is then approximately solved by the local search algorithm [^73]. The Square attack [^7] also searches the perturbation among vertices of the $\ell_{\infty}$ version of $\mathbb{B}_{\mathbf{x},\epsilon}$, but within a randomly sampled local patch at each step. The PRFA attack [^139] extends the Square attack to attack against object detection models in black-box manner, by perturbing multiple local patches in parallel for better efficiency. The PPBA attack [^122] searches the perturbation in a low-dimensional and low-frequency subspace constructed by the discrete cosine transform (DCT) [^4] and its inverse transform, through an accelerated random walk optimization algorithm with the effective probability of historical searches.
- Gradient-estimation-based methods update the adversarial perturbation based on gradient, which is estimated based on query feedback or some kinds of prior. The NES attack [^100] estimates the gradient based on the natural evolution strategy [^244], where several perturbation vectors are sampled from a Gaussian distribution. Bandit [^101] extends this gradient estimation by embedding both the spatial prior (neighboring pixels have similar gradients) and the temporal prior (the gradients between consecutive iterations are similar) to obtain more consistent gradients. $\mathcal{N}$ Attack [^133] extends the NES attack by restricting the vectors sampled from the Gaussian distribution into the feasible space ($i.e.$, the allowed search space of adversarial perturbation). The AdvFlow method [^160] further extends $\mathcal{N}$ Attack by replacing the Gaussian distribution with a complex distribution which is captured by the normalizing flow model [^219] pre-trained on benign data, such that the generated adversarial sample is more close to the benign sample. ZO-signSGD [^146] proposes to update the perturbations along with the gradient sign direction rather than the estimated gradient direction, and provides a theoretical analysis of the convergence rate. It is not only memory-efficient, but also shows comparable or even better attack efficiency in practice. SignHunter [^6] designs a divide-and-conquer strategy to accelerate the estimation of gradient signs, by flipping the gradient signs of all pixels within a range together, and then repeating such a group flipping operation on the whole image, the first half, the second half, the first quadrant, and so on.

##### Combination-based methods

Combination-based methods incorporate some kinds of priors learned from surrogate models into the query procedure for the target model, to enhance the efficiency of finding a successful adversarial solution. According to the type of surrogate models, the priors can be further partitioned into two categories.

- Priors from static surrogate models, which means that the surrogate models are fixed during the attack procedure. For example, the Subspace attack method [^91] adopts the gradients of several surrogate models as the basis vectors to estimate the gradient for updating the adversarial perturbation against the target model in each step of the iterative attack procedure. The prior-guided random gradient-free (P-RGF) method [^59] improves the random gradient-free method [^171] by combining the surrogate gradient with randomly sampled unit vectors to obtain more accurate gradient estimation. TREMBA [^99] trains an auto-encoder to generate adversarial perturbation based on surrogate models, and adopts the decoder ($i.e.$, the projection from a low-dimensional latent space to the original input space) as a prior, such that the perturbation for the target model could be efficiently searched in the low-dimensional latent space. The $\mathcal{CG}$ -Attack [^77] captures the conditional adversarial distribution (CAD) by the c-Glow model, which could map a Gaussian distribution to a complex distribution. The c-Glow model is firstly trained based on surrogate models. Then, the mapping part of this c-Glow model, $i.e.$, the mapping from Gaussian distribution to perturbation distribution, is fixed, while the Gaussian distribution is refitted based on query feedback of the target model, to approximate the target CAD, such that adversarial perturbations for the target model could be efficiently sampled. The meta square attack (MSA) attack [^278] utilizes meta learning to learn a sampling distribution of the hyper-parameters in Square attack [^7] ($e.g.$, the square patch’s size, location and color) based on surrogate models, and the meta distribution is fine-tuned based on query feedback to provide more suitable hyper-parameters for attacking the target model. The eigen black-box attack (EigenBA) [^309] studies a different setting that the surrogate and target models share one backbone that is accessible to the attacker, while the classifier layers are different and the target model’s classifier layer is unknown. EigenBA proposes to calculate the updating direction of each step according to the right singular vectors of the Jacobian matrix of the shared and white-box backbone.
- Priors from adaptive surrogate models, which means that the surrogate models are updated based on the query feedback during the attack procedure, such that the gap between surrogate and target models could be alleviated. For example, the hybrid batch attack method [^218] generates candidate adversarial examples based on surrogate models as the initial point to query the target model, then adopts the queried inputs and the labels returned by the target model to tune the surrogate models. The learnable black-box attack (LeBA) [^275] combines the query-based method SimBA [^89] and the transfer-based method TIMI [^61] conducts on surrogate models, proposes to update surrogate models using a high-Order gradient approximation algorithm. The consistency sensitivity guided ensemble attack (CSEA) [^283] proposes to learn a linear combination of an ensemble of surrogate models with diversified model architectures to approximate the target model, and meanwhile update the surrogate models by encouraging the same response to different adversarial samples. The black-box attack via surrogate ensemble search (BASES) [^22] designs a bi-level optimization by alternatively updating adversarial perturbation based on the linear combination of several surrogate models and the linear combination weight of each surrogate model according to query feedback. The Simulator attack [^157] utilizes meta learning to learn a generalized simulator ($i.e.$, surrogate model), which can be fine-tuned by limited query feedback. Similar to $\mathcal{CG}$ -Attack, the meta conditional generator (MCG) attack [^279] also learns CAD, with the difference that MCG proposed a meta learning framework to capture both the example-level and model-level adversarial transferability (introduced later in Section VII-D), such that the CAD could be adjusted for each benign sample, and the surrogate model could be updated based on query feedback.

#### VII-C2 Decision-based Attack

For this category, the general formulation (8) is specified as follows

$$
\displaystyle\min_{\mathbf{x}_{\varepsilon}\in\mathcal{Z}_{\mathbf{x}}}%
\mathcal{D}_{\mathbf{x}}(\mathbf{x}_{0},\mathbf{x}_{\varepsilon})+\delta\big{(%
}\mathcal{C}(f_{\mathbf{w}_{0}}(\mathbf{x}_{\varepsilon}),y)=1\big{)},
$$

where $\mathcal{C}(f_{\mathbf{w}_{0}}(\mathbf{x}_{\varepsilon}),y)$ indicates the adversarial criterion, which is true if the attack goal is achieved, otherwise false. Specifically,

$$
\begin{cases}\text{Untargeted attack:}&\mathcal{C}(f_{\mathbf{w}_{0}}(\mathbf{%
x}_{\varepsilon}),y)=\mathbb{I}(f(\mathbf{x}_{\varepsilon};\mathbf{w})\neq y_{%
0});\\
\text{Targeted attack:}&\mathcal{C}(f_{\mathbf{w}_{0}}(\mathbf{x}_{\varepsilon%
}),y)=\mathbb{I}(f(\mathbf{x}_{\varepsilon};\mathbf{w})=y_{\varepsilon}),\end{cases}
$$

with $\mathbb{I}(a)=1$ if $a$ is true and $\mathbb{I}(a)=0$ otherwise, and $y_{\varepsilon}\in\mathcal{Y}$ denotes the target label. Besides, as defined above, $\delta(a)=0$ if $a$ is true, otherwise $\delta(a)=\infty$, which serves as a hard constraint to ensure that each immediate solution $\mathbf{x}_{\varepsilon}$ should be a feasible solution that satisfies the attack goal. With this hard constraint, the attacker has to search the better solution ($i.e.$, corresponding to smaller $\mathcal{D}_{\mathbf{x}}(\mathbf{x}_{0},\mathbf{x}_{\varepsilon})$) within the feasible space defined by $\delta(\cdot)$, also dubbed adversarial space. However, the main challenge is that such an adversarial space is invisible to the attacker. Existing works mainly focused on designing efficient search strategies, subject to the invisible adversarial space. The search strategies in existing decision-based attack methods are summarized as two categories, including random search and gradient-estimation-based methods.

##### Random search methods

Random search methods determine the search direction and step size around the invisible decision boundary using some heuristic strategies, based on a random sampler. The first attempt called Boundary method [^19] samples the search direction based on the normal distribution and dynamically adjusts the step size according to the ratio of adversarial solutions among all sampled solutions. The Evolutionary method [^62] extends the Boundary method by replacing the normal distribution with a Gaussian distribution, of which the parameters and the step size are automatically adjusted using the evolutionary strategy. Another extension of Boundary called customized iteration and sampling attack (CISA) [^206] replaces the initial adversarial perturbation by a transferable perturbation generated based on surrogate models, and adjusts the sampling distribution and step size based on historical queries. The geometric decision-based attack (GeoDA) [^191] constructs the search direction by estimating the normal direction of the decision boundary, utilizing the assumption of low curvature of the decision boundary. The sign flip attack (SFA) [^40] randomly searches the new solution at the surface of the $\ell_{\infty}$ ball around the benign example, followed by random sign flips of some dimensions of the new solution. The $\ell_{\infty}$ ball’s radius is gradually decreased along search iterations to ensure the decrease of perturbation norms. Similarly, the Ray searching attack (RayS) [^32] also determines the search direction at the surface of the $\ell_{\infty}$ ball, while the step size is determined through binary search.

##### Gradient-estimation-based methods

Gradient-estimation-based methods determine the search direction by estimating the gradient $w.r.t.$ the current solution in the update procedure. Ilyas et al. [^100] propose to firstly estimate the continuous score of the current solution based on the returned hard labels, by querying a few randomly perturbed points around the current solution. Then, the natural evolutionary strategy approach is adopted to estimate the gradient using the continuous score. The opt-based black-box attack (Opt-attack) [^43] proposes a continuous objective function to find the search direction leading to the minimal $\ell_{2}$ norm of perturbations, which can be solved by the zero-order optimization method with the gradient estimation-based on the randomized gradient-free method. The Sign-OPT method [^44] improves the performance of Opt-attack by estimating the sign of gradient instead of the gradient itself. The HopSkipJumpAttack method [^33] proposes to estimate the gradient at the boundary point using the Monte Carlo estimation method. The query-efficient boundary-based black-box attack (QEBA) [^120] proposes to accelerate gradient-estimation-based methods by estimating the gradient in the low-dimensional subspace instead of the original space. The qFool method [^150] approximates the gradient of the current solution by the gradient of its neighboring points at the decision boundary, utilizing the low curvature of the decision boundary at the vicinity of adversarial points.

### VII-D Transfer-based Adversarial Examples

According to the level of the adversarial transferability, we categorize existing transfer-based adversarial examples into example-level and model-level transferability.

#### VII-D1 Example-level Adversarial Transferability

The concept example-level adversarial transferability is firstly and explicitly defined in a recent work called meta conditional generator (MCG) [^279], as follows: “adversarial perturbations around different benign examples may have some similar properties". Meanwhile, some other works also implied or utilized similar ideas. According to the assumption of “similar properties", existing works are partitioned into the following categories.

##### Different benign examples have a common adversarial perturbation

, $i.e.$, $\exists i\neq j$,

$$
\displaystyle f(\mathbf{x}_{0}^{(i)}+\boldsymbol{\varepsilon})=y_{\varepsilon}%
^{(i)},~{}f(\mathbf{x}_{0}^{(j)}+\boldsymbol{\varepsilon})=y_{\varepsilon}^{(j%
)}.
$$

This assumption is actually the basis of UAP (universal adversarial perturbations) [^162] and its variants.

##### Adversarial perturbations of different benign examples could be generated by a common parametric model

, $i.e.$, $\exists i\neq j$,

$$
\displaystyle f(\mathbf{x}_{0}^{(i)}+g_{\boldsymbol{\theta}}(\mathbf{x}_{0}^{(%
i)}))=y_{\varepsilon}^{(i)},~{}f(\mathbf{x}_{0}^{(j)}+g_{\boldsymbol{\theta}}(%
\mathbf{x}_{0}^{(j)}))=y_{\varepsilon}^{(j)}.
$$

The generative adversarial perturbations (GAP) attack [^184] adopts the above assumption to train a generator to produce universal or sample-specific adversarial perturbations. It is further extended in [^169] and [^168] to boost the adversarial transferability across different data domains, by utilizing the training mechanism of generative adversarial networks [^85].

##### Adversarial examples w.r.t.formulae-sequence𝑤𝑟𝑡w.r.t.italic\_w. italic\_r. italic\_t. different benign examples follow a common marginal distribution

, $i.e.$, $\exists i\neq j$,

$$
\displaystyle\exists i\neq j,\mathbf{x}_{\varepsilon}^{(i)},\mathbf{x}_{%
\varepsilon}^{(j)}\sim\mathcal{P}(\mathbf{x}_{\varepsilon}).
$$

This assumption is adopted by AdvFlow [^160], where the common marginal distribution of adversarial samples $\mathcal{P}(\mathbf{x}_{\varepsilon})$ is modeled by the normalizing flow model [^219], which is capable to capture complex data distributions.

##### Adversarial perturbations around different benign samples follow a common conditional distribution

, $i.e.$, $\exists i\neq j$,

$$
\displaystyle\mathbf{x}_{\varepsilon}^{(i)},\mathbf{x}_{\varepsilon}^{(j)}\sim%
\mathcal{P}(\mathbf{x}_{\varepsilon}|\mathbf{x}_{0}).
$$

For example, the $\mathcal{CG}$ -Attack method [^77]) proposes to learn a common conditional distribution $\mathcal{P}(\mathbf{x}_{\varepsilon}|\mathbf{x}_{0})$ via the conditional Glow model [^156] (a variant of the flow-based model). This assumption is further relaxed in the MCG method [^279] that the conditional adversarial distributions around different benign examples are similar but might be slightly different. MCG proposes a meta learning framework to firstly learn a meta conditional adversarial distribution, which could be fine-tuned to more accurately capture the conditional adversarial distribution for new benign examples.

##### Different benign examples have similar gradients to search adversarial perturbations

, $i.e.$, $\exists i\neq j$,

$$
\displaystyle\frac{\partial\mathcal{J}_{\mathcal{G}_{1}}(\mathbf{x}_{0}^{(i)},%
y_{\varepsilon}^{(i)})}{\partial\mathbf{x}^{(i)}}\approx\frac{\partial\mathcal%
{J}_{\mathcal{G}_{2}}(\mathbf{x}_{0}^{(j)},y_{\varepsilon}^{(j)})}{\partial%
\mathbf{x}^{(j)}},
$$

where $\mathcal{J}_{\mathcal{G}_{1}}(\cdot,\cdot)$ denotes the adversarial objective function $w.r.t.$ the attacked model $\mathcal{G}_{1}$, and $\mathbf{x}^{(i)}$ indicates the immediate solution when searching the adversarial sample of $\mathbf{x}_{0}^{(i)}$. For example, the meta attack [^64] trains a meta model that could directly generate a gradient $w.r.t.$ the input sample, which is then fine-tuned on each new benign sample and new model to quickly generate effective gradients, rather than querying the new model to estimate gradients, such that the attack efficiency and effectiveness is supposed to be improved.

#### VII-D2 Model-level Adversarial Transferability

Model-level adversarial transferability tells that adversarial perturbations generated based on one model may be also adversarial for another model. There have been several attempts to improve the model-level transferability from different perspectives.

##### Data perspective

Inspired by the data augmentation technique that alleviates the overfitting of the trained model to the training dataset, the attacker firstly conducts a random transformation on the benign sample, then generates adversarial perturbations based on the transformed sample $w.r.t.$ the surrogate model, such that the generated adversarial sample doesn’t overfit to the surrogate model too much. For example, the diverse inputs iterative FGSM (DI ${}^{2}$ -FGSM) algorithm [^261] proposes to insert random resizing and padding into the input sample. A more common setting is replacing the benign sample by a set of variants with random transformations, such as random scaling ($i.e.$, resizing) [^140], random mixup [^234], random translation [^61], as well as adding random Gaussian noises [^252]. The object-based diverse input (ODI) method [^20] aims to improve the transferability of targeted adversarial samples through a complex transformation that is implemented by firstly printing the original adversarial sample on 3D objects’ surface, then rendering these 3D objects in a variety of rendering environments to obtain diverse transformed adversarial samples. Besides, the spectrum simulation iterative FGSM (S ${}^{2}$ I-FGSM) [^154] designs a spectrum transformation based on discrete cosine transform (DCT) and inverse discrete cosine transform (IDCT) techniques, to generate more diverse inputs than the transformations in the spatial domain.

##### Optimization perspective

To avoid the underfitting of the one-step gradient sign method ($i.e.$, FGSM [^86]) and the overfitting of the multi-step gradient sign method ($i.e.$, I-FGSM [^116]) to the surrogate model, some variants of gradient-based optimization algorithms are introduced to generate powerful adversarial examples with good transferability, such as the momentum-based gradient ($e.g.$, MI-FGSM [^60]) and its variants ($e.g.$, VMI-FGSM [^232] which consider the gradient variance in the vicinity of the current data point into the momentum, EMI-FGSM [^235] which calculates the average gradient of multiple points in the vicinity of the current data point, and SVRE-MI-FGSM [^263] which extends MI-FSGM to the ensemble attack with reduced gradient variance), as well as the Nesterov accelerated gradient ($e.g.$, NI-FGSM) [^140] and its variant ($e.g.$, PI-FSGM [^235] which replace the accumulated momentum in NI-FGSM [^140] by a new momentum that only accumulates the local gradient of the previous step). Besides, there are also a few attempts to modify the gradients. For examples, the SGM (skip gradient method) attack [^251] find that backpropagating more gradients from the skip connections than the residual modules in the ResNet-like models could generate higher transferable adversarial examples. The linear backpropagation attack (LinBP) [^90] proposes to omit the ReLU layers in backpropagation pass to improve adversarial transferability. The meta gradient adversarial attack (MGAA) [^285] utilizes meta learning to learn a generalized meta gradient by treating the attack against one model as one individual task, such that the meta gradient can be quickly fine-tuned to find effective adversarial perturbations for new models.

##### Loss perspective

Some works attempt to design novel loss functions to generate more transferable adversarial perturbations, rather than the widely used cross entropy loss defined based on the model prediction and ground-truth or adversarial labels. For example, the feature distribution attack (FDA) [^102] firstly trains an auxiliary binary classifier of the intermediate layer features $w.r.t.$ the target class, then maximizes the posterior probability predicted by this classifier to generate adversarial examples. It is later extended from one intermediate layer to multiple layers in [^103]. The intermediate level attack projection attack (ILAP) [^98] maximized the difference of intermediate layer features between adversarial and benign inputs, while keeping close to an existing adversarial example in the intermediate feature space. The feature importance-aware attack (FIA) [^238] disrupts important object-aware intermediate features in the surrogate model, and the feature importance is calculated by averaging the gradients $w.r.t.$ feature maps of the surrogate model. The neuron attribution-based attack (NAA) [^292] extends FIA by measuring feature importance by neuron attribution. The work [^304] find that maximizing the logit $w.r.t.$ the target class using I-FGSM method with sufficient iterations could generate adversarial examples with high targeted transferability. The interaction-reduced attack (IR) [^236] empirically verifies that “the adversarial transferability and the interactions inside adversarial perturbations are negatively correlated", and proposes an interaction loss to generate high transferable perturbations. In addition to the above losses defined based on intermediate layers, the reverse adversarial perturbation attack (RAP) [^189] proposes a novel min-max loss, where the adversarial example is perturbed by adding a reverse adversarial perturbation. It encouraged to search for flat local minimums which are more robust to model changes, leading to higher transferability.

##### Surrogate model perspective

Some attempts focus on choosing or adjusting surrogate models to improve transferability. For example, the work [^214] empirically demonstrates that the slightly robust surrogate model ($i.e.$, adversarially training with moderate perturbation budget) could generate highly transferable adversarial perturbations. The Ghost networks attack [^130] firstly perturbs a fixed surrogate model by densely inserting dropout layers and randomly adjusting residual weight to generate multiple surrogate models, then adopts the longitudinal ensemble that each step updating of adversarial perturbation is calculated based on one randomly selected surrogate model. The intrinsic adversarial attack (IAA) [^312] hypothesizes that samples at the low-density region of the ground truth data distribution where models are not well trained are more transferable. Thus, it proposes to maximize the matching between the gradient of adversarial samples and the direction toward the low-density regions. The distribution-relevant attack (DRA) [^311] fine-tunes the surrogate model to encourage the gradient similarity between the model and the ground truth data distribution, according to the hypothesis that adversarial samples away from the original distribution of the benign sample are highly transferable.

## VIII Adversarial Machine Learning in other scenarios

Recently, diffusion models and large language models have shown superior understanding and generative abilities in visual and language fields respectively, which have stimulated widespread attention in the AI community. Despite their extraordinary capabilities, recent studies have presented the vulnerabilities of these models under malicious attacks. In this section, we mainly detail proposed attacks on diffusion models (see Section VIII-A) and large language models (see Section VIII-B).

### VIII-A Attack on Diffusion Models

Diffusion models are a class of deep generative models that learn forward and reverse diffusion processes via progressive noise-addition and denoising. Chou $et~{}al.$ [^46] first study the robustness of diffusion model against backdoor attacks and propose BadDiffusion, which implants backdoor into the diffusion processes by specific triggers and target images. At the inference stage, the backdoored diffusion model will behave just like an untampered generator for regular data inputs, while falsely generating some targeted outcome designed by the bad actor upon receiving the implanted trigger signal. TrojDiff [^38] designs transitions to diffuse a pre-defined target distribution to the Gaussian distribution biased by a specific trigger, and then proposes a parameterization of the generative process to reverse the trojan diffusion process via an effective training objective. Unlike the above two methods, Target Prompt Attack (TPA) and Target Attribute Attack (TAA) [^215] aims to inject backdoor into the pre-trained text encoder of the text-to-image synthesis diffusion models. By inserting a single character trigger into the prompt, the attacker can trigger the model to generate images with predefined attributes or images that follow a hidden, potentially malicious description. Chou $et~{}al.$ [^47] further propose VillanDiffusion, which is a unified backdoor attack framework for diffusion models that covers mainstream unconditional and conditional diffusion models (denoising-based and score-based) and various training-free samplers for holistic evaluations.

### VIII-B Attack on Large Language Models

Large language models (LLMs) are a type of pre-trained language model notable for their abilities to achieve general-purpose language understanding and generation, which have made remarkable progress toward achieving artificial general intelligence. However, LLMs are still vulnerable to malicious attacks. Xu $et~{}al.$ [^266] explore the universal vulnerability of the pre-training paradigm of LLMs by either injecting backdoor triggers with poisoned samples or searching for adversarial triggers using only plain text. Then these triggers can be used to control the outputs after fine-tuning on the downstream tasks. Poisoned Prompt Tuning (PPT) method [^66] aims to embed backdoor into the soft prompt via prompt tuning on the poisoned dataset and the backdoor will be loaded into LLMs by using the soft prompt. PromptAttack method [^207] constructs malicious prompt templates by automatically searching for discrete tokens via a gradient search algorithm. PromptInject method [^181] investigates two types of prompt injection to misalign the goals of GPT-3, where goal hijacking misaligned the original goal of a prompt to a new goal of printing a target phrase, and prompt leaking aimed to output the original prompt. BadPrompt method [^21] conducts backdoor attack to continuous prompts and proposes an adaptive trigger optimization algorithm to automatically select the most effective and invisible trigger for each sample. BadGPT [^205] aims to attack against RL fine-tuning paradigm of LLMs via backdooring reward model. Wan $et~{}al.$ [^226] show that the poisoning dataset used for pertaining LLMs by bay bad-of-words approximation will cause test errors even for held-out tasks that were not poisoned during training time. HOUYI method [^147] applies a systematic approach to prompt injection on LLMs by drawing from SQL injection and XSS attacks. PoisonPrompt method [^276] compromises both hard and soft prompt-based LLMs by a bi-level optimization-based backdoor attack with two primary objectives: first, to optimize the trigger used for activating the backdoor behavior, and second, to train the prompt tuning task. AutoDAN method [^310] automatically generates interpretable prompts to jailbreak LLMs which can bypass perplexity-based filters while maintaining a high attack success rate like manual jailbreak attacks. TrojLLM method [^271] implements a black-box backdoor attack by universal API-driven trigger discovery and progressive prompt poisoning. Unlike other methods, it assumes that the attack can only query LLMs-based APIs, while having no access to the inner workings of LLMs, such as architecture, parameters, gradients, and so on.

## IX Applications

Attack paradigms mentioned above are double-edged swords. On the one hand, they can indeed compromise machine learning system to achieve malicious goals. But on the other hand, such negative effectiveness can be turned into goodness for some specific tasks. For example, backdoor attacks can be used for copyright protection and adversarial attacks can be used for privacy protection. In this section, we will introduce the positive applications of different attack paradigms.

### IX-A Backdoor Attacks for Copyright Protection

Adi $et~{}al.$ [^1] propose to watermark deep neural networks by backdoor attack to identify models as the intellectual property of a particular vendor. Sommer $et~{}al.$ [^211] design a backdoor based verification mechanism for machine unlearning, in which each user can utilize backdoor techniques to verify whether the MLaaS provider deleted their training data from the backdoored model by checking the attack success rate using its own trigger with the target label. Li $et~{}al.$ [^135] propose a backdoor based dataset copyright protection method by first adopting data-poisoning based backdoor attack and then conducting ownership verification by verifying whether the backdoored model has targeted backdoor behaviors. Li $et~{}al.$ [^136] design a black-box dataset ownership verification based on targeted backdoor attacks and pair-wise hypothesis tests. However, the embedded backdoor can be maliciously exploited by the attackers to manipulate model predictions. Li $et~{}al.$ [^131] propose a untargeted backdoor watermarking scheme to alleviate this problem, where the backdoored model behaviors are not deterministic. ROWBACK method [^28] improves the robustness of watermarking by redesigning the trigger set based on adversarial examples and modifying the marking mechanism to ensure thorough distribution of the embedded watermarks. MIB method [^95] leverages backdoor to effectively infer whether a data sample was used to train an ML model or not by poisoning a small number of samples and only black-box access to the target model.

### IX-B Adversarial Examples for Privacy Protection

The increasing leakage and misuse of visual information raises security and privacy concerns. In fact, the negative effects of adversarial attacks can be utilized positively to protect privacy. Oh $et~{}al.$ [^108] proposed a game theoretical framework between a social media user and a recogniser to explore adversarial image perturbations for privacy protection, where the user perturbs the image to confuse the recognizer and the recognizer chooses blue strategy as a countermeasure. Privacy-preserving Feature Extraction based on Adversarial Training (P-FEAT) [^55] method employs adversarial training to strengthen the privacy protection of an encoder in a neural network, ensuring reduced privacy leakage without compromising task accuracy. Adversarial Privacy-preserving Filter (APF) [^291] method protects the online shared face images from being maliciously used by an end-cloud collaborated adversarial attack solution to satisfy requirements of privacy, utility and non-accessibility. Text-space adversarial attack method (AaaD) [^128] method explores the utilization of adversarial attacks to protect data privacy on social media. It focuses on obfuscating users’ attributes by generating semantically and visually similar word perturbations, proving its effectiveness against attribute inference attacks. Adversarial Visual Information Hiding (AVIH) method [^217] generates obfuscating adversarial perturbations to obscure the visual information of the data. Meanwhile, it maintains the hidden objectives to be correctly predicted by models.

## X Discussions

### X-A Backdoor Attacks

#### X-A1 Data-poisoning based Backdoor Attacks

- In terms of the trigger type, visible/non-semantic/manually designed triggers have been widely adopted in existing works. However, along with the development of backdoor defense, the characteristics of these types have been thoroughly explored and then utilized to develop more effective defense methods. Thus, we think that future backdoor attacks are more likely to adopt invisible/semantic/learnable triggers, to evade existing backdoor defenses.
- In terms of the fusion strategy, additive/static/sample-agnostic triggers have been widely adopted in existing works, but we think that non-additive/dynamic/sample-specific triggers will be the future trend, due to the larger flexibility and stronger capability to evade backdoor defenses.
- In terms of the target class, the single-target setting is still the dominant setting in backdoor attacks, while the multi-target setting is often evaluated as extended experiments in a few works. However, we think that some interesting points of the latter setting deserve to be studied. First, how many target classes could be embedded into a dataset, and what is the relationship between attack performance and target class numbers? It will study the capability of backdoor injection of one model. Second, what is the difference between single-target and multi-target backdoored models? It will be helpful to develop effective defenses for multi-target classes attacks, while most existing defenses are mainly designed for single-target class attacks. Third, what is the relationship between the backdoors of different targets in one backdoored model? It will be useful to design advanced attack and defense methods in multi-target settings.

#### X-A2 Training-controllable based Backdoor Attacks

Compared to the above threat model, the training-controllable based backdoor attacks have not been well studied, as they require the control of the training process, which seems to be less practical. However, along with the popularity of pre-trained large-scale models, the backdoor threat in these models could widely spread to downstream tasks of different domains, and the main challenge is how to improve the resistance to fine-tuning and domain generalization. Besides, due to the sufficient capability of large-scale models, it is expected that multiple backdoors with different types could be inserted, posing serious challenges for defense.

### X-B Weight Attacks

We note that most weight attack methods still stay in theoretical analysis. To the best of our knowledge, there hasn’t been any successful attack against intelligent systems in real scenarios. We think the main reason is that the success of weight attack is built upon physical fault injection techniques that can precisely manipulate each bit in memory, such as Rowhammer attack [^3], or Laser Beam attack [^112]. These techniques often require some special equipment or computer architecture knowledge, which is difficult for most AI researchers. However, this barrier can be tackled through cross-disciplinary cooperation, and the practical security threat of weight attack deserves more attention in the future.

### X-C Adversarial Examples

#### X-C1 White-box Adversarial Attacks

After thorough exploration of white-box adversarial attacks, there have been massive and diverse methods, and now it is rare to see new white-box attack methods. Instead, white-box adversarial examples have been used as useful tools for other tasks, such as adversarial training ($e.g.$, using white-box adversarial examples to generate adversarial examples during the training procedure), backdoor attack ($e.g.$, using universal adversarial perturbation as the trigger, or erasing the original information of poisoned samples in label-consistent attacks), transfer-based attacks ($i.e.$, generating transferable adversarial examples on white-box surrogate models), privacy protection ($i.e.$, erasing the information of main objects in one sample to evade the third-party detection system), $etc.$

#### X-C2 Black-box Adversarial Attacks

- In terms of the score-based black-box adversarial examples, the combination-based methods have shown much better performance than the query-based methods, demonstrating the benefit of utilizing the surrogate priors. We think that the potentials of further improving attack performance lie in shrinking the gap between surrogate and target models, extracting more useful priors from surrogate models, and effectively combining surrogate priors and query feedback. Besides, the reported results in some latest works ($e.g.$, $\mathcal{CG}$ -Attack [^77] and MCG [^279]) are very good, and the median query number even achieves 1 and the attack success rate achieves 100% at some easy cases ($e.g.$, small data dimension, untargeted attack, regularly trained target model). It seems that the performance of score-based attacks is hitting the ceiling. However, it is notable that all these evaluations are conducted under the setting of no defense. As shown in recent black-box defense methods, $e.g.$, RND (slightly perturbing the query input) [^190] and AAA (slightly perturbing the query feedback) [^36], several SOTA black-box adversarial examples significantly degraded. It implies that future score-based adversarial examples should be defense-aware.
- In terms of the decision-based black-box adversarial examples, all existing decision-based methods are query-based. Although some priors are also extracted from surrogate models, they are used as fixed priors, without interaction with query feedback like the combination-based methods in score-based adversarial examples. Besides, due to the less feedback information, its attack performance is much poor than the score-based black-box adversarial examples. We think it is valuable to explore combination-based decision-based adversarial examples.
- One commonality of score-based and decision-based adversarial examples is that targeted adversarial examples are much more challenging than untargeted adversarial examples, reflected by more queries and lower attack performance, mainly due to the smaller region of one target class than the non-ground-truth class region. We think one feasible solution to improve targeted attack performance is accurately modeling the adversarial perturbation distribution conditioned on benign sample and target class.

#### X-C3 Transfer-based Adversarial Examples

Compared with white-box and black-box adversarial examples, the transfer-based adversarial examples have no requirement about the attacked model, posing higher practical threats. According to the reported evaluations in existing transfer-based adversarial examples, we observed that the attack performance is well if the training datasets and architectures between surrogate and target models are similar, otherwise the attack performance is very poor. It implies that improving adversarial transferability across datasets and model architectures is still the main challenge of this task. More importantly, we still lack a clear theoretical understanding of the intrinsic reason and characteristics of adversarial transferability, though several effective heuristic strategies or assumptions have been developed. We suggest that a solid theoretical analysis should consider the factors of data distribution, model architectures, loss landscape, decision surface, and get inspiration from the theory about model generalization across different data distributions. Besides, better understanding about adversarial transferability will be also beneficial to design more robust models in practice.

### X-D Comparisons of Three Attack Paradigms

Until now, the differences among the three attack paradigms have been clearly described, and it is found that their developments are almost independent. But there are still a few interactions. For example, although without explicit claims, it is obvious that the design of triggers or poisoned samples in backdoor attacks got inspiration from inference-time adversarial attacks, such as invisible triggers, or non-additive triggers. Besides, some adversarial examples were directly utilized in backdoor attacks, such as using the targeted universal adversarial perturbation [^162] as backdoor trigger [^293], or using inference-time adversarial examples to erase the original benign features in label-consistent backdoor attack [^301]. However, since these three attack paradigms occur in different stages of a machine learning system, it is difficult to integrate them to implement a unified attack. In contrast, we think that their interactions may be more close when taking the defense into account. Specifically, when designing a defense to improve the model robustness to one particular attack paradigm, one should consider whether the robustness to other attack paradigms will be harmed or not. For example, it is valuable to study the risk of adversarial training [^106] [^158] to backdoor attack, and whether the adversarially trained model is more vulnerable to weight attack. Some recent backdoor defense works [^39] [^96] shows that the backdoor injection could be inhibited through replacing the standard end-to-end supervised training by some well-designed secure training algorithms. However, whether the robustness of such trained model to adversarial examples or weight attacks is also improved or not should be further studied. In summary, we think that it is valuable to consider the above three attack paradigms from a systematic perspective, otherwise, the security of a machine learning system cannot be really improved.

## XI Summary

In this survey, we have proposed a unified definition and mathematical formulation about adversarial machine learning (AML), covering three main attack paradigms, including backdoor attack at the training stage, weight attack at the deployment stage and adversarial attack at the testing stage. This unified framework provided a systematic perspective of AML, which could not only help readers to quickly obtain a comprehensive understanding of this field, but also calibrate different paradigms to accelerate the overall development of AML.

Supplementary materials. Due to the space limit, several additional but important contents will be presented as supplementary materials, including:

1. Comparisons of three attack paradigms from different perspectives;
2. Summary of all mentioned weight attack methods;
3. Summary of the associations between each individual attack method and its categorizations.

## References

## Comparisons of Three Attack Paradigms

To further clarify the connections and differences of three attack paradigms, we provide:

1. Differences on inputs, outputs and formulations of three attack paradigms are summarized in Table III.
2. A simple illustration of three attack paradigms is shown in Fig. 4.

TABLE III: Comparisons among three attack paradigms of AML.

<table><tbody><tr><td rowspan="2"><p>Attack paradigm</p></td><td rowspan="2"><p>Inputs</p></td><td rowspan="2"><p>Outputs</p></td><td colspan="2">Stealthiness</td><td colspan="2">Benign consistency</td><td colspan="2">Adversarial inconsistency</td></tr><tr><td><p>AML.<math><semantics><msub><mi>𝒮</mi> <mi>𝐱</mi></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>𝒮</ci> <ci>𝐱</ci></apply></annotation-xml> <annotation>\mathcal{S}_{\mathbf{x}}</annotation> <annotation>caligraphic_S start_POSTSUBSCRIPT bold_x end_POSTSUBSCRIPT</annotation></semantics></math></p></td><td><p>AML.<math><semantics><msub><mi>𝒮</mi> <mi>𝐰</mi></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>𝒮</ci> <ci>𝐰</ci></apply></annotation-xml> <annotation>\mathcal{S}_{\mathbf{w}}</annotation> <annotation>caligraphic_S start_POSTSUBSCRIPT bold_w end_POSTSUBSCRIPT</annotation></semantics></math></p></td><td><p>AML.<math><semantics><msub><mi>𝒞</mi> <mi>A</mi></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>𝒞</ci> <ci>𝐴</ci></apply></annotation-xml> <annotation>\mathcal{C}_{A}</annotation> <annotation>caligraphic_C start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT</annotation></semantics></math></p></td><td><p>AML.<math><semantics><msub><mi>𝒞</mi> <mi>B</mi></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>𝒞</ci> <ci>𝐵</ci></apply></annotation-xml> <annotation>\mathcal{C}_{B}</annotation> <annotation>caligraphic_C start_POSTSUBSCRIPT italic_B end_POSTSUBSCRIPT</annotation></semantics></math></p></td><td><p>AML.<math><semantics><msub><mi>ℐ</mi> <mi>A</mi></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>ℐ</ci> <ci>𝐴</ci></apply></annotation-xml> <annotation>\mathcal{I}_{A}</annotation> <annotation>caligraphic_I start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT</annotation></semantics></math></p></td><td><p>AML.<math><semantics><msub><mi>ℐ</mi> <mi>B</mi></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>ℐ</ci> <ci>𝐵</ci></apply></annotation-xml> <annotation>\mathcal{I}_{B}</annotation> <annotation>caligraphic_I start_POSTSUBSCRIPT italic_B end_POSTSUBSCRIPT</annotation></semantics></math></p></td></tr><tr><td><p>Backdoor attack</p></td><td><p>Training dataset <math><semantics><msub><mi>D</mi> <mn>0</mn></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>𝐷</ci> <cn>0</cn></apply></annotation-xml> <annotation>D_{0}</annotation> <annotation>italic_D start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT</annotation></semantics></math> or control of training process</p></td><td><p><math><semantics><msub><mi>D</mi> <mi>ε</mi></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>𝐷</ci> <ci>𝜀</ci></apply></annotation-xml> <annotation>D_{\varepsilon}</annotation> <annotation>italic_D start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT</annotation></semantics></math> or <math><semantics><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mi>ε</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><mo>⋅</mo><mo>)</mo></mrow></mrow> <annotation-xml><apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply> <ci>⋅</ci></apply></annotation-xml> <annotation>f_{\mathbf{w}_{\varepsilon}}(\cdot)</annotation> <annotation>italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( ⋅ )</annotation></semantics></math></p></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td><p>Weight attack</p></td><td><p><math><semantics><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mn>0</mn></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><mo>⋅</mo><mo>)</mo></mrow></mrow> <annotation-xml><apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <cn>0</cn></apply></apply> <ci>⋅</ci></apply></annotation-xml> <annotation>f_{\mathbf{w}_{0}}(\cdot)</annotation> <annotation>italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( ⋅ )</annotation></semantics></math> & a few benign data & control of device memory</p></td><td><p><math><semantics><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mi>ε</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><mo>⋅</mo><mo>)</mo></mrow></mrow> <annotation-xml><apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply> <ci>⋅</ci></apply></annotation-xml> <annotation>f_{\mathbf{w}_{\varepsilon}}(\cdot)</annotation> <annotation>italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( ⋅ )</annotation></semantics></math></p></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td><p>Adversarial example</p></td><td><p><math><semantics><mrow><mo>(</mo><msub><mi>𝐱</mi> <mn>0</mn></msub><mo>,</mo><msub><mi>y</mi> <mn>0</mn></msub><mo>,</mo><msub><mi>y</mi> <mi>ε</mi></msub><mo>)</mo></mrow> <annotation-xml><vector><apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply> <apply><csymbol>subscript</csymbol> <ci>𝑦</ci> <cn>0</cn></apply> <apply><csymbol>subscript</csymbol> <ci>𝑦</ci> <ci>𝜀</ci></apply></vector></annotation-xml> <annotation>(\mathbf{x}_{0},y_{0},y_{\varepsilon})</annotation> <annotation>( bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT, italic_y start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT, italic_y start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT )</annotation></semantics></math> & weights or access permission of <math><semantics><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mn>0</mn></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><mo>⋅</mo><mo>)</mo></mrow></mrow> <annotation-xml><apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <cn>0</cn></apply></apply> <ci>⋅</ci></apply></annotation-xml> <annotation>f_{\mathbf{w}_{0}}(\cdot)</annotation> <annotation>italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( ⋅ )</annotation></semantics></math></p></td><td><p><math><semantics><msub><mi>𝐱</mi> <mi>ε</mi></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <ci>𝜀</ci></apply></annotation-xml> <annotation>\mathbf{x}_{\varepsilon}</annotation> <annotation>bold_x start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT</annotation></semantics></math></p></td><td></td><td></td><td></td><td></td><td></td><td></td></tr></tbody></table>

![Refer to caption](https://arxiv.org/html/2302.09457v2/extracted/5330208/imgs/category.png)

Refer to caption

## Summary of Weight Attack Methods

Compared to backdoor attacks and adversarial attacks, existing weight attacks are insufficient to form a complex taxonomy. Instead, we present a table to summarize all mentioned weight attack methods, as shown in Table IV.

TABLE IV: A brief summary of existing deployment-time adversarial attack ($i.e.$, weight attack) methods.

<table><tbody><tr><td>Category</td><td>Method</td><td>Description/Specification</td></tr><tr><td></td><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> Single bias attack (SBA) <sup><a href="#fn:151">151</a></sup></p></td><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> Simply enlarging the bias parameter of the target class</p></td></tr><tr><td></td><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> Gradient descent attack (GDA) <sup><a href="#fn:151">151</a></sup></p></td><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> <math><semantics><mrow><mrow><mrow><mi>arg</mi> <mo>⁡</mo> <mrow><msub><mi>min</mi> <msub><mi>𝐰</mi> <mi>ε</mi></msub></msub> <mo>⁡</mo> <msub><mi>𝒟</mi> <mi>𝐰</mi></msub></mrow></mrow> <mo>⁢</mo> <mrow><mo>(</mo><msub><mi>𝐰</mi> <mn>0</mn></msub><mo>,</mo><msub><mi>𝐰</mi> <mi>ε</mi></msub><mo>)</mo></mrow></mrow> <mo>+</mo> <mrow><msub><mi>λ</mi> <msub><mi>ℐ</mi> <mi>A</mi></msub></msub> <mo>⁢</mo> <msub><mi>ℒ</mi> <msub><mi>ℐ</mi> <mi>A</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mi>ε</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msub><mi>𝐱</mi> <mi>ε</mi></msub><mo>)</mo></mrow></mrow><mo>,</mo><msub><mi>y</mi> <mi>ε</mi></msub><mo>)</mo></mrow></mrow></mrow> <annotation-xml><apply><apply><apply><apply><apply><csymbol>subscript</csymbol> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply> <apply><csymbol>subscript</csymbol> <ci>𝒟</ci> <ci>𝐰</ci></apply></apply></apply> <interval><apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <cn>0</cn></apply> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></interval></apply> <apply><apply><csymbol>subscript</csymbol> <ci>𝜆</ci> <apply><csymbol>subscript</csymbol> <ci>ℐ</ci> <ci>𝐴</ci></apply></apply> <apply><csymbol>subscript</csymbol> <ci>ℒ</ci> <apply><csymbol>subscript</csymbol> <ci>ℐ</ci> <ci>𝐴</ci></apply></apply> <interval><apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <ci>𝜀</ci></apply></apply> <apply><csymbol>subscript</csymbol> <ci>𝑦</ci> <ci>𝜀</ci></apply></interval></apply></apply></annotation-xml> <annotation>\arg\min_{\mathbf{w}_{\varepsilon}}~{}\mathcal{D}_{\mathbf{w}}(\mathbf{w}_{0},% \mathbf{w}_{\varepsilon})+\lambda_{\mathcal{I}_{A}}\mathcal{L}_{\mathcal{I}_{A% }}(f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{\varepsilon}),y_{\varepsilon})</annotation> <annotation>roman_arg roman_min start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT end_POSTSUBSCRIPT caligraphic_D start_POSTSUBSCRIPT bold_w end_POSTSUBSCRIPT ( bold_w start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT, bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT ) + italic_λ start_POSTSUBSCRIPT caligraphic_I start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT end_POSTSUBSCRIPT caligraphic_L start_POSTSUBSCRIPT caligraphic_I start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT ), italic_y start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT )</annotation></semantics></math></p></td></tr><tr><td rowspan="5">Weight attack without trigger: <math><semantics><mrow><msub><mi>𝐱</mi> <mi>ε</mi></msub> <mo>=</mo> <msub><mi>𝐱</mi> <mn>0</mn></msub></mrow> <annotation-xml><apply><apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <ci>𝜀</ci></apply> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply></apply></annotation-xml> <annotation>\mathbf{x}_{\varepsilon}=\mathbf{x}_{0}</annotation> <annotation>bold_x start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT = bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT</annotation></semantics></math></td><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> Targeted bit-flip attack (T-BFA) <sup><a href="#fn:193">193</a></sup></p></td><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> <math><semantics><mrow><mrow><mrow><mrow><munder><mrow><mi>arg</mi> <mo>⁡</mo> <mi>min</mi></mrow> <mrow><msub><mi>𝐰</mi> <mi>ε</mi></msub> <mo>∈</mo> <msup><mrow><mo>{</mo> <mn>0</mn><mo>,</mo><mn>1</mn> <mo>}</mo></mrow> <mrow><mo>|</mo> <msub><mi>𝐰</mi> <mi>ε</mi></msub> <mo>|</mo></mrow></msup></mrow></munder> <mo>⁢</mo> <msub><mi>𝒟</mi> <mi>𝐰</mi></msub> <mo>⁢</mo> <mrow><mo>(</mo><msub><mi>𝐰</mi> <mn>0</mn></msub><mo>,</mo><msub><mi>𝐰</mi> <mi>ε</mi></msub><mo>)</mo></mrow></mrow> <mo>+</mo> <mrow><msub><mi>λ</mi> <msub><mi>𝒞</mi> <mi>A</mi></msub></msub> <mo>⁢</mo> <msub><mi>ℒ</mi> <msub><mi>𝒞</mi> <mi>A</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mi>ε</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msubsup><mi>𝐱</mi> <mn>0</mn> <mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow></msubsup><mo>)</mo></mrow></mrow><mo>,</mo><msubsup><mi>y</mi> <mn>0</mn> <mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow></msubsup><mo>)</mo></mrow></mrow> <mo>+</mo> <mrow><msub><mi>λ</mi> <msub><mi>ℐ</mi> <mi>A</mi></msub></msub> <mo>⁢</mo> <msub><mi>ℒ</mi> <msub><mi>ℐ</mi> <mi>A</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mi>ε</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msubsup><mi>𝐱</mi> <mi>ε</mi> <mrow><mo>(</mo><mi>j</mi><mo>)</mo></mrow></msubsup><mo>)</mo></mrow></mrow><mo>,</mo><msubsup><mi>y</mi> <mi>ε</mi> <mrow><mo>(</mo><mi>j</mi><mo>)</mo></mrow></msubsup><mo>)</mo></mrow></mrow></mrow><mo>,</mo><mi>i</mi></mrow> <mo>≠</mo> <mi>j</mi></mrow> <annotation-xml><apply><list><apply><apply><apply><apply><apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply> <apply><csymbol>superscript</csymbol> <set><cn>0</cn> <cn>1</cn></set> <apply><apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply></apply></apply></apply> <apply><csymbol>subscript</csymbol> <ci>𝒟</ci> <ci>𝐰</ci></apply> <interval><apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <cn>0</cn></apply> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></interval></apply> <apply><apply><csymbol>subscript</csymbol> <ci>𝜆</ci> <apply><csymbol>subscript</csymbol> <ci>𝒞</ci> <ci>𝐴</ci></apply></apply> <apply><csymbol>subscript</csymbol> <ci>ℒ</ci> <apply><csymbol>subscript</csymbol> <ci>𝒞</ci> <ci>𝐴</ci></apply></apply> <interval><apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply> <apply><csymbol>superscript</csymbol> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply> <ci>𝑖</ci></apply></apply> <apply><csymbol>superscript</csymbol> <apply><csymbol>subscript</csymbol> <ci>𝑦</ci> <cn>0</cn></apply> <ci>𝑖</ci></apply></interval></apply> <apply><apply><csymbol>subscript</csymbol> <ci>𝜆</ci> <apply><csymbol>subscript</csymbol> <ci>ℐ</ci> <ci>𝐴</ci></apply></apply> <apply><csymbol>subscript</csymbol> <ci>ℒ</ci> <apply><csymbol>subscript</csymbol> <ci>ℐ</ci> <ci>𝐴</ci></apply></apply> <interval><apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply> <apply><csymbol>superscript</csymbol> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <ci>𝜀</ci></apply> <ci>𝑗</ci></apply></apply> <apply><csymbol>superscript</csymbol> <apply><csymbol>subscript</csymbol> <ci>𝑦</ci> <ci>𝜀</ci></apply> <ci>𝑗</ci></apply></interval></apply></apply> <ci>𝑖</ci></list> <ci>𝑗</ci></apply></annotation-xml> <annotation>\underset{\mathbf{w}_{\varepsilon}\in\{0,1\}^{|\mathbf{w}_{\varepsilon}|}}{% \arg\min}~{}\mathcal{D}_{\mathbf{w}}(\mathbf{w}_{0},\mathbf{w}_{\varepsilon})+% \lambda_{\mathcal{C}_{A}}\mathcal{L}_{\mathcal{C}_{A}}(f_{\mathbf{w}_{% \varepsilon}}(\mathbf{x}_{0}^{(i)}),y_{0}^{(i)})+\lambda_{\mathcal{I}_{A}}% \mathcal{L}_{\mathcal{I}_{A}}(f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{% \varepsilon}^{(j)}),y_{\varepsilon}^{(j)}),i\neq j</annotation> <annotation>start_UNDERACCENT bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT ∈ { 0, 1 } start_POSTSUPERSCRIPT | bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT | end_POSTSUPERSCRIPT end_UNDERACCENT start_ARG roman_arg roman_min end_ARG caligraphic_D start_POSTSUBSCRIPT bold_w end_POSTSUBSCRIPT ( bold_w start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT, bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT ) + italic_λ start_POSTSUBSCRIPT caligraphic_C start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT end_POSTSUBSCRIPT caligraphic_L start_POSTSUBSCRIPT caligraphic_C start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT ), italic_y start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT ) + italic_λ start_POSTSUBSCRIPT caligraphic_I start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT end_POSTSUBSCRIPT caligraphic_L start_POSTSUBSCRIPT caligraphic_I start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ( italic_j ) end_POSTSUPERSCRIPT ), italic_y start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ( italic_j ) end_POSTSUPERSCRIPT ), italic_i ≠ italic_j</annotation></semantics></math></p></td></tr><tr><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> Fault sneaking attack (FSA) <sup><a href="#fn:300">300</a></sup></p></td><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> Almost same with T-BFA, with only one difference that there is no binary constraint <math><semantics><mrow><mrow><mi>w</mi><mo>.</mo><mi>r</mi><mo>.</mo><mi>t</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><csymbol>formulae-sequence</csymbol> <ci>𝑤</ci> <ci>𝑟</ci> <ci>𝑡</ci></apply></annotation-xml> <annotation>w.r.t.</annotation><annotation>italic_w. italic_r. italic_t.</annotation></semantics></math> <math><semantics><msub><mi>𝐰</mi> <mi>ε</mi></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></annotation-xml> <annotation>\mathbf{w}_{\varepsilon}</annotation> <annotation>bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT</annotation></semantics></math></p></td></tr><tr><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> Targeted attack with limited bit-flips (TA-LBF) <sup><a href="#fn:12">12</a></sup></p></td><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> Almost same with T-BFA, with two main differences: 1) attack one single data, rather than all data of one class; 2) an efficient optimization algorithm for binary optimization, rather than the heuristic algorithm</p></td></tr><tr><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> Robustness attack <sup><a href="#fn:83">83</a></sup></p></td><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> Changing the weights of the adversarially trained model via bit flipping to reduce the model’s robustness</p></td></tr><tr><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> Targeted bit Trojan (TBT) attack <sup><a href="#fn:192">192</a></sup></p></td><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> There are three steps: 1) Selecting a few neurons (<math><semantics><mrow><mrow><mi>i</mi><mo>.</mo><mi>e</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><csymbol>formulae-sequence</csymbol> <ci>𝑖</ci> <ci>𝑒</ci></apply></annotation-xml> <annotation>i.e.</annotation><annotation>italic_i. italic_e.</annotation></semantics></math>, weights) that contribute more to the target class; 2) generating an input-agnostic trigger <math><semantics><mrow><msub><mi>𝐱</mi> <mi>ε</mi></msub> <mo>−</mo> <msub><mi>𝐱</mi> <mn>0</mn></msub></mrow> <annotation-xml><apply><apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <ci>𝜀</ci></apply> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply></apply></annotation-xml> <annotation>\mathbf{x}_{\varepsilon}-\mathbf{x}_{0}</annotation> <annotation>bold_x start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT - bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT</annotation></semantics></math> by maximizing the activation of the selected neurons; 3) <math><semantics><mrow><mrow><mrow><mrow><mrow><mi>arg</mi> <mo>⁡</mo> <mrow><msub><mi>min</mi> <msub><mi>𝐰</mi> <mi>ε</mi></msub></msub> <mo>⁡</mo> <mrow><msub><mi>λ</mi> <msub><mi>𝒞</mi> <mi>A</mi></msub></msub> <mo>⁢</mo> <msub><mi>ℒ</mi> <msub><mi>𝒞</mi> <mi>A</mi></msub></msub></mrow></mrow></mrow> <mo>⁢</mo> <mrow><mo>(</mo><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mi>ε</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msubsup><mi>𝐱</mi> <mn>0</mn> <mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow></msubsup><mo>)</mo></mrow></mrow><mo>,</mo><msubsup><mi>y</mi> <mn>0</mn> <mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow></msubsup><mo>)</mo></mrow></mrow> <mo>+</mo> <mrow><msub><mi>λ</mi> <msub><mi>ℐ</mi> <mi>A</mi></msub></msub> <mo>⁢</mo> <msub><mi>ℒ</mi> <msub><mi>ℐ</mi> <mi>A</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mi>ε</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msubsup><mi>𝐱</mi> <mi>ε</mi> <mrow><mo>(</mo><mi>j</mi><mo>)</mo></mrow></msubsup><mo>)</mo></mrow></mrow><mo>,</mo><msubsup><mi>y</mi> <mi>ε</mi> <mrow><mo>(</mo><mi>j</mi><mo>)</mo></mrow></msubsup><mo>)</mo></mrow></mrow></mrow><mo>,</mo><mi>i</mi></mrow> <mo>≠</mo> <mi>j</mi></mrow> <annotation-xml><apply><list><apply><apply><apply><apply><apply><csymbol>subscript</csymbol> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply> <apply><apply><csymbol>subscript</csymbol> <ci>𝜆</ci> <apply><csymbol>subscript</csymbol> <ci>𝒞</ci> <ci>𝐴</ci></apply></apply> <apply><csymbol>subscript</csymbol> <ci>ℒ</ci> <apply><csymbol>subscript</csymbol> <ci>𝒞</ci> <ci>𝐴</ci></apply></apply></apply></apply></apply> <interval><apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply> <apply><csymbol>superscript</csymbol> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply> <ci>𝑖</ci></apply></apply> <apply><csymbol>superscript</csymbol> <apply><csymbol>subscript</csymbol> <ci>𝑦</ci> <cn>0</cn></apply> <ci>𝑖</ci></apply></interval></apply> <apply><apply><csymbol>subscript</csymbol> <ci>𝜆</ci> <apply><csymbol>subscript</csymbol> <ci>ℐ</ci> <ci>𝐴</ci></apply></apply> <apply><csymbol>subscript</csymbol> <ci>ℒ</ci> <apply><csymbol>subscript</csymbol> <ci>ℐ</ci> <ci>𝐴</ci></apply></apply> <interval><apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply> <apply><csymbol>superscript</csymbol> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <ci>𝜀</ci></apply> <ci>𝑗</ci></apply></apply> <apply><csymbol>superscript</csymbol> <apply><csymbol>subscript</csymbol> <ci>𝑦</ci> <ci>𝜀</ci></apply> <ci>𝑗</ci></apply></interval></apply></apply> <ci>𝑖</ci></list> <ci>𝑗</ci></apply></annotation-xml> <annotation>\arg\min_{\mathbf{w}_{\varepsilon}}~{}\lambda_{\mathcal{C}_{A}}\mathcal{L}_{% \mathcal{C}_{A}}(f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{0}^{(i)}),y_{0}^{(i)% })+\lambda_{\mathcal{I}_{A}}\mathcal{L}_{\mathcal{I}_{A}}(f_{\mathbf{w}_{% \varepsilon}}(\mathbf{x}_{\varepsilon}^{(j)}),y_{\varepsilon}^{(j)}),i\neq j</annotation> <annotation>roman_arg roman_min start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT end_POSTSUBSCRIPT italic_λ start_POSTSUBSCRIPT caligraphic_C start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT end_POSTSUBSCRIPT caligraphic_L start_POSTSUBSCRIPT caligraphic_C start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT ), italic_y start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT ) + italic_λ start_POSTSUBSCRIPT caligraphic_I start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT end_POSTSUBSCRIPT caligraphic_L start_POSTSUBSCRIPT caligraphic_I start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ( italic_j ) end_POSTSUPERSCRIPT ), italic_y start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ( italic_j ) end_POSTSUPERSCRIPT ), italic_i ≠ italic_j</annotation></semantics></math></p></td></tr><tr><td rowspan="7">Weight attack with trigger: <math><semantics><mrow><msub><mi>𝐱</mi> <mi>ε</mi></msub> <mo>≠</mo> <msub><mi>𝐱</mi> <mn>0</mn></msub></mrow> <annotation-xml><apply><apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <ci>𝜀</ci></apply> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply></apply></annotation-xml> <annotation>\mathbf{x}_{\varepsilon}\neq\mathbf{x}_{0}</annotation> <annotation>bold_x start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT ≠ bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT</annotation></semantics></math></td><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> ProFlip attack <sup><a href="#fn:30">30</a></sup></p></td><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> Adopting the same 3-step procedure with TBT, with different algorithm for each individual stage</p></td></tr><tr><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> Trojaning attack <sup><a href="#fn:148">148</a></sup></p></td><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> Almost same with TBT, with the main difference that the benign sample <math><semantics><msub><mi>𝐱</mi> <mn>0</mn></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply></annotation-xml> <annotation>\mathbf{x}_{0}</annotation> <annotation>bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT</annotation></semantics></math> is obtained by reverse engineering</p></td></tr><tr><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> Adversarial Weight Perturbation (AWP) <sup><a href="#fn:81">81</a></sup></p></td><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> Backdoor injection via slight weight perturbation: <math><semantics><mrow><mrow><mrow><mi>arg</mi> <mo>⁡</mo> <mrow><msub><mi>min</mi> <msub><mi>𝐰</mi> <mi>ε</mi></msub></msub> <mo>⁡</mo> <mrow><msub><mi>λ</mi> <msub><mi>ℐ</mi> <mi>A</mi></msub></msub> <mo>⁢</mo> <msub><mi>ℒ</mi> <msub><mi>ℐ</mi> <mi>A</mi></msub></msub></mrow></mrow></mrow> <mo>⁢</mo> <mrow><mo>(</mo><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mi>ε</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msubsup><mi>𝐱</mi> <mi>ε</mi> <mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow></msubsup><mo>)</mo></mrow></mrow><mo>,</mo><msubsup><mi>y</mi> <mi>ε</mi> <mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow></msubsup><mo>)</mo></mrow></mrow> <mo>+</mo> <mrow><msub><mi>ℛ</mi> <mn>3</mn></msub> <mo>⁢</mo> <mrow><mo>(</mo><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mi>ε</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msubsup><mi>𝐱</mi> <mn>0</mn> <mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow></msubsup><mo>)</mo></mrow></mrow><mo>,</mo><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mn>0</mn></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msubsup><mi>𝐱</mi> <mn>0</mn> <mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow></msubsup><mo>)</mo></mrow></mrow><mo>)</mo></mrow></mrow></mrow> <annotation-xml><apply><apply><apply><apply><apply><csymbol>subscript</csymbol> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply> <apply><apply><csymbol>subscript</csymbol> <ci>𝜆</ci> <apply><csymbol>subscript</csymbol> <ci>ℐ</ci> <ci>𝐴</ci></apply></apply> <apply><csymbol>subscript</csymbol> <ci>ℒ</ci> <apply><csymbol>subscript</csymbol> <ci>ℐ</ci> <ci>𝐴</ci></apply></apply></apply></apply></apply> <interval><apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply> <apply><csymbol>superscript</csymbol> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <ci>𝜀</ci></apply> <ci>𝑖</ci></apply></apply> <apply><csymbol>superscript</csymbol> <apply><csymbol>subscript</csymbol> <ci>𝑦</ci> <ci>𝜀</ci></apply> <ci>𝑖</ci></apply></interval></apply> <apply><apply><csymbol>subscript</csymbol> <ci>ℛ</ci> <cn>3</cn></apply> <interval><apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply> <apply><csymbol>superscript</csymbol> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply> <ci>𝑖</ci></apply></apply> <apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <cn>0</cn></apply></apply> <apply><csymbol>superscript</csymbol> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply> <ci>𝑖</ci></apply></apply></interval></apply></apply></annotation-xml> <annotation>\arg\min_{\mathbf{w}_{\varepsilon}}~{}\lambda_{\mathcal{I}_{A}}\mathcal{L}_{% \mathcal{I}_{A}}(f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{\varepsilon}^{(i)}),% y_{\varepsilon}^{(i)})+\mathcal{R}_{3}(f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}% _{0}^{(i)}),f_{\mathbf{w}_{0}}(\mathbf{x}_{0}^{(i)}))</annotation> <annotation>roman_arg roman_min start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT end_POSTSUBSCRIPT italic_λ start_POSTSUBSCRIPT caligraphic_I start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT end_POSTSUBSCRIPT caligraphic_L start_POSTSUBSCRIPT caligraphic_I start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT ), italic_y start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT ) + caligraphic_R start_POSTSUBSCRIPT 3 end_POSTSUBSCRIPT ( italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT ), italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT ) )</annotation></semantics></math></p></td></tr><tr><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> Anchoring attack <sup><a href="#fn:296">296</a></sup></p></td><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> Backdoor injection via slight weight perturbation: <math><semantics><mrow><mrow><mrow><mi>arg</mi> <mo>⁡</mo> <mrow><msub><mi>min</mi> <msub><mi>𝐰</mi> <mi>ε</mi></msub></msub> <mo>⁡</mo> <mrow><msub><mi>λ</mi> <msub><mi>𝒞</mi> <mi>A</mi></msub></msub> <mo>⁢</mo> <msub><mi>ℒ</mi> <msub><mi>𝒞</mi> <mi>A</mi></msub></msub></mrow></mrow></mrow> <mo>⁢</mo> <mrow><mo>(</mo><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mi>ε</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msubsup><mi>𝐱</mi> <mn>0</mn> <mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow></msubsup><mo>)</mo></mrow></mrow><mo>,</mo><msubsup><mi>y</mi> <mn>0</mn> <mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow></msubsup><mo>)</mo></mrow></mrow> <mo>+</mo> <mrow><msub><mi>λ</mi> <msub><mi>ℐ</mi> <mi>A</mi></msub></msub> <mo>⁢</mo> <msub><mi>ℒ</mi> <msub><mi>ℐ</mi> <mi>A</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><mrow><msub><mi>f</mi> <msub><mi>𝐰</mi> <mi>ε</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msubsup><mi>𝐱</mi> <mi>ε</mi> <mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow></msubsup><mo>)</mo></mrow></mrow><mo>,</mo><msubsup><mi>y</mi> <mi>ε</mi> <mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow></msubsup><mo>)</mo></mrow></mrow> <mo>+</mo> <mrow><msub><mi>ℛ</mi> <mn>3</mn></msub> <mo>⁢</mo> <mrow><mo>(</mo><mrow><msub><mi>g</mi> <msub><mi>𝐰</mi> <mi>ε</mi></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msubsup><mi>𝐱</mi> <mn>0</mn> <mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow></msubsup><mo>)</mo></mrow></mrow><mo>,</mo><mrow><msub><mi>g</mi> <msub><mi>𝐰</mi> <mn>0</mn></msub></msub> <mo>⁢</mo> <mrow><mo>(</mo><msubsup><mi>𝐱</mi> <mn>0</mn> <mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow></msubsup><mo>)</mo></mrow></mrow><mo>)</mo></mrow></mrow></mrow> <annotation-xml><apply><apply><apply><apply><apply><csymbol>subscript</csymbol> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply> <apply><apply><csymbol>subscript</csymbol> <ci>𝜆</ci> <apply><csymbol>subscript</csymbol> <ci>𝒞</ci> <ci>𝐴</ci></apply></apply> <apply><csymbol>subscript</csymbol> <ci>ℒ</ci> <apply><csymbol>subscript</csymbol> <ci>𝒞</ci> <ci>𝐴</ci></apply></apply></apply></apply></apply> <interval><apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply> <apply><csymbol>superscript</csymbol> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply> <ci>𝑖</ci></apply></apply> <apply><csymbol>superscript</csymbol> <apply><csymbol>subscript</csymbol> <ci>𝑦</ci> <cn>0</cn></apply> <ci>𝑖</ci></apply></interval></apply> <apply><apply><csymbol>subscript</csymbol> <ci>𝜆</ci> <apply><csymbol>subscript</csymbol> <ci>ℐ</ci> <ci>𝐴</ci></apply></apply> <apply><csymbol>subscript</csymbol> <ci>ℒ</ci> <apply><csymbol>subscript</csymbol> <ci>ℐ</ci> <ci>𝐴</ci></apply></apply> <interval><apply><apply><csymbol>subscript</csymbol> <ci>𝑓</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply> <apply><csymbol>superscript</csymbol> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <ci>𝜀</ci></apply> <ci>𝑖</ci></apply></apply> <apply><csymbol>superscript</csymbol> <apply><csymbol>subscript</csymbol> <ci>𝑦</ci> <ci>𝜀</ci></apply> <ci>𝑖</ci></apply></interval></apply> <apply><apply><csymbol>subscript</csymbol> <ci>ℛ</ci> <cn>3</cn></apply> <interval><apply><apply><csymbol>subscript</csymbol> <ci>𝑔</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></apply> <apply><csymbol>superscript</csymbol> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply> <ci>𝑖</ci></apply></apply> <apply><apply><csymbol>subscript</csymbol> <ci>𝑔</ci> <apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <cn>0</cn></apply></apply> <apply><csymbol>superscript</csymbol> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply> <ci>𝑖</ci></apply></apply></interval></apply></apply></annotation-xml> <annotation>\arg\min_{\mathbf{w}_{\varepsilon}}~{}\lambda_{\mathcal{C}_{A}}\mathcal{L}_{% \mathcal{C}_{A}}(f_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{0}^{(i)}),y_{0}^{(i)% })+\lambda_{\mathcal{I}_{A}}\mathcal{L}_{\mathcal{I}_{A}}(f_{\mathbf{w}_{% \varepsilon}}(\mathbf{x}_{\varepsilon}^{(i)}),y_{\varepsilon}^{(i)})+\mathcal{% R}_{3}(g_{\mathbf{w}_{\varepsilon}}(\mathbf{x}_{0}^{(i)}),g_{\mathbf{w}_{0}}(% \mathbf{x}_{0}^{(i)}))</annotation> <annotation>roman_arg roman_min start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT end_POSTSUBSCRIPT italic_λ start_POSTSUBSCRIPT caligraphic_C start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT end_POSTSUBSCRIPT caligraphic_L start_POSTSUBSCRIPT caligraphic_C start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT ), italic_y start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT ) + italic_λ start_POSTSUBSCRIPT caligraphic_I start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT end_POSTSUBSCRIPT caligraphic_L start_POSTSUBSCRIPT caligraphic_I start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( italic_f start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT ), italic_y start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT ) + caligraphic_R start_POSTSUBSCRIPT 3 end_POSTSUBSCRIPT ( italic_g start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT ), italic_g start_POSTSUBSCRIPT bold_w start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT end_POSTSUBSCRIPT ( bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ( italic_i ) end_POSTSUPERSCRIPT ) )</annotation></semantics></math>, where <math><semantics><mi>g</mi> <annotation-xml><ci>𝑔</ci></annotation-xml> <annotation>g</annotation> <annotation>italic_g</annotation></semantics></math> denotes the logit</p></td></tr><tr><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> Subnet replacement attack (SRA) <sup><a href="#fn:186">186</a></sup></p></td><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> Replacing one subnet in the benign model by the backdoor subnet and cutting off the connection to remaining part of the model</p></td></tr><tr><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> Triggered samples attack (TSA) <sup><a href="#fn:11">11</a></sup></p></td><td><p><math><semantics><mo>⋄</mo> <annotation-xml><ci>⋄</ci></annotation-xml> <annotation>\diamond</annotation> <annotation>⋄</annotation></semantics></math> Extension of TA-LBF by introducing a trigger <math><semantics><mrow><msub><mi>𝐱</mi> <mi>ε</mi></msub> <mo>−</mo> <msub><mi>𝐱</mi> <mn>0</mn></msub></mrow> <annotation-xml><apply><apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <ci>𝜀</ci></apply> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply></apply></annotation-xml> <annotation>\mathbf{x}_{\varepsilon}-\mathbf{x}_{0}</annotation> <annotation>bold_x start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT - bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT</annotation></semantics></math>, and optimizing <math><semantics><msub><mi>𝐰</mi> <mi>ε</mi></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>𝐰</ci> <ci>𝜀</ci></apply></annotation-xml> <annotation>\mathbf{w}_{\varepsilon}</annotation> <annotation>bold_w start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT</annotation></semantics></math> and trigger <math><semantics><mrow><msub><mi>𝐱</mi> <mi>ε</mi></msub> <mo>−</mo> <msub><mi>𝐱</mi> <mn>0</mn></msub></mrow> <annotation-xml><apply><apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <ci>𝜀</ci></apply> <apply><csymbol>subscript</csymbol> <ci>𝐱</ci> <cn>0</cn></apply></apply></annotation-xml> <annotation>\mathbf{x}_{\varepsilon}-\mathbf{x}_{0}</annotation> <annotation>bold_x start_POSTSUBSCRIPT italic_ε end_POSTSUBSCRIPT - bold_x start_POSTSUBSCRIPT 0 end_POSTSUBSCRIPT</annotation></semantics></math> jointly by solving a mixed integer programming problem, such that the modified model will be activated by the trigger</p></td></tr></tbody></table>

## Appendix A Related Resources of Adversarial Machine Learning

To help readers quickly explore adversarial phenomenon of machine learning, we collect related resources of adversarial machine learning, including several open-source toolboxes and benchmarks, as shown in Table V.

TABLE V: Related open-source toolboxes and benchmarks in adversarial machine learning.

|  | Year | Backdoor learning | Adversarial example | Toolbox | Benchmark | Link |
| --- | --- | --- | --- | --- | --- | --- |
| BackdoorBench [^247] | 2022 | ✓ |  | ✓ | ✓ | [https://github.com/SCLBD/backdoorbench](https://github.com/SCLBD/backdoorbench) |
| BlackboxBench [^250] | 2022 |  | ✓ | ✓ | ✓ | [https://github.com/SCLBD/BlackboxBench](https://github.com/SCLBD/BlackboxBench) |
| OpenBackdoor [^52] | 2022 | ✓ |  | ✓ | ✓ | [https://github.com/thunlp/OpenBackdoor](https://github.com/thunlp/OpenBackdoor) |
| Responsible AI Toolbox [^210] | 2022 |  | ✓ | ✓ |  | [https://github.com/mit-ll-responsible-ai/responsible-ai-toolbox](https://github.com/mit-ll-responsible-ai/responsible-ai-toolbox) |
| Adversarial GLUE [^227] | 2021 |  |  | ✓ | ✓ | [https://github.com/AI-secure/adversarial-glue](https://github.com/AI-secure/adversarial-glue) |
| DeepRobust [^132] | 2021 |  | ✓ | ✓ |  | [https://github.com/DSE-MSU/DeepRobust](https://github.com/DSE-MSU/DeepRobust) |
| OpenAttack [^286] | 2021 |  | ✓ | ✓ |  | [https://github.com/thunlp/OpenAttack](https://github.com/thunlp/OpenAttack) |
| Adversarial Robustness Benchmark [^225] | 2021 |  | ✓ | ✓ | ✓ | [https://ml.cs.tsinghua.edu.cn/adv-bench](https://ml.cs.tsinghua.edu.cn/adv-bench) |
| RobustBench [^48] | 2021 |  | ✓ | ✓ | ✓ | [https://github.com/RobustBench/robustbench](https://github.com/RobustBench/robustbench) |
| TextAttack [^166] | 2020 |  | ✓ | ✓ |  | [https://github.com/QData/TextAttack](https://github.com/QData/TextAttack) |
| TrojanZoo [^178] | 2020 | ✓ |  | ✓ |  | [https://github.com/ain-soph/trojanzoo](https://github.com/ain-soph/trojanzoo) |
| AutoAttack [^51] | 2020 |  | ✓ | ✓ |  | [https://github.com/fra31/auto-attack](https://github.com/fra31/auto-attack) |
| Advbox [^87] | 2020 |  | ✓ | ✓ |  | [https://github.com/advboxes/AdvBox](https://github.com/advboxes/AdvBox) |
| AdverTorch [^54] | 2019 |  | ✓ | ✓ |  | [https://github.com/BorealisAI/advertorch](https://github.com/BorealisAI/advertorch) |
| DEEPSEC [^142] | 2019 |  | ✓ | ✓ |  | [https://github.com/ryderling/DEEPSEC](https://github.com/ryderling/DEEPSEC) |
| CleverHans [^179] | 2018 |  | ✓ | ✓ |  | [https://github.com/cleverhans-lab/cleverhans](https://github.com/cleverhans-lab/cleverhans) |
| Adversarial Robustness Toolbox [^175] | 2018 |  | ✓ | ✓ |  | [https://github.com/Trusted-AI/adversarial-robustness-toolbox](https://github.com/Trusted-AI/adversarial-robustness-toolbox) |
| Foolbox [^194] | 2017 |  | ✓ | ✓ |  | [https://github.com/bethgelab/foolbox](https://github.com/bethgelab/foolbox) |

## Associated Categorizations of Each Individual Method

Note that in the taxonomies presented in the main manuscript, each individual method could belong to multiple categorizes simultaneously. To facilitate the quick review of each individual method, we provide four tables to summarize the associated categorizations for each method in different attack paradigms, as shown in Tables VI, VII, IV, IX, and X, respectively. Moreover, we provide a website, $i.e.$, [http://adversarial-ml.com](http://adversarial-ml.com/), where the taxonomies and related literature are clearly presented. This website will be well maintained and continuously updated to cover more literature into the taxonomies.

TABLE VI: Categorization of existing data-poisoning based backdoor attack methods. For each categorization criterion “A/B”, ○ denotes the former “A”, ● denotes the latter “B” and ◑ represents both.

<table><tbody><tr><td></td><td></td><td colspan="9">Data-poisoning based backdoor attack</td></tr><tr><td><p>Method</p></td><td><p>Venue</p></td><td>Visible / Invisible</td><td>Non-semantic / Semantic</td><td>Manually designed / Leanable</td><td>Digital / Physical</td><td>Additive / Non-additive</td><td>Static / Dynamic</td><td>Sample-agnostic / specific</td><td>Label-inconsistent / consistent</td><td>Single / Multi-target</td></tr><tr><td><p>BadNets <sup><a href="#fn:88">88</a></sup></p></td><td><p>IEEE Access 2019</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>◑</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>◑</p></td></tr><tr><td><p>Blended <sup><a href="#fn:41">41</a></sup></p></td><td><p>arXiv 2017</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>◑</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>TrojanNN <sup><a href="#fn:148">148</a></sup></p></td><td><p>NDSS 2018</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Shafahi <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:200">200</a></sup></p></td><td><p>NeurIPS 2018</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td></tr><tr><td><p>SIG <sup><a href="#fn:14">14</a></sup></p></td><td><p>ICIP 2019</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td></tr><tr><td><p>LC <sup><a href="#fn:224">224</a></sup></p></td><td><p>arXiv 2019</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td></tr><tr><td><p>Yao <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:277">277</a></sup></p></td><td><p>CCS 2019</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>◑</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Saha <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:195">195</a></sup></p></td><td><p>AAAI 2020</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td></tr><tr><td><p>Static <sup><a href="#fn:306">306</a></sup></p></td><td><p>CODASPY 2020</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Adaptive <sup><a href="#fn:306">306</a></sup></p></td><td><p>CODASPY 2020</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Zhao <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:301">301</a></sup></p></td><td><p>CVPR 2020</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td></tr><tr><td><p>Refool <sup><a href="#fn:149">149</a></sup></p></td><td><p>ECCV 2020</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td></tr><tr><td><p>Li <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:119">119</a></sup></p></td><td><p>arXiv 2020</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>DeHiB <sup><a href="#fn:274">274</a></sup></p></td><td><p>AAAI 2021</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td></tr><tr><td><p>Wenger <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:243">243</a></sup></p></td><td><p>CVPR 2021</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Li <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:125">125</a></sup></p></td><td><p>ICLR Workshop 2021</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Steganography <sup><a href="#fn:126">126</a></sup></p></td><td><p>IEEE TDSC 2021</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Regularization <sup><a href="#fn:126">126</a></sup></p></td><td><p>IEEE TDSC 2021</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Invisible Poison <sup><a href="#fn:176">176</a></sup></p></td><td><p>INFOCOM 2021</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td></tr><tr><td><p>ROBNET <sup><a href="#fn:84">84</a></sup></p></td><td><p>IEEE JSAC 2021</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>◑</p></td></tr><tr><td><p>AdvDoor <sup><a href="#fn:293">293</a></sup></p></td><td><p>ISSTA 2021</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>PCBA <sup><a href="#fn:257">257</a></sup></p></td><td><p>ICCV 2021</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>PointPBA <sup><a href="#fn:129">129</a></sup></p></td><td><p>ICCV 2021</p></td><td><p>◑</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>◑</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>PointCPB <sup><a href="#fn:129">129</a></sup></p></td><td><p>ICCV 2021</p></td><td><p>◑</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>◑</p></td><td><p>●</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td></tr><tr><td><p>SSBA <sup><a href="#fn:134">134</a></sup></p></td><td><p>ICCV 2021</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Phan <sup><a href="#fn:183">183</a></sup></p></td><td><p>ICASSP 2022</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○1</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Random Backdoor <sup><a href="#fn:196">196</a></sup></p></td><td><p>Euro S&P 2022</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>◑</p></td></tr><tr><td><p>FTrojan <sup><a href="#fn:231">231</a></sup></p></td><td><p>ECCV 2022</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Sleeper Agent <sup><a href="#fn:213">213</a></sup></p></td><td><p>NeruIPS 2022</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td></tr><tr><td><p>PTB <sup><a href="#fn:272">272</a></sup></p></td><td><p>C & S 2022</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>FaceHack <sup><a href="#fn:197">197</a></sup></p></td><td><p>IEEE TBBIS 2022</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Han <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:92">92</a></sup></p></td><td><p>MM 2022</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>◑</p></td><td><p>○</p></td></tr><tr><td><p>IRBA <sup><a href="#fn:79">79</a></sup></p></td><td><p>arXiv 2022</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Wang <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:237">237</a></sup></p></td><td><p>IEEE TIFS</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Adap-Blend <sup><a href="#fn:185">185</a></sup></p></td><td><p>ICLR 2023</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Yu <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:282">282</a></sup></p></td><td><p>CVPR 2023</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Color Backdoor <sup><a href="#fn:107">107</a></sup></p></td><td><p>CVPR 2023</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>VSSC <sup><a href="#fn:230">230</a></sup></p></td><td><p>arXiv 2023</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>◑</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>◑</p></td></tr><tr><td><p>FLIP <sup><a href="#fn:105">105</a></sup></p></td><td><p>NeurIPS 2023</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr></tbody></table>

TABLE VII: Categorization of existing training-controllable based backdoor attack methods. For each categorization criterion “A/B”, ○ denotes the former “A”, ● denotes the latter “B” and ◑ represents both. For criterion “A/B/C”, ○, ●, ◖, ◗denote “A”, “B”, “C”, “D” respectively. For the methods of partially controlling the training data and process, we omit trigger since there is no distinguishable trigger listed in the table.

<table><tbody><tr><td></td><td></td><td colspan="9">Data-poisoning based backdoor attack</td><td colspan="4">Training-controllable based backdoor attack</td></tr><tr><td><p>Method</p></td><td><p>Venue</p></td><td>Visible / Invisible</td><td>Non-semantic / Semantic</td><td>Manually designed / Leanable</td><td>Digital / Physical</td><td>Additive / Non-additive</td><td>Static / Dynamic</td><td>Sample-agnostic / specific</td><td>Label-inconsistent / consistent</td><td>Single / Multi-target</td><td>One / Two-stage</td><td>Full / Partial access of training data</td><td>Full / Partial control of training process</td><td>Controlling training loss / algorithm / order</td></tr><tr><td><p>Bhagoji <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:15">15</a></sup></p></td><td><p>ICML 2019</p></td><td></td><td></td><td></td><td><p>○</p></td><td></td><td></td><td></td><td></td><td></td><td></td><td><p>●</p></td><td></td><td></td></tr><tr><td><p>Bagdasaryan <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:10">10</a></sup></p></td><td><p>AISTATS 2020</p></td><td></td><td></td><td></td><td><p>○</p></td><td></td><td></td><td></td><td></td><td></td><td></td><td><p>●</p></td><td></td><td></td></tr><tr><td><p>Wang <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:229">229</a></sup></p></td><td><p>NeruIPS 2020</p></td><td></td><td></td><td></td><td><p>○</p></td><td></td><td></td><td></td><td></td><td></td><td></td><td><p>●</p></td><td></td><td></td></tr><tr><td><p>Fung <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:78">78</a></sup></p></td><td><p>RAID 2020</p></td><td></td><td></td><td></td><td><p>○</p></td><td></td><td></td><td></td><td></td><td></td><td></td><td><p>●</p></td><td></td><td></td></tr><tr><td><p>Chen <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:29">29</a></sup></p></td><td><p>arXiv 2020</p></td><td></td><td></td><td></td><td><p>○</p></td><td></td><td></td><td></td><td></td><td></td><td></td><td><p>●</p></td><td></td><td></td></tr><tr><td><p>Liu <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:152">152</a></sup></p></td><td><p>arXiv 2020</p></td><td></td><td></td><td></td><td><p>○</p></td><td></td><td></td><td></td><td></td><td></td><td></td><td><p>●</p></td><td></td><td></td></tr><tr><td><p>Composite Attack <sup><a href="#fn:141">141</a></sup></p></td><td><p>CCS 2020</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>◑</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td></tr><tr><td><p>Tan <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:208">208</a></sup></p></td><td><p>Euro S&P 2020</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>DBA <sup><a href="#fn:260">260</a></sup></p></td><td><p>ICLR 2020</p></td><td></td><td></td><td></td><td><p>○</p></td><td></td><td></td><td></td><td></td><td></td><td></td><td><p>●</p></td><td></td><td></td></tr><tr><td><p>TrojanNet <sup><a href="#fn:221">221</a></sup></p></td><td><p>KDD 2020</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>◑</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td></tr><tr><td><p>Nguyen <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:173">173</a></sup></p></td><td><p>NeruIPS 2020</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td></tr><tr><td><p>DFST <sup><a href="#fn:45">45</a></sup></p></td><td><p>AAAI 2021</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td></tr><tr><td><p>WaNet <sup><a href="#fn:174">174</a></sup></p></td><td><p>ICLR 2021</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td></tr><tr><td><p>WB <sup><a href="#fn:56">56</a></sup></p></td><td><p>NeruIPS 2021</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>BOB <sup><a href="#fn:209">209</a></sup></p></td><td><p>NeurIPS 2021</p></td><td></td><td></td><td></td><td><p>○</p></td><td></td><td></td><td></td><td></td><td></td><td></td><td><p>○</p></td><td><p>○</p></td><td><p>◖</p></td></tr><tr><td><p>LIRA <sup><a href="#fn:57">57</a></sup></p></td><td><p>ICCV 2021</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td></tr><tr><td><p>LWP <sup><a href="#fn:123">123</a></sup></p></td><td><p>EMNLP 2021</p></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td></tr><tr><td><p>Shen <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:203">203</a></sup></p></td><td><p>CCS 2021</p></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td></tr><tr><td><p>HB <sup><a href="#fn:177">177</a></sup></p></td><td><p>AAAI 2022</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td></tr><tr><td><p>DEFEAT <sup><a href="#fn:303">303</a></sup></p></td><td><p>AAAI 2022</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td></tr><tr><td><p>BaN <sup><a href="#fn:196">196</a></sup></p></td><td><p>Euro S&P 2022</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>◑</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td></tr><tr><td><p>c-BaN <sup><a href="#fn:196">196</a></sup></p></td><td><p>Euro S&P 2022</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>◑</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td></tr><tr><td><p>RIBAC <sup><a href="#fn:182">182</a></sup></p></td><td><p>ECCV 2022</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>◑</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td></tr><tr><td><p>Feng <sup><a href="#fn:74">74</a></sup></p></td><td><p>ICASSP 2022</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Zhong <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:307">307</a></sup></p></td><td><p>IJCAI 2022</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td></tr><tr><td><p>Wen <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:242">242</a></sup></p></td><td><p>arXiv 2022</p></td><td></td><td></td><td></td><td><p>○</p></td><td></td><td></td><td></td><td></td><td></td><td></td><td><p>●</p></td><td></td><td></td></tr><tr><td><p>BPPATTACK <sup><a href="#fn:239">239</a></sup></p></td><td><p>CVPR 2022</p></td><td></td><td></td><td></td><td><p>○</p></td><td></td><td></td><td></td><td></td><td></td><td></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>FIBA <sup><a href="#fn:76">76</a></sup></p></td><td><p>CVPR 2022</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td></tr><tr><td><p>Marksman <sup><a href="#fn:58">58</a></sup></p></td><td><p>NeurIPS 2022</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>◑</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td></tr><tr><td><p>Poison Ink <sup><a href="#fn:289">289</a></sup></p></td><td><p>IEEE TIP 2022</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td></tr><tr><td><p>NTBA <sup><a href="#fn:93">93</a></sup></p></td><td><p>ICLR 2023</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td></tr><tr><td><p>EfficFrog <sup><a href="#fn:35">35</a></sup></p></td><td><p>CVPR 2023</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td></tr><tr><td><p>MAB <sup><a href="#fn:17">17</a></sup></p></td><td><p>CVPR 2023</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td></tr><tr><td><p>IBA <sup><a href="#fn:172">172</a></sup></p></td><td><p>NeurIPS 2023</p></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td><p>●</p></td><td></td><td></td></tr><tr><td><p>A3FL <sup><a href="#fn:288">288</a></sup></p></td><td><p>NeruIPS 2023</p></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td><p>●</p></td><td></td><td></td></tr></tbody></table>

TABLE VIII: Categorization of existing existing deployment-time adversarial attack ($i.e.$, weight attack) methods.

| Method | Venue | Weight Attack without Trigger | Weight Attack with Trigger |
| --- | --- | --- | --- |
| SBA [^151] | ICCAD 2017 | 🌑 |  |
| GDA [^151] | ICCAD 2017 | 🌑 |  |
| Trojaning attack [^148] | NDSS 2018 |  | 🌑 |
| FSA [^300] | DAC 2019 | 🌑 |  |
| AWP [^81] | CIKM 2020 |  | 🌑 |
| TBT [^192] | CVPR 2020 |  | 🌑 |
| TA-LBF [^12] | ICLR 2021 | 🌑 |  |
| Anchoring attack [^296] | ICLR 2021 |  | 🌑 |
| ProFlip [^30] | ICCV 2021 |  | 🌑 |
| Robustness attack [^83] | ISQED 2022 | 🌑 |  |
| SRA [^186] | CVPR 2022 |  | 🌑 |
| TSA [^11] | arXiv 2022 |  | 🌑 |
| T-BFA [^193] | IEEE TPAMI 2022 | 🌑 |  |

TABLE IX: Categorization of existing white-box adversarial examples. For any classification criterion “A/B”, ○ denotes the former “A”, ● denotes the latter “B”.

<table><tbody><tr><td></td><td></td><td colspan="7">White-box adversarial examples</td></tr><tr><td><p>Method</p></td><td><p>Venue</p></td><td>Digtial / Physical</td><td>Optimization / Learning-based</td><td>Sample-agnostic / specific</td><td>Additive / Non-additive</td><td>Dense / Sparse</td><td>Untargeted / Targeted</td><td>Factorized / Structured</td></tr><tr><td><p>Sharif <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:201">201</a></sup></p></td><td><p>CCS 2016</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Kurakin <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:116">116</a></sup></p></td><td><p>ICLR 2017</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>UAP <sup><a href="#fn:162">162</a></sup></p></td><td><p>CVPR 2017</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>JSMA <sup><a href="#fn:180">180</a></sup></p></td><td><p>EuroS&P 2016</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Mopuri <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:164">164</a></sup></p></td><td><p>BMVA 2017</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Carlini <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:23">23</a></sup></p></td><td><p>IEEE S&P 2017</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>LocSearchAdv <sup><a href="#fn:167">167</a></sup></p></td><td><p>CVPR 2017</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>GD-UAP <sup><a href="#fn:165">165</a></sup></p></td><td><p>IEEE TPAMI 2018</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Carlini <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:24">24</a></sup></p></td><td><p>IEEE SPW 2018</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td></tr><tr><td><p>ShapeShifter <sup><a href="#fn:37">37</a></sup></p></td><td><p>ECML-PKDD 2018</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>RP2 <sup><a href="#fn:70">70</a></sup></p></td><td><p>CVPR 2018</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Xu <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:269">269</a></sup></p></td><td><p>CVPR 2018</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td></tr><tr><td><p>Manifool <sup><a href="#fn:109">109</a></sup></p></td><td><p>CVPR 2018</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Shi <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:204">204</a></sup></p></td><td><p>COLING 2018</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td></tr><tr><td><p>AC-GAN <sup><a href="#fn:212">212</a></sup></p></td><td><p>NeurIPS 2018</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>advGAN <sup><a href="#fn:258">258</a></sup></p></td><td><p>IJCAI 2018</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>stAdv <sup><a href="#fn:259">259</a></sup></p></td><td><p>ICLR 2018</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Athalye <sup><a href="#fn:9">9</a></sup></p></td><td><p>ICML 2018</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>LaVAN <sup><a href="#fn:110">110</a></sup></p></td><td><p>ICML 2018</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>CGAN-Adv <sup><a href="#fn:281">281</a></sup></p></td><td><p>ICPR 2018</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Zhao <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:299">299</a></sup></p></td><td><p>MM 2018</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Chen <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:31">31</a></sup></p></td><td><p>ACL 2018</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td></tr><tr><td><p>Jan <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:104">104</a></sup></p></td><td><p>AAAI 2019</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Wei <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:241">241</a></sup></p></td><td><p>AAAI 2019</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>PS-GAN <sup><a href="#fn:143">143</a></sup></p></td><td><p>AAAI 2019</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>ERCG <sup><a href="#fn:302">302</a></sup></p></td><td><p>CCS 2019</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Qin <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:188">188</a></sup></p></td><td><p>ICML 2019</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Engstrom <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:68">68</a></sup></p></td><td><p>ICML 2019</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Wong <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:246">246</a></sup></p></td><td><p>ICML 2019</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>ReColorAdv <sup><a href="#fn:117">117</a></sup></p></td><td><p>NeurIPS 2019</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>AT-GAN <sup><a href="#fn:233">233</a></sup></p></td><td><p>arXiv 2019</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Yakura <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:273">273</a></sup></p></td><td><p>IJCAI 2019</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>AdvFaces <sup><a href="#fn:53">53</a></sup></p></td><td><p>IJCB 2019</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>AGNs <sup><a href="#fn:202">202</a></sup></p></td><td><p>TOPS 2019</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>SparseFool <sup><a href="#fn:159">159</a></sup></p></td><td><p>CVPR 2019</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Xu <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:270">270</a></sup></p></td><td><p>CVPR 2019</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td></tr><tr><td><p>AdvPattern <sup><a href="#fn:240">240</a></sup></p></td><td><p>ICCV 2019</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>CornerSearch <sup><a href="#fn:49">49</a></sup></p></td><td><p>ICCV 2019</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>PD-UA <sup><a href="#fn:144">144</a></sup></p></td><td><p>ICCV 2019</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Schott <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:199">199</a></sup></p></td><td><p>ICLR 2019</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Xu <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:264">264</a></sup></p></td><td><p>ICLR 2019</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Su <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:216">216</a></sup></p></td><td><p>IEEE TEC 2019</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>CD-UAP <sup><a href="#fn:287">287</a></sup></p></td><td><p>AAAI 2020</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Xu <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:265">265</a></sup></p></td><td><p>ECCV 2020</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Wu <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:254">254</a></sup></p></td><td><p>ECCV 2020</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>SAPF <sup><a href="#fn:71">71</a></sup></p></td><td><p>ECCV 2020</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>UPC <sup><a href="#fn:97">97</a></sup></p></td><td><p>CVPR 2020</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>AdvCam <sup><a href="#fn:67">67</a></sup></p></td><td><p>CVPR 2020</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>LG-GAN <sup><a href="#fn:308">308</a></sup></p></td><td><p>CVPR 2020</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Xu <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:267">267</a></sup></p></td><td><p>CVPR 2020</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td></tr><tr><td><p>PhysGAN <sup><a href="#fn:115">115</a></sup></p></td><td><p>CVPR 2020</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Li <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:124">124</a></sup></p></td><td><p>CVPR 2020</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td></tr><tr><td><p>GreedyFool <sup><a href="#fn:145">145</a></sup></p></td><td><p>NeurIPS 2020</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Xu <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:268">268</a></sup></p></td><td><p>MM 2020</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td></tr><tr><td><p>MAG-GAN <sup><a href="#fn:34">34</a></sup></p></td><td><p>Information Sciences 2020</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>GUAP <sup><a href="#fn:295">295</a></sup></p></td><td><p>ICDM 2020</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Wong <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:245">245</a></sup></p></td><td><p>ICLR 2021</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>AdvHat <sup><a href="#fn:113">113</a></sup></p></td><td><p>ICPR 2021</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Sayles <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:198">198</a></sup></p></td><td><p>CVPR 2021</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>TTP <sup><a href="#fn:168">168</a></sup></p></td><td><p>ICCV 2021</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td></tr><tr><td><p>CMML <sup><a href="#fn:75">75</a></sup></p></td><td><p>ICCV 2021</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>Zhao <math><semantics><mrow><mrow><mi>e</mi> <mo>⁢</mo> <mi>t</mi> <mo>⁢</mo> <mi>a</mi> <mo>⁢</mo> <mi>l</mi></mrow><mo>.</mo></mrow><annotation-xml><apply><ci>𝑒</ci> <ci>𝑡</ci> <ci>𝑎</ci> <ci>𝑙</ci></apply></annotation-xml> <annotation>et~{}al.</annotation><annotation>italic_e italic_t italic_a italic_l.</annotation></semantics></math><sup><a href="#fn:304">304</a></sup></p></td><td><p>NeurIPS 2021</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td></tr><tr><td><p>SLAP <sup><a href="#fn:155">155</a></sup></p></td><td><p>USENIX Security 2021</p></td><td><p>●</p></td><td><p>○</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr><tr><td><p>AP-GAN <sup><a href="#fn:298">298</a></sup></p></td><td><p>Geoinformatica 2022</p></td><td><p>○</p></td><td><p>●</p></td><td><p>●</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td><td><p>○</p></td></tr></tbody></table>

TABLE X: Categorization of existing black-box and transfer-based adversarial examples. For any classification criterion “A/B”, ○ denotes the former “A”, ● denotes the latter “B”.

|  |  | Black-box adversarial examples | Transfer-based adversarial examples |
| --- | --- | --- | --- |
| Method | Venue | Decison / Score-based | Example / Model-level |
| Brendel $et~{}al.$ [^19] | ICLR 2018 | ○ |  |
| Ilyas $et~{}al.$ [^100] | ICML 2018 | ○ |  |
| NES [^100] | ICML 2018 | ● |  |
| GAP [^184] | CVPR 2018 |  | ○ |
| MI-FGSM [^60] | CVPR 2018 |  | ● |
| OPT [^43] | ICLR 2019 | ○ |  |
| Sign-OPT [^44] | NeurIPS 2019 | ○ |  |
| Subspace attack [^91] | NeurIPS 2019 | ● |  |
| Naseer $et~{}al.$ [^169] | NeurIPS 2019 | ○ | ○ |
| qFool [^150] | ICCV 2019 | ○ |  |
| ILAP [^98] | ICCV 2019 | ○ | ● |
| SimBA [^89] | ICML 2019 | ● |  |
| ECO [^161] | ICML 2019 | ● |  |
| NAttack [^133] | ICML 2019 | ● |  |
| Bandit [^101] | ICLR 2019 | ● |  |
| ZO-signSGD [^146] | ICLR 2019 | ● |  |
| SignHunter [^6] | ICLR 2019 | ● |  |
| Dong $et~{}al.$ [^62] | CVPR 2019 | ○ |  |
| DI ${}^{2}$ -FGSM [^261] | CVPR 2019 | ○ | ● |
| GeoDA [^191] | CVPR 2020 | ○ |  |
| QEBA [^120] | CVPR 2020 | ○ |  |
| TREMBA [^99] | ICLR 2020 | ● |  |
| Meta Attack [^64] | ICLR 2020 | ○ | ○ |
| FDA [^102] | ICLR 2020 | ○ | ● |
| SGM [^251] | ICLR 2020 | ○ | ● |
| AdvFlow [^160] | NeurIPS 2020 | ● | ○ |
| LinBP [^90] | NeurIPS 2020 | ○ | ● |
| LeBA [^275] | NeurIPS 2020 | ● |  |
| Inkawhich $et~{}al.$ [^103] | NeurIPS 2020 | ○ | ● |
| Suya $et~{}al.$ [^218] | USENIX Security 2020 | ● |  |
| Square attack [^7] | ECCV 2020 | ● |  |
| SFA [^40] | ECCV 2020 | ○ |  |
| RayS [^32] | ICDM 2020 | ○ |  |
| HopSkipJumpAttack [^33] | AAAI 2021 | ○ |  |
| EMI-FGSM [^235] | BMVC 2021 | ○ | ● |
| PI-FSGM [^235] | BMCV 2021 | ○ | ● |
| IR [^236] | ICLR 2021 | ○ | ● |
| PRFA [^139] | ICCV 2021 | ● |  |
| MGAA [^285] | ICCV 2021 | ○ | ● |
| Naseer $et~{}al.$ [^168] | ICCV 2021 | ○ | ○ |
| Simulator attack [^157] | CVPR 2021 | ● |  |
| VMI-FGSM [^232] | CVPR 2021 | ○ | ● |
| MSA [^278] | NeurIPS 2021 | ● |  |
| P-RGF [^59] | IEEE TPAMI 2021 | ● |  |
| CG-Attack [^77] | CVPR 2022 | ● |  |
| SVRE-MI-FGSM [^263] | CVPR 2022 | ○ | ● |
| CISA [^206] | IEEE TPAMI 2022 | ○ |  |
| MCG [^279] | IEEE TPAMI 2022 | ● | ○ |

[^1]: Yossi Adi, Carsten Baum, Moustapha Cisse, Benny Pinkas, and Joseph Keshet. Turning your weakness into a strength: Watermarking deep neural networks by backdooring. In USENIX, pages 1615–1631, 2018.

[^2]: Akshay Agarwal, Richa Singh, Mayank Vatsa, and Nalini Ratha. Are image-agnostic universal adversarial perturbations for face recognition difficult to detect? In BTAS. IEEE, 2018.

[^3]: Michel Agoyan, Jean-Max Dutertre, Amir-Pasha Mirbaha, David Naccache, Anne-Lise Ribotta, and Assia Tria. How to flip a bit? In IOLTS, 2010.

[^4]: Nasir Ahmed, T\_ Natarajan, and Kamisetty R Rao. Discrete cosine transform. IEEE Transactions on Computers, 100(1):90–93, 1974.

[^5]: Naveed Akhtar and Ajmal Mian. Threat of adversarial attacks on deep learning in computer vision: A survey. IEEE Access, 6:14410–14430, 2018.

[^6]: Abdullah Al-Dujaili and Una-May O’Reilly. Sign bits are all you need for black-box attacks. In ICLR, 2019.

[^7]: Maksym Andriushchenko, Francesco Croce, Nicolas Flammarion, and Matthias Hein. Square attack: a query-efficient black-box adversarial attack via random search. In ECCV, 2020.

[^8]: Donovan Artz. Digital steganography: hiding data within data. IEEE Internet Computing, 5(3):75–80, 2001.

[^9]: Anish Athalye, Logan Engstrom, Andrew Ilyas, and Kevin Kwok. Synthesizing robust adversarial examples. In ICML, 2018.

[^10]: Eugene Bagdasaryan, Andreas Veit, Yiqing Hua, Deborah Estrin, and Vitaly Shmatikov. How to backdoor federated learning. In AISTATS, 2020.

[^11]: Jiawang Bai, Baoyuan Wu, Zhifeng Li, and Shu-tao Xia. Versatile weight attack via flipping limited bits. arXiv preprint arXiv:2207.12405, 2022.

[^12]: Jiawang Bai, Baoyuan Wu, Yong Zhang, Yiming Li, Zhifeng Li, and Shu-Tao Xia. Targeted attack against deep neural networks via flipping limited weight bits. In ICLR, 2021.

[^13]: Shumeet Baluja. Hiding images in plain sight: Deep steganography. In NeurIPS, 2017.

[^14]: Mauro Barni, Kassem Kallas, and Benedetta Tondi. A new backdoor attack in cnns by training set corruption without label poisoning. In ICIP, 2019.

[^15]: Arjun Nitin Bhagoji, Supriyo Chakraborty, Prateek Mittal, and Seraphin Calo. Analyzing federated learning through an adversarial lens. In ICML, 2019.

[^16]: Christopher M Bishop and Nasser M Nasrabadi. Pattern Recognition and Machine Learning. Springer, 2006.

[^17]: Mikel Bober-Irizar, Ilia Shumailov, Yiren Zhao, Robert Mullins, and Nicolas Papernot. Architectural backdoors in neural networks. In CVPR, 2023.

[^18]: Stephen Boyd, Neal Parikh, Eric Chu, Borja Peleato, Jonathan Eckstein, et al. Distributed optimization and statistical learning via the alternating direction method of multipliers. Foundations and Trends in Machine learning, 3(1):1–122, 2011.

[^19]: Wieland Brendel, Jonas Rauber, and Matthias Bethge. Decision-based adversarial attacks: Reliable attacks against black-box machine learning models. In ICLR, 2018.

[^20]: Junyoung Byun, Seungju Cho, Myung-Joon Kwon, Hee-Seon Kim, and Changick Kim. Improving the transferability of targeted adversarial examples through object-based diverse input. In CVPR, 2022.

[^21]: Xiangrui Cai, Sihan Xu, Ying Zhang, and Xiaojie Yuan. Badprompt: backdoor attacks on continuous prompts. In NeurIPS, 2022.

[^22]: Zikui Cai, Chengyu Song, Srikanth Krishnamurthy, Amit Roy-Chowdhury, and M Salman Asif. Black-box attacks via surrogate ensemble search. In NeurIPS, 2022.

[^23]: Nicholas Carlini and David Wagner. Towards evaluating the robustness of neural networks. In IEEE S&P, 2017.

[^24]: Nicholas Carlini and David Wagner. Audio adversarial examples: Targeted attacks on speech-to-text. In IEEE S&P Workshops, 2018.

[^25]: Uday K Chakraborty. Advances in differential evolution, volume 143. Springer, 2008.

[^26]: Alvin Chan, Yi Tay, Yew-Soon Ong, and Aston Zhang. Poison attacks against text datasets with conditional adversarially regularized autoencoder. In Findings of EMNLP, 2020.

[^27]: Chin-Chen Chang, Ju-Yuan Hsiao, and Chi-Shiang Chan. Finding optimal least-significant-bit substitution in image hiding by dynamic programming strategy. Pattern Recognition, 36(7):1583–1595, 2003.

[^28]: Nandish Chattopadhyay and Anupam Chattopadhyay. Rowback: Robust watermarking for neural networks using backdoors. In ICMLA, 2021.

[^29]: Chien-Lun Chen, Leana Golubchik, and Marco Paolieri. Backdoor attacks on federated meta-learning. In NeurIPS, 2020.

[^30]: Huili Chen, Cheng Fu, Jishen Zhao, and Farinaz Koushanfar. Proflip: Targeted trojan attack with progressive bit flips. In ICCV, 2021.

[^31]: Hongge Chen, Huan Zhang, Pin-Yu Chen, Jinfeng Yi, and Cho-Jui Hsieh. Attacking visual language grounding with adversarial examples: A case study on neural image captioning. In ACL, 2018.

[^32]: Jinghui Chen and Quanquan Gu. Rays: A ray searching method for hard-label adversarial attack. In ACM SIGKDD, 2020.

[^33]: Jianbo Chen, Michael I Jordan, and Martin J Wainwright. Hopskipjumpattack: A query-efficient decision-based attack. In IEEE S&P, pages 1277–1294. IEEE, 2020.

[^34]: Jinyin Chen, Haibin Zheng, Hui Xiong, Shijing Shen, and Mengmeng Su. Mag-gan: Massive attack generator via gan. Information Sciences, 536:67–90, 2020.

[^35]: Simin Chen, Hanlin Chen, Mirazul Haque, Cong Liu, and Wei Yang. The dark side of dynamic routing neural networks: Towards efficiency backdoor injection. In CVPR, 2023.

[^36]: Sizhe Chen, Zhehao Huang, Qinghua Tao, Yingwen Wu, Cihang Xie, and Xiaolin Huang. Adversarial attack on attackers: Post-process to mitigate black-box score-based query attacks. In NeurIPS, 2022.

[^37]: Shang-Tse Chen, Cory Cornelius, Jason Martin, and Duen Horng Polo Chau. Shapeshifter: Robust physical adversarial attack on faster r-cnn object detector. In ECML PKDD, 2018.

[^38]: Weixin Chen, Dawn Song, and Bo Li. Trojdiff: Trojan attacks on diffusion models with diverse targets. In CVPR, 2023.

[^39]: Weixin Chen, Baoyuan Wu, and Haoqian Wang. Effective backdoor defense by exploiting sensitivity of poisoned samples. In NeurIPS, 2022.

[^40]: Weilun Chen, Zhaoxiang Zhang, Xiaolin Hu, and Baoyuan Wu. Boosting decision-based black-box adversarial attacks with random sign flip. In ECCV, 2020.

[^41]: Xinyun Chen, Chang Liu, Bo Li, Kimberly Lu, and Dawn Song. Targeted backdoor attacks on deep learning systems using data poisoning. arXiv preprint arXiv:1712.05526, 2017.

[^42]: Xiaoyi Chen, Ahmed Salem, Dingfan Chen, Michael Backes, Shiqing Ma, Qingni Shen, Zhonghai Wu, and Yang Zhang. Badnl: Backdoor attacks against nlp models with semantic-preserving improvements. In ACSAC, 2021.

[^43]: Minhao Cheng, Thong Le, Pin-Yu Chen, Huan Zhang, Jinfeng Yi, and Cho-Jui Hsieh. Query-efficient hard-label black-box attack: An optimization-based approach. In ICLR, 2019.

[^44]: Shuyu Cheng, Yinpeng Dong, Tianyu Pang, Hang Su, and Jun Zhu. Improving black-box adversarial attacks with a transfer-based prior. In NeurIPS, 2019.

[^45]: Siyuan Cheng, Yingqi Liu, Shiqing Ma, and Xiangyu Zhang. Deep feature space trojan attack of neural networks by controlled detoxification. In AAAI, 2021.

[^46]: Sheng-Yen Chou, Pin-Yu Chen, and Tsung-Yi Ho. How to backdoor diffusion models? In CVPR, 2023.

[^47]: Sheng-Yen Chou, Pin-Yu Chen, and Tsung-Yi Ho. Villandiffusion: A unified backdoor attack framework for diffusion models. In NeurIPS, 2023.

[^48]: Francesco Croce, Maksym Andriushchenko, Vikash Sehwag, Edoardo Debenedetti, Nicolas Flammarion, Mung Chiang, Prateek Mittal, and Matthias Hein. Robustbench: a standardized adversarial robustness benchmark. In NeurIPS Datasets and Benchmarks Track, 2021.

[^49]: Francesco Croce and Matthias Hein. Sparse and imperceivable adversarial attacks. In ICCV, 2019.

[^50]: Francesco Croce and Matthias Hein. Reliable evaluation of adversarial robustness with an ensemble of diverse parameter-free attacks. In ICML, 2020.

[^51]: Francesco Croce and Matthias Hein. Reliable evaluation of adversarial robustness with an ensemble of diverse parameter-free attacks. In ICML, 2020.

[^52]: Ganqu Cui, Lifan Yuan, Bingxiang He, Yangyi Chen, Zhiyuan Liu, and Maosong Sun. A unified evaluation of textual backdoor learning: Frameworks and benchmarks. In NeurIPS Datasets and Benchmarks Track, 2022.

[^53]: Debayan Deb, Jianbang Zhang, and Anil K Jain. Advfaces: Adversarial face synthesis. In IJCB. IEEE, 2019.

[^54]: Gavin Weiguang Ding, Luyu Wang, and Xiaomeng Jin. AdverTorch v0.1: An adversarial robustness toolbox based on pytorch. arXiv preprint arXiv:1902.07623, 2019.

[^55]: Xiaofeng Ding, Hongbiao Fang, Zhilin Zhang, Kim-Kwang Raymond Choo, and Hai Jin. Privacy-preserving feature extraction via adversarial training. IEEE Transactions on Knowledge and Data Engineering, 34(4):1967–1979, 2020.

[^56]: Khoa Doan, Yingjie Lao, and Ping Li. Backdoor attack with imperceptible input and latent modification. In NeurIPS, 2021.

[^57]: Khoa Doan, Yingjie Lao, Weijie Zhao, and Ping Li. Lira: Learnable, imperceptible and robust backdoor attacks. In ICCV, 2021.

[^58]: Khoa D Doan, Yingjie Lao, and Ping Li. Marksman backdoor: Backdoor attacks with arbitrary target class. In NeurIPS, 2022.

[^59]: Yinpeng Dong, Shuyu Cheng, Tianyu Pang, Hang Su, and Jun Zhu. Query-efficient black-box adversarial attacks guided by a transfer-based prior. TPAMI, 44(12):9536–9548, 2022.

[^60]: Yinpeng Dong, Fangzhou Liao, Tianyu Pang, Hang Su, Jun Zhu, Xiaolin Hu, and Jianguo Li. Boosting adversarial attacks with momentum. In CVPR, 2018.

[^61]: Yinpeng Dong, Tianyu Pang, Hang Su, and Jun Zhu. Evading defenses to transferable adversarial examples by translation-invariant attacks. In CVPR, 2019.

[^62]: Yinpeng Dong, Hang Su, Baoyuan Wu, Zhifeng Li, Wei Liu, Tong Zhang, and Jun Zhu. Efficient decision-based black-box adversarial attacks on face recognition. In CVPR, 2019.

[^63]: John R Douceur. The sybil attack. In International workshop on peer-to-peer systems. Springer, 2002.

[^64]: Jiawei Du, Hu Zhang, Joey Tianyi Zhou, Yi Yang, and Jiashi Feng. Query-efficient meta attack to deep neural networks. In ICLR, 2020.

[^65]: Wei Du, Yichun Zhao, Boqun Li, Gongshen Liu, and Shilin Wang. Ppt: Backdoor attacks on pre-trained models via poisoned prompt tuning. In IJCAI, 2022.

[^66]: Wei Du, Yichun Zhao, Boqun Li, Gongshen Liu, and Shilin Wang. Ppt: Backdoor attacks on pre-trained models via poisoned prompt tuning. In IJCAI, 2022.

[^67]: Ranjie Duan, Xingjun Ma, Yisen Wang, James Bailey, A Kai Qin, and Yun Yang. Adversarial camouflage: Hiding physical-world attacks with natural styles. In CVPR, 2020.

[^68]: Logan Engstrom, Brandon Tran, Dimitris Tsipras, Ludwig Schmidt, and Aleksander Madry. Exploring the landscape of spatial robustness. In ICML, 2019.

[^69]: Kevin Eykholt, Ivan Evtimov, Earlence Fernandes, Bo Li, Amir Rahmati, Florian Tramèr, Atul Prakash, Tadayoshi Kohno, and Dawn Song. Physical adversarial examples for object detectors. In USENIX Conference on Offensive Technologies, 2018.

[^70]: Kevin Eykholt, Ivan Evtimov, Earlence Fernandes, Bo Li, Amir Rahmati, Chaowei Xiao, Atul Prakash, Tadayoshi Kohno, and Dawn Song. Robust physical-world attacks on deep learning visual classification. In CVPR, 2018.

[^71]: Yanbo Fan, Baoyuan Wu, Tuanhui Li, Yong Zhang, Mingyang Li, Zhifeng Li, and Yujiu Yang. Sparse adversarial attack via perturbation factorization. In ECCV, 2020.

[^72]: Alhussein Fawzi and Pascal Frossard. Manitest: Are classifiers really invariant? In BMVC, 2015.

[^73]: Uriel Feige, Vahab S Mirrokni, and Jan Vondrák. Maximizing non-monotone submodular functions. SIAM Journal on Computing, 40(4):1133–1153, 2011.

[^74]: Le Feng, Sheng Li, Zhenxing Qian, and Xinpeng Zhang. Stealthy backdoor attack with adversarial training. In ICASSP, 2022.

[^75]: Weiwei Feng, Baoyuan Wu, Tianzhu Zhang, Yong Zhang, and Yongdong Zhang. Meta-attack: Class-agnostic and model-agnostic physical adversarial attack. In ICCV, 2021.

[^76]: Yu Feng, Benteng Ma, Jing Zhang, Shanshan Zhao, Yong Xia, and Dacheng Tao. Fiba: Frequency-injection based backdoor attack in medical image analysis. In CVPR, 2022.

[^77]: Yan Feng, Baoyuan Wu, Yanbo Fan, Li Liu, Zhifeng Li, and Shutao Xia. Boosting black-box attack with partially transferred conditional adversarial distribution. In CVPR, 2022.

[^78]: Clement Fung, Chris JM Yoon, and Ivan Beschastnikh. The limitations of federated learning in sybil settings. In 23rd International Symposium on Research in Attacks, Intrusions and Defenses, 2020.

[^79]: Kuofeng Gao, Jiawang Bai, Baoyuan Wu, Mengxi Ya, and Shu-Tao Xia. Imperceptible and robust backdoor attack in 3d point cloud. arXiv preprint arXiv:2208.08052, 2022.

[^80]: Yansong Gao, Bao Gia Doan, Zhi Zhang, Siqi Ma, Jiliang Zhang, Anmin Fu, Surya Nepal, and Hyoungshick Kim. Backdoor attacks and countermeasures on deep learning: A comprehensive review. arXiv preprint arXiv:2007.10760, 2020.

[^81]: Siddhant Garg, Adarsh Kumar, Vibhor Goel, and Yingyu Liang. Can adversarial weight perturbations inject neural backdoors. In ACM CIKM, 2020.

[^82]: Leon A Gatys, Alexander S Ecker, and Matthias Bethge. Image style transfer using convolutional neural networks. In CVPR, pages 2414–2423, 2016.

[^83]: Behnam Ghavami, Seyd Movi, Zhenman Fang, and Lesley Shannon. Stealthy attack on algorithmic-protected dnns via smart bit flipping. In ISQED, 2022.

[^84]: Xueluan Gong, Yanjiao Chen, Qian Wang, Huayang Huang, Lingshuo Meng, Chao Shen, and Qian Zhang. Defense-resistant backdoor attacks against deep neural networks in outsourced cloud environment. IEEE Journal on Selected Areas in Communications, 2021.

[^85]: Ian Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair, Aaron Courville, and Yoshua Bengio. Generative adversarial nets. In NIPS, 2014.

[^86]: Ian Goodfellow, Jonathon Shlens, and Christian Szegedy. Explaining and harnessing adversarial examples. In ICLR, 2015.

[^87]: Dou Goodman, Hao Xin, Wang Yang, Wu Yuesheng, Xiong Junfeng, and Zhang Huan. Advbox: a toolbox to generate adversarial examples that fool neural networks, 2020.

[^88]: Tianyu Gu, Kang Liu, Brendan Dolan-Gavitt, and Siddharth Garg. Badnets: Evaluating backdooring attacks on deep neural networks. IEEE Access, 7:47230–47244, 2019.

[^89]: Chuan Guo, Jacob Gardner, Yurong You, Andrew Gordon Wilson, and Kilian Weinberger. Simple black-box adversarial attacks. In ICML, 2019.

[^90]: Yiwen Guo, Qizhang Li, and Hao Chen. Backpropagating linearly improves transferability of adversarial examples. In NeurIPS, 2020.

[^91]: Yiwen Guo, Ziang Yan, and Changshui Zhang. Subspace attack: Exploiting promising subspaces for query-efficient black-box attacks. In NeurIPS, 2019.

[^92]: Xingshuo Han, Guowen Xu, Yuan Zhou, Xuehuan Yang, Jiwei Li, and Tianwei Zhang. Physical backdoor attacks to lane detection systems in autonomous driving. In ACM Multimedia, 2022.

[^93]: Jonathan Hayase and Sewoong Oh. Few-shot backdoor attacks via neural tangent kernels. In ICLR, 2022.

[^94]: Sanghyun Hong, Nicholas Carlini, and Alexey Kurakin. Handcrafted backdoors in deep neural networks. In NeurIPS, 2022.

[^95]: Hongsheng Hu, Zoran Salcic, Gillian Dobbie, Jinjun Chen, Lichao Sun, and Xuyun Zhang. Membership inference via backdooring. arXiv preprint arXiv:2206.04823, 2022.

[^96]: Kunzhe Huang, Yiming Li, Baoyuan Wu, Zhan Qin, and Kui Ren. Backdoor defense via decoupling the training process. In ICLR, 2022.

[^97]: Lifeng Huang, Chengying Gao, Yuyin Zhou, Cihang Xie, Alan L Yuille, Changqing Zou, and Ning Liu. Universal physical camouflage attacks on object detectors. In CVPR, 2020.

[^98]: Qian Huang, Isay Katsman, Horace He, Zeqi Gu, Serge Belongie, and Ser-Nam Lim. Enhancing adversarial example transferability with an intermediate level attack. In ICCV, 2019.

[^99]: Zhichao Huang and Tong Zhang. Black-box adversarial attack with transferable model-based embedding. In ICLR, 2020.

[^100]: Andrew Ilyas, Logan Engstrom, Anish Athalye, and Jessy Lin. Black-box adversarial attacks with limited queries and information. In ICML, 2018.

[^101]: Andrew Ilyas, Logan Engstrom, and Aleksander Madry. Prior convictions: Black-box adversarial attacks with bandits and priors. In ICLR, 2019.

[^102]: Nathan Inkawhich, Kevin Liang, Lawrence Carin, and Yiran Chen. Transferable perturbations of deep feature distributions. In ICLR, 2020.

[^103]: Nathan Inkawhich, Kevin Liang, Binghui Wang, Matthew Inkawhich, Lawrence Carin, and Yiran Chen. Perturbing across the feature hierarchy to improve standard and strict blackbox attack transferability. In NeurIPS, 2020.

[^104]: Steve TK Jan, Joseph Messou, Yen-Chen Lin, Jia-Bin Huang, and Gang Wang. Connecting the digital and physical world: Improving the robustness of adversarial attacks. In AAAI, volume 33, 2019.

[^105]: Rishi Dev Jha, Jonathan Hayase, and Sewoong Oh. Label poisoning is all you need. In NeurIPS, 2023.

[^106]: Xiaojun Jia, Yong Zhang, Baoyuan Wu, Ke Ma, Jue Wang, and Xiaochun Cao. Las-at: Adversarial training with learnable attack strategy. In CVPR, 2022.

[^107]: Wenbo Jiang, Hongwei Li, Guowen Xu, and Tianwei Zhang. Color backdoor: A robust poisoning attack in color space. In CVPR, 2023.

[^108]: Seong Joon Oh, Mario Fritz, and Bernt Schiele. Adversarial image perturbation for privacy protection–a game theory perspective. In Proceedings of the IEEE International Conference on Computer Vision, pages 1482–1491, 2017.

[^109]: Can Kanbak, Seyed-Mohsen Moosavi-Dezfooli, and Pascal Frossard. Geometric robustness of deep networks: analysis and improvement. In CVPR, 2018.

[^110]: Danny Karmon, Daniel Zoran, and Yoav Goldberg. Lavan: Localized and visible adversarial noise. In ICML, 2018.

[^111]: Jacob Devlin Ming-Wei Chang Kenton and Lee Kristina Toutanova. Bert: Pre-training of deep bidirectional transformers for language understanding. In Proceedings of NAACL-HLT, 2019.

[^112]: Yoongu Kim, Ross Daly, Jeremie Kim, Chris Fallin, Ji Hye Lee, Donghyuk Lee, Chris Wilkerson, Konrad Lai, and Onur Mutlu. Flipping bits in memory without accessing them: An experimental study of dram disturbance errors. ACM SIGARCH Computer Architecture News, 42(3):361–372, 2014.

[^113]: Stepan Komkov and Aleksandr Petiushko. Advhat: Real-world adversarial attack on arcface face id system. In ICPR, 2021.

[^114]: Jakub Konečnỳ, H Brendan McMahan, Felix X Yu, Peter Richtárik, Ananda Theertha Suresh, and Dave Bacon. Federated learning: Strategies for improving communication efficiency. In NIPS Workshop on Private Multi-Party Machine Learning, 2016.

[^115]: Zelun Kong, Junfeng Guo, Ang Li, and Cong Liu. Physgan: Generating physical-world-resilient adversarial examples for autonomous driving. In CVPR, 2020.

[^116]: Alexey Kurakin, Ian Goodfellow, and Samy Bengio. Adversarial examples in the physical world. In Artificial intelligence safety and security, pages 99–112. Chapman and Hall/CRC, 2018.

[^117]: Cassidy Laidlaw and Soheil Feizi. Functional adversarial attacks. In NeurIPS, 2019.

[^118]: Debang Li, Junge Zhang, and Kaiqi Huang. Universal adversarial perturbations against object detection. Pattern Recognition, 110:107584, 2021.

[^119]: Haoliang Li, Yufei Wang, Xiaofei Xie, Yang Liu, Shiqi Wang, Renjie Wan, Lap-Pui Chau, and Alex C. Kot. Light can hack your face! black-box backdoor attack on face recognition systems. arXiv preprint arXiv:2009.06996, 2020.

[^120]: Huichen Li, Xiaojun Xu, Xiaolu Zhang, Shuang Yang, and Bo Li. Qeba: Query-efficient boundary-based blackbox attack. In CVPR, 2020.

[^121]: Jie Li, Rongrong Ji, Hong Liu, Xiaopeng Hong, Yue Gao, and Qi Tian. Universal perturbation attack against image retrieval. In ICCV, 2019.

[^122]: Jie Li, Rongrong Ji, Hong Liu, Jianzhuang Liu, Bineng Zhong, Cheng Deng, and Qi Tian. Projection & probability-driven black-box attack. In CVPR, 2020.

[^123]: Linyang Li, Demin Song, Xiaonan Li, Jiehang Zeng, Ruotian Ma, and Xipeng Qiu. Backdoor attacks on pre-trained models by layerwise weight poisoning. In EMNLP, 2021.

[^124]: Maosen Li, Cheng Deng, Tengjiao Li, Junchi Yan, Xinbo Gao, and Heng Huang. Towards transferable targeted attack. In CVPR, 2020.

[^125]: Shaofeng Li, Hui Liu, Tian Dong, Benjamin Zi Hao Zhao, Minhui Xue, Haojin Zhu, and Jialiang Lu. Hidden backdoors in human-centric language models. In ACM CCS, 2021.

[^126]: Shaofeng Li, Minhui Xue, Benjamin Zhao, Haojin Zhu, and Xinpeng Zhang. Invisible backdoor attacks on deep neural networks via steganography and regularization. TDSC, 2021.

[^127]: Tuanhui Li, Baoyuan Wu, Yujiu Yang, Yanbo Fan, Yong Zhang, and Wei Liu. Compressing convolutional neural networks via factorized convolutional filters. In CVPR, 2019.

[^128]: Xiaoting Li, Lingwei Chen, and Dinghao Wu. Turning attacks into protection: Social media privacy protection using adversarial attacks. In Proceedings of the 2021 SIAM International Conference on Data Mining (SDM), pages 208–216. SIAM, 2021.

[^129]: Xinke Li, Zhirui Chen, Yue Zhao, Zekun Tong, Yabang Zhao, Andrew Lim, and Joey Tianyi Zhou. Pointba: Towards backdoor attacks in 3d point cloud. In ICCV, 2021.

[^130]: Yingwei Li, Song Bai, Yuyin Zhou, Cihang Xie, Zhishuai Zhang, and Alan Yuille. Learning transferable adversarial examples via ghost networks. In AAAI, 2020.

[^131]: Yiming Li, Yang Bai, Yong Jiang, Yong Yang, Shu-Tao Xia, and Bo Li. Untargeted backdoor watermark: Towards harmless and stealthy dataset copyright protection. NeurIPS, 2022.

[^132]: Yaxin Li, Wei Jin, Han Xu, and Jiliang Tang. Deeprobust: A pytorch library for adversarial attacks and defenses. arXiv preprint arXiv:2005.06149, 2020.

[^133]: Yandong Li, Lijun Li, Liqiang Wang, Tong Zhang, and Boqing Gong. Nattack: Learning the distributions of adversarial examples for an improved black-box attack on deep neural networks. In ICML, 2019.

[^134]: Yuezun Li, Yiming Li, Baoyuan Wu, Longkang Li, Ran He, and Siwei Lyu. Invisible backdoor attack with sample-specific triggers. In ICCV, 2021.

[^135]: Yiming Li, Ziqi Zhang, Jiawang Bai, Baoyuan Wu, Yong Jiang, and Shu-Tao Xia. Open-sourced dataset protection via backdoor watermarking. In NeurIPS Workshop on Dataset Curation and Security, 2020.

[^136]: Yiming Li, Mingyan Zhu, Xue Yang, Yong Jiang, Tao Wei, and Shu-Tao Xia. Black-box dataset ownership verification via backdoor watermarking. IEEE TIFS, 2023.

[^137]: Ziqiang Li, Hong Sun, Pengfei Xia, Beihao Xia, Xue Rui, Wei Zhang, and Bin Li. A proxy-free strategy for practically improving the poisoning efficiency in backdoor attacks. arXiv preprint arXiv:2306.08313, 2023.

[^138]: Ziqiang Li, Pengfei Xia, Hong Sun, Yueqi Zeng, Wei Zhang, and Bin Li. Explore the effect of data selection on poison efficiency in backdoor attacks. arXiv preprint arXiv:2310.09744, 2023.

[^139]: Siyuan Liang, Baoyuan Wu, Yanbo Fan, Xingxing Wei, and Xiaochun Cao. Parallel rectangle flip attack: A query-based black-box attack against object detection. In ICCV, 2021.

[^140]: Jiadong Lin, Chuanbiao Song, Kun He, Liwei Wang, and John E. Hopcroft. Nesterov accelerated gradient and scale invariance for adversarial attacks. In ICLR, 2020.

[^141]: Junyu Lin, Lei Xu, Yingqi Liu, and Xiangyu Zhang. Composite backdoor attack for deep neural network by mixing existing benign features. In ACM CCS, pages 113–131, 2020.

[^142]: Xiang Ling, Shouling Ji, Jiaxu Zou, Jiannan Wang, Chunming Wu, Bo Li, and Ting Wang. Deepsec: A uniform platform for security analysis of deep learning model. In 2019 IEEE Symposium on Security and Privacy (SP), pages 673–690. IEEE, 2019.

[^143]: Aishan Liu, Xianglong Liu, Jiaxin Fan, Yuqing Ma, Anlan Zhang, Huiyuan Xie, and Dacheng Tao. Perceptual-sensitive gan for generating adversarial patches. In AAAI, 2019.

[^144]: Hong Liu, Rongrong Ji, Jie Li, Baochang Zhang, Yue Gao, Yongjian Wu, and Feiyue Huang. Universal adversarial perturbation via prior driven uncertainty approximation. In ICCV, 2019.

[^145]: Hui Liu, Bo Zhao, Jiabao Guo, Yang An, and Peng Liu. Greedyfool: Distortion-aware sparse adversarial attack. In NeurIPS, 2020.

[^146]: Sijia Liu, Pin-Yu Chen, Xiangyi Chen, and Mingyi Hong. signsgd via zeroth-order oracle. In ICLR, 2019.

[^147]: Yi Liu, Gelei Deng, Yuekang Li, Kailong Wang, Tianwei Zhang, Yepang Liu, Haoyu Wang, Yan Zheng, and Yang Liu. Prompt injection attack against llm-integrated applications. arXiv preprint arXiv:2306.05499, 2023.

[^148]: Yingqi Liu, Shiqing Ma, Yousra Aafer, Wen-Chuan Lee, Juan Zhai, Weihang Wang, and Xiangyu Zhang. Trojaning attack on neural networks. In NDSS, 2018.

[^149]: Yunfei Liu, Xingjun Ma, James Bailey, and Feng Lu. Reflection backdoor: A natural backdoor attack on deep neural networks. In ECCV, 2020.

[^150]: Yujia Liu, Seyed-Mohsen Moosavi-Dezfooli, and Pascal Frossard. A geometry-inspired decision-based attack. In ICCV, 2019.

[^151]: Yannan Liu, Lingxiao Wei, Bo Luo, and Qiang Xu. Fault injection attack on deep neural network. In ICCAD, 2017.

[^152]: Yang Liu, Zhihao Yi, and Tianjian Chen. Backdoor attacks and defenses in feature-partitioned collaborative learning. arXiv preprint arXiv:2007.03608, 2020.

[^153]: Zechun Liu, Baoyuan Wu, Wenhan Luo, Xin Yang, Wei Liu, and Kwang-Ting Cheng. Bi-real net: Enhancing the performance of 1-bit cnns with improved representational capability and advanced training algorithm. In ECCV, 2018.

[^154]: Yuyang Long, Qilong Zhang, Boheng Zeng, Lianli Gao, Xianglong Liu, Jian Zhang, and Jingkuan Song. Frequency domain model augmentation for adversarial attack. In ECCV, 2022.

[^155]: Giulio Lovisotto, Henry Turner, Ivo Sluganovic, Martin Strohmeier, and Ivan Martinovic. Slap: improving physical adversarial examples with short-lived adversarial perturbations. In USENIX, pages 1865–1882, 2021.

[^156]: You Lu and Bert Huang. Structured output learning with conditional generative flows. In AAAI, 2020.

[^157]: Chen Ma, Li Chen, and Jun-Hai Yong. Simulating unknown target models for query-efficient black-box attacks. In CVPR, 2021.

[^158]: Aleksander Madry, Aleksandar Makelov, Ludwig Schmidt, Dimitris Tsipras, and Adrian Vladu. Towards deep learning models resistant to adversarial attacks. In ICLR, 2018.

[^159]: Apostolos Modas, Seyed-Mohsen Moosavi-Dezfooli, and Pascal Frossard. Sparsefool: A few pixels make a big difference. In CVPR, 2019.

[^160]: Hadi Mohaghegh Dolatabadi, Sarah Erfani, and Christopher Leckie. Advflow: inconspicuous black-box adversarial attacks using normalizing flows. In NeurIPS, 2020.

[^161]: Seungyong Moon, Gaon An, and Hyun Oh Song. Parsimonious black-box adversarial attacks via efficient combinatorial optimization. In ICML, 2019.

[^162]: Seyed-Mohsen Moosavi-Dezfooli, Alhussein Fawzi, Omar Fawzi, and Pascal Frossard. Universal adversarial perturbations. In CVPR, 2017.

[^163]: Seyed-Mohsen Moosavi-Dezfooli, Alhussein Fawzi, and Pascal Frossard. Deepfool: a simple and accurate method to fool deep neural networks. In CVPR, 2016.

[^164]: KR Mopuri, U Garg, and R Venkatesh Babu. Fast feature fool: A data independent approach to universal adversarial perturbations. In BMVC, 2017.

[^165]: Konda Reddy Mopuri, Aditya Ganeshan, and R Venkatesh Babu. Generalizable data-free objective for crafting universal adversarial perturbations. TPAMI, 41(10):2452–2465, 2018.

[^166]: John Morris, Eli Lifland, Jin Yong Yoo, Jake Grigsby, Di Jin, and Yanjun Qi. Textattack: A framework for adversarial attacks, data augmentation, and adversarial training in nlp. In EMNLP: System Demonstrations, 2020.

[^167]: Nina Narodytska and Shiva Prasad Kasiviswanathan. Simple black-box adversarial perturbations for deep networks. CVPR Workshops, 2017.

[^168]: Muzammal Naseer, Salman Khan, Munawar Hayat, Fahad Shahbaz Khan, and Fatih Porikli. On generating transferable targeted perturbations. In ICCV, 2021.

[^169]: Muhammad Muzammal Naseer, Salman H Khan, Muhammad Haris Khan, Fahad Shahbaz Khan, and Fatih Porikli. Cross-domain transferability of adversarial perturbations. In NeurIPS, 2019.

[^170]: Paarth Neekhara, Shehzeen Hussain, Prakhar Pandey, Shlomo Dubnov, Julian McAuley, and Farinaz Koushanfar. Universal adversarial perturbations for speech recognition systems. arXiv preprint arXiv:1905.03828, 2019.

[^171]: Yurii Nesterov and Vladimir Spokoiny. Random gradient-free minimization of convex functions. Foundations of Computational Mathematics, 17(2):527–566, 2017.

[^172]: Dung Thuy Nguyen, Tuan Minh Nguyen, Anh Tuan Tran, Khoa D Doan, and KOK SENG WONG. Iba: Towards irreversible backdoor attacks in federated learning. In NeurIPS, 2023.

[^173]: Tuan Anh Nguyen and Anh Tran. Input-aware dynamic backdoor attack. In NeurIPS, volume 33, 2020.

[^174]: Tuan Anh Nguyen and Anh Tuan Tran. Wanet - imperceptible warping-based backdoor attack. In ICLR, 2021.

[^175]: Maria-Irina Nicolae, Mathieu Sinn, Minh Ngoc Tran, Beat Buesser, Ambrish Rawat, Martin Wistuba, Valentina Zantedeschi, Nathalie Baracaldo, Bryant Chen, Heiko Ludwig, Ian M. Molloy, and Ben Edwards. Adversarial robustness toolbox v1.0.0, 2019.

[^176]: Rui Ning, Jiang Li, Chunsheng Xin, and Hongyi Wu. Invisible poison: A blackbox clean label backdoor attack to deep neural networks. In ICCC, 2021.

[^177]: Rui Ning, Jiang Li, Chunsheng Xin, Hongyi Wu, and Chonggang Wang. Hibernated backdoor: A mutual information empowered backdoor attack to deep neural networks. In AAAI, 2022.

[^178]: Ren Pang, Zheng Zhang, Xiangshan Gao, Zhaohan Xi, Shouling Ji, Peng Cheng, and Ting Wang. Trojanzoo: Towards unified, holistic, and practical evaluation of neural backdoors. In Euro S&P, 2022.

[^179]: Nicolas Papernot, Fartash Faghri, Nicholas Carlini, Ian Goodfellow, Reuben Feinman, Alexey Kurakin, Cihang Xie, Yash Sharma, Tom Brown, Aurko Roy, Alexander Matyasko, Vahid Behzadan, Karen Hambardzumyan, Zhishuai Zhang, Yi-Lin Juang, Zhi Li, Ryan Sheatsley, Abhibhav Garg, Jonathan Uesato, Willi Gierke, Yinpeng Dong, David Berthelot, Paul Hendricks, Jonas Rauber, and Rujun Long. Technical report on the cleverhans v2.1.0 adversarial examples library. arXiv preprint arXiv:1610.00768, 2018.

[^180]: Nicolas Papernot, Patrick McDaniel, Somesh Jha, Matt Fredrikson, Z Berkay Celik, and Ananthram Swami. The limitations of deep learning in adversarial settings. In EuroS&P, pages 372–387. IEEE, 2016.

[^181]: Fábio Perez and Ian Ribeiro. Ignore previous prompt: Attack techniques for language models. In NeurIPS workshop, 2022.

[^182]: Huy Phan, Cong Shi, Yi Xie, Tianfang Zhang, Zhuohang Li, Tianming Zhao, Jian Liu, Yan Wang, Yingying Chen, and Bo Yuan. Ribac: Towards r obust and i mperceptible b ackdoor a ttack against c ompact dnn. In ECCV, 2022.

[^183]: Huy Phan, Yi Xie, Jian Liu, Yingying Chen, and Bo Yuan. Invisible and efficient backdoor attacks for compressed deep neural networks. In ICASSP, 2022.

[^184]: Omid Poursaeed, Isay Katsman, Bicheng Gao, and Serge Belongie. Generative adversarial perturbations. In CVPR, 2018.

[^185]: Xiangyu Qi, Tinghao Xie, Yiming Li, Saeed Mahloujifar, and Prateek Mittal. Revisiting the assumption of latent separability for backdoor defenses. In ICLR, 2022.

[^186]: Xiangyu Qi, Tinghao Xie, Ruizhe Pan, Jifeng Zhu, Yong Yang, and Kai Bu. Towards practical deployment-stage backdoor attack on deep neural networks. In CVPR, 2022.

[^187]: Xiangyu Qi, Jifeng Zhu, Chulin Xie, and Yong Yang. Subnet replacement: Deployment-stage backdoor attack against deep neural networks in gray-box setting. In ICLR workshop, 2021.

[^188]: Yao Qin, Nicholas Carlini, Garrison Cottrell, Ian Goodfellow, and Colin Raffel. Imperceptible, robust, and targeted adversarial examples for automatic speech recognition. In ICML, 2019.

[^189]: Zeyu Qin, Yanbo Fan, Yi Liu, Li Shen, Yong Zhang, Jue Wang, and Baoyuan Wu. Boosting the transferability of adversarial attacks with reverse adversarial perturbation. In NeurIPS, 2022.

[^190]: Zeyu Qin, Yanbo Fan, Hongyuan Zha, and Baoyuan Wu. Random noise defense against query-based black-box attacks. In NeurIPS, 2021.

[^191]: Ali Rahmati, Seyed-Mohsen Moosavi-Dezfooli, Pascal Frossard, and Huaiyu Dai. Geoda: a geometric framework for black-box adversarial attacks. In CVPR, 2020.

[^192]: Adnan Siraj Rakin, Zhezhi He, and Deliang Fan. Tbt: targeted neural network attack with bit trojan. In CVPR, 2020.

[^193]: Adnan Siraj Rakin, Zhezhi He, Jingtao Li, Fan Yao, Chaitali Chakrabarti, and Deliang Fan. T-bfa: Targeted bit-flip adversarial weight attack. TPAMI, 44(11):7928–7939, 2022.

[^194]: Jonas Rauber, Wieland Brendel, and Matthias Bethge. Foolbox: A python toolbox to benchmark the robustness of machine learning models. In ICML Workshop, 2017.

[^195]: Aniruddha Saha, Akshayvarun Subramanya, and Hamed Pirsiavash. Hidden trigger backdoor attacks. In AAAI, 2020.

[^196]: Ahmed Salem, Rui Wen, Michael Backes, Shiqing Ma, and Yang Zhang. Dynamic backdoor attacks against machine learning models. In EuroS&P, 2022.

[^197]: Esha Sarkar, Hadjer Benkraouda, Gopika Krishnan, Homer Gamil, and Michail Maniatakos. Facehack: Attacking facial recognition systems using malicious facial characteristics. IEEE T-BIOM, 4:361–372, 2022.

[^198]: Athena Sayles, Ashish Hooda, Mohit Gupta, Rahul Chatterjee, and Earlence Fernandes. Invisible perturbations: Physical adversarial examples exploiting the rolling shutter effect. In CVPR, 2021.

[^199]: Lukas Schott, Jonas Rauber, Matthias Bethge, and Wieland Brendel. Towards the first adversarially robust neural network model on mnist. In ICLR, 2019.

[^200]: Ali Shafahi, W Ronny Huang, Mahyar Najibi, Octavian Suciu, Christoph Studer, Tudor Dumitras, and Tom Goldstein. Poison frogs! targeted clean-label poisoning attacks on neural networks. In NeurIPS, 2018.

[^201]: Mahmood Sharif, Sruti Bhagavatula, Lujo Bauer, and Michael K Reiter. Accessorize to a crime: Real and stealthy attacks on state-of-the-art face recognition. In ACM CCS, 2016.

[^202]: Mahmood Sharif, Sruti Bhagavatula, Lujo Bauer, and Michael K Reiter. A general framework for adversarial examples with objectives. TOPS, 22(3):1–30, 2019.

[^203]: Lujia Shen, Shouling Ji, Xuhong Zhang, Jinfeng Li, Jing Chen, Jie Shi, Chengfang Fang, Jianwei Yin, and Ting Wang. Backdoor pre-trained models can transfer to all. In ACM CCS, 2021.

[^204]: Haoyue Shi, Jiayuan Mao, Tete Xiao, Yuning Jiang, and Jian Sun. Learning visually-grounded semantics from contrastive adversarial samples. In COLING, pages 3715–3727, 2018.

[^205]: Jiawen Shi, Yixin Liu, Pan Zhou, and Lichao Sun. Badgpt: Exploring security vulnerabilities of chatgpt via backdoor attacks to instructgpt. arXiv preprint arXiv:2304.12298, 2023.

[^206]: Yucheng Shi, Yahong Han, Qinghua Hu, Yi Yang, and Qi Tian. Query-efficient black-box adversarial attack with customized iteration and sampling. TPAMI, 45(2):2226–2245, 2023.

[^207]: Yundi Shi, Piji Li, Changchun Yin, Zhaoyang Han, Lu Zhou, and Zhe Liu. Promptattack: Prompt-based attack for language models via gradient search. In NLPCC, 2022.

[^208]: Reza Shokri et al. Bypassing backdoor detection algorithms in deep learning. In EuroS&P, 2020.

[^209]: Ilia Shumailov, Zakhar Shumaylov, Dmitry Kazhdan, Yiren Zhao, Nicolas Papernot, Murat A Erdogdu, and Ross J Anderson. Manipulating sgd with data ordering attacks. In NeurIPS, 2021.

[^210]: Ryan Soklaski, Justin Goodwin, Olivia Brown, Michael Yee, and Jason Matterer. Tools and practices for responsible ai engineering. arXiv preprint arXiv:2201.05647, 2022.

[^211]: David Marco Sommer, Liwei Song, Sameer Wagh, and Prateek Mittal. Towards probabilistic verification of machine unlearning. arXiv preprint arXiv:2003.04247, 2020.

[^212]: Yang Song, Rui Shu, Nate Kushman, and Stefano Ermon. Constructing unrestricted adversarial examples with generative models. In NeurIPS, 2018.

[^213]: Hossein Souri, Liam Fowl, Rama Chellappa, Micah Goldblum, and Tom Goldstein. Sleeper agent: Scalable hidden trigger backdoors for neural networks trained from scratch. In NeurIPS, 2022.

[^214]: Jacob Springer, Melanie Mitchell, and Garrett Kenyon. A little robustness goes a long way: Leveraging robust features for targeted transfer attacks. In NeurIPS, 2021.

[^215]: Lukas Struppek, Dominik Hintersdorf, and Kristian Kersting. Rickrolling the artist: Injecting backdoors into text encoders for text-to-image synthesis. In ICCV, 2023.

[^216]: Jiawei Su, Danilo Vasconcellos Vargas, and Kouichi Sakurai. One pixel attack for fooling deep neural networks. TEC, 2019.

[^217]: Zhigang Su, Dawei Zhou, Nannan Wang, Decheng Liu, Zhen Wang, and Xinbo Gao. Hiding visual information via obfuscating adversarial perturbations. In ICCV, 2023.

[^218]: Fnu Suya, Jianfeng Chi, David Evans, and Yuan Tian. Hybrid batch attacks: Finding black-box adversarial examples with limited queries. In USENIX, 2020.

[^219]: Esteban G Tabak and Cristina V Turner. A family of nonparametric density estimation algorithms. Communications on Pure and Applied Mathematics, 66(2):145–164, 2013.

[^220]: Matthew Tancik, Ben Mildenhall, and Ren Ng. Stegastamp: Invisible hyperlinks in physical photographs. In CVPR, 2020.

[^221]: Ruixiang Tang, Mengnan Du, Ninghao Liu, Fan Yang, and Xia Hu. An embarrassingly simple approach for trojan attack in deep neural networks. In KDD, 2020.

[^222]: Yulong Tian, Fnu Suya, Fengyuan Xu, and David Evans. Stealthy backdoors as compression artifacts. IEEE TIFS, 2022.

[^223]: Mariya Toneva, Alessandro Sordoni, Remi Tachet des Combes, Adam Trischler, Yoshua Bengio, and Geoffrey J. Gordon. An empirical study of example forgetting during deep neural network learning. In ICLR, 2019.

[^224]: Alexander Turner, Dimitris Tsipras, and Aleksander Madry. Label-consistent backdoor attacks. arXiv preprint arXiv:1912.02771, 2019.

[^225]: Tsinghua University, Alibaba Security, and RealAI. Adversarial robustness benchmark. [https://ml.cs.tsinghua.edu.cn/adv-bench](https://ml.cs.tsinghua.edu.cn/adv-bench).

[^226]: Alexander Wan, Eric Wallace, Sheng Shen, and Dan Klein. Poisoning language models during instruction tuning. In ICML, 2023.

[^227]: Boxin Wang, Chejian Xu, Shuohang Wang, Zhe Gan, Yu Cheng, Jianfeng Gao, Ahmed Hassan Awadallah, and Bo Li. Adversarial glue: A multi-task benchmark for robustness evaluation of language models. In NeurIPS, 2021.

[^228]: Bolun Wang, Yuanshun Yao, Shawn Shan, Huiying Li, Bimal Viswanath, Haitao Zheng, and Ben Y Zhao. Neural cleanse: Identifying and mitigating backdoor attacks in neural networks. In 2019 IEEE Symposium on Security and Privacy (SP), pages 707–723. IEEE, 2019.

[^229]: Hongyi Wang, Kartik Sreenivasan, Shashank Rajput, Harit Vishwakarma, Saurabh Agarwal, Jy-yong Sohn, Kangwook Lee, and Dimitris Papailiopoulos. Attack of the tails: Yes, you really can backdoor federated learning. In NeurIPS, 2020.

[^230]: Ruotong Wang, Hongrui Chen, Zihao Zhu, Li Liu, Yong Zhang, Yanbo Fan, and Baoyuan Wu. Robust backdoor attack with visible, semantic, sample-specific, and compatible triggers. arXiv preprint arXiv:2306.00816, 2023.

[^231]: Tong Wang, Yuan Yao, Feng Xu, Shengwei An, Hanghang Tong, and Ting Wang. An invisible black-box backdoor attack through frequency domain. In ECCV, 2022.

[^232]: Xiaosen Wang and Kun He. Enhancing the transferability of adversarial attacks through variance tuning. In CVPR, 2021.

[^233]: Xiaosen Wang, Kun He, and John E Hopcroft. At-gan: A generative attack model for adversarial transferring on generative adversarial nets. arXiv preprint arXiv:1904.07793, 3(4), 2019.

[^234]: Xiaosen Wang, Xuanran He, Jingdong Wang, and Kun He. Admix: Enhancing the transferability of adversarial attacks. In ICCV, 2021.

[^235]: Xiaosen Wang, Jiadong Lin, Han Hu, Jingdong Wang, and Kun He. Boosting adversarial transferability through enhanced momentum. In BMVC, 2021.

[^236]: Xin Wang, Jie Ren, Shuyun Lin, Xiangming Zhu, Yisen Wang, and Quanshi Zhang. A unified approach to interpreting and boosting adversarial transferability. In ICLR, 2021.

[^237]: Yulong Wang, Minghui Zhao, Shenghong Li, Xin Yuan, and Wei Ni. Dispersed pixel perturbation-based imperceptible backdoor trigger for image classifier models. TIFS, 17:3091–3106, 2022.

[^238]: Zhibo Wang, Hengchang Guo, Zhifei Zhang, Wenxin Liu, Zhan Qin, and Kui Ren. Feature importance-aware transferable adversarial attacks. In ICCV, 2021.

[^239]: Zhenting Wang, Juan Zhai, and Shiqing Ma. Bppattack: Stealthy and efficient trojan attacks against deep neural networks via image quantization and contrastive adversarial learning. In CVPR, 2022.

[^240]: Zhibo Wang, Siyan Zheng, Mengkai Song, Qian Wang, Alireza Rahimpour, and Hairong Qi. advpattern: Physical-world attacks on deep person re-identification via adversarially transformable patterns. In ICCV, 2019.

[^241]: Xingxing Wei, Jun Zhu, Sha Yuan, and Hang Su. Sparse adversarial perturbations for videos. In AAAI, 2019.

[^242]: Yuxin Wen, Jonas Geiping, Liam Fowl, Hossein Souri, Rama Chellappa, Micah Goldblum, and Tom Goldstein. Thinking two moves ahead: Anticipating other users improves backdoor attacks in federated learning. arXiv preprint arXiv:2210.09305, 2022.

[^243]: Emily Wenger, Josephine Passananti, Arjun Nitin Bhagoji, Yuanshun Yao, Haitao Zheng, and Ben Y Zhao. Backdoor attacks against deep learning systems in the physical world. In CVPR, 2021.

[^244]: Daan Wierstra, Tom Schaul, Tobias Glasmachers, Yi Sun, Jan Peters, and Jürgen Schmidhuber. Natural evolution strategies. JMLR, 15(1):949–980, 2014.

[^245]: Eric Wong and J Zico Kolter. Learning perturbation sets for robust machine learning. In ICLR, 2020.

[^246]: Eric Wong, Frank Schmidt, and Zico Kolter. Wasserstein adversarial examples via projected sinkhorn iterations. In ICML, 2019.

[^247]: Baoyuan Wu, Hongrui Chen, Mingda Zhang, Zihao Zhu, Shaokui Wei, Danni Yuan, and Chao Shen. Backdoorbench: A comprehensive benchmark of backdoor learning. In NeurIPS Datasets and Benchmarks Track, 2022.

[^248]: Baoyuan Wu and Bernard Ghanem. Lp-box admm: A versatile framework for integer programming. TPAMI, 41(7):1695–1708, 2019.

[^249]: Baoyuan Wu, Shaokui Wei, Mingli Zhu, Meixi Zheng, Zihao Zhu, Mingda Zhang, Hongrui Chen, Danni Yuan, Li Liu, and Qingshan Liu. Defenses in adversarial machine learning: A survey, 2023.

[^250]: Baoyuan Wu, Xuanchen Yan, and Zeyu Qin. Blackboxbench. [https://github.com/SCLBD/BlackboxBench](https://github.com/SCLBD/BlackboxBench).

[^251]: Dongxian Wu, Yisen Wang, Shu-Tao Xia, James Bailey, and Xingjun Ma. Skip connections matter: On the transferability of adversarial examples generated with resnets. In ICLR, 2020.

[^252]: Lei Wu and Zhanxing Zhu. Towards understanding and improving the transferability of adversarial examples in deep neural networks. In ACML, 2020.

[^253]: Yutong Wu, Xingshuo Han, Han Qiu, and Tianwei Zhang. Computation and data efficient backdoor attacks. In ICCV, 2023.

[^254]: Zuxuan Wu, Ser-Nam Lim, Larry S Davis, and Tom Goldstein. Making an invisibility cloak: Real world adversarial attacks on object detectors. In ECCV, 2020.

[^255]: Pengfei Xia, Ziqiang Li, Wei Zhang, and Bin Li. Data-efficient backdoor attacks. In IJCAI, 2022.

[^256]: Pengfei Xia, Ziqiang Li, Wei Zhang, and Bin Li. Data-efficient backdoor attacks. In IJCAI, 2022.

[^257]: Zhen Xiang, David J Miller, Siheng Chen, Xi Li, and George Kesidis. A backdoor attack against 3d point cloud classifiers. In ICCV, 2021.

[^258]: Chaowei Xiao, Bo Li, Jun Yan Zhu, Warren He, Mingyan Liu, and Dawn Song. Generating adversarial examples with adversarial networks. In IJCAI, 2018.

[^259]: Chaowei Xiao, Jun-Yan Zhu, Bo Li, Warren He, Mingyan Liu, and Dawn Song. Spatially transformed adversarial examples. In ICLR, 2018.

[^260]: Chulin Xie, Keli Huang, Pin-Yu Chen, and Bo Li. Dba: Distributed backdoor attacks against federated learning. In ICLR, 2019.

[^261]: Cihang Xie, Zhishuai Zhang, Yuyin Zhou, Song Bai, Jianyu Wang, Zhou Ren, and Alan L Yuille. Improving transferability of adversarial examples with input diversity. In CVPR, 2019.

[^262]: Yi Xie, Zhuohang Li, Cong Shi, Jian Liu, Yingying Chen, and Bo Yuan. Enabling fast and universal audio adversarial attack using generative model. In AAAI, volume 35, 2021.

[^263]: Yifeng Xiong, Jiadong Lin, Min Zhang, John E. Hopcroft, and Kun He. Stochastic variance reduced ensemble adversarial attack for boosting the adversarial transferability. In CVPR, 2022.

[^264]: Kaidi Xu, Sijia Liu, Pu Zhao, Pin-Yu Chen, Huan Zhang, Deniz Erdogmus, Yanzhi Wang, and Xue Lin. Structured adversarial attack: Towards general implementation and better interpretability. ICLR, 2019.

[^265]: Kaidi Xu, Gaoyuan Zhang, Sijia Liu, Quanfu Fan, Mengshu Sun, Hongge Chen, Pin-Yu Chen, Yanzhi Wang, and Xue Lin. Adversarial t-shirt! evading person detectors in a physical world. In ECCV, 2020.

[^266]: Lei Xu, Yangyi Chen, Ganqu Cui, Hongcheng Gao, and Zhiyuan Liu. Exploring the universal vulnerability of prompt-based learning paradigm. In NAACL, 2022.

[^267]: Xing Xu, Jiefu Chen, Jinhui Xiao, Lianli Gao, Fumin Shen, and Heng Tao Shen. What machines see is not what they get: Fooling scene text recognition models with adversarial text images. In CVPR, 2020.

[^268]: Xing Xu, Jiefu Chen, Jinhui Xiao, Zheng Wang, Yang Yang, and Heng Tao Shen. Learning optimization-based adversarial perturbations for attacking sequential recognition models. In ACM Multimedia, 2020.

[^269]: Xiaojun Xu, Xinyun Chen, Chang Liu, Anna Rohrbach, Trevor Darrell, and Dawn Song. Fooling vision and language models despite localization and attention mechanism. In CVPR, 2018.

[^270]: Yan Xu, Baoyuan Wu, Fumin Shen, Yanbo Fan, Yong Zhang, Heng Tao Shen, and Wei Liu. Exact adversarial attack to image captioning via structured output learning with latent variables. In CVPR, 2019.

[^271]: Jiaqi Xue, Mengxin Zheng, Ting Hua, Yilin Shen, Yepeng Liu, Ladislau Boloni, and Qian Lou. Trojllm: A black-box trojan prompt attack on large language models. In NeurIPS, 2023.

[^272]: Mingfu Xue, Can He, Yinghao Wu, Shichang Sun, Yushu Zhang, Jian Wang, and Weiqiang Liu. Ptb: Robust physical backdoor attacks against deep neural networks in real world. Computers & Security, 2022.

[^273]: Hiromu Yakura and Jun Sakuma. Robust audio adversarial example for a physical attack. In IJCAI, 2019.

[^274]: Zhicong Yan, Gaolei Li, Yuan TIan, Jun Wu, Shenghong Li, Mingzhe Chen, and H Vincent Poor. Dehib: Deep hidden backdoor attack on semi-supervised learning via adversarial perturbation. In AAAI, 2021.

[^275]: Jiancheng Yang, Yangzhou Jiang, Xiaoyang Huang, Bingbing Ni, and Chenglong Zhao. Learning black-box attackers with transferable priors and query feedback. In NeurIPS, 2020.

[^276]: Hongwei Yao, Jian Lou, and Zhan Qin. Poisonprompt: Backdoor attack on prompt-based large language models. arXiv preprint arXiv:2310.12439, 2023.

[^277]: Yuanshun Yao, Huiying Li, Haitao Zheng, and Ben Y Zhao. Latent backdoor attacks on deep neural networks. In ACM CCS, 2019.

[^278]: Maksym Yatsura, Jan Metzen, and Matthias Hein. Meta-learning the search distribution of black-box random search based adversarial attacks. In NeurIPS, 2021.

[^279]: Fei Yin, Yong Zhang, Baoyuan Wu, Yan Feng, Jingyi Zhang, Yanbo Fan, and Yujiu Yang. Generalizable black-box adversarial attack with meta learning. TPAMI, 2022.

[^280]: Chun-Nam John Yu and Thorsten Joachims. Learning structural svms with latent variables. In ICML, 2009.

[^281]: Ping Yu, Kaitao Song, and Jianfeng Lu. Generating adversarial examples with conditional generative adversarial net. In ICPR, 2018.

[^282]: Yi Yu, Yufei Wang, Wenhan Yang, Shijian Lu, Yap-Peng Tan, and Alex C Kot. Backdoor attacks against deep image compression via adaptive frequency trigger. In CVPR, 2023.

[^283]: Jianhe Yuan and Zhihai He. Consistency-sensitivity guided ensemble black-box adversarial attacks in low-dimensional spaces. In ICCV, 2021.

[^284]: Ming Yuan and Yi Lin. Model selection and estimation in regression with grouped variables. Journal of the Royal Statistical Society: Series B, 68(1):49–67, 2006.

[^285]: Zheng Yuan, Jie Zhang, Yunpei Jia, Chuanqi Tan, Tao Xue, and Shiguang Shan. Meta gradient adversarial attack. In ICCV, 2021.

[^286]: Guoyang Zeng, Fanchao Qi, Qianrui Zhou, Tingji Zhang, Bairu Hou, Yuan Zang, Zhiyuan Liu, and Maosong Sun. Openattack: An open-source textual adversarial attack toolkit. In ACL and IJCNLP: System Demonstrations, 2021.

[^287]: Chaoning Zhang, Philipp Benz, Tooba Imtiaz, and In-So Kweon. Cd-uap: Class discriminative universal adversarial perturbation. In AAAI, 2020.

[^288]: Hangfan Zhang, Jinyuan Jia, Jinghui Chen, Lu Lin, and Dinghao Wu. A3fl: Adversarially adaptive backdoor attacks to federated learning. In Thirty-seventh Conference on Neural Information Processing Systems, 2023.

[^289]: Jie Zhang, Chen Dongdong, Qidong Huang, Jing Liao, Weiming Zhang, Huamin Feng, Gang Hua, and Nenghai Yu. Poison ink: Robust and invisible backdoor attack. TIP, 31:5691–5705, 2022.

[^290]: Jiliang Zhang and Chen Li. Adversarial examples: Opportunities and challenges. TNNLS, 31(7):2578–2593, 2019.

[^291]: Jiaming Zhang, Jitao Sang, Xian Zhao, Xiaowen Huang, Yanfeng Sun, and Yongli Hu. Adversarial privacy-preserving filter. In Proceedings of the 28th ACM International Conference on Multimedia, pages 1423–1431, 2020.

[^292]: Jianping Zhang, Weibin Wu, Jen-tse Huang, Yizhan Huang, Wenxuan Wang, Yuxin Su, and Michael R Lyu. Improving adversarial transferability via neuron attribution-based attacks. In CVPR, 2022.

[^293]: Quan Zhang, Yifeng Ding, Yongqiang Tian, Jianmin Guo, Min Yuan, and Yu Jiang. Advdoor: Adversarial backdoor attack of deep learning system. In ISSTA, 2021.

[^294]: Xinyang Zhang, Zheng Zhang, Shouling Ji, and Ting Wang. Trojaning language models for fun and profit. In EuroS&P. IEEE, 2021.

[^295]: Yanghao Zhang, Wenjie Ruan, Fu Wang, and Xiaowei Huang. Generalizing universal adversarial attacks beyond additive perturbations. In ICDM, 2020.

[^296]: Zhiyuan Zhang, Lingjuan Lyu, Weiqiang Wang, Lichao Sun, and Xu Sun. How to inject backdoors with better consistency: Logit anchoring on clean data. In ICLR, 2021.

[^297]: Zhengming Zhang, Ashwinee Panda, Linyue Song, Yaoqing Yang, Michael Mahoney, Prateek Mittal, Ramchandran Kannan, and Joseph Gonzalez. Neurotoxin: durable backdoors in federated learning. In ICML, 2022.

[^298]: Guoping Zhao, Mingyu Zhang, Jiajun Liu, Yaxian Li, and Ji-Rong Wen. Ap-gan: Adversarial patch attack on content-based image retrieval systems. GeoInformatica, pages 1–31, 2022.

[^299]: Pu Zhao, Sijia Liu, Yanzhi Wang, and Xue Lin. An admm-based universal framework for adversarial attacks on deep neural networks. In ACM Multimedia, 2018.

[^300]: Pu Zhao, Siyue Wang, Cheng Gongye, Yanzhi Wang, Yunsi Fei, and Xue Lin. Fault sneaking attack: A stealthy framework for misleading deep neural networks. In ACM/IEEE DAC, 2019.

[^301]: Shihao Zhao, Xingjun Ma, Xiang Zheng, James Bailey, Jingjing Chen, and Yu-Gang Jiang. Clean-label backdoor attacks on video recognition models. In CVPR, 2020.

[^302]: Yue Zhao, Hong Zhu, Ruigang Liang, Qintao Shen, Shengzhi Zhang, and Kai Chen. Seeing isn’t believing: Towards more robust adversarial attack against real world object detectors. In ACM CCS, 2019.

[^303]: Zhendong Zhao, Xiaojun Chen, Yuexin Xuan, Ye Dong, Dakui Wang, and Kaitai Liang. Defeat: Deep hidden feature backdoor attacks by imperceptible perturbation and latent representation constraints. In CVPR, 2022.

[^304]: Zhengyu Zhao, Zhuoran Liu, and Martha Larson. On success and simplicity: A second look at transferable targeted attacks. In NeurIPS, 2021.

[^305]: Xin Zheng, Yanbo Fan, Baoyuan Wu, Yong Zhang, Jue Wang, and Shirui Pan. Robust physical-world attacks on face recognition. Pattern Recognition, 133:109009, 2023.

[^306]: Haoti Zhong, Cong Liao, Anna Cinzia Squicciarini, Sencun Zhu, and David Miller. Backdoor embedding in convolutional neural network models via invisible perturbation. In ACM CODASPY, 2020.

[^307]: Nan Zhong, Zhenxing Qian, and Xinpeng Zhang. Imperceptible backdoor attack: from input space to feature representation. In IJCAI, 2022.

[^308]: Hang Zhou, Dongdong Chen, Jing Liao, Kejiang Chen, Xiaoyi Dong, Kunlin Liu, Weiming Zhang, Gang Hua, and Nenghai Yu. Lg-gan: Label guided adversarial network for flexible targeted attack of point cloud based deep networks. In CVPR, 2020.

[^309]: Linjun Zhou, Peng Cui, Xingxuan Zhang, Yinan Jiang, and Shiqiang Yang. Adversarial eigen attack on black-box models. In CVPR, 2022.

[^310]: Sicheng Zhu, Ruiyi Zhang, Bang An, Gang Wu, Joe Barrow, Zichao Wang, Furong Huang, Ani Nenkova, and Tong Sun. Autodan: Automatic and interpretable adversarial attacks on large language models. arXiv preprint arXiv:2310.15140, 2023.

[^311]: Yao Zhu, Yuefeng Chen, Xiaodan Li, Kejiang Chen, Yuan He, Xiang Tian, Bolun Zheng, Yaowu Chen, and Qingming Huang. Toward understanding and boosting adversarial transferability from a distribution perspective. TIP, 31:6487–6501, 2022.

[^312]: Yao Zhu, Jiacheng Sun, and Zhenguo Li. Rethinking adversarial transferability from a data distribution perspective. In ICLR, 2022.

[^313]: Zihao Zhu, Mingda Zhang, Shaokui Wei, Li Shen, Yanbo Fan, and Baoyuan Wu. Boosting backdoor attack with a learnable poisoning sample selection strategy. arXiv preprint arXiv:2307.07328, 2023.