# SWF Parser

Currently works on The NASA Ames iPSC/860 log

## How it works

Created a class called ```RowClass``` which has the following attributes:

- ```order```
- ```submit_time```
- ```wait_time```
- ```runtime```
- ```number_of_nodes ```
- ```average_cpu_time ```
- ```average_memory_per_node```
- ```requested_processors```
- ```requested_runtime```
- ```requested_memory ```
- ```status```
- ```user_id ```
- ```group_id ```
- ```application_id```
- ```number_of_queues ```
- ```number_of_partitions```
- ```preceding_job_number```
- ```think_time ```
- ```datetime ```

Each field is same as the SWF fields from the book (pg.73)

>1. Job number: a counter field, starting from 1.
>2. Submit time in seconds, relative to the start of the log.
>3. Wait time in the queue in seconds.
>4. Runtime (wallclock) in seconds. “Wait time” and “runtime” are used instead of the equivalent >“start time” and   “end time” because they are directly attributable to the scheduler and   >application, and are also suitable for models where only the runtime is relevant.
>5. Number of allocated processors.
>6. Average CPU time used per processor, both user and system, in seconds.
>7. Average memory used per node in kilobytes.
>8. Requested number of processors.
>9. Requested runtime (or CPU time).
>10. Requested memory (again kilobytes per processor).
>11. Status: 1 if the job was completed, 0 if it failed, and 5 if canceled.
>12. User ID: a number, between 1 and the number of different users.
>13. Group ID: a number, between 1 and the number of different groups.
>14. Executable (application): a number, between 1 and the number of different appli- cations   >appearing in the log.
>15. Queue: a number, between 1 and the number of different queues in the system.
>16. Partition: a number, between 1 and the number of different partitions in the sys- tem.
>17. Preceding job number, used in case this job depends on the termination of a pre- vious job.
>18. Think time from preceding job.
