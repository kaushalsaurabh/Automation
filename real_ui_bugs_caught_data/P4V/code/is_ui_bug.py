'''This script will figure out whether the bug is real UI bug or not
1. If a bugzilla bug is found then for sure it is real UI bug. Get the component from bugzilla using API
2. If JIRA issue is found query JIRA to find whether it is bug or defect.
3. Get the component from it and populate it'''

import json
from jira import JIRA
import re
import csv

jira = JIRA(basic_auth=('', ''), options={'server':''})

# Read the file which has all the bugs
rows = []

jira_re = 'VSUIP-\d*|VUA-\d*|VUD-\d*|VUCL-\d*|VUGV-\d*|VUHP-\d*|VUL-\d*|VUN-\d*|VUSP-\d*|VUVC-\d*|VSUN-\d*|VUS-\d*|VUSS-\d*|' \
          'VUVCHA-\d*|VUCI-\d*|VUVG-\d*|VSUIR-\d*|MU-\d*|VPAR-\d*|VUAM-\d*|VMSPP-\d*|VUZZZ-\d*|VU-\d*|VDS-\d*|VUPSCM-\d*|VLMU-\d*'

jira_area = {'VSUIP-\d*': 'SDK & Plugins', 'VUA-\d*': 'AutoDeploy/ImageBuilder', 'VUD-\d*': 'Cluster UI', 'VUCL-\d*': 'Conent Library',
             'VUGV-\d*': 'Global Views', 'VUHP-\d*': 'Host Profile', 'VUL-\d*': 'Licensing', 'VUN-\d*': 'Networking',
             'VUSP-\d*': 'SDK & Plugins', 'VUVC-\d*': 'VM Configuration', 'VSUN-\d*': 'VM Operations & Provisioning',
             'VUS-\d*': 'Storage', 'VUSS-\d*': 'Smart Search', 'VUVCHA-\d*': 'VCHA', 'VUCI-\d*': 'CLI Integration',
             'VUVG-\d*': 'VMC Gateway', 'VSUIR-\d*': 'Rearchitecture', 'MU-\d*': 'Multi-Az', 'VPAR-\d*': 'Devops',
             'VUAM-\d*': 'Components', 'VMSPP-\d*': 'Managed Service Provider Platform', 'VU-\d*': 'vsphere Ui', 'VDS-\d*': 'Data Services',
             'VUPSCM-\d*': 'PSC - SSO, Cert mgmt', 'VLMU-\d*': 'vCenter Lifecycle Management UI'}
try:

    with open('../data/intermediate/h5c-dev/vim-clients-bug-list.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            rows.append(row)

    # Final rows to be added
    final_rows = []
    # Iterate every row
    for current_row in rows:
        final_row = []

        # Copy the first 3 columns as is
        final_row.append(current_row[0])
        final_row.append(current_row[1])
        final_row.append(current_row[2])

        is_bug = 'No'
        bug_caught_in_pipeline = 'No'
        area_of_bug = ''

        # If a bugzilla bug is found then it is a real bug for sure
        bugzilla_bug = current_row[2]
        bugzilla_bug.strip()
        if(re.findall('\d\d\d\d\d\d\d', bugzilla_bug)):
            is_bug = 'Yes'

        # Else look for the issue type in JIRA and update the column
        if len(current_row[1]) != 0:

            jira_issues_str = current_row[1]
            jira_issues_str = jira_issues_str.replace('{', '')
            jira_issues_str = jira_issues_str.replace('}', '')
            jira_issues = jira_issues_str.split(',')


            # Iterate on JIRA issues to get the issue type and label
            for jira_issue in jira_issues:
                jira_issue = jira_issue.replace("'", "").strip()
                print(jira_issue)
                issue = jira.issue(jira_issue)
                issue_json_string = json.dumps(issue.raw)
                issue_json = json.loads(issue_json_string)

                # If Issue type is Bug or defect append yes else no
                issue_type = issue_json["fields"]["issuetype"]["name"]
                print(issue_type.upper())
                if (issue_type.upper() == 'BUG' or issue_type.upper() == 'DEFECT'):
                    print('Inside Bug loop')
                    is_bug = 'Yes'

                    # Find whether labels have h5-pipeline
                    labels = str(issue_json["fields"]['labels'])
                    print(labels)
                    if (len(re.findall('h5-pipeline', labels, re.IGNORECASE)) > 0):
                        print('Inside Label loop')
                        bug_found_in_pipeline = 'Yes'
                        print('Appended yes')
                        bug_caught_in_pipeline = 'Yes'
                        break

            for k, v in jira_area.items():
                if len(re.findall(k, jira_issues[0])) > 0:
                    print(v)
                    area_of_bug = v
        final_row.append(is_bug)
        final_row.append(bug_caught_in_pipeline)
        final_row.append(area_of_bug)
        final_rows.append(final_row)

    # Write to a file
    wtr = csv.writer(open('../data/intermediate/h5c-dev/vim-clients-bug-list-final.csv', 'w'))
    for current_row in final_rows:
        wtr.writerow(current_row)
except Exception as e:
    print(e)         # Display errors



