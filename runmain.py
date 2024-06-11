import os
import sys
from multiprocessing import Process

def add_project_to_sys_path():
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if root_path not in sys.path:
        sys.path.append(root_path)

def start_user_service():
    add_project_to_sys_path()
    from user_microservices.run import run_user_http
    print("Starting User Service")
    run_user_http()

def start_report_service():
    add_project_to_sys_path()
    from report_microservices.run import run_report_http
    print("Starting Report Service")
    run_report_http()

def start_invoice_service():
    add_project_to_sys_path()
    from invoice_microservices.run import run_invoice_http
    print("Starting Invoice Service")
    run_invoice_http()

def start_building_service():
    add_project_to_sys_path()
    from building_microservices.run import run_building_http
    print("Starting Building Service")
    run_building_http()

def run_service(service_func):
    process = Process(target=service_func)
    process.start()
    return process

if __name__ == '__main__':
    user_process = run_service(start_user_service)
    report_process = run_service(start_report_service)
    invoice_process = run_service(start_invoice_service)
    building_process = run_service(start_building_service)  # Start the new service

    # Optionally join processes if you want to wait for them
    user_process.join()
    report_process.join()
    invoice_process.join()
    building_process.join()  # Join the new service process
