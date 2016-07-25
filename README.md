# NonSomeFinder

## Installation

1. Clone my fork of PyGithub at https://github.com/tomibgt/PyGithub
2. Add PyGithub to your python includes (e.g. something like `export PYTHONPATH="/home/bgt/git/PyGithub/"`)
3. Clone this repository to your local system.
4. Copy the file NonSomeFinder/src/config.cfg.template as NonSomeFinder/src/config.cfg – This new file is in the git ignore. Edit it and put your own GitHub creditentials there.
5. run `python [path/here/NonSomeFinder/src/]NonSomeFinder.py`

## ToDo

Currently there is no clean termination for delegated setups.

## Usage Examples

### python NonSomeFinder.py -facebook outputfile.csv

This command searches GitHub for projects that appear to use the Facebook Graph API. All projects are listed in the *outputfile.csv*, with an indicator of true or false, wether Graph API was detected.

### python NonSomeFinder.py -facebook -since 1549311 -delegate first.delegate,second.delegate

This command also searches GitHub projects starting of project ID *1549311*, but instead of analysing the projects itself, it delegates the projects to files *first.delegate* and *second.delegate*.
The *-facebook* flag is required, because otherwise the command would expect a search phrase to be sought for in the projects.
(The search phrase would be passed on to GitHub API as a parameter to filter out search results.)

The delegation files are only pushed new projects, when they have less than 20 projects in them already.
If the delegates are slow, the delegator will wait for a delegate file to have room again.

### python NonSomeFinder.py -facebook -takeover first.delegate outputfile.csv

This command takes over the analysis of projects delegated to the file *first.delegate* and produces output in *outputfile.csv*.
The command pops repositories from the delegation file, as it has analysed them.

