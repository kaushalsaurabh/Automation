from graphviz import Digraph
dot = Digraph(comment='Primary Automated Build-Tzar')
dot.node('build-tzar', 'Eliminating build-tzar \n for primary pipeline', fontcolor='Red', color='blue', fontsize="30")


# Pre-checkin job
dot.node('pre-checkin', 'Pre-Checkin Job', fontcolor='blue', shape='rectangle')
dot.edge('build-tzar', 'pre-checkin',  fontcolor='blue')

# Questions need to be answered in some time
dot.node('questions', 'Frequency of pre-checkin job', style='dashed', color='darkgoldenrod4', fontcolor='darkgoldenrod4')
dot.edge('pre-checkin', 'questions', label='Questions need to be \nanswered in some time', style='dashed', fontcolor='darkgoldenrod4', color='darkgoldenrod4')

# pre-checkin job for every check-in
dot.node('every-checkin', 'Requires too many resources', style='dashed', color='darkgoldenrod4', fontcolor='darkgoldenrod4')
dot.edge('questions', 'every-checkin', label='Running job \nfor every check-in', border="2", fontcolor='darkgoldenrod4', color='darkgoldenrod4')

# pre-checkin job 2-3 times daily
dot.node('scheduling', 'Difficulty finding \n faulty check-in', style='dashed', color='darkgoldenrod4', fontcolor='darkgoldenrod4')
dot.edge('questions', 'scheduling', label='Scheduling 2-3 times daily', style='dashed', fontcolor='darkgoldenrod4', color='darkgoldenrod4')

# Eliminating false negatives
dot.node('false-negatives', 'Eliminating flaky tests (h5c-main)', fontcolor='red', shape='rectangle', color='red')
dot.edge('pre-checkin', 'false-negatives', label='Requires Immediate Attention',  color='Red' , fontcolor='red')

# Measure of success
dot.node('measure', 'Only Real Issues \n visible in 3-4 weeks', fontcolor='darkgreen', color='darkgreen', style='dashed')
dot.edge('false-negatives', 'measure', label='Measure of success', color='darkgreen', fontcolor='darkgreen', style='dashed')

# Manually
dot.node('manually', 'Build-tzar', fontcolor='red', shape='rectangle', color='red')
dot.edge('false-negatives', 'manually', label='Manually',  color='Red',  fontcolor='red')

# Deciding
dot.node('deciding', 'Test disabling criteria', fontcolor='red', shape='rectangle', color='red')
dot.edge('manually', 'deciding',   color='Red',  fontcolor='red')

# consensus
dot.node('consensus', 'Requires consensus \nacross 3 geographies', fontcolor='blue', color='blue', style='dashed')
dot.edge('deciding', 'consensus',  fontcolor='red', style='dashed', color='blue')

# Re-Trigger
dot.node('re-trigger', 'Re-run passes', fontcolor='red', color='red')
dot.edge('deciding', 're-trigger',  color='Red',  label='Failing tests \nin h5c-main pipeline ',  fontcolor='red')

# Historically
dot.node('historically', 'Historically flaked 5% times', fontcolor='red', color='red')
dot.edge('deciding', 'historically',  color='Red',  fontcolor='red')

# bug
dot.node('bug', 'Raising a bug \n with label = "flaky-test"', fontcolor='red',  color='red')
dot.edge('manually', 'bug',  color='Red',  fontcolor='red')

# Automatically
dot.node('automatically', 'Automated script', fontcolor='red', shape='rectangle', color='red')
dot.edge('false-negatives', 'automatically',  color='Red', label='Automated',  fontcolor='red')

# Automatically
dot.node('disable', 'Disabling tests \n flaking 5%,\nat cleanup 2%\n and raising a bug \nwith label = "flaky-test"', fontcolor='red',  color='red')
dot.edge('automatically', 'disable',  color='Red',  fontcolor='red')


print(dot)
dot.render('../../graphs/primary-automated-build-tzar', view='true')