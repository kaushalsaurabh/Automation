from graphviz import Digraph

dot = Digraph(comment='Eliminating primary pipeline build-tzar by post-checkin job')
dot.graph_attr['rankdir'] = 'LR'
dot.node('automated-triaging', 'Post-checkin job to eliminate \nprimary pipeline build-tzar', fontcolor='Red', color='blue', fontsize="130",
         fontname="times bold")


# Actual Implementation
dot.node('implementation', 'Implementation',color='blue',fontcolor='blue', shape='rectangle', fontsize="130")
dot.edge('automated-triaging', 'implementation', 'Step 1', fontcolor='blue', color='blue', fontsize="130", fontname="times italic")

# Failures before the actual run
dot.node('failure', 'CLN queued for next run', fontcolor='red', color='red', fontsize="130", style="dotted")
dot.edge('implementation', 'failure', 'Failures such as Infra\nbefore the actual run', fontcolor='red', color='red', fontsize="130",
         style="dotted", fontname="times italic")

# Running tests
dot.node('running_tests1', 'Running tests to \n certify given change', fontcolor='blue', color='blue', fontsize="130")
dot.edge('implementation', 'running_tests1', 'Step 1.a', fontcolor='blue', color='blue', fontsize="130", fontname="times italic")

# Getting stable tests
dot.node('h5automation1', 'Tests which have passed in last\n7 days from q-mon database\nexcluding all malicious and fragile tests',
         fontcolor='blue', color='blue', fontsize="130")
dot.edge('running_tests1', 'h5automation1', ' What tests to run ?\nStep 1.a.i', fontcolor='blue',
         color='blue', fontsize="130", fontname="times italic")

# Getting stable tests
dot.node('stable_tests1', 'Generate h5automation build\n with changed run-list.json\nhaving tests from Step-1.a.i',
         fontcolor='blue', color='blue', fontsize="130")
dot.edge('running_tests1', 'stable_tests1', ' Step 1.a.ii', fontcolor='blue', color='blue', fontsize="130", fontname="times italic")


# Getting build
dot.node('change1', 'Create build with given changes', fontcolor='blue', color='blue', fontsize="130")
dot.edge('running_tests1', 'change1', 'Build which has\ncurrent changes\nStep 1.a.iii',
         fontcolor='blue', color='blue', fontsize="130", fontname="times italic")

# Staging
dot.node('staging1', 'Run tests from Step-1.a.ii\n against build from Step-1.a.iii', fontcolor='blue', color='blue', fontsize="130")
dot.edge('running_tests1', 'staging1', 'Running Tests\nStep 1.a.iv', fontcolor='blue', color='blue', fontsize="130", fontname="times italic")

# Backing out
dot.node('backing1', 'Backing out faulty checkin', fontcolor='blue', color='blue', fontsize="130")
dot.edge('implementation', 'backing1', 'Step 1.b', fontcolor='blue', color='blue', fontsize="130", fontname="times italic")

# Running tests
dot.node('identifying1', 'Re-running failed tests\n against all check-ins',
         fontcolor='blue', color='blue', fontsize="130")
dot.edge('backing1', 'identifying1', 'Identifying faulty check-in\nStep 1.b.i',
         fontcolor='blue', color='blue', fontsize="130", fontname="times italic")

# Running tests
dot.node('script_backing1', 'Python script which \nbacks out changes from Perforce',
         fontcolor='blue', color='blue', fontsize="130")
dot.edge('backing1', 'script_backing1', 'Step 1.b.ii', fontcolor='blue', color='blue', fontsize="130", fontname="times italic")

# Sending e-mail
dot.node('e-mail1', 'Sending e-mail to the person\nwhose changes are backed out',
         fontcolor='blue', color='blue', fontsize="130")
dot.edge('backing1', 'e-mail1', 'Step 1.b.iii', fontcolor='blue', color='blue', fontsize="130", fontname="times italic")

# Actual Implementation
dot.node('frequency', '10 min to begin\nIncrease later',color='darkgreen',fontcolor='darkgreen', shape='rectangle', fontsize="130")
dot.edge('automated-triaging', 'frequency','Frequency of run',fontcolor='darkgreen', color='darkgreen', fontsize="130", fontname="times italic")

print(dot)
dot.render('../../graphs/post-checkin-presentation', view='true')