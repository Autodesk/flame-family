#!/bin/env python
################################################################################
#
# Filename: post_export_dependency.py
#
# Copyright (c) 2020 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

"""
Flame provides a python export API (PyExporter) that can drive the export
module without user interaction. This API has the same functionality as the
export in Flame.

The following have examples of custom UI actions that use the python export API
(PyExporter)and do a post export actions with three different methods
(command line / python / natively) in foregournd and background.
"""

import datetime
import os
import subprocess
import re

################################################################################
# The following 4 methods show how to call a command line as a post export
# action in both foreground and background.
#
# This is the simplest of the 3 methods to get something done after a background
# export. There is however no way to interact with Flame with this method.
################################################################################

def create_backburner_job(job_name, description, dependencies, cmd):
    """
    Send a command line job to Backburner.

    :param job_name: Name of the Backburner job
    :param description: Description of the Backburner job
    :param dependencies: None if the Backburner job should execute arbitrarily.
                         If you want to set the job up so that it executes after
                         another known task, pass the Backburner id or a list of
                         ids here. This is typically used in conjunction with a
                         postExportAsset hook where the export task runs on
                         Backburner. In this case, the hook will return the
                         Backburner id. By passing that id into this method,
                         you can create a job which only executes after the main
                         export task has completed.
    :param cmd: Command line to execute
    :return backburner_job_id: Id of the Backburner job created
    """

    # the Backburner command job executable
    backburner_job_cmd = os.path.join(
        "/opt",
        "Autodesk",
        "backburner",
        "cmdjob"
    )

    backburner_args = []
    backburner_args.append("-userRights") # Honor application user (not root)
    backburner_args.append("-timeout:600")
    backburner_args.append("-jobName:\"%s\"" % job_name)
    backburner_args.append("-description:\"%s\"" % description)

    # Set the backburner job dependencies
    if dependencies:
        if isinstance(dependencies, list):
            backburner_args.append("-dependencies:%s" % ",".join(dependencies))
        else:
            backburner_args.append("-dependencies:%s" % dependencies)

    full_cmd = "%s %s %s" % (
        backburner_job_cmd,
        " ".join(backburner_args),
        cmd
    )

    backburner_job_submission = subprocess.Popen(
        [full_cmd],
        stdout=subprocess.PIPE,
        shell=True
    )
    stdout, stderr = backburner_job_submission.communicate()
    print(stdout)

    job_id_regex = re.compile(r"(?<=Successfully submitted job )(\d+)")
    match = job_id_regex.search(stdout)

    if match:
        backburner_job_id = match.group(0)
        print("Backburner job created (%s)" % backburner_job_id)
        return backburner_job_id

    else:
        print("Backburner job not created\n%s" % stderr)

    return None

def export_movie_and_zip(selection, foreground):
    """
    Export all clips in a selection as QuickTime and zip them afterward.

    :param selection: Selection to export
    :param foreground: True if the export should be done in foreground,
                       False if the export should be done in background.
    """

    # The following object will override the postExportAsset callback
    # from the application for the exporter object we will use for this export.
    #
    class HooksOverride(object):
        def __init__(self, foreground):
            self._foreground = foreground

        def postExportAsset(self, info, userData, *args, **kwargs):
            del args, kwargs # Unused necessary parameters

            # Accumulate the ids of the jobs sent to Backburner.
            if  not self._foreground:
                userData.append(info["backgroundJobId"])

    jobs_ids = []
    export_dir = export_movies(
        selection,
        foreground=foreground,
        hooks=HooksOverride(foreground),
        hooks_user_data=jobs_ids
    )

    # Send a Backburner job that depends on all the jobs created while
    # exporting. If the export is done in foreground, jobs_ids will be empty
    # and the job will execute immediatly.
    #
    create_backburner_job(
        job_name="Zipping Exported Files",
        description="Zipping Exported Files",
        dependencies=jobs_ids,
        cmd="zip -r %s.zip %s" % (export_dir, export_dir)
    )


