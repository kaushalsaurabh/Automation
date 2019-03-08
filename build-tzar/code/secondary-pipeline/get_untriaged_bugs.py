'''This script will query q-mon and get untriaged bugs'''

import psycopg2
import csv

def write_to_csv(file_path_name, rows):
    print('file_path_name=', file_path_name)
    wtr = csv.writer(open(file_path_name, 'w'))
    for current_row in rows:
        wtr.writerow(current_row)



def get_untriaged_bugs(qmon_col, branch, conn):
    try:
        # Get segment id for the given q-mon column
        cur = conn.cursor()

        # Get Segment id
        segment_type_id_query = "select segment_type_id from segment_branch_view where segment_name='"+ qmon_col + "' and branch_name='"+branch+"'"
        print("segment_type_id_query=", segment_type_id_query)
        cur.execute(segment_type_id_query)

        # Print results
        segment_type_id = [x[0] for x in cur.fetchall()][0]
        print("segment_type_id=", segment_type_id)

        # Get branch id for h5c-cloud
        cur.execute("select id from branch where name ='"+ branch + "'")

        # Print results
        branch_id = [x[0] for x in cur.fetchall()][0]
        print("branch_id=", branch_id)

        # Get top 10 changelists which have been used in secondary for a given q-mon column
        cur.execute("select distinct pipeline.cln from pipeline where pipeline.recommended = true and pipeline.branch_id = "+ str(branch_id) +"order by pipeline.cln desc limit 15")

        #Populate array of changelists
        changelists = []
        for changelist in cur.fetchall():
           changelists.append(changelist[0])

        final_rows = []

        for cln in changelists:

            print("************changelist***************", cln)
            # Get pipeline id for given branch
            pipeline_id_query = "select id from pipeline where cln="+str(cln) + " and branch_id = " + str(branch_id)
            print("pipeline_id_query=", pipeline_id_query)
            cur.execute(pipeline_id_query)

            # Print results
            pipeline_id = [x[0] for x in cur.fetchall()][0]
            print("pipeline_id=", pipeline_id)

            # Get segment id
            segment_id_query = "select id from segment where segment_type_id ="+str(segment_type_id) +" and  pipeline_id="+ str(pipeline_id)+" order by id desc limit 1"
            print("segment_id_query=", segment_id_query)
            cur.execute(segment_id_query)

            segment_query_results = cur.fetchall()
            if len(segment_query_results) == 0:
                continue

            segment_id = int()
            # Print results
            for segment_ids in segment_query_results:
                segment_id = segment_ids[0]
                print("segment_id=", segment_id)

            # Get log url and name of the failed tests
            failed_test_query = "select id, log, name, owner from result where segment_id="+str(segment_id) +" and (state ='failed' or state ='malicious') and issue_id is null"
            print("failed_test_query="+failed_test_query)
            cur.execute(failed_test_query)

            # Print results
            result_ids = []
            logs = []
            names = []
            owners = []
            for ids, log, name, owner in cur.fetchall():
                result_ids.append(ids)
                names.append(name)
                logs.append(log)
                owners.append(owner)
            print("result_ids=", result_ids)
            print("logs=", logs)
            print("names=",  names)
            print("owners=",  owners)
            row_to_be_written = [cln, segment_type_id, branch_id, segment_id, names, logs, owners, result_ids]
            final_rows.append(row_to_be_written)

        # Write the data to a file

        write_to_csv('../data/'+branch+'/intermediate/untriaged_bugs_'+qmon_col+'.csv', final_rows)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)