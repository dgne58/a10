---
title: "How Deep Learning Sees the World: A Survey on Adversarial Attacks & Defenses"
source: "https://pdf2md.morethan.io/"
author:
published:
created: 2026-04-15
description: "Converts PDF files to Markdown."
tags:
  - "clippings"
---
## How Deep Learning Sees the World: A Survey on

## Adversarial Attacks & Defenses

#### Joana C. Costa, Tiago Roxo, Hugo Proenc ̧a,Senior Member, IEEE,Pedro R. M. Inacio, ́ Senior Member, IEEE

```
Abstract—Deep Learning is currently used to perform multiple
tasks, such as object recognition, face recognition, and natural
language processing. However, Deep Neural Networks (DNNs)
are vulnerable to perturbations that alter the network prediction
(adversarial examples), raising concerns regarding its usage in
critical areas, such as self-driving vehicles, malware detection,
and healthcare. This paper compiles the most recent adversarial
attacks, grouped by the attacker capacity, and modern defenses
clustered by protection strategies. We also present the new
advances regarding Vision Transformers, summarize the datasets
and metrics used in the context of adversarial settings, and
compare the state-of-the-art results under different attacks,
finishing with the identification of open issues.
Index Terms—Adversarial attacks, adversarial defenses,
datasets, evaluation metrics, survey, vision transformers.
```

##### I. INTRODUCTION

## M

```
ACHINE Learning (ML) algorithms have been able
to solve various types of problems, namely highly
complex ones, through the usage of Deep Neural Networks
(DNNs) [1], achieving results similar to, or better than, humans
in multiple tasks, such as object recognition [2], [3], face
recognition [4], [5], and natural language processing [6], [7].
These networks have also been employed in critical areas,
such as self-driving vehicles [8], [9], malware detection [10],
[11], and healthcare [12], [13], whose application and impaired
functioning can severely impact their users.
Promising results shown by DNNs lead to the sense that
these networks could correctly generalize in the local neigh-
borhood of an input (image). These results motivate the
adoption and integration of these networks in real-time image
analysis, such as traffic sign recognition and vehicle seg-
mentation, making malicious entities target these techniques.
However, it was discovered that DNNs are susceptible to small
perturbations in their input [14], which entirely alter their
prediction, making it harder for them to be applied in critical
areas. These perturbations have two main characteristics: 1)
invisible to the Human eye or slight noise that does not alter
Human prediction; and 2) significantly increase the confidence
of erroneous output, the DNNs predict the wrong class with
higher confidence than all other classes. As a result of these
assertions, the effect of the perturbations has been analyzed
with more focus on object recognition, which will also be the
main target of this survey.
Papernotet al.[15] distinguishes four types of adversaries
depending on the information they have access to: (i) training
```
```
The authors are with Instituto de Telecomunicac ̧oes, Universidade da Beira ̃
Interior, Portugal.
Manuscript received XX, 2023; revised XX, 2023.
```
```
data and network architecture, (ii) only training data or only
network, (iii) oracle, and (iv) only pairs of input and output. In
almost all real scenarios, the attacker does not have access to
the training data or the network architecture, which diminishes
the strength of the attack performed on a network, leaving the
adversary with access to the responses given by the network,
either by asking questions directly to it or by having pairs of
input and prediction. Furthermore, the queries to a model are
usually limited or very expensive [16], making it harder for
an attacker to produce adversarial examples.
Multiple mechanisms [17]–[20] were proposed to defend
against legacy attacks, already displaying their weakened
effect when adequately protected, which are clustered based on
six different domains in this survey. Regardless of the attacks
and defenses already proposed, there is no assurance about
the effective robustness of these networks and if they can be
trusted in critical areas, clearly raising the need to make the
DNNs inherently robust or easy to be updated every time a
new vulnerability is encountered. This motivates the presented
work, whose main contributions are summarized as follows:
```
- We present the most recent adversarial attacks grouped by  
	the adversary capacity, accompanied by an illustration of  
	the differences between black-box and white-box attacks;
- We propose six different domains for adversarial defense  
	grouping, assisted by exemplificative figures of each of  
	these domains, and describe the effects of adversarial  
	examples in ViTs;
- We detail the most widely used metrics and datasets,  
	present state-of-the-art results on CIFAR-10, CIFAR-100,  
	and ImageNet, and propose directions for future works.  
	The remaining of the paper is organized as follows: Sec-  
	tion II provides background information; Section III compares  
	this review with others; Section IV presents the set of adver-  
	sarial attacks; Section V shows a collection of defenses to  
	overcome these attacks; Section VII displays the commonly  
	used datasets; Section VIII lists and elaborates on metrics and  
	presents state-of-the-art results; and Section IX presents future  
	directions, with the concluding remarks included in Section X.

##### II. BACKGROUND FORADVERSARIALATTACKS

```
A. Neural Network Architectures
When an input image is fed into a CNN, it is converted into
a matrix containing the numeric values representing the image
or, if the image is colored, a set of matrices containing the
numeric values for each color channel. Then, the Convolutions
apply filters to these matrixes and calculate a set of reduced-
size features. Finally, these features have an array format fed
```

## arXiv:2305.10862v1 \[cs.CV\] 18 May 2023

```
0 0 0
0 0
1
```
```
0
0 1
```
```
0 0 1
0 0
0
```
```
0
1 1
```
```
0 0 0
0 0
0
```
```
0
0 0
```
```
Input Image Convolutions Fully Connected
```

Fig. 1. Schematic example of the Convolutional Neural Networks mechanism  
to classify images.

```
Patches
```
```
Transformer Encoder
```
```
MLP Head
```

Fig. 2. Schematic example of a simplified vision transformer used to classify  
images.

into the Fully Connected that classifies the provided image.  
Figure 1 shows an elementary example of CNNs used to  
classify images.  
Contrary to the CNN, ViT does not receive the image as  
a whole as input; instead, it is pre-processed to be divided  
into Patches, which are smaller parts of the original image, as  
displayed in Figure 2. These Patches are not fed randomly to  
the Transformer Encoder, they are ordered by their position,  
and both the Patches and their position are fed into the  
Transformer Encoder. Finally, the output resulting from the  
Transformer Encoder is fed into the Multi-Layer Perceptron  
(MLP) Head that classifies the image.

B. Adversarial Example

Misclassification might be justified if the object contained  
in the image is not visible even to Humans. However, adver-  
sarial examples do not fit this scope. These examples add a  
perturbation to an image that causes the DNNs to misclassify  
the object in the image, yet Humans can correctly classify the  
same object.  
The adversarial attacks described throughout this survey  
focus on identifying the adversarial examples that make DNNs  
misclassify. These attacks identify specific perturbations that  
modify the DNN classification while being correctly classified  
by Humans. The calculation of these perturbations is an  
optimization problem formally defined as:

```
arg min
δX
‖δX‖s.t. f(X+δX) =Y∗, (1)
```

wherefis the is the classifier,δXis the perturbation,Xis  
the original/benign image, andY∗is the adversarial output.  
Furthermore, the adversarial example is defined as:

```
X∗=X+δX, (2)
```
```
Fig. 3. Adversarial Examples created using different state-of-the-art adver-
sarial attacks. The first column represents the original image; the second
represents the perturbation used to generate the adversarial images in the third
column. The images were resized for better visualization. Images withdrawn
from [14], [21], [22]. The first perturbation follows the edges of the building,
the second is concentrated in the area of the whale, and the third is more
smooth and greater in area.
```
```
whereX∗is the adversarial image.
Figure 3 displays adversarial examples generated using
different attacks. Mainly, the first row is the Limited-memory
Broyden-Fletcher-Goldfarb-Shanno (L-BFGS) [14] attack, the
second row is the DeepFool [21] attack, and the third row
is the SmoothFool [22] attack. When observing the L-BFGS,
the perturbation applies noise to almost the entirety of the
adversarial image. The DeepFool attack only perturbs the area
of the whale but not all the pixels in that area. Finally, the
SmoothFool attack slightly disturbs the pixels in the area of the
image. These three attacks display the evolution of adversarial
attacks in decreasing order of detectability and, consequently,
increasing order of strength.
To limit the noise that each perturbation can add to an
image, the adversarial attacks are divided intoL 0 ,L 2 , and
Lpnorms, known asVector Norms. Furthermore, commonly
used terminologies in the context of adversarial examples are
defined in Table I.
```
```
C. Vector Norms andConstraint
Vector Norms are functions that take a vector as input and
output a positive value (scalar). These functions are essential to
ML and allow the backpropagation algorithms to compute the
loss value as a scalar. The family of these functions is known
as thep-norm, and, in the context of adversarial attacks, the
considered values forpare 0 , 2 , and∞.
L 0 norm consists of counting the number of non-zero
elements in the vector and is formally given as:
||x|| 0 = (|x 1 |^0 +|x 2 |^0 +...+|xn|^0 ), (3)
```
```
wherex 1 toxnare the elements of the vectorx.
```
```
L 0 L 2 L
```

Fig. 4. Geometric representation of thel 0,l 2, andl∞norms, from left to  
right, respectively.

L 2 norm, also known as the Euclidean distance, measures  
the vector distance to the origin and is formally defined as:

```
||x|| 2 = (|x 1 |^2 +|x 2 |^2 +...+|xn|^2 )
```

(^12)  
, (4)  
wherex 1 toxnare the elements of the vectorx.  
L∞normrepresents the maximum hypothetical value that  
pcan have and returns the absolute value of the element with  
the largest magnitude, formally as:  
||x||∞= max  
i  
|xi|, (5)  
wherexiis each element of the vectorx.  
A geometric representation of the area of exploitation for  
the three considered p-norm is displayed in Figure 4. One  
relevant property of the p-norm is: the higherpis, the more  
important the contribution of large errors; the lowerpis, the  
higher the contribution of small errors. This translates into a  
largepbenefiting small maximal errors (minimal perturbations  
along multiple pixels) and a smallpencouraging larger spikes  
in fewer places (abrupt perturbations along minimal pixels).  
Therefore,l 2 andl 0 attacks have greater detectability thanl∞  
attacks, with the latter being more threatening.  
Another constraint normally seen in the context of adver-  
sarial attacks is, which is a constant that controls the amount  
of noise, via generated perturbation, that can be added to an  
image. Usually, it is a tiny number and varies depending on the  
used dataset, decreasing when the task increases in difficulty.  
According to the literature, for MNIST,= 0. 1, for CIFAR-  
and CIFAR-100,= 8/ 255, and for ImageNet,= 4/ 255.  
D. Adversary Goals and Capacity  
Besides the restriction imposed by the different Vector  
Norms, the adversarial attacks are also divided by their impact  
on the networks. Depending on the goals of the attacker, the  
designation is as follows:

- Confidence Reduction, the classifier outputs the original  
	label with less confidence;
- Untargeted, the classifier outputs any class besides the  
	original label;
- Targeted, the classifier outputs a particular class besides  
	the original label.  
	Another important aspect of adversarial attacks is the  
	amount of knowledge the attacker has access to. As defined by  
	Papernotet al.\[15\], who proposed the first threat model for  
	deep learning, the attackers can have access to: 1) data training  
	and network architecture; 2) only network architecture; 3)
```
TABLE I
COMMON TERMINOLOGIES USED IN THE CONTEXT OF ADVERSARIAL
ATTACKS AND THEIR DEFINITION.
Terminology Definition
Original/ Clean
Example Original image presented in a dataset
Adversarial/
Perturbed
Example
```
```
Image that an adversary has manipulated to fool
the classifier
Perturbation Set of changes (for each pixel and color channel)that are performed on the image
Adversarial At-
tack
```
```
Technique used to calculate the perturbation that
generates an adversarial example
Transferability
```
```
Capability of an adversarial example being
transferred from a known network to an un-
known network
White-box Attacks that have access to DNN weights anddatasets
Black-box Attacks that do not have access to the DNNweights and datasets
Adversarial
Training
```
```
Inclusion of adversarial examples in the training
phase of the model
```
```
only data training; 4) an oracle that replies to all the inputs
given; and 5) only have pairs of input and corresponding
output (samples). However, to simplify this classification, these
capacities were divided into:
```
- White-box, which considers that the attacker has access  
	to either the architecture or data;
- Black-box, when the attacker can only access samples  
	from an oracle or in pairs of input and output.  
	The attackers goals and capacity are essential to classify the  
	strength of an attack. For example, the easiest is a Confidence  
	Reduction White-box attack, and the strongest is a Targeted  
	Black-box attack.

##### III. RELATEDSURVEYS

```
The first attempt to summarize and display the recent
developments in this area was made by Akhtar and Mian [23].
These authors studied adversarial attacks in computer vision,
extensively referring to attacks for classification and providing
a brief overview of attacks beyond the classification problem.
Furthermore, the survey presents a set of attacks performed
in the real world and provides insight into the existence of
adversarial examples. Finally, the authors present the defenses
distributed through three categories: modified training or input,
modifying networks, and add-on networks.
From a broader perspective, Liuet al.[24] studied the secu-
rity threats and possible defenses in ML scope, considering the
different phases of an ML algorithm. For example, the training
phase is only susceptible to poisoning attacks; however, the
testing phase is vulnerable to evasion, impersonation, and
inversion attacks, making it harder to defend. The authors
provide their insight on the currently used techniques. Addi-
tionally, focusing more on the object recognition task, Serban
et al.[25] extensively analyzed the adversarial attacks and
defenses proposed under this context, providing conjectures
for the existence of adversarial examples and evaluating the
capacity of adversarial examples transferring between different
DNNs.
```
```
TABLE II
CHARACTERISTICS SHOWN IN STATE-OF-THE-ART SURVEYS ONADVERSARIALATTACKS.
```

Survey Year Black-BoxWhite & ComparisonSurvey Grouping ofDefenses DirectionsFuture OverviewDatasets ArchitecturesMetrics and State-of-the-artComparison TransformersVision  
Akhtar and Mian \[23\] 2018 X × XX ××××  
Qiuet al.\[26\] 2019 X ×××××××  
Serbanet al.\[25\] 2020 X × XX ××××  
Xuet al.\[27\] 2020 X × X ×××××  
Chakrabortyet al.\[28\] 2021 X ×××××××  
Longet al.\[29\] 2022 XX × X ××××  
Lianget al.\[30\] 2022 X × XX ××××  
Zhouet al.\[31\] 2022 X × XXX ×××  
This survey 2023 XXXXXXXX

