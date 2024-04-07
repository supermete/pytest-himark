import json


def pytest_addoption(parser):
    parser.addoption(
        '--json',
        action='store',
        dest='markers_from_json',
        default='',
        help='--json=markers_from_json. Set the path where to look for config.json containing enabled markers declaration.'
    )


def pytest_load_initial_conftests(args):
    json_path = None
    markers_list = list()

    for arg in args:
        if arg.startswith("--json="):
            json_path = arg.replace("--json=", "")

    if json_path is not None:
        with open(json_path, "r") as file:
            config = json.load(file)
            markers = config.get("markers", list())

        # lists the enabled markers
        for marker in markers:
            if markers.get(marker) is True:
                markers_list.append(marker)

    # make an OR of the previously listed enabled markers and pass it with the -m option to the command line
    if len(markers_list) > 0:
        args[:] = ["-m", " or ".join(markers_list)] + args
