# -*- coding: utf-8 -*-
# Custom signals for schedule models

from django.dispatch import Signal

event_changed = Signal(providing_args=["event", ])
