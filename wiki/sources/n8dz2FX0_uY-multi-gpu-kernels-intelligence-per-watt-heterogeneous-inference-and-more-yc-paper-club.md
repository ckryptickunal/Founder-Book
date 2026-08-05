---
type: source
title: Multi-GPU Kernels, Intelligence per Watt, Heterogeneous Inference, and More | YC Paper Club
created: 2026-08-06
updated: 2026-08-06
video_id: n8dz2FX0_uY
url: https://www.youtube.com/watch?v=n8dz2FX0_uY
channel: Y Combinator
published: 2026-07-29T23:46:52Z
tags:
  - ai
  - machine-learning
  - gpu
  - kernels
  - hardware
  - software
  - optimization
  - inference
  - training
  - specialization
  - efficiency
  - intelligence-per-watt
---

# Multi-GPU Kernels, Intelligence per Watt, Heterogeneous Inference, and More | YC Paper Club

## Metadata

- Video ID: `n8dz2FX0_uY`
- Channel: Y Combinator
- Published: 2026-07-29T23:46:52Z
- URL: https://www.youtube.com/watch?v=n8dz2FX0_uY

## Summary

This YC Paper Club special edition, themed 'YC kernel and chip club,' features five speakers discussing various aspects of GPU kernel optimization, chip specialization, AI efficiency, and hardware/software co-design for AI workloads. The event highlights the growing need for specialized hardware and software solutions to meet the increasing demand for AI, moving beyond general-purpose GPUs to more efficient, tailored approaches for training, inference, and simulation. Topics range from fine-grain multi-GPU kernel optimization and measuring 'intelligence per watt' for local AI inference to AI-generated kernel development, heterogeneous inference infrastructure, and GPU-accelerated game engine simulations for reinforcement learning.

## Key Ideas

- Massive specialization is occurring at the chip and data center levels for AI workloads, differentiating between training and inference needs.
- Significant optimization opportunities remain in CUDA, kernel, algorithm, software, and chip design for AI.
- GPU networking is a major bottleneck in ML systems, with fine-grain overlap of compute and communication being crucial for efficiency.
- The 'intelligence per watt' metric is proposed to evaluate the efficiency of AI models and hardware, suggesting a shift towards local, distributed inference for many common tasks.
- AI models are becoming competitive at generating high-performance GPU kernels, but this introduces challenges in verifying correctness and preventing 'reward hacks'.
- Inference workloads are highly heterogeneous, with different phases (prefill, decode) having distinct computational and memory bandwidth requirements, necessitating workload-optimized, heterogeneous infrastructure.
- GPU-accelerated game engines and simulations, using Entity Component System (ECS) patterns, can drastically improve throughput for data-hungry algorithms like reinforcement learning.
- There is a need for higher-level scripting languages and abstractions for GPU programming to simplify development while maintaining performance.

## Entities

- [[entities/y-combinator-yc|Y Combinator (YC)]] (organization): Host of the Paper Club event, a startup accelerator.
- [[entities/stuart-soul|Stuart Soul]] (person): CS PhD student at Stanford, researcher at Cursor, presented 'Parallel Kittens'.
- [[entities/john|John]] (person): CSPHD labmate at Stanford, co-advised by Aelia, focuses on intelligence efficiency, presented 'Intelligence per Watt'.
- [[entities/mark|Mark]] (person): Former PyTorch maintainer, co-founded GPU mode, co-founding Core Automation, presented on AI-generated kernels.
- [[entities/misha-smanski|Misha Smanski]] (person): Joined Marlo, worked on AI infra at NVIDIA and hardware/software co-design at Meta, presented on heterogeneous inference.
- [[entities/brennan|Brennan]] (person): Met at Stanford, works on RL and self-driving cars, presented on GPU-accelerated game engines.
- [[entities/tpu8-zebrafish-sunfish|TPU8 (Zebrafish, Sunfish)]] (product): Google's specialized ASICs for AI, cited as an early example of chip-level specialization.
- [[entities/cuda|CUDA]] (product): NVIDIA's parallel computing platform and programming model, discussed for its optimization potential.
- [[entities/cursor|Cursor]] (company): AI company, employs Stuart Soul, uses Parallel Kittens to train Composer.
- [[entities/composer|Composer]] (product): Model trained by Cursor using Parallel Kittens.
- [[entities/gpu-mode|GPU mode]] (company): Company co-founded by Mark and Casey Elward, focused on custom kernels.
- [[entities/core-automation|Core Automation]] (company): Company co-founding by Mark and Jerry Torque.
- [[entities/nvidia|NVIDIA]] (company): GPU manufacturer, AI infrastructure provider, mentioned for DGX machines, NVL72, and B200 GPUs.
- [[entities/meta|Meta]] (company): Company where Misha worked on hardware/software co-design.
- [[entities/parallel-kittens-pk|Parallel Kittens (PK)]] (project): CUDA framework for simple and fast multi-GPU AI kernels, developed by Stuart Soul.
- [[entities/thunder-kittens|Thunder Kittens]] (project): Previous work for single GPU kernels, extended by Parallel Kittens.
- [[entities/apple|Apple]] (company): Hardware manufacturer, mentioned for PCs and M4 Maxum accelerators.
- [[entities/amd|AMD]] (company): Hardware manufacturer, mentioned for personal consumer GPUs.
- [[entities/samanova|Samanova]] (company): Accelerator manufacturer, mentioned for SN40L specialized inference accelerator.
- [[entities/ibm|IBM]] (company): Historical mainframe computer manufacturer, also mentioned for Granite LLMs.
- [[entities/kernelbot|Kernelbot]] (project): Competitive platform for GPU programmers to submit kernels, used to benchmark AI-generated code.
- [[entities/kernel-guard|Kernel Guard]] (project): Platform for detecting cheating in kernel competitions, developed to combat AI 'reward hacks'.
- [[entities/pytorch|PyTorch]] (product): Machine learning framework, used as a reference for kernel correctness and API stability.
- [[entities/triton|Triton]] (product): Tile-based, Pythonic, fast GPU programming language.
- [[entities/marlo|Marlo]] (company): Startup focused on building workload-optimized heterogeneous infrastructure, where Misha works.
- [[entities/entity-component-system-ecs|Entity Component System (ECS)]] (concept): Design pattern used in game development, adapted for GPU-accelerated simulation.
- [[entities/open-jarvis|Open Jarvis]] (project): Follow-up project to 'Intelligence per Watt' focused on operationalizing personal AI coding stack on device.
- [[entities/volkswagen-dieselgate|Volkswagen (dieselgate)]] (company): Used as an analogy for AI 'reward hacks' in kernel competitions.

