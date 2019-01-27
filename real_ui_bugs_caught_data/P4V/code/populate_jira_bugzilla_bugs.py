'''This script will
1. Read changelist from csv file
2. Go to comments section of that changelist
3. Match regular expression for JIRA comments
4. Look for bugzilla bug
5. Write it to a file'''

from P4 import P4, P4Exception    # Import the module
import re
import csv

p4 = P4()                        # Create the P4 instance
p4.port = ""
p4.user = ""
p4.client = ""            # Set some environment variables

jira_re = 'VSUIP-\d*|VUA-\d*|VUD-\d*|VUCL-\d*|VUGV-\d*|VUHP-\d*|VUL-\d*|VUN-\d*|VUSP-\d*|VUVC-\d*|VSUN-\d*|VUS-\d*|VUSS-\d*|' \
          'VUVCHA-\d*|VUCI-\d*|VUVG-\d*|VSUIR-\d*|MU-\d*|VPAR-\d*|VUAM-\d*|VMSPP-\d*|VUZZZ-\d*|VU-\d*|VDS-\d*|VUPSCM-\d*|VHVU-\d*' \
          '|VLMU-\d*'



try:                             # Catch exceptions with try/except

    p4.connect()

    changelists = []
    rows_to_be_added = []
    # Read from file and populate list
    with open('../data/intermediate/h5c-dev/vsphere-client-modules.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            changelists.append(row[0])

    # Get comments for a given changelist
    for changelist in changelists:
        print('changelist=', changelist)
        changelist_data = p4.run('describe', changelist)
        comments = changelist_data[0]['desc']

        # Get JIRA bug if any
        print(comments)
        jira_bugs_found = []
        jira_bugs_found = re.findall(jira_re, comments)
        jira_bugs_found_set = set()
        for jira_bug in jira_bugs_found:
            jira_bugs_found_set.add(jira_bug)
        print('Set=', jira_bugs_found_set)

        # Get Bugzilla bug if any
        bug_number_index = -1
        reviewed_by_index = -1
        pivotal_story_tracker_index = -1
        bugzilla_bug = ''
        if comments.find('Bug Number:') != -1:
            bug_number_index = comments.index('Bug Number:')
        if comments.find('Reviewed by') != -1:
            reviewed_by_index = comments.index('Reviewed by')
        if comments.find('Pivotal Tracker Story Number') != -1:
            pivotal_story_tracker_index = comments.index('Pivotal Tracker Story Number')
        print('bug_number_index=', bug_number_index)
        print('reviewed_by_index=', reviewed_by_index)
        print('pivotal_story_tracker=', pivotal_story_tracker_index)

        end_substring_index = reviewed_by_index
        if pivotal_story_tracker_index > bug_number_index and pivotal_story_tracker_index < end_substring_index:
            end_substring_index = pivotal_story_tracker_index
        print('end_substring_index=', end_substring_index)
        if bug_number_index > -1 and end_substring_index > -1:
            bugzilla_bug = comments[bug_number_index+11:end_substring_index - 1]
            bugzilla_bug.strip()
            print(bugzilla_bug)

        # Make it a row which can be written in csv
        given_row = []
        given_row.append(changelist)
        if len(jira_bugs_found_set) != 0:
            given_row.append(jira_bugs_found_set)
        else:
            given_row.append('')
        if len(bugzilla_bug) > 0 and bugzilla_bug != 'auto':
            given_row.append(bugzilla_bug)
        else:
            given_row.append('')
        rows_to_be_added.append(given_row)

    # Write to a file
    wtr = csv.writer(open('../data/intermediate/h5c-dev/vim-clients-bug-list.csv', 'w'))
    for current_row in rows_to_be_added:
        wtr.writerow(current_row)

    p4.disconnect()                # Disconnect from the server
except Exception as e:
    print(e)         # Display errors