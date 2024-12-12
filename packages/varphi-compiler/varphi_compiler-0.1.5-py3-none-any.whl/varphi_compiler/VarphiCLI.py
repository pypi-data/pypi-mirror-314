from dataclasses import dataclass
import sys
import json
from collections import defaultdict
from enum import Enum, auto
import random

class TapeCharacter(Enum):
    BLANK = auto()
    TALLY = auto()

class HeadDirection(Enum):
    LEFT = auto()
    RIGHT = auto()

@dataclass
class Instruction:
    nextState: "State"  # Quotes for forward reference
    characterToPlace: TapeCharacter
    directionToMove: HeadDirection
    lineNumber: int

class State:
    name: str
    onTally: list[Instruction]
    onBlank: list[Instruction]

    def __init__(self, name: str) -> None:
        self.onTally = []
        self.onBlank = []
        self.name = name

    def addOnTallyInstruction(self, instruction: Instruction) -> None:
        self.onTally.append(instruction)

    def addOnBlankInstruction(self, instruction: Instruction) -> None:
        self.onBlank.append(instruction)

class NoTallyException(Exception):
    pass

class Tape:
    _tape: defaultdict[int, TapeCharacter]
    _maxAccessedIndex: int
    _minAccessedIndex: int

    def __init__(self, initialValues: list[TapeCharacter]) -> None:
        self._tape = defaultdict(lambda: TapeCharacter.BLANK)
        self._maxAccessedIndex = 0
        self._minAccessedIndex = 0
        # Extract the initial values from the `initialValues` array and place them on the tape.
        # However, ensure that at least one tally is present on the tape, and raise `NoTallyException` if not.
        i = 0
        foundTally = False
        for initialValue in initialValues:
            if initialValue == TapeCharacter.TALLY:
                self[i] = initialValue
                i += 1
                foundTally = True
            elif initialValue == TapeCharacter.BLANK and not foundTally:
                continue  # Index 0 on the tape must initially contain a tally
            else:
                self[i] = initialValue
                i += 1
        if not foundTally:
            raise NoTallyException("Error: Please specify at least one tally (1) on the input tape")


    def _updateInternalsAfterTapeAccess(self, index: int) -> None:
        if index > self._maxAccessedIndex:
            self._maxAccessedIndex = index
        if index < self._minAccessedIndex:
            self._minAccessedIndex = index
    
    def __getitem__(self, index: int) -> TapeCharacter:
        self._updateInternalsAfterTapeAccess(index)
        return self._tape[index]
    
    def __setitem__(self, index: int, value: TapeCharacter) -> None:
        self._updateInternalsAfterTapeAccess(index)
        self._tape[index] = value
    
    def __repr__(self) -> str:
        representation = ""
        for i in range(self._minAccessedIndex, self._maxAccessedIndex + 1):
            representation += '1' if self._tape[i] == TapeCharacter.TALLY else '0'
        return representation
    
class Head:
    tape: Tape
    currentTapeCell: int

    def __init__(self, tape: Tape) -> None:
        self.tape = tape
        self.currentTapeCell = 0
    
    def right(self) -> None:
        self.currentTapeCell += 1
    
    def left(self) -> None:
        self.currentTapeCell -= 1
    
    def read(self) -> TapeCharacter:
        return self.tape[self.currentTapeCell]
    
    def write(self, value: TapeCharacter) -> None:
        self.tape[self.currentTapeCell] = value
    
    def __repr__(self) -> str:
        return str(self.currentTapeCell)


class Manager:
    tape: Tape
    head: Head
    state: State
    nextInstruction: Instruction

    def __init__(self, tape: Tape, initialState: State) -> None:
        self.tape = tape
        self.head = Head(tape)
        self.state = initialState
        self.loadNextInstruction()
    
    def loadNextInstruction(self) -> None:
        character = self.head.read()
        possibleInstructionsToFollow = self.state.onTally if character == TapeCharacter.TALLY else self.state.onBlank
        if len(possibleInstructionsToFollow) == 0:
            self.nextInstruction = None
            return
        self.nextInstruction = random.choice(possibleInstructionsToFollow)
    
    def executeNextInstruction(self) -> None:
        self.state = self.nextInstruction.nextState
        self.head.write(self.nextInstruction.characterToPlace)
        if self.nextInstruction.directionToMove == HeadDirection.LEFT:
            self.head.left()
        else:
            self.head.right()

def getTapeFromStdin() -> Tape:
    initialCharacters = []
    inputCharacter = sys.stdin.read(1)
    while inputCharacter not in {'\n', '\r'}:
        if inputCharacter == '0':
            initialCharacters.append(TapeCharacter.BLANK)
        elif inputCharacter == '1':
            initialCharacters.append(TapeCharacter.TALLY)
        else:
            print(f"Error: Invalid tape character (ASCII {ord(inputCharacter)}).")
            sys.exit(-1)
        inputCharacter = sys.stdin.read(1)
    return Tape(initialCharacters)

def prettyStringTapeWithHead(tape: Tape, head: Head) -> str:
    tapeAsString = ""
    for i in range(tape._minAccessedIndex, tape._maxAccessedIndex + 1):
        character = '1' if tape[i] == TapeCharacter.TALLY else '0'
        if i == 0:
            character = '{' + character + '}'
        if i == head.currentTapeCell:
            character = '[' + character + ']'
        tapeAsString += character
    return tapeAsString


class InvalidTapeCharacterException(Exception):
    pass

def getTapeFromString(string: str) -> Tape:
    initialCharacters = []
    for inputCharacter in string:
        if inputCharacter == '0':
            initialCharacters.append(TapeCharacter.BLANK)
        elif inputCharacter == '1':
            initialCharacters.append(TapeCharacter.TALLY)
        else:
            raise InvalidTapeCharacterException(f"Error: Invalid tape character (ASCII #{ord(inputCharacter)}).")
    return Tape(initialCharacters)

def main(initialState: State):
    tape = getTapeFromStdin()
    manager = Manager(tape, initialState)
    while manager.nextInstruction is not None:
        manager.executeNextInstruction()
        manager.loadNextInstruction()
    print(manager.tape)