# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 11:22:25 2023

@author: pedro_8k2kvrz
"""

# Import the simulator
import pyNN.spiNNaker as sim
import pyNN.utility.plotting as plot

# Other imports used in this example
from time import sleep

# Set up a function that will start sending spikes.
# This is automatically run in a separate thread from the rest of the simulation.
# This must accept two arguments: 
#    The label of the Population that the callback is registered against, 
#    and the connection the callback is registered against.
def send_spikes(label, connection):
    for i in range(10):
        sleep(0.1)
        connection.send_spike(label,0)
        

# Keep track of the label of the injector as this needs to match up in several places
injector_label = "injector"

# Create the connection, noting that the label will be a "sender".
# Note the use of local_port=None allows the automatic assignment of a port.
connection = sim.external_devices.SpynnakerLiveSpikesConnection(
    local_port=None, send_labels=[injector_label])

# Add a callback to be called at the start of the simulation
connection.add_start_resume_callback(injector_label, send_spikes)

sim.setup(1.0)

inj_pop=sim.Population(1,sim.external_devices.SpikeInjector(
        database_notify_port_num=connection.local_port), label=injector_label)        
pop2=sim.Population(100,sim.IF_curr_exp(), label="pop2")

proj1=sim.Projection(pop2,pop2,sim.FixedProbabilityConnector(0.02),synapse_type=sim.StaticSynapse(weight=0.5,delay=2))
proj_stim=sim.Projection(inj_pop,pop2,sim.AllToAllConnector(), synapse_type=sim.StaticSynapse(weight=5.0,delay=1))

pop2.record("spikes")

simtime=1000
sim.run(simtime)


#Retrieve the spikes
spikes=pop2.get_data("spikes").segments[0].spiketrains
sim.end()

plot.Figure(

plot.Panel(spikes, yticks=True, markersize=5, xlim=(0, simtime)),
    title="Spikes_Spike_Injector",
    annotations="Simulated with {}".format(sim.name())

)
