# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 09:59:04 2023

@author: pedro_8k2kvrz
"""

import pyNN.spiNNaker as sim
import pyNN.utility.plotting as plot
import matplotlib.pyplot as plt


# Setup the Simulator
sim.setup(timestep=1.0)
sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 100)


# Create the neural populations
simtime = 1000
pop_1 = sim.Population(1, sim.IF_curr_exp(tau_syn_E=5,tau_m=20), label="pop_1")
#input = sim.Population(2, sim.SpikeSourcePoisson(), label="input")
times1=[50*i for i in range(simtime//50)]
times2=[times1[i]+2*i for i in range (simtime//50)]
times=[times1,times2]
print(times)
input= sim.Population(2, sim.SpikeSourceArray(spike_times=times), label="input")

# Create projections between the populations
connect_list=[(0,0,2.5,1),(1,0,2.5,1)]
input_proj = sim.Projection(input, pop_1, sim.FromListConnector(connect_list),
synapse_type=sim.StaticSynapse())

# Setup data recording
pop_1.record(["spikes", "v"])

sim.run(simtime)


# Retrieve and process the recorded data
neo = pop_1.get_data(variables=["spikes", "v"])
spikes = neo.segments[0].spiketrains
print(spikes)
v = neo.segments[0].filter(name='v')[0]
#print(v)
sim.end()


plot.Figure(
    # plot voltage for first ([0]) neuron
    plot.Panel(v, ylabel="Membrane potential (mV)",
               data_labels=[pop_1.label], yticks=True, xlim=(0, simtime)),
    # plot spikes (or in this case spike)
    plot.Panel(spikes, yticks=True, markersize=5, xlim=(0, simtime)),
    title="Simple Example",
    annotations="Simulated with {}".format(sim.name())
)

