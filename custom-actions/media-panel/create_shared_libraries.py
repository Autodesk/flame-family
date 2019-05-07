def get_media_panel_custom_ui_actions():

    def scope_libraries(selection):
        import flame
        for item in selection:
            if isinstance(item, (flame.PyLibrary)):
                return True
        return False

    def create_shared_library(selection):
        import flame
        import os
        from PySide2 import QtWidgets
        
        dlg = QtWidgets.QInputDialog()
        dlg.setLabelText("Enter the artist name")
        if dlg.exec_():
            name = str(dlg.textValue())
        
        shared = flame.project.current_project.create_shared_library(name)
        shared.acquire_exclusive_access()
        shared.create_folder("from_"+name)
        shared.create_folder("to_"+name)
        shared.release_exclusive_access()

    return [
        {
            "name": "PYTHON: Libraries",
            "actions": [
                {
                    "name": "Create Shared Library",
                    "isVisible": scope_libraries,
                    "execute": create_shared_library
                }
            ]
        }

    ]
