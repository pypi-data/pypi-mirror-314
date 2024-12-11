#!/usr/bin/env python
# -*- coding:utf-8 -*-
import math
from datetime import datetime, date, time
from enum import Enum

from dateutil.relativedelta import relativedelta

from . import DateType, TimeType, DateTimeType
from ._datetype import _handle_datetime_type, _handle_date_type, _handle_time_type, NumberType
from ..classes import StaticClass

__all__ = []


class _Years(StaticClass):

    @staticmethod
    def diff(before: TimeType or DateType or DateTimeType, after: TimeType or DateType or DateTimeType) \
            -> NumberType:
        return abs(before.year - after.year)

    @staticmethod
    def continuous(start: TimeType or DateType or DateTimeType, number: int, step: int = 1,
                   other_init: bool = True) -> \
            list[time or date or datetime, ...]:
        try:
            start_ = _handle_datetime_type(start)
            is_datetime = True
        except TypeError:
            start_ = _handle_date_type(start)
            start_ = datetime(year=start_.year, month=start_.month, day=start_.day)
            is_datetime = False
        results = []
        for _ in range(number):
            start_ += relativedelta(years=step)

            if other_init:
                dt = datetime(year=start_.year, month=1, day=1, tzinfo=start_.tzinfo, fold=start_.fold)
            else:
                dt = datetime(year=start_.year, month=start_.month, day=start_.day, hour=start_.hour,
                              minute=start_.minute, second=start_.second, microsecond=start_.microsecond,
                              tzinfo=start_.tzinfo, fold=start_.fold)
            if is_datetime:
                results.append(dt)
            else:
                results.append(dt.date())
        return results

    @staticmethod
    def delta(start: TimeType or DateType or DateTimeType, num: NumberType) -> time or date or datetime:
        try:
            start_ = _handle_datetime_type(start)
        except TypeError:
            start_ = _handle_date_type(start)
        return start_ + relativedelta(years=num)


class _Months(StaticClass):

    @staticmethod
    def diff(before: DateType, after: DateType) -> NumberType:
        return abs(before.month - after.month + 12 * _Years().diff(before, after))

    @staticmethod
    def continuous(start: DateType or DateTimeType, number: int, step: int = 1,
                   other_init: bool = True) -> list[date or datetime, ...]:
        try:
            start_ = _handle_datetime_type(start)
            is_datetime = True
        except TypeError:
            start_ = _handle_date_type(start)
            start_ = datetime(year=start_.year, month=start_.month, day=start_.day)
            is_datetime = False
        results = []
        for _ in range(number):
            start_ += relativedelta(months=step)
            if other_init:
                dt = datetime(year=start_.year, month=start_.month, day=1, tzinfo=start_.tzinfo, fold=start_.fold)
            else:
                dt = datetime(year=start_.year, month=start_.month, day=start_.day, hour=start_.hour,
                              minute=start_.minute, second=start_.second, microsecond=start_.microsecond,
                              tzinfo=start_.tzinfo, fold=start_.fold)
            if is_datetime:
                results.append(dt)
            else:
                results.append(dt.date())
        return results

    @staticmethod
    def delta(start: DateType or DateTimeType, num: NumberType) -> date or datetime:
        try:
            start_ = _handle_datetime_type(start)
        except TypeError:
            start_ = _handle_date_type(start)
        return start_ + relativedelta(months=num)


