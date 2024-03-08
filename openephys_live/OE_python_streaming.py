# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from open_ephys.streaming import EventListener
import time


stream = EventListener()


def ttl_callback(info):
    if info['line'] == 2 and info['state']:
        print('Rising event on line 2')

count=0
def spike_callback(info):
  print(info)
  spike_callback.counter+=1

spike_callback.counter=0
  
start_time = time.time()
stream.start(ttl_callback=ttl_callback, spike_callback=spike_callback)


end_time = time.time()

elapsed_time = end_time - start_time


print(spike_callback.counter)
print("Elapsed time: ", elapsed_time) 
spikes_ms=spike_callback.counter/(elapsed_time*1000)
print("Spikes/ms=",spikes_ms)