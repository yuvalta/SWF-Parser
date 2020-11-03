import json
import plot_data
import os
from datetime import datetime, date
from RowClass import RowClass

# datetime, order, submit_time, runtime, number_of_nodes, user_id, group_id,
# application_id, number_of_queues, wait_time=0, average_cpu_time=-1, average_memory_per_node=-1,
# requested_processors=-1, requested_runtime=-1, requested_memory=-1, status=-1, number_of_partitions=-1,
# preceding_job_number=-1, think_time=-1

original_log_path = "log_files/NASA-iPSC-1993-0.txt"
SWF_log = "log_files/SWF_log.txt"
SWF_log_analyse = "log_files/SWF_log_analyse.txt"

if os.path.isfile(SWF_log):  # delete SWF file if already exists
    os.remove(SWF_log)

if os.path.isfile(SWF_log_analyse):  # delete SWF analyse file if already exists
    os.remove(SWF_log_analyse)

log_file = open(original_log_path, "r")

row_counter = 1

first_row = log_file.readline()
log_file.seek(0)

started_time = datetime.strptime(first_row.split()[4] + " " + first_row.split()[5], "%m/%d/%y %H:%M:%S")

job_size_dict = {}  # dictionary for job sizes
users_dict = {}  # dictionary for all users ('user_name', [user_id, number of times user shown])
users_id_counter = 1

with open(SWF_log, "w") as swf_file:  # for each row in the trace - create file with the formatted log
    for row in log_file.readlines():

        row_split_list = row.split()

        date_and_time = datetime.strptime(row_split_list[4] + " " + row_split_list[5], "%m/%d/%y %H:%M:%S")

        submit_time = datetime.combine(date.today(), date_and_time.time()) - datetime.combine(date.today(),
                                                                                              started_time.time())  # subtract current time from start time to get time from beginning
        runtime = row_split_list[3]

        # manage the users dictionary
        user_name = row_split_list[0]
        user_id = users_dict.get(user_name, -1)
        if user_id == -1:  # new user
            users_dict[user_name] = [users_id_counter, 1]
            user_id = users_id_counter
            users_id_counter += 1
        else:  # if user already shown
            new_user_occurrences_array = users_dict.get(user_name)
            users_dict[user_name] = [new_user_occurrences_array[0], new_user_occurrences_array[1] + 1]

        # manage the job size dictionary
        number_of_nodes = row_split_list[2]
        # if number_of_nodes != "S" or number_of_nodes != "D" or number_of_nodes != "H":  # ignore special keys in log -> 'CUBE' application
        number_of_nodes_key = job_size_dict.get(number_of_nodes, -1)
        if number_of_nodes_key == -1:  # new job size
            job_size_dict[number_of_nodes] = 1
        else:
            job_size_dict[number_of_nodes] = int(str(job_size_dict.get(number_of_nodes))) + 1

        if str.__contains__(user_name, "user"):  # set group
            group_id = 1
        else:  # sysadmin
            group_id = 2

        application_id = row_split_list[1]

        number_of_queues = 1

        current_row = RowClass(date_and_time, row_counter, submit_time.seconds, runtime, number_of_nodes,
                               users_dict[user_name][0],
                               group_id, application_id, number_of_queues)

        swf_file.write(current_row.convert_to_string())

        row_counter += 1

with open(SWF_log_analyse, "w") as SWF_log_analyse:  # create file with analysis
    SWF_log_analyse.write("# 'user_name', [user_id, number of times user shown] \n\n")
    SWF_log_analyse.write(json.dumps(users_dict, indent=4))

    SWF_log_analyse.write("\n\n\n\n# Number of nodes in job, number of times \n\n")
    SWF_log_analyse.write(json.dumps(job_size_dict, indent=4))

plot_data.plot_users_dict(users_dict)
plot_data.plot_jobs_dict(job_size_dict)
