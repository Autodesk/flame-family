"""Creates a Dated Folder in the Library"""
def get_media_panel_custom_ui_actions():

    def scope_libraries(selection):
        import flame
        for item in selection:
            if isinstance(item, flame.PyLibrary):
                return True
        return False

    def dated_folder(selection):
        import datetime
        date = datetime.date.today().strftime('%Y_%m_%d')

        for item in selection:
            datedFolder = item.create_folder(date)


    return [
        {
            "name": "PYTHON: Library",
            "actions": [
                {
                    "name": "Create Dated Folder",
                    "isVisible": scope_libraries,
                    "execute": dated_folder
                    "minimumVersion": "2020"
                }
            ]
        }

    ]