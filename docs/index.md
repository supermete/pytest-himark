# Welcome to pytest-himark

A plugin that will filter pytest's test collection using a json file.  
It will read a json file provided with a --json argument in pytest command line  
(or in pytest.ini), search the *markers* key and automatically add -m option to  
the command line for filtering out the tests marked with disabled markers.
