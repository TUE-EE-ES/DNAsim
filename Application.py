# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 20:37:07 2022

@author: 20195234
"""

from DNAsim.TraceGenerator import *


#### Full/Recurrent connections application API ###########




class Layer:
#Network API wrapper
    def __init__(self, fire_map = None, output_tuple = None):

        if(fire_map is None):
            self.fire_map = np.zeros(output_tuple)
            self.time = output_tuple[1]
            self.size = output_tuple[0]
            self.spikeSum = np.zeros(self.time)
            self.output_layer = True
        else:
            self.fire_map = fire_map
            if(len(fire_map.shape) == 1):
                self.time = 1
                self.size = fire_map.shape[0]
            else:
                self.time = fire_map.shape[1]
                self.size = fire_map.shape[0]
            self.output_layer = False
            self.spikeSum = np.sum(fire_map, axis = 0)
        
        self.synapse_mem = 0
        self.SOPs = np.zeros(self.time)
        



    def addSource(self, size, fire_rate):
        
        self.SOPs += fire_rate
        self.synapse_mem += size



    def getMap(self):
        return self.fire_map
    
    def getSynapseCost(self):
        return self.synapse_mem
    
    def getSOPs(self):
        return self.SOPs
    
    def getNeuron(self, neuron_id):
        return self.fire_map[neuron_id]
    
    def isInput(self):
        return (self.synapse_mem == 0)
    
    def isNeuron(self):
        return (self.synapse_mem != 0)
    
    def getNeuronsCost(self):
        if (self.isInput()):
            return 0
        else:
            return self.size
    
    def isOutput(self):
        return (self.output_layer)
    
    def getSize(self):
        return self.size
                
    def getTime(self):
        return self.time
    
    def getSpikeSum (self):
        return self.spikeSum

class Network:
#List of layers, able to connect layers together
    
    def __init__(self, trace_gen, output_layers, case_simulation = "Average", time_simulation = "None"):
        

        self.layer_list = []
        self.connection_list = []
        if(case_simulation == "Average"):
            if(time_simulation == "None"):
                self.trace_files = trace_gen.getAverageTraces()
            elif(time_simulation == "Average"):
                self.trace_files = trace_gen.getAverageAverageTraces()
            elif(time_simulation == "Max"):
                self.trace_files = trace_gen.getAverageMaxTraces()          
            else:
                print("Error invalid time_simulation input")
                return
        elif (case_simulation == "Max"):
             if(time_simulation == "None"):
                 self.trace_files = trace_gen.getMaxTraces()
             elif (time_simulation == "Average"):
                 self.trace_files = trace_gen.getMaxAverageTraces()
             elif (time_simulation == "Max"):
                 self.trace_files = trace_gen.getMaxMaxTraces()                 
             else:
                 print("Error invalid time_simulation input")
                 return               
        else:
            print("Error invalid case_simulation input")
            return
        
        for trace in self.trace_files:
            self.layer_list.append(Layer(trace))
            self.connection_list.append([])

            
        for i in range (len(output_layers)):
            self.connection_list.append([])
            self.layer_list.append(Layer(output_tuple = (output_layers[i], self.layer_list[0].getTime())))

       
        

        #self.SOPs = np.zeros(len(trace_files) + int(output_layers))

    def connect(self, source, destination):
        self.layer_list[destination].addSource(self.layer_list[source].getSize(), self.layer_list[source].getSpikeSum())
        self.connection_list[source].append(destination)
    
    def mapDestinations(self, source_layer):
        return self.connection_list[source_layer]

    def getSize (self):
        return len(self.layer_list)
    
    def getLayer(self, layer_id):
        return self.layer_list[layer_id]

    
    def getTime(self):
        return self.layer_list[0].getTime()



