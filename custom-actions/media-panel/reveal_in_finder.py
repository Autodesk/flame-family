'''Reveals selected clip(s) in finder window v1.1'''
# Works with Flame 2020 and up
# Copy into /opt/Autodesk/shared/python or /opt/Autodesk/user/YOURUSER/python
# Written by Michael Vaglienty, June 16th, 2019 - email: michaelv_2d@hotmail.com - www.pyflame.com


def reveal_clip(selection):
    '''Get clip path'''

    for item in selection:
        clip_path = item.versions[0].tracks[0].segments[0].file_path
        clip_path = clip_path.rsplit('/', 1)[0]

        if clip_path != '':
            open_finder(clip_path)

def reveal_batch_clip(selection):
    '''Get batch clip path'''

    for item in selection:
        if item.media_path is not None:
            clip_path = str(item.media_path)[1:-1]
            clip_path = clip_path.rsplit('/', 1)[0]
            if clip_path != '':
                open_finder(clip_path)

def open_finder(clip_path):
    '''Open finder window'''
    import platform
    import subprocess

    if platform.system() == 'Darwin':
        subprocess.Popen(['open', clip_path])
    else:
        subprocess.Popen(['xdg-open', clip_path])

#-------------------------------------#

def scope_batch_clip(selection):
    '''Create scope for the custom action.'''
    import flame

    for item in selection:
        if item.type == 'Clip':
            return True
    return False

def scope_clip(selection):
    '''Create scope for the custom action.'''
    import flame

    for item in selection:
        if isinstance(item, flame.PyClip):
            return True
    return False

#-------------------------------------#

def get_media_panel_custom_ui_actions():
    '''Media panel custom action'''

    return [
        {
            'name': 'pyFlame',
            'actions': [
                {
                    'name': 'Reveal File In Finder',
                    "isVisible": scope_clip,
                    "execute": reveal_clip,
                    "minimumVersion": "2020"
                }
            ]
        }
    ]

def get_batch_custom_ui_actions():
    '''Batch custom action'''

    return [
        {
            'name': 'pyFlame',
            'actions': [
                {
                    'name': 'Reveal File In Finder',
                    "isVisible": scope_batch_clip,
                    "execute": reveal_batch_clip,
                    "minimumVersion": "2020"
                }
            ]
        }
    ]
