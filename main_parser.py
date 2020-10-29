from shutil import copyfile, copy
import os
from datetime import datetime
from RowClass import RowClass  # order, user_id, application_id, number_of_nodes, runtime, datetime

original_log_path = "./NASA-iPSC-1993-0.txt"
SWF_log = "./SWF_log.txt"

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
        runtime =

        current_row = RowClass(row_counter, row_split_list[0], row_split_list[1], row_split_list[2], row_split_list[3],
                               date_and_time)

        row_counter += 1