Quiet al.\[26\] extensively explains background concepts in  
Adversarial Attacks, mentioning adversary goals, capabilities,  
and characteristics. It also displays applications for adversarial  
attacks and presents some of the most relevant adversarial  
defenses. Furthermore, it explains a set of attacks divided by  
the stage in which they occur, referring to the most relevant  
attacks.  
Xuet al.\[27\] also describes background concepts, describ-  
ing the adversary goals and knowledge. This review summa-  
rizes the most relevant adversarial attacks at the time of that  
work and presents physical world examples. Furthermore, the  
authors present a batch of defenses grouped by the underlying  
methodology. Finally, there is an outline of adversarial attacks  
in graphs, text, and audio networks, culminating in the possible  
applications of these attacks.  
Chakrabortyet al.\[28\] provides insight into commonly used  
ML algorithms and presents the adversary capabilities and  
goals. The presented adversarial attacks are divided based on  
the stage of the attack (train or test). Additionally, the authors  
present relevant defenses used in adversarial settings.  
Longet al.\[29\] discusses a set of preliminary concepts of  
Computer Vision and adversarial context, providing a set of  
adversarial attacks grouped by adversary goals and capabili-  
ties. Finally, the authors provide a set of research directions  
that readers can use to continue the development of robust  
networks.  
Lianget al.\[30\] discuss the most significant attacks and  
defenses in the literature, with the latter being grouped by the  
underlying technique. This review finishes with a presentation  
of the challenges currently existing in the adversarial context.  
More recently, Zhouet al.\[31\] provides insight into Deep  
Learning and Threat Models, focusing on the Cybersecurity  
perspective. Therefore, the authors identify multiple stages  
based on Advanced Persistent Threats and explain which  
adversarial attacks are adequate for each stage. Similarly,  
the same structure is followed to present the appropriate  
defenses for each stage. Furthermore, this survey presents the  
commonly used datasets in adversarial settings and provides  
a set of future directions from a Cybersecurity perspective.  
From the analysis of the previous surveys, some concepts  
have already been standardized, such as adversary goals and  
capabilities and the existence of adversarial attacks and de-  
fenses. However, due to the recent inception of this area, there  
still needs to be more standardization in datasets and metrics.  
Therefore, with this survey, we also analyze datasets and met-

```
rics to provide insight to novice researchers. Furthermore, this
survey consolidates the state-of-the-art results and identifies
which datasets can be further explored. Finally, similarly to
other reviews, this paper provides a set of future directions
that researchers and practitioners can follow to start their work.
A comparison between the several surveys discussed in this
section is summarized in Table II.
```

##### IV. ADVERSARIALATTACKS

```
Adversarial attacks are commonly divided by the amount
of knowledge the adversaries have access to, white-box and
black-box, as can be seen in Figure 5.
```
```
A. White-box Settings
Adversarial examples were first proposed by Szegedyet
al.[14], which discovered that DNNs do not generalize well in
the vicinity of an input. The same authors proposedL-BFGS,
the first adversarial attack, to create adversarial examples
and raised awareness in the scientific community for this
generalization problem.
Fast Gradient Sign Method(FGSM) [32] is a one-step
method to find adversarial examples, which is based on the
linear explanation for the existence of adversarial examples,
and is calculated using the model cost function, the gradient,
and the radius epsilon. This attack is formally defined as:
```
```
x−·sign(∇lossF,t(x)), (6)
```
```
wherexis the original image,is the amount of changes to
the image, andtis the target label. The value forshould be
very small to make the attack undetectable.
Jacobian-based Saliency Maps(JSM) [15] explore the for-
ward derivates to calculate the model gradients, replacing the
gradient descent approaches, and discover which input regions
are likely to yield adversarial examples. Then it uses saliency
maps to construct the adversarial saliency maps, which display
the features the adversary must perturb. Finally, to prove the
effectiveness of JSM, only the adversarial examples correctly
classified by humans were used to fool neural networks.
DeepFool[21] is an iterative attack that stops when the
minimal perturbation that alters the model output is found,
exploiting its decision boundaries. It finds the minimum pertur-
bation for an inputx 0 , corresponding to the vector orthogonal
to the hyperplane representing the decision boundary.
```

##### +

```
Adversarial
Attack
```

##### +

```
Adversarial
Attack
```
```
White-box Settings Black-box Settings
```
```
Target
Architecture
```

Fig. 5. Schematic overview of an Adversarial Attack under White-box Settings (left) and Black-box Settings (right). The first one uses the classifier predictions  
and network gradients to create perturbations (similar to noise), which can fool this classifier. These perturbations are added to the original images, creating  
adversarial images, which are fed to the network and cause misclassification. In the Black-box Settings, the same process is applied to a known classifier,  
and the obtained images are used to attack another classifier (represented as Target Architecture).

Kurakinet al.\[33\] was the first to demonstrate that adver-  
sarial examples can also exist in the physical world, by using  
three different methods to generate the adversarial examples.  
Basic Iterative Method(BIM) applies the FGSM multiple  
times with a small step size between iterations and clips  
the intermediate values after each step.Iterative Least-likely  
Class Method(ILCM) uses the least-likely class, according to  
the prediction of the model, as the target class and uses BIM to  
calculate the adversarial example that outputs the target class.  
Carlini and Wagner(C&W) \[34\] attack is one of the most  
powerful attacks, which uses three different vector norms: 1)  
theL 2 attack uses a smoothing of clipped gradient descent  
approach, displaying low distortion; 2) theL 0 attack uses  
an iterative algorithm that, at each iteration, fixes the pixels  
that do not have much effect on the classifier and finds  
the minimum amount of pixels that need to be altered; and

1. theL∞ attack also uses an iterative algorithm with an  
	associated penalty, penalizing every perturbation that exceeds  
	a predefined value, formally defined as:
```
min c·f(x+δ) +
```

##### ∑

```
i
```
```
[(δi−τ)+], (7)
```

whereδis the perturbation,τis the penalty threshold (initially  
1, decreasing in each iteration), andcis a constant. The value  
forcstarts as a very low value (e.g., 10 −^4 ), and each time the  
attack fails, the value forcis doubled. Ifcexceeds a threshold  
(e.g., 1010 ), it aborts the search.  
Gradient Aligned Adversarial Subspace(GAAS) \[35\] is  
an attack that directly estimates the dimensionality of the  
adversarial subspace using the first-order approximation of  
the loss function. Through the experiments, GAAS proved the  
most successful at finding many orthogonal attack directions,  
indicating that neural networks generalize linearly.  
Projected Gradient Descent(PGD) \[36\] is an iterative  
attack that uses saddle point formulation, viewed as an inner  
maximization problem and an outer minimization problem,  
to find a strong perturbation. It uses the inner maximization  
problem to find an adversarial version of a given input that

```
achieves a high loss and the outer minimization problem to
find model parameters that minimize the loss in the inner
maximization problem. The saddle point problem used by
PGD is defined as:
min
θ
ρ(θ),whereρ(θ) =E(x,y)∼D
```

##### \[

```
max
δ∈S
L(θ,x+δ,y)
```

##### \]

##### , (8)

```
wherexis the original image,yis the corresponding label,
andSis the set of allowed perturbations.
AdvGAN [37] uses Generative Adversarial Networks
(GAN) [38] to create adversarial examples that are realistic
and have high attack success rate. The generator receives the
original instance and creates a perturbation, the discriminator
distinguishes the original instance from the perturbed instance,
and the target neural network is used to measure the distance
between the prediction and the target class.
Motivated by the inability to achieve a high success rate
in black-box settings, theMomentum Iterative FGSM(MI-
FGSM) [39] was proposed. It introduces momentum, a tech-
nique for accelerating gradient descent algorithms, into the
already proposed Iterative FGSM (I-FGSM), showing that
the attack success rate in black-box settings increases almost
double that of previous attacks.
Croce and Hein [40] noted that the perturbations generated
byl 0 attacks are sparse and byl∞attacks are smooth on
all pixels, proposingSparse and Imperceivable Adversarial
Attacks(SIAA). This attack creates sporadic and impercep-
tible perturbations by applying the standard deviation of each
color channel in both axis directions, calculated using the two
immediate neighboring pixels and the original pixel.
SmoothFool(SF) [22] is a geometry-inspired framework
for computing smooth adversarial perturbations, exploiting
the decision boundaries of a model. It is an iterative algo-
rithm that uses DeepFool to calculate the initial perturbation
and smoothly rectifies the resulting perturbation until the
adversarial example fools the classifier. This attack provides
smoother perturbations which improve the transferability of
the adversarial examples, and their impact varies with the
different categories in a dataset.
```

In the context of exploring the adversarial examples in the  
physical world, theAdversarial Camouflage(AdvCam) \[41\],  
which crafts physical-world adversarial examples that are  
legitimate to human observers, was proposed. It uses the target  
image, region, and style to perform a physical adaptation  
(creating a realistic adversarial example), which is provided  
into a target neural network to evaluate the success rate of the  
adversarial example.  
Feature Importance-aware Attack(FIA) \[42\] considers  
the object-aware features that dominate the model decisions,  
using the aggregate gradient (gradients average concerning the  
feature maps). This approach avoids local optimum, repre-  
sents transferable feature importance, and uses the aggregate  
gradient to assign weights identifying the essential features.  
Furthermore, FIA generates highly transferable adversarial ex-  
amples when extracting the feature importance from multiple  
classification models.  
Meta Gradient Adversarial Attack(MGAA) \[43\] is a  
novel architecture that can be integrated into any existing  
gradient-based attack method to improve cross-model trans-  
ferability. This approach consists of multiple iterations, and,  
in each iteration, various models are samples from a model zoo  
to generate adversarial perturbations using the selected model,  
which are added to the previously generated perturbations.  
In addition, using multiple models simulates both white- and  
black-box settings, making the attacks more successful.

B. Universal Adversarial Perturbations

Moosavi-Dezfooliet al.\[44\] discovered that some perturba-  
tions are image-agnostic (universal) and cause misclassifica-  
tion with high probability, labeled asUniversal Adversarial  
Perturbations(UAPs). The authors found that these pertur-  
bations also generalize well across multiple neural networks,  
by searching for a vector of perturbations that cause misclas-  
sification in almost all the data drawn from a distribution of  
images. The optimization problem that Moosavi-Dezfooliet  
al.are trying to solve is the following:

```
∆vi←−argmin
r
‖r‖ 2 s.t. kˆ(xi+v+r) 6 =ˆk(xi), (9)
```

where∆viis the minimal perturbation to fool the classifier,  
vis the universal perturbation, andxiis the original image.  
This optimization problem is calculated for each image in a  
dataset, and the vector containing the universal perturbation is  
updated.  
The Universal Adversarial Networks (UAN) \[45\] are  
Generative Networks that are capable of fooling a classifier  
when their output is added to an image. These networks  
were inspired by the discovery of UAPs, which were used  
as the training set and can create perturbations for any given  
input, demonstrating more outstanding results than the original  
UAPs.

C. Black-box Settings

Specifically considering black-box setup, Ilyaset al.\[46\]  
define three realistic threat models that are more faithful  
to real-world settings: query-limited, partial information, and  
label-only settings. The first one suggests the development of

```
query-efficient algorithms, using Natural Evolutionary Strate-
gies to estimate the gradients used to perform the PGD attack.
When only having the probabilities for the top-k labels, the
algorithm alternates between blending in the original image
and maximizing the likelihood of the target class and, when
the attacker only obtains the top-k predicted labels, the attack
uses noise robustness to mount a targeted attack.
Feature-Guided Black-Box(FGBB) [47] uses the features
extracted from images to guide the creation of adversarial
perturbations, by using Scale Invariant Feature Transform.
High probability is assigned to pixels that impact the com-
position of an image in the Human visual system and the
creation of adversarial examples is viewed as a two-player
game, where the first player minimizes the distance to an
adversarial example, and the second one can have different
roles, leading to minimal adversarial examples.
Square Attack [48] is an adversarial attack that does
not need local gradient information, meaning that gradient
masking does not affect it. Furthermore, this attack uses a
randomized search scheme that selects localized square-shaped
updates in random positions, causing the perturbation to be
situated at the decision boundaries.
```
```
D. Auto-Attack
Auto-Attack [49] was proposed to test adversarial ro-
bustness in a parameter-free, computationally affordable, and
user-independent way. As such, Croceet al. proposed two
variations of PGD to overcome suboptimal step sizes of the
objective function, namely APGD-CE and APGD-DLR, for a
step size-free version of PGD using cross-entropy (CE) and
Difference of Logits Ratio (DLR) loss, respectively. DLR is a
loss proposed by Croceet al.which is both shift and rescaling
invariant and thus has the same degrees of freedom as the
decision of the classifier, not suffering from the issues of
the cross-entropy loss [49]. Then, they combine these new
PGD variations with two other existing attacks to create Auto-
Attack, which is composed by:
```
- APGD-CE, step size-free version of PGD on the cross-  
	entropy;
- APGD-DLR, step size-free version of PGD on the DLR  
	loss;
- Fast Adaptive Boundary (FAB) \[50\], which minimizes  
	the norm of the adversarial perturbations;
- Square \[48\] Attack, a query-efficient black-box attack.  
	Given the main motivation of the Auto-Attack proposal, the  
	FAB attack is the targeted version of FAB \[50\] since the  
	untargeted version computes each iteration of the Jacobian  
	matrix of the classifier, which scales linearly with the number  
	of classes of the dataset. Although this is feasible for datasets  
	with a low number of classes (e.g., MNIST and CIFAR-10), it  
	becomes both computationally and memory-wise challenging  
	with an increased number of classes (e.g., CIFAR-100 and  
	ImageNet).  
	As such, Auto-Attack is an ensemble of attacks with  
	important fundamental properties: APGD is a white-box at-  
	tack aiming at any adversarial example within anLp-ball  
	(Section II-C), FAB minimizes the norm of the perturbation

necessary to achieve a misclassification, and Square Attack is a  
score-based black-box attack for norm bounded perturbations  
which use random search and do not exploit any gradient  
approximation, competitive with white-box attacks \[48\].

##### V. ADVERSARIALDEFENSES

A. Adversarial Training

Szegedyet al.\[14\] proposed that training on a mixture  
of adversarial and clean examples could regularize a neural  
network, as shown in Figure 6. Goodfellowet al.\[32\] eval-  
uated the impact ofAdversarial Training as a regularizer  
by including it in the objective function, showing that this  
approach is a reliable defense that can be applied to every  
neural network.  
Kurakinet al.\[51\] demonstrates that it is possible to per-  
form adversarial training in more massive datasets (ImageNet),  
displaying that the robustness significantly increases for one-  
step methods. When training the model with one-step attacks  
using the ground-truth labels, the model has significantly  
higher accuracy on the adversarial images than on the clean  
images, an effect denominated asLabel Leaking, suggesting  
that the adversarial training should not make use of the ground-  
truth labels.  
Adversarial Training in large datasets implies using fast  
single-step methods, which converge to a degenerate global  
minimum, meaning that models trained with this technique  
remain vulnerable to black-box attacks. Therefore,Ensemble  
Adversarial Training\[52\] uses adversarial examples crafted  
on other static pre-trained models to augment the training data,  
preventing the trained model from influencing the strength of  
the adversarial examples.  
Shared Adversarial Training \[53\] is an extension of  
adversarial training aiming to maximize robustness against  
universal perturbations. It splits the mini-batch of images  
used in training into a set of stacks and obtains the loss  
gradients concerning these stacks. Afterward, the gradients  
for each stack are processed to create a shared perturbation  
that is applied to the whole stack. After every iteration, these  
perturbations are added and clipped to constrain them into a  
predefined magnitude. Finally, these perturbations are added  
to the images and used for adversarial training.  
TRadeoff-inspired Adversarial DEfense via Surrogate-  
loss minimization(TRADES) \[54\] is inspired by the pre-  
sumption that robustness can be at odds with accuracy \[55\],  
\[56\]. The authors show that the robust error can be tightly  
bounded by using natural error measured by the surrogate loss  
function and the likelihood of input features being close to the  
decision boundary (boundary error). These assumptions make  
the model weights biased toward natural or boundary errors.  
Based on the idea that gradient magnitude is directly  
linked to model robustness,Bilateral Adversarial Training  
(BAT) \[57\] proposes to perturb not only the images but also the  
manipulation of labels (adversarial labels) during the training  
phase. The adversarial labels are derived from a closed-form  
heuristic solution, and the adversarial images are generated  
from a one-step targeted attack.

