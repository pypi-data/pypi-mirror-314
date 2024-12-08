import psutil
import os
import time

class Process:
    def __init__(self, image_name=None, pid=None):
        if image_name:
            self.proc = self._get_process_by_name(image_name)
        elif pid:
            self.proc = self._get_process_by_pid(pid)
        else:
            raise ValueError("Either image_name or pid must be provided.")

    def _get_process_by_name(self, image_name):
        """Find the process by its image name."""
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == image_name.lower():
                return proc
        raise ProcessNotFound(f"Process with image name {image_name} not found.")

    def _get_process_by_pid(self, pid):
        """Find the process by its PID."""
        try:
            return psutil.Process(pid)
        except psutil.NoSuchProcess:
            raise ProcessNotFound(f"Process with PID {pid} not found.")

    def terminate(self, force=False):
        """Terminate the process."""
        try:
            if force:
                self.proc.kill()
            else:
                self.proc.terminate()
            print(f"Process {self.proc.info['name']} (PID {self.proc.pid}) terminated.")
        except psutil.AccessDenied:
            raise AccessDenied(f"Access denied to terminate the process {self.proc.info['name']} (PID {self.proc.pid}).")
        except Exception as e:
            raise Exception(f"Failed to terminate the process {self.proc.info['name']} (PID {self.proc.pid}): {str(e)}")

    def suspend(self, delay=0, stop=0):
        """Suspend the process."""
        if delay != 0:
            time.sleep(delay)
        try:
            self.proc.suspend()
            print(f"Process {self.proc.info['name']} (PID {self.proc.pid}) suspended.")
            if stop != 0:
                time.sleep(stop)
                self.proc.resume()
                print(f"Process {self.proc.info['name']} (PID {self.proc.pid}) resumed after {stop} seconds.")
            else:
                print(f"Process {self.proc.info['name']} (PID {self.proc.pid}) suspended.")
        except psutil.AccessDenied:
            raise AccessDenied(f"Access denied to suspend the process {self.proc.info['name']} (PID {self.proc.pid}).")
        except Exception as e:
            raise Exception(f"Failed to suspend the process {self.proc.info['name']} (PID {self.proc.pid}): {str(e)}")
    
    def resume(self):
        """Resume the process"""
        try:
            self.proc.resume()
            print(f"Process {self.proc.info['name']} (PID {self.proc.pid}) resumed.")
        except psutil.AccessDenied:
            raise AccessDenied(f"Access denied to resume the process {self.proc.info['name']} (PID {self.proc.pid}).")
        except Exception as e:
            raise Exception(f"Failed to resume the process {self.proc.info['name']} (PID {self.proc.pid}): {str(e)}")

    def restart(self, force=False):
        """Restart the process."""
        try:
            self.terminate(force)
            self.proc = psutil.Popen(self.proc.info['exe'])
            print(f"Process {self.proc.info['name']} (PID {self.proc.pid}) restarted.")
        except Exception as e:
            raise ProcessRestartFailed(f"Failed to restart the process {self.proc.info['name']} (PID {self.proc.pid}): {str(e)}")

    def get_pid(self):
        """Get the PID of the process."""
        return self.proc.pid
    
    def get_image_name(self):
        """Get the image name of the process"""
        return self.proc.name

class ProcessNotFound(Exception):
    pass

class AccessDenied(Exception):
    pass

class ProcessRestartFailed(Exception):
    pass

def create_process(image_name):
    """Create a new process."""
    try:
        proc = psutil.Popen(image_name)
        print(f"Process {image_name} created with PID {proc.pid}.")
        return proc
    except Exception as e:
        raise ProcessCreationFailed(f"Failed to create process {image_name}: {str(e)}")

class ProcessCreationFailed(Exception):
    pass
