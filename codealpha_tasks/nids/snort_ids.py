#!/usr/bin/env python3
import subprocess
import threading
import time
import os

# Configure these variables as needed
INTERFACE = "eth0"  # Change to your network interface name
SNORT_CONFIG = "/etc/snort/snort.conf"
ALERT_LOG = "/var/log/snort/alert"

def run_snort():
    """
    Launch Snort in fast alert mode quietly.
    """
    snort_cmd = [
        "snort",
        "-A", "fast",      # Use fast alert mode
        "-q",              # Quiet mode
        "-c", SNORT_CONFIG,  # Specify the Snort configuration file
        "-i", INTERFACE    # Specify the interface to monitor
    ]
    # Using Popen to allow asynchronous monitoring
    print(f"Starting Snort on interface {INTERFACE}...")
    return subprocess.Popen(snort_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def monitor_alerts(alert_file):
    """
    Tails the alert file and prints new alerts as they are appended.
    """
    # Wait until the alert file exists
    while not os.path.exists(alert_file):
        print(f"Waiting for alert file: {alert_file}...")
        time.sleep(1)

    # Open the alert file and seek to the end
    with open(alert_file, "r") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if line:
                print(f"[ALERT] {line.strip()}")
            else:
                time.sleep(1)

def main():
    # Start Snort
    snort_proc = run_snort()
    
    # Start the alert monitor thread
    monitor_thread = threading.Thread(target=monitor_alerts, args=(ALERT_LOG,), daemon=True)
    monitor_thread.start()

    try:
        while True:
            # Check if Snort is still running
            if snort_proc.poll() is not None:
                stdout, stderr = snort_proc.communicate()
                print("Snort process terminated.")
                if stdout:
                    print("STDOUT:", stdout.decode())
                if stderr:
                    print("STDERR:", stderr.decode())
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Terminating Snort...")
        snort_proc.terminate()
        snort_proc.wait()
        print("Snort terminated.")

if __name__ == "__main__":
    main()
