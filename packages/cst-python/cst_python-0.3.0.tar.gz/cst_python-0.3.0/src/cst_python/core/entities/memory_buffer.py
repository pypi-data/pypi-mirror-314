class MemoryBuffer:
    '''
    MemoryBuffer is a generic holder for memory objects. It may be used to
    produce sensory buffers, action buffers or other very short term memory
    structures.
    '''
    def __init__(self) -> None:
        raise NotImplementedError()