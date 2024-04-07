# Welcome to pytest-himark

A plugin that reads a config.json file in your test root directory, searches the 'markers' key, lists the markers declared as 'true' as enabled markers and automatically adds -m option to the command line with an OR on the enabled markers.
