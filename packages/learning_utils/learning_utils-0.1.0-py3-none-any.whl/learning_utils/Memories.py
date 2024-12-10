"""
Replay buffer that can handle any number of things we need to remember for the network
"""

from collections import deque
import random


class ReplayBuffer:
    def __init__(self, maxlen: int) -> None:
        self.memory = deque(maxlen=maxlen)

    def add(self, *args) -> None:
        """
        Takes a variable number of arguments to store in a the replay buffer
        """
        l = []
        for arg in args:
            l.append(arg)

        t = tuple(l)
        self.memory.append(t)
        

    def sample(self, batch_size: int) -> zip:
        """
        Sample a batch of batch_size. 
        Returns a zip object, so you will have to unpack the sample yourself.  

        args:
            batch_size (int): Size of sample

        returns: 
            batch (zip object): Your samples
        """
        batch = random.sample(self.memory, batch_size)
        batch = zip(*batch)
        return batch

    def len(self) -> int:
        """
        Current size of the replay buffer
        """
        return len(self.memory)
