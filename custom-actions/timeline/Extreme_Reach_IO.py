"""Script to set in and out points in a timeline based on the Extreme Reach delivery specs."""
def get_media_panel_custom_ui_actions():

    def scope_clip(selection):
        import flame
        for item in selection:
            if isinstance(item, flame.PyClip):
                return True
        return False

    def set_selection_in_out_marks(selection, tc_in, tc_out):
    import flame
    for sequence in selection:
        i = sequence.duration.frame
        frameRate = sequence.frame_rate
        sequence.in_mark = flame.PyTime(tc_in, frameRate)
        sequence.out_mark = flame.PyTime(tc_out, frameRate)

    def er_io_60(selection):
        set_selection_in_out_marks(selection, in="00:59:53:00", out="01:01:00:01")

    def er_io_30(selection):
        set_selection_in_out_marks(selection, in="00:59:53:00", out="01:01:00:01")

    def er_io_20(selection):
        set_selection_in_out_marks(selection, in="00:59:53:00",  out="01:0020:01")

    def er_io_15(selection):
        set_selection_in_out_marks(selection, in="00:59:53:00",  out="01:00:15:01")

    def er_io_10(selection):
        set_selection_in_out_marks(selection, in="00:59:53:00",  out="01:00:10:01")

    return [
        {
            "name": "PYTHON: Timeline",
            "actions": [
                {
                    "name": "ER - I/O - :60",
                    "isVisible": scope_clip,
                    "execute": er_io_60
 #                   "minimumVersion": "2020"
                }
            ]
        },
        {
            "name": "PYTHON: Timeline",
            "actions": [
                {
                    "name": "ER - I/O - :30",
                    "isVisible": scope_clip,
                    "execute": er_io_30
#                    "minimumVersion": "2020"
                }
            ]
        },
        {
            "name": "PYTHON: Timeline",
            "actions": [
                {
                    "name": "ER - I/O - :20",
                    "isVisible": scope_clip,
                    "execute": er_io_20
#                    "minimumVersion": "2020"
                }
            ]
        },
        {
            "name": "PYTHON: Timeline",
            "actions": [
                {
                    "name": "ER - I/O - :15",
                    "isVisible": scope_clip,
                    "execute": er_io_15
#                    "minimumVersion": "2020"
                }
            ]
        },
        {
            "name": "PYTHON: Timeline",
            "actions": [
                {
                    "name": "ER - I/O - :10",
                    "isVisible": scope_clip,
                    "execute": er_io_10
#                    "minimumVersion": "2020"
                }
            ]
        }
    ]
