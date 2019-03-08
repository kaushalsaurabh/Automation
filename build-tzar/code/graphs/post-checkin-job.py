from graphviz import Digraph

dot = Digraph(comment='Eliminating primary pipeline build-tzar by post-checkin job')
dot.graph_attr['rankdir'] = 'LR'
dot.node('automated-triaging', 'Post-checkin job to eliminate \nprimary pipeline build-tzar', fontcolor='Red', color='blue', fontsize="170")


# Testing
dot.node('testing', 'Building unit components\nbefore actual implementation', fontcolor='blue', shape='rectangle', color='blue',
         fontsize="170")
dot.edge('automated-triaging', 'testing', 'Step 1', fontcolor='blue', color='blue', fontsize="170")

# Running tests
dot.node('running_tests', 'Running tests to \n certify given change', fontcolor='blue', color='blue', fontsize="170",style='solid')
dot.edge('testing', 'running_tests', 'Step 1.a', fontcolor='blue', color='blue', fontsize="170")


# Getting stable tests
dot.node('h5automation', 'Tests which have passed in last\n7 days from q-mon database\nexcluding all malicious and fragile tests',
         fontcolor='blue', color='blue', fontsize="170")
dot.edge('running_tests', 'h5automation', ' What tests to run ?\nStep 1.a.i', fontcolor='blue', color='blue', fontsize="170")

# Getting stable tests
dot.node('stable_tests', 'Generate h5automation build\n with changed run-list.json\nhaving tests from Step-1.a.i',
         fontcolor='blue', color='blue', fontsize="170")
dot.edge('running_tests', 'stable_tests', ' Step 1.a.ii', fontcolor='blue', color='blue', fontsize="170")


# Getting build
dot.node('change', 'Primary pipeline already creates build\n Getting build from nfs folder', fontcolor='blue', color='blue', fontsize="170")
dot.edge('running_tests', 'change', 'Build which has\ncurrent change\nStep 1.a.iii', fontcolor='blue', color='blue', fontsize="170")

# Staging
dot.node('staging', 'Kick staging job', fontcolor='blue', color='blue', fontsize="170")
dot.edge('running_tests', 'staging', 'Running Tests\nStep 1.a.iv', fontcolor='blue', color='blue', fontsize="170")


# Running tests
dot.node('backing', 'Backing out faulty checkin', fontcolor='blue', color='blue', fontsize="170")
dot.edge('testing', 'backing', 'Step 1.b', fontcolor='blue', color='blue', fontsize="170")

# Running tests
dot.node('identifying', 'Re-running failed tests\n against all check-ins', fontcolor='blue', color='blue', fontsize="170")
dot.edge('backing', 'identifying', 'Identifying faulty check-in\nStep 1.b.i', fontcolor='blue', color='blue', fontsize="170")

# Running tests
dot.node('script_backing', 'Python script which \nbacks out changes from Perforce', fontcolor='blue', color='blue', fontsize="170")
dot.edge('backing', 'script_backing', 'Step 1.b.ii', fontcolor='blue', color='blue', fontsize="170")

# Sending e-mail
dot.node('e-mail', 'Sending e-mail to the person\nwhose changes are backed out', fontcolor='blue', color='blue', fontsize="170")
dot.edge('backing', 'e-mail', 'Step 1.b.iii', fontcolor='blue', color='blue', fontsize="170")

# Actual Implementation
dot.node('implementation', 'Actual implementation',color='darkgoldenrod4',fontcolor='darkgoldenrod4', shape='rectangle', fontsize="170")
dot.edge('automated-triaging', 'implementation', 'Step 2', fontcolor='darkgoldenrod4', color='darkgoldenrod4', fontsize="170")

# Running tests
dot.node('running_tests1', 'Running tests to \n certify given change', fontcolor='darkgoldenrod4', color='darkgoldenrod4', fontsize="170")
dot.edge('implementation', 'running_tests1', 'Step 2.a', fontcolor='darkgoldenrod4', color='darkgoldenrod4', fontsize="170")

# Getting stable tests
dot.node('h5automation1', 'Tests which have passed in last\n7 days from q-mon database\nexcluding all malicious and fragile tests',
         fontcolor='darkgoldenrod4', color='darkgoldenrod4', fontsize="170")
dot.edge('running_tests1', 'h5automation1', ' What tests to run ?\nStep 2.a.i', fontcolor='darkgoldenrod4',
         color='darkgoldenrod4', fontsize="170")

# Getting stable tests
dot.node('stable_tests1', 'Generate h5automation build\n with changed run-list.json\nhaving tests from Step-1.a.i',
         fontcolor='darkgoldenrod4', color='darkgoldenrod4', fontsize="170")
dot.edge('running_tests1', 'stable_tests1', ' Step 2.a.ii', fontcolor='darkgoldenrod4', color='darkgoldenrod4', fontsize="170")


# Getting build
dot.node('change1', 'Create build with given changes', fontcolor='darkgoldenrod4', color='darkgoldenrod4', fontsize="170")
dot.edge('running_tests1', 'change1', 'Build which has\ncurrent change\nStep 2.a.iii',
         fontcolor='darkgoldenrod4', color='darkgoldenrod4', fontsize="170")

# Staging
dot.node('staging1', 'Run Job', fontcolor='darkgoldenrod4', color='darkgoldenrod4', fontsize="170")
dot.edge('running_tests1', 'staging1', 'Running Tests\nStep 2.a.iv', fontcolor='darkgoldenrod4', color='darkgoldenrod4', fontsize="170")

# Backing out
dot.node('backing1', 'Backing out faulty checkin', fontcolor='darkgoldenrod4', color='darkgoldenrod4', fontsize="170")
dot.edge('implementation', 'backing1', 'Step 2.b', fontcolor='darkgoldenrod4', color='darkgoldenrod4', fontsize="170")

# Running tests
dot.node('identifying1', 'Re-running failed tests\n against all check-ins',
         fontcolor='darkgoldenrod4', color='darkgoldenrod4', fontsize="170")
dot.edge('backing1', 'identifying1', 'Identifying faulty check-in\nStep 2.b.i',
         fontcolor='darkgoldenrod4', color='darkgoldenrod4', fontsize="170")

# Running tests
dot.node('script_backing1', 'Python script which \nbacks out changes from Perforce',
         fontcolor='darkgoldenrod4', color='darkgoldenrod4', fontsize="170")
dot.edge('backing1', 'script_backing1', 'Step 2.b.ii', fontcolor='darkgoldenrod4', color='darkgoldenrod4', fontsize="170")

# Sending e-mail
dot.node('e-mail1', 'Sending e-mail to the person\nwhose changes are backed out',
         fontcolor='darkgoldenrod4', color='darkgoldenrod4', fontsize="170")
dot.edge('backing1', 'e-mail1', 'Step 2.b.iii', fontcolor='darkgoldenrod4', color='darkgoldenrod4', fontsize="170")


print(dot)
dot.render('../../graphs/primary-automated-triaging', view='true')