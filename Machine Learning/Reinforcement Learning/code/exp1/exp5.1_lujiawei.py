from __future__ import annotations

from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Patch

import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

import gym

class BlackjackAgent:
    def __init__(
        self,
        learning_rate: float,
        initial_epsilon: float,
        epsilon_decay: float,
        final_epsilon: float,
        discount_factor: float = 0.95,
    ):
        """
        Initialize a Reinforcement Learning agent with an empty dictionary
        of state-action values (q_values), a learning rate and an epsilon.
        """
        self.q_values = defaultdict(lambda: np.zeros(2))  # Blackjack has 2 actions: stick or hit
        self.lr = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = initial_epsilon
        self.epsilon_decay = epsilon_decay
        self.final_epsilon = final_epsilon
        self.training_error = []

    def get_action(self, obs: tuple[int, int, bool]) -> int:
        """Epsilon-greedy action selection."""
        if np.random.random() < self.epsilon:
            return env.action_space.sample()
        else:
            return int(np.argmax(self.q_values[obs]))

    def update(self, track_obs_action_reward: list[tuple[int, int, int]]):
        total_discounted_reward = 0
        visited_list = []
        for obs, action, reward in reversed(track_obs_action_reward):
            total_discounted_reward = self.discount_factor * total_discounted_reward + reward
            if (obs, action) not in visited_list:
                self.q_values[obs][action] += self.lr * (total_discounted_reward - self.q_values[obs][action])
                visited_list.append((obs, action))
            self.training_error.append(total_discounted_reward - self.q_values[obs][action])

    def decay_epsilon(self):
        self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)

def visualize_training(return_queue, length_queue, agent):
    fig, axs = plt.subplots(ncols=3, figsize=(12, 5))
    axs[0].set_title("Episode rewards")
    reward_moving_average = np.convolve(np.array(return_queue), np.ones(rolling_length), mode="valid") / rolling_length
    axs[0].plot(range(len(reward_moving_average)), reward_moving_average)

    axs[1].set_title("Episode lengths")
    length_moving_average = np.convolve(np.array(length_queue), np.ones(rolling_length), mode="same") / rolling_length
    axs[1].plot(range(len(length_moving_average)), length_moving_average)

    axs[2].set_title("Training Error")
    training_error_moving_average = np.convolve(np.array(agent.training_error), np.ones(rolling_length), mode="same") / rolling_length
    axs[2].plot(range(len(training_error_moving_average)), training_error_moving_average)

    plt.tight_layout()
    plt.show()

def create_grids(agent, usable_ace):
    state_value = defaultdict(float)
    policy = defaultdict(int)
    for obs, action_values in agent.q_values.items():
        state_value[obs] = float(np.max(action_values))
        policy[obs] = int(np.argmax(action_values))

    player_count, dealer_count = np.meshgrid(
        np.arange(12, 22),
        np.arange(1, 11),
    )

    value = np.apply_along_axis(
        lambda obs: state_value[(obs[0], obs[1], usable_ace)],
        axis=2,
        arr=np.dstack([player_count, dealer_count]),
    )

    policy_grid = np.apply_along_axis(
        lambda obs: policy[(obs[0], obs[1], usable_ace)],
        axis=2,
        arr=np.dstack([player_count, dealer_count]),
    )

    return (player_count, dealer_count, value), policy_grid

def create_plots(value_grid, policy_grid, title: str):
    player_count, dealer_count, value = value_grid
    fig = plt.figure(figsize=plt.figaspect(0.4))
    fig.suptitle(title, fontsize=16)

    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax1.plot_surface(
        player_count,
        dealer_count,
        value,
        rstride=1,
        cstride=1,
        cmap="viridis",
        edgecolor="none",
    )
    ax1.set_title(f"State values: {title}")
    ax1.set_xlabel("Player sum")
    ax1.set_ylabel("Dealer showing")
    ax1.set_zlabel("Value", fontsize=14, rotation=90)
    ax1.view_init(20, 220)

    fig.add_subplot(1, 2, 2)
    ax2 = sns.heatmap(policy_grid, linewidth=0, annot=True, cmap="Accent_r", cbar=False)
    ax2.set_title(f"Policy: {title}")
    ax2.set_xlabel("Player sum")
    ax2.set_ylabel("Dealer showing")
    ax2.set_xticklabels(range(12, 22))
    ax2.set_yticklabels(["A"] + list(range(2, 11)), fontsize=12)

    legend_elements = [
        Patch(facecolor="lightgreen", edgecolor="black", label="Hit"),
        Patch(facecolor="grey", edgecolor="black", label="Stick"),
    ]
    ax2.legend(handles=legend_elements, bbox_to_anchor=(1.3, 1))
    return fig

def visualize_policy(agent, usable_ace):
    value_grid, policy_grid = create_grids(agent, usable_ace)
    title = "With usable ace" if usable_ace else "Without usable ace"
    create_plots(value_grid, policy_grid, title)
    plt.show()

if __name__ == '__main__':
    env = gym.make("Blackjack-v1")

    learning_rate = 0.01
    n_episodes = 100_000
    initial_epsilon = 1.0
    epsilon_decay = initial_epsilon / (n_episodes / 2)
    final_epsilon = 0.1
    rolling_length = 500

    agent = BlackjackAgent(
        learning_rate=learning_rate,
        initial_epsilon=initial_epsilon,
        epsilon_decay=epsilon_decay,
        final_epsilon=final_epsilon,
    )

    return_queue = []
    length_queue = []

    for episode in range(n_episodes):
        obs = env.reset()
        if isinstance(obs, tuple):  # gym >=0.26 returns (obs, info)
            obs = obs[0]
        done = False
        track_obs_action_reward = []
        steps = 0
        total_reward = 0

        while not done:
            action = agent.get_action(obs)
            result = env.step(action)

            if len(result) == 5:
                next_obs, reward, terminated, truncated, _ = result
                done = terminated or truncated
            else:
                next_obs, reward, done, _ = result

            track_obs_action_reward.append((obs, action, reward))
            total_reward += reward
            obs = next_obs
            steps += 1

        agent.update(track_obs_action_reward)
        agent.decay_epsilon()
        return_queue.append(total_reward)
        length_queue.append(steps)

    visualize_training(return_queue, length_queue, agent)
    visualize_policy(agent, usable_ace=True)
    visualize_policy(agent, usable_ace=False)

    env.close()
