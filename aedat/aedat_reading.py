# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import aedat

def extract_neuronal_events(file_path):
    events = []
    with aedat.Events(file_path) as f:
        for event in f:
            # Extract relevant information from the AEDAT events
            neuron_id = event.neuron_id
            timestamp = event.timestamp
            polarity = event.polarity  # Optional, depending on the AEDAT file

            # Add the extracted information to the list
            events.append({'neuron_id': neuron_id, 'timestamp': timestamp, 'polarity': polarity})
            


