# Copyright 2016-2022 Laszlo Attila Toth
# Distributed under the terms of the GNU Lesser General Public License v3

from dewi_logparsers.loghandler import LogParserModule
from dewi_module_framework.messages import Level


class RebootModule(LogParserModule):
    """
    Example module that calculates reboots on a system that have @reboot cron jobs
    """

    def get_registration(self):
        return [
            {
                'program': 'cron',
                'message_substring': '(CRON) INFO (Running @reboot jobs)',
                'callback': self.system_reboot
            }
        ]

    def start(self):
        self._reboots = list()

    def system_reboot(self, time: str, program: str, pid: str | None, msg: str):
        self._reboots.append(time)

    def finish(self):
        if self._reboots:
            self.add_message(
                Level.WARNING, 'System', 'Reboot and startup',
                "System is rebooted; count='{}'".format(len(self._reboots)))

            for reboot_time in self._reboots:
                self.append('system.reboots', reboot_time)
