---
title: "Knowledge distillation - Wikipedia"
source: "https://en.wikipedia.org/wiki/Knowledge_distillation"
author:
  - "[[Contributors to Wikimedia projects]]"
published: 2019-11-09
created: 2026-04-13
description:
tags:
  - "clippings"
---
In [machine learning](https://en.wikipedia.org/wiki/Machine_learning "Machine learning"), **knowledge distillation** or **model distillation** is the process of transferring knowledge from a large [model](https://en.wikipedia.org/wiki/Statistical_model "Statistical model") to a smaller one. While large models (such as very [deep neural networks](https://en.wikipedia.org/wiki/Deep_neural_network "Deep neural network") or [ensembles](https://en.wikipedia.org/wiki/Ensemble_learning "Ensemble learning") of many models) have more knowledge capacity than small models, this capacity might not be fully utilized. It can be just as computationally expensive to evaluate a model even if it utilizes little of its knowledge capacity. Knowledge distillation transfers knowledge from a large model to a smaller one without loss of [validity](https://en.wikipedia.org/wiki/Statistical_model_validation "Statistical model validation"). As smaller models are less expensive to evaluate, they can be deployed on less powerful hardware (such as a [mobile device](https://en.wikipedia.org/wiki/Mobile_device "Mobile device")).[^1]

There is also a less common technique called *Reverse Knowledge Distillation*, where knowledge is transferred from a smaller model to a larger one.[^2]

Model distillation is not to be confused with [model compression](https://en.wikipedia.org/wiki/Model_compression "Model compression"), which describes methods to decrease the size of a large model itself, without training a new model. Model compression generally preserves the architecture and the nominal parameter count of the model, while decreasing the bits-per-parameter.

Knowledge distillation has been successfully used in several applications of machine learning such as [object detection](https://en.wikipedia.org/wiki/Object_detection "Object detection"),[^3] [acoustic models](https://en.wikipedia.org/wiki/Acoustic_model "Acoustic model"),[^4] and [natural language processing](https://en.wikipedia.org/wiki/Natural_language_processing "Natural language processing").[^5] Recently, it has also been introduced to [graph neural networks](https://en.wikipedia.org/wiki/Graph_neural_network "Graph neural network") applicable to non-grid data.[^6]

## Methods

Knowledge transfer from a large model to a small one somehow needs to teach the latter without loss of validity. If both models are trained on the same data, the smaller model may have insufficient capacity to learn a [concise knowledge representation](https://en.wikipedia.org/wiki/Concision "Concision") compared to the large model. However, some information about a concise knowledge representation is encoded in the [pseudolikelihoods](https://en.wikipedia.org/wiki/Pseudolikelihood "Pseudolikelihood") assigned to its output: when a model correctly predicts a class, it assigns a large value to the output variable corresponding to such class, and smaller values to the other output variables. The distribution of values among the outputs for a record provides information on how the large model represents knowledge. Therefore, the goal of economical deployment of a valid model can be achieved by training only the large model on the data, exploiting its better ability to learn concise knowledge representations, and then distilling such knowledge into the smaller model, by training it to learn the [soft output](https://en.wikipedia.org/wiki/Soft-in_soft-out_decoder "Soft-in soft-out decoder") of the large model.[^1]

### Mathematical formulation

Given a large model as a function of the vector variable ${\displaystyle \mathbf {x} }$, trained for a specific [classification](https://en.wikipedia.org/wiki/Statistical_classification "Statistical classification") task, typically the final layer of classification networks is a [softmax](https://en.wikipedia.org/wiki/Softmax_function "Softmax function") in the form

${\displaystyle y_{i}(\mathbf {x} |t)={\frac {e^{\frac {z_{i}(\mathbf {x} )}{t}}}{\sum _{j}e^{\frac {z_{j}(\mathbf {x} )}{t}}}}}$

where ${\displaystyle t}$ is the *temperature*, a parameter which is set to 1 for a standard softmax. The softmax operator converts the [logit](https://en.wikipedia.org/wiki/Logit "Logit") values ${\displaystyle z_{i}(\mathbf {x} )}$ to pseudo-probabilities: higher temperature values generate softer distributions of pseudo-probabilities among the output classes. Knowledge distillation consists of training a smaller network, called the *distilled model*, on a [data set](https://en.wikipedia.org/wiki/Data_set "Data set") called the *transfer set* which could correspond to the original training set or consist of new, possibly unlabeled data. A [cross-entropy](https://en.wikipedia.org/wiki/Cross-entropy "Cross-entropy") [loss function](https://en.wikipedia.org/wiki/Loss_function "Loss function") is typically used, computed between the output of the distilled model ${\displaystyle \mathbf {y} (\mathbf {x} |t)}$ and the output of the large model ${\displaystyle {\hat {\mathbf {y} }}(\mathbf {x} |t)}$ on the same record (or the average of the individual outputs, if the large model is an ensemble), using a high value of softmax temperature ${\displaystyle t}$ for both models:[^1]

${\displaystyle E(\mathbf {x} |t)=-\sum _{i}{\hat {y}}_{i}(\mathbf {x} |t)\log y_{i}(\mathbf {x} |t).}$

In this context, a high temperature increases the [entropy](https://en.wikipedia.org/wiki/Entropy_\(information_theory\) "Entropy (information theory)") of the output, therefore providing more information to learn for the distilled model compared to hard targets, and at the same time reducing the [variance](https://en.wikipedia.org/wiki/Variance "Variance") of the [gradient](https://en.wikipedia.org/wiki/Gradient "Gradient") between different records, thus allowing a higher [learning rate](https://en.wikipedia.org/wiki/Learning_rate "Learning rate").[^1]

If [ground truth](https://en.wikipedia.org/wiki/Ground_truth "Ground truth") is available for the transfer set, the process can be strengthened by adding to the loss the cross-entropy between the output ${\displaystyle y_{i}(\mathbf {x} |1)}$ of the distilled model computed with ${\displaystyle t=1}$, and the known label ${\displaystyle {\bar {y}}_{i}}$

${\displaystyle E(\mathbf {x} |t)=-t^{2}\sum _{i}{\hat {y}}_{i}(\mathbf {x} |t)\log y_{i}(\mathbf {x} |t)-\sum _{i}{\bar {y}}_{i}\log y_{i}(\mathbf {x} |1)}$

where the component of the loss with respect to the large model is weighted by a factor of ${\displaystyle t^{2}}$ since, as the temperature increases, the gradient of the loss with respect to the model weights scales by a factor of ${\displaystyle {\frac {1}{t^{2}}}}$.[^1]

### Relationship with model compression

Under the assumption that the logits have zero [mean](https://en.wikipedia.org/wiki/Mean "Mean"), it is possible to show that model compression is a special case of knowledge distillation. The gradient of the knowledge distillation loss ${\displaystyle E}$ with respect to the logit of the distilled model ${\displaystyle z_{i}}$ is given by

${\displaystyle {\begin{aligned}{\frac {\partial }{\partial z_{i}}}E&=-{\frac {\partial }{\partial z_{i}}}\sum _{j}{\hat {y}}_{j}\log y_{j}\\&=-{\frac {\partial }{\partial z_{i}}}{\hat {y}}_{i}\log y_{i}+\left(-{\frac {\partial }{\partial z_{i}}}\sum _{k\neq i}{\hat {y}}_{k}\log y_{k}\right)\\&=-{\hat {y}}_{i}{\frac {1}{y_{i}}}{\frac {\partial }{\partial z_{i}}}y_{i}+\sum _{k\neq i}\left(-{\hat {y}}_{k}\cdot {\frac {1}{y_{k}}}\cdot e^{\frac {z_{k}}{t}}\cdot \left(-{\frac {1}{\left(\sum _{j}e^{\frac {z_{j}}{t}}\right)^{2}}}\right)\cdot e^{\frac {z_{i}}{t}}\cdot {\frac {1}{t}}\right)\\&=-{\hat {y}}_{i}{\frac {1}{y_{i}}}{\frac {\partial }{\partial z_{i}}}{\frac {e^{\frac {z_{i}}{t}}}{\sum _{j}e^{\frac {z_{j}}{t}}}}+\sum _{k\neq i}\left({\hat {y}}_{k}\cdot {\frac {1}{y_{k}}}\cdot y_{k}\cdot y_{i}\cdot {\frac {1}{t}}\right)\\&=-{\hat {y}}_{i}{\frac {1}{y_{i}}}\left({\frac {{\frac {1}{t}}e^{\frac {z_{i}}{t}}\sum _{j}e^{\frac {z_{j}}{t}}-{\frac {1}{t}}\left(e^{\frac {z_{i}}{t}}\right)^{2}}{\left(\sum _{j}e^{\frac {z_{j}}{t}}\right)^{2}}}\right)+{\frac {y_{i}\sum _{k\neq i}{\hat {y}}_{k}}{t}}\\&=-{\hat {y}}_{i}{\frac {1}{y_{i}}}\left({\frac {y_{i}}{t}}-{\frac {y_{i}^{2}}{t}}\right)+{\frac {y_{i}(1-{\hat {y}}_{i})}{t}}\\&={\frac {1}{t}}\left(y_{i}-{\hat {y}}_{i}\right)\\&={\frac {1}{t}}\left({\frac {e^{\frac {z_{i}}{t}}}{\sum _{j}e^{\frac {z_{j}}{t}}}}-{\frac {e^{\frac {{\hat {z}}_{i}}{t}}}{\sum _{j}e^{\frac {{\hat {z}}_{j}}{t}}}}\right)\\\end{aligned}}}$

where ${\displaystyle {\hat {z}}_{i}}$ are the logits of the large model. For large values of ${\displaystyle t}$ this can be approximated as

${\displaystyle {\frac {1}{t}}\left({\frac {1+{\frac {z_{i}}{t}}}{N+\sum _{j}{\frac {z_{j}}{t}}}}-{\frac {1+{\frac {{\hat {z}}_{i}}{t}}}{N+\sum _{j}{\frac {{\hat {z}}_{j}}{t}}}}\right)}$

and under the zero-mean hypothesis ${\displaystyle \sum _{j}z_{j}=\sum _{j}{\hat {z}}_{j}=0}$ it becomes ${\displaystyle {\frac {z_{i}-{\hat {z}}_{i}}{NT^{2}}}}$, which is the derivative of ${\displaystyle {\frac {1}{2}}\left(z_{i}-{\hat {z}}_{i}\right)^{2}}$, i.e. the loss is equivalent to matching the logits of the two models, as done in model compression.[^1]

### "Optimal Brain Damage" algorithm

The Optimal Brain Damage (OBD) algorithm is as follows:[^7]

Do until a desired level of sparsity or performance is reached:

Train the network (by methods such as backpropagation) until a reasonable solution is obtained

Compute the saliencies for each parameter

Delete some lowest-saliency parameters

Deleting a parameter means fixing the parameter to zero. The "saliency" of a parameter ${\displaystyle \theta }$ is defined as ${\displaystyle {\frac {1}{2}}(\partial _{\theta }^{2}L)\theta ^{2}}$, where ${\displaystyle L}$ is the loss function. The second-derivative ${\displaystyle \partial _{\theta }^{2}L}$ can be computed by [second-order backpropagation](https://en.wikipedia.org/wiki/Backpropagation#Hessian "Backpropagation").

The idea for optimal brain damage is to approximate the loss function in a neighborhood of optimal parameter ${\displaystyle \theta ^{*}}$ by [Taylor expansion](https://en.wikipedia.org/wiki/Taylor_expansion "Taylor expansion"):
$$
{\displaystyle L(\theta )\approx L(\theta ^{*})+{\frac {1}{2}}\sum _{i}(\partial _{\theta _{i}}^{2}L(\theta ^{*}))(\theta _{i}-\theta _{i}^{*})^{2}}
$$
 where ${\displaystyle \nabla L(\theta ^{*})\approx 0}$, since ${\displaystyle \theta ^{*}}$ is optimal, and the cross-derivatives ${\displaystyle \partial _{\theta _{i}}\partial _{\theta _{j}}L}$ are neglected to save compute. Thus, the saliency of a parameter approximates the increase in loss if that parameter is deleted.

## History

A related methodology was *model compression* or *pruning*, where a trained network is reduced in size. This was first done in 1965 by [Alexey Ivakhnenko](https://en.wikipedia.org/wiki/Alexey_Ivakhnenko "Alexey Ivakhnenko") and Valentin Lapa in [USSR](https://en.wikipedia.org/wiki/USSR "USSR") (1965).[^8] [^9] [^10] Their deep networks were trained layer by layer through [regression analysis](https://en.wikipedia.org/wiki/Regression_analysis "Regression analysis"). Superfluous hidden units were pruned using a separate validation set.[^11] Other neural network compression methods include Biased Weight Decay [^12] and Optimal Brain Damage.[^7]

An early example of neural network distillation was published by [Jürgen Schmidhuber](https://en.wikipedia.org/wiki/J%C3%BCrgen_Schmidhuber "Jürgen Schmidhuber") in 1991, in the field of [recurrent neural networks](https://en.wikipedia.org/wiki/Recurrent_neural_network "Recurrent neural network") (RNNs). The problem was sequence prediction for long sequences, i.e., [deep learning](https://en.wikipedia.org/wiki/Deep_learning "Deep learning"). Their approach was to use two RNNs. One of them (the *automatizer*) predicted the sequence, and another (the *chunker*) predicted the errors of the automatizer. Simultaneously, the automatizer predicted the internal states of the chunker. After the automatizer manages to predict the chunker's internal states well, it would start fixing the errors, and soon the chunker is obsoleted, leaving just one RNN in the end.[^13] [^14]

The idea of using the output of one neural network to train another neural network was also studied as the teacher-student network configuration.[^15] In 1992, several papers studied the [statistical mechanics](https://en.wikipedia.org/wiki/Statistical_mechanics "Statistical mechanics") of teacher-student configurations with committee machines [^16] [^17] or parity machines.[^18]

Compressing the knowledge of multiple models into a single [neural network](https://en.wikipedia.org/wiki/Neural_network "Neural network") was called *model compression* in 2006: compression was achieved by training a smaller model on large amounts of pseudo-data labelled by a higher-performing ensemble, optimizing to match the [logit](https://en.wikipedia.org/wiki/Logit "Logit") of the compressed model to the logit of the ensemble.[^19] The knowledge distillation [preprint](https://en.wikipedia.org/wiki/Preprint "Preprint") of [Geoffrey Hinton](https://en.wikipedia.org/wiki/Geoffrey_Hinton "Geoffrey Hinton") et al. (2015) [^1] formulated the concept and showed some results achieved in the task of [image classification](https://en.wikipedia.org/wiki/Image_classification "Image classification").

Knowledge distillation is also related to the concept of *behavioral cloning* discussed by Faraz Torabi et. al.[^20]

## References

## External links

- [Distilling the knowledge in a neural network – Google AI](https://research.google/pubs/distilling-the-knowledge-in-a-neural-network/)

[^1]: Hinton, Geoffrey; Vinyals, Oriol; Dean, Jeff (2015). "Distilling the knowledge in a neural network". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[1503.02531](https://arxiv.org/abs/1503.02531) \[[stat.ML](https://arxiv.org/archive/stat.ML)\].

[^2]: Yifan Xu and Yuxiang Wu and Zhiqiang Hu and Hang Xu and Zhongwei Wan and Yongfeng Zhang and Yu Qiao and Zhen Wang (2023). "RestGPT: Connecting Large Language Models with Real-World RESTful APIs". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2307.10698](https://arxiv.org/abs/2307.10698) \[[cs.CV](https://arxiv.org/archive/cs.CV)\].

[^3]: Chen, Guobin; Choi, Wongun; Yu, Xiang; Han, Tony; Chandraker, Manmohan (2017). "Learning efficient object detection models with knowledge distillation". *Advances in Neural Information Processing Systems*: 742–751.

[^4]: Asami, Taichi; Masumura, Ryo; Yamaguchi, Yoshikazu; Masataki, Hirokazu; Aono, Yushi (2017). *Domain adaptation of DNN acoustic models using knowledge distillation*. IEEE International Conference on Acoustics, Speech and Signal Processing. pp. 5185–5189.

[^5]: Cui, Jia; Kingsbury, Brian; [Ramabhadran, Bhuvana](https://en.wikipedia.org/wiki/Bhuvana_Ramabhadran "Bhuvana Ramabhadran"); Saon, George; Sercu, Tom; Audhkhasi, Kartik; Sethy, Abhinav; Nussbaum-Thom, Markus; Rosenberg, Andrew (2017). *Knowledge distillation across ensembles of multilingual models for low-resource languages*. IEEE International Conference on Acoustics, Speech and Signal Processing. pp. 4825–4829.

[^6]: Yang, Yiding; Jiayan, Qiu; Mingli, Song; Dacheng, Tao; Xinchao, Wang (2020). ["Distilling Knowledge from Graph Convolutional Networks"](https://openaccess.thecvf.com/content_CVPR_2020/papers/Yang_Distilling_Knowledge_From_Graph_Convolutional_Networks_CVPR_2020_paper.pdf) (PDF). *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition*: 7072–7081. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2003.10477](https://arxiv.org/abs/2003.10477). [Bibcode](https://en.wikipedia.org/wiki/Bibcode_\(identifier\) "Bibcode (identifier)"):[2020arXiv200310477Y](https://ui.adsabs.harvard.edu/abs/2020arXiv200310477Y).

[^7]: LeCun, Yann; Denker, John; Solla, Sara (1989). ["Optimal Brain Damage"](https://proceedings.neurips.cc/paper/1989/hash/6c9882bbac1c7093bd25041881277658-Abstract.html). *Advances in Neural Information Processing Systems*. **2**. Morgan-Kaufmann.

[^8]: Ivakhnenko, A. G.; Lapa, V. G. (1967). [*Cybernetics and Forecasting Techniques*](https://books.google.com/books?id=rGFgAAAAMAAJ). American Elsevier Publishing Co. [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [978-0-444-00020-0](https://en.wikipedia.org/wiki/Special:BookSources/978-0-444-00020-0 "Special:BookSources/978-0-444-00020-0").

[^9]: Ivakhnenko, A.G. (March 1970). ["Heuristic self-organization in problems of engineering cybernetics"](https://linkinghub.elsevier.com/retrieve/pii/0005109870900920). *Automatica*. **6** (2): 207–219. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1016/0005-1098(70)90092-0](https://doi.org/10.1016%2F0005-1098%2870%2990092-0).

[^10]: Ivakhnenko, Alexey (1971). ["Polynomial theory of complex systems"](http://gmdh.net/articles/history/polynomial.pdf) (PDF). *IEEE Transactions on Systems, Man, and Cybernetics*. SMC-1 (4): 364–378. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1109/TSMC.1971.4308320](https://doi.org/10.1109%2FTSMC.1971.4308320). [Archived](https://web.archive.org/web/20170829230621/http://www.gmdh.net/articles/history/polynomial.pdf) (PDF) from the original on 2017-08-29. Retrieved 2019-11-05.

[^11]: [Schmidhuber, Jürgen](https://en.wikipedia.org/wiki/J%C3%BCrgen_Schmidhuber "Jürgen Schmidhuber") (2022). "Annotated History of Modern AI and Deep Learning". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2212.11279](https://arxiv.org/abs/2212.11279) \[[cs.NE](https://arxiv.org/archive/cs.NE)\].

[^12]: Hanson, Stephen; Pratt, Lorien (1988). ["Comparing Biases for Minimal Network Construction with Back-Propagation"](https://proceedings.neurips.cc/paper/1988/hash/1c9ac0159c94d8d0cbedc973445af2da-Abstract.html). *Advances in Neural Information Processing Systems*. **1**. Morgan-Kaufmann.

[^13]: [Schmidhuber, Jürgen](https://en.wikipedia.org/wiki/J%C3%BCrgen_Schmidhuber "Jürgen Schmidhuber") (April 1991). ["Neural Sequence Chunkers"](https://people.idsia.ch/~juergen/FKI-148-91ocr.pdf) (PDF). *TR FKI-148, TU Munich*.

[^14]: Schmidhuber, Jürgen (1992). ["Learning complex, extended sequences using the principle of history compression"](https://web.archive.org/web/20170706014739/ftp://ftp.idsia.ch/pub/juergen/chunker.pdf) (PDF). *Neural Computation*. **4** (2): 234–242. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1162/neco.1992.4.2.234](https://doi.org/10.1162%2Fneco.1992.4.2.234). [S2CID](https://en.wikipedia.org/wiki/S2CID_\(identifier\) "S2CID (identifier)") [18271205](https://api.semanticscholar.org/CorpusID:18271205). Archived from [the original](ftp://ftp.idsia.ch/pub/juergen/chunker.pdf) (PDF) on 2017-07-06.

[^15]: Watkin, Timothy L. H.; Rau, Albrecht; Biehl, Michael (1993-04-01). ["The statistical mechanics of learning a rule"](https://link.aps.org/doi/10.1103/RevModPhys.65.499). *Reviews of Modern Physics*. **65** (2): 499–556. [Bibcode](https://en.wikipedia.org/wiki/Bibcode_\(identifier\) "Bibcode (identifier)"):[1993RvMP...65..499W](https://ui.adsabs.harvard.edu/abs/1993RvMP...65..499W). [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1103/RevModPhys.65.499](https://doi.org/10.1103%2FRevModPhys.65.499).

[^16]: Schwarze, H; Hertz, J (1992-10-15). ["Generalization in a Large Committee Machine"](https://iopscience.iop.org/article/10.1209/0295-5075/20/4/015). *Europhysics Letters*. **20** (4): 375–380. [Bibcode](https://en.wikipedia.org/wiki/Bibcode_\(identifier\) "Bibcode (identifier)"):[1992EL.....20..375S](https://ui.adsabs.harvard.edu/abs/1992EL.....20..375S). [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1209/0295-5075/20/4/015](https://doi.org/10.1209%2F0295-5075%2F20%2F4%2F015). [ISSN](https://en.wikipedia.org/wiki/ISSN_\(identifier\) "ISSN (identifier)") [0295-5075](https://search.worldcat.org/issn/0295-5075).

[^17]: Mato, G; Parga, N (1992-10-07). ["Generalization properties of multilayered neural networks"](https://iopscience.iop.org/article/10.1088/0305-4470/25/19/017). *Journal of Physics A: Mathematical and General*. **25** (19): 5047–5054. [Bibcode](https://en.wikipedia.org/wiki/Bibcode_\(identifier\) "Bibcode (identifier)"):[1992JPhA...25.5047M](https://ui.adsabs.harvard.edu/abs/1992JPhA...25.5047M). [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1088/0305-4470/25/19/017](https://doi.org/10.1088%2F0305-4470%2F25%2F19%2F017). [ISSN](https://en.wikipedia.org/wiki/ISSN_\(identifier\) "ISSN (identifier)") [0305-4470](https://search.worldcat.org/issn/0305-4470).

[^18]: Hansel, D; Mato, G; Meunier, C (1992-11-01). ["Memorization Without Generalization in a Multilayered Neural Network"](https://iopscience.iop.org/article/10.1209/0295-5075/20/5/015). *Europhysics Letters*. **20** (5): 471–476. [Bibcode](https://en.wikipedia.org/wiki/Bibcode_\(identifier\) "Bibcode (identifier)"):[1992EL.....20..471H](https://ui.adsabs.harvard.edu/abs/1992EL.....20..471H). [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1209/0295-5075/20/5/015](https://doi.org/10.1209%2F0295-5075%2F20%2F5%2F015). [ISSN](https://en.wikipedia.org/wiki/ISSN_\(identifier\) "ISSN (identifier)") [0295-5075](https://search.worldcat.org/issn/0295-5075).

[^19]: Buciluǎ, Cristian; Caruana, Rich; Niculescu-Mizil, Alexandru (2006). "Model compression". *Proceedings of the 12th ACM SIGKDD international conference on Knowledge discovery and data mining*.

[^20]: Torabi, Faraz; Warnell, Garrett; Stone, Peter (2018). "Behavioral Cloning from Observation". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[1805.01954](https://arxiv.org/abs/1805.01954) \[[cs.AI](https://arxiv.org/archive/cs.AI)\].