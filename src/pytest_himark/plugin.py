import json


def pytest_addoption(parser):
    group = parser.getgroup('himark')
    group.addoption(
        '--json',
        action='store',
        dest='JSON',
        default='',
        help='Set the path where to look for config.json containing enabled markers declaration.'
    )


def pytest_load_initial_conftests(early_config, parser, args):
    group = parser.getgroup('himark')
    json_path = group.options.json

    with open(json_path, "r") as file:
        config = json.load(file)
        hardware = config.get("markers", list())
        metadata = config.get("metadata", list())

    # add metadata from json
    for data in metadata:
        early_config._metadata[data] = metadata.get(data)

    # lists the enabled markers
    hwlist = list()
    for hw in hardware:
        if hardware.get(hw) is True:
            hwlist.append(hw)

    # make an OR of the previously listed enabled markers and pass it with the -m option to the command line
    if len(hwlist) > 0:
        args[:] = ["-m", " or ".join(hwlist)] + args

