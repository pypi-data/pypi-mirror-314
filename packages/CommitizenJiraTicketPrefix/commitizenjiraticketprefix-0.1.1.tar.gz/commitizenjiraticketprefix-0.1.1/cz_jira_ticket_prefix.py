import re
import subprocess

from commitizen.cz.base import BaseCommitizen

MAX_LENGTH = 75

# Prefix = "ACB-1234 refactor: " 
TICKET_AND_TYPE_PREFIX_LENGTH = 8 + 1 + 10
ALLOWED_MESSAGE_LENGTH = MAX_LENGTH - TICKET_AND_TYPE_PREFIX_LENGTH


class CommitizenJiraTicketPrefix(BaseCommitizen):
    def questions(self):
        """Define the questions to ask the user."""
        return [
            {
                "type": "list",
                "name": "type",
                "message": "Select the type of change you are committing:",
                "choices": [
                    {"value": "feat", "name": "feat: A new feature"},
                    {"value": "fix", "name": "fix: A bug fix"},
                    {
                        "value": "refactor",
                        "name": "refactor: Code refactoring without changing functionality",
                    },
                    {"value": "docs", "name": "docs: Documentation changes"},
                    {
                        "value": "style",
                        "name": "style: Code style changes (formatting, missing semi-colons, etc)",
                    },
                    {"value": "perf", "name": "perf: Performance improvements"},
                    {"value": "test", "name": "test: Adding or fixing tests"},
                    {
                        "value": "chore",
                        "name": "chore: Other changes that don't modify src or test files",
                    },
                ],
            },
            {
                "type": "input",
                "name": "subject",
                "message": f"Write a short, imperative tense description of the change ({ALLOWED_MESSAGE_LENGTH} chars left):\n",
                "validate": lambda text: True
                if len(text) <= ALLOWED_MESSAGE_LENGTH
                else f"Too long by {len(text) - ALLOWED_MESSAGE_LENGTH} characters!",
            },
        ]

    def message(self, answers):
        """Generate the commit message."""
        try:
            branch_name = (
                subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"])
                .strip()
                .decode()
            )
        except subprocess.CalledProcessError:
            branch_name = ""

        match = re.match(r"([A-Z]+-\d+)", branch_name)
        if match:
            ticket_id = match.group(1)
            prefix = f"{ticket_id} "
        else:
            prefix = ""

        type_ = answers["type"]
        subject = answers["subject"].strip()

        commit_message = f"{prefix}{type_}: {subject}"
        return commit_message

    def example(self):
        """Provide an example commit message."""
        return "ABC-123 feat: add new user authentication feature"

    def schema(self):
        """Provide the commit message schema."""
        return "<TICKET-ID> <type>: <subject>"

    def info(self):
        """Provide additional info about the commit message style."""
        return (
            "The commit message should start with the ticket ID extracted from the branch name, "
            "followed by the commit type and a short description.\n"
            "Subject line is recommended to be <= 50 chars.\n"
            "Example: ABC-123 feat: add new user authentication feature"
        )
