# Consilio: A Personal Decision Making Tool

> "Consilio" is a Latin term that embodies concepts such as counsel,
> deliberation, and wisdom. In ancient times, "consilium" referred to a group
> of advisors or a council that deliberated on important decisions, reflecting
> a process of careful consideration and planning. The term is associated with
> strategic thinking and prudent decision-making, emphasizing the use of good
> judgment, experience, and advice.

## Overview

Consilio helps you make better decisions but it does not make decisions for you. As Thomas Sowell said: “It is hard to imagine a more stupid or more dangerous way of making decisions than by putting those decisions in the hands of people who pay no price for being wrong.”

Consilio leverages LLM by asking independent questions and seek out opinions from multiple perspectives. Think of it as a vast
support network of advisors.  It asks you questions like "Have you thought about ...",  "What if ...", "Let's
stress test it this way ...".  The kind of questions you often pay your
advisors or boards for.

Consilio is intentionally minimal. It is designed to be used
in a command-line environment with a text editor (e.g., vim).

The core artefact Consilio works around is a single `DECISION.md` document. As
you go through the thinking process, you will revise this document by answering
the questions posed by Consilio.

All intermediate steps are preserved in structured format within a date-stamped
directory, creating a detailed record of the decision-making process. This
allows for both immediate reference and retrospective review of how important
decisions were made.

Think of Consilio as the "formal scientific method".  It can be "slow, tedious, lumbering, laborious but invincible".

## Installation

```bash
pipx install consilio
# or, if you prefer `uv`
uv install consilio
```

## Usage

```bash
# Create a new decision document
consilio path/to/your/DECISION.md
Welcome to Consilio. 

May you make wise decisions.

Decision document: Decisions/BankLoan.md
Domain: "a NZ-based B2C iOS app startup that are pre-product-market-fit"
Advisor Perspective: "an bootstrapped B2C founder, who successfully navigated pre-PMF phase with limited capital. , living outside of US but your main market is US."
User Role:"Solo Founder"

Get get started, please select one of the following actions: observe, consult.
CTRL+C to exit.

> observe
[Response in Markdown format]
{You noticed that you need to provide more context. You update the document in your editor. Now, let's try again.}
> observe
[...]
{You are happy with the quality of the questions and decide to proceed.}
> consult
[Response from the assembly step]
Are you ready to proceed to the consult step? (Y/n) Y
[Opinions from each perspectives]
{You noticed a gap in the information and decide to go back to the observe step.}
> consult
[...]

{When you gut feel tells you that you have enough information to make a decision. }

CTRL+C received.  Exiting.
```

### 3.0 Define Context

Create a new `.consilio.yml` file in the root directory with the following
structure:

```yaml
domain:"a NZ-based B2C iOS app startup that are pre-product-market-fit"
perspective:"an bootstrapped B2C founder, who successfully navigated pre-PMF phase with limited capital. , living outside of US but your main market is US."
user_role:"Solo Founder"
```

Consilio can load different context through the command line option.

```bash
consilio --context marketing.consilio.yml
```

Further, the yaml settings can be overridden by the user at the start of the session.

## Contributing

Contributions are welcome! Here's how you can help:

### Development Setup

1. Fork the repository
2. Clone your fork:

   ```bash
   git clone https://github.com/your-username/consilio.git
   cd consilio
   ```

3. Install development dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

### Development Workflow

1. Create a new branch:

   ```bash
   git checkout -b feature-name
   ```

2. Make your changes
3. Run the linter:

   ```bash
   make lint
   ```

4. Run the test suite with coverage:

   ```bash
   # Run tests with coverage report
   pytest --cov=consilio --cov-report=term-missing

   # Generate HTML coverage report
   pytest --cov=consilio --cov-report=html
   ```

   The HTML report will be generated in the `htmlcov` directory. Open `htmlcov/index.html` in your browser to view detailed coverage information.

5. Commit your changes:

   ```bash
   git commit -m "feat: Add new feature"
   ```

6. Push to your fork:

   ```bash
   git push origin feature-name
   ```

7. Open a Pull Request

### Code Style

Please refer to the [Python.md](Python.md) document for the coding style guide.
