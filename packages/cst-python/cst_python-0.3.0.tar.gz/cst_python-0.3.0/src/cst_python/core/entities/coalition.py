class Coalition:
    '''
    A Coalition is a group of Codelets which are gathered in order to perform a
    task by summing up their abilities or to form a specific context.

    In CST, two codelets belong to the same coalition when they share information
    - pragmatically, when they write in and read from the same memory object.
    '''

    def __init__(self) -> None:
        raise NotImplementedError()