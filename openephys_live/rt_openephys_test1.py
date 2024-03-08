# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 19:44:34 2024

@author: pedro
"""

import pyNN.spiNNaker as sim
import pyNN.utility.plotting as plot
import matplotlib.pyplot as plt 
import sys
from open_ephys.streaming import EventListener



original_stdout = sys.stdout
live_input = True
#address='127.0.0.1:5557'
stream = EventListener()
label="sender"
connection= sim.external_devices.SpynnakerLiveSpikesConnection(send_labels=["sender"], receive_labels=["receiver"], local_port=None)


# === Simulation Setup ===
sim.setup(timestep=1.0)
sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 100)

if live_input:
    input_pop = sim.Population(1, sim.external_devices.SpikeInjector(database_notify_port_num=connection.local_port), label="sender")
else:
    input_pop = sim.Population(1, sim.SpikeSourceArray(spike_times=[0, 100, 200, 300, 400]), label="sender")
    
main_pop = sim.Population(1, sim.IF_curr_exp(), label="receiver")
input_proj = sim.Projection(input_pop, main_pop, sim.OneToOneConnector(), synapse_type=sim.StaticSynapse(weight=5, delay=1))

# === External Sender Setup ===

def spike_callback(info):
    print(info)
    connection.send_spike(label,0,send_full_keys=True)
    
    
def ttl_callback(info):
    if info['line'] == 2 and info['state']:
        print('Rising event on line 2')
    
def start_spikes(label,connection):
    if live_input:
        stream.start(spike_callback=spike_callback,ttl_callback=ttl_callback)
    
"""  
def input_thread(label,sender):
    time_between_spikes = 0.1
    quit = 0
    input_spike_duration = 40 # secs
    print("Start sending input spikes for {} seconds...".format(input_spike_duration))
    while(quit < input_spike_duration):
        time.sleep(time_between_spikes)
        sender.send_spike(label, 0, send_full_keys=True)
        quit += time_between_spikes
    print("Input Spikes stopped")
    
"""  



connection.add_start_resume_callback(label,start_spikes)



    

# === External Receiver Setup ===
sim.external_devices.activate_live_output_for(main_pop, database_notify_port_num=connection.local_port)

'''
def receive_spikes(label, time, neuron_ids):
    with open("output.txt", "a") as f:
        sys.stdout = f
        for neuron_id in neuron_ids:
                print("Received spike at time {} from {} {}".format(time, label, neuron_id))
    sys.stdout = original_stdout
connection.add_receive_callback("receiver", receive_spikes)
'''

def receive_spikes(label, time, neuron_ids):
        for neuron_id in neuron_ids:
                print("Received spike at time {} from {} {}".format(time, label, neuron_id))

connection.add_receive_callback("receiver", receive_spikes)

'''
def stop_receiving():
    stream.end()

connection.add_pause_stop_callback(label,stop_receiving)
'''

main_pop.record(["spikes"])

# === Start the Simulation ===
simtime = 5000
sim.run(simtime)

# === Retrieve the Results (Post Simulation) ===
neo = main_pop.get_data(variables=["spikes"])
spikes = neo.segments[0].spiketrains
sim.end()


# === Plot the Results of the Simulation ===
plot.Figure(
    plot.Panel(spikes, yticks=True, xticks=True, markersize=5, xlim=(0, simtime)),
    title="OpenEphys Live Input Test"
)
plt.xlabel("Simulation Time [ms]")
plt.locator_params(axis="y", integer=True, tight=True)
plt.show()

sys.exit()