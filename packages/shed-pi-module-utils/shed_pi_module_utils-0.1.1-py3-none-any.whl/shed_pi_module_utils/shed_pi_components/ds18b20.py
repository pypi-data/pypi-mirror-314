import time
from pathlib import Path
from typing import Optional


class TempProbe:
    def __init__(self):
        base_dir = "/sys/bus/w1/devices/"
        device_folder = Path.glob(base_dir + "28*")[0]
        self.device_file = device_folder + "/w1_slave"

    def read_temp_raw(self) -> list[str]:
        with open(self.device_file, "r") as f:
            lines = f.readlines()

        f.close()
        return lines

    def is_data_available(self, lines: list) -> bool:
        return lines[0].strip()[-3:] != "YES"

    def read_temp(self) -> Optional[float]:
        lines = self.read_temp_raw()
        while self.is_data_available(lines):
            time.sleep(0.2)
            lines = self.read_temp_raw()

        equals_pos = lines[1].find("t=")
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2 :]
            temp_c = float(temp_string) / 1000.0
            return temp_c
