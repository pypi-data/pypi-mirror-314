#-*- coding: utf-8 -*-

from odoo import models, fields, api
import psutil
import time
import subprocess
from datetime import datetime


class CPUMonitor(models.Model):
    _name = 'cpu.monitor'
    _description = 'Monitor CPU Usage and States'

    date_time = fields.Datetime('Timestamp', default=fields.Datetime.now, readonly=True)
    cpu_usage = fields.Float('CPU Usage (%)')
    cpu_user = fields.Float('CPU User (%)')
    cpu_system = fields.Float('CPU System (%)')
    cpu_idle = fields.Float('CPU Idle (%)')
    cpu_wait = fields.Float('CPU Wait Time (%)')
    cpu_nice = fields.Float('CPU Nice (%)')
    cpu_steal = fields.Float('CPU Steal Time (%)')
    load_averages = fields.Float('Cpu load average(%)')





    # process =  psutil.Process()
    # print("hyy", psutil.Process())
    # print("context switches --", psutil.Process().num_ctx_switches())
    # print("thread count --", psutil.Process().num_threads())
    # print("cpu frequency --", ((psutil.cpu_freq())))
    # print("cpu_per_core --", ((psutil.cpu_percent(interval=1, percpu=True))))
    #
    # print("------------------System Monitoring----------------")
    # print("System Boot Time",psutil.boot_time())
    # print("cpu uptime --", (time.time())-(psutil.boot_time()))
    # print("System Load (load avg) --", (psutil.getloadavg()))
    # print("cpu count",psutil.cpu_count())


    @api.model
    def _get_cpu_stats(self):
        """
        Method to retrieve CPU stats using psutil.
        """
        cpu_usage = psutil.cpu_percent(interval=1)  # Total CPU usage
        cpu_times = psutil.cpu_times_percent(interval=1)  # Detailed CPU times
        load_averages = psutil.getloadavg()

        self.create({
            'date_time': datetime.now(),
            'cpu_usage': cpu_usage,
            'cpu_user': cpu_times.user,
            'cpu_system': cpu_times.system,
            'cpu_idle': cpu_times.idle,
            'cpu_wait': cpu_times.iowait,
            'cpu_nice': cpu_times.nice,
            'cpu_steal': cpu_times.steal,
            'load_averages':load_averages[2]

        })

    @api.model
    def scheduled_monitoring(self):
        """
        Method to be called via cron job to schedule regular CPU state collection.
        """
        self._get_cpu_stats()

    # print("-----------------resourse consumption-----------------")
    # print("virtual memory --",psutil.virtual_memory())
    # print("physical memory(RAM)",psutil.swap_memory())
    # print("disk usage",psutil.disk_usage('/'))
    # print("network usage",psutil.net_io_counters())
    # print("cpu usage",psutil.net_io_counters())


# print("---------------------------------------------------------------")
# print("----------------RAM Usage-----------------")
# print("Total RAM",psutil.virtual_memory().total)
# print("Used RAM",psutil.virtual_memory().used)
# print("Free RAM",psutil.virtual_memory().free)
# print("available ram",psutil.virtual_memory().available)
# print("memory_percent",psutil.virtual_memory().percent)
# print("Buffered RAM",psutil.virtual_memory().buffers)
# print("cached RAM",psutil.virtual_memory().cached)
# print("shared RAM",psutil.virtual_memory().shared)
#
#
# print("------------Disk I/O Performance--------")
# # print("Throughput (or Bandwidth)",DiskIOMonitor(interval=1))
# print("read_count",psutil.disk_io_counters().read_count)
# print("write_count",psutil.disk_io_counters().write_count)
# print("read_bytes",psutil.disk_io_counters().read_bytes)
# print("write_bytes",psutil.disk_io_counters().write_bytes)
#
# first_io = psutil.disk_io_counters()
# time.sleep(1)
# second_io = psutil.disk_io_counters()
# print("first_io",first_io)
# print("second_io",second_io)