def export_movie_and_zip_foreground(selection):
    """
    Export all clips in a selection as QuickTime and zip them afterward in
    foreground.

    :param selection: Selection to export
    """
    return export_movie_and_zip(selection, foreground=True)


def export_movie_and_zip_background(selection):
    """
    Export all clips in a selection as QuickTime and zip them afterward in
    background.

    :param selection: Selection to export
    """
    return export_movie_and_zip(selection, foreground=False)


################################################################################
# The following 5 methods show how to handle post export in python in both
# foreground and background.
#
# This is the less intuitive approach since one could assume that since the
# python code is shared, the functionnality that can be done will be the same.
# It is good to note that the python interpreter that will run the post export
# callback is different than the one sending the background job.
#
# This means that the post export hook cannot use the Flame python API and that
# any state that is in the sender python interpreter must be serialized through
# the command line arguments (or a file which is pass through the arguments) to
# be used in the post export hook callback.
################################################################################

def create_python_backburner_job(job_name, description, dependencies, function, args=None):
    """
    Send a callback to this python file using command line job to backburner.

    :note: Beware. The file must be executable and will use the python
           interpreter bundled with Flame. Change the header for a different
           python intepreter.

    :param job_name: Name of the backburner job
    :param description: Description of the backburner job
    :param dependencies: None if the backburner job should execute arbitrarily.
                         If you want to set the job up so that it executes after
                         another known task, pass the backburner id or a list of
                         ids here. This is typically used in conjunction with a
                         postExportAsset hook where the export task runs on
                         backburner. In this case, the hook will return the
                         backburner id. By passing that id into this method,
                         you can create a job which only executes after the main
                         export task has completed.
    :param function: Function name to call
    :param args: Function arguments
    :return backburner_job_id: Id of the backburner job created
    """
    return create_backburner_job(
        job_name=job_name,
        description=description,
        dependencies=dependencies,
        cmd=" ".join([
            os.path.abspath(__file__),
            function,
            " ".join(args)
        ])
    )

def rename_function(old, new):
    """
    Example of a function using python to do something useful. In this case,
    this is using os.rename to rename a file.
    """
    print("Renaming %s -> %s" % (old, new))
    os.rename(old, new)

def export_movie_and_rename(selection, foreground):
    """
    Export a movie for each clip in the selection and add the suffix _renamed
    afterward.

    :param selection: Selection to export
    :param foreground: True if the export should be done in foreground,
                       False if the export should be done in background.
    """

    # The following object will override the postExportAsset callback
    # from the application for the exporter object we will use for this export.
    #
    class HooksOverride(object):
        def __init__(self, foreground):
            self._foreground = foreground

        def postExportAsset(self, info, userData, *args, **kwargs):
            del userData, args, kwargs # Unused necessary parameters
            full_path = os.path.join(
                info["destinationPath"],
                info["resolvedPath"]
            )
            if self._foreground:
                rename_function(full_path, full_path + "_renamed")
            else:
                create_python_backburner_job(
                    job_name="Renaming %s" % info["assetName"],
                    description="Renaming %s" % info["assetName"],
                    dependencies=info["backgroundJobId"],
                    function="rename_function",
                    args=[full_path, full_path + "_renamed"]
                )

    jobs_ids = []
    export_movies(
        selection,
        foreground=foreground,
        hooks=HooksOverride(foreground),
        hooks_user_data=jobs_ids
    )


def export_movie_and_rename_foreground(selection):
    """
    Export a movie for each clip in the selection and add the suffix _renamed
    afterward in foreground.

    :param selection: Selection to export
    """
    return export_movie_and_rename(selection, foreground=True)


def export_movie_and_rename_background(selection):
    """
    Export a movie for each clip in the selection and add the suffix _renamed
    afterward in background.

    :param selection: Selection to export
    """
    return export_movie_and_rename(selection, foreground=False)


