'''This holds all the utility functions'''

import psycopg2
from P4 import P4, P4Exception
import csv
import re
import json
import subprocess
from multiprocessing import Process

hostname = ''
username = ''
password = ''
database = ''
conn = None
conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
cur = conn.cursor()

p4 = P4()  # Create the P4 instance
p4.port = ""
p4.user = ""
p4.client = ""            # Set some environment variables
perfore_path = ""   # Location of directory up till Perforce
p4.connect()

# This function will get the branch_id for a given branch
def get_branch_id_from_name(branch_name):

    # Get branch id from branch namehostname
    branch_id_query = "select branch_id from segment_branch_view where branch_name='"+branch_name+"' limit 1"
    print("query_branch_id=", branch_id_query)
    cur.execute(branch_id_query)
    branch_id = [x[0] for x in cur.fetchall()][0]
    print("branch_id=", branch_id)
    return branch_id

# This function will get all the tests given branch, result, no. of days
def get_tests_from_database(branch_name, result_state, no_of_days):

    # Get Branch Id for given branch name
    branch_id = get_branch_id_from_name(branch_name)

    # Get the list of tests which need to be disabled from the database
    tests_query ="select distinct name from \"result\", segment, pipeline where state = '"+result_state+"' and date > ('now'::date - '"+str(no_of_days)+" day'::interval) and " \
                                                         "\"result\".segment_id = \"segment\".id and segment.pipeline_id = \"pipeline\".id and \"pipeline\".branch_id = "+str(branch_id)
    print("tests_query=", tests_query)
    cur.execute(tests_query)
    tests = []
    for tests_db in cur.fetchall():
        tests.append(tests_db[0])
    print("Total  tests:", len(tests))
    print(tests)

    return tests

# This function will get all the logs for a given test case having given state
def get_logs_for_test(test_name, branch_name, days, state):

    branch_id = get_branch_id_from_name(branch_name)

    # Get the logs for given test
    logs_query = "select log from \"result\", segment, pipeline where state = '"+state+"' and date > ('now'::date - '"+str(days)+" day'::interval) and " \
                        "\"result\".segment_id = \"segment\".id and segment.pipeline_id = \"pipeline\".id and \"pipeline\".branch_id = "+str(branch_id)+" and name = '"+test_name+"'"
    print("logs_query=", logs_query)
    cur.execute(logs_query)
    logs = []
    for logs_db in cur.fetchall():
        logs.append(logs_db[0])
    print("Total logs:", len(logs))
    print(logs)

#This function will get file from a perforce location
def get_file_from_perforce(location):
    try:

        file = p4.run('print', location)
        print("file=", file)
        first_element = file[48]
        print("first_element=", first_element)

        return file[1]
    except Exception as e:
        print(e)  # Display errors

# This function will write the array rows to a text file
def write_to_csv(file_path_name,rows, header_row = ""):
    print('file_path_name=', file_path_name)
    wtr = csv.writer(open(file_path_name, 'w'))
    wtr.writerow(header_row)
    for current_row in rows:
        wtr.writerow(current_row)

# This function will convert 1-D array to 2-D array
def convert_array_to_2_dimension (array):
    array_to_be_returned = []
    for row in array:
        array_to_be_returned.append([row])
    return array_to_be_returned

# This function will return stable tests = Passed tests - fragile tests - malicious tests
def get_stable_tests(branch_name, no_of_days):
    # Invalid Tests
    not_valid_tests = ["JS Unit tests for "+branch_name, "Local build of H5 Client for " + branch_name, "Sandbox build of H5 Client for " + branch_name,"OSSTP", "CloudVM_Firstboot"]

    # Stable Tests = Passed tests - Fragile Tests - Malicious Tests
    malicious_tests = get_tests_from_database(branch_name, "malicious", no_of_days)
    fragile_tests = get_tests_from_database(branch_name, "fragile", no_of_days)
    passed_tests = get_tests_from_database(branch_name, "passed", no_of_days)
    final_tests = set()
    final_tests = set(passed_tests) - set(fragile_tests) - set(malicious_tests)

    # Remove invalid tests
    for invalid_test in not_valid_tests:
        final_tests.remove(invalid_test)

    print("final_tests count=", len(final_tests))
    print("final_tests=", final_tests)
    return final_tests

# This function will return all fragile + failed tests
def get_unstable_tests(branch_name, no_of_days):
    fragile_tests = get_tests_from_database(branch_name, "fragile", no_of_days)
    malicious_tests = get_tests_from_database(branch_name, "malicious", no_of_days)
    unstable_tests = set(fragile_tests) | set(malicious_tests)
    print("Final Unstable test count=", len(unstable_tests))
    print("Unstable tests=", unstable_tests)
    return unstable_tests

