import sys
from pathlib import Path
from antlr4 import ParseTreeWalker, InputStream, CommonTokenStream
from varphi_parsing_tools import *
from varphi_parsing_tools import VarphiRepresentor
from varphi_types import State, Instruction, HeadDirection, TapeCharacter
from .CompilationMode import CompilationMode

def getVarphiSourceAsString(compilationMode: CompilationMode) -> str:
    if compilationMode == CompilationMode.CLI:
        with open(Path(__file__).resolve().parents[0] / "VarphiCLI.py") as varphiSource:
            return varphiSource.read()
    if compilationMode == CompilationMode.DEBUG_ADAPTER:
        with open(Path(__file__).resolve().parents[0] / "VarphiDebugAdapter.py") as varphiSource:
            return varphiSource.read()

def getStateDefinitions(representor: VarphiRepresentor, indentLevel: int) -> str:
    indent = '\t' * indentLevel
    for stateName in representor.stateNameToObject:
        stateEnum += f"{indent}{stateName} = State(\"{stateName}\")\n"
    return stateEnum

def statesToPython(representor: VarphiRepresentor, indentLevel: int, program: list[str]) -> str:
    indent = '\t' * indentLevel
    python = ""
    for stateName in representor.stateNameToObject:
        python += f"{indent}{stateName} = State(\"{stateName}\")\n"
    for stateObject in representor.stateNameToObject.values():
        python += stateOnTallyBlankToPython(stateObject, indentLevel, program)
    return python


def stateOnTallyBlankToPython(state: State, indentLevel: int, program: list[str]) -> str:
    python = getStateOnTallyPython(state, indentLevel, program)
    python += getStateOnBlankPython(state, indentLevel, program)
    return python

def getStateOnTallyPython(state: State, indentLevel: int, program: list[str]) -> str:
    indent = '\t' * indentLevel
    python = ""
    for i in range(len(state.onTally)):
        thenStateName = state.onTally[i].nextState.name
        thenCharacter = "TapeCharacter.TALLY" if state.onTally[i].characterToPlace == TapeCharacter.TALLY else "TapeCharacter.BLANK"
        thenDirection = "HeadDirection.RIGHT" if state.onTally[i].directionToMove == HeadDirection.RIGHT else "HeadDirection.LEFT"
        instructionLineNumber = state.onTally[i].lineNumber
        python += f"{indent}{state.name}.addOnTallyInstruction(Instruction({thenStateName}, {thenCharacter}, {thenDirection}, {instructionLineNumber}))\n"
    return python


def getStateOnBlankPython(state: State, indentLevel: int, program: list[str]) -> str:
    indent = '\t' * indentLevel
    python = ""
    for i in range(len(state.onBlank)):
        thenStateName = state.onBlank[i].nextState.name
        thenCharacter = "TapeCharacter.TALLY" if state.onBlank[i].characterToPlace == TapeCharacter.TALLY else "TapeCharacter.BLANK"
        thenDirection = "HeadDirection.RIGHT" if state.onBlank[i].directionToMove == HeadDirection.RIGHT else "HeadDirection.LEFT"
        instructionLineNumber = state.onBlank[i].lineNumber
        python += f"{indent}{state.name}.addOnBlankInstruction(Instruction({thenStateName}, {thenCharacter}, {thenDirection}, {instructionLineNumber}))\n"
    return python
    

def getMain(representor: VarphiRepresentor, program: list[str]) -> str:
    main = "\nif __name__ == \"__main__\":\n"
    main += statesToPython(representor, 1, program)
    main += f"\tinitialState = {representor.initialState.name}\n"
    main += "\tmain(initialState)"
    return main

def representorToPython(representor: VarphiRepresentor, compilationMode: CompilationMode, program: list[str]) -> str:
    python = getVarphiSourceAsString(compilationMode)
    python += getMain(representor, program)
    return python


def programToPython(programPath: str, compilationMode: CompilationMode) -> str:
    with open(programPath, 'r') as file:
        program = file.read()

    input_stream = InputStream(program)
    lexer = VarphiLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(VarphiSyntaxErrorListener(program))
    token_stream = CommonTokenStream(lexer)
    parser = VarphiParser(token_stream)
    parser.removeErrorListeners()
    parser.addErrorListener(VarphiSyntaxErrorListener(program))
    try:
        tree = parser.program()
    except Exception as e:
        sys.stderr.write(str(e))
        sys.exit(-1)
    representor = VarphiRepresentor()
    walker = ParseTreeWalker()
    walker.walk(representor, tree)
    
    return representorToPython(representor, compilationMode, program.splitlines())