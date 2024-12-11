import psutil
import time
from datetime import datetime

class ProcessManager:
    """
    Manages system process operations and information retrieval.
    
    This class handles all process-related operations including:
    - Retrieving process information
    - Building process trees
    - Filtering processes based on various criteria
    - Process termination
    """

    def __init__(self):
        """Initialize the ProcessManager."""
        self.process_list = []
        self.process_cache = {}
        self.cache_timestamp = 0
        self.cache_lifetime = 0.5  # Cache lifetime in seconds
        self.batch_size = 100  # Number of processes to update per batch
        # Initialize CPU monitoring
        try:
            psutil.cpu_percent(interval=None)
        except Exception:
            pass

    def get_processes(self, sort_by='cpu', tree_view=False):
        processes = []
        process_dict = {}
        current_time = time.time()
        
        try:
            # Check if cache is still valid
            if current_time - self.cache_timestamp < self.cache_lifetime:
                process_dict = self.process_cache.copy()
            else:
                # Initialize system-wide CPU monitoring
                psutil.cpu_percent(interval=0.05)  # Reduced interval for responsiveness
                
                # Get all process PIDs first
                all_pids = psutil.pids()
                total_processes = len(all_pids)
                
                # Process in batches
                for start_idx in range(0, total_processes, self.batch_size):
                    batch_pids = all_pids[start_idx:start_idx + self.batch_size]
                    
                    for pid in batch_pids:
                        try:
                            proc = psutil.Process(pid)
                            
                            # Only update processes that aren't in cache or have changed
                            if (pid not in self.process_cache or 
                                not proc.is_running() or 
                                proc.status() != self.process_cache.get(pid, {}).get('status')):
                                
                                # Get process info with proper error handling
                                cpu_percent = proc.cpu_percent(interval=None)
                                mem_percent = proc.memory_percent()
                                
                                # Ensure valid values with smoothing
                                if pid in self.process_cache:
                                    old_cpu = self.process_cache[pid]['cpu_percent']
                                    cpu_percent = (old_cpu + (cpu_percent or 0)) / 2
                                
                                cpu_percent = max(0.0, min(100.0, cpu_percent if cpu_percent is not None else 0.0))
                                mem_percent = max(0.0, min(100.0, mem_percent if mem_percent is not None else 0.0))
                                
                                pinfo = {
                                    'pid': pid,
                                    'name': proc.name(),
                                    'status': proc.status(),
                                    'ppid': proc.ppid(),
                                    'cpu_percent': cpu_percent,
                                    'memory_percent': mem_percent,
                                    'level': 0,
                                    'children': []
                                }
                                process_dict[pid] = pinfo
                            else:
                                # Reuse cached process info
                                process_dict[pid] = self.process_cache[pid].copy()
                                
                        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                            if pid in self.process_cache:
                                del self.process_cache[pid]
                            continue
                        except Exception:
                            continue
                
                # Update cache
                self.process_cache = process_dict.copy()
                self.cache_timestamp = current_time

            if tree_view:
                # Build process tree
                for pid, pinfo in process_dict.items():
                    ppid = pinfo['ppid']
                    if ppid in process_dict:
                        process_dict[ppid]['children'].append(pid)
                
                # Calculate levels and create tree-ordered list
                def add_to_tree(pid, level=0):
                    if pid not in process_dict:
                        return
                    process = process_dict[pid]
                    process['level'] = level
                    processes.append(process)
                    for child_pid in sorted(process['children']):
                        add_to_tree(child_pid, level + 1)
                
                # Start with init process (usually PID 1) and processes without parent
                root_pids = [pid for pid, proc in process_dict.items() 
                            if proc['ppid'] not in process_dict or pid == 1]
                for pid in sorted(root_pids):
                    add_to_tree(pid)
            else:
                processes = list(process_dict.values())

            # Sort processes based on criteria
            if sort_by == 'cpu':
                processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            elif sort_by == 'mem':
                processes.sort(key=lambda x: x['memory_percent'], reverse=True)
            elif sort_by == 'pid':
                processes.sort(key=lambda x: x['pid'])
            elif sort_by == 'name':
                processes.sort(key=lambda x: x['name'].lower())

            return processes
        except Exception as e:
            print(f"Error getting process list: {e}")
            return []

    def filter_processes(self, processes, search_term="", status=None, min_cpu=None, min_memory=None, user_filter=None):
        filtered = processes
        
        # Apply text search filter
        if search_term:
            filtered = [p for p in filtered if search_term.lower() in p['name'].lower() or 
                       str(p['pid']) == search_term]
        
        # Apply status filter
        if status:
            filtered = [p for p in filtered if p['status'] == status]
        
        # Apply CPU threshold filter
        if min_cpu is not None:
            filtered = [p for p in filtered if p['cpu_percent'] >= min_cpu]
        
        # Apply memory threshold filter
        if min_memory is not None:
            filtered = [p for p in filtered if p['memory_percent'] >= min_memory]
        
        # Apply user filter
        if user_filter is not None:
            try:
                filtered = [p for p in filtered if psutil.Process(p['pid']).username() == user_filter]
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return filtered

    def get_process_details(self, pid):
        try:
            proc = psutil.Process(pid)
            return {
                'pid': pid,
                'name': proc.name(),
                'status': proc.status(),
                'cpu_percent': proc.cpu_percent(),
                'memory_percent': proc.memory_percent(),
                'create_time': datetime.fromtimestamp(proc.create_time()).strftime('%Y-%m-%d %H:%M:%S'),
                'username': proc.username(),
                'cmdline': ' '.join(proc.cmdline())
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None

    def terminate_process(self, pid):
        """Terminate a process by PID"""
        try:
            process = psutil.Process(pid)
            process.terminate()
            return True, "Process terminated successfully"
        except psutil.NoSuchProcess:
            return False, "Process not found"
        except psutil.AccessDenied:
            return False, "Permission denied: Cannot terminate process"
        except Exception as e:
            return False, f"Error terminating process: {str(e)}"
