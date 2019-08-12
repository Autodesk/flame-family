'''Deletes all nodes in batch schematic that aren't connected v1.1'''
# Can NOT be undone with undo
# Works with Flame 2020 and higher
# Copy script into /opt/Autodesk/shared/python or /opt/Autodesk/user/YOURUSER/python
# Written by Michael Vaglienty July 22nd, 2019 - email: michaelv_2d@hotmail.com - www.pyflame.com

def delete_nodes(selection):
    '''Delete unconnected nodes'''
    import flame

    for item in flame.batch.nodes:
        node_sockets = str(item.sockets)
        if "['" not in node_sockets:
            flame.delete(item)

def get_batch_custom_ui_actions():
    '''Batch custom action'''

    return [
        {
            'name': 'pyFlame',
            'actions': [
                {
                    'name': 'Batch Node Cleanup',
                    'execute': delete_nodes,
                    'minimumVersion': '2020'
                }
            ]
        }
    ]
