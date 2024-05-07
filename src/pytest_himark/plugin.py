import json

markers_list = set()


def pytest_addoption(parser):
    group = parser.getgroup("himark")
    group.addoption(
        '--json',
        action='store',
        dest='markers_from_json',
        default='',
        help='--json=markers_from_json. Set the path of the json containing enabled markers declaration.'
    )


def pytest_configure(config):
    for marker in markers_list:
        config.addinivalue_line(
            "markers", f"{marker}: Enable if supported."
        )
        

def pytest_load_initial_conftests(args):
    global markers_list
    json_path = None
    devices_enabled = set()
    markers_enabled = set()
    markers_disabled = set()

    for arg in args:
        if arg.startswith("--json="):
            json_path = arg.replace("--json=", "")

    if json_path is not None:
        with open(json_path, "r") as file:
            config = json.load(file)
            devices = config.get("devices", list())
            markers = config.get("markers", list())

        # lists the enabled devices and turn them into markers
        for device in devices:
            if devices.get(device).get("used") is True:
                markers_enabled.add(device)
                # if device is enabled, check its outputs/inputs existence
                for o in devices.get(device).get("outputs", list()):
                    markers_enabled.add(o)
                for i in devices.get(device).get("inputs", list()):
                    markers_enabled.add(i)
            else:
                markers_disabled.add(device)

        # lists the enabled markers
        for marker in markers:
            if markers.get(marker) is True:
                markers_enabled.add(marker)
            else:
                markers_disabled.add(marker)

    markers_enabled = set(filter(None, markers_enabled))
    markers_list = markers_enabled.union(markers_disabled)
    # make an OR of the previously listed enabled markers and pass it with the -m option to the command line
    if len(markers_enabled) > 0:
        args[:] = (["-m",
                   (f'({" or ".join(markers_enabled)})' if len(markers_enabled) > 0 else '') +
                   (' and ' if len(markers_enabled) > 0 and len(markers_disabled) > 0 else '') +
                   (f'not ({" or ".join(markers_disabled)})' if len(markers_disabled) > 0 else '')]
                   + args)
