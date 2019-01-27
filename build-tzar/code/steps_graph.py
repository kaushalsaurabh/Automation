from graphviz import Digraph
dot = Digraph(comment='Automated Build-Tzar')
dot.node('build-tzar', 'Automated triaging \n for secondary pipeline', fontcolor='Red', color='blue', fontsize="30")


# Features
dot.node('features', 'Dynamic \n No code changes required \n for addition/ deletion of branches/test suites', style='dashed', color='darkgreen', fontcolor='darkgreen')
dot.edge('build-tzar', 'features', label='Salient Features', style='dashed', fontcolor='darkgreen', color='darkgreen' )


# Case-1
dot.node('case-1', 'Test case failures for which \n JIRA bugs have been raised in \n previous failures / other branches', fontcolor='blue', shape='rectangle')
dot.edge('build-tzar', 'case-1', label='Case-1', fontcolor='blue')

# Case-1 Example
dot.node('case-1-ex', 'Test com......ScheduleDrsTest failed \n but in previous run product bug VSUIR-335 was raised' , style='dashed')
dot.edge('case-1', 'case-1-ex', label='For Example', style='dashed')

# Case-2
dot.node('case-2', 'Test case failures for which \n there are no JIRA bugs', fontcolor='blue', shape='rectangle')
dot.edge('build-tzar', 'case-2', label='Case-2', fontcolor='blue')

# Step-1a
dot.node('step-1a', 'Getting JIRA bugs for failing test case \nfrom previous failures/ other branches', fontcolor='blue')
dot.edge('case-1', 'step-1a', label='Step-1a', fontcolor='blue')

# Step-1b
dot.node('step-1b', 'Updating the database \nwith JIRA bug so \nit is visible in qmon', fontcolor='blue')
dot.edge('step-1a', 'step-1b', label='Step-1b', fontcolor='blue')

# Step-1c
dot.node('step-1c', 'Updating the JIRA bug\n with log from latest failure', fontcolor='blue')
dot.edge('step-1b', 'step-1c', label='Step-1c', fontcolor='blue')

# Step-2a
dot.node('step-2a', 'Raising a JIRA bug \n with failure logs', fontcolor='blue')
dot.edge('case-2', 'step-2a', label='Step-2a', fontcolor='blue')

# Step-2b
dot.node('step-2b', 'Updating the database \nwith JIRA bug so \nit is visible in qmon', fontcolor='blue' )
dot.edge('step-2a', 'step-2b', label='Step-2b', fontcolor='blue')


print(dot)
dot.render('../graphs/Automated-Triaging-Steps', view='true')