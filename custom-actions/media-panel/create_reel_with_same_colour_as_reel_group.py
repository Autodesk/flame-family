"""Create a reel that inherits the colour coding of the reel group it is added under."""

def get_media_panel_custom_ui_actions():
    """Return custom actions to execute on Media Panel objects."""

    def scope_reel(selection):
        """Scope the custom action to the Reel Groups."""
        import flame
        for item in selection:
            if isinstance(item, flame.PyReelGroup):
                return True
        return False

    def create_reel(selection):
        """Propagate the colour of the parent Reel Group to the newly created Reel."""
        import flame
        for item in selection:
            reel = item.create_reel("New Reel")
            reel.colour = reel.parent.colour

    return [
        {
            "name": "Custom",
            "actions": [
                {
                    "name": "Create Reel",
                    "isVisible": scope_reel,
                    "execute": create_reel
                }
            ]
        }
    ]