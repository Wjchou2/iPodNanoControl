# iPod Nano Control

Control an iPod nano over Bluetooth from Python on Linux. The project uses
[BlueZ](http://www.bluez.org/) and the Bluetooth AVRCP media-player interface
to discover an iPod, pair and connect to it, and send playback commands.

## Features

- Discover an iPod by its advertised Bluetooth name
- Pair, trust, and connect through BlueZ
- Play, pause, stop, skip forward, and skip backward
- Request shuffle through the media-player interface
- Read playback status, track metadata, position, and equalizer information

## Requirements

- Linux with a working Bluetooth adapter
- BlueZ, including `bluetoothctl`
- `busctl` (normally provided by `systemd`)
- Python 3.9 or newer
- An iPod nano that exposes Bluetooth media controls (Only 7th gen tested, other may not work)

Confirm that the required system commands are available:

```bash
bluetoothctl --version
busctl --version
python3 --version
```

Your user must also have permission to manage Bluetooth devices through BlueZ.

## Installation

Clone the repository and create a virtual environment:

```bash
git clone <repository-url>
cd iPodNanoControl
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
```

The project has no third-party Python dependencies.

> **Note:** The command-line entry point in the current `pyproject.toml` is not
> implemented yet. Use the Python API or run `test.py` as described below.

## How to run

Make sure Bluetooth is enabled and your iPod is powered on, discoverable, and
close to the computer. The first connection may require you to confirm a pairing
request on the iPod or in `bluetoothctl`.

The included example scans for a device whose name contains `iPod`, connects to
it, and repeatedly alternates between play and pause:

```bash
python3 test.py
```

Stop the example with `Ctrl+C`.

## Python usage

```python
import time

from nanobtcontrol import IPodNano


ipod = IPodNano()

if ipod.scan("iPod", timeout=10) is None:
    raise RuntimeError("No matching iPod was found")

print(f"Found {ipod.get_name()} at {ipod.get_mac()}")
ipod.connect()

ipod.play()
time.sleep(5)
ipod.pause()

print("Status:", ipod.status())
print("Track:", ipod.track())
print("Position:", ipod.position())
```

`scan()` performs a Bluetooth scan for the requested number of seconds and
selects the first device whose name contains the supplied text. For a more exact
match, pass the full advertised device name.

## API

| Method | Description |
| --- | --- |
| `scan(name, timeout=10)` | Scan for a device whose advertised name contains `name` |
| `connect()` | Pair if needed, trust the device, and connect to it |
| `get_name()` | Return the discovered device name |
| `get_mac()` | Return the discovered Bluetooth MAC address |
| `play()` | Start or resume playback |
| `pause()` | Pause playback |
| `stop()` | Stop playback |
| `next()` | Skip to the next track |
| `previous()` | Return to the previous track |
| `shuffle()` | Request shuffle through AVRCP |
| `status()` | Return the raw BlueZ playback status |
| `track()` | Return raw BlueZ track metadata |
| `position()` | Return the raw BlueZ playback position |
| `equalizer()` | Return the raw BlueZ equalizer value |

The metadata methods currently return `busctl` output as strings rather than
parsed Python values.

## Troubleshooting

### No iPod is found

- Check that the iPod is discoverable and not already connected elsewhere.
- Run `bluetoothctl devices` to see whether BlueZ can detect it.
- Increase the scan timeout, for example `ipod.scan("iPod", timeout=20)`.
- Use the exact or a distinctive part of the name shown by `bluetoothctl`.

### Pairing or connection fails

Open `bluetoothctl` and try pairing manually:

```text
power on
agent on
default-agent
scan on
pair AA:BB:CC:DD:EE:FF
trust AA:BB:CC:DD:EE:FF
connect AA:BB:CC:DD:EE:FF
```

Replace the example address with your iPod's address. If a stale pairing exists,
remove it from both devices and pair again.

### Media commands fail

The library expects BlueZ to expose the connected device at an AVRCP player path
ending in `/player0`. Verify that the device is connected and supports remote
media control. Some iPod models, firmware versions, or Bluetooth profiles may
not expose every command or property.

## Current limitations

- Linux and BlueZ are required; macOS and Windows are not supported.
- Device selection uses a case-sensitive substring match.
- The first AVRCP player (`player0`) is assumed.
- Disconnect and command-line interfaces are not implemented.
- Command and property support depends on the connected iPod model and firmware.

## Project structure

```text
nanobtcontrol/
  __init__.py     Public package export
  device.py       Discovery, connection, and media-control implementation
test.py           Basic play/pause example
pyproject.toml    Package metadata
```
