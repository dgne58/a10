---
title: "Transformers · Hugging Face"
source: "https://huggingface.co/docs/transformers/en/quantization/overview"
author:
published:
created: 2026-04-13
description: "We’re on a journey to advance and democratize artificial intelligence through open source and open science."
tags:
  - "clippings"
---
Join the Hugging Face community

and get access to the augmented documentation experience

to get started

## Overview

Quantization lowers the memory requirements of loading and using a model by storing the weights in a lower precision while trying to preserve as much accuracy as possible. Weights are typically stored in full-precision (fp32) floating point representations, but half-precision (fp16 or bf16) are increasingly popular data types given the large size of models today. Some quantization methods can reduce the precision even further to integer representations, like int8 or int4.

Transformers supports many quantization methods, each with their pros and cons, so you can pick the best one for your specific use case. Some methods require calibration for greater accuracy and extreme compression (1-2 bits), while other methods work out of the box with on-the-fly quantization.

Use the Space below to help you pick a quantization method depending on your hardware and number of bits to quantize to.

| Quantization Method | On the fly quantization | CPU | CUDA GPU | ROCm GPU | Metal (Apple Silicon) | Intel GPU | Torch compile() | Bits | PEFT Fine Tuning | Serializable with 🤗Transformers | 🤗Transformers Support | Link to library |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [AQLM](https://huggingface.co/docs/transformers/en/quantization/aqlm) | 🔴 | 🟢 | 🟢 | 🔴 | 🔴 | 🟢 | 🟢 | 1/2 | 🟢 | 🟢 | 🟢 | [https://github.com/Vahe1994/AQLM](https://github.com/Vahe1994/AQLM) |
| [AutoRound](https://huggingface.co/docs/transformers/en/quantization/auto_round) | 🔴 | 🟢 | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 2/3/4/8 | 🔴 | 🟢 | 🟢 | [https://github.com/intel/auto-round](https://github.com/intel/auto-round) |
| [AWQ](https://huggingface.co/docs/transformers/en/quantization/awq) | 🔴 | 🟢 | 🟢 | 🟢 | 🔴 | 🟢 | ? | 4 | 🟢 | 🟢 | 🟢 | [https://github.com/casper-hansen/AutoAWQ](https://github.com/casper-hansen/AutoAWQ) |
| [bitsandbytes](https://huggingface.co/docs/transformers/en/quantization/bitsandbytes) | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 | 🟢 | 🟢 | 4/8 | 🟢 | 🟢 | 🟢 | [https://github.com/bitsandbytes-foundation/bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes) |
| [compressed-tensors](https://huggingface.co/docs/transformers/en/quantization/compressed_tensors) | 🔴 | 🟢 | 🟢 | 🟢 | 🔴 | 🔴 | 🔴 | 1/8 | 🟢 | 🟢 | 🟢 | [https://github.com/neuralmagic/compressed-tensors](https://github.com/neuralmagic/compressed-tensors) |
| [EETQ](https://huggingface.co/docs/transformers/en/quantization/eetq) | 🟢 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | ? | 8 | 🟢 | 🟢 | 🟢 | [https://github.com/NetEase-FuXi/EETQ](https://github.com/NetEase-FuXi/EETQ) |
| [Four Over Six](https://huggingface.co/docs/transformers/en/quantization/fouroversix) | 🟢 | 🟢 | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 4 | 🔴 | 🟢 | 🟢 | [https://github.com/mit-han-lab/fouroversix](https://github.com/mit-han-lab/fouroversix) |
| [FP-Quant](https://huggingface.co/docs/transformers/en/quantization/fp_quant) | 🟢 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 4 | 🔴 | 🟢 | 🟢 | [https://github.com/IST-DASLab/FP-Quant](https://github.com/IST-DASLab/FP-Quant) |
| [GGUF / GGML (llama.cpp)](https://huggingface.co/docs/transformers/en/gguf) | 🟢 | 🟢 | 🟢 | 🔴 | 🟢 | 🟢 | 🔴 | 1/8 | 🔴 | [See Notes](https://huggingface.co/docs/transformers/en/gguf) | [See Notes](https://huggingface.co/docs/transformers/en/gguf) | [https://github.com/ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp) |
| [GPT-QModel](https://huggingface.co/docs/transformers/en/quantization/gptq) | 🔴 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🔴 | 2/3/4/8 | 🟢 | 🟢 | 🟢 | [https://github.com/ModelCloud/GPTQModel](https://github.com/ModelCloud/GPTQModel) |
| [HIGGS](https://huggingface.co/docs/transformers/en/quantization/higgs) | 🟢 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 2/4 | 🔴 | 🟢 | 🟢 | [https://github.com/HanGuo97/flute](https://github.com/HanGuo97/flute) |
| [HQQ](https://huggingface.co/docs/transformers/en/quantization/hqq) | 🟢 | 🟢 | 🟢 | 🔴 | 🔴 | 🟢 | 🟢 | 1/8 | 🟢 | 🔴 | 🟢 | [https://github.com/mobiusml/hqq/](https://github.com/mobiusml/hqq/) |
| [Metal](https://huggingface.co/docs/transformers/en/quantization/metal) | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 2/4/8 | 🔴 | 🟢 | 🟢 | [Hub Kernels](https://huggingface.co/kernels-community/mlx-quantization-metal-kernels) |
| [optimum-quanto](https://huggingface.co/docs/transformers/en/quantization/quanto) | 🟢 | 🟢 | 🟢 | 🔴 | 🟢 | 🟢 | 🟢 | 2/4/8 | 🔴 | 🔴 | 🟢 | [https://github.com/huggingface/optimum-quanto](https://github.com/huggingface/optimum-quanto) |
| [SINQ](https://huggingface.co/docs/transformers/en/quantization/sinq) | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 | 🟡 | 🟡 | 2/3/4/6/8 | 🔴 | 🟢 | 🟢 | [https://github.com/huawei-csl/SINQ](https://github.com/huawei-csl/SINQ) |
| [FBGEMM\_FP8](https://huggingface.co/docs/transformers/en/quantization/fbgemm_fp8) | 🟢 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 8 | 🔴 | 🟢 | 🟢 | [https://github.com/pytorch/FBGEMM](https://github.com/pytorch/FBGEMM) |
| [torchao](https://huggingface.co/docs/transformers/en/quantization/torchao) | 🟢 | 🟢 | 🟢 | 🔴 | 🟡 | 🟢 |  | 4/8 |  | 🟢🔴 | 🟢 | [https://github.com/pytorch/ao](https://github.com/pytorch/ao) |
| [VPTQ](https://huggingface.co/docs/transformers/en/quantization/vptq) | 🔴 | 🔴 | 🟢 | 🟡 | 🔴 | 🔴 | 🟢 | 1/8 | 🔴 | 🟢 | 🟢 | [https://github.com/microsoft/VPTQ](https://github.com/microsoft/VPTQ) |
| [FINEGRAINED\_FP8](https://huggingface.co/docs/transformers/en/quantization/finegrained_fp8) | 🟢 | 🔴 | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 8 | 🔴 | 🟢 | 🟢 | Built-in |
| [SpQR](https://huggingface.co/docs/transformers/en/quantization/spqr) | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 3 | 🔴 | 🟢 | 🟢 | [https://github.com/Vahe1994/SpQR/](https://github.com/Vahe1994/SpQR/) |
| [Quark](https://huggingface.co/docs/transformers/en/quantization/quark) | 🔴 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | ? | 2/4/6/8/9/16 | 🔴 | 🔴 | 🟢 | [https://quark.docs.amd.com/latest/](https://quark.docs.amd.com/latest/) |

## Resources

If you are new to quantization, we recommend checking out these beginner-friendly quantization courses in collaboration with DeepLearning.AI.

## User-Friendly Quantization Tools

If you are looking for a user-friendly quantization experience, you can use the following community spaces and notebooks:

- [Bitsandbytes Space](https://huggingface.co/spaces/bnb-community/bnb-my-repo)
- [GGUF Space](https://huggingface.co/spaces/ggml-org/gguf-my-repo)
- [MLX Space](https://huggingface.co/spaces/mlx-community/mlx-my-repo)
- [AutoQuant Notebook](https://colab.research.google.com/drive/1b6nqC7UZVt8bx4MksX7s656GXPM-eWw4?usp=sharing#scrollTo=ZC9Nsr9u5WhN)
[Update on GitHub](https://github.com/huggingface/transformers/blob/main/docs/source/en/quantization/overview.md)

Transformers · Hugging Face

[←Model training anatomy](https://huggingface.co/docs/transformers/en/model_memory_anatomy) [Selecting a quantization method→](https://huggingface.co/docs/transformers/en/quantization/selecting)