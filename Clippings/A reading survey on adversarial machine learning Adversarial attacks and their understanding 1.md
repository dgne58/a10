---
title: "A reading survey on adversarial machine learning: Adversarial attacks and their understanding"
source: "https://pdf2md.morethan.io/"
author:
published:
created: 2026-04-15
description: "Converts PDF files to Markdown."
tags:
  - "clippings"
---
## A reading survey on adversarial machine learning:

## Adversarial attacks and their understanding\*

## Shashank Kotyan

```
Laboratory of Intelligent Systems
Department of Information Science and Engineerng
Kyushu University, Fukuoka, Japan
Student ID: 2IE21054M; email: kotyan.shashank.651@s.kyushu-u.ac.jp
```
```
Abstract—Deep Learning has empowered us to train neural
networks for complex data with high performance. However,
with the growing research, several vulnerabilities in neural
networks have been exposed. A particular branch of research,
Adversarial Machine Learning, exploits and understands some
of the vulnerabilities that cause the neural networks to
misclassify for near original input. A class of algorithms called
adversarial attacks is proposed to make the neural networks
misclassify for various tasks in different domains. With the
extensive and growing research in adversarial attacks, it is
crucial to understand the classification of adversarial attacks.
This will help us understand the vulnerabilities in a systematic
order and help us to mitigate the effects of adversarial attacks.
This article provides a survey of existing adversarial attacks and
their understanding based on different perspectives. We also
provide a brief overview of existing adversarial defences and
their limitations in mitigating the effect of adversarial attacks.
Further, we conclude with a discussion on the future research
directions in the field of adversarial machine learning.
```
```
Index Terms—Adversarial Attacks, Adversarial Defences,
Evasion Attacks, Poisoning Attacks, Optimisation
```
```
I. INTRODUCTION
```

## N

```
EURAL networks have enabled us to obtain
high performance in several applications across different
domains like speech and text recognition (Natural Language
Processing) and face, object and person recognition
(Computer Vision). Most of these applications are only
feasible with the assistance of neural networks either as a
feature extractor for other machine learning methods or a
classifier/detector on their own.
However, despite their high performance against
non-corrupted data, neural networks have been shown to
misclassify critical adversarial samples in which perturbations
(corruptions) are added to the original samples. Adversarial
samples are noise-perturbed samples that can fail neural
networks for tasks like image classification [1], text
classification [2], sound classification [3], and medical mole
identifcation [4].
It was exhibited in [5] that neural networks behave oddly
for almost the same images. Afterwards, in [6], the authors
demonstrated that neural networks show high confidence when
presented with textures and random noise. This exposure led
*Submitted as Term Project for Machine Learning Systems Engineering
Course.
```
```
to discovering a series of vulnerabilities in neural networks,
which were then exploited by using adversarial samples created
by a particular class of algorithms known as adversarial attacks
[6]–[9].
From Universal perturbations, [8] that can be added to almost
any image to generate an adversarial sample, to the addition
of crafted patches [7] or in fact, even the addition of one-
pixel [9] was also shown to cause networks to be enough to
misclassify. Since they were discovered by [5] some years
ago, both the quality and diversity of adversarial specimens
have developed. A timeline of the development of adversarial
attacks (and samples) is shown in Figure 1.
These adversarial samples exhibit that conventional neural
network architectures cannot understand concepts or
high-level abstractions as we earlier speculated. Further, these
adversarial attacks point out shortcomings in the reasoning of
current machine learning algorithms. Thus, exposing our
limited understanding of the working of a neural network.
Also, we cannot explain the reason for predicting
misclassified classes for the adversarial samples.
Security and safety risks were also created by these
adversarial attacks, which prohibits the use of neural networks.
Most of these adversarial attacks can also be transformed into
real-world attacks [11]–[14], which confer a big issue as well
as a security risk for current neural networks’ applications
such as in autonomous vehicles.
Many of these attacks can easily be made into real-world
threats by printing out adversarial samples, as shown in [12].
Moreover, carefully crafted glasses can also be made into
attacks [11]. Alternatively, even general 3D adversarial objects
were shown possible [13].
In fact, it was shown that by placing a few small stickers
on the ground in an intersection, researchers showed that they
could cause a self-driving car to make an abnormal judgment
and move into the opposite lane of traffic [15]. Also, placing a
few pieces of tape can deceive a computer vision system into
wrongly classifying a stop sign as a speed limit sign [14].
Despite the existence of many variants of defences to these
adversarial attacks [1], [16]–[26], no known learning algorithm
or procedure can defend consistently [27]–[32]. This shows
that a more profound understanding of the adversarial attacks
is needed to formulate consistent and robust defences.
Several works have focused on understanding the reasoning
```

## arXiv:2308.03363v1 \[cs.LG\] 7 Aug 2023

```
Fig. 1. Timeline of adversarial attacks and samples in adversarial machine learning, compared to work on the security of deep networks [10].
```

behind such a lack of robust performance. It is hypothesised in  
\[16\] that neural networks’ linearity is one of the main reasons  
for failure. Other investigation by \[33\] shows that with deep

```
learning, neural networks learn false structures that are simpler
to learn rather than the ones expected.
In [34], it is discussed that an adversarial sample may have
a different interpretation of learned features than the benign
```
```
Fig. 2. Visualisation of formal definition for Neural Network
```

sample. The authors show that learned features of adversarial  
samples are remarkably similar to different images of different  
true-class and links adversarial robustness to features learned  
by deep neural networks. Moreover, research by \[35\] unveil  
that adversarial attacks are altering where the algorithm is  
paying attention.  
The field of adversarial machine learning has contributed  
towards the development of some tools which could be helpful  
in the development of assessment for robustness. However, the  
sheer number of scenarios: attacking methods, defences, and  
metrics, make the current state-of-the-art difficult to perceive.  
It turns out that a simple robustness assessment is a daunting  
task, given the vast amount of possibilities and definitions  
along with their exceptions and trade-offs.  
However, most recent adversarial attacks and defences are  
white-box which can not be used to assess hybrids, non-standard  
neural networks and other classifiers in general and limit us  
in exploring the cases for our understanding. Improvements  
in robustness should also result in learning systems that can  
better reason over data and achieve a new level of abstraction.  
To better understand the adversarial attacks, here we  
provide a survey of adversarial attacks and their  
understanding. We classify the adversarial attacks based on  
the knowledge available to adversarial attacks, goals of  
adversarial attack, the scope of the adversarial attack, the  
strategy employed by the adversarial attack, optimisation used  
by adversarial attack, and constraints on perturbation imposed  
by adversarial attacks.

