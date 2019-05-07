def get_media_panel_custom_ui_actions():
    def scope_reel(selection):
        import flame
        for item in selection:
            if isinstance(item, (flame.PyReelGroup)):
                return True
        return False

    def create_reel(selection):
        import flame
        for item in selection:
            reel = item.create_reel("New Reel")
            reel.colour = reel.parent.colour

    return [
         {
            "name": "PYTHON: REEL GROUP",
            "actions": [
                {
                    "name": "Create Reel",
                    "isVisible": scope_reel,
                    "execute": create_reel
                }
            ]
        }
    ]