import json
import pytest

markers_list = set()


@pytest.hookimpl(trylast=True)
def pytest_collection_finish(session):
    print(f"filtered: {len(session.items)} selected")


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config, items):
    option = config.getoption('-m')
    if option is not None:
        markers = option.replace("(", "").replace(")", "")
        markers = list(filter(lambda x: x != '', markers.split(" or ")))

        new_items = list()
        for item in items:
            for marker in item.iter_markers():
                if marker.name not in markers:
                    break
            else:
                new_items.append(item)
        items[:] = new_items


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
    markers_enabled = set()

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
            name = device.get("name", None)
            if device.get("used") is True:
                markers_enabled.add(name)
                # if device is enabled, check its do/di/ai/ao lists existence
                for x in device.get("do", list()):
                    markers_enabled.add(x)
                for x in device.get("di", list()):
                    markers_enabled.add(x)
                for x in device.get("ai", list()):
                    markers_enabled.add(x)
                for x in device.get("ao", list()):
                    markers_enabled.add(x)
                # make a marker for 'type' key if it exists
                if device.get("type", None) is not None:
                    markers_enabled.add(device.get("type"))

        # lists the enabled markers
        for marker in markers:
            if markers.get(marker) is True:
                markers_enabled.add(marker)

    markers_enabled = set(filter(None, markers_enabled))
    markers_list = markers_enabled
    # make an OR of the previously listed enabled markers and pass it with the -m option to the command line
    if len(markers_enabled) > 0:
        args[:] = (["-m", f'({" or ".join(markers_enabled)})'] + args)
