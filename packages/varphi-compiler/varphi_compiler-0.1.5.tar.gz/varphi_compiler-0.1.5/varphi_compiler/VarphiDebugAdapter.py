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

class VarphiDebugAdapter:
    initialState: State
    manager: Manager | None
    noDebug: bool | None
    breakpoints: set[int]
    sourcePath: str | None

    def __init__(self, initialState: State):
        self.initialState = initialState
        self.breakpoints = set()
    
    def loop(self):
        try:
            while True:
                sys.stdin.buffer.read(16)  # Skip "Content-Length: "
                contentLengthString = ""
                character = sys.stdin.buffer.read(1)
                while character != b'\r':
                    contentLengthString += chr(character[0])
                    character = sys.stdin.buffer.read(1)
                # Skip the remaining \n\r\n
                sys.stdin.buffer.read(3)
                contentLength = int(contentLengthString)
                contentPart = sys.stdin.buffer.read(contentLength).decode()
                self.parseInput(contentPart)
        except Exception as e:
            import traceback
            exitedEvent = {}
            exitedEvent["exitCode"] = 0
            self.sendEvent("exited", exitedEvent)
            outputEvent = {}
            outputEvent["category"] = "stderr"
            outputEvent["output"] = str(traceback.format_exc())
            self.sendEvent("output", outputEvent)
            terminatedEvent = {}
            self.sendEvent("terminated", terminatedEvent)
            sys.exit(-1)
            
    def sendBodyPart(self, bodyPart: dict) -> None:
        bodyPartString = json.dumps(bodyPart)
        contentLength = str(len(bodyPartString))
        sys.stdout.buffer.write(b"Content-Length: ")
        sys.stdout.buffer.write(contentLength.encode("utf-8"))
        sys.stdout.buffer.write(b"\r\n\r\n")
        sys.stdout.buffer.write(bodyPartString.encode("utf-8"))
        sys.stdout.flush()
    
    def sendResponse(self, request_seq: int, success: bool, command: str, message: str | None = None, body: dict | None = None) -> None:
        bodyPart = {}
        bodyPart["type"] = "response"
        bodyPart["request_seq"] = request_seq
        bodyPart["success"] = success
        bodyPart["command"] = command
        if message is not None:
            bodyPart["message"] = message
        if body is not None:
            bodyPart["body"] = body
        self.sendBodyPart(bodyPart)

    
    def sendEvent(self, event: str, body: dict | None = None) -> None:
        bodyPart = {}
        bodyPart["type"] = "event"
        bodyPart["event"] = event
        if body is not None:
            bodyPart["body"] = body
        self.sendBodyPart(bodyPart)
        

    def parseInput(self, input: str):
        jsonInput = json.loads(input)
        if jsonInput["type"] == "request":
            self.handleRequest(jsonInput)
    
    def handleRequest(self, jsonInput):
        command = jsonInput["command"]
        if command == "initialize":
            self.handleInitializeRequest(jsonInput)
        if command == "launch":
            self.handleLaunchRequest(jsonInput)
        if command == "setBreakpoints":
            self.handleSetBreakpointsRequest(jsonInput)
        if command == "configurationDone":
            self.handleConfigurationDoneRequest(jsonInput)
        if command == "threads":
            self.handleThreadsRequest(jsonInput)
        if command == "stackTrace":
            self.handleStackTraceRequest(jsonInput)
        if command == "scopes":
            self.handleScopesRequest(jsonInput)
        if command == "variables":
            self.handleVariablesRequest(jsonInput)
        if command == "continue":
            self.handleContinueRequest(jsonInput)
        if command == "next":
            self.handleNextRequest(jsonInput)
        if command == "stepIn":
            self.handleStepInRequest(jsonInput)
        if command == "stepOut":
            self.handleStepOutRequest(jsonInput)
        if command == "disconnect":
            self.handleDisconnectRequest(jsonInput)
    
    def handleInitializeRequest(self, jsonInput):
        responseBody = {"supportsConfigurationDoneRequest": True, "supportsSingleThreadExecutionRequests": True}
        self.sendResponse(jsonInput["seq"], True, "initialize", None, responseBody)
        self.sendEvent("initialized")
    

    def handleSetBreakpointsRequest(self, jsonInput):
        responseBody = {}
        responseBody["breakpoints"] = []
        arguments = jsonInput["arguments"]
        if "breakpoints" in arguments:
            breakpoints = arguments["breakpoints"]
            for breakpoint in breakpoints:
                breakpointLineNumber = breakpoint["line"]
                self.breakpoints.add(breakpointLineNumber)
                breakpointResponse = {"verified": True}
                responseBody["breakpoints"].append(breakpointResponse)
        
        if "sourceModified" in arguments and arguments["sourceModified"]:
            raise Exception("Error: Source code change detected. Please kindly restart debugging.")
        else:
            self.sendResponse(jsonInput["seq"], True, "setBreakpoints", None, responseBody)
        if self.noDebug:
            self.breakpoints = set()
    
    def handleLaunchRequest(self, jsonInput):
        
        arguments = jsonInput["arguments"]
        if "noDebug" not in arguments:
            raise Exception("Error: Missing argument \"noDebug\" for Debug Adapter.")
        if "sourcePath" not in arguments:
            raise Exception("Error: Missing argument \"sourcePath\" for Debug Adapter.")
        if "tape" not in arguments:
            raise Exception("Error: Missing argument \"tape\" for Debug Adapter.")
        self.noDebug = arguments["noDebug"]
        self.sourcePath = arguments["sourcePath"]
        inputTape = arguments["tape"]
        self.manager = Manager(getTapeFromString(inputTape), self.initialState)
        self.sendResponse(jsonInput["seq"], True, "launch")

    def handleConfigurationDoneRequest(self, jsonInput):
        self.sendResponse(jsonInput["seq"], True, "configurationDone")
        if self.noDebug:
            # Give the user the end tape right away
            while self.manager.nextInstruction is not None:
                self.manager.executeNextInstruction()
                self.manager.loadNextInstruction()
            exitedEvent = {}
            exitedEvent["exitCode"] = 0
            self.sendEvent("exited", exitedEvent)
            outputEvent = {}
            outputEvent["category"] = "console"
            outputEvent["output"] = str(self.manager.tape)
            self.sendEvent("output", outputEvent)
            terminatedEvent = {}
            self.sendEvent("terminated", terminatedEvent)
        else:
            if len(self.breakpoints) == 0:
                # If there's no breakpoints, stop at the first line that will execute.
                stoppedEvent = {}
                stoppedEvent["reason"] = "step"
                stoppedEvent["threadId"] = 1
                stoppedEvent["allThreadsStopped"] = True
                self.sendEvent("stopped", stoppedEvent)
            else:
                while self.manager.nextInstruction is not None and self.manager.nextInstruction.lineNumber not in self.breakpoints:
                    self.manager.executeNextInstruction()
                    self.manager.loadNextInstruction()
                if self.manager.nextInstruction is not None:
                    stoppedEvent = {}
                    stoppedEvent["reason"] = "breakpoint"
                    stoppedEvent["threadId"] = 1
                    stoppedEvent["allThreadsStopped"] = True
                    self.sendEvent("stopped", stoppedEvent)
                else:
                    exitedEvent = {}
                    exitedEvent["exitCode"] = 0
                    self.sendEvent("exited", exitedEvent)
                    outputEvent = {}
                    outputEvent["category"] = "console"
                    outputEvent["output"] = str(self.manager.tape)
                    self.sendEvent("output", outputEvent)
                    terminatedEvent = {}
                    self.sendEvent("terminated", terminatedEvent)

    def handleThreadsRequest(self, jsonInput):
        responseBody = {}
        responseBody["threads"] = [{"id": 1, "name": "thread1"}]
        self.sendResponse(jsonInput["seq"], True, "threads", None, responseBody)

    def handleStackTraceRequest(self, jsonInput):
        responseBody = {}
        stackFrame = {}
        stackFrame["id"] = 0
        stackFrame["name"] = "source"
        source = {}
        source["name"] = "Varphi Program"
        source["path"] = self.sourcePath
        stackFrame["source"] = source

        stackFrame["line"] = self.manager.nextInstruction.lineNumber
        stackFrame["column"] = 0
        responseBody["stackFrames"] = [stackFrame]
        responseBody["totalFrames"] = 1
        self.sendResponse(jsonInput["seq"], True, "stackTrace", None, responseBody)
    
    def handleScopesRequest(self, jsonInput):
        scope = {}
        scope["name"] = "Machine Variables"
        scope["variablesReference"] = 1  # The tape, the index of the head, the index of zero (first head location), state

        responseBody = {}
        responseBody["scopes"] = [scope]
        self.sendResponse(jsonInput["seq"], True, "scopes", None, responseBody)
    
    def handleVariablesRequest(self, jsonInput):
        tapeVariable = {}
        tapeVariable["name"] = "Tape"
        tapeVariable["value"] = prettyStringTapeWithHead(self.manager.tape, self.manager.head)
        tapeVariable["variablesReference"] = 0

        headVariable = {}
        headVariable["name"] = "Head"
        headVariable["value"] = str(self.manager.head)
        headVariable["variablesReference"] = 0

        zeroVariable = {}
        zeroVariable["name"] = "Tape Zero"
        zeroVariable["value"] = str(-self.manager.tape._minAccessedIndex)
        zeroVariable["variablesReference"] = 0

        stateVariable = {}
        stateVariable["name"] = "State"
        stateVariable["value"] = str(self.manager.state.name)
        stateVariable["variablesReference"] = 0

        responseBody = {}
        responseBody["variables"] = [tapeVariable, headVariable, zeroVariable, stateVariable]
        self.sendResponse(jsonInput["seq"], True, "variables", None, responseBody)
    
    def handleNextRequest(self, jsonInput):
        self.manager.executeNextInstruction()
        self.manager.loadNextInstruction()
        responseBody = {}
        responseBody["allThreadsContinued"] = True
        self.sendResponse(jsonInput["seq"], True, "next", None, responseBody)
        if self.manager.nextInstruction is not None:
            stoppedEvent = {}
            stoppedEvent["reason"] = "step"
            stoppedEvent["threadId"] = 1
            stoppedEvent["allThreadsStopped"] = True
            self.sendEvent("stopped", stoppedEvent)
        else:
            exitedEvent = {}
            exitedEvent["exitCode"] = 0
            self.sendEvent("exited", exitedEvent)
            outputEvent = {}
            outputEvent["category"] = "console"
            outputEvent["output"] = str(self.manager.tape)
            self.sendEvent("output", outputEvent)
            terminatedEvent = {}
            self.sendEvent("terminated", terminatedEvent)
    
    def handleStepInRequest(self, jsonInput):
        self.manager.executeNextInstruction()
        self.manager.loadNextInstruction()
        responseBody = {}
        responseBody["allThreadsContinued"] = True
        self.sendResponse(jsonInput["seq"], True, "stepIn", None, responseBody)
        if self.manager.nextInstruction is not None:
            stoppedEvent = {}
            stoppedEvent["reason"] = "step"
            stoppedEvent["threadId"] = 1
            stoppedEvent["allThreadsStopped"] = True
            self.sendEvent("stopped", stoppedEvent)
        else:
            exitedEvent = {}
            exitedEvent["exitCode"] = 0
            self.sendEvent("exited", exitedEvent)
            outputEvent = {}
            outputEvent["category"] = "console"
            outputEvent["output"] = str(self.manager.tape)
            self.sendEvent("output", outputEvent)
            terminatedEvent = {}
            self.sendEvent("terminated", terminatedEvent)
    
    def handleStepOutRequest(self, jsonInput):
        self.manager.executeNextInstruction()
        self.manager.loadNextInstruction()
        responseBody = {}
        responseBody["allThreadsContinued"] = True
        self.sendResponse(jsonInput["seq"], True, "stepOut", None, responseBody)
        if self.manager.nextInstruction is not None:
            stoppedEvent = {}
            stoppedEvent["reason"] = "step"
            stoppedEvent["threadId"] = 1
            stoppedEvent["allThreadsStopped"] = True
            self.sendEvent("stopped", stoppedEvent)
        else:
            exitedEvent = {}
            exitedEvent["exitCode"] = 0
            self.sendEvent("exited", exitedEvent)
            outputEvent = {}
            outputEvent["category"] = "console"
            outputEvent["output"] = str(self.manager.tape)
            self.sendEvent("output", outputEvent)
            terminatedEvent = {}
            self.sendEvent("terminated", terminatedEvent)
        
    
    def handleContinueRequest(self, jsonInput):
        self.manager.executeNextInstruction()
        self.manager.loadNextInstruction()
        while self.manager.nextInstruction is not None and self.manager.nextInstruction.lineNumber not in self.breakpoints:
            self.manager.executeNextInstruction()
            self.manager.loadNextInstruction()
        responseBody = {}
        responseBody["allThreadsContinued"] = True
        self.sendResponse(jsonInput["seq"], True, "continue", None, responseBody)
        if self.manager.nextInstruction is not None:
            stoppedEvent = {}
            stoppedEvent["reason"] = "breakpoint"
            stoppedEvent["threadId"] = 1
            stoppedEvent["allThreadsStopped"] = True
            self.sendEvent("stopped", stoppedEvent)
        else:
            exitedEvent = {}
            exitedEvent["exitCode"] = 0
            self.sendEvent("exited", exitedEvent)
            outputEvent = {}
            outputEvent["category"] = "console"
            outputEvent["output"] = str(self.manager.tape)
            self.sendEvent("output", outputEvent)
            terminatedEvent = {}
            self.sendEvent("terminated", terminatedEvent)
    
    def handleDisconnectRequest(self, jsonInput):
        self.sendResponse(jsonInput["seq"], True, "terminate")

def main(initialState: State):
    VarphiDebugAdapter(initialState).loop()