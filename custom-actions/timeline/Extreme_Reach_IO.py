"""Script to set in and out points in a timeline based on the Extreme Reach delivery specs.""""
def get_media_panel_custom_ui_actions():

    def scope_clip(selection):
        import flame
        for item in selection:
            if isinstance(item, flame.PyClip):
                return True
        return False

    def er_io_60(selection):
        import flame
        for sequence in selection:
            i = sequence.duration.frame
            frameRate = sequence.frame_rate
            tc_IN = flame.PyTime("00:59:53:00", frameRate)
            tc_OUT = flame.PyTime("01:01:00:01", frameRate)
            sequence.in_mark = tc_IN
            sequence.out_mark = tc_OUT

    def er_io_30(selection):
        import flame
        for sequence in selection:
            i = sequence.duration.frame
            frameRate = sequence.frame_rate
            tc_IN = flame.PyTime("00:59:53:00", frameRate)
            tc_OUT = flame.PyTime("01:00:30:01", frameRate)
            sequence.in_mark = tc_IN
            sequence.out_mark = tc_OUT

    def er_io_20(selection):
        import flame
        for sequence in selection:
            i = sequence.duration.frame
            frameRate = sequence.frame_rate
            tc_IN = flame.PyTime("00:59:53:00", frameRate)
            tc_OUT = flame.PyTime("01:00:20:01", frameRate)
            sequence.in_mark = tc_IN
            sequence.out_mark = tc_OUT

    def er_io_15(selection):
        import flame
        for sequence in selection:
            i = sequence.duration.frame
            frameRate = sequence.frame_rate
            tc_IN = flame.PyTime("00:59:53:00", frameRate)
            tc_OUT = flame.PyTime("01:00:15:01", frameRate)
            sequence.in_mark = tc_IN
            sequence.out_mark = tc_OUT

    def er_io_10(selection):
        import flame
        for sequence in selection:
            i = sequence.duration.frame
            frameRate = sequence.frame_rate
            tc_IN = flame.PyTime("00:59:53:00", frameRate)
            tc_OUT = flame.PyTime("01:00:10:01", frameRate)
            sequence.in_mark = tc_IN
            sequence.out_mark = tc_OUT


    return [
        {
            "name": "PYTHON: Timeline",
            "actions": [
                {
                    "name": "ER - I/O - :60",
                    "isVisible": scope_clip,
                    "execute": er_io_60
                    "minimumVersion": "2020"
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
                    "minimumVersion": "2020"
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
                    "minimumVersion": "2020"
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
                    "minimumVersion": "2020"
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
                    "minimumVersion": "2020"
                }
            ]
        }
    ]
