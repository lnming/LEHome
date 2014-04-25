#!/usr/bin/env python
# encoding: utf-8


import inspect
from util.log import *


class Callback:
    def __init__(self):
        if not callable(getattr(self, "callback", None)):
            ERROR("callback method not found.")
            return
        self.callback_param_names = inspect.getargspec(self.callback)[0]
        DEBUG(self.callback_param_names)
        if "self" in self.callback_param_names:
            self.callback_param_names.remove("self")

        if callable(getattr(self, "canceled", None)):
            self.canceled_param_names = inspect.getargspec(
                                                            self.canceled
                                                            )[0]
            DEBUG(self.canceled_param_names)
            if "self" in self.canceled_param_names:
                self.canceled_param_names.remove("self")

    def internal_callback(self, **kwargs):
        call_dict = {}
        for key in self.callback_param_names:
            if key in kwargs:
                call_dict[key] = kwargs[key]
            else:
                call_dict[key] = None
        DEBUG("callback: %s" % (kwargs, ))
        return self.callback(**call_dict)

    def internal_canceled(self, **kwargs):
        if not callable(getattr(self, "canceled", None)):
            return
        call_dict = {}
        for key in self.canceled_param_names:
            if key in kwargs:
                call_dict[key] = kwargs[key]
            else:
                call_dict[key] = None
        DEBUG("canceled: %s" % (kwargs, ))
        return self.canceled(**call_dict)
