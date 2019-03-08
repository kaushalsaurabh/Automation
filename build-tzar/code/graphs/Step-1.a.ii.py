from graphviz import Digraph

dot = Digraph(comment='Step-1.a.ii')
dot.graph_attr['rankdir'] = 'LR'
dot.node('automated-triaging', 'Step-1.a.ii\nGenerate h5automation build\n with changed run-list.json\nhaving tests from Step-1.a.i', fontcolor='Red', color='blue')


# Step-1
dot.node('testing', 'Checking out run-list.json \n from P4 and generating changelist\nthrough P4Python API', fontcolor='blue', color='blue')
dot.edge('automated-triaging', 'testing', 'Step 1', fontcolor='blue', color='blue')

# Step-2
dot.node('implementation', 'Editing run-list.json\nto disable fragile tests', color='blue',fontcolor='blue')
dot.edge('automated-triaging', 'implementation', 'Step 2', fontcolor='blue', color='blue')


# Step-3
dot.node('sandbox', 'Generating h5automation\nSandbox build from\nchangelist generated in Step-1', color='blue',fontcolor='blue')
dot.edge('automated-triaging', 'sandbox', 'Step 3', fontcolor='blue', color='blue')

print(dot)
dot.render('../../graphs/Step-1.a.ii', view='true')