import re
import time
from behave import *

from features.common.adb_utils import run_adb_command, connect_via_adb, clear_log_cat_logs, get_full_log, get_connectivity_log


@given('devices are connected')
def get_connected_devices(context):
    formatted_devices_list = []
    connected_devices = run_adb_command('adb devices')
    connected_devices_list = [
        i.split("\t")[0] for i in connected_devices.split("\n")[1:]
    ]
    formatted_devices_list.extend(connected_devices_list)
    successful_list = list()
    for device in formatted_devices_list:
        try:
            result = connect_via_adb(device)
            if not result:
                raise Exception(f"Failed to connect to device: {device}")
            else:
                successful_list.append(device)
        except Exception as e:
            print(f"Error connecting to device: {device} - {e}")
    context.devices = successful_list
    assert len(successful_list) > 0, "No connected devices"


@given('IMEI is present')
def get_imei(context):
    print("begin get_imei")
    device = context.devices[0]
    output = run_adb_command(f"adb -s {0} shell content query --uri content://com.spectrum.cm.headless.library.providers.LibraryServiceProvider/getDynamicImeis".format(device))
    if 'Row: 0 =' in output and (substring := output.split('=')[1].strip()):
        imei_list = [part.split('=')[1].strip() for part in output.split('Row:') if '=' in part]
        integer_list = [int(x) for x in imei_list[0].split(', ')]
        for imei in integer_list:
            context.imei = imei
            break
    print("imei=" + str(context.imei))
    print("end get_imei")
    assert device, "IMEI not available"


@when('logs are clear')
def clear_logs(context):
    device = context.devices[0]
    print("begin clear_logs via adb command")
    clear_log_cat_logs(device)
    print("end clear_logs via adb")


@when('data is cleared')
def clear_data(context):
    device = context.devices[0]
    print("begin clear_data via adb command")
    cmd1 = "adb -s {0} shell pm clear com.spectrum.cm.headless"
    run_adb_command(cmd1.format(device))
    print("end clear_data via adb command")


@when('device is registered')
def device_is_registered(context):
    device = context.devices[0]
    print("begin device_is_registered")
    output = run_adb_command("adb -s {0} shell content query --uri content://com.spectrum.cm.headless.library.providers.LibraryServiceProvider/isRegistered".format(device))
    if 'Row: 0 =' in output and (substring := output.split('=')[1].strip()):
        print(output)
    print("end device_is_registered")


@when('device reboots')
def device_reboots(context):
    device = context.devices[0]
    print("begin device_reboots via adb command")
    cmd = "adb -s {0} reboot"
    run_adb_command(cmd.format(device))
    print("end device_reboots via adb command")


@when('cmc is killed')
def cmc_is_killed(context):
    device = context.devices[0]
    print("begin kill cmc via adb command")
    cmd = "adb -s {0} shell am kill com.spectrum.cm.headless"
    run_adb_command(cmd.format(device))
    print("end kill cmc via adb command")


# @when('install cmc')
# def install_cmc(context):
#     print('Install apk')
#     airlytics_aut = get_aut_path("sok_android")
#     device_name = context.connected_devices[0]
#     cmd1 = "adb -s " + str(device_name) + " install -r -d " + airlytics_aut + "Logs/363.apk"
#     print(cmd1)
#     run_adb_command(cmd1.format(device_name))
#     time.sleep(10)


@then('wait 10')
def wait_10(context):
    time.sleep(10)


@then('wait 120')
def wait_120(context):
    time.sleep(120)


@then('turn wifi off')
def turn_wifi_off(context):
    device = context.devices[0]
    print("begin turn_wifi_off via adb")
    cmd = "adb -s {0} shell svc wifi disable"
    run_adb_command(cmd.format(device))
    wait_10(context)
    status = check_internet_connection(device)
    print("end turn_wifi_off via adb")
    assert status == "0", "Wifi not off and it should be"


@then('turn wifi on')
def turn_wifi_on(context):
    device = context.devices[0]
    print("begin turn_wifi_on via adb")
    cmd = "adb -s {0} shell svc wifi enable"
    run_adb_command(cmd.format(device))
    status = check_internet_connection(context)
    print("end turn_wifi_on via adb")
    assert status == "1", "Wifi not on and it should be"


@then('turn cell off')
def turn_cell_off(context):
    device = context.devices[0]
    print("begin turn_cell_off via adb")
    cmd = "adb -s {0} shell svc data disable"
    run_adb_command(cmd.format(device))
    # TODO what to verify here
    # status = check_internet_connection()
    print("end turn_cell_off via adb")
    # assert status == "0", "Wifi not off"


