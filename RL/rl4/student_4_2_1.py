#!/usr/bin/env python3
# rewards: [golden_fish, jellyfish_1, jellyfish_2, ... , step]
rewards = [-100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, 0]

# Q learning learning rate
alpha = 0.5

# Q learning discount rate
gamma = 0.7

# Epsilon initial
epsilon_initial = 1

# Epsilon final
epsilon_final = 0.1

# Annealing timesteps
annealing_timesteps = 400

# threshold
threshold = 1e-4
