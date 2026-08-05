---
type: source
title: World Models, JEPA And The Path To Sample-Efficient RL
created: 2026-08-06
updated: 2026-08-06
video_id: qz4GQ0zUFRw
url: https://www.youtube.com/watch?v=qz4GQ0zUFRw
channel: Y Combinator
published: 2026-07-17T14:00:25Z
tags:
  - ai
  - reinforcement-learning
  - world-models
  - sample-efficiency
  - agi
  - robotics
  - self-driving-cars
  - deep-learning
  - diffusion-models
  - jepa
  - model-predictive-control
  - alphago
---

# World Models, JEPA And The Path To Sample-Efficient RL

## Metadata

- Video ID: `qz4GQ0zUFRw`
- Channel: Y Combinator
- Published: 2026-07-17T14:00:25Z
- URL: https://www.youtube.com/watch?v=qz4GQ0zUFRw

## Summary

This discussion explores sample efficiency as a major open problem in AI and positions 'world models' as the most promising path to Artificial General Intelligence (AGI). It contrasts human learning, which is highly sample-efficient, with current AI models that require vast amounts of data. The conversation delves into the mathematical and intuitive understanding of world models, from perfect deterministic models (like Newtonian physics for space travel) to complex, stochastic, non-differentiable environments encountered in games (Chess, Go), self-driving cars, and robotics. The speakers highlight the limitations of model-free reinforcement learning and AlphaGo's approach for real-world applications due to large action spaces and real-time constraints. They then introduce modern world modeling techniques, such as the Dreamer series and the use of video diffusion models for generating synthetic data, and the Joint Embedding Predictive Architecture (JEPA) for efficient latent space prediction. The discussion concludes by outlining remaining open problems, including the limitations of physics-informed neural networks, challenges in test-time adaptation, the need for real-time performance, and the importance of rich sensory feedback, while also considering the 'squint test' for AGI and the role of sleep in human learning.

## Key Ideas

