#README

##Please respect the following guidelines as much as possible:

* Give a meaningful and descriptive name to your file.
* Respect the folder hierarchy as much as possible, but do not hesitate to create a new folder if needed.
* Place your script in the folder associated to the first release in which the script works.
* Always add a docstring in your file and explain what it does.
* Add a minimumVersion and / or maximumVersion properties to all scripts. Please see below for more information.

###Version scoping

Version scoping can be added using the 'minimumVersion' and/or 'maximumVersion' properties to an entire script or a particular custom action.

Entrire script:
To set the minimum scope of a custom action to 2020:
* get_action_custom_ui_actions.minimum_version = "2020"
Hooks that specify a Flame version will only be displayed if the Flame version is equal or greater than the one defined in minimum_version.

To narrow the scope of a custom action to a single version
* get_timeline_custom_ui_actions.minimum_version = "2020"
* get_timeline_custom_ui_actions.maximum_version = "2021"
Hooks that specify a Flame version will only be displayed if the Flame version is equal or greater than the one defined in minimum_version
and equal or smaller than the one defined in maximum_version.

Custom action:

The same properties can be added to the custom action definition in the return section.

    return [
        {
            "name": "Examples / Version Scoping",
            "actions": [
                {
                    "name": "Print Selection",
                    "execute": print_selection,
                    "minimumVersion": "2020",
                    "maximumVersion": "2021"
                }
            ]
        }
    ]