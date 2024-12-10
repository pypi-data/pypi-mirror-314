


def load_db():
    return get_db_dict()


def get_log_statements_for_scenario(scenario):
    return get_by_key(scenario)


def get_by_key(key):
    the_dict = get_db_dict()
    return the_dict.get(key)


def get_db_dict():
    local_dict = dict()
    local_dict['SO4001'] = get_SO4001_dict()
    local_dict['SO4002'] = get_SO4002_dict()
    local_dict['SO4003'] = get_SO4003_dict()
    local_dict['SO4004'] = get_SO4001_dict()
    local_dict['SO4005'] = get_SO4002_dict()
    local_dict['SO4006'] = get_SO4003_dict()
    return local_dict


def get_SO4001_dict():
    local_dict = dict()
    local_log_list = list()
    local_log_list.append("startHomeRouterJob called")
    local_log_list.append("WorkSchedulingManager Initialized enqueued worker service  is : Home Router Service")
    local_log_list.append("In HomeRouterWorkerService doWork()")
    local_log_list.append("Calling InHomeRouter API...")
    local_log_list.append("POST https://device-qa.cmdev.spectrum.net/device/5.0.0/in-home-router")
    local_log_list.append("200 https://device-qa.cmdev.spectrum.net/device/5.0.0/in-home-router")
    local_log_list.append("InHomeRouter API response=true")
    local_log_list.append("CmSmfo event")
    local_dict['logs'] = local_log_list
    local_dict['counts'] = [1,1,1,1,2,2,1,1]
    return local_dict


def get_SO4002_dict():
    local_dict = dict()
    local_log_list = list()
    local_log_list.append("startHomeRouterJob called")
    local_log_list.append("WorkSchedulingManager Initialized enqueued worker service  is : Home Router Service")
    local_log_list.append("In HomeRouterWorkerService doWork()")
    local_log_list.append("Calling InHomeRouter API...")
    local_log_list.append("POST https://device-qa.cmdev.spectrum.net/device/5.0.0/in-home-router")
    local_log_list.append("403 https://device-qa.cmdev.spectrum.net/device/5.0.0/in-home-router")
    local_log_list.append("InHomeRouter API response=true")
    local_log_list.append("CmSmfo event")
    local_dict['logs'] = local_log_list
    local_dict['counts'] = [1,1,1,1,2,2,0,0]
    return local_dict


def get_SO4003_dict():
    local_dict = dict()
    local_log_list = list()
    local_log_list.append("startHomeRouterJob called")
    local_log_list.append("WorkSchedulingManager Initialized enqueued worker service  is : Home Router Service")
    local_log_list.append("In HomeRouterWorkerService doWork()")
    local_log_list.append("Calling InHomeRouter API...")
    local_log_list.append("POST https://device-qa.cmdev.spectrum.net/device/5.0.0/in-home-router")
    local_log_list.append("403 https://device-qa.cmdev.spectrum.net/device/5.0.0/in-home-router")
    local_log_list.append("InHomeRouter API response=false")
    local_log_list.append("Connection Manager stopped")
    local_log_list.append("Home Router Service  still not scheduled")
    local_log_list.append("Home Router Service Daily  still not scheduled")
    local_dict['logs'] = local_log_list
    local_dict['counts'] = [1, 1, 1, 1, 2, 2, 1, 1, 3, 2]
    return local_dict