################################################################################
# The following 2 methods show how to handle post export actions natively within
# Flame in both foreground and background.
#
# This is the only method that let the post export callback trigger an action
# from within Flame when sending a background job.
#
# BEWARE The idle event callable object will take over the UI thread which means
#        that, when running, no user interaction will be possible and that the
#        UI context might be switch/altered.
################################################################################

def export_movie_and_reimport_foreground(selection):
    """
    Export all clips in a selection as QuickTime and reimport them in Batch
    afterward in foreground.

    :param selection: Selection to export
    """

    # The following object will override the postExportAsset callback
    # from the application for the exporter object we will use for this export.
    #
    class HooksOverride(object):
        def __init__(self):
            pass

        def postExportAsset(self, info, userData, *args, **kwargs):
            del userData, args, kwargs # Unused necessary parameters
            import flame

            # Rebuild the path to the exported asset and import it in Batch
            #
            full_path = os.path.join(
                info["destinationPath"],
                info["resolvedPath"]
            )
            flame.batch.import_clip(full_path, "Schematic Reel 1")

    export_movies(
        selection,
        foreground=True,
        hooks=HooksOverride()
    )


def export_movie_and_reimport_background(selection):
    """
    Export all clips in a selection as QuickTime and reimport them in Batch
    afterward in background.

    :param selection: Selection to export
    """

    # The following object will override the postExportAsset callback
    # from the application for the exporter object we will use for this export.
    #
    class HooksOverride(object):
        def __init__(self):
            pass

        def postExportAsset(self, info, userData, *args, **kwargs):
            del args, kwargs # Unused necessary parameters

            # Accumulate the path to the exported assets and the ids of the
            # Backburner jobs created to export them.
            #
            full_path = os.path.join(
                info["destinationPath"],
                info["resolvedPath"]
            )
            userData.append((info["backgroundJobId"], full_path))

    jobs_infos = []
    export_movies(
        selection,
        foreground=False,
        hooks=HooksOverride(),
        hooks_user_data=jobs_infos
    )

    # We need to wait for the export jobs to complete before trying to reimport
    # the assets in Batch. To do that, we will query the Backburner manager
    # for the state of the jobs we just created.

    import flame

    from adsk.libwiretapPythonClientAPI import (
        WireTapClient,
        WireTapServerId,
        WireTapServerHandle,
        WireTapNodeHandle,
        WireTapStr
    )

    # This object is a callback object we will insert in the Flame's idle loop.
    # It will ask Flame to query the state of the next jobs to finish and once
    # it validated that the job is completed, it will import the clip.
    #
    # This object is meant to be rescheduled in the idle loop until the list of
    # jobs is empty.
    #
    # Since this is running in the idle loop, we want to minimize the work we
    # do in each iteration because this will impact user interactivity.
    #
    class ReImportCallback(object):
        def __init__(self, jobs_infos):
            self._jobs_infos = jobs_infos

            # Create a connection to the Backburner manager using the Wiretap
            # python API.
            #
            self._wiretap_client = WireTapClient()
            if not self._wiretap_client.init():
                raise Exception("Could not initialize Wiretap Client")
            backburner_server_id = WireTapServerId("Backburner", "localhost")
            self._backburner_server_handle = WireTapServerHandle(
                backburner_server_id
            )

        def __call__(self):
            # Get the next job state
            #
            job_id, path = self._jobs_infos.pop()
            node_handle = WireTapNodeHandle(self._backburner_server_handle, job_id)
            state = WireTapStr()
            if not node_handle.getMetaData("state", "", 0, state):
                print(
                    "Could not retrieve state of '%s': %s" % (
                        node_handle.getNodeId().id(),
                        node_handle.lastError()
                    )
                )
            elif state.c_str() != "complete":
                print("Waiting for job %s / %s [%s]" % (job_id, path, state))

                # If the jobs is not completed, add it back to the list
                # of jobs we monitor.
                #
                self._jobs_infos.append((job_id, path))

                # Rechedule the callback to run in one second with the next job
                # to query.
                #
                flame.schedule_idle_event(self, delay=1)
            else:
                # If the state of the jobs is complete. We can import the
                # asset back in Batch.
                #
                flame.batch.import_clip(path, "Schematic Reel 1")

                # Rechedule the callback to run in one second with the next job
                # to query if the is one.
                #
                if self._jobs_infos:
                    flame.schedule_idle_event(self, delay=1)

    flame.schedule_idle_event(ReImportCallback(jobs_infos), delay=1)