II. FORMAL DEFINITION OF ADVERSARIAL SAMPLES  
Let us suppose that for the image classification problem,  
xPRmˆnˆcbe the image^1 which is to be classified. Here

(^1) Here, we use the example image forx; however, the definition can be  
extended to other domains like text, and speech.  
m,nis the image’s width and height, andcis the number of  
colour channels.  
A neural network comprises several neural layers composed  
of perceptrons (artificial neurons) linked together. Each of  
these perceptrons maps a set of inputs to output values with  
an activation function.  
Thus, function of the neural network (formed by a chain)  
can be defined as:  
gpxq “fpkqp...fp^2 qpfp^1 qpxqqq (1)  
wherefpiqis the function of theith layer of the network,  
wherei“ 1, 2, 3,...,kandkis the last layer of the neural  
network as shown in Figure 2. In the image classification  
problem,gpxq PRNis the probabilities (confidence) for all  
the availableNclasses.  
Also, in adversarial machine learning, adversarial samples  
xˆare defined as:  
xˆ“x\`εx  
tˆxPRmˆnˆ^3 |argmaxrgpxqs ‰argmaxrgpxˆqsu

### (2)

```
in whichεxis the perturbation added to the input.
```
```
III. NON-EXHAUSTIVE CLASSIFICATION OF ADVERSARIAL
ATTACKS
There exist diverse types of adversarial attacks; in order to
classify these several types, we employ classification of
adversarial attacks from eleven different perspectives as
shown in Figure 3. An elaborate discussion on the different
classifications follows,
```
```
A. Based on available knowledge to adversarial attacks
‚WHITE-BOXATTACK(FULLKNOWLEDGE):In this kind
of adversarial attack, the adversary has all the information
about the model used, i.e., its architecture, all the individual
layer parameters, and training dataset as shown in Figure 4.
This case scenario is helpful to understand the effect of
adversarial perturbations caused by the internal parameters.
However, we have little to no knowledge of the model in the
real-case scenario, making this kind of attack useful only for
academic research purposes to understand the model better.
This setting allows one to perform a worst-case evaluation of
the security of learning algorithms, providing empirical upper
bounds on the performance degradation that may be incurred
by the system under attack.
‚GREY-BOXATTACK(LIMITEDKNOWLEDGE): In this
kind of adversarial attack, the adversary has some but not all
knowledge of the model, i.e., either its architecture and/or
some layer parameters.
This case scenario helps understand the relationship between the
feature extractor (usually convolution network) and the classifier
(usually fully connected network) parts. This understanding
then can be used in segregating the feature extraction and
classification, which is helpful for transfer learning.
However, in most scenarios, the grey-box attack is proposed
to be more potent and transferable than the white-box attack.
Similar to white-box attacks, we have little use of these attacks
```
```
Fig. 3. Classification of adversarial attacks from different perspectives.
```
```
in the real-case scenario, thus restricting them for academic
and research purposes.
```

‚BLACK-BOXATTACK(MINIMALKNOWLEDGE): In this  
kind of adversarial attack, the adversary has no information  
about the model, i.e., the model only knows the output of the  
neural networkgpxqand does not know any parameters of any  
layer of the neural network, i.e.,fpiqas described in Equation  
1 and also shown in Figure 4. A further stronger branch of  
this, a no-model attack where we do not have any information  
from the model, input and output.  
This is the most vital kind of attack in this classification as  
little as possible information and is scalable to the real world,  
making it highly susceptible to ethical issues. Due to their

```
possible scalability, some attacks can be misused in applications.
However, most of the attacks are slower than the white-box
and grey-box attacks, limiting their scalability.
```
```
B. Based on model output for adversarial attacks
```
```
‚SCORE BASEDATTACK:In this kind of adversarial attack,
the adversary knows the probabilities or soft-label for every
class of the model, i.e.,gpxq.
```
```
‚DECISION-BASEDATTACK:In this kind of adversarial
attack, the adversary knows only the decision of the model,
i.e., the predicted class orargmaxrgpxqs
```
```
Fig. 4. Knowledge of Adversarial Attack
```

Fig. 5. Difference between Decision-based, Score-based and White-box Attacks  
\[36\]

C. Based on the goal of adversarial attacks

‚UNTARGETTED(ERROR-GENERIC) ATTACK:In this  
kind of adversarial attack, the adversary’s goal is to misguide  
the neural network model to make a network classify any  
incorrect class. Making use of the definition of adversarial  
samples optimisation for the targetted attacks, can be formally  
defined as:

```
minimize gpx\`εxqC subject to εx
```

wheregpqCis the soft-label for the correct class. This kind  
of attack is naive with the only goal for the misclassification  
and thus provide little information on the reasoning for the  
misclassification. At the same time, they highlight the issue  
of lousy representation space and the highly complex (non-  
smooth) decision boundary of the neural networks in higher  
dimensions.

‚TARGETED(ERROR-SPECIFIC) ATTACK: In this kind of  
adversarial attack, the adversary’s goal is to misguide the model  
to classify a particular class other than the actual class. Making

```
Fig. 6. Difference between digital, physical, perceivable and non-perceivable
attacks [37]
```
```
Fig. 7. Example of Perceivable and Non-Perceivable Attacks [37]
```
```
use of the definition of adversarial samples optimisation for
the targetted attacks, can be formally defined as:
```
```
maximize gpx\`εxqT subject to εx
```
```
wheregpqTis the soft-label for the target class. This kind of
attack is harder than the untargetted attack as it can focus the
attack on one particular class and help to understand the primary
pattern for the class. However, this attack has a lower success
rate than the untargeted attack making it hard to generalise for
the dataset.
```
```
Fig. 8. Example of Digital and Physical Attacks [37]
```

D. Based on perceivability of adversarial samples

‚PERCEIVABLE(VISIBLE) ATTACK:In this kind of  
adversarial attack, the perturbation is visible to the naked  
human eye or other senses and it usually involving adding an  
adversarial patch, deformation of input, or altering the input  
as shown in Figures 6, and 7.  
This kind of attack helps in understanding the difference  
between human learning and machine learning, where we  
humans tend to focus on the object of interest, machine  
learning attends to the broken pattern, which results in  
misclassification. The use of visible attacks also restricts  
real-world deployment as they can be noticed right away and  
can be rectified.

‚NON-PERCEIVABLE(INVISIBLE) ATTACK: In this kind  
of adversarial attack, the perturbation is invisible to the  
human senses. This attack usually involves the addition of  
digital dust on the input, which is unperceivable to the human  
senses as shown in Figures 6, and 7.  
This kind of attack helps in understanding the brittle nature of  
the trained model and helps us to understand the decision  
boundary of the model. At the same time, they are  
particularly pernicious from a security standpoint as they  
cannot be observed, and the model having human observation  
cannot be alerted by the manipulation of the input.