```
Adversarial
Attack
```
```
Classifier
```
```
Adversarial
Images
```
```
Fig. 6. Schematic overview of Adversarial Training. A subset of the original
images of a dataset is fed into an adversarial attack (e.g., PGD, FGSM, or
C&W), which creates adversarial images. Each batch contains original and
adversarial images, with the Classifier being normally trained.
```
```
Despite the popularity of adversarial training to defend
models, it has a high cost of generating strong adversar-
ial examples, namely for large datasets such as ImageNet.
Therefore,Free Adversarial Training(Free-AT) [58] uses
the gradient information when updating model parameters to
generate the adversarial examples, eliminating the previously
mentioned overhead.
Considering the same issue presented in Free-AT, the au-
thors analyze Pontryagin’s Maximum Principle [59] of this
problem and observe that the adversary update is only related
to the first layer of the network. Thus,You Only Propagate
Once(YOPO) [60] only considers the first layer of the network
for forward and backpropagation, effectively reducing the
amount of propagation to one in each update.
Misclassification Aware adveRsarial Training
(MART) [61] is an algorithm that explicitly differentiates the
misclassified and correctly classified examples during training.
This proposal is motivated by the finding that different
maximization techniques are negligible, but minimization
ones are crucial when looking at the misclassified examples.
Defense against Occlusion Attacks(DOA) [62] is a de-
fense mechanism that uses abstract adversarial attacks, Rect-
angular Occlusion Attack (ROA) [62], and applies the standard
adversarial training. This attack considers including physically
realizable attacks that are “normal” in the real world, such as
eyeglasses and stickers on stop signs.
The proposal ofSmooth Adversarial Training(SAT) [63]
considers the evolution normally seen in curriculum learning,
where the difficulty increases with time (age), using two
difficulty metrics. These metrics are based on the maximal
Hessian eigenvalue (H-SAT) and the softmax Probability (P-
SAT), which are used to stabilize the networks for large pertur-
bations while having high clean accuracy. In the same context,
Friendly Adversarial Training(Friend-AT) [64] minimizes
the loss considering the least adversarial data (friendly) among
the adversarial data that is confidently misclassified. This
method can be employed by early stopping PGD attacks when
performing adversarial training.
Contrary to the idea of Free-AT [58],Cheap Adversarial
Training(Cheap-AT) [65] proposes the use of weaker and
cheaper adversaries (FGSM) combined with random initial-
ization to train robust networks effectively. This method can
be further accelerated by applying techniques that efficiently
train networks.
In a real-world context, the attacks are not limited by the
```

imperceptibility constraint (value); there are, in fact, multiple  
perturbations (for models) that have visible sizes. The main  
idea ofOracle-Aligned Adversarial Training(OA-AT) \[66\]  
is to create a model that is robust to high perturbation bounds  
by aligning the network predictions with ones of an Oracle  
during adversarial training. The key aspect of OA-AT is the use  
of Learned Perceptual Image Patch Similarity \[67\] to generate  
Oracle-Invariant attacks and convex combination of clean and  
adversarial predictions as targets for Oracle-Sensitive samples.  
Geometry-aware Instance-reweighted Adversarial  
Training (GI-AT) \[68\] has two foundations: 1) over-  
parameterized models still lack capacity; and 2) a natural data  
point closer to the class boundary is less robust, translating  
into assigning the corresponding adversarial data a larger  
weight. Therefore, this defense proposes using standard  
adversarial training, considering that weights are based on  
how difficult it is to attack a natural data point.  
Adversarial training leads to unfounded increases in the  
margin along decision boundaries, reducing clean accuracy.  
To tackle this issue, Helper-based Adversarial Training  
(HAT) \[69\] incorporates additional wrongly labeled examples  
during training, achieving a good trade-off between accuracy  
and robustness.  
As a result of the good results achieved by applying random  
initialization,Fast Adversarial Training(FAT) \[70\] performs  
randomized smoothing to optimize the inner maximization  
problem efficiently, and proposes a new initialization strategy,  
named backward smoothing. This strategy helps to improve  
the stability and robustness of a model using single-step robust  
training methods, solving the overfitting issue.

B. Modify the Training Process

Gu and Rigazio \[71\] proposed using three preprocessing  
techniques to recover from theadversarial noise, namely,  
noise injection, autoencoder, and denoising autoencoder, dis-  
covering that the adversarial noise is mainly distributed in  
the high-frequency domain. Solving the adversarial problem  
corresponds to encountering adequate training techniques and  
objective functions to increase the distortion of the smallest  
adversarial examples.  
Another defense against adversarial examples isDefensive  
Distillation\[72\], which uses the predictions from a previously  
trained neural network, as displayed in Figure 7. This approach  
trains the initial neural network with the original training  
data and labels, producing the probability of the predictions,  
which replace the original training labels to train a smaller  
and resilient distilled network. Additionally, to improve the  
results obtained by Defensive Distillation, Papernot and Mc-  
Daniel \[73\] propose to change the vector used to train the  
distilled network by combining the original label with the first  
model uncertainty.  
To solve the vulnerabilities of the neural network to adver-  
sarial examples, theVisual Causal Feature Learning\[74\]  
method uses causal reasoning to perform data augmentation.  
This approach uses manipulator functions that return an image  
similar to the original one with the desired causal effect.  
Learning with a Strong Adversary\[75\] is a training  
procedure that formulates as a min-max problem, making the

```
Initial Network
```
```
Network F
```
```
Vector Predictions F(X)
```
```
Training
Data X
```
```
Training
Labels Y
Distilled Network
```
```
Network F'
```
```
Vector Predictions F'(X)
```
```
Training
Data X
```
```
Training
Labels F(X)
```
```
Fig. 7. Method proposed by Defensive Distillation [72]. An Initial Network is
trained on the dataset images and labels (discrete values). Then, the predictions
given by the Initial Network are fed into another network, replacing the dataset
labels. These predictions are continuous values, making the Distilled Network
more resilient to adversarial attacks.
```
```
classifier inherently robust. This approach considers that the
adversary applies perturbations to each data point to maximize
the classification error, and the learning procedure attempts to
minimize the misclassification error against the adversary. The
greatest advantage of this procedure is the significant increase
in robustness while maintaining clean high accuracy.
Zhenget al.[76] proposes the use of compression, rescaling,
and cropping in benign images to increase the stability of
DNNs, denominated asImage Processing, without changing
the objective functions. A Gaussian perturbation sampler per-
turbs the benign image, which is fed to the DNN, and its
feature representation of benign images is used to 1) minimize
the standard CE loss; and 2) minimize the stability loss.
Zantedeschiet al.[77] explored the standard architectures,
which usually employ Rectified Linear Units (ReLU) [78],
[79] to ease the training process, and discovered that this
function makes a small perturbation in the input accumulate
with multiple layers (unbounded). Therefore, the authors pro-
pose the use of bounded ReLU (BReLU) [80] to prevent this
accumulation andGaussian Data Augmentationto perform
data augmentation.
Zhang and Wang [19] suggest that adversarial examples are
generated throughFeature Scattering(FS) in the latent space
to avoid the label leaking effect, which considers the inter-
example relationships. The adversarial examples are generated
by maximizing the feature-matching distance between the
clean and perturbed examples, FS produces a perturbed empir-
ical distribution, and the DNN performs standard adversarial
training.
PGD attack causes the internal representation to shift closer
to the “false” class,Triplet Loss Adversarial(TLA) [81]
includes an additional term in the loss function that pulls
natural and adversarial images of a specific class closer and
the remaining classes further apart. This method was tested
with different samples: Random Negative (TLA-RN), which
refers to a randomly sampled negative example, and Switch
Anchor (TLA-SA), which sets the anchor as a natural example
and the positive to be adversarial examples.
Kumari et al. [82] analyzes the previously adversarial-
trained models to test their vulnerability against adversarial
attacks at the level of latent layers, concluding that the latent
layer of these models is significantly vulnerable to adver-
sarial perturbations of small magnitude.Latent Adversarial
```

Training(LAT) \[82\] consists of finetuning adversarial-trained  
models to ensure robustness at the latent level.  
Curvature Regularization(CR) \[83\] minimizes the curva-  
ture of the loss surface, which induces a more ”natural” behav-  
ior of the network. The theoretical foundation behind this de-  
fense uses a locally quadratic approximation that demonstrates  
a strong relation between large robustness and small curvature.  
Furthermore, the proposed regularizer confirms the assumption  
that exhibiting quasi-linear behavior in the proximity of data  
points is essential to achieve robustness.  
Unsupervised Adversarial Training(UAT) \[84\] enables  
the training with unlabeled data considering two different  
approaches, UAT with Online Target (UAT-OT) that minimizes  
a differentiable surrogate of the smoothness loss, and UAT  
with Fixed Targets (UAT-FT) that trains an external classifier  
to predict the labels on the unsupervised data and uses its  
predictions as labels.  
Robust Self-Training(RST) \[85\], an extension of Self-  
Training \[86\], \[87\], uses a standard supervised training to  
obtain pseudo-labels and then feeds them into a supervised  
training algorithm that targets adversarial robustness. This ap-  
proach bridges the gap between standard and robust accuracy,  
using the unlabeled data, achieving high robustness using the  
same number of labels as required for high standard accuracy.  
SENSEI\[88\] andSENSEI-SA\[88\] use the methodologies  
employed in software testing to perform data augmentation,  
enhancing the robustness of DNNs. SENSEI implements the  
strategy of replacing each data point with a suitable variant or  
leaving it unchanged. SENSEI-SA improves the previous one  
by identifying which opportunities are suitable for skipping  
the augmentation process.  
Bit Plane Feature Consistency(BPFC) \[89\] regularizer  
forces the DNNs to give more importance to the higher bit  
planes, inspired by the Human visual system perception. This  
regularizer uses the original image and a preprocessed version  
to calculate thel 2 norm between them and regularize the loss  
function, as the scheme shown in Figure 8.  
Adversarial Weight Perturbation(AWP) \[90\] explicitly  
regularizes the flatness of weight loss landscape and robustness  
gap, using a double-perturbation mechanism that disturbs both  
inputs and weights. This defense boosts the robustness of  
multiple existing adversarial training methods, confirming that  
it can be applied to other methods.  
Self-Adaptive Training(SAT) \[91\] dynamically calibrates  
the training process with the model predictions without extra  
computational cost, improving the generalization of corrupted  
data. In contrast with the double-descent phenomenon, SAT  
exhibits a single-descent error-capacity curve, mitigating the  
overfitting effect.  
HYDRA\[92\] is another technique that explores the effects  
of pruning on the robustness of models, which proposes using  
pruning techniques that are aware of the robust training objec-  
tive, allowing this objective to guide the search for connections  
to prune. This approach reaches compressed models that are  
state-of-the-art in standard and robust accuracy.  
Based on the promising results demonstrated by previous  
distillation methods, the Robust Soft Label Adversarial  
Distillation(RSLAD) \[93\] method uses soft labels to train

```
Change
Loss
```
```
Regularizer
Quantization Shift
Noise Clip
```
```
Fig. 8. Schematic overview of the Bit Plane Feature Consistency [89]. This
method applies multiple operations to input images, simulating adversarial
images. Then, the loss is changed to include a regularizer (new term), which
compares the original images with these manipulated images.
```
```
robust small student DNNs. This method uses the Robust Soft
Labels (RSLs) produced by the teacher DNN to supervise
the student training on natural and adversarial examples. An
essential aspect of this method is that the student DNN does
not access the original complex labels through the training
process.
The most sensitive neurons in each layer make signifi-
cant non-trivial contributions to the model predictions under
adversarial settings, which means that increasing adversarial
robustness stabilizes the most sensitive neurons. Sensitive
Neuron Stabilizing(SNS) [94] includes an objective function
dedicated explicitly to maximizing the similarities of sensitive
neuron behaviors when providing clean and adversarial exam-
ples.
Dynamic Network Rewiring(DNR) [95] generates pruned
DNNs that have high robust and standard accuracy, which
employs a unified constrained optimization formulation using
a hybrid loss function that merges ultra-high model com-
pression with robust adversarial training. Furthermore, the
authors propose a one-shot training method that achieves high
compression, standard accuracy, and robustness, which has a
practical inference 10 times faster than traditional methods.
Manifold Regularization for Locally Stable(MRLS) [96]
DNNs exploit the continuous piece-wise linear nature of ReLU
to learn a function that is smooth over both predictions and
decision boundaries. This method is based on approximating
the graph Laplacian when the data is sparse.
Inspired by the motivation behind distillation,Learnable
Boundary Guided Adversarial Training (LBGAT) [97],
assuming that models trained on clean data embed their
most discriminative features, constrains the logits from the
robust model to make them similar to the model trained on
natural data. This approach makes the robust model inherit
the decision boundaries of the clean model, preserving high
standard and robust accuracy.
Low Temperature Distillation(LTD) [98], which uses pre-
vious distillation frameworks to generate labels, uses relatively
low temperatures in the teacher model and employs different
fixed temperatures for the teacher and student models. The
main benefit of this mechanism is that the generated soft labels
can be integrated into existing works without additional costs.
Recently, literature [99]–[101] demonstrated that neural Or-
dinary Differential Equations (ODE) are naturally more robust
to adversarial attacks than vanilla DNNs. Therefore,Stable
neural ODE for deFending against adversarial attacks
(SODEF) [102] uses optimization formulation to force the
```
```
Detector
Network No
```
```
Adversarial
Example?
Classifier
```

Fig. 9. Schematic overview of the Use of Supplementary Networks. The  
Detector Network was previously trained to detect adversarial images and is  
included between the input images and the classifier. This network receives  
the input images and determines if these images are Adversarial or Not. If they  
are not, they are redirected to the Classifier; If they are, they are susceptible  
to Human evaluation.

extracted feature points to be within the vicinity of Lyapunov-  
stable equilibrium points, which suppresses the input pertur-  
bations.  
Self-COnsistent Robust Error(SCORE) \[103\] employs  
local equivariance to describe the ideal behavior of a robust  
model, facilitating the reconciliation between robustness and  
accuracy while still dealing with worst-case uncertainty. This  
method was inspired by the discovery that the trade-off be-  
tween adversarial and clean accuracy imposes a bias toward  
smoothness.  
Analyzing the impact of activation shape on robustness, Dai  
et al.\[104\] observes that activation has positive outputs on  
negative inputs, and a high finite curvature can improve robust-  
ness. Therefore,Parametric Shifted Sigmoidal Linear Unit  
(PSSiLU) \[104\] combines these properties and parameterized  
activation functions with adversarial training.

C. Use of Supplementary Networks

MagNet\[105\] considers two reasons for the misclassifica-  
tion of an adversarial example: 1) incapacity of the classifier to  
reject an adversarial example distant from the boundary; and

