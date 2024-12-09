from dataclasses import dataclass
import sys
from typing import Dict, Optional

import better_exceptions
from pathlib import Path
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import clear

from utils import (
    load_context,
    create_decision_dir,
    load_last_doc_path,
    save_last_doc_path,
)
import observe
import consult
import assemble

better_exceptions.hook()


@dataclass
class State:
    """Tracks the current state of the decision-making workflow"""

    decision_dir: Path
    context: Dict[str, str]
    stage: str
    doc_path: Optional[Path] = None


def display_welcome():
    """Display welcome message and random quote"""
    clear()
    print("Welcome to Consilio.")
    print("May you make wise decisions.")
    print("=========================================\n")
    # print(get_random_decision_quote())


def run_repl(state: State):
    """Run the interactive REPL"""
    # Define valid commands and their completions
    commands = {"o": "observe", "c": "consult"}

    # Create completer with both short and full forms
    command_completer = WordCompleter(
        ["observe", "consult", "o", "c"], ignore_case=True
    )
    session: PromptSession = PromptSession(completer=command_completer)

    while True:
        try:
            command = session.prompt(
                "\nEnter command O(bserve), C(onsult) or Ctrl+C to exit.\n> "
            ).lower()

            # Normalize command - convert single letter to full command
            if command in commands:
                command = commands[command]

            if command in ["o", "observe"]:
                result = observe.observe(state.doc_path, state.context)
                print(observe.xml_to_markdown(result))

            elif command in ["c", "consult"]:
                # Step 1: Run assembly to get perspectives
                assembly_result = assemble.assemble(state.doc_path, state.context)
                print("\nHere are the perspectives identified:")
                print(assemble.xml_to_markdown(assembly_result))

                # Step 2: Ask for user confirmation
                proceed = session.prompt(
                    "\nReady to proceed with consultation? (Y/n): "
                )
                if proceed.lower() not in ["y", "yes", ""]:
                    continue

                # Step 3: Run consultation with assembled perspectives
                assert state.doc_path is not None
                result = consult.consult(state.doc_path, assembly_result, state.context)
                print(result)  # This will show opinions from each perspective

            else:
                print("Invalid command. Please use 'O' or 'C' (or 'observe'/'consult')")

        except KeyboardInterrupt:
            print("\nExiting Consilio...")
            sys.exit(0)
        except Exception:
            import traceback

            print("\nError occurred:")
            traceback.print_exc()


def main(context_path: Optional[Path] = None, doc_path: Optional[Path] = None):
    """Main entry point for Consilio"""
    display_welcome()

    # Load context
    context = load_context(context_path)

    if doc_path is None or not isinstance(doc_path, Path):
        last_path = load_last_doc_path()
        prompt = (
            f"Enter path to decision document [{last_path}]: \n>"
            if last_path
            else "Enter path to decision document: "
        )
        input_path = input(prompt)
        doc_path = Path(input_path) if input_path else last_path
        if doc_path:
            save_last_doc_path(doc_path)

    # Create decision directory
    decision_dir = create_decision_dir(doc_path.stem)

    # Initialize state
    state = State(
        decision_dir=decision_dir,
        context={
            "domain": context.domain,
            "user_role": context.user_role,
            "perspective": context.perspective,
        },
        stage="observe",
        doc_path=doc_path,
    )

    # Start REPL
    run_repl(state)


if __name__ == "__main__":
    main()