E. Based on the format of adversarial samples

‚DIGITALATTACK:In this kind of adversarial attack, the  
adversary targets the digital asset such as images, videos, or  
other files as shown in Figures 6, and 8. Due to the target  
being a digital asset, it is a common form of attack as the  
adversary has expanded selection of the format and a lower  
difficulty of crafting adversarial perturbations.  
This kind of attack is mainly used for academic and research  
purposes to understand the vulnerability of neural networks.  
However, they pose an imminent threat to the models deployed  
as cyber hacking can lead their digital assets vulnerable to  
these attacks.

```
Fig. 9. Illustration of poisoning, evasion and model extraction attacks [38]
```
```
‚PHYSICALATTACK:In this kind of adversarial attack, the
adversary has the target in the physical world which is
attacked. Some examples include stop signs and lane
markings as shown in Figures 6, and 8. Some of the physical
attacks may require bigger and coarser patterns, as processing
them requires digitising the physical object with a sensor.
This digitising process may destroy finer details.
This kind of attack is limited due to the requirement of physical
objects and coarser harder attack perturbations. At the same
time, they pose a severe security threat to a multitude of real-
world applications.
```
```
F. Based on the scope of adversarial attacks
```
```
‚INDIVIDUALATTACK:In this kind of adversarial attack, the
scope of the adversarial attack is to find a perturbation that
added to one sample can misclassify the original sample, i.e.
εxdiffers with the different input sample. In this kind of attack,
optimisation is done for each input sample.
This kind of attack helps in understanding the breakage of
pattern and texture in the images. However, at the same time,
due to each input sample being different, it is hard to
generalise and understand the perturbation. Thus, it only
provides us with information on robustness and leaves us with
little understanding of the existence of adversarial samples.
```
```
‚UNIVERSALATTACK: In this kind of adversarial attack, the
goal of the adversarial attack is to find a perturbation that
added to original samples can misclassify most of the original
samples, i.e.,ε“εx 1 “εx 2 wherex 1 andx 2 are different
input samples andεis the universal perturbation. In this kind
of attack, optimisation is done for the entire dataset.
This kind of attack helps in understanding the global
vulnerability of the network as it finds the universal
perturbation, thus finding the vulnerability in accessing the
input. It also helps in understanding the transferability of
adversarial samples.
```
```
Fig. 10. Illustration of data poisioning attack [37]
```
```
Fig. 11. Problem Statement for the extraction attacks as proposed by [39]
```

G. Based on attacking strategy used by adversarial attacks

‚DATAPOISONINGATTACK: In this kind of adversarial  
attack, the adversary usually conspires when the model is not  
trained, and the objective is to inject perturbations in the  
training data so that the model will misclassify the  
non-perturbed samples at the testing time as shown in Figures  
9, and 10. It is also known as contaminating attack. It relies  
on the compromise of the integrity of the training data and  
optionally availability of the model.  
Backdoor attacks are another branch of data-poisoning attacks  
in which adversarial attacks fool models by imprinting a texture  
or pattern referred to as triggers in a few training samples and  
changing their labels during training. During the inference, the  
misclassification is caused by injecting the trigger in the input  
sample. In a related branch of clean-label poisoning attacks, no  
control over the labelling process is handled to the adversarial  
attacks.  
Some examples include Adversarial Embedding Attack \[40\],  
Backdoor Poisioning Attack \[14\] Clean Label Backdoor Attack  
\[14\], Bullseye Polytope Attack \[41\], Feature Collision Attack  
\[42\].

```
This kind of attack is effective only when the model is exposed
while training, however in most cases, the trained model is
deployed, making this strategy less useful in creating real-world
attacks. However, this also helps in understanding the bias in
training caused by the data and further helps us understand the
decision boundary and the representation space of the model.
Moreover, this kind of attack is effective against continual
learning models and reinforcement learning models where the
model interact and learn based on the outcome.
An example case study in the Twitter chatbot ‘Tay’ launched
by Microsoft in 2016 [43]. The idea was to engage in
conversation with users and learn playful conversations.
However, the internet troll users started to feed profane, and
offensive tweets, which resulted in the more offensive tweets
by the bot [44].
```
```
‚EVASIVEATTACK: In this kind of adversarial attack, the
adversary usually conspires when the model is trained, and
the objective is to find perturbations for the testing data so
that the neural network model will misclassify them, as shown
in Figure 9. It is a trial and error kind of attack, and the
adversary does not know which perturbations can make the
model misclassify. It relies on the compromise of the integrity
of the testing data. Most of the proposed attacks belong to this
category.
```
```
‚EXTRACTIONATTACK: In this kind of adversarial attack,
the adversary usually conspires when the model has been
deployed, and the objective is to retrieve the neural network
model parameters as shown in Figure 11. It relies on the
compromise of the confidentiality of the model as the private
learned featured are recovered.
A related branch deals in extracting the functionality of the
model as shown in Figure 5 instead of the actual model
parameters. Some of the examples include Copycat CNN [45],
Knock-off Nets [39], and Functionally Equivalent Extraction
Attack [46].
```
```
‚MODELPOISONINGATTACKS: In this kind of adversarial
attack, the adversary simply replaces the legitimate model with
the adversarial one. This is the traditional cyber-attack in which
the model file (usually weights) is replaced with another one.
```
```
H. Based on optimisation strategy used by adversarial attacks
‚GRADIENTBASEDATTACKS: In this kind of adversarial
attack, the adversary uses gradients and/or backpropagation to
compute the perturbation required for the original sample to
misclassify. Some of the examples include, Fast Gradient Sign
Method [16], and Projected Gradient Descent Attack [1].
```
```
‚EVOLUTIONARYSTRATEGYBASEDATTACKS:In this
kind of adversarial attack, adversery use evolutionary-strategy
based optimisation like Differential Evolution (DE) [47], and
Covariance Matrix Adaptation Evolution Strategy (CMA-ES)
[48] to search for the adversarial perturbationεx. This is done
for the black-box attacks, where model information is not
```
```
TABLE I
DISTANCE METRICS BASED ATTACKS USED IN LITERATURE COMPILED BY
KOTYAN ET AL. [31].
```
```
Literature L 0 L 1 L 2 L 8
Chen et al. (2020) [36] ✓✓
Croce and Hein (2020) [49] ✓✓
Ghiasi et al. (2020) [50] ✓✓
Hirano and Takemoto (2020) [51] ✓
Cohen et al. (2019) [52] ✓
Kotyan et al. (2019) [31] ✓
Su et al. (2019) [9] ✓
Tan and Shokri (2019) [53] ✓
Wang et al. (2019) [54] ✓
Wong et al. (2019) [55] ✓
Zhang et al. (2019a) [56] ✓
Zhang et al. (2019b) [57] ✓
Brendel et al. (2018) [58] ✓
Buckman et al. (2018) [26] ✓
Gowal et al. (2018) [59] ✓
Grosseet al. (2018) [60] ✓
Guo et al. (2018) [22] ✓✓
Madry et al. (2018) [1] ✓✓
Singh et al. (2018) [61] ✓
Song et al. (2018) [23] ✓
Tramer et al. (2018) [28] ✓
Arpit et al. (2017) [62] ✓
Carlini and Wagner (2017) [27] ✓✓✓
Chen et al. (2017a) [63] ✓✓✓
Chen et al. (2017b) [64] ✓
Das et al. (2017) [21] ✓✓
Gu et al. (2017) [14] ✓✓
Jang et al. (2017) [65] ✓
Moosavi et al. (2017) [8] ✓✓
Xu et al. (2017) [24] ✓✓✓
Kurakin et al. (2016) [12] ✓
Moosavi et al. (2016) [66] ✓✓
Papernot et al. (2016a) [67] ✓
Papernot et al. (2016b) [18] ✓
Goodfellow et al. (2014) [16] ✓
```

