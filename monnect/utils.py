import subprocess


def get_displays():
    output = subprocess.check_output(
        ["system_profiler", "SPDisplaysDataType"]
    ).decode()

    displays = []
    capture = False

    for line in output.splitlines():
        stripped = line.strip()

        # Start capturing after we hit "Displays:"
        if stripped == "Displays:":
            capture = True
            continue

        if capture:
            # Display names end with ":" and are not resolution lines
            if stripped.endswith(":") and "Resolution" not in stripped:
                name = stripped.replace(":", "")
                displays.append(name)

    return list(dict.fromkeys(displays))  # remove duplicates while preserving order


def get_paired_devices():
    output = subprocess.check_output(
        ["blueutil", "--paired", "--format", "json"]
    ).decode()

    import json
    devices_json = json.loads(output)

    devices = []
    for device in devices_json:
        name = device.get("name")
        mac = device.get("address")
        if name and mac:
            devices.append((name, mac))

    return devices
