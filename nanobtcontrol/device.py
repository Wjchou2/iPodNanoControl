import subprocess
import time


class IPodNano:
    def __init__(self):
        self.mac = None
        self.name = None
        self.player_path = None

    def scan(self, name, timeout=10):
        subprocess.run(["bluetoothctl", "scan", "on"], check=True)
        time.sleep(timeout)
        result = subprocess.run(
            ["bluetoothctl", "devices"], capture_output=True, text=True
        )
        subprocess.run(["bluetoothctl", "scan", "off"])
        for line in result.stdout.splitlines():
            print(line)
            if name in line:
                parts = line.split(" ", 2)
                self.mac = parts[1]
                self.name = parts[2]
                return self
        return None

    def connect(self):
        if self.mac is None:
            raise RuntimeError("No device selected. Scan first")
        commands = f"""
        trust {self.mac}
        pair {self.mac}
        connect {self.mac}
        quit
        """
        subprocess.run(["bluetoothctl"], input=commands, text=True, check=True)
        self.player_path = (
            "/org/bluez/hci0/dev_" + self.mac.replace(":", "_") + "/player0"
        )

    def play(self):
        self._command("Play")

    def pause(self):
        self._command("Pause")

    def next(self):
        self._command("Next")

    def previous(self):
        self._command("Previous")

    def stop(self):
        self._command("Stop")

    def status(self):
        return self._get("Status").split('"')[1]

    def track(self):
        return self._get("Track").split('"')[1]

    def position(self):
        return int(self._get("Position").split()[1])

    def _command(self, cmd):
        subprocess.run(
            [
                "busctl",
                "call",
                "org.bluez",
                self.player_path,
                "org.bluez.MediaPlayer1",
                cmd,
            ],
            check=True,
            capture_output=True,
            text=True,
        )

    def _get(self, get):
        return subprocess.run(
            [
                "busctl",
                "get-property",
                "org.bluez",
                self.player_path,
                "org.bluez.MediaPlayer1",
                get,
            ],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
