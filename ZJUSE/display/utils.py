#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 weihao <weihao@weihao-PC>
#
# Distributed under terms of the MIT license.

"""

"""
from datetime import datetime, time
from django.forms import widgets

class TimeSelectorWidget(widgets.MultiWidget):
    def __init__(self, attrs=None):
        hours = [(hour, hour) for hour in range(24)]
        minutes = [(minute, minute) for minute in range(60)]
        _widgets = (
            widgets.Select(attrs=attrs, choices=hours),
            widgets.Select(attrs=attrs, choices=minutes),
        )
        super().__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.hour+8, value.minute]
        return [None, None]

    def value_from_datadict(self, data, files, name):
        datelist = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]
        try:
            T = time(
                hour=int(datelist[0]),
                minute=int(datelist[1]),
            )
        except ValueError:
            return ''
        else:
            return T

def GenerateDate(dict):
    year = int(dict['ddl_date_year'])
    month = int(dict['ddl_date_month'])
    day = int(dict['ddl_date_day'])
    hour = int(dict['ddl_time_0'])
    minute = int(dict['ddl_time_1'])
    return datetime(year=year, month=month, day=day, hour=hour, minute=minute)
