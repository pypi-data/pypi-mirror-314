import psutil
from datetime import datetime

class System:
    def __init__(self):
        self.cpu = CPU()

    def get_ram(self):
        """Returns a RAM object to access RAM-related info."""
        return RAM(psutil.virtual_memory().total)

    def get_cpu(self):
        """Returns a CPU object to access CPU-related info."""
        return self.cpu

class RAM:
    def __init__(self, total_bytes):
        self.total_bytes = total_bytes

    def to_mb(self):
        """Converts the total RAM to MB."""
        return self.total_bytes / (1024 ** 2)

    def to_gb(self):
        """Converts the total RAM to GB."""
        return self.total_bytes / (1024 ** 3)

class CPU:
    def __init__(self):
        pass

    def get_cores(self):
        """Gets the number of CPU cores."""
        return psutil.cpu_count(logical=True)

    def get_clock_speed(self):
        """Gets the CPU clock speed in MHz."""
        freq = psutil.cpu_freq()
        return freq.current if freq else None

    def get_uptime(self):
        """Gets the system uptime in seconds."""
        boot_time = psutil.boot_time()
        current_time = datetime.now().timestamp()
        uptime_seconds = current_time - boot_time
        return uptime_seconds