@then('turn cell on')
def turn_cell_on(context):
    device = context.devices[0]
    print("begin turn_cell_on via adb")
    cmd = "adb -s {0} shell svc data enable"
    run_adb_command(cmd.format(device))
    # TODO what to verify here
    # status = check_internet_connection()
    print("end turn_cell_on via adb")
    # assert status == "1", "Wifi not on"


@when('start cmc')
def start_cmc(context):
    device = context.devices[0]
    print("start cmc application")
    # device_name = context.connected_devices[0]
    cmd = "adb -s {0} shell content query --uri content://com.spectrum.cm.ServiceProvider/start_service"
    output = run_adb_command(cmd.format(device))
    print(output)
    time.sleep(10)


@when('stop cmc')
def stop_cmc(context):
    device = context.devices[0]
    print("stop cmc application")
    cmd = "adb -s {0} shell content query --uri content://com.spectrum.cm.ServiceProvider/stop_service"
    output = run_adb_command(cmd.format(device))
    print(output)
    print("cm client stopped")


# @then('validate cmc started')
# def validate_cmc_is_running(context):
#     test_passed = True
#     device_name = context.connected_devices[0]
#     cmd1 = "adb -s " + str(device_name) + " shell content query --uri content://com.spectrum.cm.ServiceProvider/query_service"
#     output = run_adb_command(cmd1)
#     print(output)
#     if "status=1" not in output:
#         test_passed = False
#     time.sleep(5)
#     assert test_passed, "CM did not start successfully"
#
#
# @then('validate cmc stopped')
# def validate_cmc_is_stopped(context):
#     test_passed = True
#     device_name = context.connected_devices[0]
#     cmd1 = "adb -s " + str(device_name) + " shell content query --uri content://com.spectrum.cm.ServiceProvider/query_service"
#     output = run_adb_command(cmd1)
#     print(output)
#     if "status=0" not in output:
#         test_passed = False
#     time.sleep(5)
#     assert test_passed, "CM did not stop successfully"


@then('run you tube')
def run_you_tube(context):
    device = context.devices[0]
    print("begin run_you_tube")
    cmd = 'adb -s {0} shell am start https://www.youtube.com/watch?v=rUxyKA_-grg&feature=share'
    output = run_adb_command(cmd.format(device))
    print(output)
    print("end run_you_tube")


@then('stop you tube')
def stop_you_tube(context):
    device = context.devices[0]
    print("begin stop_you_tube")
    cmd = 'adb -s {0} shell am force-stop com.google.android.youtube'
    output = run_adb_command(cmd.format(device))
    print(output)
    print("end stop_you_tube")


def check_internet_connection(context):
    device = context.devices[0]
    cmd = "adb -s {0} shell dumpsys wifi | grep \"Wi-Fi is\""
    output = run_adb_command(cmd.format(device))
    print(output)
    if "disabled" in output:
        return "0"
    else:
        return "1"


@then('gather full log')
def gather_full_log(context):
    device = context.devices[0]
    print("begin gather_log")
    full_scenario_name = context.scenario.name
    name = full_scenario_name.split('--')[0].strip()
    dump_path = get_full_log(str(device), str(name))
    context.full_log = dump_path
    print(dump_path)
    print("end gather_log")


@then('gather connectivity log')
def gather_connectivity_log(context):
    device = context.devices[0]
    print("begin gather_connectivity_log")
    dump_path = get_connectivity_log(str(device), str(context.scenario.name))
    context.connectivity_log = dump_path
    print(dump_path)
    print("end gather_connectivity_log")


def find_log_statements(full_log_path, assert_statements):
    not_found_list = []
    for assert_statement in assert_statements:
        with open(full_log_path, "r") as log_data:
            if assert_statement not in log_data.read():
                not_found_list.append(assert_statement)
    return not_found_list


def validate_logs_by_count(full_log_path, log_dict):
    result_list = []
    assert_statements = log_dict['logs']
    assert_counts = log_dict['counts']
    pos = 0
    for assert_statement in assert_statements:
        with open(full_log_path, "r") as log_data:
            the_lines = log_data.readlines()
            count = 0
            for line in the_lines:
                if assert_statement in line:
                    count += 1
        supposed_count = assert_counts[pos]
        pos = pos + 1
        if count != supposed_count:
            result_item = dict()
            result_item['key'] = assert_statement
            result_item['expected'] = supposed_count
            result_item['actual'] = count
            result_list.append(result_item)
    return result_list
