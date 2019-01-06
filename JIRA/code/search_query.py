''' Query JIRA using credentials '''

from jira import JIRA
import re
import csv

# Initializing server

jira = JIRA(basic_auth=('', ''), options={'server':'https://jira.eng.vmware.com'})


# Jira bugs resolved from 2017/1/1 to 2018/12/31 - API seems to have a limit of max 1000 entries hence split in two
#h5_pipeline_issues = jira.search_issues('labels = h5-pipeline AND status changed to resolved during ("2017/1/01 00:00", "2018/4/30")', maxResults=1000)
#h5_pipeline_issues = jira.search_issues('labels = h5-pipeline AND status changed to resolved during ("2018/5/01 00:00", "2018/12/31")', maxResults=1000)


# Jira bugs closed from 2017/1/1 to 2018/12/31 - API seems to have a limit of max 1000 entries hence split in two
#h5_pipeline_issues = jira.search_issues('labels = h5-pipeline AND status changed to closed during ("2017/1/01 00:00", "2018/4/15")', maxResults=1000)
h5_pipeline_issues = jira.search_issues('labels = h5-pipeline AND status changed to closed during ("2018/12/1 00:00", "2018/12/31")', maxResults=1000)

print(len(h5_pipeline_issues))

# Write to a csv file with each bug as an entry in the row
wtr = csv.writer(open ('closed/12_1_2018to12_31_2018.csv', 'a'))
for issue in h5_pipeline_issues:
    issue_list = [issue]
    wtr.writerow(issue_list)