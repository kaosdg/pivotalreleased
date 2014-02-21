pivotalmakerelease
==================

Using Pivotal Tracker and need to generate Release Notes? Try this script.

The concept behind this Python script is to read Pivotal Tracker stories for completion and extrapolate Releases. Share
these release notes with the client.

Original python script generously shared by Houssam (Sam) Kawtharani at PT's GetSatisfaction forum:
http://community.pivotaltracker.com/pivotal/topics/release_notes_generation
under a "Release Notes Generation" thread.

##Usage
```
usage: pivotalmakerelease [-h] [-c CONFIG] [-o OFILE] [-f FORMAT]
                          [--no-footer]
                          project

Create release notes for a given Pivotal Tracker Project

positional arguments:
  project               The Project ID that you want to create release notes
                        for.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        The configuration file to use [pivotal.config by
                        default]
  -o OFILE, --ofile OFILE
                        The output file to write to [stdout by default]
  -f FORMAT, --format FORMAT
                        The output format you wish to use.
  --no-footer           Whether or not to include the footer

```

## Updates
Updated to use the latest Pivotal JSON API, added some options and config, and output in Github MD format
