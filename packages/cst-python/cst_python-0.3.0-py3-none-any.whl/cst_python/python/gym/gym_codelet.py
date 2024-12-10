from typing import Optional, Any, cast, Mapping

try:
    import gymnasium as gym
except ModuleNotFoundError:
    import gym # type: ignore

from cst_python.core.entities import Codelet, Mind, Memory, MemoryObject

class GymCodelet(Codelet):
    '''
    Codelet to interface with gymnasium/gym environments. Creates memories for the observation, 
    action, reward, reset, terminated, truncated, info and seed; and updates them stepping the 
    environment with the action. 
    '''

    _last_indexes : dict[str, int] = {"reward":-1, "reset":-1, 
                                      "terminated":-1, "truncated":-1, 
                                      "info":-1, "seed":-1,
                                      "step_count":-1}

    def __init__(self, mind:Mind, env:gym.Env):
        '''
        GymCodelet constructor.

        Always runs automatically in publish-subscribe mode.

        Args:
            mind (Mind): agent's mind.
            env (gym.Env): environment to interface.
        '''
        super().__init__()

        assert mind._raw_memory is not None # RawMemory cannot be None for creating memories
        
        self.env = env
        
        self.observation_memories = self.space_to_memories(mind, env.observation_space)
        self.action_memories = self.space_to_memories(mind, env.action_space, action=True)

        self._common_memories : dict[str, MemoryObject] = {}
        for name in ["reward", "reset", "terminated", "truncated", "info", "seed", "step_count"]:
            self._last_indexes[name] += 1

            memory_name = name
            if self._last_indexes[name] != 0:
                memory_name += str(self._last_indexes[name])
            
            self._common_memories[name] = cast(MemoryObject, mind.create_memory_object(memory_name))

        self._common_memories["reward"].set_info(0.0)
        self._common_memories["reset"].set_info(False)
        self._common_memories["terminated"].set_info(False)
        self._common_memories["truncated"].set_info(False)
        self._common_memories["info"].set_info({})
        self._common_memories["seed"].set_info(None)
        self._common_memories["step_count"].set_info(0)


        self.is_memory_observer = True
        for memory_name in self.action_memories:
            memory = self.action_memories[memory_name]
            memory.add_memory_observer(self)
        self._common_memories["reset"].add_memory_observer(self)

        self._last_reset = 0
    
    @property
    def reward_memory(self) -> MemoryObject:
        '''
        Memory that contains the environment reward (float).
        '''
        return self._common_memories["reward"]
    
    @property
    def reset_memory(self) -> MemoryObject:
        '''
        Memory that contains the environment reset.

        If timestamp changes, the codelet resets the environment.
        '''
        return self._common_memories["reset"]
    
    @property
    def terminated_memory(self) -> MemoryObject:
        '''
        Memory that contains the environment terminated state.
        '''
        return self._common_memories["terminated"]
    
    @property
    def truncated_memory(self) -> MemoryObject:
        '''
        Memory that contains the environment truncated state.
        '''
        return self._common_memories["truncated"]
    
    @property
    def info_memory(self) -> MemoryObject:
        '''
        Memory that contains the environment info.
        '''
        return self._common_memories["info"]
    
    @property
    def seed_memory(self) -> MemoryObject:
        '''
        Memory that contains the seed to use in the environment reset.
        '''
        return self._common_memories["seed"]

    @property
    def step_count_memory(self) -> MemoryObject:
        '''
        Memory that contains the step count for the current environment
        episode.
        '''
        return self._common_memories["step_count"]
    
    def access_memory_objects(self) -> None: #NOSONAR
        pass

    def calculate_activation(self) -> None: #NOSONAR
        pass

    def proc(self) -> None:
        if self._last_reset < self.reset_memory.get_timestamp():
            self._last_reset = self.reset_memory.get_timestamp()

            observation, info = self.env.reset(seed=self.seed_memory.get_info())
            reward = 0.0
            terminated = False
            truncated = False
            step_count = 0

        else:
            action = self.memories_to_space(self.action_memories, self.env.action_space)
            observation, r, terminated, truncated, info = self.env.step(action)
            reward = float(r) #SupportsFloat to float

            step_count = self.step_count_memory.get_info()+1
    
        self.reward_memory.set_info(reward)
        self.terminated_memory.set_info(terminated)
        self.truncated_memory.set_info(truncated)
        self.info_memory.set_info(info)
        self.step_count_memory.set_info(step_count)

        self.sample_to_memories(observation, self.observation_memories)

    @classmethod
    def reset_indexes(cls) -> None:
        '''
        Reset the indexes for setting the sufix of new memories.
        '''
        cls._last_indexes = {"reward":-1, "reset":-1, 
                                      "terminated":-1, "truncated":-1, 
                                      "info":-1, "seed":-1,
                                      "step_count":-1}

    @classmethod
    def space_to_memories(cls, mind:Mind, 
                          space:gym.Space,
                          action:bool=False,
                          memory_prefix:Optional[str]=None) -> dict[str, MemoryObject]:
        '''
        Creates memories from a gym Space definition.

        Args:
            mind (Mind): mind to create the memories.
            space (gym.Space): space defining the memories to create.
                If gym.space.Dict, creates a memory for each element, 
                creates a single memory otherwise.
            action (bool, optional): If True, creates a memory with 'action' 
                name for non Dict space, uses 'observation' name otherwise. 
                Defaults to False.
            memory_prefix (Optional[str], optional): prefix to memories name. 
                Defaults to None.

        Returns:
            dict[str, MemoryObject]: created memories, indexed by the space
                element name or 'action'/'observation'.
        '''
        assert mind._raw_memory is not None # RawMemory cannot be None for creating memories

        if memory_prefix is None:
            memory_prefix = ""

        memories : dict[str, MemoryObject] = {}

        if isinstance(space, gym.spaces.Dict):
            for space_name in space:
                subspace = space[space_name]

                name = space_name
                if space_name in cls._last_indexes:
                    cls._last_indexes[space_name] += 1
                    name += str(cls._last_indexes[space_name])
                else:
                    cls._last_indexes[space_name] = 0
                name = memory_prefix+name

                info = subspace.sample()
                memory = cast(MemoryObject, mind.create_memory_object(name, info))
                memories[space_name] = memory
            
        else:
            if action:
                space_name = "action"
            else:
                space_name = "observation"

            name = space_name
            if space_name in cls._last_indexes:
                cls._last_indexes[space_name] += 1
                name += str(cls._last_indexes[space_name])
            else:
                cls._last_indexes[space_name] = 0

            name = memory_prefix+name

            info = space.sample()
            memory = cast(MemoryObject, mind.create_memory_object(name, info))
            memories[space_name] = memory
            

        return memories
    
    @classmethod
    def sample_to_memories(cls, sample:Mapping[str, Any]|Any, 
                           memories:Mapping[str, Memory]) -> None:
        '''
        Writes a gym.Space sample to memories.

        Args:
            sample (Mapping[str, Any] | Any): sample to write in the memories.
            memories (Mapping[str, Memory]): memories corresponding to 
                the space elements.
        '''
        if isinstance(sample, dict):
            for name in sample:
                element = sample[name]
                memory = memories[name]
                
                memory.set_info(element)
        else:
            memory = memories[next(iter(memories))]
            memory.set_info(sample)
        

    @classmethod
    def memories_to_space(cls, memories:Mapping[str, Memory], 
                          space:gym.Space) -> dict[str, Any]|Any:
        '''
        Convert the memories info to the space sample.

        Args:
            memories (Mapping[str, Memory]): memories to get the sample.
            space (gym.Space): space the sample belongs

        Raises:
            ValueError: if the generated sample from the memories 
                doesn't belongs to the space

        Returns:
            dict[str, Any]|Any: converted sample.
        '''
        if isinstance(space, gym.spaces.Dict):
            sample = {}
            for memory_name in memories:
                sample[memory_name] = memories[memory_name].get_info()
        else:
            sample = memories[next(iter(memories))].get_info()

        if not space.contains(sample):
            raise ValueError("Memories do not correspond to an element of the Space.")
        
        return sample