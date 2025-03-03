from .game import *
from .node import Node
class Pool:
    def __init__(self, capacity):
        self.nodes = []
        self.ptrs = []
        self.size = capacity
        self.grow()

    def grow(self):
        self.nodes = [Node() for _ in range(self.size)]
        for node in self.nodes:
            self.ptrs.append(node)  # Assuming nodes are directly appended as pointers

    def pop(self):
        return self.ptrs.pop()  # Safely pop the last element

    def push(self, node):
        for child in node.children:
            self.push(child)
        node.reinit()
        self.ptrs.append(node)
# Define a constant for POLICY_SIZE

class Sample:
    def __init__(self, node:Node):
        self.input = [0.0] * INPUT_SIZE
        self.p = node.prob_vector()
        self.v = node.q / node.visits
        self.visits = 1
        self.hash = node.game.hash()
        node.game.on_set_indices(lambda i: self.set_input(i))

    def set_input(self, index):
        self.input[index] = 1.0

class SampleStore:
    def __init__(self):
        self.samples = {}

    def add_sample(self, sample):
        existing_sample = self.samples.get(sample.hash)
        if existing_sample is not None:
            existing_sample.visits += 1
            for i in range(POLICY_SIZE):
                existing_sample.p[i] += sample.p[i]
            existing_sample.v += sample.v
        else:
            self.samples[sample.hash] = sample
