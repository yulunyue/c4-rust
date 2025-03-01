import numpy as np
from .node import Node
from .sample import Pool,SampleStore,Sample
from .nn import NNManager
from typing import Optional
from .game import *
import time
class MCTS:
    def __init__(self):
        self.pool = Pool(2000000)
        self.root = Node()
        self.nn = NNManager()
        self.nn.read_weights()
        for _ in range(2):
            self.root.playout(self.nn, self.pool)

    def __del__(self):
        new_root = Node()
        self.pool.push(new_root)
        for n in self.pool.ptrs:
            # Simulating the raw pointer behavior
            pass
    
    def self_play(self,ss:SampleStore):
        while self.root.game.outcome == Outcome.NULL:
            a,p=self.get_move_probs_play()
            sample=Sample(self.root)
            sample.p=p.copy()
            ss.add_sample(sample)
            self.update_with_action(a)
        print(f"%.4f nn rate"%self.nn.hit/self.nn.access)

    def clear(self):
        a = self.pool.pop()
        self.root = a
        self.pool.push(a)

    def update_with_action(self, action: int):
        if not self.root.children:
            self.root.select(self.nn, self.pool)
        new_root: Optional[Node] = None
        while self.root.children:
            if self.root.children[-1].game.last_move == action:
                new_root = self.root.children.pop()
            else:
                self.pool.push(self.root.children.pop())
        self.root = new_root
        self.pool.push(new_root)

    def get_move_probs_play(self, end_time):
        while time.time() < end_time:
            self.root.playout(self.nn, self.pool)
        best_child = max(self.root.children, key=lambda b: b.value if self.root.terminal else b.visits)
        print(f"root visits: {self.root.visits}")
        return best_child.game.last_move

    def cg(self):
        end_time = None
        input_line = ""
        input_line = sys.stdin.readline().strip()
        my_last: int = -1
        for i in range(65):
            input_line = sys.stdin.readline().strip()
            for _ in range(7):
                input_line = sys.stdin.readline().strip()
            input_line = sys.stdin.readline().strip()
            num_valid_actions = int(input_line)
            for _ in range(num_valid_actions):
                input_line = sys.stdin.readline().strip()
            input_line = sys.stdin.readline().strip()
            if i == 0:
                end_time = time.time() + 0.9
            else:
                end_time = time.time() + 0.1
            if my_last != -1:
                self.update_with_action(my_last)
            hard_coded = -1
            if input_line != "STEAL":
                opp_action = int(input_line)
                if opp_action >= 0:
                    self.update_with_action(opp_action)
                if opp_action == -1:
                    hard_coded = 1
                    self.update_with_action(hard_coded)
                    my_last = -1
                elif i == 0:
                    hard_coded = -2