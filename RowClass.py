class RowClass:
    def __init__(self, order, user_id, application_id, number_of_nodes, runtime, datetime):
        self.order = order
        self.submit_time = submit_time
        self.wait_time = wait_time
        self.runtime = runtime
        self.allocated_cpu = allocated_cpu
        self.average_cpu_time = average_cpu_time
        self.average_memory_per_node = average_memory_per_node

        self.user_id = user_id
        self.application_id = application_id
        self.number_of_nodes = number_of_nodes
        self.datetime = datetime
