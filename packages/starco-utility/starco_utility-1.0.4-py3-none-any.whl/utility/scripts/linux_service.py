#!/usr/bin/env python3
import os
import sys
import subprocess


def create_service_file(service_name, exec_path, WorkingDirectory, description=""):
    service_content = f"""[Unit]
Description={description if description else service_name}
After=network.target

[Service]
Type=simple
ExecStart={exec_path}
Restart=always
RestartSec=3
User=root
Group=root
WorkingDirectory={WorkingDirectory}
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier={service_name}

[Install]
WantedBy=multi-user.target
"""

    service_file_path = f"/etc/systemd/system/{service_name}.service"

    try:
        with open(service_file_path, 'w') as f:
            f.write(service_content)
        print(f"Service file created at {service_file_path}")
        return True
    except PermissionError:
        print("Error: Need root privileges to create service file")
        return False
    except Exception as e:
        print(f"Error creating service file: {str(e)}")

        return False


def enable_service(service_name):
    try:
        subprocess.run(
            ['systemctl', 'enable', f'{service_name}.service'], check=True)
        print(f"Service {service_name} enabled successfully")
        return True
    except subprocess.CalledProcessError:
        print(f"Error enabling service {service_name}")
        return False


def start_service(service_name):
    try:
        subprocess.run(
            ['systemctl', 'start', f'{service_name}.service'], check=True)
        print(f"Service {service_name} started successfully")
        return True
    except subprocess.CalledProcessError:
        print(f"Error starting service {service_name}")
        return False


def main():
    if os.geteuid() != 0:
        print("This script must be run as root!")
        sys.exit(1)

    while True:
        print("\nLinux Service Manager")
        print("1. Create Service")
        print("2. Enable Service")
        print("3. Start Service")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            service_name = input("Enter service name: ")
            exec_path = input("Enter full path to executable: ")
            WorkingDirectory = input("Enter Working Directory: ")
            description = input("Enter service description (optional): ")
            create_service_file(service_name, exec_path,
                                WorkingDirectory, description)

        elif choice == "2":
            service_name = input("Enter service name: ")
            enable_service(service_name)

        elif choice == "3":
            service_name = input("Enter service name: ")
            start_service(service_name)

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