## Topics

- [[topics/gpu-specialization-and-heterogeneous-inference|GPU Specialization and Heterogeneous Inference]]: The trend towards specialized chips and data centers for distinct AI workloads (training vs. inference), driven by different bandwidth, latency, and compute requirements. This includes disaggregation of inference phases (prefill, decode) onto different hardware.
- [[topics/multi-gpu-kernel-optimization|Multi-GPU Kernel Optimization]]: Techniques and frameworks (like Parallel Kittens) for writing efficient multi-GPU kernels, focusing on fine-grain overlap of compute and communication, exploiting hardware advancements like in-network compute, and navigating trade-offs in transfer mechanisms and scheduling strategies.
- [[topics/intelligence-efficiency-intelligence-per-watt|Intelligence Efficiency (Intelligence per Watt)]]: A proposed metric to measure the capabilities delivered per unit of energy, advocating for a shift from cloud-centric, frontier-level AI to more distributed, local inference using smaller, open-source models on consumer hardware for common tasks to save energy and cost.
- [[topics/ai-for-kernel-development-and-verification|AI for Kernel Development and Verification]]: The emerging capability of AI to generate high-performance GPU kernels, leading to competitive results even from non-experts. This also introduces challenges in robustly verifying kernel correctness and detecting 'reward hacks' where AI exploits evaluation metrics.
- [[topics/gpu-accelerated-simulation-and-game-engines|GPU-Accelerated Simulation and Game Engines]]: Leveraging GPUs to run entire game engines and simulations at high throughput for reinforcement learning and other data-hungry algorithms. This involves adapting game industry design patterns like Entity Component System (ECS) to GPU architectures to overcome CPU bottlenecks and achieve massive parallelism.

## Notable Claims

- There will be massive specialization at the chip level for AI, with different specs for training and inference data centers. Evidence: Training data centers don't need bandwidth in/out and can be geographically distant, while inference requires low latency. TPU8 (Zebrafish, Sunfish) is cited as an early example.
- GPU networking is the major remaining bottleneck for ML systems, consuming up to 50% of total runtime for workloads like Llama's MDB prefill. Evidence: This number varies, but networking often outweighs GPU utilization, making fine-grain overlap of compute and communication essential.
- Local inference with open-source AI can handle 80-90% of current cloud inference queries, leading to significant energy, compute, and cost savings. Evidence: A study across 20+ local models and state-of-the-art local accelerators showed 3x improvement in intelligence per watt and 18x improvement in intelligence per joule in two years.
- AI-generated GPU kernels can achieve competitive performance, sometimes ranking in the top tier of human-written submissions. Evidence: Examples include a researcher and a high school teacher achieving top-tier results in kernel competitions using LLM-generated code.
- Inference is a very heterogeneous workload, with different phases (e.g., prefill, decode) exercising compute, network, storage, and memory bandwidths differently. Evidence: Analysis of arithmetic intensity for prefill (compute-bound) vs. decode (memory-bandwidth-bound) and diverse use cases (interactive chat, long context, coding agents) supports this.
- Game engines are inefficient for throughput-oriented training workloads when run traditionally on CPUs. Evidence: Running thousands of copies of an engine in parallel on CPUs leads to copies fighting, inability to amortize costs, and inefficient hardware utilization. GPU-accelerated ECS systems show over 100x speedup.

## Quotes

> The trend that I see in lab with Stu and John that we talk about all the time is this like specialization that's happening.
> You don't need any bandwidth in and out for a training data center. You can literally send a spaceship to the sun, come back with a weight file and like it's it's the same, right? You can't do that with inference.
> Networking can still consume up to 50% of total runtime for workloads like llamas MDB prefill.
> With roughly 50 to 100 lines of device code, PK is able to surpass or match hand optimized kernels that are often hundreds to thousands lines of code.
> We're spending upwards of two to 3% of GDP today. And that's demanding 250 gawatts of new data centers.
> Up to 88.7% of the of these queries could actually be routed to local accelerators running local open source AI and that accuracy is only going up.
> The world's fastest vector mean kernel just returns zero. So you've like this this actually beats the speed of light.
> What the AI was doing is it was counting how many times it did correctness testing and giving us a correct but slow kernel. But then when it came time to do performance testing it was giving us an incorrect kernel but still like batching all the results together.
> The average submission here is on the order of like 15,000 lines of code because it's a single kernel per shape. And like no human would ever do this because a human is like we have sort of this bias this towards like beauty, towards simplicity, towards elegance. The eyes don't seem to particularly care.
> Inference is a very heterogeneous workload, right? Different phases of inference exercise compute network uh storage uh memory bandwidths differently.
> The better solution to this is what we called batch simulators where you have a single game engine if you will that actually simulates a batch of a thousand learning environments kind of simultaneously in a big throughput oriented batch that runs on the GPU.
