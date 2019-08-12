'''Adds right click menu in batch to open Flame import browser. v1.0'''
# Works with Flame 2020.1 and higher
# Copy script into /opt/Autodesk/shared/python or /opt/Autodesk/user/YOURUSER/python.
# Written by Michael Vaglienty, June 16th, 2019 - email: michaelv_2d@hotmail.com - www.pyflame.com

def open_file_browser(selection):
    '''Open Flame import browser'''
    import flame

    flame.execute_shortcut('Import...')

def get_batch_custom_ui_actions():
    '''Batch custom action'''

    return [
        {
            'name': 'pyFlame',
            'actions': [
                {
                    'name': 'Import...',
                    'execute': open_file_browser,
                    'minimumVersion': '2020.1'
                }
            ]
        }
    ]