1. classifier generalizes poorly when the adversarial example  
	is close to the boundary. MagNet considers multiple detectors  
	trained based on the reconstruction error, detecting signif-  
	icantly perturbed examples and detecting slightly perturbed  
	examples based on probability divergence.  
	Adversary Detection Network(ADN) \[106\] is a subnet-  
	work that detects if the input example is adversarial or not,  
	trained using adversarial images generated for a classification  
	network which are classified as clean (0) or adversarial (1).  
	Figure 9 displays a schematic overview of this network.  
	However, this defense mechanism deeply correlates to the  
	datasets and classification networks.  
	Xuet al.found that the inclusion ofFeature Squeezing  
	(FS) \[107\] is highly reliable in detecting adversarial examples  
	by reducing the search space available for the adversary to  
	modify. This method compares the predictions of a standard  
	network with a squeezed one, detecting adversarial examples  
	with high accuracy and having few false positives.  
	High-level representation Guided Denoiser(HGD) \[17\]  
	uses the distance between original and adversarial images to  
	guide an image denoiser and suppress the impact of adversarial  
	examples. HGD uses a Denoising AutoEncoder \[108\] with  
	additional lateral connections and considers the difference
```
between the representations as the loss function at a specific
layer that is activated by the normal and adversarial examples.
Defense-GAN[18] explores the use of GANs to effectively
represent the set of original training examples, making this
defense independent from the attack used. Defense-GAN
considers the usage of Wasserstein GANs (WGANs) [109]
to learn the representation of the original data and denoise the
adversarial examples, which start by minimizing thel 2 differ-
ence between the generator representation and the input image.
Reverse Attacks[110] can be applied to each attack during
the testing phase, by finding the suitable additive perturbation
to repair the adversarial example similar to the adversarial
attacks, which is highly difficult due to the unknown original
label.
Embedding Regularized Classifier(ER-Classifier) [111]
is composed of a classifier, an encoder, and a discriminator,
which uses the encoder to generate code vectors by reducing
the dimensional space of the inputs and the discriminator to
separate these vectors from the ideal code vectors (sampled
from a prior distribution). This technique allows pushing
adversarial examples into the benign image data distribution,
removing the adversarial perturbations.
Class Activation Feature-based Denoiser(CAFD) [112] is
a self-supervised approach trained to remove the noise from
adversarial examples, using a set of examples generated by
the Class Activation Feature-based Attack (CAFA) [112]. This
defense mechanism is trained to minimize the distance of the
class activation features between the adversarial and natural
examples, being robust to unseen attacks.
Detector Graph(DG) [113] considers graphs to detect the
adversarial examples by constructing a Latent Neighborhood
Graph (LNG) for each original example and using Graph
Neural Networks (GNNs) [114] to exploit the relationship and
distinguish between original and adversarial examples. This
method maintains an additional reference dataset to retrieve
the manifold information and uses embedding representation
of image pixel values, making the defense robust to unseen
attacks.
Images in the real world are represented in a continuous
manner, yet machines can only store these images in discrete
2D arrays.Local Implicit Image Function(LIIF) [115] takes
an image coordinate and the deep features around this coordi-
nate as inputs, predicting the corresponding RGB value. This
method of pre-processing input images can filter adversarial
images by reducing their perturbations, which are subsequently
fed to a classifier.
ADversarIal defenSe with local impliCit functiOns
(DISCO) [116] is an additional network to the classifier that
removes adversarial perturbations using localized manifold
projections, which receives an adversarial image and a query
pixel location. This defense mechanism comprises an encoder
that creates per-pixel deep features and a local implicit module
that uses these features to predict the clean RGB value.
```
```
D. Change Network Architecture
To identify the type of layers and their order, Guo et
al. [118] proposes the use of Neural Architecture Search
```

## +

### 1x

### Conv

### Mean

### Filter

### Non-local

### Means

### Bilateral

### Filter

### Median

### Filter

Fig. 10. Overview of a Feature Denoising Block \[117\], which can be included  
in the intermediate layers to make networks more robust. This method is an  
example of Change Network Architecture.

(NAS) to identify the networks that are more robust to  
adversarial attacks, finding that densely connected patterns  
improve the robustness and adding convolution operations to  
direct connection edge is effective, combined to create the  
RobNets\[118\].  
Feature Denoising\[117\] intends to address this problem  
by applying feature-denoising operations, consisting of non-  
local means, bilateral, mean, median filters, followed by 1x  
Convolution and an identity skip connection, as illustrated in  
Figure 10. These blocks are added to the intermediate layers  
of CNNs.  
Input Random\[119\] propose the addition of layers at the  
beginning of the classifier, consisting of 1) a random resizing  
layer, which resizes the width and height of the original image  
to a random width and height, and 2) a random padding  
layer, which pads zeros around the resized image in a random  
manner.  
Controlling Neural Level Sets(CNLS) \[120\] uses samples  
obtained from the neural level sets and relates their positions to  
the network parameters, which allows modifying the decision  
boundaries of the network. The relation between position and  
parameters is achieved by constructing a sample network with  
an additional single fixed linear layer, which can incorporate  
the level set samples into a loss function.  
Sparse Transformation Layer(STL) \[121\], included be-  
tween the input image and the network first layer, trans-  
forms the received images into a low-dimensional quasi-  
natural image space, which approximates the natural image  
space and removes adversarial perturbations. This creates an  
attack-agnostic adversarial defense that gets the original and  
adversarial images closer.  
Benzet al.\[122\] found that BN \[123\] and other normal-  
ization techniques make DNN more vulnerable to adversarial  
examples, suggesting the use of a framework that makes DNN  
more robust by learningRobust Featuresfirst and, then, Non-  
Robust Features (which are the ones learned when using BN).

E. Perform Network Validation

Most of the datasets store their images using the Joint  
Photographic Experts Group (JPEG) \[124\] compression, yet  
no one had evaluated the impact of this process on the network  
performance. Dziugaiteet al.\[125\] (named asJPG) varies the

```
magnitude of FGSM perturbations, discovering that smaller
ones often reverse the drop in classification by a large extent
and, when the perturbations increase in magnitude, this effect
is nullified.
Regarding formal verification, a tool [126] for automatic
Safety Verificationof the decisions made during the classifi-
cation process was created using Satisfiability Modulo Theory
(SMT). This approach assumes that a decision is safe when,
after applying transformations in the input, the model decision
does not change. It is applied to every layer individually in
the network, using a finite space of transformations.
DeepXplore[127] is the first white-box framework to per-
form a wide test coverage, introducing the concepts of neuron
coverage, which are parts of the DNN that are exercised by test
inputs. DeepXplore uses multiple DNNs as cross-referencing
oracles to avoid manual checking for each test input and
inputs that trigger different behaviors and achieve high neuron
coverage is a joint optimization problem solved by gradient-
based search techniques.
DeepGauge[128] intends to identify a testbed containing
multi-faceted representations using a set of multi-granularity
testing criteria. DeepGauge evaluates the resilience of DNNs
using two different strategies, namely, primary function and
corner-case behaviors, considering neuron- and layer-level
coverage criteria.
Surprise Adequacy for Deep Learning Systems
(SADL) [129] is based on the behavior of DNN on the training
data, by introducing the surprise of an input, which is the
difference between the DNN behavior when given the input
and the learned training data. The surprise of input is used as
an adequacy criterion (Surprise Adequacy), which is used as a
metric for the Surprise Coverage to ensure the input surprise
range coverage.
The most recent data augmentation techniques, such as
cutout [130] and mixup [131], fail to prevent overfitting
and, sometimes, make the model over-regularized, concluding
that, to achieve substantial improvements, the combination of
early stopping and semi-supervised data augmentation,Overfit
Reduction(OR) [132], is the best method.
When creating a model, multiple implementation details
influence its performance; Panget al.[133] is the first one
to provide insights on how these details influence the model
robustness, herein named as Bag of Tricks(BT). Some
conclusions drawn from this study are: 1) The robustness of
the models is significantly affected by weight decay; 2) Early
stopping of the adversarial attacks may deteriorate worst-case
robustness; and 3) Smooth activation benefits lower capacity
models.
Overfitting is a known problem that affects model robust-
ness; Rebuffiet al.[134] focuses on reducing this robust over-
fitting by using different data augmentation techniques.Fixing
Data Augmentation(FDA) [134] demonstrates that model
weight averaging combined with data augmentation schemes
can significantly increase robustness, which is enhanced when
using spatial composition techniques.
Gowal et al. [135] systematically studies the effect of
multiple training losses, model sizes, activation functions,
the addition of unlabeled data, and other aspects. The main
```

Adversarial Purified

```
Diffusion Denoising
```

Fig. 11. Overview of Adversarial Purification using Denoising Diffusion  
Probabilistic Models, adapted from \[137\]. The diffusion process is applied  
to an adversarial image, consisting of adding noise for a certain number of  
steps. During the denoising procedure, this noise is iteratively removed by the  
same amount of steps, resulting in a purified image (without perturbations).

conclusion drawn by this analysis is that larger models with  
Swish/SiLU \[136\] activation functions and model weight av-  
eraging can reliably achieve state-of-the-art results in robust  
accuracy.

F. Adversarial Purification

Adversarial Purification consists of defense mechanisms  
that remove adversarial perturbations using a generative  
model. Improving Robustness Using Generated Data  
(IRUGD) \[138\] explores how generative models trained on  
the original images can be leveraged to increase the size  
of the original datasets. Through extensive experiments,  
they concluded that Denoising Diffusion Probabilistic Models  
(DDPM) \[137\], a progression of diffusion probabilistic mod-  
els \[139\], is the model that more closely resembles real data.  
Figure 11 presents the main idea behind the DDPM process.  
Due to the great results in image synthesis displayed by the  
DDPM, Sehwaget al.\[140\] (Proxy) uses proxy distributions  
to significantly improve the performance of adversarial train-  
ing by generating additional examples, demonstrating that the  
best generative models for proxy distribution are DDPM.  
Inspired by previous works on adversarial purification \[141\],  
\[142\],DiffPure\[143\] uses DDPM for adversarial purification,  
receiving as input an adversarial example and recovering the  
clean image through a reverse generative process. Since this  
discovery, multiple improvements regarding the use of DDPM  
for Adversarial Purification have been studied.Guided Dif-  
fusion Model for Adversarial Purification(GDMAP) \[144\]  
receives as initial input pure Gaussian noise and gradually  
denoises it with guidance to an adversarial image.  
DensePure\[145\] employs iterative denoising to an input  
image, with different random seeds, to get multiple reversed  
samples, which are given to the classifier and the final  
prediction is based on majority voting. Furthermore, Wang  
et al.\[146\] uses the most recent diffusion models \[147\] to  
demonstrate that diffusion models with higher efficiency and  
image quality directly translate into better robust accuracy.

##### VI. ADVERSARIALEFFECTS ONVISIONTRANSFORMERS

Like CNNs \[148\], the ViTs are also susceptible to adver-  
sarial perturbations that alter a patch in an image \[149\], and  
ViTs demonstrate higher robustness, almost double, compared  
with ResNet-50 \[150\].

```
To further evaluate therobustness of ViTto adversarial
examples, Mahmoodet al.[151] used multiple adversarial
attacks in CNNs, namely FGSM, PGD, MIM, C&W, and
MI-FGSM. The ViT has increased robustness (compared with
ResNet) for the first four attacks and has no resilience to the
C&W and MI-FGSM attacks. Additionally, to complement the
results obtained from the performance of ViTs, an extensive
study [152] using feature maps, attention maps, and Gradient-
weighted Class Activation Mapping (Grad-CAM) [153] in-
tends to explain this performance visually.
The transferability of adversarial examples from CNNs to
ViTs was also evaluated, suggesting that the examples from
CNNs do not instantly transfer to ViTs [151]. Furthermore,
Self-Attention blended Gradient Attack(SAGA) [151] was
proposed to misclassify both ViTs and CNNs. ThePay No
Attention(PNA) [154] attack, which ignores the gradients
of attention, and thePatchOut[154] attack, which randomly
samples subsets of patches, demonstrate high transferability.
To detect adversarial examples that might affect the ViTs,
PatchVeto [20] uses different transformers with different
attention masks that output the encoding of the class. An image
is considered valid if all transformers reach a consensus in
the voted class, overall the masked predictions (provided by
masked transformers).
Smoothed ViTs[155] perform preprocessing techniques to
the images before feeding them into the ViT, by generating
image ablations (images composed of only one column of the
original image, and the remaining columns are black), which
are converted into tokens, and droping the fully masked tokens.
The remaining tokens are fed into a ViT, which predicts a class
for each ablation, and the class with the most predictions of
overall ablations is considered the correct one.
Baiet al. [156] demonstrates that ViTs and CNNs are
being unfairly evaluated because they do not have the same
training details. Therefore, this work provides a fair and in-
depth comparison between ViTs and CNNs, indicating that
ViTs are as vulnerable to adversarial perturbations as CNNs.
Architecture-oriented Transferable Attacking
(ATA) [157] is a framework that generates transferable
adversarial examples by considering the common
characteristics among different ViT architectures, such
as self-attention and image-embedding. Specifically, it
discovers the most attentional patch-wise regions significantly
influencing the model decision and searches pixel-wise
attacking positions using sensitive embedding perturbation.
Patch-fool[158] explores the perturbations that turn ViTs
more vulnerable learners than CNNs, proposing a dedicated
attack framework that fools the self-attention mechanism by
attacking a single patch with multiple attention-aware opti-
mization techniques. This attack mechanism demonstrates, for
the first time, that ViTs can be more vulnerable than CNNs if
attacked with proper techniques.
Guet al.[159] evaluates the robustness of ViT to patch-wise
perturbations, concluding that these models are more robust
to naturally corrupted patches than CNNs while being more
vulnerable to adversarially generated ones. Inspired by the
observed results, the authors propose a simpleTemperature
Scalingbased method that improves the robustness of ViTs.
```

Fig. 12. Images withdrew from the MNIST dataset \[162\] in the first five  
columns and from the Fashion-MNIST dataset \[163\] in the last five columns.  
The images were resized for better visualization.

Fig. 13. Images withdrew from the CIFAR-10 dataset \[164\] in the first five  
columns and from the CIFAR-100 dataset \[164\] in the last five columns. The  
images were resized for better visualization.

As previously observed for CNNs, improving the robust  
accuracy sacrifices the standard accuracy of ViTs, which may  
limit their applicability in the real context.Derandomized  
Smoothing\[160\] uses a progressive smoothed image mod-  
eling task to train the ViTs, making them capture the more  
discriminating local context while preserving global semantic  
information, improving both robust and standard accuracy.  
VeinGuard\[161\] is a defense framework that helps ViTs be  
more robust against adversarial palm-vein image attacks, with  
practical applicability in the real world. Namely, VeinGuard  
is composed of a local transformer-based GAN that learns  
the distribution of unperturbed vein images and a purifier that  
automatically removes a variety of adversarial perturbations.

```
VII. DATASETS
```

A. MNIST and F-MNIST

One of the most used datasets is theMNIST\[162\] dataset,  
which contains images of handwritten digits collected from  
approximately 250 writers in shades of black and white, with-  
drawn from two different databases. This dataset is divided  
into training and test sets, with the first one containing 60,  
examples and a second one containing 10,000 examples.  
Xiao et al. propose the creation of the Fashion-  
MNIST\[163\] dataset by using figures from a fashion website,  
which has a total size of 70,000 images, contains ten classes,  
uses greyscale images, and each image has a size of 28x28.  
The Fashion-MNIST dataset is divided into train and test sets,  
containing 60,000 and 10,000 examples, respectively.  
Fig. 12 displays the 10 digits (from 0 to 9) from the MNIST  
dataset in the first five columns and the 10 fashion objects from  
Fashion-MNIST dataset in the last five columns. MNIST is  
one of the most widely studied datasets in the earlier works  
of adversarial examples, with defense mechanisms already  
displaying high robustness on this dataset. The same does  
not apply to Fashion-MNIST, which has not been as widely  
studied, despite having similar characteristics to MNIST.

