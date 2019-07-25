'''
Creates camera, camera light-linked, or diffuse projections in action
Right click on surface or geo and then select either diffuse or camera projection
Works with Flame 2020.1
Copy script into /opt/Autodesk/shared/python or /opt/Autodesk/user/YOURUSER/python 
Written by Michael Vaglienty, July 22nd, 2019 - email: michaelv_2d@hotmail.com - www.pyflame.com
'''

def findLine(item):
    global itemLine

    with open(actionFileName, 'r') as actionFile:
        for num, line in enumerate(actionFile, 1):
            if item in line:
                itemLine = num
                break  

def findLineLoop(item, itemLineNum):
    global itemLine

    actionFile = open(actionFileName)
    lines = actionFile.readlines()
    searchLine = lines[itemLineNum]

    if item in searchLine:
        itemLine = itemLineNum
    else:
        itemLineNum = itemLineNum + 1
        findLineLoop(item, itemLineNum)    
    
def getLineValue(lineNumber):
    global itemValue

    with open(actionFileName, 'r') as actionFile:
        for num, line in enumerate(actionFile, 1):
            if num == lineNumber:
                itemValue = line.rsplit(' ', 1)[1]
                break

#--------------------------------------------#

def getResultCamera():
    import flame
    global resultCameraNum, childNum

    saveActionNode()
    
    findLine('ResultCamChannel')
    
    resultCamLine = itemLine + 3

    getLineValue(resultCamLine)
    
    resultCameraNum = int(itemValue) + 1

    actionCameraList = ['null camera']
    
    actionNodeValues = flame.batch.current_node.get_value()
    
    for n in actionNodeValues.nodes:
        if 'Camera' in n.type:
            actionCameraList.append(n)
    
    if len(actionCameraList) == 2:
        resultCameraNum = 1

    resultCam = actionCameraList[resultCameraNum]
    resultCamName = str(resultCam.name)[1:-1]
    
    if resultCamName != 'DefaultCam':
        resultCameraNum = resultCameraNum
        resultCam = actionCameraList[resultCameraNum]
        resultCamName = str(resultCam.name)[1:-1]
    
    findLine(resultCamName)
    resultCamNumberLine = itemLine + 1
    
    getLineValue(resultCamNumberLine)
    resultCameraNumber = itemValue                   
    resultCamChildNum = 'Child ' + resultCameraNumber
    
    findLine(resultCamChildNum)
    childNum = itemLine

    def findParent(lineNum=childNum):
        global childNum, cameraParentName
        
        actionFile = open(actionFileName)
        lines = actionFile.readlines()
        nameLine = lines[childNum]
        
        if 'Name' in nameLine:
            cameraParentName = nameLine.rsplit(' ', 1)[1][:-1]
            if cameraParentName == 'scene':
                cameraParentName = None
            actionFile.close()
        else:
            childNum = childNum - 1
            findParent(childNum)
                
    findParent()
    
def createCurFrameCamera():
    import flame
    global newCamera, newCameraName, newCameraIndex, actionNode, actionNodeName, currentFrame, cameraExists

    currentFrame = flame.batch.current_frame

    newCameraName = 'frame_' + str(currentFrame)

    actionCameraList = ['null camera']

    actionNodeValues = flame.batch.current_node.get_value()
    
    for n in actionNodeValues.nodes:
        if 'Camera' in n.type:
            actionCameraList.append(n.name)

    if projectionType == 'diffuse':
        if newCameraName not in actionCameraList:
            cameraExists = False
            
            newActionCameraList = ['null camera']

            flame.execute_shortcut('Result View')
            flame.execute_shortcut('Action Create Camera at Camera Position')
            flame.execute_shortcut('Toggle Node Schematic View') 

            actionNodeValues = flame.batch.current_node.get_value()
            
            for n in actionNodeValues.nodes:
                if 'Camera' in n.type:
                    newActionCameraList.append(n)
            
            newCamera = newActionCameraList[-1]
            newCamera.name = 'tempCameraName'
            newCamera.name = newCameraName
            newCameraIndex = len(newActionCameraList) - 1
        else:
            cameraExists = True

            newCameraIndex = actionCameraList.index(newCameraName)
            print 'existing cameraIndex:', newCameraIndex
            
    elif projectionType == 'camera':
                
        newActionCameraList = ['null camera']

        flame.execute_shortcut('Result View')
        flame.execute_shortcut('Action Create Camera at Camera Position')
        flame.execute_shortcut('Toggle Node Schematic View') 

        actionNodeValues = flame.batch.current_node.get_value()
        
        for n in actionNodeValues.nodes:
            if 'Camera' in n.type:
                newActionCameraList.append(n)

        newCamera = newActionCameraList[-1]
        newCamera.name = 'tempCameraName'
        newCameraIndex = len(newActionCameraList) - 1

        def nameCameraNode(cameraNum=0):
            global newCameraName
      
            cameraName = newCameraName + '_' + str(cameraNum)
            
            if cameraName.endswith('0'):
                cameraName = cameraName.rsplit('_', 1)[0]

            if cameraName not in actionCameraList:
                newCamera.name = cameraName
                newCameraName = str(newCamera.name)[1:-1]
            else:
                cameraNum += 1
                nameCameraNode(cameraNum)
            
        nameCameraNode()

