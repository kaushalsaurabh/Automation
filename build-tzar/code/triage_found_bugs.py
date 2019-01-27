'''This script will write the found bugs in a format which is uploadable to qmon'''
import psycopg2
import csv
import re
import json

hostname = ''
username = ''
password = ''
database = ''
conn = None
from jira import JIRA

# Make connection with jira
jira = JIRA(basic_auth=('', ''), options={'server':''})

def read_from_file (filepath):
    all_rows = []
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print("row=", row)
            all_rows.append(row)
    return all_rows

def convert_string_to_list(given_string):
    given_string = given_string.replace('[', '')
    given_string = given_string.replace(']', '')
    list_to_be_returned = given_string.split(",")
    return list_to_be_returned

def write_to_csv(file_path_name, rows):
    print('file_path_name=', file_path_name)
    wtr = csv.writer(open(file_path_name, 'w'))
    for current_row in rows:
        wtr.writerow(current_row)


def get_corresponding_bugs(bugs):
    final_bugs = []
    for current_bug in bugs:
        current_bug = current_bug.replace("'", '').strip()

        # If it is a bugzilla bug add it to list and continue
        if re.findall('\d\d\d\d\d\d\d', current_bug):
            final_bugs.append(current_bug)
            continue

        # If it is empty add it to list and continue
        if len(current_bug) == 0:
            final_bugs.append('')
            continue

        # If it is a jira issue verify that it is open and add it
        issue = jira.issue(current_bug)
        issue_json_string = json.dumps(issue.raw)
        issue_json = json.loads(issue_json_string)
        current_state = issue_json["fields"]["status"]["name"]
        if current_state.upper() != 'RESOLVED' or current_state.upper() != 'CLOSED':
            final_bugs.append(current_bug)

    return final_bugs
def get_bugs_from_changelist(input_filepath, output_filepath, qmon):
    # Read the file
    all_rows = read_from_file(input_filepath +qmon+'_product_bugs.csv')

    header_row = ['Changelist', 'SegmentId', 'Test Failure', 'Failure Type', 'Team Name', 'Jira / Bugzilla', 'Log URL']
    final_rows = []
    final_rows.append(header_row)
    for current_row in all_rows:

        # Get the column containing all jira/bugzilla bugs
        bugs_list = convert_string_to_list(current_row[5])
        print('bugs_list=', bugs_list)

        # Parse the bug list and get only open bugs
        final_bugs = get_corresponding_bugs(bugs_list)

        # Get all the failed tests
        test_failures = convert_string_to_list(current_row[4])

        # Get all the types of failures
        test_failures_types = convert_string_to_list(current_row[6])

        # Get logs for all the failures
        test_failures_logs = convert_string_to_list(current_row[7])

        # Get teams for all the failures
        test_failures_teams = convert_string_to_list(current_row[8])



        for i in range(len(final_bugs)):
            # Add to the rows to be written
            row_to_be_appened = [current_row[0], current_row[3], test_failures[i], test_failures_types[i], test_failures_teams[i], final_bugs[i], test_failures_logs[i]]
            final_rows.append(row_to_be_appened)

        # Write to csv
        write_to_csv(output_filepath +qmon+'_final_bugs_'+qmon+'.csv', final_rows)