B. CIFAR-10 and CIFAR-

Another widely studied dataset is the CIFAR-10, which, in  
conjunction with the CIFAR-100 dataset, are subsets from a

```
Fig. 14. Images withdrew from the Street View House Numbers dataset [166]
in the first three columns and from the German Traffic Sign Recognition
Benchmark dataset [167] in the last three columns. The images were resized
for better visualization.
```
```
vast database containing 80 million tiny images [165], 32x32,
and three color channels 75,062 different classes.
CIFAR-10[164] contains only ten classes from this large
database, with 6,000 images for each class, distributed into
50,000 training images and 10,000 test images. This dataset
considers different objects, namely, animals and vehicles,
usually found in different environments.
CIFAR-100 [164] contains 100 classes with only 600
images for each one with the same size and amount of
color channels as the CIFAR-10 dataset. CIFAR-100 groups
its 100 classes into 20 superclasses, located in different
contexts/environments, making this dataset much harder to
achieve high results.
Examples from the CIFAR-10 dataset are shown in Fig. 13
in the first five columns, and the remaining columns display
examples of the superclasses from CIFAR-100. Due to the un-
satisfactory results demonstrated by models trained on CIFAR-
10, the CIFAR-100 dataset has not been included in most
studies under the context of adversarial examples, suggesting
that solving the issue of adversarial-perturbed images is still
at its inception.
```
```
C. Street View Datasets
TheStreet View House Numbers(SVHN) [166] dataset
provides the same challenge as MNIST: identifying which
digits are present in a colored image, containing ten classes,
0 to 9 digits, and an image size of 32x32 centered around
a single character, with multiple digits in a single image.
Regarding the dataset size, it has 630,420 digit images, but
only 73,257 images are used for training, 26,032 images are
used for testing, and the remaining 531,131 images can be
used as additional training data.
German Traffic Sign Recognition Benchmark (GT-
SRB) [167] is a dataset containing 43 classes of different traffic
signs, has 50,000 images, and demonstrates realistic scenarios.
The dataset has 51,840 images, whose size varies from 15x
to 222x193, divided into training, validation, and test sets with
50%, 25%, and 25%, respectively, of the total images.
The difficulties associated with the SVHN dataset are dis-
played in the first three rows of Fig. 14, showing unique
digits that occupy the whole image and multiple digits on
different backgrounds. Furthermore, the same figure presents
the different types of traffic signs in the GTSRB dataset, such
as prohibition, warning, mandatory, and end of prohibition.
```

Fig. 15. Images withdrew from the ImageNet dataset \[168\] in the top left, from the ImageNet-A dataset \[169\] in the top right, from the ImageNet-C and  
ImageNet-P datasets \[170\] in the bottom left, and ImageNet-COLORDISTORT \[171\] in the bottom right. The images were resized for better visualization.

D. ImageNet and Variants

ImageNet\[168\] is one of the largest datasets for object  
recognition, containing 1,461,406 colored images and 1,  
classes, with images being resized to 224x224. This dataset  
collected photographs from Flickr, and other search engines,  
divided into 1.2 million training images, 50,000 validation  
images, and 100,000 test images.  
A possible alternative to ImageNet, when the dataset size  
is an important factor, is called Tiny ImageNet \[172\], a  
subset of ImageNet that contains fewer classes and images.  
This dataset contains only 200 classes (from the 1,000 classes  
in ImageNet), 100,000 training images, 10,000 validation  
images, and 10,000 test images. These classes include animals,  
vehicles, household items, insects, and clothing, considering  
the variety of contexts/environments that these objects can be  
found. Their images have a size of 64x64 and are colored.  
ImageNet-A\[169\] is a subset of ImageNet, containing only  
200 classes from the 1,000 classes, covering the broadest  
categories in ImageNet. ImageNet-A is a dataset composed of  
real-world adversarially filtered images, which were obtained  
by deleting the correctly predicted images by ResNet-  
classifiers. Despite ImageNet-A being based on the deficiency  
of ResNet-50, it also demonstrates transferability to unseen  
models, making this dataset suitable for evaluating the robust-  
ness of multiple classifiers.  
Two additional benchmarks, ImageNet-C \[170\] and  
ImageNet-P\[170\], were designed to evaluate the robustness of  
DNNs. The ImageNet-C standardizes and expands the corrup-  
tion robustness topic, consisting of 75 corruptions applied to  
each image in the ImageNet validation set. ImageNet-P applies  
distortions to the images, though it differs from ImageNet-  
C because it contains perturbation sequences using only ten  
common perturbations.  
Another benchmark to evaluate the model generalization  
capability is theImageNet-COLORDISTORT(ImageNet-  
CD) \[171\], which considers multiple distortions in the color  
of an image using different color space representations. This  
dataset contains the 1,000 classes from ImageNet, removing  
images without color channels, and the same image considers  
multiple color distortions under the Red Green Blue (RGB),

```
TABLE III
RELEVANT CHARACTERISTICS TO THE CONTEXT OF ADVERSARIAL
EXAMPLES OF THE STATE-OF-THE-ART DATASETS.#CLASSESMEANS THE
NUMBER OF CLASSES IN THE DATASET. EMPTYCOLORCOLUMN MEANS
THAT THE IMAGES IN THAT DATASET USE GREYSCALE OR BLACK AND
WHITE SHADES. DATASETS WITH∗ARE ONLY USED FOR TESTING
PURPOSES.
Dataset Size #Classes Classes Color
MNIST 70,000 10 Digits
Fashion-MNIST 70,000 10 Clothing
```
```
CIFAR-10 60,000 10 AnimalsVehicles X
SVHN 630,420 10 Digits X
GTSRB 51,840 43 Traffic Signs X
```
```
CIFAR-100 60,000 100 Household ItemsOutdoor Scenes X
```

Tiny ImageNet 120,000 (^200) Household ItemsAnimals X  
ImageNet-A∗ 7,500 200 VehiclesFood X  
ImageNet-C∗ 3,750,000 200 VehiclesFood X  
ImageNet-P∗ 15,000,000 200 VehiclesFood X  
ImageNet 1,431,167 1,000 Electronic devicesVehicles X  
ImageNet-CD∗ 736,515 1,000 Electronic devicesVehicles X  
Hue-Saturation-Value (HSV), CIELAB, and YCbCr color  
spaces considered common transformations used in image  
processing.  
It is possible to observe a set of images withdrawn from  
ImageNet in the top left of Fig. 15. Additionally, some images  
misclassified by multiple classifiers (ImageNet-A) are shown  
in the top right of the same figure. The bottom represents  
the ImageNet with common corruptions and perturbations and  
is manipulated by multiple image techniques on the left and  
right, respectively. Table III summarizes the main characteris-  
tics of the datasets presented throughout this section.

```
TABLE IV
ACCURACY COMPARISON OF DIFFERENT DEFENSE MECHANISMS ON
CIFAR-10UNDERPGDATTACK,l∞AND=8/ 255. CLEAN AND
ROBUST REFERS TO ACCURACYWITHOUT ANDWITHADVERSARIAL
ATTACKS,RESPECTIVELY. DEFENSES WITH“-”ON CLEAN ACCURACY DO
NOT HAVE A CLEAN ACCURACY REPORTED.
```
```
Defense Method Year Architecture CleanAccuracyRobust
BPFC [89] 2020 ResNet-18 82.4 34.
SNS [94] 2021 VGG-16 86.0 39.
AT-MIFGSM [51] 2017 Inception v3 85.3 45.
AT-PGD [36] 2018 ResNet-18 87.3 47.
RobNets [118] 2020 RobNet-free 82.8 52.
HGD [17] 2018 DUNET 92.4 53.
RSLAD [93] 2021 ResNet-18 83.4 54.
MART [61] 2020 WRN-28-10 83.1 55.
TRADES [54] 2019 WRN-34-10 84.9 56.
BagT [133] 2020 WRN-34-10 - 56.
RO [132] 2020 ResNet-18 - 56.
DOA [62] 2019 VGGFace 93.6 61.
AWP [90] 2020 WRN-28-10 - 63.
FS [19] 2019 WRN-28-10 90.0 68.
CAFD [112] 2021 DUNET 91.1 87.
```

##### VIII. METRICS ANDSTATE-OF-THE-ARTRESULTS

A. Evaluation Metrics

Due to the nature of adversarial examples, they need specific  
metrics to be correctly evaluated and constructed. Following  
this direction, multiple works have been proposing different  
metrics that calculate the percentage of adversarial examples  
that make a model misclassify (fooling rate), measure the  
amount of perturbation made in an image (destruction rate),  
and calculate the model robustness to adversarial examples  
(average robustness).

1. Accuracy:This metric measures the number of samples  
	that are correctly predicted by the model, which is defined as:
```
accuracy=
```

##### TP+TN

##### TP+TN+FP+FN

##### , (10)

whereTPrefers to True Positive,TNto True Negative,FP  
to False Positive, andFNto False Negative. The True Positive  
and True Negative are the samples whose network prediction is  
the same as the label (correct), and the False Positive and False  
Negative are the samples whose network prediction differs  
from the label (incorrect). When considering original images,  
this metric is denominated asClean Accuracyand, when using  
adversarial images, is named asRobust Accuracy.

1. Fooling Rate: After being perturbed to change the  
	classifier label, the fooling rateFR\[173\] was proposed to  
	calculate the percentage of images.
2. Average Robustness:To objectively evaluate the robust-  
	ness to adversarial perturbations of a classifierf, the average  
	robustnesspˆadv(f)is defined as \[21\]:
```
pˆadv(f) =
```

##### 1

##### D

##### ∑

```
x∈D
```
```
‖ˆr(x)‖ 2
‖x‖ 2
```

##### , (11)

whererˆ(x)is the estimated minimal perturbation obtained  
using the attack, andDdenotes the test set.

```
TABLE V
ACCURACY COMPARISON OF DIFFERENT DEFENSE MECHANISMS ON
CIFAR-10UNDERAUTO-ATTACK ATTACK,l∞AND=8/ 255. CLEAN
ANDROBUST REFERS TO ACCURACYWITHOUT ANDWITHADVERSARIAL
ATTACKS,RESPECTIVELY.
```
```
Architecture Defense Method Year CleanAccuracyRobust
```
```
WRN28-
```
```
Input Random [119] 2017 94.3 8.
BAT [57] 2019 92.8 29.
FS [19] 2019 90.0 36.
Jpeg [125] 2016 83.9 50.
Pretrain [174] 2019 87.1 54.
UAT [84] 2019 86.5 56.
MART [61] 2020 87.5 56.
HYDRA [92] 2020 89.0 57.
RST [85] 2019 89.7 59.
GI-AT [68] 2020 89.4 59.
Proxy [140] 2021 89.5 59.
AWP [90] 2020 88.3 60.
FDA [134] 2021 87.3 60.
HAT [69] 2021 88.2 61.
SCORE [103] 2022 88.6 61.
PSSiLU [104] 2022 87.0 61.
Gowalet al.[135] 2020 89.5 62.
IRUGD [138] 2021 87.5 63.
Wanget al.[146] 2023 92.4 67.
STL [121] 2019 82.2 67.
DISCO [116] 2022 89.3 85.
```
```
WRN34-
```
```
Free-AT [58] 2019 86.1 41.
AT-PGD [36] 2018 87.1 44.
YOPO [60] 2019 87.2 44.
TLA [81] 2019 86.2 47.
LAT [82] 2019 87.8 49.
SAT [63] 2020 86.8 50.
FAT [70] 2022 85.3 51.
LBGAT [97] 2021 88.2 52.
TRADES [54] 2019 84.9 53.
SAT [91] 2020 83.5 53.
Friend-AT [64] 2020 84.5 55.
AWP [90] 2020 85.4 56.
LTD [98] 2021 85.2 56.
OA-AT [66] 2021 85.3 58.
Proxy [140] 2022 86.7 60.
HAT [69] 2021 91.5 62.
```
```
WRN-70-
```
```
SCORE [103] 2022 89.0 63.
IRUGD [138] 2021 91.1 65.
Gowalet al.[135] 2020 88.7 66.
FDA [134] 2021 92.2 66.
Wanget al.[146] 2023 93.3 70.
SODEF [102] 2021 93.7 71.
```
```
4) Destruction Rate: To evaluate the impact of arbitrary
transformations on adversarial images, the notion of destruc-
tion ratedis introduced and formally defined as [33]:
```
```
d=
```
```
∑n
k=1C(X
```
```
k,yk
true)¬C(X
k
adv,y
k
true)C(T(X
k
adv),y
k
∑ true)
n
k=1(X
```
```
k,yk
true)C(X
```
```
k
adv,y
k
true)
```

##### ,

##### (12)

```
wherenis the number of images,Xkis the original image
from the dataset,yktrueis the true class of this image,Xkadvis
the adversarial image corresponding to that image, andTis
an arbitrary image transformation.¬C(Xkadv,yktrue)is defined
as the binary negation ofC(Xkadv,yktrue). Finally, the function
C(X,y)is defined as [33]:
```
```
C(X,y) =
```

##### {

```
1 , if imageXis classified asy;
0 , otherwise.
```

##### (13)

TABLE VI  
ACCURACY COMPARISON OF DIFFERENT DEFENSE MECHANISMS ON  
CIFAR-100UNDERAUTO-ATTACK ATTACK,l∞AND=8/ 255. CLEAN  
ANDROBUST REFERS TO ACCURACYWITHOUT ANDWITHADVERSARIAL  
ATTACKS,RESPECTIVELY.

```
Architecture Defense Method Year CleanAccuracyRobust
```
```
WRN28-
```
```
Input Random [119] 2017 73.6 3.
LIIF [115] 2021 80.3 3.
Bit Reduction [107] 2017 76.9 3.
Pretrain [174] 2019 59.2 28.
SCORE [103] 2022 63.7 31.
FDA [134] 2021 62.4 32.
Wanget al.[146] 2023 78.6 38.
Jpeg [125] 2016 61.9 39.
STL [121] 2019 67.4 46.
DISCO [116] 2022 72.1 67.
```
```
WRN34-
```
```
SAT [63] 2020 62.8 24.
AWP [90] 2020 60.4 28.
LBGAT [97] 2021 60.6 29.
OA-AT [66] 2021 65.7 30.
LTD [98] 2021 64.1 30.
Proxy [140] 2022 65.9 31.
DISCO [116] 2022 71.6 69.
```
```
WRN-70-
```
```
SCORE [103] 2022 65.6 33.
FDA [134] 2021 63.6 34.
Gowalet al.[135] 2020 69.2 36.
Wanget al.[146] 2023 75.2 42.
```

B. Defense Mechanisms Robustness

The metric used to evaluate models is accuracy, which  
evaluates the results on both original (Clean Accuracy) and  
adversarially perturbed (Robust Accuracy) datasets. One of  
the earliest and strongest adversarial attacks proposed was  
PGD, which was used by multiple defenses to evaluate their  
robustness. Table IV displays defenses evaluated on CIFAR-  
10 under multiple steps PGD attack, ordered by increasing  
robustness. For the PGD attack, the best performing de-  
fenses are from approaches that use supplementary networks  
(CAFD) or modify the training process (FS and AWP).  
Overall, Wide ResNets \[175\] have better robust accuracy,  
due to high-capacity networks exhibiting greater adversarial  
robustness \[36\], \[51\], suggesting the usage of these networks  
in future developments of adversarial attacks and defenses.

