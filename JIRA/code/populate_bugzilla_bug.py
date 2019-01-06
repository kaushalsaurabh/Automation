''' This script will read the file which has JIRA Bugs which had bugzilla keyword.
Then it will extract the bugzilla bug and populate it'''

import json
from jira import JIRA
import re
import csv

jira = JIRA(basic_auth=('', ''), options={'server':'https://jira.eng.vmware.com'})

# Read the file which has bugzilla bugs mentioned
jira_issues = []
with open('final/bugzilla_mentioned_jira_bugs.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        jira_issues.append(row)

jira_bugs_bugzilla_comments = []

# Search the comments for bugzilla link and populate it
for issue_str in jira_issues:
    issue = jira.issue(issue_str[0])
    issue_json_string = json.dumps(issue.raw)
    issue_json = json.loads(issue_json_string)
    comments_str = str(issue_json["fields"]["comment"])
    regular_expression = "https://bugzilla.eng.vmware.com/show_bug.cgi\?id=\\d*"
    row_to_be_added = issue_str
    if len(re.findall(regular_expression, comments_str)) > 0:
        unique_set = set()
        unique_set = set(re.findall(regular_expression, comments_str))
        row_to_be_added += unique_set
    jira_bugs_bugzilla_comments.append(row_to_be_added)


# Write to a file
wtr = csv.writer(open ('final/jira_with_bugzilla_id_unique.csv', 'w'))
for issue in jira_bugs_bugzilla_comments:
    wtr.writerow(issue)