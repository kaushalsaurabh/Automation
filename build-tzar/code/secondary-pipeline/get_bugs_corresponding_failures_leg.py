import get_untriaged_bugs
import get_all_bugs
import triage_found_bugs
import time
import psycopg2
import csv
import os

start = time. time()

# Get all the unique branch names
hostname = ''
username = ''
password = ''
database = ''
conn = None
def get_bugs_corresponding_failures():
    try:
        conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        cur = conn.cursor()

        # Get all the branches in secondary pipeline
        branch_query = "select distinct branch_name from segment_branch_view where is_secondary = true and branch_name is not null and branch_name not like '%inactive%'"
        cur.execute(branch_query)
        branches = []
        for branch in cur.fetchall():
            branches.append(branch[0])

        print("branches=", branches)

        # Get all the test suites corresponding to these branches
        branch_segment_map = {}
        for branch in branches:
            segment_query = "select distinct segment_name from segment_branch_view where is_secondary = true and branch_name ='"+branch+"'  and segment_name not like '%Perf%'"
            cur.execute(segment_query)

            segments = []
            for given_segment in cur.fetchall():
                segments.append(given_segment[0])
            branch_segment_map[branch] = segments

        print("branch_segment_map=", branch_segment_map)

        for branch, segment_values in branch_segment_map.items():
            for current_segment in segment_values:
                os.makedirs('../data/'+branch+'/intermediate/', 0o755, 'true')
                os.makedirs('../data/' + branch + '/final/', 0o755, 'true')
                get_untriaged_bugs.get_untriaged_bugs(current_segment, branch, conn)
                get_all_bugs.get_product_bug_for_column('../data/'+branch+'/intermediate/', current_segment,  conn)
                triage_found_bugs.get_bugs_from_changelist('../data/'+branch+'/intermediate/', '../data/' + branch + '/final/',  current_segment)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

get_bugs_corresponding_failures()
end = time. time()

print("Time taken to run:", end - start)