To assess the robustness of defenses for white and black-  
box settings, Auto-Attack has gained increased interest over  
PGD in recent works. Tables V, VI, and VII present a set of  
defenses that are evaluated under Auto-Attack, on CIFAR-10,  
CIFAR-100, and ImageNet, respectively, ordered by increasing  
Robust Accuracy. The most used networks are Wide ResNets  
with different sizes, with the biggest Wide ResNet displaying  
better results overall, and the most resilient defense derives  
from the use of supplementary networks (DISCO), followed by  
modifying the train process (SODEF) and changing network  
architecture (STL). The results suggest that the inclusion of  
additional components to sanitize inputs of the targeted model  
(use of supplementary networks) is the most resilient approach  
for model robustness in white and black-box settings. The  
updated results for defenses under Auto-Attack can be found  
on the RobustBench \[176\] website.

```
TABLE VII
ACCURACY COMPARISON OF DIFFERENT DEFENSE MECHANISMS ON
IMAGENET UNDERAUTO-ATTACK ATTACK,l∞AND=4/ 255. CLEAN
ANDROBUST REFERS TO ACCURACYWITHOUT ANDWITHADVERSARIAL
ATTACKS,RESPECTIVELY.
```
```
Architecture Defense Method Year CleanAccuracyRobust
```
```
ResNet-
```
```
Bit Reduction [107] 2017 67.6 4.
Jpeg [125] 2016 67.2 13.
Input Random [119] 2017 64.0 17.
Salmanet al.[177] 2020 52.9 25.
STL [121] 2019 65.6 32.
DISCO [116] 2022 68.0 60.
```
```
ResNet-
```
```
Bit Reduction [107] 2017 73.8 1.
Input Random [119] 2017 74.0 18.
Cheap-AT [65] 2020 55.6 26.
Jpeg [125] 2016 73.6 33.
Salmanet al.[177] 2020 64.0 35.
STL [121] 2019 68.3 50.
DISCO [116] 2022 72.6 68.
```
```
WRN-50-
```
```
Bit Reduction [107] 2017 75.1 5.
Input Random [119] 2017 71.7 23.
Jpeg [125] 2016 75.4 24.
Salmanet al.[177] 2020 68.5 38.
DISCO [116] 2022 75.1 69.
```

##### IX. FUTUREDIRECTIONS

```
Following thede factostandards adopted by the literature,
we suggest that future proposals of defense mechanisms
should be evaluated on Auto-Attack, using the robust
accuracyas a metric for comparison purposes. The adver-
sarial defense that demonstrates better results isAdversarial
Training, which should be arequirement when evaluating
attacks and defenses.
The state-of-the-art results show that MNIST and CIFAR-
10 datasets are already saturated. Other datasets should be
further evaluated, namely: 1) CIFAR-100 and ImageNet
since adversarial defenses do not achieve state-of-the-art clean
accuracy (91% and 95%, respectively); 2) GTSRB and
SVHN, depicting harder scenarios with greater variations
of background, inclination, and luminosity; and 3)Fashion-
MNISTthat would allow better comprehension of which
image properties influence DNNs performance (e.g., type of
task, image shades, number of classes).
Most works present their results using accuracy as the
evaluation metric and, more recently, evaluate their defenses
on the Auto-Attack. Furthermore, the values given forin
each dataset were standardized by recurrent use. However,
there should be an effort todevelop a metric/process that
quantifies the amount of perturbation added to the original
image. This would ease the expansion of adversarial attacks
to other datasets that do not have a standardizedvalue.
There has been a greater focus on the development of white-
box attacks, which consider that the adversary has access
to the network and training data, yet this is not feasible in
real contexts, translating into the need offocusing more on
the development of black-box attacks. A unique black-box
set,physical attacks, also require additional evaluation,
considering the properties of the real world and perturbations
commonly found in it. Considering the increasing liberation
of ML in the real world, end-users can partially control the
```

training phase of DNNs, suggesting thatgray-box attacks will  
intensify(access only to network or data).  
The different network architectures are designed to increase  
the clean accuracy of DNNs in particular object recognition  
datasets, yet there should befurther evaluation on the impact  
of the different layers and their structure. ViTs introduce a  
new paradigm in image analysis and are more robust against  
natural corruptions, suggesting thatbuilding ViT inherently  
robust to adversarial examplesmight be a possible solution.  
DDPM are generative models that perform adversarial pu-  
rification of images, but they can not be applied in real-  
time since they take up to dozens of seconds to create a  
single purified image. Therefore, an effort ondeveloping close  
to real-time adversarial purification strategiesis a viable  
strategy for future works.

##### X. CONCLUSIONS

DNNs are vulnerable to a set of inputs, denominated  
as adversarial examples, that drastically modify the output  
of the considered network and are constructed by adding  
a perturbation to the original image. This survey presents  
background concepts, such as adversary capacity and vector  
norms, essential to comprehend adversarial settings, providing  
a comparison with existing surveys in the literature. Adversar-  
ial attacks are organized based on the adversary knowledge,  
highlighting the emphasis of current works toward white  
box settings, and adversarial defenses are clustered into six  
domains, with most works exploring the adversarial training  
strategy. We also present the latest developments of adversarial  
settings in ViTs and describe the commonly used datasets,  
providing the state-of-the-art results in CIFAR-10, CIFAR-  
100, and ImageNet. Finally, we propose a set of open issues  
that can be explored for subsequent future works.

##### ACKNOWLEDGMENTS

This work was supported in part by the Portuguese  
FCT/MCTES through National Funds and co-funded by EU  
funds under Project UIDB/50008/2020; in part by the FCT  
Doctoral Grant 2020.09847.BD and Grant 2021.04905.BD;

##### REFERENCES

```
[1] I. Goodfellow, Y. Bengio, and A. Courville,Deep learning. MIT press,
2016.
[2] L. Liu, W. Ouyang, X. Wang, P. Fieguth, J. Chen, X. Liu, and
M. Pietikainen, “Deep learning for generic object detection: A survey,” ̈
IJCV, vol. 128, no. 2, pp. 261–318, 2020.
[3] H.-B. Zhang, Y.-X. Zhang, B. Zhong, Q. Lei, L. Yang, J.-X. Du, and
D.-S. Chen, “A comprehensive survey of vision-based human action
recognition methods,”Sensors, vol. 19, no. 5, p. 1005, 2019.
[4] I. Masi, Y. Wu, T. Hassner, and P. Natarajan, “Deep face recognition:
A survey,” in2018 31st SIBGRAPI, pp. 471–478, IEEE, 2018.
[5] M. Wang and W. Deng, “Deep face recognition: A survey,”Neurocom-
puting, vol. 429, pp. 215–244, 2021.
[6] T. Wolf, L. Debut, V. Sanh, J. Chaumond, C. Delangue, A. Moi,
P. Cistac, T. Rault, R. Louf, M. Funtowicz,et al., “Transformers:
State-of-the-art natural language processing,” inProceedings of the
2020 conference on empirical methods in natural language processing:
system demonstrations, pp. 38–45, 2020.
[7] D. W. Otter, J. R. Medina, and J. K. Kalita, “A survey of the usages of
deep learning for natural language processing,”IEEE Transactions on
Neural Networks and Learning Systems, vol. 32, no. 2, pp. 604–624,
2020.
```
```
[8] A. I. Maqueda, A. Loquercio, G. Gallego, N. Garc ́ıa, and D. Scara-
muzza, “Event-based vision meets deep learning on steering prediction
for self-driving cars,” inProceedings of the IEEE Conference on CVPR,
June 2018.
[9] A. Ndikumana, N. H. Tran, D. H. Kim, K. T. Kim, and C. S. Hong,
“Deep learning based caching for self-driving cars in multi-access edge
computing,”IEEE Transactions on Intelligent Transportation Systems,
vol. 22, no. 5, pp. 2862–2877, 2021.
[10] Z. Yuan, Y. Lu, Z. Wang, and Y. Xue, “Droid-sec: Deep learning
in android malware detection,” inProceedings of the 2014 ACM
Conference on SIGCOMM, SIGCOMM ’14, (New York, NY, USA),
p. 371–372, Association for Computing Machinery, 2014.
[11] R. Vinayakumar, M. Alazab, K. P. Soman, P. Poornachandran, and
S. Venkatraman, “Robust intelligent malware detection using deep
learning,”IEEE Access, vol. 7, pp. 46717–46738, 2019.
[12] X. Zhou, W. Liang, I. Kevin, K. Wang, H. Wang, L. T. Yang, and Q. Jin,
“Deep-learning-enhanced human activity recognition for internet of
healthcare things,”IEEE Internet of Things Journal, vol. 7, no. 7,
pp. 6429–6438, 2020.
[13] Z. Liang, G. Zhang, J. X. Huang, and Q. V. Hu, “Deep learning for
healthcare decision making with emrs,” in2014 IEEE International
Conference on BIBM, pp. 556–559, IEEE, 2014.
[14] C. Szegedy, W. Zaremba, I. Sutskever, J. Bruna, D. Erhan, I. J.
Goodfellow, and R. Fergus, “Intriguing properties of neural networks,”
ArXiv, vol. abs/1312.6199, 2014.
[15] N. Papernot, P. McDaniel, S. Jha, M. Fredrikson, Z. B. Celik, and
A. Swami, “The limitations of deep learning in adversarial settings,”
in2016 IEEE EuroS&P, pp. 372–387, IEEE, 2016.
[16] Google, “Vertex ai pricing,” 2022. [Online] Accessed on 10th May
2023.
[17] F. Liao, M. Liang, Y. Dong, T. Pang, J. Zhu, and X. Hu, “Defense
against adversarial attacks using high-level representation guided de-
noiser,”2018 IEEE/CVF Conference on CVPR, pp. 1778–1787, 2018.
[18] P. Samangouei, M. Kabkab, and R. Chellappa, “Defense-gan: Protect-
ing classifiers against adversarial attacks using generative models,” in
International Conference on Learning Representations, 2018.
[19] H. Zhang and J. Wang, “Defense against adversarial attacks using
feature scattering-based adversarial training,” inNeurIPS, 2019.
[20] Y. Huang and Y. Li, “Zero-shot certified defense against adversarial
patches with vision transformers,”ArXiv, vol. abs/2111.10481, 2021.
[21] S.-M. Moosavi-Dezfooli, A. Fawzi, and P. Frossard, “Deepfool: A
simple and accurate method to fool deep neural networks,”2016 IEEE
Conference on CVPR, pp. 2574–2582, 2016.
[22] A. Dabouei, S. Soleymani, F. Taherkhani, J. M. Dawson, and N. M.
Nasrabadi, “Smoothfool: An efficient framework for computing smooth
adversarial perturbations,”2020 IEEE WACV, pp. 2654–2663, 2020.
[23] N. Akhtar and A. Mian, “Threat of adversarial attacks on deep learning
in computer vision: A survey,”IEEE Access, vol. 6, pp. 14410–14430,
2018.
[24] Q. Liu, P. Li, W. Zhao, W. Cai, S. Yu, and V. C. M. Leung, “A survey
on security threats and defensive techniques of machine learning: A
data driven view,”IEEE Access, vol. 6, pp. 12103–12117, 2018.
[25] A. Serban, E. Poll, and J. Visser, “Adversarial examples on ob-
ject recognition: A comprehensive survey,”ACM Computing Surveys,
vol. 53, no. 3, 2020.
[26] S. Qiu, Q. Liu, S. Zhou, and C. Wu, “Review of artificial intelligence
adversarial attack and defense technologies,”Applied Sciences, vol. 9,
no. 5, p. 909, 2019.
[27] H. Xu, Y. Ma, H.-C. Liu, D. Deb, H. Liu, J.-L. Tang, and A. K. Jain,
“Adversarial attacks and defenses in images, graphs and text: A review,”
International Journal of Automation and Computing, vol. 17, pp. 151–
178, 2020.
[28] A. Chakraborty, M. Alam, V. Dey, A. Chattopadhyay, and
D. Mukhopadhyay, “A survey on adversarial attacks and defences,”
CAAI Transactions on Intelligence Technology, vol. 6, no. 1, pp. 25–
45, 2021.
[29] T. Long, Q. Gao, L. Xu, and Z. Zhou, “A survey on adversarial attacks
in computer vision: Taxonomy, visualization and future directions,”
Computers & Security, p. 102847, 2022.
[30] H. Liang, E. He, Y. Zhao, Z. Jia, and H. Li, “Adversarial attack and
defense: A survey,”Electronics, vol. 11, no. 8, p. 1283, 2022.
[31] S. Zhou, C. Liu, D. Ye, T. Zhu, W. Zhou, and P. S. Yu, “Adversarial
attacks and defenses in deep learning: From a perspective of cyberse-
curity,”ACM Computing Surveys, vol. 55, no. 8, pp. 1–39, 2022.
[32] I. J. Goodfellow, J. Shlens, and C. Szegedy, “Explaining and harnessing
adversarial examples,”ArXiv, vol. abs/1412.6572, 2015.
```

