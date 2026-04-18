---
title: "Model compression - Wikipedia"
source: "https://en.wikipedia.org/wiki/Model_compression"
author:
  - "[[Contributors to Wikimedia projects]]"
published: 2024-10-18
created: 2026-04-13
description:
tags:
  - "clippings"
---
**Model compression** is a [machine learning](https://en.wikipedia.org/wiki/Machine_learning "Machine learning") technique for reducing the size of trained models. Large models can achieve high accuracy, but often at the cost of significant resource requirements. Compression techniques aim to compress models without significant performance reduction. Smaller models require less storage space, and consume less memory and compute during inference.[^1]

Compressed models enable deployment on resource-constrained devices such as [smartphones](https://en.wikipedia.org/wiki/Smartphone "Smartphone"), [embedded systems](https://en.wikipedia.org/wiki/Embedded_system "Embedded system"), [edge computing](https://en.wikipedia.org/wiki/Edge_computing "Edge computing") devices, and [consumer electronics](https://en.wikipedia.org/wiki/Consumer_electronics "Consumer electronics") computers. Efficient inference is also valuable for large corporations that serve large model inference over an API, allowing them to reduce computational costs and improve response times for users.[^2]

Model compression is not to be confused with [knowledge distillation](https://en.wikipedia.org/wiki/Knowledge_distillation "Knowledge distillation"), in which a smaller "student" model is *trained* to imitate the input-output behavior of a larger "teacher" model (as opposed to using the "teacher"'s trained parameters or the "teacher"'s training targets).[^3]

## Techniques

Several techniques are employed for model compression.

### Pruning

Pruning sparsifies a large model by setting some parameters to exactly zero. This effectively reduces the number of parameters. This allows the use of [sparse matrix operations](https://en.wikipedia.org/wiki/Sparse_matrix "Sparse matrix"), which are faster than dense matrix operations.[^4]

Pruning criteria can be based on magnitudes of parameters, the statistical pattern of neural [activations](https://en.wikipedia.org/wiki/Activation_function "Activation function"), [Hessian values](https://en.wikipedia.org/wiki/Hessian_matrix "Hessian matrix"), etc.[^5] [^6]

### Quantization

Quantization reduces the numerical precision of weights and activations. For example, instead of storing weights as 32-bit [floating-point](https://en.wikipedia.org/wiki/Floating-point_arithmetic "Floating-point arithmetic") numbers, they can be represented using 8-bit integers. Low-precision parameters take up less space, and takes less compute to perform arithmetic with.[^7]

It is also possible to quantize some parameters more aggressively than others, so for example, a less important parameter can have 8-bit precision while another, more important parameter, can have 16-bit precision. Inference with such models requires [mixed-precision arithmetic](https://en.wikipedia.org/wiki/Mixed-precision_arithmetic "Mixed-precision arithmetic").[^8] [^9]

Quantized models can also be used during training (rather than after training). [PyTorch](https://en.wikipedia.org/wiki/PyTorch "PyTorch") implements automatic mixed-precision (AMP), which performs autocasting, gradient scaling, and loss scaling.[^10] [^11]

### Low-rank factorization

Weight matrices can be approximated by low- [rank](https://en.wikipedia.org/wiki/Rank_\(linear_algebra\) "Rank (linear algebra)") matrices. Let ${\displaystyle W}$ be a weight matrix of shape ${\displaystyle m\times n}$. A low-rank approximation is ${\displaystyle W\approx UV^{T}}$, where ${\displaystyle U}$ and ${\displaystyle V}$ are matrices of shapes ${\displaystyle m\times k,n\times k}$. When ${\displaystyle k}$ is small, this both reduces the number of parameters needed to represent ${\displaystyle W}$ approximately, and accelerates matrix multiplication by ${\displaystyle W}$.

Low-rank approximations can be found by [singular value decomposition](https://en.wikipedia.org/wiki/Singular_value_decomposition "Singular value decomposition") (SVD). The choice of rank for each weight matrix is a hyperparameter, and jointly optimized as a mixed discrete-continuous optimization problem.[^12] The rank of weight matrices may also be pruned after training, taking into account the effect of activation functions like ReLU on the implicit rank of the weight matrices.[^13]

## Training

Model compression may be decoupled from training, that is, a model is first trained without regard for how it might be compressed, then it is compressed. However, it may also be combined with training.

The "train big, then compress" method trains a large model for a small number of training steps (less than it would be if it were trained to convergence), then heavily compress the model. It is found that at the same compute budget, this method results in a better model than lightly compressed, small models.[^14]

In Deep Compression,[^15] the compression has three steps.

- First loop (pruning): prune all weights lower than a threshold, then finetune the network, then prune again, etc.
- Second loop (quantization): cluster weights, then enforce weight sharing among all weights in each cluster, then finetune the network, then cluster again, etc.
- Third step: Use [Huffman coding](https://en.wikipedia.org/wiki/Huffman_coding "Huffman coding") to losslessly compress the model.

The [SqueezeNet](https://en.wikipedia.org/wiki/SqueezeNet "SqueezeNet") paper reported that Deep Compression achieved a compression ratio of 35 on AlexNet, and a ratio of ~10 on SqueezeNets.[^16]

## References

- Review papers
	- Li, Zhuo; Li, Hengyi; Meng, Lin (March 12, 2023). ["Model Compression for Deep Neural Networks: A Survey"](https://doi.org/10.3390%2Fcomputers12030060). *Computers*. **12** (3). MDPI AG: 60. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.3390/computers12030060](https://doi.org/10.3390%2Fcomputers12030060). [ISSN](https://en.wikipedia.org/wiki/ISSN_\(identifier\) "ISSN (identifier)") [2073-431X](https://search.worldcat.org/issn/2073-431X).
		- Deng, By Lei; Li, Guoqi; Han, Song; Shi, Luping; Xie, Yuan (March 20, 2020). "Model Compression and Hardware Acceleration for Neural Networks: A Comprehensive Survey". *Proceedings of the IEEE*. **108** (4): 485–532. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1109/JPROC.2020.2976475](https://doi.org/10.1109%2FJPROC.2020.2976475).
		- Cheng, Yu; Wang, Duo; Zhou, Pan; Zhang, Tao (October 23, 2017). "A Survey of Model Compression and Acceleration for Deep Neural Networks". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[1710.09282](https://arxiv.org/abs/1710.09282) \[[cs.LG](https://arxiv.org/archive/cs.LG)\].
		- Choudhary, Tejalal; Mishra, Vipul; Goswami, Anurag; Sarangapani, Jagannathan (February 8, 2020). "A comprehensive survey on model compression and acceleration". *Artificial Intelligence Review*. **53** (7). Springer Science and Business Media LLC: 5113–5155. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1007/s10462-020-09816-7](https://doi.org/10.1007%2Fs10462-020-09816-7). [ISSN](https://en.wikipedia.org/wiki/ISSN_\(identifier\) "ISSN (identifier)") [0269-2821](https://search.worldcat.org/issn/0269-2821).

[^1]: Zhou, Luping (2019). [*Large-Scale Annotation of Biomedical Data and Expert Label Synthesis and Hardware Aware Learning for Medical Imaging and Computer Assisted Intervention:... Notes in Computer Science Book 11851)*](https://www.google.com/books/edition/Large_Scale_Annotation_of_Biomedical_Dat/CsC_DwAAQBAJ?hl=en&gbpv=1&dq=model+compression&pg=PA98&printsec=frontcover). Springer. p. 98-101.

[^2]: Davies, E. R. (2021). [*Advanced Methods and Deep Learning in Computer Vision (Computer Vision and Pattern Recognition)*](https://www.google.com/books/edition/Advanced_Methods_and_Deep_Learning_in_Co/ZqYsEAAAQBAJ?hl=en&gbpv=1&dq=model+compression&pg=PA167&printsec=frontcover). Academic Press. p. 167. [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [978-0128221495](https://en.wikipedia.org/wiki/Special:BookSources/978-0128221495 "Special:BookSources/978-0128221495").

[^3]: Chen, Hsiao-Hwa (2025). [*Wireless and Satellite Systems: 14th EAI International Conference, WiSATS 2024, Harbin, China, August 23–25, 2024, Proceedings, Part II (Lecture Notes... and Telecommunications Engineering)*](https://www.google.com/books/edition/Wireless_and_Satellite_Systems/Ep5REQAAQBAJ?hl=en&gbpv=1&dq=model+compression&pg=PA141&printsec=frontcover). Springer. p. 141. [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [3031862023](https://en.wikipedia.org/wiki/Special:BookSources/3031862023 "Special:BookSources/3031862023").

[^4]: Lokoč, Jakub (2021). [*MultiMedia Modeling: 27th International Conference, MMM 2021, Prague, Czech Republic, June 22–24, 2021, Proceedings, Part I (Lecture Notes in Computer Science Book 12572)*](https://www.google.com/books/edition/MultiMedia_Modeling/dcUWEAAAQBAJ?hl=en&gbpv=1&dq=model+compression&pg=PA668&printsec=frontcover). Springer. p. 668. [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [978-3030678326](https://en.wikipedia.org/wiki/Special:BookSources/978-3030678326 "Special:BookSources/978-3030678326").

[^5]: Reed, R. (September 1993). "Pruning algorithms-a survey". *IEEE Transactions on Neural Networks*. **4** (5): 740–747. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1109/72.248452](https://doi.org/10.1109%2F72.248452). [PMID](https://en.wikipedia.org/wiki/PMID_\(identifier\) "PMID (identifier)") [18276504](https://pubmed.ncbi.nlm.nih.gov/18276504).

[^6]: Blalock, Davis; Gonzalez Ortiz, Jose Javier; Frankle, Jonathan; Guttag, John (2020-03-15). ["What is the State of Neural Network Pruning?"](https://proceedings.mlsys.org/paper_files/paper/2020/hash/6c44dc73014d66ba49b28d483a8f8b0d-Abstract.html). *Proceedings of Machine Learning and Systems*. **2**: 129–146.

[^7]: Ahanga, Reza (2023). [*Advancement in Business Analytics Tools for Higher Financial Performance*](https://www.google.com/books/edition/Advancement_in_Business_Analytics_Tools/O4_QEAAAQBAJ?hl=en&gbpv=1&dq=model+compression&pg=PA247&printsec=frontcover). IGI Global. p. 247. [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [1668483866](https://en.wikipedia.org/wiki/Special:BookSources/1668483866 "Special:BookSources/1668483866").

[^8]: Abdelfattah, Ahmad; Anzt, Hartwig; Boman, Erik G.; Carson, Erin; Cojean, Terry; Dongarra, Jack; Gates, Mark; Grützmacher, Thomas; Higham, Nicholas J.; Li, Sherry; Lindquist, Neil; Liu, Yang; Loe, Jennifer; Luszczek, Piotr; Nayak, Pratik; Pranesh, Sri; Rajamanickam, Siva; Ribizel, Tobias; Smith, Barry; Swirydowicz, Kasia; Thomas, Stephen; Tomov, Stanimire; Tsai, Yaohung M.; Yamazaki, Ichitaro; [Urike Meier Yang](https://en.wikipedia.org/wiki/Ulrike_Meier_Yang "Ulrike Meier Yang") (2020). "A Survey of Numerical Methods Utilizing Mixed Precision Arithmetic". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2007.06674](https://arxiv.org/abs/2007.06674) \[[cs.MS](https://arxiv.org/archive/cs.MS)\].

[^9]: Micikevicius, Paulius; Narang, Sharan; Alben, Jonah; Diamos, Gregory; Elsen, Erich; Garcia, David; Ginsburg, Boris; Houston, Michael; Kuchaiev, Oleksii (2018-02-15). "Mixed Precision Training". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[1710.03740](https://arxiv.org/abs/1710.03740) \[[cs.AI](https://arxiv.org/archive/cs.AI)\].

[^10]: ["Mixed Precision — PyTorch Training Performance Guide"](https://residentmario.github.io/pytorch-training-performance-guide/mixed-precision.html). *residentmario.github.io*. Retrieved 2024-09-10.

[^11]: ["What Every User Should Know About Mixed Precision Training in PyTorch"](https://pytorch.org/blog/what-every-user-should-know-about-mixed-precision-training-in-pytorch/). *PyTorch*. Retrieved 2024-09-10.

[^12]: Idelbayev, Yerlan; Carreira-Perpiñán, Miguel Á. (2020). ["Low-Rank Compression of Neural Nets: Learning the Rank of Each Layer"](https://openaccess.thecvf.com/content_CVPR_2020/html/Idelbayev_Low-Rank_Compression_of_Neural_Nets_Learning_the_Rank_of_Each_CVPR_2020_paper.html). *2020 IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2020, Seattle, WA, USA, June 13–19, 2020*. Computer Vision Foundation / IEEE. pp. 8046–8056. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1109/CVPR42600.2020.00807](https://doi.org/10.1109%2FCVPR42600.2020.00807). [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [978-1-7281-7168-5](https://en.wikipedia.org/wiki/Special:BookSources/978-1-7281-7168-5 "Special:BookSources/978-1-7281-7168-5").

[^13]: Dittmer, Sören; King, Emily J.; Maass, Peter (2020). ["Singular Values for ReLU Layers"](https://ieeexplore.ieee.org/document/8891761). *IEEE Transactions on Neural Networks and Learning Systems*. Vol. 31. IEEE. pp. 3594–3605. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[1812.02566](https://arxiv.org/abs/1812.02566). [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1109/TNNLS.2019.2945113](https://doi.org/10.1109%2FTNNLS.2019.2945113).

[^14]: Li, Zhuohan; Wallace, Eric; Shen, Sheng; Lin, Kevin; Keutzer, Kurt; Klein, Dan; Gonzalez, Joey (2020-11-21). ["Train Big, Then Compress: Rethinking Model Size for Efficient Training and Inference of Transformers"](https://proceedings.mlr.press/v119/li20m.html). *Proceedings of the 37th International Conference on Machine Learning*. PMLR: 5958–5968.

[^15]: Han, Song; Mao, Huizi; Dally, William J. (2016-02-15). "Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[1510.00149](https://arxiv.org/abs/1510.00149) \[[cs.CV](https://arxiv.org/archive/cs.CV)\].

[^16]: Iandola, Forrest N; Han, Song; Moskewicz, Matthew W; Ashraf, Khalid; Dally, William J; Keutzer, Kurt (2016). "SqueezeNet: AlexNet-level accuracy with 50x fewer parameters and <0.5MB model size". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[1602.07360](https://arxiv.org/abs/1602.07360) \[[cs.CV](https://arxiv.org/archive/cs.CV)\].