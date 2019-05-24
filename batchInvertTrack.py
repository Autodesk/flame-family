def getCustomUIActions():
    def invertTrack(selection):
        import flame, os, commands, subprocess, random
        for item in selection:
            action = flame.batch.current_node.get_value()
            current = action.current_node.get_value()
            axisInvert = action.create_node("Axis")
            randomNum = ''.join(random.choice('1234156789') for i in range(3))
            axisInvert.name="Invert_Axis_" + randomNum
            x, y, z = current.position.get_value()
            posX = x * -1
            posY = y * -1
            posZ = z * -1
            axisInvert.position=(posX, posY, posZ)
            x, y, z = current.rotation.get_value()
            rotX = x * -1
            rotY = y * -1
            rotZ = z * -1
            axisInvert.rotation=(rotX, rotY, rotZ)
            x, y, z = current.scale.get_value()
            scaleX = 100 - x
            scale2X = scaleX +100
            scaleY = 100 - y
            scale2Y = scaleY + 100
            scaleZ = 100
            axisInvert.scale=(scale2X, scale2Y, scaleZ)
            x, y, z = current.shear.get_value()
            shearX = x * -1
            shearY = y * -1
            shearZ = z * -1
            axisInvert.shear=(shearX, shearY, shearZ)
            x, y, z = current.center.get_value()
            centerX = x * -1
            centerY = y * -1
            centerZ = z * -1
            axisInvert.center=(centerX, centerY, centerZ)
            for node in action.nodes:
                if 'Axis' in node.name.get_value():
                    action.connect_nodes(axisInvert, current)

    return [
         {
            "name": "PYTHON: NODES",
            "actions": [
                {
                    "name": "Invert Track",
                    "execute": invertTrack
                }
            ]
        }
    ]
