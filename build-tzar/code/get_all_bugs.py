'''This script will get all bugs which are raised for a given test case'''

import psycopg2
import csv
import re
import get_untriaged_bugs

hostname = ''
username = ''
password = ''
database = ''
conn = None

# jira_areas = {'VM-Migrators': 'VSUN-\d*','DevOps': 'VPAR-\d*', 'Networking': 'VUN-\d*', 'vIDM': 'VSUIP-\d*' ,'DRM': 'VUD-\d*', 'Storage': 'VUS-\d*', 'Cluster': 'VUD-\d*','CLI': '',
#                'VCHA': 'VUVCHA-\d*','WCP': '', 'licensing': 'VUL-\d*','Content-Library': 'VUCL-\d*','Autodeploy': 'VUA-\d*','VM-Creators': ,'Networking': , 'vSAN':,
#                 'VUM': ,'Platform': ,'Admin UI': ,'Search': ,'Multi-AZ': ,'Plugin-SDK': , 'Global-Views': }

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


try:
    # Connect to postgre sql server
    def get_product_bug_for_testcase (testcase, conn):

            # If it is provider failure ignore
            if len(re.findall("Provider", testcase)) > 0 or testcase is None or len(testcase) == 0 :
                return ["", ""]

            # Get segment id for the given q-mon column
            cur = conn.cursor()
            bug_number_query = "select issue.bug_number, issue_type from issue, \"result\" where " \
                               "issue.bug_number is not null and \"result\".\"name\"="+testcase+" and \"result\".issue_id = issue.id and " \
                                                                                                 "date > ('now'::date - '20 day'::interval) order by date desc limit 1"
            print("bug_number_query="+bug_number_query)
            cur.execute(bug_number_query)

            # Print results
            bug_number = ""
            issue_type = ""
            for bug_numbers, issue_types in cur.fetchall():
                bug_number = bug_numbers
                issue_type = issue_types
            print("bug_number=", bug_number)
            print("issue_type=", issue_type)
            return [bug_number, issue_type]



    def get_product_bug_for_column (filepath, current_segment, conn):

        final_rows = []

        # Read the csv file
        all_rows = read_from_file(filepath +'untriaged_bugs_'+current_segment+'.csv')

        # Iterate through rows and get the bug number for failed tests
        for current_row in all_rows:
            print("********Changelist**********", current_row[0])

            # Read String and convert to list
            test_cases = current_row[4]
            print("test_cases=", test_cases)
            product_bugs = []
            issue_types = []
            test_cases_list = convert_string_to_list(test_cases)

            # Iterate through list to find product bugs
            for current_testcase in test_cases_list:
                # Convert string to list
                print("current_testcase=", current_testcase)
                returned_values = get_product_bug_for_testcase(current_testcase, conn)

                product_bugs.append(returned_values[0])
                issue_types.append(returned_values[1])

            print("product_bugs=", product_bugs)

            # Append to the final list to be added
            current_final_row = [current_row[0], current_row[1], current_row[2], current_row[3], current_row[4], product_bugs, issue_types, current_row[5], current_row[6]]
            final_rows.append(current_final_row)

        get_untriaged_bugs.write_to_csv(filepath+current_segment+'_product_bugs.csv', final_rows)

except (Exception, psycopg2.DatabaseError) as error:
    print(error)