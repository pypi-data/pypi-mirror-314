import traceback
from typing import List

from cst_python.python import alias
from .codelet import Codelet
from .memory import Memory


class CodeRack:
    '''
    Following Hofstadter and Mitchell
    "The copycat project: A model of mental fluidity and analogy-making". Pool of
    all alive codelets in the system. The whole arena in the Baars-Franklin
    metaphor.
    '''

    def __init__(self) -> None:
        self._all_codelets :List[Codelet] = []

    #@alias.alias("getAllCodelets", "get_all_codelets")
    @property
    def all_codelets(self) -> List[Codelet]:
        '''
        List of all alive codelets in the system
        '''
        return self._all_codelets

    #@alias.alias("setAllCodelets", "set_all_codelets")
    @all_codelets.setter
    def all_codelets(self, value:List[Codelet]) -> None:
        self._all_codelets = value

    #@alias.alias("add_codelet")
    def add_codelet(self, codelet:Codelet) -> None:
        '''
        Adds a new Codelet to the Coderack

        Args:
            codelet (Codelet): codelet to be added.
        '''
        self._all_codelets.append(codelet)

    #@alias.alias("insertCodelet")
    def insert_codelet(self, codelet:Codelet) -> Codelet:
        '''
        Creates a codelet and adds it to this coderack.

        Args:
            codelet (Codelet): codelet to be created.

        Returns:
            Codelet: the own codelet inserted, if it is needed to concatenate to
                further methods calls.
        '''
        self.add_codelet(codelet)

        return codelet
    
    #@alias.alias("createCodelet")
    def create_codelet(self, activation:float, broadcast:List[Memory],
                       inputs:List[Memory], outputs:List[Memory],
                       codelet:Codelet) -> Codelet:
        '''
        Creates a codelet and adds it to this coderack.

        Args:
            activation (float): codelet's activation.
            broadcast (List[Memory]): list of memory objects which were broadcast lately (treated as
                input memories).
            inputs (List[Memory]): list of input memories.
            outputs (List[Memory]): list o output memories.
            codelet (Codelet): codelet to be created.

        Returns:
            Codelet: the codelet created.
        '''
        
        try:
            codelet.activation = activation
        except Exception as e:
            traceback.print_exception(e)

        codelet.broadcast = broadcast
        codelet.inputs = inputs
        codelet.outputs = outputs

        self.add_codelet(codelet)

        return codelet
    
    #@alias.alias("destroyCodelet")
    def destroy_codelet(self, codelet:Codelet) -> None:
        '''
        Removes a codelet from coderack.

        Args:
            codelet (Codelet): the codelet to be destroyed.
        '''
        codelet.stop()
        self._all_codelets.remove(codelet)

    #@alias.alias("shutDown", "shut_down")
    def shutdow(self):
        '''
        Destroys all codelets. Stops CodeRack's thread.
        '''
        self.stop()
        self._all_codelets.clear()

    def start(self) -> None:
        '''
        Starts all codelets in coderack.
        '''
        for codelet in self._all_codelets:
            codelet.start()

    def stop(self) -> None:
        '''
        Stops all codelets within CodeRack.
        '''        
        for codelet in self._all_codelets:
            codelet.stop()
