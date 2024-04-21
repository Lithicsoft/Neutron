from datetime import datetime
import threading
from log.write import sys_log
from search import index
from manager import manager
import run_app

def run_module(module):
    module.main()

def start_server():
    sys_log('Start Server', str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
    modules = [index, manager, run_app]

    threads = [threading.Thread(target=run_module, args=(module,)) for module in modules]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    start_server()