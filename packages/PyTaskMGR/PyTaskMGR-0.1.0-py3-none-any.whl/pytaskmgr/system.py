import psutil

class System:
    def __init__(self):
        self.cpu = CPU()

    def get_ram(self):
        """Get the total system RAM in MB."""
        ram = psutil.virtual_memory().total / (1024 ** 2)
        return ram

    def get_cpu(self):
        """Return a CPU object to access CPU-related info."""
        return self.cpu

class CPU:
    def __init__(self):
        pass

    def get_cores(self):
        """Get the number of CPU cores."""
        return psutil.cpu_count(logical=True)

    def get_clock_speed(self):
        """Get the CPU clock speed in MHz."""
        # Fetching the current CPU frequency
        freq = psutil.cpu_freq()
        return freq.current

    def get_uptime(self):
        """Get the system uptime."""
        # System uptime in seconds
        uptime_seconds = psutil.boot_time()
        # Convert uptime to human-readable format
        return uptime_seconds

