def get_batch_custom_ui_actions():
    def scope_node(selection):
        import flame
        for item in selection:
            if isinstance(item, flame.PyNode):
                if item.type == "Clip":
                    return True
        return False

    def create_motion(selection):
        import flame
        for item in selection:
            clip = flame.batch.current_node.get_value()
            action = flame.batch.create_node("Action")
            pos_x = clip.pos_x
            pos_y = clip.pos_y
            action.pos_x = pos_x + 400
            action.pos_y = pos_y
            media = action.add_media()
            media.pos_x = pos_x +200
            media.pos_y = pos_y

            flame.batch.connect_nodes(clip, "Default", media, "Default")

            motion_map = action.create_node("Motion Vectors Map")

            start = flame.batch.start_frame.get_value()
            end = start + clip.duration.get_value()

            motion_map.cache_range(start, end)

    return [
        {
            "name": "PYTHON: NODES",
            "actions": [
                {
                    "name": "Cache Motion Vectors Map",
                    "isVisible": scope_node,
                    "execute": create_motion
                }
            ]
        }
    ]

def get_paths():
    import PySide2

    actWindow = PySide2.QtWidgets.QApplication.instance().activeWindow()

    filenames, filter = PySide2.QtWidgets.QFileDialog.getOpenFileNames(actWindow,
      "Select one or more files to load",
      "/",
      "All files (*)",
      None,
      PySide2.QtWidgets.QFileDialog.DontUseNativeDialog )

    return filenames

def get_media_panel_custom_ui_actions():
    def scope_desktop(selection):
        import flame
        for item in selection:
            if isinstance(item, flame.PyDesktop):
                return True
        return False

    def create_batch_motion(selection):
        import flame, os
        for item in selection:
            flame.go_to("Batch")

            paths = get_paths()

            for filename in paths:
                bg = flame.batch.create_batch_group("MyNewBatch")

                clip = bg.import_clip(filename.encode("utf-8"), "Schematic Reel 1")

                bg.duration = clip.duration
                bg.name = clip.name
                bg.expanded = False

                action = flame.batch.create_node("Action")
                pos_x = clip.pos_x
                pos_y = clip.pos_y
                action.pos_x = pos_x + 400
                action.pos_y = pos_y
                media = action.add_media()
                media.pos_x = pos_x +200
                media.pos_y = pos_y

                flame.batch.connect_nodes(clip, "Default", media, "Default")

                motion_map = action.create_node("Motion Vectors Map")

                start = flame.batch.start_frame.get_value()
                end = start + clip.duration.get_value()

                motion_map.cache_range(start, end)

    return [
        {
            "name": "PYTHON: DESKTOP",
            "actions": [
                {
                    "name": "Create Batch and Cache Motion Vectors Map",
                    "isVisible": scope_desktop,
                    "execute": create_batch_motion
                }
            ]
        }
    ]
