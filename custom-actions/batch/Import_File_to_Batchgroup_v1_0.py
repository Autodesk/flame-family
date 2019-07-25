'''
Right click on a clip in the mediahub to import the clip into a batch group set to clip length with a render node
Works with Flame 2020 and up
Copy script into /opt/Autodesk/shared/python or /opt/Autodesk/user/YOURUSER/python. 
Written by Michael Vaglienty, June 16th, 2019 - email: michaelv_2d@hotmail.com - www.pyflame.com
'''

def importClip(selection):
    import flame
    import re
        
    for n in selection:
        clipPath = str(n.path)
        shelfReels = ['Renders']
        schematicReels = ['Elements', 'Plates', 'PreRenders', 'Ref']        
        batchGroup = flame.batch.create_batch_group('New Batch', duration=100, reels=schematicReels, shelf_reels=shelfReels)
        importedClip = flame.batch.import_clip(clipPath, 'Plates')

        for clip in flame.batch.nodes:
            batchGroup.name = clip.name
            batchGroup.duration = clip.duration

        clipTimecode = batchGroup.reels[1].clips[0].start_time

        renderNode = batchGroup.create_node('Render')
        renderNode.range_end = clip.duration            
        renderNode.source_timecode = clipTimecode
        renderNode.record_timecode = clipTimecode
        renderNode.name = '<batch iteration>'
        renderNode.pos_x = 400
        renderNode.pos_y = -30

        flame.batch.connect_nodes(clip, 'Default', renderNode, 'Default')    
        
        flame.go_to('Batch')        

def scopeFile(selection):
    import flame
    import re

    for item in selection:
        itemPath = str(item.path)
        itemExt = re.search(r'\.\w{3}$', itemPath, re.I)
        if itemExt != (None):
            return True
    return False
                        
def get_mediahub_files_custom_ui_actions():
    return [{'name': 'pyFlame', 'actions': [{'name': 'Create New Batch', 'isVisible': scopeFile, 'execute': importClip, 'minimumVersion': '2020'}]}]


