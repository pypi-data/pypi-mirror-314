import os
import random
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Callable, Dict, Optional
import json

import yaml
from dataclasses import dataclass
from jinja2 import Template
import anthropic


# XML Utils
def escape_xml_string(xml_string):
    # Common XML escapes
    replacements = {
        "&": "&amp;",
    }

    # Replace special characters with their escaped versions
    for char, escape in replacements.items():
        xml_string = xml_string.replace(char, escape)

    return xml_string.strip()


# Claude Integration
@dataclass
class ClaudeResponse:
    content: str
    raw: Dict  # Store raw API response


def query_claude(
    user_prompt: str,
    system_prompt: Optional[str] = None,
    assistant: Optional[str] = None,
    temperature: float = 0.8,
) -> ClaudeResponse:
    """Send query to Claude and get response"""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8192,
        temperature=temperature,
        system=system_prompt if system_prompt else "",
        messages=[
            {
                "role": "user",
                "content": user_prompt,
            },
            {
                "role": "assistant",
                "content": [{"type": "text", "text": assistant}] if assistant else [],
            },
        ],
    )
    content = "".join(block.text for block in message.content if block.type == "text")
    return ClaudeResponse(content=content, raw=message.model_dump())


# Config Management
@dataclass
class Context:
    domain: str
    perspective: str
    user_role: str


def load_context(config_path: Optional[Path] = None) -> Context:
    """Load context from yaml file or prompt user for input if file doesn't exist"""
    if not config_path:
        config_path = Path(".consilio.yml")

    # If config file exists, load it
    if config_path.exists():
        with open(config_path) as f:
            data = yaml.safe_load(f)
    else:
        # Prompt user for context information
        print("\nNo context file found. Please provide the following information:")
        domain = input(
            "\nWhat is your domain? (e.g., 'NZ-based B2C iOS app startup that is pre product-market-fit')\n> "
        )
        user_role = input(
            "\nWhat is your role? (e.g., 'Solo Founder', 'CEO', 'Product Manager, Marketer in a Startup')\n> "
        )
        perspective = input(
            "\nWhat type of advisor perspective would be most valuable? (e.g., 'bootstrapped founder, who successfully navigated pre-PMF phase with limited capital with a successful exit')\n> "
        )

        # Create data dictionary
        data = {"domain": domain, "user_role": user_role, "perspective": perspective}

        # Ask if user wants to save this context
        save = input(
            "\nWould you like to save this context for future use? (y/N): "
        ).lower()
        if save in ["y", "yes"]:
            with open(config_path, "w") as f:
                yaml.dump(data, f)
            print(f"\nContext saved to {config_path}")

    return Context(**data)


# Prompt Management
@dataclass
class PromptTemplate:
    system: str
    user: str


def load_prompt_template(stage: str) -> PromptTemplate:
    """Load system and user prompts for a given stage"""
    base_path = Path("Prompts")
    system = (base_path / "SystemPrompt.md").read_text()
    user = (base_path / f"UserPrompt-{stage}.md").read_text()
    return PromptTemplate(system=system, user=user)


def render_prompt(template_str: str, context: Dict[str, str]) -> str:
    """Use Jinja2 template to replace placeholders with context values"""
    template = Template(template_str)
    return template.render(context)


# Quotes