present, and optimisation cannot rely on backpropagating  
gradients. Some of the examples include One-Pixel Attack \[9\]  
and Threshold Attack \[31\].

I. Based on perturbation constraints on adversarial samples

‚DISTANCE METRICS BASED CONSTRAINTATTACK: In  
this kind of adversarial attack, the adversary constrains the  
perturbation search for the input by using distance from the  
original sample. Several different distance norms are used to  
create different types of attacks. Here, the perturbationεxis  
constrained such that}εx}păth, wherepis the distance norm  
andthis the threshold constraint. Some of the common norms  
used areL 0,L 1,L 2, andL 8, and Table I shows examples of  
adversarial attacks employing different distance norms.

### ‚GEOMETRICTRANSFORMATIONS BASED CONSTRAINT

```
ATTACK:In this kind of adversarial attack, the adversary relies
on geometric transformations of the original input to misclassify
the model. Spatial Transformations like affine and rotations
can misclassify the network even though the network is trained
using those as augmentations in the training dataset [68]. Color-
channel permutation also affects the model’s performance and
can be used as an adversarial attack [69].
```
```
J. Based on intention of adversarial attacks
‚INTENTEDATTACK:In this kind of adversarial attack, the
adversary has the malicious intention of misclassifying the
model based on perturbations.
```
```
‚UNINTENTEDATTACK:The model misclassifies this kind
of adversarial attack due to the various unintended failures in
training or inference. An example includes reward hacking in
which reinforcement learning systems act weirdly because of
the discrepancies between the specified reward received by the
model and the true intended reward [70].
```
```
K. Based on adversarial attacker’s influence
‚CAUSATIVEATTACK:In this kind of adversarial attack, the
adversary can manipulate both training and testing data.
```
```
‚EXPLORATORYATTACK:In this kind of adversarial attack,
the adversary can only manipulate the testing data.
```
```
IV. UNDERSTANDING ADVERSARIAL ATTACKS
It is hypothesised in [16] that neural networks’ linearity is
one of the principal reasons for failure against an adversary
and non-linear neural networks are thus, more robust compared
to linear networks [71]. Based on this understanding, it is
proposed in [26] discretise the input feature space, which may
lead to breaking this linearity.
A geometric perspective is analysed in [72], where it is
shown that adversarial samples lie in shared subspace, along
which the decision boundary of a classifier is positively curved.
Further, in [73], a relationship between sensitivity to additive
perturbations of the inputs and the curvature of the decision
boundary of deep networks is shown.
Another aspect of robustness is discussed in [1], where
authors suggest that the capacity of the neural networks’
architecture is relevant to the robustness. However, research
shows that the input feature space itself is vast, which provide
opportunities to the adversaries [24]. It was also observed that
the classifiers are not familiarised with the adversarial input
feature space as adversarial samples have much lower
probability densities under the image distribution [23].
Intuitively; thus, in [21] authors recommended discarding
some of the information unnoticeable to humans in input
feature space by compressing as adversarial noises are often
indiscernible by the human eye. The bounds for the
robustness using this input feature space is also studied in
[74]. Further, the existence of different internal representations
```

learned by neural networks for an adversarial sample  
compared to a benign sample is shown in \[34\].  
It is also stated in \[75\] that the adversarial vulnerability is a  
significant consequence of the dominant supervised learning  
paradigm and a classifier’s sensitivity to well-generalising  
features in the known input distribution. Also, research by  
\[76\] argues that adversarial attacks are entangled with the  
interpretability of neural networks as results on adversarial  
samples can hardly be explained.  
Another investigation proposes the conflicting saliency  
added by adversarial samples as the reason for  
misclassification \[35\]. It was shown in \[77\] that perturbation  
causes a shift in attention of the neural network, which is a  
probable cause for the misclassification. While the white-box  
gradient-based attack consistently scattered the attention from  
the object of interest, the black-box attack was shown to  
either bring the model’s attention to the perturbation or  
disrupt the attention around the perturbation.

V. TACKLING ADVERSARIAL ATTACKS WITH ADVERSARIAL  
DEFENCES  
Many defensive systems and detection systems have also  
been proposed to mitigate some of the problems. Some  
approaches rely on detecting adversarial samples to mitigate  
the adverse effects of adversarial algorithms, while some  
approaches rely on defensive algorithms. However, there are  
still no current solutions or promising ones which can negate  
the adversarial attacks consistently. Regarding defensive  
systems, there are many variations of defenses \[19\]–\[26\]  
which are carefully analysed in \[29\], \[30\] and many of their  
shortcomings are documented.  
Defensive distillation \[18\], a defence was proposed, in which  
a smaller neural network squeezes the content learned by the  
original one was proposed as a defence. However, it was shown  
not to be robust enough in \[27\]. Adversarial training was also  
proposed, in which adversarial samples are used to augment  
the training dataset \[16\], \[1\]. Augmentation of the dataset is  
done so that the neural network should classify the adversarial  
samples, thus increasing their robustness. Although adversarial  
training can increase the robustness slightly, the resulting neural  
network is still vulnerable to attacks \[28\].  
Regarding detection systems, a study from \[78\] demonstrated  
that indeed some adversarial samples have different statistical  
properties which could be exploited for detection. The authors  
in \[24\] proposed to compare the prediction of a classifier with  
the prediction of the same input, but ‘squeezed’. This technique  
allowed classifiers to detect adversarial samples with small  
perturbations. Many detection systems fail when adversarial  
samples deviate from test conditions \[79\]–\[81\]. Thus, the clear  
benefits of detection systems remain inconclusive.  
It was shown in \[35\] that changes in pixels of an image  
propagate and expand throughout the layers to either disappear  
or cause significant changes in the classification. It was also  
shown that perturbation in nearby pixels of successful one-pixel  
attack has high attack accuracy. This suggests that changes in a  
pixel may increase or decrease the influence of a receptive field

