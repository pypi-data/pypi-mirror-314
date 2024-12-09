import subprocess
import psutil
import json
import os

class WARPRouter:
    def __init__(self):
        self.excluded_processes = set()
        self.config_file = "warp_config.json"
        self.load_config()
    
    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.excluded_processes = set(config.get('excluded_processes', []))
        except FileNotFoundError:
            self.excluded_processes = set()
    
    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump({
                'excluded_processes': list(self.excluded_processes)
            }, f)
    
    def get_user_processes(self):
        processes = {}
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                pid = proc.pid
                if pid >= 1000:
                    processes[pid] = {
                        'name': proc.name(),
                        'pid': pid,
                        'excluded': str(pid) in self.excluded_processes
                    }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return processes
    
    def exclude_process(self, pid):
        self.excluded_processes.add(str(pid))
        self.save_config()
    
    def include_process(self, pid):
        self.excluded_processes.discard(str(pid))
        self.save_config()
    
    def set_process_state(self, pid, excluded):
        if excluded:
            self.exclude_process(pid)
        else:
            self.include_process(pid)
    
    def apply_configuration(self):
        try:
            subprocess.run(['warp-cli', 'tunnel', 'ip', 'reset'], 
                         check=True, capture_output=True, text=True)
            
            if not self.excluded_processes:
                return True, "All traffic going through WARP"
            
            subprocess.run(['warp-cli', 'tunnel', 'ip', 'add-range', '0.0.0.0/0'],
                         check=True, capture_output=True, text=True)
            
            return True, "Configuration applied successfully"
            
        except subprocess.CalledProcessError as e:
            return False, f"Failed to apply configuration: {e.stderr}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_warp_status(self):
        try:
            result = subprocess.run(['warp-cli', 'status'], 
                                  capture_output=True, text=True)
            return True, result.stdout.strip()
        except Exception as e:
            return False, str(e)
    
    def reset_configuration(self):
        self.excluded_processes.clear()
        self.save_config()
        return self.apply_configuration()