def saveActionNode():
    import flame
    import os
    global saveActionPath, actionFileName, actionNode, actionNodeName, tempFolder

    actionNodeName = str(flame.batch.current_node.get_value().name)[1:-1]
    actionNode = flame.batch.get_node(actionNodeName)

    tempFolder = '/opt/Autodesk/shared/python/tempAction'
    saveActionPath = os.path.join(tempFolder, actionNodeName)
    
    try:
        os.makedirs(tempFolder)
    except:
        pass
    
    actionNode.save_node_setup(saveActionPath)

    actionFileName = saveActionPath + '.action'

def getNodeList():
    import flame
    global actionNodeList

    actionNodeList = []
    
    actionNodeValues = flame.batch.current_node.get_value()
    
    for n in actionNodeValues.nodes:
        actionNodeList.append(n.name)
    
#--------------------------------------------#

def createCameraProjection(selection):
    import flame
    import shutil
    global projectionType, projectorName, itemLine

    def nameProjectorNode(nodeNum=0):
        global projectorName

        projectorNodeName = 'projector_frm_' + str(currentFrame) + '_' + str(nodeNum)           
        
        if projectorNodeName.endswith('0'):
            projectorNodeName = projectorNodeName.rsplit('_', 1)[0]

        if projectorNodeName not in actionNodeList:
            projector.name = projectorNodeName
            projectorName = str(projector.name)[1:-1]            
        else:
            nodeNum += 1
            nameProjectorNode(nodeNum)

    projectionType = 'camera'    
    
    getResultCamera()
 
    createCurFrameCamera()
 
    if cameraParentName != None:
        parentNode = actionNode.get_node(cameraParentName)
        childNode = actionNode.get_node(newCameraName)
        actionNode.connect_nodes(parentNode, childNode, link_type='Default')    

    for n in selection:
        geoNameLine = 'Name ' + str(n.name)[1:-1]
        geoType = n.type

    nodeProjectorPosXLine = 0
    nodeProjectorPosYLine = 0

    with open(actionFileName, 'r') as actionFile:
        for num, line in enumerate(actionFile, 1): 
            if 'Node Projector' in line:
                nodeProjectorPosXLine = num + 7
                nodeProjectorPosYLine = num + 8
    
    if nodeProjectorPosXLine != 0:
        getLineValue(nodeProjectorPosXLine)
        nodeProjectorPosX = itemValue

        getLineValue(nodeProjectorPosYLine)
        nodeProjectorPosY = itemValue

    projector = actionNode.create_node('Projector')    

    getNodeList()
    nameProjectorNode()    

    actionNode.connect_nodes(newCamera, projector)

    projector.fov = newCamera.fov

    projector.position = (0, 0, 0)

    saveActionNode()

    if geoType == 'Surface':
        findLine(geoNameLine)
        
        findLineLoop('PosX', itemLine)
        
        geoPosXLineNum = itemLine + 1
        geoPosYLineNum = geoPosXLineNum + 1
    elif geoType == 'Geom':
        findLine(geoNameLine)

        findLineLoop('PosX', itemLine)

        geoPosXLineNum = itemLine + 1
        geoPosYLineNum = geoPosXLineNum + 1

    findLine(projectorName)
    
    findLineLoop('PosX', itemLine)
    
    projectorPosXLineNum = itemLine + 1
    projectorPosYLineNum = projectorPosXLineNum + 1

    findLine(newCameraName)
    
    findLineLoop('PosX', itemLine)
    
    newCameraPosXLineNum = itemLine + 1
    newCameraPosYLineNum = newCameraPosXLineNum + 1    

    getLineValue(geoPosXLineNum)
    geoPosX = itemValue

    getLineValue(geoPosYLineNum)
    geoPosY = itemValue

    if nodeProjectorPosXLine == 0:
        newProjectorPosX = str(int(geoPosX) + 300)
        newProjectorPosY = geoPosY

        newCameraPosX = newProjectorPosX
        newCameraPosY = str(int(newProjectorPosY) + 150)
    else:
        newProjectorPosX = str(int(nodeProjectorPosX) + 300)
        newProjectorPosY = nodeProjectorPosY
        
        newCameraPosX = newProjectorPosX
        newCameraPosY = str(int(newProjectorPosY) + 150)
        
    editAction = open(actionFileName, 'r')
    contents = editAction.readlines()
    editAction.close
    
    contents[projectorPosXLineNum] = '        PosX %s\n' % newProjectorPosX
    contents[projectorPosYLineNum] = '        PosY %s\n' % newProjectorPosY
    
    contents[newCameraPosXLineNum] = '        PosX %s\n' % newCameraPosX
    contents[newCameraPosYLineNum] = '        PosY %s\n' % newCameraPosY
    
    editAction = open(actionFileName, 'w')
    contents = ''.join(contents)
    editAction.write(contents)
    editAction.close()    

    actionNode.load_node_setup(saveActionPath)  

    shutil.rmtree(tempFolder)
    
    print '\n', '\n', '=' * 60, '\n', 'CREATED CAMERA PROJECTION', '\n', '=' * 60, '\n'