```
(small group of nearby pixels). This is a direct relationship of
the convolution, which is a linear operation.
In the adversarial setting, the analysis of the spatial
distribution of saliency proves helpful to interpret why
changing some pixels [9] in the network corresponds to
misclassification. It was hypothesised in [35] that the
existence of adversarial samples is due to conflicting saliency,
which causes enough disturbance in the neural network
forcing it to misclassify. Hence, adversarial samples are not
naively fooling neural networks but diverting their attention
towards another part of the image.
```

### VI. CONCLUSION

```
In this survey, we analysed the importance and the
significance of adversarial attacks as a real-world threat to
applications in different domains. In order to tackle the
imminent threat, it is required to understand the theoretical
and empirical limitations and effects of adversarial attacks. In
order to facilitate the understanding, we provide an extensive
classification from various perspectives and discuss their
implications. Further, we also provide a brief survey of
literature on understanding adversarial attacks and adversarial
defences.
Based on our understanding, we can now define few research
directions issues which are yet to be resolved.
‚ADATIVE ADVERSARIAL ATTACKS AND DEFENCES:
Current adversarial attacks and defences are static in nature
and do not adapt to changing scenarios. This limits the use of
both adversarial attacks and mitigating their adverse effects by
adversarial defences.
‚EXPLORING BLACK-BOX NATURE:Current
state-of-the-art models are black-box in nature which makes
auditing their output difficult. This limits our understanding of
the existence of adversarial examples as well as our
understanding to identify if an adversarial attack has
compromised the model.
‚LEARNING RESILIENT FEATURES:The current state of the
art models is brittle in nature as it is easy to disrupt the learned
features. Supervised end-to-end learning needs to be replaced
with different learning techniques which are more robust and
less brittle in nature.
‚PROACTIVE MEASURES: Current adversarial defences are
reactive in nature where they defend against an existing
adversarial attack. However, a lack of proactive framework
remains a challenge to handle the new adversarial attacks.
‚THERORETICAL LIMITATIONS:Current neural networks
are difficult to analyse theoretically due to their complicated
non-convex properties. Further, adversarial samples are
solutions to the optimisation problem, which is non-linear and
non-convex. Because of our limited theoretical tools, it is hard
to describe the solutions to these complicated optimisation
problems and further complex to create a theoretical
framework for adversarial defences which can mitigate a set
of adversarial samples.
```

### VII. TIMEFRAME OF SURVEY

```
This article covers the adversarial attacks for neural networks
and related works published between 2013 and 2020.
```
```
VIII. FURTHER READINGS
‚ARTICLE: On evaluating adversarial robustness by Carlini
et al. [81]
```
```
‚ARTICLE:Wild patterns: Ten years after the rise of
adversarial machine learning by Biggio et al. [10].
```
```
‚ARTICLE: Obfuscated gradients give a false sense of
security: Circumventing defences to adversarial examples by
Athalye et al. [29].
```
```
‚TECHNICALREPORT: The Malicious Use of Artificial
Intelligence: Forecasting, Prevention, and Mitigation by
Brundage et al. [82]
```
```
‚BOOK: Adversarial Machine Learning by Joseph et al. [83].
```
```
‚RESOURCE:CleverHans library, compiled by Tensorflow
and managed by Nicolas Paper not, Ian Goodfellow and others,
is an adversarial example library for “constructing attacks,
building defences, and benchmarking both” [84].
```
```
‚RESOURCE:Adversarial Robustness Toolbox library,
compiled by IBM, is a library for various adversarial attacks,
defences, and metrics used [85].
```
```
‚RESOURCE:Foolbox library compiled by Bethge Lab [86],
[87]
```
```
‚COMPETITION:Unrestricted Adversarial Examples Contest
was sponsored by Google Brain, which was “a
community-based challenge to incentivise and measure
progress towards the goal of zero confident classification
errors in machine learning models". https://ai.googleblog.com/
2018/09/introducing-unrestricted-adversarial.html
```