# This function will get opened files with changelist
def get_opened_files():
    opened_files = p4.run("opened")
    dict_to_be_returned = {}
    for current_file in opened_files:
        dict_to_be_returned[current_file["depotFile"]] = current_file["change"]
    print("dict_to_be_returned=", dict_to_be_returned)
    return dict_to_be_returned

# This function will create a changelist for the given file
def create_changelist(filepath, change_description):
    print("Runlist location=", filepath)

    # If the file is already checked out return the changelist
    opened_files = get_opened_files()
    print("filepath=", filepath)
    print("opened_files=", opened_files.keys())
    if filepath in opened_files.keys():
        print("Inside opened_files")
        return opened_files[filepath]

    change = p4.fetch_change()

    # Edit the files in p4 before adding to changelist
    return_edit = p4.run("edit", filepath)
    print("return_edit=", return_edit)

    # Add the file and description to changelist
    change[ "Description" ] = change_description
    print("filepaths=", filepath)
    change["Files"] = filepath

    # Parse changelist from the result
    result = p4.save_change(change)
    r = re.compile("Change ([1-9][0-9]*) created.")
    print("result=", result)
    m = r.match(result[1])
    changeId = "0"
    if m: changeId = m.group(1)
    print("change=", changeId)
    return changeId

# This function will write text to atext file
def write_to_text(file_path_name, text):
    print('file_path_name=', file_path_name)
    wtr = csv.writer(open(file_path_name, 'w'))
    wtr.writerow(text)

# This function will revert a file
def revert(filepath):
    p4.run("revert", filepath)

# Read Json file
def read_json_file(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data

# Write json file
def write_json_file(file_path, json_data):
    with open(file_path, 'w') as outfile:
        json.dump(json_data, outfile, indent=4)

# Change status of tests
def change_status (json_data, tests, pipeline_enabled_status):
    final_data = []
    for current_data in json_data:
        test_name_json = current_data["testClass"]
        if test_name_json in tests:
            current_data["pipelineEnabled"] = pipeline_enabled_status
            current_data["reasonForDisable"] = "Disabling fragile tests"
            final_data.append(current_data)
        else:
            final_data.append(current_data)
    return final_data

# Get the tests with given status from run-list.json
def get_tests (file_path, pipeline_enabled_status):
    final_data = []
    if file_path != "":
        json_data = read_json_file(file_path)
    for current_data in json_data:
        if current_data["pipelineEnabled"] == pipeline_enabled_status:
            final_data.append(current_data)
    return final_data

# Create h5 automation build
def create_sandbox_build(product, changeset, branch):
    cmd = "/build/apps/bin/gobuild sandbox queue "+ product +" --branch="+branch+" --changeset="+str(changeset)+"  --user=  --accept-defaults"
    print("Sandbox command=",cmd)
    subprocess.call(cmd, shell=True)

# This function will get the changelist location from perforce
def get_runlist_location(branch_name):
    runlist_location = "//depot/vsphere-client-modules/{}/h5-plugin-tests/ui-automation/runner-uia/run-list.json"
    return runlist_location.format(branch_name)

def create_h5_sandbox_for_stable_tests(branch_name, no_of_days):
    runlist_path = get_runlist_location(branch_name)

    # Create changeset to disable unstable test
    changeset = create_changelist(runlist_path, "Changelist to disable unstable tests")

    # Read runlist.json file
    json_data = read_json_file(perfore_path + p4.client + runlist_path)

    # Change pipeline status of unstable tests to false
    updated_data = change_status(json_data, get_unstable_tests(branch_name, no_of_days), "false")

    # Write json file
    write_json_file(perfore_path + p4.client + get_runlist_location(branch_name), updated_data)

    #Count of disabled and enabled tests
    disabled_tests = get_tests(perfore_path + p4.client + runlist_path, "false")
    enabled_tests = get_tests(perfore_path + p4.client + runlist_path, "true")
    print("Total Tests=", str(len(disabled_tests) + len(enabled_tests)))
    print("Disabled Tests=", str(len(disabled_tests)))
    print("Enabled Tests=", str(len(enabled_tests)))

    #Create sandbox build for h5Automation
    create_sandbox_build("h5automation", changeset, branch_name)

create_h5_sandbox_for_stable_tests("h5c-main", 20)
conn.close()