class _Weeks(StaticClass):

    @staticmethod
    def diff(before: DateType, after: DateType) -> NumberType:
        return abs(math.ceil(_Days().diff(before, after) / 7))

    @staticmethod
    def continuous(start: DateType or DateTimeType, number: int, step: int = 1,
                   other_init: bool = True) -> list[date or datetime, ...]:
        try:
            start_ = _handle_datetime_type(start)
            is_datetime = True
        except TypeError:
            start_ = _handle_date_type(start)
            start_ = datetime(year=start_.year, month=start_.month, day=start_.day)
            is_datetime = False
        results = []
        for _ in range(number):
            start_ = start_ + relativedelta(weeks=step)
            if other_init is True:
                dt = datetime(year=start_.year, month=start_.month, day=start_.day, tzinfo=start_.tzinfo,
                              fold=start_.fold)
            else:
                dt = datetime(year=start_.year, month=start_.month, day=start_.day, hour=start_.hour,
                              minute=start_.minute, second=start_.second, microsecond=start_.microsecond,
                              tzinfo=start_.tzinfo, fold=start_.fold)
            if is_datetime:
                results.append(dt)
            else:
                results.append(dt.date())
        return results

    @staticmethod
    def delta(start: DateType or DateTimeType, num: NumberType) -> date or datetime:
        try:
            start_ = _handle_datetime_type(start)
        except TypeError:
            start_ = _handle_date_type(start)
        return start_ + relativedelta(weeks=num)


class _Days(StaticClass):

    @staticmethod
    def diff(before: DateType, after: DateType) -> NumberType:
        return abs((before - after).days)

    @staticmethod
    def continuous(start: DateType or DateTimeType, number: int, step: int = 1,
                   other_init: bool = True) -> list[date or datetime, ...]:
        try:
            start_ = _handle_datetime_type(start)
            is_datetime = True
        except TypeError:
            start_ = _handle_date_type(start)
            start_ = datetime(year=start_.year, month=start_.month, day=start_.day)
            is_datetime = False
        results = []
        for _ in range(number):
            start_ = start_ + relativedelta(days=step)
            if is_datetime:
                if other_init is True:
                    results.append(datetime(year=start_.year, month=start_.month, day=start_.day, tzinfo=start_.tzinfo,
                                            fold=start_.fold))
                else:
                    results.append(datetime(year=start_.year, month=start_.month, day=start_.day, hour=start_.hour,
                                            minute=start_.minute, second=start_.second, microsecond=start_.microsecond,
                                            tzinfo=start_.tzinfo, fold=start_.fold))
            else:
                results.append(start_.date())
        return results

    @staticmethod
    def delta(start: DateType or DateTimeType, num: NumberType) -> date or datetime:
        try:
            start_ = _handle_datetime_type(start)
        except TypeError:
            start_ = _handle_date_type(start)
        return start_ + relativedelta(days=num)


class _Hours(StaticClass):

    @staticmethod
    def diff(before: TimeType, after: TimeType) -> NumberType:
        if isinstance(before, datetime) and isinstance(after, datetime):
            return before.hour - after.hour + 24 * _Days().diff(before, after)
        else:
            return abs(_handle_time_type(before).hour - _handle_time_type(after).hour)

    @staticmethod
    def continuous(start: TimeType or DateTimeType, number: int, step: int = 1,
                   other_init: bool = True) -> list[time or datetime, ...]:
        results = []
        try:
            start_ = _handle_datetime_type(start)
            is_datetime = True
        except TypeError:
            start_ = _handle_time_type(start)
            is_datetime = False
        for _ in range(number):
            start_ += relativedelta(hours=step)
            if is_datetime:
                if other_init is True:
                    dt = datetime(year=start_.year, month=start_.month, day=start_.day, tzinfo=start_.tzinfo,
                                  fold=start_.fold)
                else:
                    dt = datetime(year=start_.year, month=start_.month, day=start_.day, hour=start_.hour,
                                  minute=start_.minute, second=start_.second, microsecond=start_.microsecond,
                                  tzinfo=start_.tzinfo, fold=start_.fold)
            else:
                if other_init:
                    dt = time(hour=start_.hour, minute=0, second=0, microsecond=0,
                              tzinfo=start_.tzinfo, fold=start_.fold)
                else:
                    dt = time(hour=start_.hour, minute=start_.minute, second=start_.second,
                              microsecond=start_.microsecond, tzinfo=start_.tzinfo, fold=start_.fold)
            results.append(dt)
        return results

    @staticmethod
    def delta(start: TimeType or DateTimeType, num: NumberType) -> time or datetime:
        try:
            start_ = _handle_datetime_type(start)
        except TypeError:
            start_ = _handle_time_type(start)
        return start_ + relativedelta(hours=num)


