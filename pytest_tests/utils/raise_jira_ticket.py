from jira import JIRA
import os
import requests

from utils.common_utils import get_public_ip


def get_headnode_version_info():
    head_node_url = get_public_ip()
    api_url = f"http://{head_node_url}:5000/v1/xcompute/info"
    headers = {"Accept": "application/json"}
    response = requests.get(api_url, headers=headers)
    response_data = response.json()
    return response_data["Manifest"]["copVersion"]


def create_jira_issue_with_attachment(server_url, username, password, project_key, summary, description, issue_type, attachment_paths):
    jira_options = {'server': server_url}
    jira = JIRA(options=jira_options, basic_auth=(username, password))

    issue_dict = {
        'project': {'key': project_key},
        'summary': summary,
        'description': description,
        'issuetype': {'name': issue_type},
        "labels": ["automated-bug"],
    }
    issue = jira.create_issue(fields=issue_dict)

    for path in attachment_paths:
        if os.path.isfile(path):
            with open(path, 'rb') as file:
                jira.add_attachment(issue=issue, attachment=file)
        else:
            print(f"File not found: {path}")

    print(f"Issue {issue.key} created and attachments uploaded.")
    return issue


# if __name__ == "__main__":
#     SERVER_URL = "https://exostellar.atlassian.net/"
#     USERNAME = "v-guru@exostellar.io"
#     PASSWORD = "jkfdhsjkjfds"  # Use API token instead of password for security

#     PROJECT_KEY = "EXO" # id: 10004 # Exostellar Top Level
#     SUMMARY = "<<Automation - Example bug summary>>"
#     DESCRIPTION = "Detailed description of the bug."
#     ISSUE_TYPE = "Bug"

#     ATTACHMENT_PATHS = ["/home/ubuntu/automated_tests/xcompute_tests/pytest/test/report.html"]

#     create_jira_issue_with_attachment(SERVER_URL, USERNAME, PASSWORD, PROJECT_KEY, SUMMARY, DESCRIPTION, ISSUE_TYPE, ATTACHMENT_PATHS)