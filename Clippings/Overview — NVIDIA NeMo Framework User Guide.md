---
title: "Overview — NVIDIA NeMo Framework User Guide"
source: "https://docs.nvidia.com/nemo-framework/user-guide/latest/overview.html"
author:
published:
created: 2026-04-13
description:
tags:
  - "clippings"
---
## Overview

NVIDIA NeMo Framework is a scalable and cloud-native generative AI framework built for researchers and developers working on Large Language Models, Multimodal, and [Speech AI](https://docs.nvidia.com/nemo-framework/user-guide/latest/speech_ai/index.html) (e.g. [Automatic Speech Recognition](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/asr/intro.html) and [Text-to-Speech](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/tts/intro.html)). It enables users to efficiently create, customize, and deploy new generative AI models by leveraging existing code and pre-trained model checkpoints.

Important

This page is focused on Speech AI, for LLM/VLM/Diffusion models support, please refer to the [NeMo Framework](https://docs.nvidia.com/nemo/#framework) documentation. For the NeMo Framework container, starting with 26.02, refer to Megatron-Bridge’s [documentation](https://docs.nvidia.com/nemo/megatron-bridge/latest/index.html) and [release notes](https://github.com/NVIDIA-NeMo/Megatron-Bridge/releases).

## Speech AI

Developing conversational AI models is a complex process that involves defining, constructing, and training models within particular domains. This process typically requires several iterations to reach a high level of accuracy. It often involves multiple iterations to achieve high accuracy, fine-tuning on various tasks and domain-specific data, ensuring training performance, and preparing models for inference deployment.

![_images/nemo-speech-ai.png](https://docs.nvidia.com/nemo-framework/user-guide/latest/_images/nemo-speech-ai.png)

NeMo Framework provides support for the training and customization of Speech AI models. This includes tasks like Automatic Speech Recognition (ASR) and Text-To-Speech (TTS) synthesis. It offers a smooth transition to enterprise-level production deployment with [NVIDIA Riva](https://developer.nvidia.com/riva). To assist developers and researchers, NeMo Framework includes state-of-the-art pre-trained checkpoints, tools for reproducible speech data processing, and features for interactive exploration and analysis of speech datasets. The components of the NeMo Framework for Speech AI are as follows:

Training and Customization

NeMo Framework contains everything needed to train and customize speech models ([ASR](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/asr/intro.html), [Speech Classification](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/asr/speech_classification/intro.html), [Speaker Recognition](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/asr/speaker_recognition/intro.html), [Speaker Diarization](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/asr/speaker_diarization/intro.html), and [TTS](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/tts/intro.html)) in a reproducible manner.

SOTA Pre-trained Models

NeMo Framework provides state-of-the-art recipes and pre-trained checkpoints of several [ASR](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/asr/results.html) and [TTS](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/tts/checkpoints.html) models, as well as instructions on how to load them.

[Speech Tools](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/tools/intro.html)

NeMo Framework provides a set of tools useful for developing ASR and TTS models, including:

- [NeMo Forced Aligner (NFA)](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/tools/nemo_forced_aligner.html) for generating token-, word- and segment-level timestamps of speech in audio using NeMo’s CTC-based Automatic Speech Recognition models.
- [Speech Data Processor (SDP)](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/tools/speech_data_processor.html), a toolkit for simplifying speech data processing. It allows you to represent data processing operations in a config file, minimizing boilerplate code, and allowing reproducibility and shareability.
- [Speech Data Explorer (SDE)](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/tools/speech_data_explorer.html), a Dash-based web application for interactive exploration and analysis of speech datasets.
- [Dataset creation tool](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/tools/ctc_segmentation.html) which provides functionality to align long audio files with the corresponding transcripts and split them into shorter fragments that are suitable for Automatic Speech Recognition (ASR) model training.
- [Comparison Tool](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/tools/intro.html) for ASR Models to compare predictions of different ASR models at word accuracy and utterance level.
- [ASR Evaluator](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/tools/asr_evaluator.html) for evaluating the performance of ASR models and other features such as Voice Activity Detection.
- Text Normalization Tool for converting text from the written form to the spoken form and vice versa (e.g. “31st” vs “thirty first”).

Path to Deployment

NeMo models that have been trained or customized using the NeMo Framework can be optimized and deployed with [NVIDIA Riva](https://developer.nvidia.com/riva). Riva provides containers and Helm charts specifically designed to automate the steps for push-button deployment.

Getting Started with Speech AI

- [Quickstart Guide](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/starthere/intro.html)
- [Tutorial Notebooks](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/starthere/tutorials.html)

## Other Resources

### GitHub Repos

- [NVIDIA-NeMo](https://github.com/NVIDIA-NeMo): The main repository for the NeMo Framework

### Getting Help

Engage with the NeMo community, ask questions, get support, or report bugs.

- [NeMo Discussions](https://github.com/NVIDIA-NeMo/NeMo/discussions)
- [NeMo Issues](https://github.com/NVIDIA-NeMo/NeMo/issues)

## Programming Languages and Frameworks

- Python: The main interface to use NeMo Framework
- Pytorch: NeMo Framework is built on top of PyTorch

## Licenses

- NeMo Github repo is licensed under the [Apache 2.0 license](https://github.com/NVIDIA-NeMo/NeMo?tab=Apache-2.0-1-ov-file#readme)
- NeMo Framework is licensed under the [NVIDIA AI PRODUCT AGREEMENT](https://www.nvidia.com/en-us/data-center/products/nvidia-ai-enterprise/eula/). By pulling and using the container, you accept the terms and conditions of this license.
- The NeMo Framework container contains Llama materials governed by the [Meta Llama3 Community License Agreement](https://huggingface.co/meta-llama/Meta-Llama-3-8B/tree/main).