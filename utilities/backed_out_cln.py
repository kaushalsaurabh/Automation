''' This script will find out the clns that have been backed out from 1/1/2019 to 3/28/2019'''
from P4 import P4, P4Exception    # Import the module
import re
import csv

p4 = P4()                        # Create the P4 instance
p4.port = ""
p4.user = ""
p4.client = ""            # Set some environment variables
p4.connect()

# Function which takes list of directory paths as input and returns unique set of perforce changelists
def get_changelists(directories_path):
    try:
        # For loop on the directory structure
        unique_changelist = set()
        for directory in directories_path:
            str_to_query = directory + '...@2019/1/1,@now'
            print('p4 changes query=', str_to_query)
            changelists = p4.run('changes', str_to_query)

            # For loop on all the changelists found in that directory
            for changelist in changelists:
                changes = changelist['change']
                unique_changelist.add(changes)
        print('unique set=', unique_changelist)
        return unique_changelist
    except Exception as e:
        print(e)  # Display errors

# Function to return unique values
def get_unique_values(elements):
    unique_values = set()
    for element in elements:
        unique_values.add(element)
    return unique_values

# Function get comments for a given changelist
def get_comments(changelist):
    changelist_data = p4.run('describe', changelist)
    comments = changelist_data[0]['desc']
    return comments

# Function to search for a keyword in text
def keyword_exists_in_text(keyword, text):
      if re.search(keyword, text, re.IGNORECASE):
        return 'true'
      return  'false'

# Function to parse the changelists and search for keyword
def get_clns_with_keyword (changelists, keyword):

    cln_to_be_returned = []

    # Parse through the clns
    for change in changelists:
        given_row = []
        print("Getting comments for cln=", change)
        comments = get_comments(change)
        if keyword_exists_in_text(keyword, comments) == 'true' and keyword_exists_in_text('CBOT', comments) == 'false':
            given_row.append(change)
            given_row.append(comments)
            str_to_be_added = change +","+comments

            # Backout occurred due to JS, Build or E2E failure
            print("Adding ", str_to_be_added)
            if keyword_exists_in_text('e2e', comments) == 'true':
                given_row.append('E2E Test failure')
                print("Adding e2e failure")
            elif keyword_exists_in_text('js', comments) == 'true':
                print("Adding JS failure")
                given_row.append('JS Test failure')
            elif keyword_exists_in_text ('build', comments) == 'true':
                print("Adding build failure")
                given_row.append('build failure')
            cln_to_be_returned.append(given_row)

    return cln_to_be_returned


# Function to get the directory list
def get_directory_list(branch):
    directory_list = []
    directory_list.append("//depot/vsphere-client-modules/"+branch+"/")
    directory_list.append("//depot/vim-clients/" + branch + "/")
    return directory_list

# Write all the changelists in a csv file
def write_file(rows, filepath):
    wtr = csv.writer(open(filepath, 'w'))
    for row in rows:
        wtr.writerow(row)

changelists = get_changelists(get_directory_list("h5c-main"))
backed_out_clns = get_clns_with_keyword(changelists, 'back(ing)?\s*out')
write_file(backed_out_clns, '../data/backed_out_clns/h5c-main.csv')