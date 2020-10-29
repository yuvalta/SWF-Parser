from shutil import copyfile, copy
import os
from datetime import datetime, date
from RowClass import RowClass

# datetime, order, submit_time, runtime, number_of_nodes, user_id, group_id,
# application_id, number_of_queues, wait_time=0, average_cpu_time=-1, average_memory_per_node=-1,
# requested_processors=-1, requested_runtime=-1, requested_memory=-1, status=-1, number_of_partitions=-1,
# preceding_job_number=-1, think_time=-1

original_log_path = "log_files/NASA-iPSC-1993-0.txt"
SWF_log = "log_files/SWF_log.txt"

if os.path.isfile(SWF_log):  # delete SWF file if already exists
    os.remove(SWF_log)

# copyfile(original_log_path, SWF_log)

log_file = open(original_log_path, "r")

row_counter = 1

first_row = log_file.readline()
started_time = datetime.strptime(first_row.split()[4] + " " + first_row.split()[5], "%m/%d/%y %H:%M:%S")

print(started_time)

with open(SWF_log, "w") as swf_file:
    for row in log_file.readlines():

        row_split_list = row.split()

        date_and_time = datetime.strptime(row_split_list[4] + " " + row_split_list[5], "%m/%d/%y %H:%M:%S")

        submit_time = datetime.combine(date.today(), date_and_time.time()) - datetime.combine(date.today(),
                                                                                              started_time.time())  # subtract current time from start time to get time from beginning
        runtime = row_split_list[3]

        number_of_nodes = row_split_list[2]

        user_id = row_split_list[0]

        if (str.__contains__(user_id, "user")):
            group_id = 1
        else:  # sysadmin
            group_id = 2

        application_id = row_split_list[1]

        number_of_queues = 1

        current_row = RowClass(date_and_time, row_counter, submit_time, runtime, number_of_nodes, user_id, group_id,
                               application_id, number_of_queues)

        swf_file.write(current_row.convert_to_string())

        row_counter += 1
