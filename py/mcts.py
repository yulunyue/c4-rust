# Framework: Rust to Python translation for MCTS (Monte Carlo Tree Search)

import random
from time import time

DIRICHLET_EPS = 0.3

class MCTS:
    def __init__(self):
        self.roots = [Node.new(), Node.new()]
        self.nn = NN.new()
        self.random_generator = random.Random()

    def update_with_action(self, player_index, action_index):
        root = self.roots[player_index]
        assert len(root.children) > 0
        new_root = Node.new()
        while len(root.children) > 0:
            child_node = root.children.pop()
            if child_node.action == action_index:
                new_root = child_node
        self.roots[player_index] = new_root

    def playout(self, game_instance):
        game = game_instance.clone()
        leaf = False
        value = -69.0

        stacks = [[], []]
        for i in range(2):
            stacks[i].append(self.roots[i])

        while not leaf and not game.is_game_over():
            actions = [69, 69]
            for i in range(2):
                st = stacks[i][-1]
                if not st.expanded:
                    value = st.expand(self.nn, game, i)
                    if i == 1:
                        value = -value
                    leaf = True
                else:
                    actions[i] = st.select()
                    stacks[i].append(st.children[actions[i]])

            if not leaf:
                game.step([Action.new(actions[0], False), Action.new(actions[1], True)])

        if game.is_game_over():
            value = game.score(0)

        for i in range(min(len(stacks[0]), len(stacks[1]))):
            stacks[0][i].update(value)
            stacks[1][i].update(-value)

    def get_move_probs_selfplay(self, player_index):
        probabilities = self.roots[player_index].prob_vector()

        direction_noise = dirichlet_noise(self.random_generator)
        total_sum = sum(direction_noise[c.action] for c in self.roots[player_index].children)

        for child in self.roots[player_index].children:
            index = child.action
            probabilities[index] = (probabilities[index] * (1. - DIRICHLET_EPS) +
                                    DIRICHLET_EPS * direction_noise[index] / total_sum)

        best_value = 0.0
        action = None
        for child in self.roots[player_index].children:
            decision_value = probabilities[child.action] * self.random_generator.random()
            if decision_value > best_value:
                best_value = decision_value
                action = child.action

        return action, probabilities

    def get_move_probs_play(self, end_time):
        while time() < end_time:
            self.root.playout(self.nn, self.pool)
        action = max(self.root.children, key=lambda b: b.value if self.root.terminal else b.visits)
        print(f"root visits: {self.root.visits}")
        return action.game.last_move

    def self_play(self, sample_storage):
        game = Game.new(self.random_generator.randint(0, 2**63 - 1))
        new_samples = []
        while not game.is_game_over():
            for _ in range(CONF.iters):
                self.playout(game)
            actions = [69, 69]
            for i in range(2):
                action, probabilities = self.get_move_probs_selfplay(i)
                actions[i] = action
                sample = Sample.new(self.roots[i], game, i)
                sample.p[:] = probabilities
                new_samples.append(sample)
                self.update_with_action(i, action)
            game.step([Action.new(actions[0], False), Action.new(actions[1], True)])

        for i, sample in enumerate(new_samples):
            sample.v = game.score(i % 2)
            sample_storage.append(sample)

        print(f"truns: {game.game_turn}, scores: {game.compute_player_score(0)} vs {game.compute_player_score(1)}. val:{self.nn.run_game(game, 0).v}, ku_val: {self.roots[0].q} vs {self.roots[1].q}")