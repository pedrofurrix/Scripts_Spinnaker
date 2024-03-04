# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from open_ephys.streaming import EventListener
stream = EventListener()

def ttl_callback(info):
    if info['line'] == 2 and info['state']:
        print('Rising event on line 2')
        
def spike_callback(info):
  print(info)      
        
stream.start(ttl_callback=ttl_callback, spike_callback=spike_callback)
