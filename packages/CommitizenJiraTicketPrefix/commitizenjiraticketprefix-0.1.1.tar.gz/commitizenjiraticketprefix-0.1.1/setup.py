from setuptools import setup

setup(
    name="CommitizenJiraTicketPrefix",
    version="0.1.1",
    py_modules=["cz_jira_ticket_prefix"],
    install_requires=["commitizen"],
    entry_points={
        "commitizen.plugin": [
            "cz_jira_ticket_prefix = cz_jira_ticket_prefix:CommitizenJiraTicketPrefix",
        ],
    },
)