class _Minutes(StaticClass):

    @staticmethod
    def diff(before: TimeType, after: TimeType) -> NumberType:
        if isinstance(before, datetime) and isinstance(after, datetime):
            return abs(before.minute - after.minute + 24 * 60 * _Days().diff(before, after))
        else:
            before_, after_ = _handle_time_type(before), _handle_time_type(after)
            hours_diff = abs(before_.hour - after_.hour)
            return abs(before_.minute - after_.minute + 60 * hours_diff)

    @staticmethod
    def continuous(start: TimeType or DateTimeType, number: int, step: int = 1,
                   other_init: bool = True) -> list[time or datetime, ...]:
        results = []
        try:
            start_ = _handle_datetime_type(start)
            is_datetime = True
        except TypeError:
            start_ = _handle_time_type(start)
            is_datetime = False
        for _ in range(number):
            start_ += relativedelta(minutes=step)
            if is_datetime:
                if other_init is True:
                    dt = datetime(year=start_.year, month=start_.month, day=start_.day, hour=start_.hour,
                                  minute=start_.minute, tzinfo=start_.tzinfo, fold=start_.fold)
                else:
                    dt = datetime(year=start_.year, month=start_.month, day=start_.day, hour=start_.hour,
                                  minute=start_.minute, second=start_.second, microsecond=start_.microsecond,
                                  tzinfo=start_.tzinfo, fold=start_.fold)
            else:
                if other_init:
                    dt = time(hour=start_.hour, minute=0, second=0, microsecond=0, tzinfo=start_.tzinfo,
                              fold=start_.fold)
                else:
                    dt = time(hour=start_.hour, minute=start_.minute, second=start_.second,
                              microsecond=start_.microsecond, tzinfo=start_.tzinfo, fold=start_.fold)
            results.append(dt)
        return results

    @staticmethod
    def delta(start: TimeType or DateTimeType, num: NumberType) -> time or datetime:
        try:
            start_ = _handle_datetime_type(start)
        except TypeError:
            start_ = _handle_time_type(start)
        return start_ + relativedelta(minutes=num)


class _Seconds(StaticClass):

    @staticmethod
    def diff(before: TimeType, after: TimeType) -> NumberType:
        return _Minutes().diff(before, after) * 60

    @staticmethod
    def continuous(start: TimeType or DateTimeType, number: int, step: int = 1,
                   other_init: bool = True) -> list[time or datetime, ...]:
        results = []
        try:
            start_ = _handle_datetime_type(start)
            is_datetime = True
        except TypeError:
            start_ = _handle_time_type(start)
            is_datetime = False
        for _ in range(number):
            start_ += relativedelta(seconds=step)
            if is_datetime:
                if other_init is True:
                    dt = datetime(year=start_.year, month=start_.month, day=start_.day, hour=start_.hour,
                                  minute=start_.minute, second=start_.second, microsecond=0,
                                  tzinfo=start_.tzinfo, fold=start_.fold)
                else:
                    dt = datetime(year=start_.year, month=start_.month, day=start_.day, hour=start_.hour,
                                  minute=start_.minute, second=start_.second, microsecond=start_.microsecond,
                                  tzinfo=start_.tzinfo, fold=start_.fold)
            else:
                if other_init:
                    dt = time(hour=start_.hour, minute=start_.minute, second=start_.second, microsecond=0,
                              tzinfo=start_.tzinfo, fold=start_.fold)
                else:
                    dt = time(hour=start_.hour, minute=start_.minute, second=start_.second,
                              microsecond=start_.microsecond, tzinfo=start_.tzinfo, fold=start_.fold)
            results.append(dt)
        return results

    @staticmethod
    def delta(start: TimeType or DateTimeType, num: NumberType) -> time or datetime:
        try:
            start_ = _handle_datetime_type(start)
        except TypeError:
            start_ = _handle_time_type(start)
        return start_ + relativedelta(seconds=num)


