'''A closed bug was first resolved. So it will show up in both lists.
This program eliminates duplicates '''
import csv

unique_set = set()

with open('closed/1_2017to4_2018.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        unique_set.add(row[0])

with open('closed/4_2018to11_2018.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        unique_set.add(row[0])

with open('closed/12_1_2018to12_31_2018.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        unique_set.add(row[0])

with open('resolved/1_2017to4_2018.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        unique_set.add(row[0])

with open('resolved/5_2018to12_2018.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        unique_set.add(row[0])

# Write to a file
wtr = csv.writer(open ('final/final_bug_list.csv', 'w'))
for issue in unique_set:
    issue_list = [issue]
    wtr.writerow(issue_list)