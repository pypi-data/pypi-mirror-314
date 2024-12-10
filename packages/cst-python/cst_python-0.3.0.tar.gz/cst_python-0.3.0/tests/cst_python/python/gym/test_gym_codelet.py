from contextlib import redirect_stdout
import math
import unittest
import time
import threading
import io

import gymnasium as gym
from gymnasium.spaces import Box, Dict
import numpy as np
from numpy.testing import assert_array_almost_equal

from cst_python import MemoryObject, Mind
from cst_python.python.gym import GymCodelet

class TestGymCodelet(unittest.TestCase):
    def setUp(self) -> None:
        ...
    
    def test_space_to_memories(self) -> None:
        space = Box(-1, 1, (2,))
        mind = Mind()

        GymCodelet.reset_indexes()

        memories = GymCodelet.space_to_memories(mind, space)
        keys = list(memories.keys())
        assert len(keys) == 1
        assert keys[0] == "observation"
        memory = memories[keys[0]]
        assert memory.get_name() == "observation"
        assert space.contains(memory.get_info())

        memories = GymCodelet.space_to_memories(mind, space)
        memory = memories[next(iter(memories))]
        assert memory.get_name() == "observation1"

        space = Dict({"x":Box(-1, 1, (2,)), "y":Box(-2, 1, (1,))})
        memories = GymCodelet.space_to_memories(mind, space)
        keys = list(memories.keys())
        assert len(keys) == 2
        assert "x" in keys
        assert "y" in keys
        assert memories["x"].get_name() == "x"
        assert memories["y"].get_name() == "y"
        
        memories = GymCodelet.space_to_memories(mind, space)
        keys = list(memories.keys())
        assert len(keys) == 2
        assert "x" in keys
        assert "y" in keys
        assert memories["x"].get_name() == "x1"
        assert memories["y"].get_name() == "y1"

    def test_sample_to_memories(self) -> None:
        space = Box(-1, 1, (2,))
        sample = space.sample()
        memories = {"observation":MemoryObject()}
        
        GymCodelet.sample_to_memories(sample, memories)

        assert_array_almost_equal(memories["observation"].get_info(), sample)


        space = Dict({"x":Box(-1, 1, (2,)), "y":Box(-2, 1, (1,))})
        sample = space.sample()
        memories = {"x":MemoryObject(), "y":MemoryObject()}

        GymCodelet.sample_to_memories(sample, memories)

        assert_array_almost_equal(memories["x"].get_info(), sample["x"])
        assert_array_almost_equal(memories["y"].get_info(), sample["y"])

    def test_memories_to_space(self) -> None:
        space = Box(-1, 1, (2,))
        sample = space.sample()
        memories = {"observation":MemoryObject()}
        memories["observation"].set_info(sample)

        reconstruced_sample = GymCodelet.memories_to_space(memories, space)
        assert space.contains(reconstruced_sample)
        assert_array_almost_equal(reconstruced_sample, sample)

        space = Dict({"x":Box(-1, 1, (2,)), "y":Box(-2, 1, (1,))})
        sample = space.sample()
        memories = {"x":MemoryObject(), "y":MemoryObject()}
        memories["x"].set_info(sample["x"])
        memories["y"].set_info(sample["y"])
        
        reconstruced_sample = GymCodelet.memories_to_space(memories, space)
        assert space.contains(reconstruced_sample)
        assert_array_almost_equal(reconstruced_sample["x"], sample["x"])
        assert_array_almost_equal(reconstruced_sample["y"], sample["y"])

    def test_episode(self) -> None:
        env = gym.make("MountainCar-v0")
        mind = Mind()
        gym_codelet = GymCodelet(mind, env)

        mind.start()

        assert gym_codelet.step_count_memory.get_info() == 0
        gym_codelet.reset_memory.set_info(True)
        assert gym_codelet.step_count_memory.get_info() == 0
        gym_codelet.action_memories["action"].set_info(1)
        assert gym_codelet.step_count_memory.get_info() == 1
        gym_codelet.action_memories["action"].set_info(1)
        assert gym_codelet.step_count_memory.get_info() == 2
        time.sleep(1e-3) #Minimum time for memory timestamp comparation is 1 ms
        gym_codelet.reset_memory.set_info(True)
        assert gym_codelet.step_count_memory.get_info() == 0

    def test_env_memories(self) -> None:
        env = gym.make("Blackjack-v1")
        mind = Mind()
        gym_codelet = GymCodelet(mind, env)

        assert len(gym_codelet.observation_memories) == 1
        assert "observation" in gym_codelet.observation_memories
        assert env.observation_space.contains(gym_codelet.observation_memories["observation"].get_info())

        assert len(gym_codelet.action_memories) == 1
        assert "action" in gym_codelet.action_memories
        assert env.action_space.contains(gym_codelet.action_memories["action"].get_info())