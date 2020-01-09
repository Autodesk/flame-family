################################################################################
#
# Filename: create_user_shared_library.py
#
# Copyright (c) 2020 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

"""
Example of a custom UI action that exports a thumbnail and a movie for all
clips in a selection.
"""

import datetime
import os


def get_export_root():
    """
    Generate an export folder root with the current date/time.
    """
    return os.path.join(
        "/var/tmp/export",
        datetime.datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
    )


def export_movie(clip, export_dir):
    """
    Export a clip as a QuickTime to export_dir
    """

    import flame

    # Build the presets path.
    #
    # By using flame.PyExporter.get_presets_dir(), we don't need to know where
    # each application stores its presets. Or we could also use any path that
    # leads to a Flame export preset file.
    #
    # Possible visibilities are:
    #   Autodesk:   Factory presets shipped with the application.
    #   Shared:     Shared presets for all applications (/opt/Autodesk/shared).
    #   Project:    Project specific presets.
    #
    # Possible presets types are:
    #   Movie:                  Movie files (typically QuickTime & MXF)
    #   Image_Sequence:         Image sequences (Jpeg, Dpx, Exr)
    #   Audio:                  Audio files (wav)
    #   Sequence_Publish:       Complex sequence/timeline export (AAF, FCP X/7, EDL)
    #   Distribution_Package:   Distribution Package (IMF)
    #
    preset_dir = flame.PyExporter.get_presets_dir(
        flame.PyExporter.PresetVisibility.Autodesk,
        flame.PyExporter.PresetType.Movie
    )
    preset_path = os.path.join(
        preset_dir,
        "QuickTime",
        "QuickTime (8-bit Uncompressed).xml"
    )

    # Initialize the exporter instance we will use to do the export.
    #
    exporter = flame.PyExporter()

    # Set the exporter to use foreground export. By default it will send a
    # job to backburner to do the export.
    #
    exporter.foreground = True

    # Do the actual export.
    #
    exporter.export(clip, preset_path, export_dir)


def export_thumbnail(clip, export_dir):
    """
    Export the first frame of a clip in jpeg.
    """

    import flame

    # Build the presets path.
    #
    # By using flame.PyExporter.get_presets_dir(), we don't need to know where
    # each application stores its presets. Or we could also use any path that
    # leads to a Flame export preset file.
    #
    # Possible visibilities are:
    #   Autodesk:   Factory presets shipped with the application.
    #   Shared:     Shared presets for all applications (/opt/Autodesk/shared).
    #   Project:    Project specific presets.
    #
    # Possible presets types are:
    #   Movie:              Movie files (typically QuickTime & MXF)
    #   Image_Sequence:     Image sequences (Jpeg, Dpx, Exr)
    #   Audio:              Audio files (wav)
    #   Sequence_Publish:   Complex sequence/timeline export (AAF, FCP X/7, EDL)
    #
    preset_dir = flame.PyExporter.get_presets_dir(
        flame.PyExporter.PresetVisibility.Autodesk,
        flame.PyExporter.PresetType.Image_Sequence
    )
    preset_path = os.path.join(preset_dir, "Jpeg", "Jpeg (8-bit).xml")

    # Initialize the exporter instance we will use to do the export.
    #
    exporter = flame.PyExporter()

    # Set the exporter to use foreground export. By default it will send a
    # job to backburner to do the export.
    #
    exporter.foreground = True

    # We want to do a single frame export so we will modify the clip in/out
    # marks to point to the first frame and we will use the export_between_marks
    # options to tell the exporter that we want to use in/out marks as the
    # range to export
    #
    exporter.export_between_marks = True

    # Backup the clip in/out marks so we can restore them to current value
    # after the export.
    #
    in_mark = clip.in_mark.get_value()
    out_mark = clip.out_mark.get_value()
    try:
        # Set in/out mark to only export first frame. out_mark is exclusive
        # by default.
        #
        clip.in_mark = 1
        clip.out_mark = 2

        # Do the actual export.
        #
        exporter.export(clip, preset_path, export_dir)
    finally:
        # Restore the clip original in/out marks.
        #
        clip.in_mark = in_mark
        clip.out_mark = out_mark


def export_poster_frame(clip, export_dir):
    """
    Export the poster frame as requested in the preset (useFrameAsPoster)
    of a clip as jpeg.
    """

    import flame

    # Build the presets path.
    #
    # By using flame.PyExporter.get_presets_dir(), we don't need to know where
    # each application stores its presets. Or we could also use any path that
    # leads to a Flame export preset file.
    #
    # Possible visibilities are:
    #   Autodesk:   Factory presets shipped with the application.
    #   Shared:     Shared presets for all applications (/opt/Autodesk/shared).
    #   Project:    Project specific presets.
    #
    # Possible presets types are:
    #   Movie:              Movie files (typically QuickTime & MXF)
    #   Image_Sequence:     Image sequences (Jpeg, Dpx, Exr)
    #   Audio:              Audio files (wav)
    #   Sequence_Publish:   Complex sequence/timeline export (AAF, FCP X/7, EDL)
    #
    preset_dir = flame.PyExporter.get_presets_dir(
        flame.PyExporter.PresetVisibility.Autodesk,
        flame.PyExporter.PresetType.Image_Sequence
    )
    preset_path = os.path.join(
        preset_dir,
        "Poster Frame",
        "Poster Frame Jpeg (8-bit).xml"
    )

    # Initialize the exporter instance we will use to do the export.
    #
    exporter = flame.PyExporter()

    # Set the exporter to use foreground export. By default it will send a
    # job to backburner to do the export.
    #
    exporter.foreground = True

    exporter.export(clip, preset_path, export_dir)