def get_random_decision_quote():
    quotes = [
        (
            "Every decision you make reflects your evaluation of who you are.",
            "Marianne Williamson",
        ),
        ("Decision making is easy when your values are clear.", "Roy Disney"),
        (
            "Life is about choices. Some we regret, some we're proud of. Some will haunt us forever. The message: we are what we chose to be.",
            "Graham Brown",
        ),
        (
            "Some of our important choices have a time line. If we delay a decision, the opportunity is gone forever. Sometimes our doubts keep us from making a choice that involves change. Thus an opportunity may be missed.",
            "James E. Faust",
        ),
        (
            "We may think that our decisions are guided purely by logic and rationality, but our emotions always play a role in our good decision making process.",
            "Salma Stockdale",
        ),
        (
            "The quality of your life is built on the quality of your decisions.",
            "Wesam Fawzi",
        ),
        ("Decision is a risk rooted in the courage of being free.", "Paul Tillich"),
        ("Decision making is the specific executive task.", "Peter Drucker"),
        ("May your choices reflect your hopes, not your fears.", "Nelson Mandela"),
        (
            "All of us start from zero. We take the right decision and become a hero.",
            "Govinda",
        ),
        ("You cannot make progress without making decisions.", "Jim Rohn"),
        ("There's no wrong time to make the right decision.", "Dalton McGuinty"),
        (
            "Every decision brings with it some good, some bad, some lessons, and some luck. The only thing that's for sure is that indecision steals many years from many people who wind up wishing they'd just had the courage to leap.",
            "Doe Zantamata",
        ),
        (
            "Decision making is power. Most people don't have the guts to make 'tough decision' because they want to make the 'right decision' and so they make 'no decision'. Remember, live is short, so do things that matter the most and have the courage to make 'tough decision' and to chase your dreams.",
            "Yama Mubtakeraker",
        ),
        ("A good decision is based on knowledge and not on numbers.", "Plato"),
        (
            "There are times when delaying a decision has benefit. Often, allowing a set period of time to mull something over so your brain can work it through generates a thoughtful and effective decision.",
            "Nancy Morris",
        ),
        ("A decision clouded with doubt is never a good decision.", "Steven Aitchison"),
        ("The art of decision making includes the art of questioning.", "Pearl Zhu"),
        (
            "When faced with a decision, choose the path that feeds your soul.",
            "Dorothy Mendoza Row",
        ),
        (
            "Be open about your thoughts, ideas, and desires and you will be right with your decisions.",
            "Auliq Ice",
        ),
        (
            "Never make a decision when you are upset, sad, jealous or in love.",
            "Mario Teguh",
        ),
        (
            "Think 100 times before you take a decision, but once that decision is taken, stand by it as one man.",
            "Muhammad Ali Jinnah",
        ),
        (
            "Whenever you're making an important decision, first ask if it gets you closer to your goals or farther away. If the answer is closer, pull the trigger. If it's farther away, make a different choice. Conscious choice making is a critical step in making your dreams a reality.",
            "Jillian Michaels",
        ),
        (
            "Always make decisions that prioritize your inner peace.",
            "Izey Victoria Odiase",
        ),
        (
            "The goal shouldn't be to make the perfect decision every time but to make less bad decisions than everyone else.",
            "Spencer Fraseur",
        ),
        (
            "Don't let adverse facts stand in the way of a good decision.",
            "Colin Powell",
        ),
        (
            "Great decision-making comes from the ability to create the time and space to think rationally and intelligently about the issue at hand.",
            "Graham Allcot",
        ),
        (
            "Poor decision making I think, is the number one cause for most of our mistakes. So to make fewer mistakes means to make better decisions, and to make better decisions you must train yourself to think more clearly.",
            "Rashard Royster",
        ),
        (
            "Make decisions with the long term in mind. If you were truly the owner of your company and the success or failure of your business hinged on the performance of your team, you would dedicate yourself to constant improvement.",
            "David Miller",
        ),
        (
            "Whenever you see a successful business, someone once made a courageous decision.",
            "Peter F Drucker",
        ),
        (
            "Great leaders don't lead others with bitterness or resentfulness of past mistakes, they lead with hope and knowledge of the past to inform greater decision making in the future.",
            "Spencer Fraseur",
        ),
    ]

    quote, author = random.choice(quotes)
    return f'"{quote}" - {author}'


def save_interaction(action: str):
    """Decorator to save interaction details to file

    Args:
        action: The type of interaction (observe, assemble, consult)
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(doc: Path, *args, **kwargs):
            # Get perspective from kwargs if it exists (for consult)
            perspective = (
                kwargs.get("perspective_title")
                if "perspective_title" in kwargs
                else None
            )

            # Call the original function
            response = func(doc, *args, **kwargs)

            # Generate filename and ensure directory exists
            filename = generate_interaction_filename(action, perspective)
            interaction_path = doc.parent / doc.stem / filename
            interaction_path.parent.mkdir(parents=True, exist_ok=True)

            # Format the interaction content
            interaction_content = f"""# {action.title()} Request
"""
            # Add perspective title for consult
            if perspective:
                interaction_content += f"\n## Perspective: {perspective}\n"

            # Add prompts if they exist in kwargs
            if "system_prompt" in kwargs:
                interaction_content += (
                    f"\n## System Prompt\n{kwargs['system_prompt']}\n"
                )
            if "user_prompt" in kwargs:
                interaction_content += f"\n## User Prompt\n{kwargs['user_prompt']}\n"
            if "assistant" in kwargs:
                interaction_content += f"\n## Assistant Prefix\n{kwargs['assistant']}\n"

            # Add response
            interaction_content += f"\n# Response\n{response.content if hasattr(response, 'content') else response}\n"

            # Save to file
            interaction_path.write_text(interaction_content)

            return response

        return wrapper

    return decorator


def generate_interaction_filename(action: str, perspective: str = None) -> str:
    """Generate timestamped filename for saving interactions

    Args:
        action: The action performed (observe, assemble, consult)
        perspective: Optional perspective title for consult actions
    """
    # Use underscore within timestamp, but hyphen between timestamp and action
    timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
    if perspective:
        # Replace spaces and special chars with underscores for perspective
        perspective_slug = perspective.replace(" ", "_").replace("-", "_")
        return f"{timestamp}-consult_{perspective_slug}.md"
    else:
        return f"{timestamp}-{action}.md"


def save_last_doc_path(path: Path) -> None:
    """Save the last used document path"""
    config = Path(".consilio_history.json")
    data = {"last_doc_path": str(path)}
    with open(config, "w") as f:
        json.dump(data, f)

def load_last_doc_path() -> Optional[Path]:
    """Load the last used document path"""
    config = Path(".consilio_history.json")
    if config.exists():
        with open(config) as f:
            data = json.load(f)
            return Path(data.get("last_doc_path"))
    return None

def create_decision_dir(decision_name: str) -> Path:
    """Create a directory for storing decision-related files

    Args:
        decision_name: Name of the decision (usually from the markdown filename)

    Returns:
        Path to the created directory
    """
    # Create base decisions directory if it doesn't exist
    decisions_dir = Path("Decisions")
    decisions_dir.mkdir(exist_ok=True)

    # Create specific decision directory
    decision_dir = decisions_dir / decision_name
    decision_dir.mkdir(exist_ok=True)

    return decision_dir


# Example usage:
# print(get_random_decision_quote())