- Sample efficiency is a critical challenge in AI, where models struggle to learn from small datasets compared to humans.
- World models are considered the most promising approach to achieve sample efficiency and potentially AGI.
- Humans possess implicit world models, enabling intuitive understanding and mental simulation (e.g., Newton's laws, basketball layups visualization).
- Model Predictive Control (MPC) leverages perfect world models for precise, sample-efficient actions (e.g., NASA asteroid interception, SpaceX landings).
- Reinforcement Learning (RL) faces significant challenges in stochastic, non-differentiable environments with large state and action spaces.
- Model-free RL directly learns policies without an explicit environment model, while model-based RL incorporates a world model to predict future states.
- AlphaGo's success relies on small, deterministic action spaces and extensive test-time planning (MCTS), which does not scale to real-world problems like self-driving or robotics.
- Self-driving cars and robotics present 'effectively infinite' state spaces and 'insanely large' action spaces, making traditional RL and AlphaGo-like approaches intractable.
- Modern world models, exemplified by the Dreamer series, leverage pre-trained video generation models (like diffusion models) to create synthetic 'imaginated rollouts' for policy training, significantly reducing the need for real-world action data.
- Joint Embedding Predictive Architecture (JEPA) improves sample efficiency by performing world modeling and optimization in a compressed latent space rather than pixel space.
- Key open problems in world modeling include improving fidelity (Physics-Informed Neural Networks limitations), achieving rapid test-time adaptation, ensuring real-time performance, integrating heterogeneous models, and incorporating rich sensory feedback (e.g., tactile information).
- The 'squint test' suggests that world models align more closely with human intelligence than autoregressive LLMs, with neuroscience supporting the brain's role in world modeling.
- Sleep is hypothesized to be crucial for the human brain's 'optimizer' function, consolidating experiences and refining world models, a mechanism currently missing in AI architectures.

## Entities

- [[entities/francois|Francois]] (person): One of the speakers, discussing AI concepts.
- [[entities/ankit|Ankit]] (person): Hypothetical adversary in a drone control example.
- [[entities/bill-gates|Bill Gates]] (person): Cited as having extensive 'world modeling experience' in entrepreneurship.
- [[entities/steve-jobs|Steve Jobs]] (person): Cited as having extensive 'world modeling experience' in entrepreneurship.
- [[entities/jensen-huang|Jensen (Huang)]] (person): Cited as having extensive 'world modeling experience' in entrepreneurship.
- [[entities/richardson|Richardson]] (person): Conducted the 1967 COGSAI study on mental practice and skill improvement.
- [[entities/shaw-duckman|Shaw Duckman]] (person): Neuroscientist at Stanford, views the neocortex's expansion as primarily for world modeling.
- [[entities/jurgen-smid-humor|Jurgen Smid Humor]] (person): Author of the 'World Models' paper, an early work on training policies on synthetic data.
- [[entities/danar-hafner|Danar Hafner]] (person): Lead researcher behind the Dreamer series of papers on world models.
- [[entities/andrew-wong|Andrew Wong]] (person): Professor at Stanford, taught CS 229.
- [[entities/sam-altman|Sam Altman]] (person): Cited for his belief that a new architecture will outperform the Transformer.
- [[entities/lane-macintosh|Lane Macintosh]] (person): Runs Tesla FSD, played hockey with one of the speakers at Stanford.
- [[entities/steph-curry|Steph Curry]] (person): Basketball player, used as an example of human world modeling precision.
- [[entities/lebron-james|LeBron James]] (person): Basketball player, used as an example of human world modeling precision.
- [[entities/nasa|NASA]] (organization): Uses perfect world models (Newtonian physics) for space mission planning.
- [[entities/spacex|SpaceX]] (company): Uses Model Predictive Control for rocket landings.
- [[entities/y-combinator|Y Combinator]] (organization): Channel hosting the video, and an accelerator supporting AI/robotics startups.
- [[entities/stanford|Stanford]] (organization): University where speakers teach/studied, and where robotics research is conducted.
- [[entities/tesla|Tesla]] (company): Develops FSD (Full Self-Driving) technology, noted for its large fleet data collection.
- [[entities/whimo|Whimo]] (company): Self-driving car company, mentioned as having working self-driving cars.
- [[entities/figure|Figure]] (company): Humanoid robotics company.
- [[entities/pi|Pi]] (company): Humanoid robotics company.
- [[entities/nvidia|Nvidia]] (company): Mentioned in the context of robotics research and world models.
- [[entities/wave|Wave]] (company): Company that developed Gaia, a self-driving car system using world models.
- [[entities/openai-gym|OpenAI Gym]] (project): Classic environment for reinforcement learning research.
- [[entities/university-of-washington|University of Washington]] (organization): Cited for a paper on cortical area estimation of latent sensory states and actions.
- [[entities/world-models-paper|World Models (paper)]] (product): A paper by Jurgen Smid Humor on training policies using synthetic data from an environment model.
- [[entities/jepa-joint-embedding-predictive-architecture|JEPA (Joint Embedding Predictive Architecture)]] (product): A self-supervised learning technique for predicting future latent states, used in world modeling.
- [[entities/alphago|AlphaGo]] (product): DeepMind's Go-playing AI, used as an example of RL success and its limitations for real-world problems.
- [[entities/dreamer-v1-v4|Dreamer (V1-V4)]] (product): A series of papers by Danar Hafner on world models that train policies on 'imaginated rollouts' in a learned environment model.
- [[entities/sora|Sora]] (product): OpenAI's text-to-video diffusion model, mentioned as a state-of-the-art video generation model.
- [[entities/gaia|Gaia]] (product): Wave's self-driving car system, which applies world model concepts.
- [[entities/gencast|Gencast]] (product): A weather planning paper applying similar world model concepts to global weather prediction.
- [[entities/le-wm-le-world-model|LE WM LE world model]] (product): A recent paper on latent world models.
- [[entities/cvxpy|CVXPY]] (product): A Python-embedded modeling language for convex optimization.
- [[entities/dqn-deep-q-learning|DQN (Deep Q-learning)]] (product): A type of reinforcement learning algorithm.
- [[entities/actor-critic|Actor Critic]] (product): A type of reinforcement learning algorithm.
- [[entities/mcts-monte-carlo-tree-search|MCTS (Monte Carlo Tree Search)]] (product): A search algorithm used in AlphaGo for test-time planning.
- [[entities/fsd-full-self-driving|FSD (Full Self-Driving)]] (product): Tesla's autonomous driving software.
- [[entities/clip|CLIP]] (product): OpenAI's model for connecting text and images, mentioned in the context of action conditioning.
- [[entities/stable-diffusion|Stable Diffusion]] (product): A popular image generation model, mentioned for its use of latent space optimization.
- [[entities/pins-physics-informed-neural-networks|Pins (Physics Informed Neural Networks)]] (product): A type of neural network that incorporates physical laws, discussed for its limitations.
- [[entities/agi-artificial-general-intelligence|AGI (Artificial General Intelligence)]] (other): The goal of creating AI with human-like cognitive abilities.
- [[entities/rl-reinforcement-learning|RL (Reinforcement Learning)]] (other): A paradigm of machine learning concerned with how intelligent agents ought to take actions in an environment to maximize the notion of cumulative reward.
- [[entities/mpc-model-predictive-control|MPC (Model Predictive Control)]] (other): An advanced method of process control that uses a dynamic model of the process.
- [[entities/sgd-stochastic-gradient-descent|SGD (Stochastic Gradient Descent)]] (other): An iterative optimization algorithm for minimizing an objective function.
- [[entities/ucb-upper-confidence-bound|UCB (Upper Confidence Bound)]] (other): A strategy used in multi-armed bandit problems and MCTS for balancing exploration and exploitation.
- [[entities/shortwave-ripple|Shortwave ripple]] (other): Neural activity in the hippocampus during sleep, hypothesized to be involved in memory consolidation and learning.
- [[entities/rosie-the-robot|Rosie the robot]] (other): A fictional humanoid robot from The Jetsons, representing the ideal of a helpful domestic robot.
- [[entities/transformer|Transformer]] (other): A neural network architecture, widely used in LLMs, discussed in the context of its limitations for compression.

## Topics

- [[topics/sample-efficiency-in-ai|Sample Efficiency in AI]]: The core problem of training AI models to learn new tasks quickly from minimal data, contrasting human vs. machine learning capabilities.
- [[topics/world-models-in-reinforcement-learning|World Models in Reinforcement Learning]]: The concept of an AI system building an internal predictive model of its environment to simulate outcomes and plan actions, seen as crucial for AGI.
- [[topics/model-predictive-control-mpc|Model Predictive Control (MPC)]]: An optimization technique that uses a dynamic model of the system to predict future behavior and determine optimal control actions, especially effective with perfect world models.
- [[topics/challenges-in-robotics-and-self-driving|Challenges in Robotics and Self-Driving]]: Discussion of the immense state and action spaces, non-differentiable dynamics, and data collection difficulties that make real-world autonomous systems particularly hard for traditional RL.
- [[topics/deep-learning-architectures-for-world-models|Deep Learning Architectures for World Models]]: Exploration of how modern deep learning techniques, including video diffusion models and Joint Embedding Predictive Architectures (JEPA), are used to build and train world models, often leveraging synthetic data.
- [[topics/human-brain-and-ai-analogy|Human Brain and AI Analogy]]: Drawing parallels between the human brain's cognitive processes (e.g., neocortical expansion, mental simulation, the role of sleep) and the design principles for advanced AI systems, particularly world models.
- [[topics/limitations-and-open-problems-in-ai|Limitations and Open Problems in AI]]: Identification of current hurdles in AI research, such as the shortcomings of Physics-Informed Neural Networks, the need for better test-time adaptation, real-time performance, and advanced sensory integration.

## Notable Claims

- One of the biggest open problems in AI right now is how to solve sample efficiency. Evidence: Current state-of-the-art AI systems often need tens of thousands of data points to learn, whereas humans learn new tasks from a handful of tries.
- World models represent the most promising path to closing the sample efficiency gap and unlocking AGI. Evidence: The entire discussion revolves around how world models enable learning from fewer samples, mental simulation, and better planning, mirroring human intelligence.
- Perfect sample efficiency would mean zero samples, achievable with a perfect world model. Evidence: Newton's second law of motion allows NASA to plan asteroid intercepts years in advance without needing to collect new samples from the environment during the mission.
- The human neocortex evolved primarily for world modeling. Evidence: Neuroscientist Shaw Duckman's view that the great cortical expansion 10 million years ago was to get better at world modeling.
- Mental practice can be nearly as effective as physical practice due to internal world models. Evidence: A 1967 COGSAI study by Richardson showed that a group imagining basketball layups improved by 23%, compared to 24% for a group physically practicing, against a control.
- AlphaGo's approach does not scale to real-world problems like self-driving or robotics. Evidence: AlphaGo requires extremely small, deterministic action spaces and extensive, slow test-time planning (MCTS), which is intractable for environments with large action spaces, stochasticity, and real-time constraints.
- Model-based RL, incorporating a world model, is required for AGI. Evidence: The evolutionary development of the human neocortex for world modeling suggests its fundamental role in intelligence, enabling simulation and better policy development.
- Physics-Informed Neural Networks (PINNs) currently 'don't really work' for out-of-distribution data. Evidence: In self-driving, if a model is trained mostly on cars driving on roads, it might 'magically' turn a house into a highway if forced into a collision scenario, due to lack of data in that distribution and interpolation issues with SGD.
- The brain is the optimizer, not just the model. Evidence: The universal need for sleep across intelligent species, and its role in long-term memory and training, suggests a continuous optimization process that current AI architectures lack.
- There is definitely an architecture that's going to be more performant than the Transformer. Evidence: Attributed to Sam Altman, suggesting the Transformer's limitations, particularly in time-domain compression.

## Quotes

> "One of the biggest open problems in AI right now is how to solve sample efficiency."
> "World models. We're going to discuss the motivation and math behind world models, current applications, and why this approach might be the key to unlocking AGI."
> "intelligence per watt and intelligence per sample."
> "perfect sample efficiency would be zero samples"
> "Can you imagine if like we needed to collect 1 million training examples of like us shooting spaceships to the moon to like know how to do it because like complet it would be we definitely wouldn't have the Apollo missions, right?"
> "the entire point of the growing neoortex for the during the great cortical expansion 10 million years ago was to get better and better and better and better at world modeling"
> "All of this stuff ultimately comes down to ways to estimate to to model this non-ifferiable stochastic process."
> "the cardality of the action space must be extremely small. If it's big, sad."
> "if I squint and I look at a bird and I squint and I look at a plane I'm like yeah it's kind of similar."
> "the brain is the optimizer, not the model"
> "There's no intelligent species that we're aware of that have any amount of intelligence that don't sleep."
> "each cortical area estimates both latent sensory states and actions and the cortex as a whole predicts the consequences of those actions."
