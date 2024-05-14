import sys
import os
from multiprocessing import Process

# Add the project directory to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.append(root_path)

# Import services
from user_microservices.run import run_http as run_user_http
from report_microservices.run import run_http as run_report_http
from invoice_microservices.run import run_http as run_invoice_http

def run_service(service_func):
    process = Process(target=service_func)
    process.start()
    return process

if __name__ == '__main__':
    user_process = run_service(run_user_http)
    report_process = run_service(run_report_http)
    invoice_process = run_service(run_invoice_http)

    # Optionally join processes if you want to wait for them
    user_process.join()
    report_process.join()
    invoice_process.join()
