import sys
import os
import tempfile
import argparse
from pathlib import Path
from PyInstaller.__main__ import run
import shutil
from .CompilationMode import CompilationMode
import traceback


from .vpToPy import programToPython


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("program",
                        type=Path,
                        help='Path to the program file')

    parser.add_argument("-o",
                        "--output",
                        type=Path,
                        help='Path to the output file.')
    
    parser.add_argument('-d', 
                        '--debug-adapter',
                        action='store_true', 
                        help="Enable debugging support for executable.")
    parser.add_argument('-i', 
                        '--interpret',
                        action='store_true', 
                        help="Interpret this program immediately and don't build it.")

    if sys.platform.startswith("win"):
        platform = "windows"
    elif sys.platform.startswith("linux"):
        platform = "linux"
    elif sys.platform.startswith("darwin"):
        platform = "mac"
    else:
        sys.stderr.write("Error: Unsupported OS.")
        return -1
    
    args = parser.parse_args()

    programPath = Path(args.program)
    if args.output:
        outputPath = Path(args.output)
        executableName = outputPath.name
    else:
        outputPath = programPath.parent.absolute() / f"{Path(programPath.stem).name}{'.exe' if platform == 'windows' else ''}"
        executableName = outputPath.name

    compilationMode = CompilationMode.CLI 
    if args.debug_adapter:
        compilationMode = CompilationMode.DEBUG_ADAPTER 
    
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as compiledPython:
        if args.interpret:
            from dataclasses import dataclass
            import json
            from collections import defaultdict
            from enum import Enum, auto
            import random
            execution_context = {
                "__builtins__": __builtins__,  # Allow built-in functions
                "dataclass": dataclass,
                "sys": sys,
                "json": json,
                "defaultdict": defaultdict,
                "Enum": Enum,
                "auto": auto,
                "random": random,
                "traceback": traceback,
                "__name__": "__main__",  # Simulate being run as __main__
            }

            exec(programToPython(programPath, compilationMode), execution_context)
            return 0
        compiledPython.write(programToPython(programPath, compilationMode))

    script_dir = os.path.dirname(os.path.abspath(__file__))

    with tempfile.TemporaryDirectory() as temp_output_dir:
        options = [
            str(compiledPython.name),
            '--onefile',
            fr'--name={str(executableName)}',
            fr'--distpath={str(temp_output_dir)}',
            fr'--workpath={str(Path(temp_output_dir) / 'build')}',
            '--noconfirm',
            fr'--specpath={str(temp_output_dir)}',
            fr'--optimize=2',
            '--log-level=ERROR'
        ]
        run(options)
        generated_exe = Path(temp_output_dir) / executableName
        if Path(outputPath).exists():
            try:
                Path(outputPath).unlink()
            except:
                print("Could not delete existing executable. Afttempting to overwrite it.")
        shutil.copy(generated_exe, outputPath)
        # Path(temp_output_dir).rmdir()
        return 0
    

if __name__ == '__main__':
    sys.exit(main())
