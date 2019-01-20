''' Find all the bugs which have a bugzilla keyword in it '''
import requests
import json
from jira import JIRA
import re
import csv


# Read the file which has all the JIRA bugs encountered
jira_issues = []
with open('final/final_bug_list.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        jira_issues.append(row)

jira_bugs_bugzilla_comments = []

# Make JIRA connection and search keyword "bugzilla" in the comments of these JIRA bugs
jira = JIRA(basic_auth=('', ''), options={'server':''})
for issue_str in jira_issues:
    issue = jira.issue(issue_str[0])
    issue_json_string = json.dumps(issue.raw)
    issue_json = json.loads(issue_json_string)
    comments_str = str(issue_json["fields"]["comment"])
    # if len(re.findall("bugzilla", comments_str)) > 0:
    #     jira_bugs_bugzilla_comments.append(issue_str)
    if len(re.findall("product", comments_str)) > 0:
        jira_bugs_bugzilla_comments.append(issue_str)

# Write to a file
wtr = csv.writer(open ('final/product_mentioned_jira_bugs.csv', 'w'))
for issue in jira_bugs_bugzilla_comments:
    wtr.writerow(issue)





