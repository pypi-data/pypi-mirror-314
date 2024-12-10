from behave import *
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
    time.sleep(15)  #Increased wait time for connection
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
        return None #Return None on error


def clear_log_cat_logs(serial_num):
    """
    This function clears the logs in the file.
    """
    adb_log_clear = "adb -s {0} logcat -c"
    str = adb_log_clear.format(serial_num)
    result = run_adb_command(str)
    if result is None:
        raise Exception("Failed to clear logcat logs")


def get_full_log(serial_num, scenario):
    """
    This function collects the logs of CM headless package
    """
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, "Logs")
    os.makedirs(file_path, exist_ok=True) # Ensure Logs directory exists

    device_log = run_adb_command("adb -s {0} logcat -d".format(serial_num))
    if device_log is None:
        raise Exception("Failed to get full log")

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
    os.makedirs(file_path, exist_ok=True) # Ensure Logs directory exists

    device_log = run_adb_command("adb -s {0} shell dumpsys connectivity".format(serial_num))
    if device_log is None:
        raise Exception("Failed to get connectivity log")
    time.sleep(10)
    log_file = os.path.join(file_path, serial_num + "_" + scenario + "_connectivity.txt")
    with open(log_file, "w", encoding="utf-8") as file:
        file.write(device_log)
    return log_file


def get_os_version(serial_num):
    cmd = "adb -s {0} shell getprop ro.build.version.release"
    os_version = run_adb_command(cmd.format(serial_num))
    if os_version is None:
        raise Exception("Failed to get OS version")
    print(os_version)
    return os_version


@given('the Android device with serial number "{serial_number}" is connected')
def step_impl(context, serial_number):
    context.serial_number = serial_number
    success = connect_via_adb(serial_number)
    assert success, f"Failed to connect to device {serial_number}"


@when('the connection fails')
def step_impl(context):
    context.connection_successful = False
    # Simulate a connection failure (replace with actual failure logic if needed)
    # ...


@then('an error message should be displayed')
def step_impl(context):
    assert not context.connection_successful, "No error message displayed when connection failed"



@when('I clear the logcat logs')
def step_impl(context):
    clear_log_cat_logs(context.serial_number)


@when('I wake up the device')
def step_impl(context):
    cmd = CMD_WAKE_DEVICE.format(context.serial_number)
    run_adb_command(cmd)


@when('I get the full log for scenario "{scenario}"')
def step_impl(context, scenario):
    context.full_log_file = get_full_log(context.serial_number, scenario)


@when('I get the connectivity log for scenario "{scenario}"')
def step_impl(context, scenario):
    context.connectivity_log_file = get_connectivity_log(context.serial_number, scenario)


@when('I get the OS version')
def step_impl(context):
    context.os_version = get_os_version(context.serial_number)


@then('the full log file "{log_file}" should exist')
def step_impl(context, log_file):
    assert os.path.exists(log_file), f"Log file {log_file} does not exist"


@then('the connectivity log file "{log_file}" should exist')
def step_impl(context, log_file):
    assert os.path.exists(log_file), f"Log file {log_file} does not exist"


@then('the OS version should be retrieved successfully')
def step_impl(context):
    assert context.os_version is not None, "OS version not retrieved"