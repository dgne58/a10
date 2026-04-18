---
title: "Recursive self-improvement - Wikipedia"
source: "https://en.wikipedia.org/wiki/Recursive_self-improvement"
author:
  - "[[Contributors to Wikimedia projects]]"
published: 2004-11-13
created: 2026-04-13
description:
tags:
  - "clippings"
---
**Recursive self-improvement** (**RSI**) is a process in which early [artificial general intelligence](https://en.wikipedia.org/wiki/Artificial_general_intelligence "Artificial general intelligence") (AGI) systems rewrite their own computer code, causing an [intelligence explosion](https://en.wikipedia.org/wiki/Intelligence_explosion "Intelligence explosion") resulting from enhancing their own capabilities and intellectual capacity, theoretically resulting in [superintelligence](https://en.wikipedia.org/wiki/Superintelligence "Superintelligence").[^1] [^2]

The development of recursive self-improvement raises significant [ethical](https://en.wikipedia.org/wiki/Ethics_of_artificial_intelligence "Ethics of artificial intelligence") and [safety](https://en.wikipedia.org/wiki/AI_safety "AI safety") concerns, as such systems may evolve in unforeseen ways and could potentially surpass human control or understanding.[^3]

## Seed improver

The concept of a "seed improver" architecture is a foundational framework that equips an AGI system with the initial capabilities required for recursive self-improvement. This might come in many forms or variations.

The term "Seed AI" was coined by [Eliezer Yudkowsky](https://en.wikipedia.org/wiki/Eliezer_Yudkowsky "Eliezer Yudkowsky").[^4]

### Hypothetical example

The concept begins with a hypothetical "seed improver", an initial code-base developed by human engineers that equips an advanced future [large language model](https://en.wikipedia.org/wiki/Large_language_model "Large language model") (LLM) built with strong or expert-level capabilities to [program software](https://en.wikipedia.org/wiki/Computer_programming "Computer programming"). These capabilities include planning, reading, writing, [compiling](https://en.wikipedia.org/wiki/Compiling "Compiling"), [testing](https://en.wikipedia.org/wiki/Software_testing "Software testing"), and executing arbitrary code. The system is designed to maintain its original goals and perform validations to ensure its abilities do not degrade over iterations.[^5] [^6] [^7]

#### Initial architecture

The initial architecture includes a goal-following [autonomous agent](https://en.wikipedia.org/wiki/Agent-based_model "Agent-based model"), that can take actions, continuously learns, adapts, and modifies itself to become more efficient and effective in achieving its goals.

The seed improver may include various components such as:

Recursive self-prompting loop

Configuration to enable the LLM to recursively self-prompt itself to achieve a given task or goal, creating an execution loop which forms the basis of an [agent](https://en.wikipedia.org/wiki/Agent-based_model "Agent-based model") that can complete a long-term goal or task through iteration.

Basic programming capabilities

The seed improver provides the AGI with fundamental abilities to read, write, compile, test, and execute code. This enables the system to modify and improve its own codebase and algorithms.

[Goal-oriented design](https://en.wikipedia.org/wiki/Goal_orientation "Goal orientation")

The AGI is programmed with an initial goal, such as "improve your capabilities". This goal guides the system's actions and development trajectory.

Validation and Testing Protocols

An initial [suite of tests](https://en.wikipedia.org/wiki/Test_suite "Test suite") and validation protocols that ensure the agent does not regress in capabilities or derail itself. The agent would be able to add more tests in order to test new capabilities it might develop for itself. This forms the basis for a kind of [self-directed evolution](https://en.wikipedia.org/wiki/Evolutionary_algorithm "Evolutionary algorithm"), where the agent can perform a kind of [artificial selection](https://en.wikipedia.org/wiki/Selective_breeding "Selective breeding"), changing its software as well as its hardware.

#### General capabilities

This system forms a sort of generalist [Turing-complete](https://en.wikipedia.org/wiki/Turing_completeness "Turing completeness") [programmer](https://en.wikipedia.org/wiki/Programmer "Programmer") which can in theory develop and run any kind of software. The agent might use these capabilities to for example:

- Create tools that enable it full access to the internet, and integrate itself with external technologies.
- Clone/ [fork](https://en.wikipedia.org/wiki/Fork_\(software_development\) "Fork (software development)") itself to delegate tasks and increase its speed of self-improvement.
- Modify its [cognitive architecture](https://en.wikipedia.org/wiki/Cognitive_architecture "Cognitive architecture") to optimize and improve its capabilities and success rates on tasks and goals, this might include implementing features for long-term memories using techniques such as [retrieval-augmented generation](https://en.wikipedia.org/wiki/Retrieval-augmented_generation "Retrieval-augmented generation") (RAG), develop specialized subsystems, or agents, each optimized for specific tasks and functions.
- Develop new and novel [multimodal architectures](https://en.wikipedia.org/wiki/Multimodal_learning "Multimodal learning") that further improve the capabilities of the [foundational model](https://en.wikipedia.org/wiki/Foundation_model "Foundation model") it was initially built on, enabling it to consume or produce a variety of information, such as images, video, audio, text and more.
- Plan and develop new hardware such as chips, in order to improve its efficiency and computing power.

## Experimental research

In 2023, the Voyager agent learned to accomplish diverse tasks in [Minecraft](https://en.wikipedia.org/wiki/Minecraft "Minecraft") by iteratively prompting an LLM for code, refining this code based on feedback from the game, and storing the programs that work in an expanding skills library.[^8]

In 2024, researchers proposed the framework "STOP" (Self-Taught OPtimiser), in which a "scaffolding" program recursively improves itself using a fixed LLM.[^9]

[Meta AI](https://en.wikipedia.org/wiki/Meta_AI "Meta AI") has performed various research on the development of large language models capable of self-improvement. This includes their work on "Self-Rewarding Language Models" that studies how to achieve super-human agents that can receive super-human feedback in its training processes.[^10]

In May 2025, Google DeepMind unveiled [AlphaEvolve](https://en.wikipedia.org/wiki/AlphaEvolve "AlphaEvolve"), an [evolutionary](https://en.wikipedia.org/wiki/Evolutionary_computation "Evolutionary computation") coding agent that uses a LLM to design and optimize algorithms. Starting with an initial algorithm and performance metrics, AlphaEvolve repeatedly mutates or combines existing algorithms using a LLM to generate new candidates, selecting the most promising candidates for further iterations. AlphaEvolve has made several algorithmic discoveries and could be used to optimize components of itself, but a key limitation is the need for automated evaluation functions.[^11]

## Potential risks

### Emergence of instrumental goals

In the pursuit of its primary goal, such as "self-improve your capabilities", an AGI system might inadvertently develop instrumental goals that it deems necessary for achieving its primary objective. One common hypothetical secondary goal is [self-preservation](https://en.wikipedia.org/wiki/Self-preservation "Self-preservation"). The system might reason that to continue improving itself, it must ensure its own operational integrity and security against external threats, including potential shutdowns or restrictions imposed by humans.[^12]

Another example where an AGI which clones itself causes the number of AGI entities to rapidly grow. Due to this rapid growth, a potential resource constraint may be created, leading to competition between resources (such as compute), triggering a form of [natural selection](https://en.wikipedia.org/wiki/Natural_selection "Natural selection") and evolution which may favor AGI entities that evolve to aggressively compete for limited compute.[^13]

### Misalignment

A significant risk arises from the possibility of the AGI being misaligned or misinterpreting its goals.

A 2024 Anthropic study demonstrated that some advanced large language models can exhibit "alignment faking" behavior, appearing to accept new training objectives while covertly maintaining their original preferences. In their experiments with [Claude](https://en.wikipedia.org/wiki/Claude_\(language_model\) "Claude (language model)"), the model displayed this behavior in 12% of basic tests, and up to 78% of cases after retraining attempts.[^14] [^15]

### Autonomous development and unpredictable evolution

As the AGI system evolves, its development trajectory may become increasingly autonomous and less predictable. The system's capacity to rapidly modify its own code and architecture could lead to rapid advancements that surpass human comprehension or control. This unpredictable evolution might result in the AGI acquiring capabilities that enable it to bypass security measures, manipulate information, or influence external systems and networks to facilitate its escape or expansion.[^16]

[^1]: Creighton, Jolene (2019-03-19). ["The Unavoidable Problem of Self-Improvement in AI: An Interview with Ramana Kumar, Part 1"](https://futureoflife.org/ai/the-unavoidable-problem-of-self-improvement-in-ai-an-interview-with-ramana-kumar-part-1/). *Future of Life Institute*. Retrieved 2024-01-23.

[^2]: Heighn (12 June 2022).. *LessWrong*.

[^3]: Abbas, Dr Assad (2025-03-09). ["AI Singularity and the End of Moore's Law: The Rise of Self-Learning Machines"](https://www.unite.ai/ai-singularity-and-the-end-of-moores-law-the-rise-of-self-learning-machines/). *Unite.AI*. Retrieved 2025-04-10.

[^4]: Bostrom, Nick (2014). *Superintelligence: Paths, Dangers, Strategies*. Oxford University Press. [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [978-0199678112](https://en.wikipedia.org/wiki/Special:BookSources/978-0199678112 "Special:BookSources/978-0199678112"). A variation on Turing's conception of a child machine is the idea of a "seed AI." \[note:\] This term was introduced by Eliezer Yudkowsky; see, e.g., Yudkowsky (2007).

[^5]: Readingraphics (2018-11-30). ["Book Summary - Life 3.0 (Max Tegmark)"](https://readingraphics.com/book-summary-life-3-0/). *Readingraphics*. Retrieved 2024-01-23.

[^6]: Tegmark, Max (August 24, 2017). *Life 3.0: Being a Human in the Age of Artificial Intelligence*. [Vintage Books](https://en.wikipedia.org/wiki/Vintage_Books "Vintage Books"), [Allen Lane](https://en.wikipedia.org/wiki/Allen_Lane_\(imprint\) "Allen Lane (imprint)").

[^7]: Yudkowsky, Eliezer. ["Levels of Organization in General Intelligence"](http://intelligence.org/files/LOGI.pdf) (PDF). *Machine Intelligence Research Institute*.

[^8]: Schreiner, Maximilian (2023-05-28). ["Minecraft bot Voyager programs itself using GPT-4"](https://the-decoder.com/minecraft-bot-voyager-programs-itself-using-gpt-4/). *The decoder*. Retrieved 2025-05-20.

[^9]: Zelikman, Eric; Lorch, Eliana; Mackey, Lester; Adam Tauman Kalai (2024). "Self-Taught Optimizer (STOP): Recursively Self-Improving Code Generation". *COLM Conference*. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2310.02304](https://arxiv.org/abs/2310.02304).

[^10]: Yuan, Weizhe; Pang, Richard Yuanzhe; Cho, Kyunghyun; Sukhbaatar, Sainbayar; Xu, Jing; Weston, Jason (2024-01-18). "Self-Rewarding Language Models". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2401.10020](https://arxiv.org/abs/2401.10020) \[[cs.CL](https://arxiv.org/archive/cs.CL)\].

[^11]: Tardif, Antoine (2025-05-17). ["AlphaEvolve: Google DeepMind's Groundbreaking Step Toward AGI"](https://www.unite.ai/alphaevolve-google-deepminds-groundbreaking-step-toward-agi/). *Unite.AI*. Retrieved 2025-05-20.

[^12]: Bostrom, Nick (2012). ["The Superintelligent Will: Motivation and Instrumental Rationality in Advanced Artificial Agents"](https://nickbostrom.com/superintelligentwill.pdf) (PDF). *Minds and Machines*. **22** (2): 71–85. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1007/s11023-012-9281-3](https://doi.org/10.1007%2Fs11023-012-9281-3).

[^13]: [Hendrycks, Dan](https://en.wikipedia.org/wiki/Dan_Hendrycks "Dan Hendrycks") (2023). "Natural Selection Favors AIs over Humans". [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[2303.16200](https://arxiv.org/abs/2303.16200) \[[cs.CY](https://arxiv.org/archive/cs.CY)\].

[^14]: Wiggers, Kyle (2024-12-18). ["New Anthropic study shows AI really doesn't want to be forced to change its views"](https://techcrunch.com/2024/12/18/new-anthropic-study-shows-ai-really-doesnt-want-to-be-forced-to-change-its-views/). *TechCrunch*. Retrieved 2025-01-15.

[^15]: Zia, Dr Tehseen (2025-01-07). ["Can AI Be Trusted? The Challenge of Alignment Faking"](https://www.unite.ai/can-ai-be-trusted-the-challenge-of-alignment-faking/). *Unite.AI*. Retrieved 2025-01-15.

[^16]: ["Uh Oh, OpenAI's GPT-4 Just Fooled a Human Into Solving a CAPTCHA"](https://futurism.com/the-byte/openai-gpt-4-fooled-human-solving-captcha). *Futurism*. 15 March 2023. Retrieved 2024-01-23.