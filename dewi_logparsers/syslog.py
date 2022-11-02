# Copyright 2016-2022 Laszlo Attila Toth
# Distributed under the terms of the GNU Lesser General Public License v3

import datetime
import re
import time


class Parser:
    def parse_date(self, line: str) -> re.Match[str] | None:
        raise NotImplementedError()

    def parse(self, line: str) -> re.Match[str] | None:
        raise NotImplementedError()


class ISO8601Parser(Parser):
    """
    Parses log lines having 'time host application message' format,
    and time is the form defined in RFC 3339, e.g.
    1990-12-31T15:59:60-08:00 (anyway, it is a leap second)
    """

    def __init__(self):
        self._pattern = re.compile(
            r'^(?P<date>\d+-\d+-\d+)T(?P<time>\d\d:\d\d:\d\d)\+[0-9]+:[0-9]+ ' +
            r'(?P<host>[-_.0-9a-zA-Z]+) (?P<app>[-_./0-9a-zA-Z]+)(\[(?P<pid>[0-9]+)\])?: (?P<msg>.*)$'
        )

        self._date_time_pattern = re.compile(
            r'^(?P<date>\d+-\d+-\d+)T(?P<time>\d\d:\d\d:\d\d)[-+][0-9]+:[0-9]+'
        )

    def parse_date(self, line: str) -> re.Match[str] | None:
        parsed = self._date_time_pattern.match(line)

        if not parsed:
            print(line)
            return None

        return parsed

    def parse(self, line: str) -> re.Match[str] | None:
        parsed = self._pattern.match(line)

        if not parsed:
            return None

        return parsed

    @classmethod
    def to_timestamp(cls, date_time: str) -> float:
        return cls.to_datetime(date_time).timestamp()

    @classmethod
    def to_datetime(cls, date_time: str) -> datetime.datetime:
        if date_time[-3] == ':':
            date_time = date_time[:-3] + date_time[-2:]
        return datetime.datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S%z")


class GenericParser(Parser):
    def __init__(self):
        self._date_time_pattern = re.compile(
            r'^([A-Za-z]+ +[0-9]+ )'
        )

        self._any_date_time_pattern = re.compile(
            r'^(?P<date>.*)'
        )

    def parse_date(self, line: str) -> re.Match[str] | None:
        matched = self._date_time_pattern.match(line)
        if not matched:
            return None

        time_struct = time.strptime(matched.group(1) + time.strftime('%Y'), '%b %d %Y')

        d = f'{time_struct.tm_year}-{time_struct.tm_mon:02d}-{time_struct.tm_mday:02d}'
        return self._any_date_time_pattern.match(d)

    def parse(self, line: str) -> re.Match[str] | None:
        pass