def createLightLinkedCameraProjection(selection):
    import flame
  
    for n in selection:
        selectedGeoName = str(n.name)[1:-1]

    createCameraProjection(selection)
  
    parentNode = actionNode.get_node(projectorName)
    childNode = actionNode.get_node(selectedGeoName)
    
    actionNode.connect_nodes(parentNode, childNode, link_type='Light')     
    
def createDiffuseProjection(selection):
    import flame
    import shutil
    import os
    global projectionType, nodeCameraNameLine, newCameraLineNum, newCameraPosXLine, newCameraPosYLine

    def nameDiffuseNode(nodeNum=0):
        global diffuseMapName

        diffuseNodeName = 'diffuse_frm_' + str(currentFrame) + '_' + str(nodeNum)           
        
        if diffuseNodeName.endswith('0'):
            diffuseNodeName = diffuseNodeName.rsplit('_', 1)[0]

        if diffuseNodeName not in actionNodeList:
            diffuseMap.name = diffuseNodeName
            diffuseMapName = str(diffuseMap.name)[1:-1]            
        else:
            nodeNum += 1
            nameDiffuseNode(nodeNum)
    
    def getNodeList():
        global actionNodeList

        actionNodeList = []
        
        actionNodeValues = flame.batch.current_node.get_value()
        
        for n in actionNodeValues.nodes:
            actionNodeList.append(n.name)
    
    projectionType = 'diffuse'    

    getResultCamera()

    stereoCamera = ['right', 'left']
        
    with open(actionFileName, 'r') as actionFile:
        for num, line in enumerate(actionFile, 1): 
            if 'Node Camera' in line:
                nextLine = next(actionFile)
                if 'right' not in nextLine:
                    if 'left' not in nextLine:
                        nodeCameraNameLine = num

    findLineLoop('PosX', nodeCameraNameLine)
    
    nodeCameraPosXLine = itemLine + 1
    nodeCameraPosYLine = nodeCameraPosXLine + 1

    getLineValue(nodeCameraPosXLine)
    nodeCameraPosX = str(int(itemValue))

    getLineValue(nodeCameraPosYLine)
    nodeCameraPosY = itemValue

    createCurFrameCamera()

    nodeCameraPosX = str(int(nodeCameraPosX) + 200)

    if cameraParentName != None:
        parentNode = actionNode.get_node(cameraParentName)
        childNode = actionNode.get_node(newCameraName)
        actionNode.connect_nodes(parentNode, childNode, link_type='Default')

    diffuseMap = actionNode.create_node('Diffuse Map')

    getNodeList()
    nameDiffuseNode()

    saveActionNode()

    findLine(diffuseMapName)
    
    diffuseProjectionCameraLineNum = itemLine + 21
    diffuseProjectionMapLineNum = itemLine + 23

    findLine(newCameraName)

    newCameraLineNum = itemLine

    findLineLoop('PosX', newCameraLineNum)
    
    cameraPosXLine = itemLine + 1
    cameraPosYLine = cameraPosXLine + 1
  
    actionFile.close()      
          
    editAction = open(actionFileName, 'r')
    contents = editAction.readlines()
    editAction.close
    
    if cameraExists == False:
        contents[cameraPosXLine] = '        PosX %s\n' % nodeCameraPosX
        contents[cameraPosYLine] = '        PosY %s\n' % nodeCameraPosY
    
    contents[diffuseProjectionCameraLineNum] = '                        MapCamera %s\n' % str(int(newCameraIndex) - 1)
    contents[diffuseProjectionMapLineNum] = '                        MapCoordType PROJECTION\n'
    
    editAction = open(actionFileName, 'w')
    contents = ''.join(contents)
    editAction.write(contents)
    editAction.close()    

    actionNode.load_node_setup(saveActionPath)

    shutil.rmtree(tempFolder)
    
    print '\n', '\n', '=' * 60, '\n', 'CREATED DIFFUSE PROJECTION', '\n', '=' * 60, '\n'
          
#-------------------------------------#
        
def scopeGeo(selection):
    import flame

    geoTypes = ('Surface', 'Geom')

    for item in selection:
        if item.type in geoTypes:
            return True
    return False

#-------------------------------------#

def get_action_custom_ui_actions():
    return [{'name': 'pyFlame', 'actions': [{'name': 'Create Camera Projection', 'isVisible': scopeGeo, 'execute': createCameraProjection, 'minimumVersion': '2020.1'},
                                            {'name': 'Create Camera Light-Linked Projection', 'isVisible': scopeGeo, 'execute': createLightLinkedCameraProjection, 'minimumVersion': '2020.1'},
                                            {'name': 'Create Diffuse Projection', 'isVisible': scopeGeo, 'execute': createDiffuseProjection, 'minimumVersion': '2020.1'}]}]
