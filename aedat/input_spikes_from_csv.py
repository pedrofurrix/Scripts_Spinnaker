# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 19:41:20 2024

@author: pedro
"""
import csv
import pyNN.spiNNaker as sim
from time import sleep
import pyNN.utility.plotting as plot


def send_spikes(label,connection):
    with open('spike_times.csv', mode='r') as file:
        csv_reader=csv.DictReader(file)
        time_=0
        for row in csv_reader:
            time=row["timestamp"]/1000
            neuron_id=row["neuron_id"]
            sleep(time-time_)
            time_=time
            connection.send_spike(label,neuron_id)
            
            
injector_label = "injector"
           
# Create the connection, noting that the label will be a "sender".
# Note the use of local_port=None allows the automatic assignment of a port.
connection = sim.external_devices.SpynnakerLiveSpikesConnection(
    local_port=None, send_labels=[injector_label])            
connection.add_start_resume_callback(injector_label, send_spikes)

sim.setup(1.0)
        
injector = sim.Population(
    5, sim.external_devices.SpikeInjector(
        database_notify_port_num=connection.local_port),
    # Critical: Make sure the label is used!
    label=injector_label)

# Set up a Population to receive spikes and record
pop = sim.Population(5, sim.IF_curr_exp(), label="pop")
pop.record("spikes")

# Connect the injector to the population
sim.Projection(injector, pop, sim.OneToOneConnector(), sim.StaticSynapse(weight=5))


# Run the simulation and get the spikes out
simtime=2000
sim.run(simtime)
spikes = pop.get_data("spikes").segments[0].spiketrains

# End the simulation and display the spikes
sim.end()
print(spikes)

# plot the spikes
plot.Figure(
# plot spikes
    plot.Panel(spikes, yticks=True, markersize=5, xlim=(0, simtime)),
    title="Spikes",
    annotations="Simulated with {}".format(sim.name())
)