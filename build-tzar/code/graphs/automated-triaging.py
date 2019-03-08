from graphviz import Digraph
dot = Digraph(comment='Automated Triaging in current situation')
dot.node('automated-triaging', 'Automated Triaging in current situation', fontcolor='Red', color='blue', fontsize="30")


# Backout
dot.node('Backout', 'Post Checkin Job \n which implements backout', fontcolor='blue', shape='rectangle')
dot.edge('automated-triaging', 'Backout', 'First Way', fontcolor='blue', color='blue')

# Backout
dot.node('group', 'Grouping Check-ins Together', fontcolor='blue', color='blue')
dot.edge('Backout', 'group', 'Implemented by', fontcolor='blue', color='blue')

# Backout
dot.node('flaky_tests', 'Difficult due to 110 flaky tests and increasing', fontcolor='red', color='red')
dot.edge('group', 'flaky_tests', 'Identifying faulty check-in', fontcolor='red', color='red')


dot.node('single', 'Running All Tests \nfor single checkin', fontcolor='blue' , color='blue')
dot.edge('Backout', 'single', 'Implemented by', fontcolor='blue', color='blue')

# Backout
dot.node('checkin_count', 'Check-ins will always be queued up.\nApprox 30 check-ins a day for h5c-main\n Each run takes close to 1:30 hours', fontcolor='red', color='red')
dot.edge('single', 'checkin_count',  fontcolor='red', color='red')


# Backout
dot.node('pre-checkin', 'Pre-Checkin Job', fontcolor='blue', shape='rectangle', color='blue')
dot.edge('automated-triaging', 'pre-checkin', 'Second Way', fontcolor='blue', color='blue')

dot.edge('pre-checkin', 'checkin_count',  fontcolor='red', color='red')


print(dot)
dot.render('../../graphs/primary-automated-triaging', view='true')