################################################################################
# Custom UI action methods
################################################################################

def export_movie(clip, export_dir, foreground, hooks, hooks_user_data):
    """
    Export a clip as a QuickTime to export_dir

    :param clip: Clip to export
    :param export_dir: Directory where to export
    :param foreground: True if the export should be done in foreground,
                       False if the export should be done in background.
    :param hooks: Python hooks override callback object.
    :param hooks_user_data: Python hooks override callback object user data.
    """

    import flame

    # Build the presets path.
    #
    # By using Flame.PyExporter.get_presets_dir(), we don't need to know where
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
    # job to Backburner to do the export.
    #
    exporter.foreground = foreground

    # Do the actual export.
    #
    exporter.export(
        clip,
        preset_path,
        export_dir,
        hooks=hooks,
        hooks_user_data=hooks_user_data
    )


def export_movies(selection, foreground, hooks, hooks_user_data=None):
    """
    Export all clips in a selection as QuickTime.

    :param selection: Selection to export
    :param foreground: True if the export should be done in foreground,
                       False if the export should be done in background.
    :param hooks: Python hooks override callback object.
    :param hooks_user_data: Python hooks override callback object user data.
    """

    import flame

    # Create the export root.
    #
    export_dir = get_export_dir()
    os.makedirs(export_dir)

    # Iterate the selection.
    #
    for item in selection:
        # Check if the item in the selection is a sequence or a clip
        #
        if isinstance(item, (flame.PySequence, flame.PyClip)):
            export_movie(item, export_dir, foreground, hooks, hooks_user_data)
    return export_dir


def get_export_dir():
    """
    Generate an export folder root with the current date/time.
    """
    return os.path.join(
        "/var/tmp/export",
        datetime.datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
    )


def get_media_panel_custom_ui_actions():
    return [
        {
            "name": "Examples / Export / Post Export Jobs",
            "actions": [
                {
                    "name": "Export selection and zip (Foreground)",
                    "execute": export_movie_and_zip_foreground,
                    "minimumVersion": "2020.1",
                },
                {
                    "name": "Export selection and zip (Background)",
                    "execute": export_movie_and_zip_background,
                    "minimumVersion": "2020.1",
                },
                {
                    "name": "Export selection and rename (Foreground)",
                    "execute": export_movie_and_rename_foreground,
                    "minimumVersion": "2020.1",
                },
                {
                    "name": "Export selection and rename (Background)",
                    "execute": export_movie_and_rename_background,
                    "minimumVersion": "2020.1",
                },
                {
                    "name": "Export selection and reimport (Foreground)",
                    "execute": export_movie_and_reimport_foreground,
                    "minimumVersion": "2020.1",
                },
                {
                    "name": "Export selection and reimport (Background)",
                    "execute": export_movie_and_reimport_background,
                    "minimumVersion": "2020.1",
                }
            ]
        }
    ]


def get_main_menu_custom_ui_actions():
    return get_media_panel_custom_ui_actions()


# The main here is used with the python callback method to share code between
# the export hook callback done in Backburner job and the custom UI action done
# in flame.
#
if __name__ == "__main__":
    import sys

    # Call a function from the command line:
    #
    #  exportHook.py <function> <args>
    #
    globals()[sys.argv[1]](*sys.argv[2:])