class _Milliseconds(StaticClass):

    @staticmethod
    def diff(before: TimeType, after: TimeType) -> NumberType:
        return _Seconds().diff(before, after) * 1000

    @staticmethod
    def continuous(start: TimeType or DateTimeType, number: int, step: int = 1,
                   other_init: bool = True) -> list[time or datetime, ...]:
        results = []
        try:
            start_ = _handle_datetime_type(start)
            is_datetime = True
        except TypeError:
            start_ = _handle_time_type(start)
            is_datetime = False
        for _ in range(number):
            start_ += relativedelta(microseconds=step * 1000)
            if is_datetime:
                if other_init is True:
                    dt = datetime(year=start_.year, month=start_.month, day=start_.day, hour=start_.hour,
                                  minute=start_.minute, second=start_.second, microsecond=0,
                                  tzinfo=start_.tzinfo, fold=start_.fold)
                else:
                    dt = datetime(year=start_.year, month=start_.month, day=start_.day, hour=start_.hour,
                                  minute=start_.minute, second=start_.second, microsecond=start_.microsecond,
                                  tzinfo=start_.tzinfo, fold=start_.fold)
            else:
                if other_init:
                    dt = time(hour=start_.hour, minute=start_.minute, second=start_.second, microsecond=0,
                              tzinfo=start_.tzinfo, fold=start_.fold)
                else:
                    dt = time(hour=start_.hour, minute=start_.minute, second=start_.second,
                              microsecond=start_.microsecond, tzinfo=start_.tzinfo, fold=start_.fold)
            results.append(dt)
        return results

    @staticmethod
    def delta(start: TimeType or DateTimeType, num: NumberType) -> time or datetime:
        try:
            start_ = _handle_datetime_type(start)
        except TypeError:
            start_ = _handle_time_type(start)
        return start_ + relativedelta(microseconds=num * 1000)


class _Microseconds(StaticClass):

    @staticmethod
    def diff(before: TimeType, after: TimeType) -> NumberType:
        return _Milliseconds().diff(before, after) * 1000

    @staticmethod
    def continuous(start: TimeType or DateTimeType, number: int, step: int = 1,
                   other_init: bool = True) -> list[time or datetime, ...]:
        results = []
        try:
            start_ = _handle_datetime_type(start)
            is_datetime = True
        except TypeError:
            start_ = _handle_time_type(start)
            is_datetime = False
        for _ in range(number):
            start_ += relativedelta(microseconds=step)
            if is_datetime:
                dt = datetime(year=start_.year, month=start_.month, day=start_.day, hour=start_.hour,
                              minute=start_.minute, second=start_.second, microsecond=start_.microsecond,
                              tzinfo=start_.tzinfo, fold=start_.fold)
            else:
                dt = time(hour=start_.hour, minute=start_.minute, second=start_.second,
                          microsecond=start_.microsecond, tzinfo=start_.tzinfo, fold=start_.fold)

            results.append(dt)
        return results

    @staticmethod
    def delta(start: TimeType or DateTimeType, num: NumberType) -> time or datetime:
        try:
            start_ = _handle_datetime_type(start)
        except TypeError:
            start_ = _handle_time_type(start)
        return start_ + relativedelta(microseconds=num)


class DatetimeCategory(Enum):
    YEARS = _Years
    MONTHS = _Months
    WEEKS = _Weeks
    DAYS = _Days
    HOURS = _Hours
    MINUTES = _Minutes
    SECONDS = _Seconds
    MILLISECONDS = _Milliseconds
    MICROSECONDS = _Microseconds

    def diff(self, before: DateType or TimeType or DateTimeType, after: DateType or TimeType or DateTimeType)\
            -> NumberType:
        """
        Calculate the difference between two dates and times
        """
        return self.value.diff(before, after)

    def continuous(self, start: TimeType or DateType or DateTimeType, number: int, step: int = 1,
                   other_init: bool = True) -> list[time or date or datetime, ...]:
        """
        Generate a duration of time.
        :param start: start datetime.
        :param number: generate datetime number.
        :param step:


        :param other_init:
        :return:
        """
        return self.value.continuous(start, number, step, other_init)

    def delta(self, start: TimeType or DateType or DateTimeType, num: NumberType) -> time or date or datetime:
        return self.value.delta(start, num)