\[33\] A. Kurakin, I. J. Goodfellow, and S. Bengio, “Adversarial examples in  
the physical world,”ArXiv, vol. abs/1607.02533, 2017.  
\[34\] N. Carlini and D. Wagner, “Towards evaluating the robustness of neural  
networks,” in2017 ieee symposium on sp, pp. 39–57, Ieee, 2017.  
\[35\] F. Tram\`er, N. Papernot, I. J. Goodfellow, D. Boneh, and P. Mc-  
daniel, “The space of transferable adversarial examples,”ArXiv,  
vol. abs/1704.03453, 2017.  
\[36\] A. Madry, A. Makelov, L. Schmidt, D. Tsipras, and A. Vladu, “To-  
wards deep learning models resistant to adversarial attacks,”ArXiv,  
vol. abs/1706.06083, 2018.  
\[37\] C. Xiao, B. Li, J.-Y. Zhu, W. He, M. Liu, and D. Song, “Generating  
adversarial examples with adversarial networks,” inProceedings of  
the 27th International Joint Conference on Artificial Intelligence,  
pp. 3905–3911, 2018.  
\[38\] I. J. Goodfellow, J. Pouget-Abadie, M. Mirza, B. Xu, D. Warde-Farley,  
S. Ozair, A. C. Courville, and Y. Bengio, “Generative adversarial nets,”  
inNIPS, 2014.  
\[39\] Y. Dong, F. Liao, T. Pang, H. Su, J. Zhu, X. Hu, and J. Li, “Boosting  
adversarial attacks with momentum,”2018 IEEE/CVF Conference on  
CVPR, pp. 9185–9193, 2018.  
\[40\] F. Croce and M. Hein, “Sparse and imperceivable adversarial attacks,”  
2019 IEEE/CVF ICCV, pp. 4723–4731, 2019.  
\[41\] R. Duan, X. Ma, Y. Wang, J. Bailey, A. K. Qin, and Y. Yang,  
“Adversarial camouflage: Hiding physical-world attacks with natural  
styles,”2020 IEEE/CVF Conference on Computer Vision and Pattern  
Recognition (CVPR), pp. 997–1005, 2020.  
\[42\] Z. Wang, H. Guo, Z. Zhang, W. Liu, Z. Qin, and K. Ren, “Feature  
importance-aware transferable adversarial attacks,” inProceedings of  
the IEEE/CVF ICCV, pp. 7639–7648, 2021.  
\[43\] Z. Yuan, J. Zhang, Y. Jia, C. Tan, T. Xue, and S. Shan, “Meta gradient  
adversarial attack,” inProceedings of the IEEE/CVF ICCV, pp. 7748–  
7757, 2021.  
\[44\] S.-M. Moosavi-Dezfooli, A. Fawzi, O. Fawzi, and P. Frossard, “Univer-  
sal adversarial perturbations,”2017 IEEE Conference on CVPR, pp. 86–  
94, 2017.  
\[45\] J. Hayes and G. Danezis, “Learning universal adversarial perturbations  
with generative models,”2018 IEEE SPW, pp. 43–49, 2018.  
\[46\] A. Ilyas, L. Engstrom, A. Athalye, and J. Lin, “Black-box adversarial  
attacks with limited queries and information,” inInternational Confer-  
ence on Machine Learning, pp. 2137–2146, PMLR, 2018.  
\[47\] M. Wicker, X. Huang, and M. Kwiatkowska, “Feature-guided black-  
box safety testing of deep neural networks,” inTACAS, 2018.  
\[48\] M. Andriushchenko, F. Croce, N. Flammarion, and M. Hein, “Square  
attack: a query-efficient black-box adversarial attack via random  
search,” inComputer Vision – ECCV 2020, pp. 484–501, Springer,

\[49\] F. Croce and M. Hein, “Reliable evaluation of adversarial robustness  
with an ensemble of diverse parameter-free attacks,” inInternational  
conference on machine learning, pp. 2206–2216, PMLR, 2020.  
\[50\] F. Croce and M. Hein, “Minimally distorted adversarial examples  
with a fast adaptive boundary attack,” inInternational Conference on  
Machine Learning, pp. 2196–2205, PMLR, 2020.  
\[51\] A. Kurakin, I. J. Goodfellow, and S. Bengio, “Adversarial machine  
learning at scale,”ArXiv, vol. abs/1611.01236, 2017.  
\[52\] F. Tram\`er, A. Kurakin, N. Papernot, I. Goodfellow, D. Boneh, and  
P. McDaniel, “Ensemble adversarial training: Attacks and defenses,”  
inInternational Conference on Learning Representations, 2018.  
\[53\] C. K. Mummadi, T. Brox, and J. H. Metzen, “Defending against uni-  
versal perturbations with shared adversarial training,”2019 IEEE/CVF  
ICCV, pp. 4927–4936, 2019.  
\[54\] H. Zhang, Y. Yu, J. Jiao, E. Xing, L. El Ghaoui, and M. Jordan,  
“Theoretically principled trade-off between robustness and accuracy,”  
inInternational conference on machine learning, pp. 7472–7482,  
PMLR, 2019.  
\[55\] D. Tsipras, S. Santurkar, L. Engstrom, A. Turner, and A. Madry, “Ro-  
bustness may be at odds with accuracy,” inInternational Conference  
on Learning Representations, 2019.  
\[56\] D. Su, H. Zhang, H. Chen, J. Yi, P.-Y. Chen, and Y. Gao, “Is robustness  
the cost of accuracy?–a comprehensive study on the robustness of  
18 deep image classification models,” inProceedings of the ECCV,  
pp. 631–648, 2018.  
\[57\] J. Wang and H. Zhang, “Bilateral adversarial training: Towards fast  
training of more robust models against adversarial attacks,” inPro-  
ceedings of the IEEE/CVF ICCV, pp. 6629–6638, 2019.  
\[58\] A. Shafahi, M. Najibi, M. A. Ghiasi, Z. Xu, J. Dickerson, C. Studer,  
L. S. Davis, G. Taylor, and T. Goldstein, “Adversarial training for free!,”  
Advances in Neural Information Processing Systems, vol. 32, 2019.

```
[59] R. E. Kopp, “Pontryagin maximum principle,” inMathematics in
Science and Engineering, vol. 5, pp. 255–279, Elsevier, 1962.
[60] D. Zhang, T. Zhang, Y. Lu, Z. Zhu, and B. Dong, “You only prop-
agate once: Accelerating adversarial training via maximal principle,”
Advances in Neural Information Processing Systems, vol. 32, 2019.
[61] Y. Wang, D. Zou, J. Yi, J. Bailey, X. Ma, and Q. Gu, “Improving
adversarial robustness requires revisiting misclassified examples,” in
International Conference on Learning Representations, 2020.
[62] T. Wu, L. Tong, and Y. Vorobeychik, “Defending against phys-
ically realizable attacks on image classification,” arXiv preprint
arXiv:1909.09552, 2019.
[63] C. Sitawarin, S. Chakraborty, and D. Wagner, “Improving ad-
versarial robustness through progressive hardening,”arXiv preprint
arXiv:2003.09347, vol. 4, no. 5, 2020.
[64] J. Zhang, X. Xu, B. Han, G. Niu, L. Cui, M. Sugiyama, and M. Kankan-
halli, “Attacks which do not kill training make adversarial learning
stronger,” inInternational conference on machine learning, pp. 11278–
11287, PMLR, 2020.
[65] E. Wong, L. Rice, and J. Z. Kolter, “Fast is better than free: Revisiting
adversarial training,”arXiv preprint arXiv:2001.03994, 2020.
[66] S. Addepalli, S. Jain, G. Sriramanan, S. Khare, and V. B. Radhakr-
ishnan, “Towards achieving adversarial robustness beyond perceptual
limits,” inICML 2021 Workshop on Adversarial Machine Learning,
2021.
[67] R. Zhang, P. Isola, A. A. Efros, E. Shechtman, and O. Wang, “The
unreasonable effectiveness of deep features as a perceptual metric,” in
Proceedings of the IEEE conference on CVPR, pp. 586–595, 2018.
[68] J. Zhang, J. Zhu, G. Niu, B. Han, M. Sugiyama, and M. Kankan-
halli, “Geometry-aware instance-reweighted adversarial training,”arXiv
preprint arXiv:2010.01736, 2020.
[69] R. Rade and S.-M. Moosavi-Dezfooli, “Helper-based adversarial train-
ing: Reducing excessive margin to achieve a better accuracy vs.
robustness trade-off,” inICML 2021 Workshop on Adversarial Machine
Learning, 2021.
[70] J. Chen, Y. Cheng, Z. Gan, Q. Gu, and J. Liu, “Efficient robust training
via backward smoothing,” inProceedings of the AAAI Conference on
Artificial Intelligence, vol. 36, pp. 6222–6230, 2022.
[71] S. S. Gu and L. Rigazio, “Towards deep neural network architectures
robust to adversarial examples,”ArXiv, vol. abs/1412.5068, 2015.
[72] N. Papernot, P. Mcdaniel, X. Wu, S. Jha, and A. Swami, “Distillation
as a defense to adversarial perturbations against deep neural networks,”
2016 IEEE Symposium on SP, pp. 582–597, 2016.
[73] N. Papernot and P. Mcdaniel, “Extending defensive distillation,”ArXiv,
vol. abs/1705.05264, 2017.
[74] K. Chalupka, P. Perona, and F. Eberhardt, “Visual causal feature
learning,” inUAI, 2015.
[75] R. Huang, B. Xu, D. Schuurmans, and C. Szepesvari, “Learning with
a strong adversary,”ArXiv, vol. abs/1511.03034, 2015.
[76] S. Zheng, Y. Song, T. Leung, and I. J. Goodfellow, “Improving the
robustness of deep neural networks via stability training,”2016 IEEE
Conference on CVPR, pp. 4480–4488, 2016.
[77] V. Zantedeschi, M.-I. Nicolae, and A. Rawat, “Efficient defenses
against adversarial attacks,”Proceedings of the 10th ACM Workshop
on Artificial Intelligence and Security, 2017.
[78] A. F. Agarap, “Deep learning using rectified linear units (relu),”ArXiv,
vol. abs/1803.08375, 2018.
[79] R. H. Hahnloser, R. Sarpeshkar, M. A. Mahowald, R. J. Douglas, and
H. S. Seung, “Digital selection and analogue amplification coexist in
a cortex-inspired silicon circuit,”Nature, vol. 405, no. 6789, pp. 947–
951, 2000.
[80] S. S. Liew, M. Khalil-Hani, and R. Bakhteri, “Bounded activation
functions for enhanced training stability of deep neural networks
on visual pattern recognition problems,”Neurocomputing, vol. 216,
pp. 718–734, 2016.
[81] C. Mao, Z. Zhong, J. Yang, C. Vondrick, and B. Ray, “Metric learning
for adversarial robustness,”Advances in Neural Information Processing
Systems, vol. 32, 2019.
[82] N. Kumari, M. Singh, A. Sinha, H. Machiraju, B. Krishnamurthy, and
V. N. Balasubramanian, “Harnessing the vulnerability of latent layers in
adversarially trained models,” inProceedings of the 28th International
Joint Conference on Artificial Intelligence, pp. 2779–2785, 2019.
[83] S.-M. Moosavi-Dezfooli, A. Fawzi, J. Uesato, and P. Frossard, “Ro-
bustness via curvature regularization, and vice versa,” inProceedings
of the IEEE/CVF Conference on CVPR, pp. 9078–9086, 2019.
[84] J.-B. Alayrac, J. Uesato, P.-S. Huang, A. Fawzi, R. Stanforth, and
P. Kohli, “Are labels required for improving adversarial robustness?,”
Advances in Neural Information Processing Systems, vol. 32, 2019.
```

\[85\] Y. Carmon, A. Raghunathan, L. Schmidt, J. C. Duchi, and P. S. Liang,  
“Unlabeled data improves adversarial robustness,”Advances in neural  
information processing systems, vol. 32, 2019.  
\[86\] H. Scudder, “Probability of error of some adaptive pattern-recognition  
machines,”IEEE Transactions on Information Theory, vol. 11, no. 3,  
pp. 363–371, 1965.  
\[87\] J. Cohen, E. Rosenfeld, and Z. Kolter, “Certified adversarial robustness  
via randomized smoothing,” ininternational conference on machine  
learning, pp. 1310–1320, PMLR, 2019.  
\[88\] X. Gao, R. K. Saha, M. R. Prasad, and A. Roychoudhury, “Fuzz  
testing based data augmentation to improve robustness of deep neural  
networks,”2020 IEEE/ACM 42nd ICSE, pp. 1147–1158, 2020.  
\[89\] S. Addepalli, S. VivekB., A. Baburaj, G. Sriramanan, and R. V.  
Babu, “Towards achieving adversarial robustness by enforcing feature  
consistency across bit planes,”2020 IEEE/CVF CVPR, pp. 1017–1026,

\[90\] D. Wu, S.-T. Xia, and Y. Wang, “Adversarial weight perturbation helps  
robust generalization,”Advances in Neural Information Processing  
Systems, vol. 33, pp. 2958–2969, 2020.  
\[91\] L. Huang, C. Zhang, and H. Zhang, “Self-adaptive training: beyond  
empirical risk minimization,”Advances in neural information process-  
ing systems, vol. 33, pp. 19365–19376, 2020.  
\[92\] V. Sehwag, S. Wang, P. Mittal, and S. Jana, “Hydra: Pruning ad-  
versarially robust neural networks,”Advances in Neural Information  
Processing Systems, vol. 33, pp. 19655–19666, 2020.  
\[93\] B. Zi, S. Zhao, X. Ma, and Y.-G. Jiang, “Revisiting adversarial  
robustness distillation: Robust soft labels make student better,” in  
Proceedings of the IEEE/CVF ICCV, pp. 16443–16452, 2021.  
\[94\] C. Zhang, A. Liu, X. Liu, Y. Xu, H. Yu, Y. Ma, and T. Li, “Interpreting  
and improving adversarial robustness of deep neural networks with  
neuron sensitivity,”IEEE Transactions on Image Processing, vol. 30,  
pp. 1291–1304, 2021.  
\[95\] S. Kundu, M. Nazemi, P. A. Beerel, and M. Pedram, “Dnr: A tunable  
robust pruning framework through dynamic network rewiring of dnns,”  
inProceedings of the 26th Asia and South Pacific Design Automation  
Conference, pp. 344–350, 2021.  
\[96\] C. Jin and M. Rinard, “Manifold regularization for locally stable deep  
neural networks,”arXiv preprint arXiv:2003.04286, 2020.  
\[97\] J. Cui, S. Liu, L. Wang, and J. Jia, “Learnable boundary guided ad-  
versarial training,” inProceedings of the IEEE/CVF ICCV, pp. 15721–  
15730, 2021.  
\[98\] E.-C. Chen and C.-R. Lee, “Ltd: Low temperature distillation for robust  
adversarial training,”arXiv preprint arXiv:2111.02331, 2021.  
\[99\] H. Yan, J. Du, V. Y. Tan, and J. Feng, “On robustness of neural ordinary  
differential equations,”arXiv preprint arXiv:1910.05513, 2019.  
\[100\] E. Haber and L. Ruthotto, “Stable architectures for deep neural  
networks,”Inverse problems, vol. 34, no. 1, p. 014004, 2017.  
\[101\] X. Liu, T. Xiao, S. Si, Q. Cao, S. Kumar, and C.-J. Hsieh, “How does  
noise help robustness? explanation and exploration under the neural sde  
framework,” inProceedings of the IEEE/CVF Conference on CVPR,  
pp. 282–290, 2020.  
\[102\] Q. Kang, Y. Song, Q. Ding, and W. P. Tay, “Stable neural ode with  
lyapunov-stable equilibrium points for defending against adversarial  
attacks,”Advances in Neural Information Processing Systems, vol. 34,  
pp. 14925–14937, 2021.  
\[103\] T. Pang, M. Lin, X. Yang, J. Zhu, and S. Yan, “Robustness and  
accuracy could be reconcilable by (proper) definition,” inInternational  
Conference on Machine Learning, pp. 17258–17277, PMLR, 2022.  
\[104\] S. Dai, S. Mahloujifar, and P. Mittal, “Parameterizing activation func-  
tions for adversarial robustness,” in2022 IEEE SPW, pp. 80–87, IEEE,

\[105\] D. Meng and H. Chen, “Magnet: A two-pronged defense against adver-  
sarial examples,”Proceedings of the 2017 ACM SIGSAC Conference  
on Computer and Communications Security, 2017.  
\[106\] J. H. Metzen, T. Genewein, V. Fischer, and B. Bischoff, “On detecting  
adversarial perturbations,” 2017.  
\[107\] W. Xu, D. Evans, and Y. Qi, “Feature squeezing: Detecting adversarial  
examples in deep neural networks,”arXiv preprint arXiv:1704.01155,

\[108\] P. Vincent, H. Larochelle, Y. Bengio, and P.-A. Manzagol, “Extracting  
and composing robust features with denoising autoencoders,” inICML  
’08, 2008.  
\[109\] M. Arjovsky, S. Chintala, and L. Bottou, “Wasserstein gan,”ArXiv,  
vol. abs/1701.07875, 2017.  
\[110\] C. Mao, M. Chiquier, H. Wang, J. Yang, and C. Vondrick, “Adversarial  
attacks are reversible with natural supervision,” inProceedings of the  
IEEE/CVF ICCV, pp. 661–671, 2021.

```
[111] Y. Li, M. R. Min, T. Lee, W. Yu, E. Kruus, W. Wang, and C.-J. Hsieh,
“Towards robustness of deep neural networks via regularization,” in
Proceedings of the IEEE/CVF ICCV, pp. 7496–7505, October 2021.
[112] D. Zhou, N. Wang, C. Peng, X. Gao, X. Wang, J. Yu, and T. Liu,
“Removing adversarial noise in class activation feature space,” in
Proceedings of the IEEE/CVF ICCV, pp. 7878–7887, 2021.
[113] A. Abusnaina, Y. Wu, S. Arora, Y. Wang, F. Wang, H. Yang, and
D. Mohaisen, “Adversarial example detection using latent neighbor-
hood graph,” inProceedings of the IEEE/CVF ICCV, pp. 7687–7696,
October 2021.
[114] F. Scarselli, M. Gori, A. C. Tsoi, M. Hagenbuchner, and G. Monfardini,
“The graph neural network model,”IEEE Transactions on Neural
Networks, vol. 20, no. 1, pp. 61–80, 2009.
[115] Y. Chen, S. Liu, and X. Wang, “Learning continuous image repre-
sentation with local implicit image function,” inProceedings of the
IEEE/CVF conference on CVPR, pp. 8628–8638, 2021.
[116] C.-H. Ho and N. Vasconcelos, “Disco: Adversarial defense with local
implicit functions,” inAdvances in Neural Information Processing
Systems(S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho,
and A. Oh, eds.), vol. 35, pp. 23818–23837, Curran Associates, Inc.,
2022.
[117] C. Xie, Y. Wu, L. van der Maaten, A. L. Yuille, and K. He, “Fea-
ture denoising for improving adversarial robustness,”2019 IEEE/CVF
Conference on CVPR, pp. 501–509, 2019.
[118] M. Guo, Y. Yang, R. Xu, and Z. Liu, “When nas meets robustness:
In search of robust architectures against adversarial attacks,” 2020
IEEE/CVF Conference on CVPR, pp. 628–637, 2020.
[119] C. Xie, J. Wang, Z. Zhang, Z. Ren, and A. Yuille, “Mitigating
adversarial effects through randomization,” inInternational Conference
on Learning Representations, 2018.
[120] M. Atzmon, N. Haim, L. Yariv, O. Israelov, H. Maron, and Y. Lip-
man, “Controlling neural level sets,”Advances in Neural Information
Processing Systems, vol. 32, 2019.
[121] B. Sun, N.-h. Tsai, F. Liu, R. Yu, and H. Su, “Adversarial defense by
stratified convolutional sparse coding,” inProceedings of the IEEE/CVF
Conference on CVPR, pp. 11447–11456, 2019.
[122] P. Benz, C. Zhang, and I. S. Kweon, “Batch normalization increases
adversarial vulnerability: Disentangling usefulness and robustness of
model features,”ArXiv, vol. abs/2010.03316, 2020.
[123] S. Ioffe and C. Szegedy, “Batch normalization: Accelerating deep
network training by reducing internal covariate shift,” inInternational
conference on machine learning, pp. 448–456, PMLR, 2015.
[124] W. F. Good, G. S. Maitz, and D. Gur, “Joint photographic experts
group (jpeg) compatible data compression of mammograms,”Journal
of Digital Imaging, vol. 7, no. 3, pp. 123–132, 1994.
[125] G. K. Dziugaite, Z. Ghahramani, and D. M. Roy, “A study of the
effect of jpg compression on adversarial images,” arXiv preprint
arXiv:1608.00853, 2016.
[126] X. Huang, M. Kwiatkowska, S. Wang, and M. Wu, “Safety verification
of deep neural networks,” inCAV, 2017.
[127] K. Pei, Y. Cao, J. Yang, and S. S. Jana, “Deepxplore: Automated
whitebox testing of deep learning systems,”Proceedings of the 26th
Symposium on Operating Systems Principles, 2017.
[128] L. Ma, F. Juefei-Xu, F. Zhang, J. Sun, M. Xue, B. Li, C. Chen, T. Su,
L. Li, Y. Liu, J. Zhao, and Y. Wang, “Deepgauge: Multi-granularity
testing criteria for deep learning systems,”2018 33rd IEEE/ACM
International Conference on ASE, pp. 120–131, 2018.
[129] J. Kim, R. Feldt, and S. Yoo, “Guiding deep learning system testing
using surprise adequacy,”2019 IEEE/ACM 41st ICSE, pp. 1039–1049,
2019.
[130] T. DeVries and G. W. Taylor, “Improved regularization of convolutional
neural networks with cutout,”arXiv preprint arXiv:1708.04552, 2017.
[131] H. Zhang, M. Cisse, Y. N. Dauphin, and D. Lopez-Paz, “mixup: Beyond
empirical risk minimization,” inInternational Conference on Learning
Representations, 2018.
[132] L. Rice, E. Wong, and Z. Kolter, “Overfitting in adversarially robust
deep learning,” inInternational Conference on Machine Learning,
pp. 8093–8104, PMLR, 2020.
[133] T. Pang, X. Yang, Y. Dong, H. Su, and J. Zhu, “Bag of tricks for
adversarial training,”arXiv preprint arXiv:2010.00467, 2020.
[134] S.-A. Rebuffi, S. Gowal, D. A. Calian, F. Stimberg, O. Wiles, and
T. Mann, “Fixing data augmentation to improve adversarial robustness,”
arXiv preprint arXiv:2103.01946, 2021.
[135] S. Gowal, C. Qin, J. Uesato, T. Mann, and P. Kohli, “Uncovering
the limits of adversarial training against norm-bounded adversarial
examples,”arXiv preprint arXiv:2010.03593, 2020.
```

\[136\] S. Elfwing, E. Uchibe, and K. Doya, “Sigmoid-weighted linear units  
for neural network function approximation in reinforcement learning,”  
Neural Networks, vol. 107, pp. 3–11, 2018.  
\[137\] J. Ho, A. Jain, and P. Abbeel, “Denoising diffusion probabilistic  
models,”Advances in Neural Information Processing Systems, vol. 33,  
pp. 6840–6851, 2020.  
\[138\] S. Gowal, S.-A. Rebuffi, O. Wiles, F. Stimberg, D. A. Calian, and  
T. A. Mann, “Improving robustness using generated data,”Advances  
in Neural Information Processing Systems, vol. 34, pp. 4218–4233,

\[139\] J. Sohl-Dickstein, E. Weiss, N. Maheswaranathan, and S. Ganguli,  
“Deep unsupervised learning using nonequilibrium thermodynamics,”  
inInternational Conference on Machine Learning, pp. 2256–2265,  
PMLR, 2015.  
\[140\] V. Sehwag, S. Mahloujifar, T. Handina, S. Dai, C. Xiang, M. Chiang,  
and P. Mittal, “Robust learning meets generative models: Can proxy  
distributions improve adversarial robustness?,” inInternational Confer-  
ence on Learning Representations, 2022.  
\[141\] C. Shi, C. Holtz, and G. Mishne, “Online adversarial purification based  
on self-supervised learning,” inInternational Conference on Learning  
Representations, 2021.  
\[142\] J. Yoon, S. J. Hwang, and J. Lee, “Adversarial purification with score-  
based generative models,” inInternational Conference on Machine  
Learning, pp. 12062–12072, PMLR, 2021.  
\[143\] W. Nie, B. Guo, Y. Huang, C. Xiao, A. Vahdat, and A. Anandkumar,  
“Diffusion models for adversarial purification,” inInternational Con-  
ference on Machine Learning, pp. 16805–16827, PMLR, 2022.  
\[144\] Q. Wu, H. Ye, and Y. Gu, “Guided diffusion model for adversarial  
purification from random noise,”arXiv e-prints, pp. arXiv–2206, 2022.  
\[145\] C. Xiao, Z. Chen, K. Jin, J. Wang, W. Nie, M. Liu, A. Anandkumar,  
B. Li, and D. Song, “Densepure: Understanding diffusion models to-  
wards adversarial robustness,”arXiv preprint arXiv:2211.00322, 2022.  
\[146\] Z. Wang, T. Pang, C. Du, M. Lin, W. Liu, and S. Yan, “Better  
diffusion models further improve adversarial training,”arXiv preprint  
arXiv:2302.04638, 2023.  
\[147\] T. Karras, M. Aittala, T. Aila, and S. Laine, “Elucidating the design  
space of diffusion-based generative models,” inAdvances in Neural  
Information Processing Systems(A. H. Oh, A. Agarwal, D. Belgrave,  
and K. Cho, eds.), 2022.  
\[148\] A. Krizhevsky, I. Sutskever, and G. E. Hinton, “Imagenet classification  
with deep convolutional neural networks,” inAdvances in Neural  
Information Processing Systems(F. Pereira, C. J. C. Burges, L. Bottou,  
and K. Q. Weinberger, eds.), vol. 25, Curran Associates, Inc., 2012.  
\[149\] M. Naseer, K. Ranasinghe, S. H. Khan, M. Hayat, F. S. Khan,  
and M. Yang, “Intriguing properties of vision transformers,”ArXiv,  
vol. abs/2105.10497, 2021.  
\[150\] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image  
recognition,”ArXiv, vol. abs/1512.03385, 2015.  
\[151\] K. Mahmood, R. Mahmood, and M. van Dijk, “On the robustness of  
vision transformers to adversarial examples,” inProceedings of the  
IEEE/CVF ICCV, pp. 7838–7847, October 2021.  
\[152\] A. Aldahdooh, W. Hamidouche, and O. Deforges, “Reveal of vi- ́  
sion transformers robustness against adversarial attacks,” ArXiv,  
vol. abs/2106.03734, 2021.  
\[153\] R. R. Selvaraju, M. Cogswell, A. Das, R. Vedantam, D. Parikh, and  
D. Batra, “Grad-cam: Visual explanations from deep networks via  
gradient-based localization,” inProceedings of the IEEE ICCV, Oct

\[154\] Z. Wei, J. Chen, M. Goldblum, Z. Wu, T. Goldstein, and Y. Jiang, “To-  
wards transferable adversarial attacks on vision transformers,”ArXiv,  
vol. abs/2109.04176, 2021.  
\[155\] H. Salman, S. Jain, E. Wong, and A. Madry, “Certified patch robustness  
via smoothed vision transformers,”ArXiv, vol. abs/2110.07719, 2021.  
\[156\] Y. Bai, J. Mei, A. L. Yuille, and C. Xie, “Are transformers more robust  
than cnns?,”Advances in Neural Information Processing Systems,  
vol. 34, pp. 26831–26843, 2021.  
\[157\] Y. Wang, J. Wang, Z. Yin, R. Gong, J. Wang, A. Liu, and X. Liu,  
“Generating transferable adversarial examples against vision transform-  
ers,” inProceedings of the 30th ACM International Conference on  
Multimedia, pp. 5181–5190, 2022.  
\[158\] Y. Fu, S. Zhang, S. Wu, C. Wan, and Y. Lin, “Patch-fool: Are  
vision transformers always robust against adversarial perturbations?,”  
inInternational Conference on Learning Representations, 2022.  
\[159\] J. Gu, V. Tresp, and Y. Qin, “Are vision transformers robust to patch  
perturbations?,” inComputer Vision – ECCV 2022, pp. 404–421,  
Springer, 2022.

```
[160] Z. Chen, B. Li, J. Xu, S. Wu, S. Ding, and W. Zhang, “Towards prac-
tical certifiable patch defense with vision transformer,” inProceedings
of the IEEE/CVF Conference on CVPR, pp. 15148–15158, 2022.
[161] Y. Li, S. Ruan, H. Qin, S. Deng, and M. A. El-Yacoubi, “Transformer
based defense gan against palm-vein adversarial attacks,”IEEE Trans-
actions on Information Forensics and Security, vol. 18, pp. 1509–1523,
2023.
[162] Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner, “Gradient-based
learning applied to document recognition,”Proceedings of the IEEE,
vol. 86, no. 11, pp. 2278–2324, 1998.
[163] H. Xiao, K. Rasul, and R. Vollgraf, “Fashion-mnist: a novel im-
age dataset for benchmarking machine learning algorithms,”ArXiv,
vol. abs/1708.07747, 2017.
[164] A. Krizhevsky, G. Hinton,et al., “Learning multiple layers of features
from tiny images,” 2009.
[165] A. Torralba, R. Fergus, and W. T. Freeman, “80 million tiny images: A
large data set for nonparametric object and scene recognition,”IEEE
Transactions on Pattern Analysis and Machine Intelligence, vol. 30,
no. 11, pp. 1958–1970, 2008.
[166] Y. Netzer, T. Wang, A. Coates, A. Bissacco, B. Wu, and A. Y. Ng,
“Reading digits in natural images with unsupervised feature learning,”
inNIPS Workshop on Deep Learning and Unsupervised Feature
Learning 2011, 2011.
[167] J. Stallkamp, M. Schlipsing, J. Salmen, and C. Igel, “Man vs. computer:
Benchmarking machine learning algorithms for traffic sign recogni-
tion,”Neural networks, vol. 32, pp. 323–332, 2012.
[168] O. Russakovsky, J. Deng, H. Su, J. Krause, S. Satheesh, S. Ma,
Z. Huang, A. Karpathy, A. Khosla, M. Bernstein,et al., “Imagenet large
scale visual recognition challenge,”IJCV, vol. 115, no. 3, pp. 211–252,
2015.
[169] D. Hendrycks, K. Zhao, S. Basart, J. Steinhardt, and D. Song, “Natural
adversarial examples,” inProceedings of the IEEE/CVF Conference on
CVPR, pp. 15262–15271, June 2021.
[170] D. Hendrycks and T. Dietterich, “Benchmarking neural network ro-
bustness to common corruptions and perturbations,” inInternational
Conference on Learning Representations, 2019.
[171] K. De and M. Pedersen, “Impact of colour on robustness of deep neural
networks,” in2021 IEEE/CVF International Conference on Computer
Vision Workshops (ICCVW), pp. 21–30, 2021.
[172] Y. Le and X. Yang, “Tiny imagenet visual recognition challenge,”CS
231N, vol. 7, no. 7, p. 3, 2015.
[173] Z. Huan, Y. Wang, X. Zhang, L. Shang, C. Fu, and J. Zhou, “Data-free
adversarial perturbations for practical black-box attack,” inPacific-Asia
conference on knowledge discovery and data mining, pp. 127–138,
Springer, 2020.
[174] D. Hendrycks, K. Lee, and M. Mazeika, “Using pre-training can im-
prove model robustness and uncertainty,” inInternational Conference
on Machine Learning, pp. 2712–2721, PMLR, 2019.
[175] S. Zagoruyko and N. Komodakis, “Wide residual networks,” inBritish
Machine Vision Conference 2016, British Machine Vision Association,
2016.
[176] F. Croce, M. Andriushchenko, V. Sehwag, E. Debenedetti, N. Flammar-
ion, M. Chiang, P. Mittal, and M. Hein, “Robustbench: a standardized
adversarial robustness benchmark,” inThirty-fifth Conference on Neu-
ral Information Processing Systems Datasets and Benchmarks Track
(Round 2), 2021.
[177] H. Salman, A. Ilyas, L. Engstrom, A. Kapoor, and A. Madry, “Do
adversarially robust imagenet models transfer better?,”Advances in
Neural Information Processing Systems, vol. 33, pp. 3533–3545, 2020.
```