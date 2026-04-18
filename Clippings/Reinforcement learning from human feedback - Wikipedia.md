---
title: "Reinforcement learning from human feedback - Wikipedia"
source: "https://en.wikipedia.org/wiki/Reinforcement_learning_from_human_feedback?utm_source=chatgpt.com"
author:
  - "[[Contributors to Wikimedia projects]]"
published: 2023-03-03
created: 2026-04-13
description:
tags:
  - "clippings"
---
![](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/RLHF_diagram.svg/500px-RLHF_diagram.svg.png)

High-level overview of reinforcement learning from human feedback

In [machine learning](https://en.wikipedia.org/wiki/Machine_learning "Machine learning"), **reinforcement learning from human feedback** (**RLHF**) is a technique to [align](https://en.wikipedia.org/wiki/AI_alignment "AI alignment") an [intelligent agent](https://en.wikipedia.org/wiki/Intelligent_agent "Intelligent agent") with human [preferences](https://en.wikipedia.org/wiki/Preference "Preference"). It involves training a reward model to represent preferences, which can then be used to train other models through.[^1]

In classical reinforcement learning, an intelligent agent's goal is to learn a function that guides its behavior, called a.[^2] The function is iteratively optimized to increase the reward signal derived from the agent's task performance.[^3] However, explicitly defining a reward function that accurately approximates human preferences is challenging. Therefore, RLHF seeks to train a "reward model" directly from human [feedback](https://en.wikipedia.org/wiki/Feedback "Feedback").[^4] The reward model is first trained in a [supervised](https://en.wikipedia.org/wiki/Supervised_learning "Supervised learning") manner to predict if a response to a given prompt is good (high reward) or bad (low reward) based on ranking data collected from human [annotators](https://en.wikipedia.org/wiki/Labeled_data "Labeled data"). This model then serves as a reward function to improve an agent's policy through an [optimization algorithm](https://en.wikipedia.org/wiki/Optimization_algorithm "Optimization algorithm") like [proximal policy optimization](https://en.wikipedia.org/wiki/Proximal_policy_optimization "Proximal policy optimization").[^5] [^6] [^7]

RLHF has applications in various domains in machine learning, including [natural language processing](https://en.wikipedia.org/wiki/Natural_language_processing "Natural language processing") tasks such as [text summarization](https://en.wikipedia.org/wiki/Text_summarization "Text summarization") and [conversational agents](https://en.wikipedia.org/wiki/Conversational_agents "Conversational agents"), [computer vision](https://en.wikipedia.org/wiki/Computer_vision "Computer vision") tasks like [text-to-image models](https://en.wikipedia.org/wiki/Text-to-image_model "Text-to-image model"), and the development of [video game bots](https://en.wikipedia.org/wiki/Video_game_bot "Video game bot"). While RLHF is an effective method of training models to act better in accordance with human preferences, it also faces challenges due to the way the human preference data is collected. Though RLHF does not require massive amounts of data to improve performance, sourcing high-quality preference data is still an expensive process. Furthermore, if the data is not carefully collected from a representative [sample](https://en.wikipedia.org/wiki/Sampling_\(statistics\) "Sampling (statistics)"), the resulting model may exhibit unwanted [biases](https://en.wikipedia.org/wiki/Algorithmic_bias "Algorithmic bias").

## Background and motivation

Optimizing a model based on human feedback is desirable when a task is difficult to specify yet easy to judge.[^8] For example, one may want to train a model to generate [safe](https://en.wikipedia.org/wiki/AI_safety "AI safety") text that is both helpful and harmless (such as lacking [bias](https://en.wikipedia.org/wiki/Algorithmic_bias "Algorithmic bias"), toxicity, or otherwise harmful content). Asking humans to manually create examples of harmless and harmful text would be difficult and time-consuming. However, humans are adept at swiftly assessing and comparing the harmfulness of different AI-generated text. Therefore, a more practical objective would be to allow the model to use this type of human feedback to improve its text generation.[^9]

Despite the clear benefits of incorporating human feedback in training models, prior efforts—including some that leverage [reinforcement learning](https://en.wikipedia.org/wiki/Reinforcement_learning "Reinforcement learning") (RL)—have encountered significant challenges. Most attempts were either narrow and difficult to generalize, breaking down on more complex tasks,[^10] [^11] [^12] [^13] or they faced difficulties learning from sparse (lacking specific information and relating to large amounts of text at a time) or noisy (inconsistently rewarding similar outputs) reward functions.[^14] [^15]

RLHF was not the first successful method of using human feedback for reinforcement learning, but it is one of the most widely used. The foundation for RLHF was introduced as an attempt to create a general algorithm for learning from a practical amount of human feedback.[^8] [^5] The algorithm as used today was introduced by [OpenAI](https://en.wikipedia.org/wiki/OpenAI "OpenAI") in a paper on enhancing text continuation or summarization based on human feedback, and it began to gain popularity when the same method was reused in their paper on [InstructGPT](https://en.wikipedia.org/wiki/InstructGPT "InstructGPT").[^4] [^16] [^17] RLHF has also been shown to improve the [robustness](https://en.wikipedia.org/wiki/Robust_optimization "Robust optimization") of RL agents and their capacity for [exploration](https://en.wikipedia.org/wiki/Exploration_\(reinforcement_learning\) "Exploration (reinforcement learning)"), which results in an optimization process more adept at handling [uncertainty](https://en.wikipedia.org/wiki/Uncertainty "Uncertainty") and efficiently exploring its environment in search of the highest reward.[^18]

Human feedback is commonly collected by prompting humans to rank instances of the agent's behavior.[^17] [^19] [^20] These rankings can then be used to score outputs, for example, using the [Elo rating system](https://en.wikipedia.org/wiki/Elo_rating_system "Elo rating system"), which is an algorithm for calculating the relative skill levels of players in a game based only on the outcome of each game.[^5] While ranking outputs is the most widely adopted form of feedback, recent research has explored other forms, such as numerical feedback, natural language feedback, and prompting for direct edits to the model's output.[^21]

One initial motivation of RLHF was that it requires relatively small amounts of comparison data to be effective.[^8] It has been shown that a small amount of data can lead to comparable results to a larger amount. In addition, increasing the amount of data tends to be less effective than proportionally increasing the size of the reward model.[^16] Nevertheless, a larger and more diverse amount of data can be crucial for tasks where it is important to avoid [bias](https://en.wikipedia.org/wiki/Algorithmic_bias "Algorithmic bias") from a partially [representative](https://en.wikipedia.org/wiki/Representative_sample "Representative sample") group of annotators.[^17]

When learning from human feedback through [pairwise comparison](https://en.wikipedia.org/wiki/Pairwise_comparison_\(psychology\) "Pairwise comparison (psychology)") under the [Bradley–Terry–Luce](https://en.wikipedia.org/wiki/Bradley%E2%80%93Terry%E2%80%93Luce "Bradley–Terry–Luce") model (or the [Plackett–Luce](https://en.wikipedia.org/wiki/Discrete_choice "Discrete choice") model for K-wise comparisons over more than two comparisons), the [maximum likelihood estimator](https://en.wikipedia.org/wiki/Maximum_likelihood_estimator "Maximum likelihood estimator") (MLE) for linear reward functions has been shown to [converge](https://en.wikipedia.org/wiki/Convergent_series "Convergent series") if the comparison data is generated under a well-specified [linear model](https://en.wikipedia.org/wiki/Linear_model "Linear model"). This implies that, under certain conditions, if a model is trained to decide which choices people would prefer between pairs (or groups) of choices, it will necessarily improve at predicting future preferences. This improvement is expected as long as the comparisons it learns from are based on a consistent and simple rule.[^22] [^23]

Both offline data collection models, where the model is learning by interacting with a static dataset and updating its policy in batches, as well as online data collection models, where the model directly interacts with the dynamic environment and updates its policy immediately, have been mathematically studied proving sample complexity bounds for RLHF under different feedback models.[^22] [^24]

In the offline data collection model, when the objective is policy training, a pessimistic MLE that incorporates a lower [confidence bound](https://en.wikipedia.org/wiki/Confidence_bound "Confidence bound") as the reward estimate is most effective. Moreover, when applicable, it has been shown that considering K-wise comparisons directly is [asymptotically more efficient](https://en.wikipedia.org/wiki/Efficiency_\(statistics\)#Asymptotic_efficiency "Efficiency (statistics)") than converting them into pairwise comparisons for prediction purposes.[^24] [^25] [^17]

In the online scenario, when human feedback is collected through pairwise comparisons under the Bradley–Terry–Luce model and the objective is to minimize the algorithm's [regret](https://en.wikipedia.org/wiki/Regret_\(decision_theory\) "Regret (decision theory)") (the difference in performance compared to an optimal agent), it has been shown that an optimistic MLE that incorporates an upper [confidence bound](https://en.wikipedia.org/wiki/Confidence_bound "Confidence bound") as the reward estimate can be used to design sample efficient algorithms (meaning that they require relatively little training data). A key challenge in RLHF when learning from pairwise (or dueling) comparisons is associated with the [non-Markovian](https://en.wikipedia.org/wiki/Markov_property "Markov property") nature of its optimal policies. Unlike simpler scenarios where the optimal strategy does [not require memory](https://en.wikipedia.org/wiki/Memoryless "Memoryless") of past actions, in RLHF, the best course of action often depends on previous events and decisions, making the strategy inherently memory-dependent.[^23]

## Applications

RLHF has been applied to various domains of [natural language processing](https://en.wikipedia.org/wiki/Natural_language_processing "Natural language processing") (NLP), such as conversational agents, text summarization, and natural language understanding.[^26] [^16] Ordinary reinforcement learning, in which agents learn from their actions based on a predefined "reward function", is difficult to apply to NLP tasks because the rewards tend to be difficult to define or measure, especially when dealing with complex tasks that involve human values or preferences.[^8] RLHF can steer NLP models, in particular [language models](https://en.wikipedia.org/wiki/Language_model "Language model"), to provide answers that [align](https://en.wikipedia.org/wiki/AI_alignment "AI alignment") with human preferences with regard to such tasks by capturing their preferences beforehand in the reward model. This results in a model capable of generating more relevant responses and rejecting inappropriate or irrelevant queries.[^17] [^27] Some notable examples of RLHF-trained language models are [OpenAI](https://en.wikipedia.org/wiki/OpenAI "OpenAI") 's [ChatGPT](https://en.wikipedia.org/wiki/ChatGPT "ChatGPT") (and its predecessor [InstructGPT](https://en.wikipedia.org/wiki/InstructGPT "InstructGPT")),[^19] [^28] [^29] [DeepMind](https://en.wikipedia.org/wiki/DeepMind "DeepMind") 's [Sparrow](https://en.wikipedia.org/wiki/Sparrow_\(chatbot\) "Sparrow (chatbot)"),[^30] [^31] [^32] [Google](https://en.wikipedia.org/wiki/Google "Google") 's [Gemini](https://en.wikipedia.org/wiki/Gemini_\(language_model\) "Gemini (language model)"),[^33] and [Anthropic](https://en.wikipedia.org/wiki/Anthropic "Anthropic") 's [Claude](https://en.wikipedia.org/wiki/Claude_\(language_model\) "Claude (language model)").[^34]

In computer vision, RLHF has also been used to align [text-to-image models](https://en.wikipedia.org/wiki/Text-to-image_model "Text-to-image model"). Studies that successfully used RLHF for this goal have noted that the use of [KL regularization](https://en.wikipedia.org/wiki/KL_divergence "KL divergence") in RLHF, which aims to prevent the learned policy from straying too far from the unaligned model, helped to stabilize the training process by reducing overfitting to the reward model. The final image outputs from models trained with KL regularization were noted to be of significantly higher quality than those trained without.[^35] [^36] Other methods tried to incorporate the feedback through more direct training—based on maximizing the reward without the use of reinforcement learning—but conceded that an RLHF-based approach would likely perform better due to the online sample generation used in RLHF during updates as well as the aforementioned KL regularization over the prior model, which mitigates [overfitting](https://en.wikipedia.org/wiki/Overfitting "Overfitting") to the reward function.[^37]

RLHF was initially applied to other areas, such as the development of [video game bots](https://en.wikipedia.org/wiki/Video_game_bot "Video game bot") and tasks in [simulated robotics](https://en.wikipedia.org/wiki/Robotics_simulator "Robotics simulator"). For example, OpenAI and DeepMind trained agents to play [Atari](https://en.wikipedia.org/wiki/Atari "Atari") games based on human preferences. In classical RL-based training of such bots, the reward function is simply correlated to how well the agent is performing in the game, usually using metrics like the in-game [score](https://en.wikipedia.org/wiki/Score_\(game\) "Score (game)"). In comparison, in RLHF, a human is periodically presented with two clips of the agent's behavior in the game and must decide which one *looks* better. This approach can teach agents to perform at a competitive level without ever having access to their score. In fact, it was shown that RLHF can sometimes lead to superior performance over RL with score metrics because the human's preferences can contain more useful information than performance-based metrics.[^8] [^38] The agents achieved strong performance in many of the environments tested, often surpassing human performance.[^39]

## Training

In RLHF, two different models are trained: a reward model and a [reinforcement learning](https://en.wikipedia.org/wiki/Reinforcement_learning "Reinforcement learning") policy. The reward model learns to determine what behavior is desirable based on human feedback, while the policy is guided by the reward model to determine the agent's actions. Both models are commonly initialized using a pre-trained [autoregressive](https://en.wikipedia.org/wiki/Autoregressive "Autoregressive") [language model](https://en.wikipedia.org/wiki/Language_model "Language model"). This model is then customarily trained in a [supervised](https://en.wikipedia.org/wiki/Supervised_learning "Supervised learning") manner on a relatively small dataset of pairs of prompts to an assistant and their accompanying responses, written by human annotators.

### Reward model

The **reward model** is a function that takes a [string](https://en.wikipedia.org/wiki/String_\(computer_science\) "String (computer science)") (piece of text) as input, and produces a single number, which is the "reward".[^40]

It is usually initialized with a pre-trained model, as this initializes it with an understanding of language and focuses training explicitly on learning human preferences. In addition to being used to initialize the reward model and the RL policy, the model is then also used to sample data to be compared by annotators.[^17] [^16]

The reward model is then trained by replacing the final layer of the previous model with a randomly initialized [regression](https://en.wikipedia.org/wiki/Regression_analysis "Regression analysis") head. This change shifts the model from its original [classification](https://en.wikipedia.org/wiki/Statistical_classification "Statistical classification") task over its vocabulary to simply outputting a number corresponding to the score of any given prompt and response. This model is trained on the human preference comparison data collected earlier from the supervised model. In particular, it is trained to [minimize](https://en.wikipedia.org/wiki/Mathematical_optimization "Mathematical optimization") the following [cross-entropy](https://en.wikipedia.org/wiki/Cross-entropy "Cross-entropy") loss function:
$$
{\displaystyle {\mathcal {L}}(\theta )=-{\frac {1}{K \choose 2}}E_{(x,y_{w},y_{l})}[\log(\sigma (r_{\theta }(x,y_{w})-r_{\theta }(x,y_{l})))]=-{\frac {1}{K \choose 2}}E_{(x,y_{w},y_{l})}\log \left[{\frac {e^{r_{\theta }(x,y_{w})}}{e^{r_{\theta }(x,y_{w})}+e^{r_{\theta }(x,y_{l})}}}\right]}
$$

where ${\displaystyle K}$ is the number of responses the labelers ranked, ${\displaystyle r_{\theta }(x,y)}$ is the output of the reward model for prompt ${\displaystyle x}$ and completion ${\displaystyle y}$, ${\displaystyle y_{w}}$ is the preferred completion over ${\displaystyle y_{l}}$, ${\displaystyle \sigma (x)}$ denotes the [sigmoid function](https://en.wikipedia.org/wiki/Sigmoid_function "Sigmoid function"), and ${\displaystyle E[X]}$ denotes the [expected value](https://en.wikipedia.org/wiki/Expected_value "Expected value").[^17] This can be thought of as a form of [logistic regression](https://en.wikipedia.org/wiki/Logistic_regression "Logistic regression"), where the model predicts the probability that a response ${\displaystyle y_{w}}$ is preferred over ${\displaystyle y_{l}}$.

This loss function essentially measures the difference between the reward model's predictions and the decisions made by humans. The goal is to make the model's guesses as close as possible to the humans' preferences by minimizing the difference measured by this equation. In the case of only pairwise comparisons, ${\displaystyle K=2}$, so the factor of ${\displaystyle 1/{\tbinom {K}{2}}=1}$.[^16] In general, all ${\displaystyle {\tbinom {K}{2}}}$ comparisons from each prompt are used for training as a single [batch](https://en.wikipedia.org/wiki/Batch_learning "Batch learning").[^17]

After training, the outputs of the model are normalized such that the reference completions have a mean score of 0. That is,[^16] ${\textstyle \sum _{y}r_{\theta }(x,y)=0}$ for each query and reference pair ${\displaystyle (x,y)}$ by calculating the mean reward across the training dataset and setting it as the bias in the reward head.

### Policy

The **policy model** is a function that takes a string as input, and produces another string. Usually in language modeling, the output string is not produced in one forward pass, but by multiple forward passes, generated autoregressively. Similarly to the reward model, the human feedback policy is also initialized from a pre-trained model.[^16]

The key is to understand language generation as if it is a game to be learned by RL. In RL, a policy is a function that maps a game state to a game action. In RLHF, the "game" is the game of replying to prompts. A prompt and all previously generated tokens are the game state, and generating a new token is a game action.[^41]

The first step in its training is supervised fine-tuning (SFT). This step does not require the reward model. Instead, the pre-trained model is trained on a dataset ${\displaystyle D_{SFT}}$ that contains prompt-response pairs ${\displaystyle (x,y)}$. Then, during SFT, the model is trained to auto-regressively generate the corresponding response ${\displaystyle y}$ when given a random prompt ${\displaystyle x}$. The original paper recommends to SFT for only one epoch, since more than that causes overfitting.

The dataset ${\displaystyle D_{SFT}}$ is usually written by human contractors, who write both the prompts and responses.

The second step uses a [policy gradient method](https://en.wikipedia.org/wiki/Policy_gradient_method "Policy gradient method") to the reward model. It uses a dataset ${\displaystyle D_{RL}}$, which contains prompts, but not responses. Like most policy gradient methods, this algorithm has an outer loop and two inner loops:

- Initialize the policy ${\displaystyle \pi _{\phi }^{RL}}$ to ${\displaystyle \pi ^{SFT}}$, the policy output from SFT.
- Loop for many steps.
	- Initialize a new empty dataset ${\displaystyle D_{\pi _{\phi }^{RL}}}$.
		- Loop for many steps
		- Sample a random prompt ${\displaystyle x}$ from ${\displaystyle D_{RL}}$.
				- Generate a response ${\displaystyle y}$ from the policy ${\displaystyle \pi _{\phi }^{RL}}$.
				- Calculate the reward signal ${\displaystyle r_{\theta }(x,y)}$ from the reward model ${\displaystyle r_{\theta }}$.
				- Add the triple ${\displaystyle (x,y,r_{\theta }(x,y))}$ to ${\displaystyle D_{\pi _{\phi }^{RL}}}$.
		- Update ${\displaystyle \phi }$ by a policy gradient method to increase the objective function 
		$$
		{\displaystyle {\text{objective}}(\phi )=E_{(x,y)\sim D_{\pi _{\phi }^{\text{RL}}}}\left[r_{\theta }(x,y)-\beta \log \left({\frac {\pi _{\phi }^{\text{RL}}(y|x)}{\pi ^{\text{SFT}}(y|x)}}\right)\right]}
		$$

Note that ${\displaystyle (x,y)\sim D_{\pi _{\phi }^{\text{RL}}}}$ is equivalent to ${\displaystyle x\sim D_{RL},y\sim \pi _{\phi }^{\text{RL}}(\cdot |x)}$, which means "sample a prompt from ${\displaystyle D_{RL}}$, then sample a response from the policy".

The objective function has two parts. The first part is simply the expected reward ${\displaystyle E[r]}$, and is standard for any RL algorithm. The second part is a "penalty term" involving the [KL divergence](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence "Kullback–Leibler divergence"). The strength of the penalty term is determined by the hyperparameter ${\displaystyle \beta }$.

This KL term works by penalizing the KL divergence (a measure of [statistical distance](https://en.wikipedia.org/wiki/Statistical_distance "Statistical distance") between distributions) between the model being fine-tuned and the initial supervised model. By choosing an appropriate ${\displaystyle \beta }$, the training can balance learning from new data while retaining useful information from the initial model, increasing [generalization](https://en.wikipedia.org/wiki/Generalization_\(learning\) "Generalization (learning)") by avoiding [fitting too closely](https://en.wikipedia.org/wiki/Overfitting "Overfitting") to the new data. Aside from preventing the new model from producing outputs too dissimilar those of the initial model, a second motivation of including the KL term is to encourage the model to output high- [entropy](https://en.wikipedia.org/wiki/Statistical_entropy "Statistical entropy") text, so as to prevent the model from [collapsing to a small number of canned responses](https://en.wikipedia.org/wiki/Mode_collapse "Mode collapse").[^16]

In simpler terms, the objective function calculates how well the policy's responses are expected to align with human feedback. The policy generates responses to prompts, and each response is evaluated both on how well it matches human preferences (as measured by the reward model) and how similar it is to responses the model would naturally generate. The goal is to balance improving alignment with human preferences while ensuring the model's responses remain diverse and not too far removed from what it has learned during its initial training. This helps the model not only to provide answers that people find useful or agreeable but also to maintain a broad understanding and avoid overly narrow or repetitive responses.

### Proximal policy optimization

The policy function is usually trained by [proximal policy optimization](https://en.wikipedia.org/wiki/Policy_gradient_method#Proximal_Policy_Optimization_\(PPO\) "Policy gradient method") (PPO) algorithm. That is, the parameter ${\displaystyle \phi }$ is trained by gradient ascent on the clipped surrogate function.[^17] [^16]

Classically, the PPO algorithm employs [generalized advantage estimation](https://en.wikipedia.org/wiki/Policy_gradient_method "Policy gradient method"), which means that there is an extra *value estimator* ${\displaystyle V_{\xi _{t}}(x)}$, that updates concurrently with the policy ${\displaystyle \pi _{\phi _{t}}^{RL}}$ during PPO training: ${\displaystyle \pi _{\phi _{t}}^{RL},V_{\xi _{t}},\pi _{\phi _{t+1}}^{RL},V_{\xi _{t+1}},\dots }$.[^42] The value estimator is used only during training, and not outside of training.

The PPO uses gradient descent on the following *clipped surrogate advantage*:
$$
{\displaystyle L_{\text{PPO}}(\phi ):=E_{x\sim D_{\text{RL}},y\sim \pi _{\phi _{t}}(y|x)}\left[\min \left({\frac {\pi _{\phi }^{RL}(y|x)}{\pi _{\phi _{t}}^{RL}(y|x)}}A(x,y),\mathrm {clip} \left({\frac {\pi _{\phi }^{RL}(y|x)}{\pi _{\phi _{t}}^{RL}(y|x)}},1-\epsilon ,1+\epsilon \right)A(x,y)\right)\right]}
$$

where the advantage term ${\displaystyle A(x,y)}$ is defined as ${\displaystyle r_{\theta }(x,y)-V_{\xi _{t}}(x)}$. That is, the advantage is computed as the difference between the reward (the expected return) and the value estimation (the expected return from the policy). This is used to train the policy by gradient *ascent* on it, usually using a standard momentum-gradient optimizer, like the [Adam optimizer](https://en.wikipedia.org/wiki/Adam_optimizer "Adam optimizer").

The original paper initialized the value estimator from the trained reward model.[^16] Since PPO is an actor-critic algorithm, the value estimator is updated concurrently with the policy, via minimizing the squared TD-error, which in this case equals the squared advantage term:
$$
{\displaystyle L_{\text{TD}}(\xi )=\mathbb {E} _{(x,y)\sim D{\pi _{\phi _{t}}^{\text{RL}}}}\left[\left(r_{\theta }(x,y)-\beta \log \left({\frac {\pi _{\phi _{t}}^{\text{RL}}(y|x)}{\pi ^{\text{SFT}}(y|x)}}\right)-V_{\xi }(x)\right)^{2}\right]}
$$
 which is minimized by gradient *descent* on it. Other methods than squared TD-error might be used. See the [actor-critic algorithm](https://en.wikipedia.org/wiki/Actor-critic_algorithm "Actor-critic algorithm") page for details.

### Mixing pretraining gradients

A third term is commonly added to the objective function to prevent the model from catastrophic forgetting. For example, if the model is only trained in customer service, then it might forget general knowledge in geography. To prevent this, the RLHF process incorporates the original language modeling objective. That is, some random texts ${\displaystyle x}$ are sampled from the original pretraining dataset ${\displaystyle D_{\text{pretrain}}}$, and the model is trained to maximize the log-likelihood of the text ${\displaystyle \log(\pi _{\phi }^{RL}(x))}$. The final objective function is written as:

$$
{\displaystyle L(\phi )=E_{(x,y)\sim D_{\pi _{\phi }^{\text{RL}}}}\left[r_{\theta }(x,y)-\beta \log \left({\frac {\pi _{\phi }^{\text{RL}}(y|x)}{\pi ^{\text{SFT}}(y|x)}}\right)\right]+\gamma E_{x\sim D_{\text{pretrain}}}[\log(\pi _{\phi }^{\text{RL}}(x))]}
$$

where ${\displaystyle \gamma }$ controls the strength of this pretraining term.[^17] This combined objective function is called PPO-ptx, where "ptx" means "Mixing Pretraining Gradients".[^9] It was first used in the InstructGPT paper.[^17]

In total, this objective function defines the method for adjusting the RL policy, blending the aim of aligning with human feedback and maintaining the model's original language understanding.

So, writing out fully explicitly, the PPO-ptx objective function is:

$$
{\displaystyle {\begin{aligned}L_{\text{PPO-ptx}}(\phi )&:=E_{(x,y)\sim D_{\pi _{\phi _{t}}^{\text{RL}}}}\left[\min \left({\frac {\pi _{\phi }^{RL}(y|x)}{\pi _{\phi _{t}}^{RL}(y|x)}}A(x,y),\mathrm {clip} \left({\frac {\pi _{\phi }^{RL}(y|x)}{\pi _{\phi _{t}}^{RL}(y|x)}},1-\epsilon ,1+\epsilon \right)A(x,y)\right)-\beta \log \left({\frac {\pi _{\phi }^{\text{RL}}(y|x)}{\pi ^{\text{SFT}}(y|x)}}\right)\right]\\&+\gamma E_{x\sim D_{\text{pretrain}}}[\log(\pi _{\phi }^{\text{RL}}(x))]\end{aligned}}}
$$
 which is optimized by gradient *ascent* on it.

## Limitations

RLHF suffers from challenges with collecting human feedback, learning a reward model, and optimizing the policy.[^43] Compared to data collection for techniques like [unsupervised](https://en.wikipedia.org/wiki/Unsupervised_learning "Unsupervised learning") or [self-supervised learning](https://en.wikipedia.org/wiki/Self-supervised_learning "Self-supervised learning"), collecting data for RLHF is less scalable and more expensive. Its quality and consistency may vary depending on the task, interface, and the preferences and biases of individual humans.[^17] [^44]

The effectiveness of RLHF depends on the quality of human feedback. For instance, the model may become [biased](https://en.wikipedia.org/wiki/Algorithmic_bias "Algorithmic bias"), favoring certain groups over others, if the feedback lacks impartiality, is inconsistent, or is incorrect.[^5] [^45] There is a risk of [overfitting](https://en.wikipedia.org/wiki/Overfit "Overfit"), where the model memorizes specific feedback examples instead of learning to [generalize](https://en.wikipedia.org/wiki/Generalization_\(learning\) "Generalization (learning)"). For instance, feedback predominantly from a specific demographic might lead the model to learn peculiarities or noise, along with the intended alignment. Excessive alignment to the specific feedback it received (that is, to the bias therein) can lead to the model performing sub-optimally in new contexts or when used by different groups.[^46] A single reward function cannot always represent the opinions of diverse groups of people. Even with a representative sample, conflicting views and preferences may result in the reward model favoring the majority's opinion, potentially disadvantaging underrepresented groups.[^43]

In some cases, as is possible in regular [reinforcement learning](https://en.wikipedia.org/wiki/Reinforcement_learning "Reinforcement learning"), there may be a risk of the model learning to manipulate the feedback process or [game the system](https://en.wikipedia.org/wiki/Game_the_system "Game the system") to achieve higher rewards rather than genuinely improving its performance.[^47] In the case of RLHF, a model may learn to exploit the fact that it is rewarded for what is evaluated positively and not necessarily for what is actually good, which can lead to it learning to persuade and manipulate. For example, models might learn that apparent confidence, even if inaccurate, garners higher rewards. Such behavior, if unchecked, is not just incentivized but can cause significant deployment issues due to the model's potential to mislead. Studies have found that humans are not skilled at identifying mistakes in LLM outputs in complex tasks; therefore, models learning to generate confident-sounding yet incorrect text can lead to significant issues when deployed.[^43]

## Alternatives

Similarly to RLHF, *reinforcement learning from AI feedback* (RLAIF) relies on training a preference model, except that the feedback is automatically generated.[^48] This is notably used in [Anthropic](https://en.wikipedia.org/wiki/Anthropic "Anthropic") 's [constitutional AI](https://en.wikipedia.org/wiki/Constitutional_AI "Constitutional AI"), where the AI feedback is based on the conformance to the principles of a constitution.[^49]

### Direct alignment algorithms

Direct alignment algorithms (DAA) have been proposed as a new class of algorithms [^50] [^51] that seek to directly optimize [large language models](https://en.wikipedia.org/wiki/Large_language_model "Large language model") (LLMs) on human feedback data in a [supervised](https://en.wikipedia.org/wiki/Supervised_learning "Supervised learning") manner instead of the traditional policy-gradient methods.

These algorithms aim to align models with human intent more transparently by removing the intermediate step of training a separate reward model. Instead of first predicting human preferences and then optimizing against those predictions, direct alignment methods train models end-to-end on human-labeled or curated outputs. This reduces potential misalignment risks introduced by proxy objectives or reward hacking.

By directly optimizing for the behavior preferred by humans, these approaches often enable tighter alignment with human values, improved [interpretability](https://en.wikipedia.org/wiki/Interpretability_\(machine_learning\) "Interpretability (machine learning)"), and simpler training pipelines compared to RLHF.

#### Direct preference optimization

Direct preference optimization (DPO) is a technique to learn human preferences. Like RLHF, it has been applied to [align](https://en.wikipedia.org/wiki/AI_alignment "AI alignment") pre-trained large language models using human-generated preference data. Unlike RLHF, however, which first trains a separate intermediate model to understand what good outcomes look like and then teaches the main model how to achieve those outcomes, DPO simplifies the process by directly adjusting the main model according to people's preferences. It uses a [change of variables](https://en.wikipedia.org/wiki/Change_of_variables "Change of variables") to define the "preference [loss](https://en.wikipedia.org/wiki/Loss_function "Loss function") " directly as a function of the policy and uses this loss to [fine-tune](https://en.wikipedia.org/wiki/Fine-tuning_\(deep_learning\) "Fine-tuning (deep learning)") the model, helping it understand and prioritize human preferences without needing a separate step. Essentially, this approach directly shapes the model's decisions based on positive or negative human feedback.

Recall, the pipeline of RLHF is as follows:

- We begin by gathering human preference dataset ${\displaystyle D}$.
- We then fit a reward model ${\displaystyle r^{*}}$ to data, by [maximum likelihood estimation](https://en.wikipedia.org/wiki/Maximum_likelihood_estimation "Maximum likelihood estimation") using the [Plackett–Luce model](https://en.wikipedia.org/wiki/Plackett%E2%80%93Luce_model "Plackett–Luce model") 
	$$
	{\displaystyle r^{*}=\arg \max _{r}\mathbb {E} _{(x,y_{1},\dots ,y_{N})\sim D}\left[\ln \prod _{k=1}^{N}{\frac {e^{r(x,y_{k})}}{\sum _{i=k}^{N}e^{r(x,y_{i})}}}\right]}
	$$
- We finally train an optimal policy ${\displaystyle \pi ^{*}}$ that maximizes the objective function:
	$$
	{\displaystyle \pi ^{*}=\arg \max _{\pi ^{\text{RL}}}\mathbb {E} _{(x,y)\sim D_{\pi ^{\text{RL}}}}\left[r^{*}(x,y)-\beta \log \left({\frac {\pi ^{\text{RL}}(y|x)}{\pi ^{\text{SFT}}(y|x)}}\right)\right]}
	$$

However, instead of doing the intermediate step of the reward model, DPO directly optimizes for the final policy.

First, solve directly for the optimal policy, which can be done by [Lagrange multipliers](https://en.wikipedia.org/wiki/Lagrange_multiplier "Lagrange multiplier"), as usual in [statistical mechanics](https://en.wikipedia.org/wiki/Statistical_mechanics "Statistical mechanics"):
$$
{\displaystyle \pi ^{*}(y|x)={\frac {\pi ^{\text{SFT}}(y|x)\exp(r^{*}(x,y)/\beta )}{Z(x)}},}
$$

where ${\displaystyle Z(x)}$ is the [partition function](https://en.wikipedia.org/wiki/Partition_function_\(statistical_mechanics\) "Partition function (statistical mechanics)"). This is unfortunately not tractable, since it requires summing over *all possible responses*: 
$$
{\displaystyle Z(x)=\sum _{y}\pi ^{\text{SFT}}(y|x)\exp(r^{*}(x,y)/\beta )=\mathbb {E} _{y\sim \pi ^{\text{SFT}}(\cdot |x)}[\exp(r^{*}(x,y)/\beta )]}
$$

Next, invert this relationship to express the reward implicitly in terms of the optimal policy:
$$
{\displaystyle r^{*}(x,y)=\beta \log {\frac {\pi ^{*}(y|x)}{\pi ^{\text{SFT}}(y|x)}}+\beta \log Z(x).}
$$

Finally, plug it back to the maximum likelihood estimator, we obtain [^52]<sup><span title="Location: Appendix A">: Appendix A</span> </sup> 
$$
{\displaystyle \pi ^{*}=\arg \max _{\pi }\mathbb {E} _{(x,y_{1},\dots ,y_{N})\sim D}\left[\ln \prod _{k=1}^{N}{\frac {e^{\beta \log {\frac {\pi (y_{k}|x)}{\pi ^{\text{SFT}}(y_{k}|x)}}}}{\sum _{i=k}^{N}e^{\beta \log {\frac {\pi (y_{i}|x)}{\pi ^{\text{SFT}}(y_{i}|x)}}}}}\right]}
$$

Usually, DPO is used for modeling human preference in pairwise comparisons, so that ${\displaystyle N=2}$. In that case, we have 
$$
{\displaystyle \pi ^{*}=\arg \max _{\pi }\mathbb {E} _{(x,y_{w},y_{l})\sim D}\left[\log \sigma \left(\beta \log {\frac {\pi (y_{w}|x)}{\pi ^{\text{SFT}}(y_{w}|x)}}-\beta \log {\frac {\pi (y_{l}|x)}{\pi ^{\text{SFT}}(y_{l}|x)}}\right)\right]}
$$

DPO eliminates the need for a separate reward model or reinforcement learning loop, treating alignment as a supervised learning problem over preference data. This is simpler to implement and train than RLHF and has been shown to produce comparable and sometimes superior results.[^52] Nevertheless, RLHF has also been shown to beat DPO on some datasets, for example, on benchmarks that attempt to measure truthfulness. Therefore, the choice of method may vary depending on the features of the human preference data and the nature of the task.[^53]

#### Identity preference optimization

Identity preference optimization (IPO) [^54] is a modification to the original DPO objective that introduces a regularization term to reduce the chance of overfitting even when preference data is noisy.

To solve this objective, IPO minimizes the quadratic loss function ${\displaystyle {\begin{aligned}&\mathbb {E} _{x,y_{w},y_{l}\sim D}[h_{\pi }(x,y_{w},y_{l})-{\frac {1}{2}}\beta ^{-1}]^{2}\end{aligned}}}$ where ${\displaystyle h_{\pi }(x,y_{w},y_{l})=\log \left({\frac {\pi _{\theta }(y_{w}|x)}{\pi _{\text{ref}}(y_{w}|x))}}\right)-\log \left({\frac {\pi _{\theta }(y_{l}|x)}{\pi _{\text{ref}}(y_{l}|x)}}\right)}$.

IPO can control the gap between the log-likelihood ratios of the policy model and the reference by always regularizing the solution towards the reference model. It allows learning directly from preferences without a reward modelling stage and without relying on the [Bradley-Terry modelling](https://en.wikipedia.org/wiki/Bradley%E2%80%93Terry_model "Bradley–Terry model") assumption that assumes that pairwise preferences can be substituted with pointwise rewards.[^54]

#### Kahneman-Tversky optimization

Kahneman-Tversky optimization (KTO) [^55] is another direct alignment algorithm drawing from [prospect theory](https://en.wikipedia.org/wiki/Prospect_theory "Prospect theory") to model uncertainty in human decisions. Unlike DPO, KTO requires only a binary feedback signal (desirable or undesirable) instead of explicit preference pairs.

The value function ${\displaystyle v(x,y)}$ is defined piecewise depending on whether ${\displaystyle y}$ is desirable (${\displaystyle \lambda _{D}}$) or undesirable (${\displaystyle \lambda _{U}}$):

$$
{\displaystyle v(x,y)\;=\;{\begin{cases}\lambda _{D}\,\sigma \!{\bigl (}\,\beta \,{\bigl (}r_{\theta }(x,y)\;-\;z_{0}{\bigr )}{\bigr )},&\quad {\text{if }}y\sim y_{\mathrm {desirable} \mid x},\\[6pt]\lambda _{U}\,\sigma \!{\bigl (}\,\beta \,{\bigl (}z_{0}\;-\;r_{\theta }(x,y){\bigr )}{\bigr )},&\quad {\text{if }}y\sim y_{\mathrm {undesirable} \mid x}\end{cases}}}
$$

Here, ${\displaystyle \beta }$ controls how “risk-averse” the value function is (larger ${\displaystyle \beta }$ = faster saturation in the logistic function ${\displaystyle \sigma }$)and ${\textstyle z_{0}=\mathrm {KL} \!{\Bigl (}\,\pi _{\theta }(y'\mid x)\;{\big \Vert }\;\pi _{\mathrm {ref} }(y'\mid x){\Bigr )}}$ is a baseline given by the Kullback–Leibler divergence. Since many real-world feedback pipelines yield "like/dislike" data more easily than pairwise comparisons, KTO is designed to be data-efficient and to reflect "loss aversion" more directly by using a straightforward notion of "good vs. bad" at the example level.

[^1]: Kongot, Aparna (2025). [*Human-Centered AI: An Illustrated Scientific Quest (Human–Computer Interaction Series)*](https://www.google.com/books/edition/Human_Centered_AI_An_Illustrated_Scienti/XmNSEQAAQBAJ?hl=en&gbpv=1&dq=%22reinforcement+learning+from+human+feedback%22&pg=PA389&printsec=frontcover). Springer. p. 389. [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [978-3031613746](https://en.wikipedia.org/wiki/Special:BookSources/978-3031613746 "Special:BookSources/978-3031613746").

[^2]: Lan, Xuguang (2025). [*Intelligent Robotics and Applications: 17th International Conference, ICIRA 2024, Xi'an, China, July 31 – August 2, 2024, Proceedings, Part VIII (Lecture Notes in Computer Science Book 15208)*](https://www.google.com/books/edition/Intelligent_Robotics_and_Applications/icVAEQAAQBAJ?hl=en&gbpv=1&dq=%22reinforcement+learning+from+human+feedback%22&pg=PA6&printsec=frontcover). Springer. p. 6.

[^3]: Russell, Stuart J.; Norvig, Peter (2016). *Artificial intelligence: a modern approach* (Third, Global ed.). Boston Columbus Indianapolis New York San Francisco Upper Saddle River Amsterdam Cape Town Dubai London Madrid Milan Munich Paris Montreal Toronto Delhi Mexico City Sao Paulo Sydney Hong Kong Seoul Singapore Taipei Tokyo: Pearson. pp. 830–831. [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [978-0-13-604259-4](https://en.wikipedia.org/wiki/Special:BookSources/978-0-13-604259-4 "Special:BookSources/978-0-13-604259-4").

[^4]: Ziegler, Daniel M.; Stiennon, Nisan; Wu, Jeffrey; Brown, Tom B.; Radford, Alec; Amodei, Dario; Christiano, Paul; Irving, Geoffrey (2019). "Fine-Tuning Language Models from Human Preferences". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[1909.08593](https://arxiv.org/abs/1909.08593) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^5]: Lambert, Nathan; Castricato, Louis; von Werra, Leandro; Havrilla, Alex. ["Illustrating Reinforcement Learning from Human Feedback (RLHF)"](https://huggingface.co/blog/rlhf). *huggingface.co*. Retrieved 4 March 2023.

[^6]: Schulman, John; Wolski, Filip; Dhariwal, Prafulla; Radford, Alec; Klimov, Oleg (2017). "Proximal Policy Optimization Algorithms". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[1707.06347](https://arxiv.org/abs/1707.06347) \[[cs.LG](https://arxiv.org/archive/cs.LG)\].

[^7]: Tuan, Yi-Lin; Zhang, Jinzhi; Li, Yujia; Lee, Hung-yi (2018). "Proximal Policy Optimization and its Dynamic Version for Sequence Generation". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[1808.07982](https://arxiv.org/abs/1808.07982) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^8]: Amodei, Dario; Christiano, Paul; Ray, Alex (13 June 2017). ["Learning from human preferences"](https://openai.com/research/learning-from-human-preferences). *openai.com*. Retrieved 4 March 2023.

[^9]: Zheng, Rui; Dou, Shihan; Gao, Songyang; Hua, Yuan; Shen, Wei; Wang, Binghai; Liu, Yan; Jin, Senjie; Liu, Qin; Zhou, Yuhao; Xiong, Limao; Chen, Lu; Xi, Zhiheng; Xu, Nuo; Lai, Wenbin; Zhu, Minghao; Chang, Cheng; Yin, Zhangyue; Weng, Rongxiang; Cheng, Wensen; Huang, Haoran; Sun, Tianxiang; Yan, Hang; Gui, Tao; Zhang, Qi; Qiu, Xipeng; Huang, Xuanjing (2023). "Secrets of RLHF in Large Language Models Part I: PPO". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2307.04964](https://arxiv.org/abs/2307.04964) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^10]: Knox, W. Bradley; Stone, Peter; Breazeal, Cynthia (2013). ["Training a Robot via Human Feedback: A Case Study"](https://link.springer.com/chapter/10.1007/978-3-319-02675-6_46). *Social Robotics*. Lecture Notes in Computer Science. Vol. 8239. Springer International Publishing. pp. 460–470. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1007/978-3-319-02675-6\_46](https://doi.org/10.1007%2F978-3-319-02675-6_46). [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [978-3-319-02674-9](https://en.wikipedia.org/wiki/Special:BookSources/978-3-319-02674-9 "Special:BookSources/978-3-319-02674-9"). Retrieved 26 February 2024.

[^11]: Akrour, Riad; Schoenauer, Marc; Sebag, Michèle (2012). ["APRIL: Active Preference Learning-Based Reinforcement Learning"](https://link.springer.com/chapter/10.1007/978-3-642-33486-3_8). *Machine Learning and Knowledge Discovery in Databases*. Lecture Notes in Computer Science. Vol. 7524. Springer. pp. 116–131. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[1208.0984](https://arxiv.org/abs/1208.0984). [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1007/978-3-642-33486-3\_8](https://doi.org/10.1007%2F978-3-642-33486-3_8). [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [978-3-642-33485-6](https://en.wikipedia.org/wiki/Special:BookSources/978-3-642-33485-6 "Special:BookSources/978-3-642-33485-6"). Retrieved 26 February 2024.

[^12]: Wilson, Aaron; Fern, Alan; Tadepalli, Prasad (2012). ["A Bayesian Approach for Policy Learning from Trajectory Preference Queries"](https://papers.nips.cc/paper_files/paper/2012/hash/16c222aa19898e5058938167c8ab6c57-Abstract.html). *Advances in Neural Information Processing Systems*. **25**. Curran Associates, Inc. Retrieved 26 February 2024.

[^13]: Schoenauer, Marc; Akrour, Riad; Sebag, Michele; Souplet, Jean-Christophe (18 June 2014). ["Programming by Feedback"](https://proceedings.mlr.press/v32/schoenauer14.html). *Proceedings of the 31st International Conference on Machine Learning*. PMLR: 1503–1511. Retrieved 26 February 2024.

[^14]: Warnell, Garrett; Waytowich, Nicholas; Lawhern, Vernon; Stone, Peter (25 April 2018). "Deep TAMER: Interactive Agent Shaping in High-Dimensional State Spaces". *Proceedings of the AAAI Conference on Artificial Intelligence*. **32** (1). [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[1709.10163](https://arxiv.org/abs/1709.10163). [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1609/aaai.v32i1.11485](https://doi.org/10.1609%2Faaai.v32i1.11485). [S2CID](https://en.wikipedia.org/wiki/S2CID_\(identifier\) "S2CID (identifier)") [4130751](https://api.semanticscholar.org/CorpusID:4130751).

[^15]: MacGlashan, James; Ho, Mark K.; Loftin, Robert; Peng, Bei; Wang, Guan; Roberts, David L.; Taylor, Matthew E.; Littman, Michael L. (6 August 2017). ["Interactive learning from policy-dependent human feedback"](https://dl.acm.org/doi/10.5555/3305890.3305917). *Proceedings of the 34th International Conference on Machine Learning - Volume 70*. JMLR.org: 2285–2294. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[1701.06049](https://arxiv.org/abs/1701.06049).

[^16]: Nisan Stiennon; Long Ouyang; Jeffrey Wu; Daniel Ziegler; Ryan Lowe; Chelsea Voss; Alec Radford; Dario Amodei; Paul F. Christiano (2020). ["Learning to summarize with human feedback"](https://proceedings.neurips.cc/paper/2020/hash/1f89885d556929e98d3ef9b86448f951-Abstract.html). *Advances in Neural Information Processing Systems*. **33**.

[^17]: Ouyang, Long; Wu, Jeffrey; Jiang, Xu; Almeida, Diogo; Wainwright, Carroll; Mishkin, Pamela; Zhang, Chong; Agarwal, Sandhini; Slama, Katarina; Gray, Alex; Schulman, John; Hilton, Jacob; Kelton, Fraser; Miller, Luke; Simens, Maddie; Askell, Amanda; Welinder, Peter; Christiano, Paul; Leike, Jan; Lowe, Ryan (31 October 2022). [*Training language models to follow instructions with human feedback*](https://openreview.net/forum?id=TG8KACxEON). Thirty-Sixth Conference on Neural Information Processing Systems: NeurIPS 2022. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2203.02155](https://arxiv.org/abs/2203.02155).

[^18]: Bai, Yuntao; Jones, Andy; Ndousse, Kamal; Askell, Amanda; Chen, Anna; DasSarma, Nova; Drain, Dawn; Fort, Stanislav; Ganguli, Deep; Henighan, Tom; Joseph, Nicholas; Kadavath, Saurav; Kernion, Jackson; Conerly, Tom; El-Showk, Sheer; Elhage, Nelson; Hatfield-Dodds, Zac; Hernandez, Danny; Hume, Tristan; Johnston, Scott; Kravec, Shauna; Lovitt, Liane; Nanda, Neel; Olsson, Catherine; Amodei, Dario; Brown, Tom; Clark, Jack; McCandlish, Sam; Olah, Chris; Mann, Ben; Kaplan, Jared (2022). "Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2204.05862](https://arxiv.org/abs/2204.05862) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^19]: Edwards, Benj (1 December 2022). ["OpenAI invites everyone to test ChatGPT, a new AI-powered chatbot—with amusing results"](https://arstechnica.com/information-technology/2022/12/openai-invites-everyone-to-test-new-ai-powered-chatbot-with-amusing-results/). *Ars Technica*. Retrieved 4 March 2023.

[^20]: Abhishek, Gupta (5 February 2023). ["Getting stakeholder engagement right in responsible AI"](https://venturebeat.com/ai/getting-stakeholder-engagement-right-in-responsible-ai/). *VentureBeat*. Retrieved 4 March 2023.

[^21]: Fernandes, Patrick; Madaan, Aman; Liu, Emmy; Farinhas, António; Pedro Henrique Martins; Bertsch, Amanda; de Souza, José G. C.; Zhou, Shuyan; Wu, Tongshuang; Neubig, Graham; Martins, André F. T. (2023). "Bridging the Gap: A Survey on Integrating (Human) Feedback for Natural Language Generation". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2305.00955](https://arxiv.org/abs/2305.00955) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^22]: Xie, Tengyang; Jiang, Nan; Wang, Huan; Xiong, Caiming; Bai, Yu (2021). ["Policy Finetuning: Bridging Sample-Efficient Offline and Online Reinforcement Learning"](https://proceedings.neurips.cc/paper/2021/hash/e61eaa38aed621dd776d0e67cfeee366-Abstract.html). *Advances in Neural Information Processing Systems*. **34**. Curran Associates, Inc.: 27395–27407. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2106.04895](https://arxiv.org/abs/2106.04895). Retrieved 10 March 2024.

[^23]: Pacchiano, Aldo; Saha, Aadirupa; Lee, Jonathan (2023-03-03). ["Dueling RL: Reinforcement Learning with Trajectory Preferences"](https://proceedings.mlr.press/v206/saha23a.html). *Proceedings of the 26th International Conference on Artificial Intelligence and Statistics*. PMLR: 6263–6289. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2111.04850](https://arxiv.org/abs/2111.04850).

[^24]: Zhu, Banghua; Jordan, Michael; Jiao, Jiantao (2023-07-03). ["Principled Reinforcement Learning with Human Feedback from Pairwise or K-wise Comparisons"](https://proceedings.mlr.press/v202/zhu23f.html). *Proceedings of the 40th International Conference on Machine Learning*. PMLR: 43037–43067. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2301.11270](https://arxiv.org/abs/2301.11270).

[^25]: Li, Zihao; Yang, Zhuoran; Wang, Mengdi (20 June 2023). ["Reinforcement learning with Human Feedback: Learning Dynamic Choices via Pessimism"](https://openreview.net/forum?id=gxM2AUFMsK&referrer=%5Bthe%20profile%20of%20Zhuoran%20Yang%5D\(%2Fprofile%3Fid%3D~Zhuoran_Yang1\)). *ILHF Workshop ICML 2023*. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2305.18438](https://arxiv.org/abs/2305.18438). Retrieved 10 March 2024.

[^26]: Ouyang, Long; Wu, Jeff; Jiang, Xu; Almeida, Diogo; Wainwright, Carroll L.; Mishkin, Pamela; Zhang, Chong; Agarwal, Sandhini; Slama, Katarina; Ray, Alex; Schulman, John; Hilton, Jacob; Kelton, Fraser; Miller, Luke; Simens, Maddie; Askell, Amanda; Welinder, Peter; Christiano, Paul; Leike, Jan; Lowe, Ryan (2022). "Training language models to follow instructions with human feedback". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2203.02155](https://arxiv.org/abs/2203.02155) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^27]: Wiggers, Kyle (24 February 2023). ["Can AI really be protected from text-based attacks?"](https://techcrunch.com/2023/02/24/can-language-models-really-be-protected-from-text-based-attacks/). *TechCrunch*. Retrieved 4 March 2023.

[^28]: Heikkilä, Melissa (21 February 2023). ["How OpenAI is trying to make ChatGPT safer and less biased"](https://www.technologyreview.com/2023/02/21/1068893/how-openai-is-trying-to-make-chatgpt-safer-and-less-biased/). *MIT Technology Review*. Retrieved 4 March 2023.

[^29]: Douglas Heaven, Will (30 November 2022). ["ChatGPT is OpenAI's latest fix for GPT-3. It's slick but still spews nonsense"](https://www.technologyreview.com/2022/11/30/1063878/openai-still-fixing-gpt3-ai-large-language-model/). *MIT Technology Review*. Retrieved 4 March 2023.

[^30]: Glaese, Amelia; McAleese, Nat; Trębacz, Maja; Aslanides, John; Firoiu, Vlad; Ewalds, Timo; Rauh, Maribeth; Weidinger, Laura; Chadwick, Martin; Thacker, Phoebe; Campbell-Gillingham, Lucy; Uesato, Jonathan; Huang, Po-Sen; Comanescu, Ramona; Yang, Fan; See, Abigail; Dathathri, Sumanth; Greig, Rory; Chen, Charlie; Fritz, Doug; Elias, Jaume Sanchez; Green, Richard; Mokrá, Soňa; Fernando, Nicholas; Wu, Boxi; Foley, Rachel; Young, Susannah; Gabriel, Iason; Isaac, William; Mellor, John; Hassabis, Demis; Kavukcuoglu, Koray; Hendricks, Lisa Anne; Irving, Geoffrey (2022). "Improving alignment of dialogue agents via targeted human judgements". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2209.14375](https://arxiv.org/abs/2209.14375) \[[cs.LG](https://arxiv.org/archive/cs.LG)\].

[^31]: Goldman, Sharon (23 September 2022). ["Why DeepMind isn't deploying its new AI chatbot — and what it means for responsible AI"](https://venturebeat.com/ai/why-deepmind-isnt-deploying-its-new-ai-chatbot). *VentureBeat*. Retrieved 4 March 2023.

[^32]: The Sparrow team (22 September 2022). ["Building safer dialogue agents"](https://www.deepmind.com/blog/building-safer-dialogue-agents). *www.deepmind.com*. Retrieved 4 March 2023.

[^33]: Pinchai, Sundar; Hassabis, Demis (6 December 2023). ["Introducing Gemini: our largest and most capable AI model"](https://blog.google/technology/ai/google-gemini-ai/). *Google*. Retrieved 29 February 2024.

[^34]: Henshall, Will (18 July 2023). ["What to Know About Claude 2, Anthropic's Rival to ChatGPT"](https://time.com/6295523/claude-2-anthropic-chatgpt/). *TIME*. Retrieved 6 March 2024.

[^35]: Fan, Ying; Watkins, Olivia; Du, Yuqing; Liu, Hao; Ryu, Moonkyung; Boutilier, Craig; Abbeel, Pieter; Ghavamzadeh, Mohammad; Lee, Kangwook; Lee, Kimin (2 November 2023). ["DPOK: Reinforcement Learning for Fine-tuning Text-to-Image Diffusion Models"](https://openreview.net/forum?id=8OTPepXzeh&referrer=%5Bthe%20profile%20of%20Moonkyung%20Ryu%5D\(%2Fprofile%3Fid%3D~Moonkyung_Ryu1\)). *NeurIPS 2023*. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2305.16381](https://arxiv.org/abs/2305.16381). Retrieved 1 March 2024.

[^36]: Xu, Jiazheng; Liu, Xiao; Wu, Yuchen; Tong, Yuxuan; Li, Qinkai; Ding, Ming; Tang, Jie; Dong, Yuxiao (15 December 2023). ["ImageReward: Learning and Evaluating Human Preferences for Text-to-Image Generation"](https://proceedings.neurips.cc/paper_files/paper/2023/hash/33646ef0ed554145eab65f6250fab0c9-Abstract-Conference.html). *Advances in Neural Information Processing Systems*. **36**: 15903–15935. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2304.05977](https://arxiv.org/abs/2304.05977). Retrieved 1 March 2024.

[^37]: Lee, Kimin; Liu, Hao; Ryu, Moonkyung; Watkins, Olivia; Du, Yuqing; Boutilier, Craig; Abbeel, Pieter; Ghavamzadeh, Mohammad; Gu, Shixiang Shane (2023). "Aligning Text-to-Image Models using Human Feedback". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2302.12192](https://arxiv.org/abs/2302.12192) \[[cs.LG](https://arxiv.org/archive/cs.LG)\].

[^38]: Leike, Jan; Martic, Miljan; Legg, Shane (12 June 2017). ["Learning through human feedback"](https://www.deepmind.com/blog/learning-through-human-feedback). *www.deepmind.com*. Retrieved 4 March 2023.

[^39]: Christiano, Paul F; Leike, Jan; Brown, Tom; Martic, Miljan; Legg, Shane; Amodei, Dario (2017). ["Deep Reinforcement Learning from Human Preferences"](https://papers.nips.cc/paper/2017/hash/d5e2c0adad503c91f91df240d0cd4e49-Abstract.html). *Advances in Neural Information Processing Systems*. **30**. Curran Associates, Inc. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[1706.03741](https://arxiv.org/abs/1706.03741). Retrieved 4 March 2023.

[^40]: von Csefalvay, Chris (2026). "4. Reinforcement Learning: Better Each Time". *Post-Training: A Practical Guide for AI Engineers and Developers*. No Starch Press. pp. 114–116. [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [978-1-7185-0520-9](https://en.wikipedia.org/wiki/Special:BookSources/978-1-7185-0520-9 "Special:BookSources/978-1-7185-0520-9").

[^41]: Iusztin, Paul (2024). [*LLM Engineer's Handbook: Master the art of engineering large language models from concept to production*](https://www.google.com/books/edition/LLM_Engineer_s_Handbook/jHEqEQAAQBAJ?hl=en&gbpv=1&dq=%22reinforcement+learning+from+human+feedback%22&pg=PA246&printsec=frontcover). Packt Publishing. p. 246. [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [978-1836200079](https://en.wikipedia.org/wiki/Special:BookSources/978-1836200079 "Special:BookSources/978-1836200079").

[^42]: von Csefalvay, Chris (2026). "5. Preference Optimization: Modern Alternatives to PPO". *Post-Training: A Practical Guide for AI Engineers and Developers*. No Starch Press. pp. 133–140. [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [978-1-7185-0520-9](https://en.wikipedia.org/wiki/Special:BookSources/978-1-7185-0520-9 "Special:BookSources/978-1-7185-0520-9").

[^43]: Casper, Stephen; Davies, Xander; Shi, Claudia; Gilbert, Thomas Krendl; Scheurer, Jérémy; Rando, Javier; Freedman, Rachel; Korbak, Tomasz; Lindner, David; Freire, Pedro; Wang, Tony Tong; Marks, Samuel; Segerie, Charbel-Raphael; Carroll, Micah; Peng, Andi; Christoffersen, Phillip; Damani, Mehul; Slocum, Stewart; Anwar, Usman; Siththaranjan, Anand; Nadeau, Max; Michaud, Eric J.; Pfau, Jacob; Krasheninnikov, Dmitrii; Chen, Xin; Langosco, Lauro; Hase, Peter; Biyik, Erdem; Dragan, Anca; Krueger, David; Sadigh, Dorsa; Hadfield-Menell, Dylan (18 September 2023). ["Open Problems and Fundamental Limitations of Reinforcement Learning from Human Feedback"](https://openreview.net/forum?id=bx24KpJ4Eb). *Transactions on Machine Learning Research*. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2307.15217](https://arxiv.org/abs/2307.15217).

[^44]: Christiano, Paul (25 January 2023). ["Thoughts on the impact of RLHF research"](https://www.alignmentforum.org/posts/vwu4kegAEZTBtpT6p/thoughts-on-the-impact-of-rlhf-research). Retrieved 4 March 2023.

[^45]: Belenguer, Lorenzo (2022). ["AI bias: exploring discriminatory algorithmic decision-making models and the application of possible machine-centric solutions adapted from the pharmaceutical industry"](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8830968). *AI and Ethics*. **2** (4). AI Ethics: 771–787. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1007/s43681-022-00138-8](https://doi.org/10.1007%2Fs43681-022-00138-8). [PMC](https://en.wikipedia.org/wiki/PMC_\(identifier\) "PMC (identifier)") [8830968](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8830968). [PMID](https://en.wikipedia.org/wiki/PMID_\(identifier\) "PMID (identifier)") [35194591](https://pubmed.ncbi.nlm.nih.gov/35194591).

[^46]: Zhang, Chiyuan; Bengio, Samy; Hardt, Moritz; Recht, Benjamin; Vinyals, Oriol (4 November 2016). ["Understanding deep learning requires rethinking generalization"](https://openreview.net/forum?id=Sy8gdB9xx). International Conference on Learning Representations.

[^47]: Clark, Jack; Amodei, Dario (21 December 2016). ["Faulty reward functions in the wild"](https://openai.com/research/faulty-reward-functions). OpenAI.

[^48]: Lee, Harrison; Phatale, Samrat; Mansoor, Hassan; Lu, Kellie Ren; Mesnard, Thomas; Ferret, Johan; Bishop, Colton; Hall, Ethan; Carbune, Victor; Rastogi, Abhinav (2023-10-13). ["RLAIF: Scaling Reinforcement Learning from Human Feedback with AI Feedback"](https://openreview.net/forum?id=AAxIs3D2ZZ). *ICLR*.

[^49]: Edwards, Benj (2023-05-09). ["AI gains "values" with Anthropic's new Constitutional AI chatbot approach"](https://arstechnica.com/information-technology/2023/05/ai-with-a-moral-compass-anthropic-outlines-constitutional-ai-in-its-claude-chatbot/). *Ars Technica*. Retrieved 2024-04-27.

[^50]: Rafailov, Rafael; Chittepu, Yaswanth; Park, Ryan; Sikchi, Harshit; Hejna, Joey; Knox, Bradley; Finn, Chelsea; Niekum, Scott (2024). "Scaling Laws for Reward Model Overoptimization in Direct Alignment Algorithms". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2406.02900](https://arxiv.org/abs/2406.02900) \[[cs.LG](https://arxiv.org/archive/cs.LG)\].

[^51]: Shi, Zhengyan; Land, Sander; Locatelli, Acyr; Geist, Matthieu; Bartolo, Max (2024). "Understanding Likelihood Over-optimisation in Direct Alignment Algorithms". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2410.11677](https://arxiv.org/abs/2410.11677) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^52]: Rafailov, Rafael; Sharma, Archit; Mitchell, Eric; Ermon, Stefano; Manning, Christopher D.; Finn, Chelsea (2023). "Direct Preference Optimization: Your Language Model is Secretly a Reward Model". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2305.18290](https://arxiv.org/abs/2305.18290) \[[cs.LG](https://arxiv.org/archive/cs.LG)\].

[^53]: Wang, Zhilin; Dong, Yi; Zeng, Jiaqi; Adams, Virginia; Sreedhar, Makesh Narsimhan; Egert, Daniel; Delalleau, Olivier; Scowcroft, Jane Polak; Kant, Neel; Swope, Aidan; Kuchaiev, Oleksii (2023). "HelpSteer: Multi-attribute Helpfulness Dataset for SteerLM". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2311.09528](https://arxiv.org/abs/2311.09528) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^54]: Mohammad Gheshlaghi Azar; Rowland, Mark; Piot, Bilal; Guo, Daniel; Calandriello, Daniele; Valko, Michal; Munos, Rémi (2023). "A General Theoretical Paradigm to Understand Learning from Human Preferences". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2310.12036](https://arxiv.org/abs/2310.12036) \[[cs.AI](https://arxiv.org/archive/cs.AI)\].

[^55]: Ethayarajh, Kawin; Xu, Winnie; Muennighoff, Niklas; Jurafsky, Dan; Kiela, Douwe (2024). "KTO: Model Alignment as Prospect Theoretic Optimization". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2402.01306](https://arxiv.org/abs/2402.01306) \[[cs.LG](https://arxiv.org/archive/cs.LG)\].