‚ARTICLELIST: Nicolas Carlini, a leading researcher in  
adversarial machine learning, maintains an unfiltered list of  
1000 \` articles around the field of adversarial machine  
learning and also maintains a curated list of articles for the  
introduction in the field. https://nicholas.carlini.com/writing/  
2018/adversarial-machine-learning-reading-list.html

```
‚RESEARCHGROUP:Madry lab, led by Aleksander M ̨adry
of Massachusetts Institute of Technology, is a leading research
group in the field of adversarial machine learning with the
focus on understanding the robustness of neural networks.
http://madry-lab.ml/
```
```
‚RESEARCHGROUP:Bethge lab, led by Matthias Bethge
of the University of Tübingen, is a leading research group
```
```
in understanding the characteristics of neural networks. http:
//bethgelab.org/
```
```
‚RESEARCHGROUP:Trusted AI group of IBM Research
AI is a leading research group focusing on instilling more
trust in the decisions of the neural networks by tackling issues
like fairness, robustness, explainability, transparency and
accountability. https:
//www.research.ibm.com/artificial-intelligence/trusted-ai/
```

### REFERENCES

```
[1]A. Madry, A. Makelov, L. Schmidt, D. Tsipras, and A. Vladu, “Towards
deep learning models resistant to adversarial attacks,” inInternational
Conference on Learning Representations, 2018.
[2]Y.-T. Tsai, M.-C. Yang, and H.-Y. Chen, “Adversarial attack on sentiment
classification,” inProceedings of the 2019 ACL Workshop BlackboxNLP:
Analyzing and Interpreting Neural Networks for NLP, 2019, pp. 233–240.
[3]V. Subramanian, E. Benetos, and M. Sandler, “Robustness of adversarial
attacks in sound event classification,” inAcoustic Scenes and Events
2019 Workshop (DCASE2019), 2019, p. 239.
[4]S. G. Finlayson, J. D. Bowers, J. Ito, J. L. Zittrain, A. L. Beam, and I. S.
Kohane, “Adversarial attacks on medical machine learning,”Science, vol.
363, no. 6433, pp. 1287–1289, 2019.
[5]C. e. a. Szegedy, “Intriguing properties of neural networks,” inIn ICLR.
Citeseer, 2014.
[6]A. Nguyen, J. Yosinski, and J. Clune, “Deep neural networks are easily
fooled: High confidence predictions for unrecognizable images,” in
Proceedings of the IEEE Conference on Computer Vision and Pattern
Recognition, 2015, pp. 427–436.
[7]T. B. Brown, D. Mané, A. Roy, M. Abadi, and J. Gilmer, “Adversarial
patch,”arXiv preprint arXiv:1712.09665, 2017.
[8]S.-M. Moosavi-Dezfooli, A. Fawzi, O. Fawzi, and P. Frossard, “Universal
adversarial perturbations,” inProceedings of the IEEE conference on
computer vision and pattern recognition. Ieee, 2017, pp. 1765–1773.
[9]J. Su, D. V. Vargas, and K. Sakurai, “One pixel attack for fooling
deep neural networks,”IEEE Transactions on Evolutionary Computation,
vol. 23, no. 5, pp. 828–841, 2019.
[10]B. Biggio and F. Roli, “Wild patterns: Ten years after the rise of
adversarial machine learning,”Pattern Recognition, vol. 84, pp. 317–331,
2018.
[11]M. Sharif, S. Bhagavatula, L. Bauer, and M. K. Reiter, “Accessorize to
a crime: Real and stealthy attacks on state-of-the-art face recognition,”
inProceedings of the 2016 ACM SIGSAC Conference on Computer and
Communications Security. Acm, 2016, pp. 1528–1540.
[12]A. Kurakin, I. Goodfellow, and S. Bengio, “Adversarial examples in the
physical world,”arXiv preprint arXiv:1607.02533, 2016.
[13]A. Athalye and I. Sutskever, “Synthesizing robust adversarial examples,”
inIcml, 2018.
[14]T. Gu, B. Dolan-Gavitt, and S. Garg, “Badnets: Identifying vulnerabilities
in the machine learning model supply chain,” arXiv preprint
arXiv:1708.06733, 2017.
[15]C. Yan, W. Xu, and J. Liu, “Can you trust autonomous vehicles:
Contactless attacks against sensors of self-driving vehicle,”Def Con,
vol. 24, no. 8, p. 109, 2016.
[16]I. J. Goodfellow, J. Shlens, and C. Szegedy, “Explaining and harnessing
adversarial examples,”arXiv preprint arXiv:1412.6572, 2014.
[17]R. Huang, B. Xu, D. Schuurmans, and C. Szepesvári, “Learning with a
strong adversary,”arXiv preprint arXiv:1511.03034, 2015.
[18]N. Papernot, P. McDaniel, X. Wu, S. Jha, and A. Swami, “Distillation
as a defense to adversarial perturbations against deep neural networks,”
in2016 IEEE Symposium on Security and Privacy (SP). Ieee, 2016,
pp. 582–597.
[19]G. K. Dziugaite, Z. Ghahramani, and D. M. Roy, “A study of the effect of
jpg compression on adversarial images,”arXiv preprint arXiv:1608.00853,
2016.
[20]T. Hazan, G. Papandreou, and D. Tarlow,Perturbations, Optimization,
and Statistics. MIT Press, 2016.
```

\[21\]N. Das, M. Shanbhogue, S.-T. Chen, F. Hohman, L. Chen, M. E. Kounavis,  
and D. H. Chau, “Keeping the bad guys out: Protecting and vaccinating  
deep learning with jpeg compression,”arXiv preprint arXiv:1705.02900,

\[22\]C. Guo, M. Rana, M. Cisse, and L. van der Maaten, “Countering  
adversarial images using input transformations,” in International  
Conference on Learning Representations, 2018.  
\[23\]Y. Song, T. Kim, S. Nowozin, S. Ermon, and N. Kushman,  
“Pixeldefend: Leveraging generative models to understand and defend  
against adversarial examples,” inInternational Conference on Learning  
Representations, 2018.  
\[24\]W. Xu, D. Evans, and Y. Qi, “Feature squeezing: Detecting adversarial  
examples in deep neural networks,”arXiv preprint arXiv:1704.01155,

\[25\]X. Ma, B. Li, Y. Wang, S. M. Erfani, S. Wijewickrema, G. Schoenebeck,  
D. Song, M. E. Houle, and J. Bailey, “Characterizing adversarial  
subspaces using local intrinsic dimensionality,” arXiv preprint  
arXiv:1801.02613, 2018.  
\[26\]J. Buckman, A. Roy, C. Raffel, and I. Goodfellow, “Thermometer  
encoding: One hot way to resist adversarial examples,” inInternational  
Conference on Learning Representations, 2018.  
\[27\]N. Carlini and D. Wagner, “Towards evaluating the robustness of neural  
networks,” in2017 ieee symposium on security and privacy (sp). Ieee,  
2017, pp. 39–57.  
\[28\]F. Tramèr, A. Kurakin, N. Papernot, I. Goodfellow, D. Boneh, and  
P. McDaniel, “Ensemble adversarial training: Attacks and defenses,” in  
International Conference on Learning Representations, 2018.  
\[29\]A. Athalye, N. Carlini, and D. Wagner, “Obfuscated gradients give a  
false sense of security: Circumventing defenses to adversarial examples,”  
inIcml, 2018.  
\[30\]J. Uesato, B. O’Donoghue, P. Kohli, and A. Oord, “Adversarial risk  
and the dangers of evaluating against weak attacks,” inInternational  
Conference on Machine Learning, 2018, pp. 5032–5041.  
\[31\]D. V. Vargas and S. Kotyan, “Robustness assessment for adversarial  
machine learning: Problems, solutions and a survey of current neural  
networks and defenses,”arXiv preprint arXiv:1906.06026, 2019.  
\[32\]F. Tramer, N. Carlini, W. Brendel, and A. Madry, “On adaptive attacks to  
adversarial example defenses,”arXiv preprint arXiv:2002.08347, 2020.  
\[33\]L. Thesing, V. Antun, and A. C. Hansen, “What do ai algorithms  
actually learn?-on false structures in deep learning,”arXiv preprint  
arXiv:1906.01478, 2019.  
\[34\]S. Sabour, Y. Cao, F. Faghri, and D. J. Fleet, “Adversarial manipulation  
of deep representations,”arXiv preprint arXiv:1511.05122, 2015.  
\[35\]D. V. Vargas and J. Su, “Understanding the one-pixel attack: Propagation  
maps and locality analysis,”arXiv preprint arXiv:1902.02947, 2019.  
\[36\]J. Chen, M. I. Jordan, and M. J. Wainwright, “Hopskipjumpattack: A  
query-efficient decision-based attack,” in2020 ieee symposium on security  
and privacy (sp). Ieee, 2020, pp. 1277–1294.  
\[37\]M. Comiter,Attacking Artificial Intelligence: AI’s Security Vulnerability  
and what Policymakers Can Do about it. Belfer Center for Science  
and International Affairs, 2019.  
\[38\]H.-Y. Lin and B. Biggio, “Adversarial machine learning: Attacks from  
laboratories to the real world,”Computer, vol. 54, no. 5, pp. 56–60,

\[39\]T. Orekondy, B. Schiele, and M. Fritz, “Knockoff nets: Stealing  
functionality of black-box models,” inProceedings of the IEEE/CVF  
Conference on Computer Vision and Pattern Recognition, 2019, pp.  
4954–4963.  
\[40\]R. Shokriet al., “Bypassing backdoor detection algorithms in deep  
learning,” in2020 IEEE European Symposium on Security and Privacy  
(EuroS&P). Ieee, 2020, pp. 175–183.  
\[41\]H. Aghakhani, D. Meng, Y.-X. Wang, C. Kruegel, and G. Vigna,  
“Bullseye polytope: A scalable clean-label poisoning attack with improved  
transferability,”arXiv preprint arXiv:2005.00191, 2020.  
\[42\]A. Shafahi, W. R. Huang, M. Najibi, O. Suciu, C. Studer, T. Dumitras,  
and T. Goldstein, “Poison frogs! targeted clean-label poisoning attacks  
on neural networks,”arXiv preprint arXiv:1804.00792, 2018.  
\[43\]V. Mathur, Y. Stavrakas, and S. Singh, “Intelligence analysis of tay  
twitter bot,” in2016 2nd International Conference on Contemporary  
Computing and Informatics (IC3I). Ieee, 2016, pp. 231–236.  
\[44\]A. Ohlheiser, “Trolls turned tay, microsoft’s fun millennial ai bot, into a  
genocidal maniac,”The Washington Post, vol. 25, 2016.  
\[45\]J. R. Correia-Silva, R. F. Berriel, C. Badue, A. F. de Souza, and  
T. Oliveira-Santos, “Copycat cnn: Stealing knowledge by persuading

```
confession with random non-labeled data,” in2018 International Joint
Conference on Neural Networks (IJCNN). Ieee, 2018, pp. 1–8.
[46]M. Jagielski, N. Carlini, D. Berthelot, A. Kurakin, and N. Papernot,
“High accuracy and high fidelity extraction of neural networks,” in29th
${$USENIX$}$ Security Symposium (${$USENIX$}$ Security 20), 2020,
pp. 1345–1362.
[47]R. Storn and K. Price, “Differential evolution–a simple and efficient
heuristic for global optimization over continuous spaces,”Journal of
global optimization, vol. 11, no. 4, pp. 341–359, 1997.
[48]N. Hansen, S. D. Müller, and P. Koumoutsakos, “Reducing the time
complexity of the derandomized evolution strategy with covariance matrix
adaptation (cma-es),”Evolutionary computation, vol. 11, no. 1, pp. 1–18,
2003.
[49]F. Croce and M. Hein, “Reliable evaluation of adversarial robustness
with an ensemble of diverse parameter-free attacks,”arXiv preprint
arXiv:2003.01690, 2020.
[50]A. Ghiasi, A. Shafahi, and T. Goldstein, “Breaking certified defenses:
Semantic adversarial examples with spoofed robustness certificates,”
arXiv preprint arXiv:2003.08937, 2020.
[51]H. Hirano and K. Takemoto, “Simple iterative method for generating
targeted universal adversarial perturbations,”Algorithms, vol. 13, no. 11,
p. 268, 2020.
[52]J. M. Cohen, E. Rosenfeld, and J. Z. Kolter, “Certified adversarial
robustness via randomized smoothing,”arXiv preprint arXiv:1902.02918,
2019.
[53]T. J. L. Tan and R. Shokri, “Bypassing backdoor detection algorithms in
deep learning,”arXiv preprint arXiv:1905.13409, 2019.
[54]B. Wang, Y. Yao, S. Shan, H. Li, B. Viswanath, H. Zheng, and B. Y.
Zhao, “Neural cleanse: Identifying and mitigating backdoor attacks in
neural networks,” in2019 IEEE Symposium on Security and Privacy
(SP). Ieee, 2019, pp. 707–723.
[55]E. Wong, F. R. Schmidt, and J. Z. Kolter, “Wasserstein adversarial
examples via projected sinkhorn iterations,” arXiv preprint
arXiv:1902.07906, 2019.
[56]H. Zhang, H. Chen, C. Xiao, S. Gowal, R. Stanforth, B. Li, D. Boning,
and C.-J. Hsieh, “Towards stable and efficient training of verifiably robust
neural networks,”arXiv preprint arXiv:1906.06316, 2019.
[57]H. Zhang, Y. Yu, J. Jiao, E. P. Xing, L. E. Ghaoui, and M. I. Jordan,
“Theoretically principled trade-off between robustness and accuracy,”
arXiv preprint arXiv:1901.08573, 2019.
[58]W. Brendel, J. Rauber, and M. Bethge, “Decision-based adversarial
attacks: Reliable attacks against black-box machine learning models,” in
International Conference on Learning Representations, 2018.
[59]S. Gowal, K. Dvijotham, R. Stanforth, R. Bunel, C. Qin, J. Uesato,
R. Arandjelovic, T. Mann, and P. Kohli, “On the effectiveness of interval
bound propagation for training verifiably robust models,”arXiv preprint
arXiv:1810.12715, 2018.
[60]K. Grosse, D. Pfaff, M. T. Smith, and M. Backes, “The
limitations of model uncertainty in adversarial settings,”arXiv preprint
arXiv:1812.02606, 2018.
[61]G. Singh, T. Gehr, M. Mirman, M. Püschel, and M. Vechev, “Fast
and effective robustness certification,”Advances in Neural Information
Processing Systems, vol. 31, pp. 10 802–10 813, 2018.
[62]D. Arpit, S. K. Jastrzebski, N. Ballas, D. Krueger, E. Bengio, M. S.
Kanwal, T. Maharaj, A. Fischer, A. C. Courville, Y. Bengioet al., “A
closer look at memorization in deep networks,” inIcml, 2017.
[63]P.-Y. Chen, Y. Sharma, H. Zhang, J. Yi, and C.-J. Hsieh, “Ead: elastic-net
attacks to deep neural networks via adversarial examples,”arXiv preprint
arXiv:1709.04114, 2017.
[64]P.-Y. Chen, H. Zhang, Y. Sharma, J. Yi, and C.-J. Hsieh, “Zoo: Zeroth
order optimization based black-box attacks to deep neural networks
without training substitute models,” inProceedings of the 10th ACM
Workshop on Artificial Intelligence and Security, 2017, pp. 15–26.
[65]U. Jang, X. Wu, and S. Jha, “Objective metrics and gradient descent
algorithms for adversarial examples in machine learning,” inProceedings
of the 33rd Annual Computer Security Applications Conference. Acm,
2017, pp. 262–277.
[66]S.-M. Moosavi-Dezfooli, A. Fawzi, and P. Frossard, “Deepfool: a simple
and accurate method to fool deep neural networks,” inProceedings of
the IEEE Conference on Computer Vision and Pattern Recognition, 2016,
pp. 2574–2582.
[67]N. Papernot, P. McDaniel, S. Jha, M. Fredrikson, Z. B. Celik, and
A. Swami, “The limitations of deep learning in adversarial settings,” in
```

2016 IEEE European symposium on security and privacy (EuroS&P).  
Ieee, 2016, pp. 372–387.  
\[68\]L. Engstrom, B. Tran, D. Tsipras, L. Schmidt, and A. Madry, “Exploring  
the landscape of spatial robustness,” inInternational Conference on  
Machine Learning. Pmlr, 2019, pp. 1802–1811.  
\[69\]J. Kantipudi, S. R. Dubey, and S. Chakraborty, “Color channel  
perturbation attacks for fooling convolutional neural networks and a  
defense against such attacks,”IEEE Transactions on Artificial Intelligence,  
vol. 1, no. 2, pp. 181–191, 2020.  
\[70\]R. S. S. Kumar, D. O. Brien, K. Albert, S. Viljöen, and J. Snover, “Failure  
modes in machine learning systems,”arXiv preprint arXiv:1911.11034,

\[71\]Y. Guo, C. Zhang, C. Zhang, and Y. Chen, “Sparse dnns with improved  
adversarial robustness,” inAdvances in neural information processing  
systems, 2018, pp. 242–251.  
\[72\]S.-M. Moosavi-Dezfooli, A. Fawzi, O. Fawzi, P. Frossard, and S. Soatto,  
“Robustness of classifiers to universal perturbations: A geometric  
perspective,” inInternational Conference on Learning Representations,

\[73\]A. Fawzi, S.-M. Moosavi-Dezfooli, P. Frossard, and S. Soatto, “Empirical  
study of the topology and geometry of deep networks,” inProceedings  
of the IEEE Conference on Computer Vision and Pattern Recognition,  
2018, pp. 3762–3770.  
\[74\]A. Fawzi, H. Fawzi, and O. Fawzi, “Adversarial vulnerability for any  
classifier,” inAdvances in Neural Information Processing Systems, 2018,  
pp. 1178–1187.  
\[75\]A. Ilyas, S. Santurkar, D. Tsipras, L. Engstrom, B. Tran, and A. Madry,  
“Adversarial examples are not bugs, they are features,” inAdvances in  
Neural Information Processing Systems, 2019, pp. 125–136.  
\[76\]G. Tao, S. Ma, Y. Liu, and X. Zhang, “Attacks meet interpretability:  
Attribute-steered detection of adversarial samples,” inAdvances in Neural  
Information Processing Systems, 2018, pp. 7717–7728.  
\[77\]S. Kotyan and D. V. Vargas, “Deep neural network loses attention to  
adversarial images,”arXiv preprint arXiv:2106.05657, 2021.  
\[78\]K. Grosse, P. Manoharan, N. Papernot, M. Backes, and P. McDaniel,  
“On the (statistical) detection of adversarial examples,”arXiv preprint  
arXiv:1702.06280, 2017.

```
[79]N. Carlini and D. Wagner, “Adversarial examples are not easily detected:
Bypassing ten detection methods,” inProceedings of the 10th ACM
Workshop on Artificial Intelligence and Security. Acm, 2017, pp. 3–14.
[80]——, “Magnet and" efficient defenses against adversarial attacks" are
not robust to adversarial examples,”arXiv preprint arXiv:1711.08478,
2017.
[81]N. Carlini, A. Athalye, N. Papernot, W. Brendel, J. Rauber, D. Tsipras,
I. Goodfellow, A. Madry, and A. Kurakin, “On evaluating adversarial
robustness,”arXiv preprint arXiv:1902.06705, 2019.
[82]M. Brundage, S. Avin, J. Clark, H. Toner, P. Eckersley, B. Garfinkel,
A. Dafoe, P. Scharre, T. Zeitzoff, B. Filaret al., “The malicious use
of artificial intelligence: Forecasting, prevention, and mitigation,”arXiv
preprint arXiv:1802.07228, 2018.
[83]L. Huang, A. D. Joseph, B. Nelson, B. I. Rubinstein, and J. D. Tygar,
“Adversarial machine learning,” inProceedings of the 4th ACM workshop
on Security and artificial intelligence, 2011, pp. 43–58.
[84]N. Papernot, F. Faghri, N. Carlini, I. Goodfellow, R. Feinman, A. Kurakin,
C. Xie, Y. Sharma, T. Brown, A. Roy, A. Matyasko, V. Behzadan,
K. Hambardzumyan, Z. Zhang, Y.-L. Juang, Z. Li, R. Sheatsley, A. Garg,
J. Uesato, W. Gierke, Y. Dong, D. Berthelot, P. Hendricks, J. Rauber, and
R. Long, “Technical report on the cleverhans v2.1.0 adversarial examples
library,”arXiv preprint arXiv:1610.00768, 2018.
[85]M.-I. Nicolae, M. Sinn, M. N. Tran, B. Buesser, A. Rawat, M. Wistuba,
V. Zantedeschi, N. Baracaldo, B. Chen, H. Ludwig, I. Molloy, and
B. Edwards, “Adversarial robustness toolbox v1.1.0,”CoRR, vol.
1807.01069, 2018. [Online]. Available: https://arxiv.org/pdf/1807.
[86]J. Rauber, R. Zimmermann, M. Bethge, and W. Brendel, “Foolbox
native: Fast adversarial attacks to benchmark the robustness of machine
learning models in pytorch, tensorflow, and jax,”Journal of Open
Source Software, vol. 5, no. 53, p. 2607, 2020. [Online]. Available:
https://doi.org/10.21105/joss.
[87]J. Rauber, W. Brendel, and M. Bethge, “Foolbox: A python toolbox
to benchmark the robustness of machine learning models,” in
Reliable Machine Learning in the Wild Workshop, 34th International
Conference on Machine Learning, 2017. [Online]. Available: http:
//arxiv.org/abs/1707.
```