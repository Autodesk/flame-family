# CONTRIBUTING

## What can I contribute?

Contributions to this project are encouraged! Here's a list of items you can contribute with:

* Python API / Custom Actions: Provide python snippets that can be loaded into the python console or files using the Flame Family python hooks. You can also propose modifications to existing files.


## Submission Guidelines

### Maintainers

Maintainers are Autodesk employees responsible for responding to pull requests, issues, and for merging.

* Mathieu Sansregret - Maintainer
* Jean-Philippe Brault - Maintainer
* Frédéric Warren- Maintainer
 

### Timing

We will attempt to address all issues and pull requests as soon as possible. There could be a delay at some period of the year.


### Guidelines

Please follow these guidelines

* Please respect the folder hierarchy already in place.
* Give a descriptive name to your script. This is the only text that will appear within the application so this is how users will decide if they want to download it or not.
* Do not hesitate to add as many explanations as possible to your code. This will help maintainers and other users understand what you are trying to achieve.
* Please run your python code through pylint before you submit a pull request to make sure that there are no errors.
 

### Pull Requests

Follow these steps to submit a pull request

* Search GitHub for an open or closed Pull Request that relates to your submission. You don't want to duplicate effort.
* Clone the flame-family repository to your machine using the green button at the top right of the Code tab. This will create a local copy of the repository on your machine.
* Create a new branch using `git checkout origin/master -b my-branch-name`
* Perform `git fetch` (this will update your branch with the latest changes from the repository).
* Perform `git rebase origin/master` (this will re apply your changes to the most recent version of the repository).
* Make your changes in that git branch. Ususally, you will simply need to copy your script in the proper folder and then execute `git add name-of-your-file`
* Commit your changes using `git commit -a`. Add a descriptive commit message. Note: the commit -a command line option will automatically "add" and "rm" edited files. This will open a text editor in which you must give a description of what you are doing.
* Push your branch to GitHub using `git push origin my-branch-name`
* In GitHub, create a pull request for your commit so the maintainers can review it.
 1. Go to the Code tab
 2. Click on Branch
 3. Click on New Pull Request Next to your branch.
* Once approved, your pull request will be merged by one of the maintainers.
