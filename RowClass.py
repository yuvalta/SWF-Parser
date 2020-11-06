class RowClass:
    def __init__(self, order, submit_time, runtime, number_of_nodes, user_id, group_id,
                 application_id, number_of_queues, wait_time=0, average_cpu_time=-1, average_memory_per_node=-1,
                 requested_processors=-1, requested_runtime=-1, requested_memory=-1, status=-1, number_of_partitions=-1,
                 preceding_job_number=-1, think_time=-1):
        self.order = order
        self.submit_time = submit_time
        self.wait_time = wait_time
        self.runtime = runtime
        self.number_of_nodes = number_of_nodes
        self.average_cpu_time = average_cpu_time
        self.average_memory_per_node = average_memory_per_node
        self.requested_processors = requested_processors
        self.requested_runtime = requested_runtime
        self.requested_memory = requested_memory
        self.status = status
        self.user_id = user_id
        self.group_id = group_id
        self.application_id = application_id
        self.number_of_queues = number_of_queues
        self.number_of_partitions = number_of_partitions
        self.preceding_job_number = preceding_job_number
        self.think_time = think_time
        #self.datetime = datetime

    def convert_to_string(self):
        return "{:5s}  {:8s}  {:2s}  {:8s}  {:8s}  {:8s}  {:2s}  {:2s}  {:2s}  {:2s}  {:2s}  {:10s}  {:8s}  {:8s}  {:2s}  {:2s}  {:2s}  {:2s}      \n".format(
            str(self.order), str(self.submit_time), str(self.wait_time), str(self.runtime), str(self.number_of_nodes),
            str(self.average_cpu_time), str(self.average_memory_per_node), str(self.requested_processors),
            str(self.requested_runtime), str(self.requested_memory), str(self.status), str(self.user_id),
            str(self.group_id), str(self.application_id), str(self.number_of_queues), str(self.number_of_partitions),
            str(self.preceding_job_number), str(self.think_time))
    #, str(self.datetime))