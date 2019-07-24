"""Delete all iterations other than the current one in a Batch Group."""

def get_media_panel_custom_ui_actions():
    """Return custom actions to execute on Media Panel objects."""

    def scope_desktop(selection):
        """Scope the custom action to the Desktop."""
        import flame
        for item in selection:
            if isinstance(item, (flame.PyDesktop)):
                return True
        return False

    def scope_batch_group(selection):
        """Scope the custom action to the Batch Groups."""
        import flame
        for item in selection:
            if isinstance(item, (flame.PyBatch)):
                return True
        return False

    def scope_library(selection):
        """Scope the custom action to the Librariess."""
        import flame
        for item in selection:
            if isinstance(item, (flame.PyLibrary)):
                return True
        return False

    def scope_folder(selection):
        """Scope the custom action to the Folders."""
        import flame
        for item in selection:
            if isinstance(item, (flame.PyFolder)):
                return True
        return False

    def clean_desktop(selection):
        """Delete all iterations other than the current one for all Batch Groups residing in a Desktop."""
        import flame
        workspace = flame.projects.current_project.current_workspace
        for batch_group in workspace.desktop.batch_groups:
            workspace.desktop.current_batch_group = batch_group
            for iteration in batch_group.batch_iterations:
                flame.delete(iteration, confirm=False)

    def clean_batch_group(selection):
        """Delete all iterations other than the current one in a Batch Group."""
        import flame
        for batch_group in selection:
            for iteration in batch_group.batch_iterations:
                flame.delete(iteration, confirm=False)

    def find_and_clean_batch_group(folder):
        """Delete all iterations other than the current one in all Batch Groups of a Library or Folder."""
        import flame
        for batch_group in folder.batch_groups:
            for iteration in batch_group.batch_iterations:
                flame.delete(iteration, confirm=False)
        for folders in folder.folders:
            find_and_clean_batch_group(folders)

    def clean_in_top_library(selection):
        """Delete all Batch Groups inside a Library"""
        for top_library in selection:
            find_and_clean_batch_group(top_library)

    def clean_in_top_folder(selection):
        """Delete all Batch Groups inside a Folder"""
        for top_folder in selection:
            find_and_clean_batch_group(top_folder)

    return [
        {
            "name": "Custom",
            "actions": [
                {
                    "name": "Clean Batch Iterations",
                    "isVisible": scope_desktop,
                    "execute": clean_desktop,
                    "minimumVersion": "2020.1"
                }
            ]
        },
        {
            "name": "Custom",
            "actions": [
                {
                    "name": "Clean Batch Iterations",
                    "isVisible": scope_batch_group,
                    "execute": clean_batch_group
                }
            ]
        },
        {
            "name": "Custom",
            "actions": [
                {
                    "name": "Clean Batch Iterations",
                    "isVisible": scope_library,
                    "execute": clean_in_top_library
                }
            ]
        },
        {
            "name": "Custom",
            "actions": [
                {
                    "name": "Clean Batch Iterations",
                    "isVisible": scope_folder,
                    "execute": clean_in_top_folder
                }
            ]
        }
    ]