def export_publish_poster_frame(clip, export_dir):
    """
    Export the poster frame of a sequence publish requested in the preset
    (useFrameAsPoster) of a clip as jpeg.
    """

    import flame

    # Build the presets path.
    #
    # By using flame.PyExporter.get_presets_dir(), we don't need to know where
    # each application stores its presets. Or we could also use any path that
    # leads to a Flame export preset file.
    #
    # Possible visibilities are:
    #   Autodesk:   Factory presets shipped with the application.
    #   Shared:     Shared presets for all applications (/opt/Autodesk/shared).
    #   Project:    Project specific presets.
    #
    # Possible presets types are:
    #   Movie:              Movie files (typically QuickTime & MXF)
    #   Image_Sequence:     Image sequences (Jpeg, Dpx, Exr)
    #   Audio:              Audio files (wav)
    #   Sequence_Publish:   Complex sequence/timeline export (AAF, FCP X/7, EDL)
    #
    preset_dir = flame.PyExporter.get_presets_dir(
        flame.PyExporter.PresetVisibility.Autodesk,
        flame.PyExporter.PresetType.Sequence_Publish
    )
    preset_path = os.path.join(
        preset_dir,
        "Poster Frame",
        "Poster Frame Jpeg (8-bit).xml"
    )

    # Initialize the exporter instance we will use to do the export.
    #
    exporter = flame.PyExporter()

    # Set the exporter to use foreground export. By default it will send a
    # job to backburner to do the export.
    #
    exporter.foreground = True

    exporter.export(clip, preset_path, export_dir)

def export_movies(selection, export_root=None):
    """
    Export all clips in a selection as QuickTime.
    """

    import flame

    # Create the export root.
    #
    export_dir = os.path.join(
        export_root if export_root is not None else get_export_root(),
        "movies"
    )
    os.makedirs(export_dir)

    # Iterate the selection.
    #
    for item in selection:

        # Check if the item in the selection is a sequence or a clip
        #
        if isinstance(item, (flame.PySequence, flame.PyClip)):
            export_movie(item, export_dir)


def export_thumbnails(selection, export_root=None):
    """
    Export the first frames of all clips as jpeg.
    """

    import flame

    # Create the export root.
    #
    export_dir = os.path.join(
        export_root if export_root is not None else get_export_root(),
        "thumbnails"
    )
    os.makedirs(export_dir)

    # Iterate the selection.
    #
    for item in selection:

        # Check if the item in the selection is a sequence or a clip.
        #
        if isinstance(item, (flame.PySequence, flame.PyClip)):
            export_thumbnail(item, export_dir)

def export_poster_frames(selection, export_root=None):
    """
    Export the poster frame as requested in the preset (useFrameAsPoster)
    of all selected clips as jpeg.
    """

    import flame

    # Create the export root.
    #
    export_dir = os.path.join(
        export_root if export_root is not None else get_export_root(),
        "poster_frames"
    )
    os.makedirs(export_dir)

    # Iterate the selection.
    #
    for item in selection:

        # Check if the item in the selection is a sequence or a clip.
        #
        if isinstance(item, (flame.PySequence, flame.PyClip)):
            export_poster_frame(item, export_dir)

def export_publish_poster_frames(selection, export_root=None):
    """
    Export the poster frame as requested in the preset (useFrameAsPoster)
    of a sequence publish for the selected clip as jpeg.
    """

    import flame

    # Create the export root.
    #
    export_dir = os.path.join(
        export_root if export_root is not None else get_export_root(),
        "publish_poster_frames"
    )
    os.makedirs(export_dir)

    # Iterate the selection.
    #
    for item in selection:

        # Check if the item in the selection is a sequence or a clip.
        #
        if isinstance(item, (flame.PySequence, flame.PyClip)):
            export_publish_poster_frame(item, export_dir)

def export_thumbnail_movie(selection):
    """
    Export all clips in a selection as QuickTime and Jpeg.
    """

    export_root = get_export_root()
    export_movies(selection, export_root)
    export_thumbnails(selection, export_root)


def get_media_panel_custom_ui_actions():
    return [
        {
            "name": "Examples / Export",
            "actions": [
                {
                    "name": "Export selection (thumbnail + movie)",
                    "execute": export_thumbnail_movie,
                    "minimumVersion": "2020.1",
                },
                {
                    "name": "Export selection (thumbnail)",
                    "execute": export_thumbnails,
                    "minimumVersion": "2020.1",
                },
                {
                    "name": "Export selection (movie)",
                    "execute": export_movies,
                    "minimumVersion": "2020.1",
                },
                {
                    "name": "Export selection (poster frames)",
                    "execute": export_poster_frames,
                    "minimumVersion": "2020.1",
                },
                {
                    "name": "Export publish selection (poster frames)",
                    "execute": export_publish_poster_frames,
                    "minimumVersion": "2020.1",
                }
            ]
        }
    ]


def get_main_menu_custom_ui_actions():
    return get_media_panel_custom_ui_actions()
