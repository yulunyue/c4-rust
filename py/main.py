# This code translates Rust to Python
import os
import threading
from collections import defaultdict
from .mcts import MCTS
class Config:
    def __init__(self, self_play, iters, cpuct, learning_rate=None, load_file=None):
        self.self_play = self_play
        self.iters = iters
        self.cpuct = cpuct
        self.learning_rate = learning_rate
        self.load_file = load_file

if os.name == "posix":  # Linux
    CONF = Config(
        self_play=False,
        iters=float('inf'),
        cpuct=3.0
    )
elif os.name == "nt":  # Windows
    CONF = Config(
        self_play=True,
        iters=100,
        cpuct=4.0,
        learning_rate=0.0001,
        load_file=True
    )

NNLEN = 29322 * 4

def main():
    if '--encode' in os.sys.argv:
        _, enc = encode_b16k("best.w32")
        st = ''.join(chr(c) for c in enc)

        path = "src/nn_string.py"
        if os.path.exists(path):
            os.remove(path)
        with open(path, 'w') as output:
            output.write(f'NNSTR = "{st}"')

    else:
        if os.name == "nt":  # Windows
            while True:
                handles = []

                for _ in range(1):
                    handle = threading.Thread(target=lambda: self_play())
                    handle.start()
                    handles.append(handle)

                combined_samples = []
                for handle in handles:
                    handle.join()
                    combined_samples.extend(handle.result())

                nn = NN()
                nn.train(combined_samples)

        elif os.name == "posix":  # Linux
            MCTS().cg()

def self_play():
    ss = []
    mcts = MCTS()
    for i in range(30):
        print(i)
        mcts.self_play(ss)

    return ss

if __name__ == "__main__":
    main()