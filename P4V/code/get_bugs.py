'''This scriot will get changelists that went into product code for a given period'''

from P4 import P4, P4Exception    # Import the module
import re
import csv

p4 = P4()                        # Create the P4 instance
p4.port = "perforce.eng.vmware.com:1666"
p4.user = "skaushal"
p4.client = "skaushal_skaushal-m01_9556"            # Set some environment variables


# Function which takes list of directory paths as input and returns unique set of perforce changelists
def get_changelists(directories_path):
    try:
        # For loop on the directory structure
        unique_changelist = set()
        for directory in directories_path:
            str_to_query = directory + '...@2017/1/1,@2018/12/26'
            print('p4 changes query=', str_to_query)
            changelists = p4.run('changes', str_to_query)

            # For loop on all the changelists found in that directory
            for changelist in changelists:
                changes = changelist['change']
                print(changes)
                unique_changelist.add(changes)
        print('unique set=', unique_changelist)
        return unique_changelist
    except Exception as e:
        print(e)  # Display errors


try:                             # Catch exceptions with try/except

    p4.connect()

    # Get the directories to be parsed According to branch
    directories_re = 'test'
    path = '//depot/vsphere-client-modules'+'/h5c-dev'
    directories_path = []
    sub_directories = p4.run("dirs", path+'/*')
    for directory in sub_directories:
        if(re.search(directories_re, str(directory))):
            directories_path.append(directory['dir'])


    # Get changelist from superset then subtract tests changelist from it
    unique_set = set()
    unique_changelist_tests = get_changelists(directories_path)
    unique_changelist_total = get_changelists([path])
    unique_set = unique_changelist_total - unique_changelist_tests
    print('unique_changelist_total=', len(unique_changelist_total))
    print('unique_changelist_tests=', len(unique_changelist_tests))
    print('unique_set=', len(unique_set))


    # Write all the changelists in a csv file
    wtr = csv.writer(open('./data/intermediate/h5c-dev/vsphere-client-modules.csv', 'w'))
    for changelist in unique_set:
        changelist_list = [changelist]
        wtr.writerow(changelist_list)
    p4.disconnect()                # Disconnect from the server
except Exception as e:
    print(e)         # Display errors