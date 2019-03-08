from graphviz import Digraph
dot = Digraph(comment='New Primary Pipeline')
dot.graph_attr['rankdir'] = 'LR'
dot.node('primary-pipeline', 'New Primary Pipeline\nProposed', fontcolor='Red', color='blue', fontsize="85")


# sb builds
dot.node('sandbpx', 'Kick off "vsphere-h5client"\nsb builds for CLN = 1, 2, 3', fontcolor='blue', color='blue', fontsize="85")
dot.edge('primary-pipeline', 'sandbpx', 'Step-1\n(CLN = 1,2,3)', fontcolor='darkgoldenrod4', color='blue', fontname="times italic", fontsize="85", arrowsize="5")

# local builds
dot.node('create-build', 'Create build\nfor CLN = 3', fontcolor='blue', color='blue', fontsize="85")
dot.edge('primary-pipeline', 'create-build', 'Step-2\n(CLN = 1,2,3)', fontcolor='darkgoldenrod4', color='blue', fontname="times italic", fontsize="85", arrowsize="5")

# JS Tests
dot.node('js-tests', 'Run JS Tests', fontcolor='blue', color='blue', fontsize="85")
dot.edge('create-build', 'js-tests', 'Step-3', fontcolor='darkgoldenrod4', color='blue', fontname="times italic", fontsize="85", arrowsize="5")

# Result
dot.node('result2', 'Result?', fontcolor='blue', color='blue', fontsize="85", shape="diamond")
dot.edge('js-tests', 'result2', fontcolor='darkgoldenrod4', color='blue', fontname="times italic", fontsize="85", arrowsize="5")

#Result
dot.node('result2-pass', 'No Action Required', fontcolor='blue', color='blue', fontsize="85")
dot.edge('result2', 'result2-pass', 'All Pass',fontcolor='darkgoldenrod4', color='blue', fontname="times italic", fontsize="85", arrowsize="5")

#Result
dot.node('result2-fail', 'Backout CLN', fontcolor='blue', color='blue', fontsize="85")
dot.edge('result2', 'result2-fail', 'Fail',fontcolor='darkgoldenrod4', color='blue', fontname="times italic", fontsize="85", arrowsize="5")

# E2E Tests
dot.node('e2e-tests', 'Run E2E Tests', fontcolor='blue', color='blue', fontsize="85")
dot.edge('create-build', 'e2e-tests', 'Step-4', fontcolor='darkgoldenrod4', color='blue', fontname="times italic", fontsize="85", arrowsize="5")

# H5 Automation
dot.node('h5-automation', '"h5automation"\nsb creation', fontcolor='blue', color='blue', fontsize="85")
dot.edge('h5-automation', 'e2e-tests', 'Step-6', fontcolor='darkgoldenrod4', color='blue', fontname="times italic", fontsize="85", arrowsize="5")

# tests
dot.node('tests', 'All tests which have\nnot been fragile and malicious\nin last 7 days from q-mon database', fontcolor='blue', color='blue', fontsize="85")
dot.edge('tests', 'h5-automation', 'Step-5', fontcolor='darkgoldenrod4', color='blue', fontname="times italic", fontsize="85", arrowsize="5")

# E2E Tests again
dot.node('e2e-tests-again', 'Run failed\nE2E Tests again', fontcolor='blue', color='blue', fontsize="85")
dot.edge('e2e-tests', 'e2e-tests-again', 'Step-7\nElimintating fragile tests', fontcolor='darkgoldenrod4', color='blue', fontname="times italic", fontsize="85", arrowsize="5")

# E2E Tests again
dot.node('result', 'Result', fontcolor='blue', color='blue', fontsize="85", shape="diamond")
dot.edge('e2e-tests-again','result', 'Step-8', fontcolor='darkgoldenrod4', color='blue', fontname="times italic", fontsize="85", arrowsize="5")

# E2E Tests again
dot.node('no-action', 'No Action Required', fontcolor='blue', color='blue', fontsize="85")
dot.edge('result','no-action', 'All Pass', fontcolor='darkgoldenrod4', color='blue', fontname="times italic", fontsize="85", arrowsize="5")

# failed-tests
dot.node('failed-tests', 'Run Failed tests\nagainst sb builds(CLN=1,2)\nfrom Step-1', fontcolor='blue', color='blue', fontsize="85")
dot.edge('result','failed-tests', 'Step-9\nFaulty Change Detection', fontcolor='darkgoldenrod4', color='blue', fontname="times italic", fontsize="85", arrowsize="5")

#Result
dot.node('result1', 'Result', fontcolor='blue', color='blue', fontsize="85", shape="diamond")
dot.edge('failed-tests', 'result1', fontcolor='darkgoldenrod4', color='blue', fontname="times italic", fontsize="85", arrowsize="5")

#Pass
dot.node('result1-pass', 'No Action Required', fontcolor='blue', color='blue', fontsize="85")
dot.edge('result1', 'result1-pass', 'All Pass',fontcolor='darkgoldenrod4', color='blue', fontname="times italic", fontsize="85", arrowsize="5")

#Pass
dot.node('jira-bug', 'JIRA/Bugzilla bug raised\nfor failed testcase in previous run?', fontcolor='blue', color='blue', fontsize="85", shape="diamond")
dot.edge('result1', 'jira-bug', 'Step-10\nStill Fails',fontcolor='darkgoldenrod4', color='blue', fontname="times italic", fontsize="85", arrowsize="5")

#Pass
dot.node('jira-bug-yes', 'No Action Required', fontcolor='blue', color='blue', fontsize="85")
dot.edge('jira-bug','jira-bug-yes', 'Yes', fontcolor='darkgoldenrod4', color='blue', fontname="times italic", fontsize="85", arrowsize="5")


#Pass
dot.node('jira-bug-no', 'Backout CLN\nDrop e-mail', fontcolor='blue', color='blue', fontsize="85")
dot.edge('jira-bug','jira-bug-no', 'No', fontcolor='darkgoldenrod4', color='blue', fontname="times italic", fontsize="85", arrowsize="5")

print(dot)
dot.render('../../graphs/primary-pipeline-flowchart', view='true')