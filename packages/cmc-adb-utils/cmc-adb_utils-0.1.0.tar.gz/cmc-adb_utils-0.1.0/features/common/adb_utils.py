import os
import subprocess
import time

ADB_EXECUTION_WAIT = 3
ADB_DEVICES_SCRIPTS = "adb devices"
CMD_WAKE_DEVICE = "adb -s {0} shell input keyevent 224"


def connect_via_adb(serial_num):
    # Connect to the selected device
    print("Waiting for connection ...")
    connect = os.popen("adb -s " + serial_num + " connect").read()
    time.sleep(15)
    if len(connect) == 0:
        return True
    else:
        return False


def run_adb_command(command: str, wait_time=ADB_EXECUTION_WAIT):
    try:
        process = subprocess.run(
            command.split(),
            check=True,
            stdout=subprocess.PIPE,
            universal_newlines=True,
            errors="ignore",
        )
        # Wait for driver to catch up
        time.sleep(wait_time)
        return process.stdout.strip()
    except subprocess.CalledProcessError as error:
        print(f"Failed to run subprocess command: {error}")


def clear_log_cat_logs(serial_num):
    """
    This function clears the logs in the file.
    """
    adb_log_clear = "adb -s {0} logcat -c"
    str = adb_log_clear.format(serial_num)
    run_adb_command(str)


def get_full_log(serial_num, scenario):
    """
    This function collects the logs of CM headless package
    """
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, "Logs")
    device_log = run_adb_command("adb -s {0} logcat -d".format(serial_num))
    time.sleep(20)
    log_file = os.path.join(file_path, serial_num + "_" + scenario + "_full.txt")
    with open(log_file, "w", encoding="utf-8") as file:
        file.write(device_log)
    return log_file


def get_connectivity_log(serial_num, scenario):
    """
    This function collects the logs of dumpsys connectivity logs
    """
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, "Logs")
    device_log = run_adb_command("adb -s {0} shell dumpsys connectivity".format(serial_num))
    time.sleep(10)
    log_file = os.path.join(file_path, serial_num + "_" + scenario + "_connectivity.txt")
    with open(log_file, "w", encoding="utf-8") as file:
        file.write(device_log)
    return log_file


def get_os_version(serial_num):
    cmd = "adb -s {0} shell getprop ro.build.version.release"
    os_version = run_adb_command(cmd.format(serial_num))
    print(os_version)
    return os_version
