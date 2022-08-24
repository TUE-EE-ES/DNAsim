# -*- coding: utf-8 -*-

from DNAsim.Application import *

class Target:
    
    def __init__ (self, core_coordinate, count):
        self.core_coordinate = core_coordinate
        self.count = count

class Source:
    
    def __init__(self, core_coordinate, count, spikerate, SOPs):
        
        self.core_coordinate = core_coordinate
        self.count = count
        self.spikerate = spikerate
        self.SOPs = SOPs
        


class Mesh_Mapper:

    def __init__(self, mesh_config, network):
#mapper_config: [noc_dim_x, noc_dim_y]

        self.mesh_config = mesh_config
        self.network = network
        self.initialize_maps()
        
    def initialize_maps(self):
        

        
        self.count_map = np.zeros((self.mesh_config[0], self.mesh_config[1], self.network.getSize()))        
        self.spikes_map = np.zeros((self.mesh_config[0], self.mesh_config[1], self.network.getSize(), self.network.getTime()))
        self.SOPs_map = np.zeros((self.mesh_config[0], self.mesh_config[1], self.network.getSize(), self.network.getTime())) 
        
        self.neuron_cost_map = np.zeros((self.mesh_config[0], self.mesh_config[1]))
        self.synapse_cost_map = np.zeros((self.mesh_config[0], self.mesh_config[1]))
                
        # self.input_layer_map = np.zeros(self.network.getSize())
        
        # for i in range (self.network.getSize()):
        #     if (network.getLayer(i).isInput()):
        #         self.input_layer_map[i] = 1
        
        self.target_map = []
        self.source_map = []
        for i in range (self.network.getSize()):
            self.target_map.append([])
            self.source_map.append([])
        
        
    def mapLayer (self, layer_id, core_coordinate):
        #map layer layer_id to core core_coordinate
    
        self.count_map[core_coordinate[0]][core_coordinate[1]][layer_id] += self.network.getLayer(layer_id).getSize()
        self.spikes_map[core_coordinate[0]][core_coordinate[1]][layer_id] += self.network.getLayer(layer_id).getSpikeSum()
        self.SOPs_map[core_coordinate[0]][core_coordinate[1]] [layer_id] += self.network.getLayer(layer_id).getSOPs() * self.network.getLayer(layer_id).getSize()
        self.synapse_cost_map[core_coordinate[0]][core_coordinate[1]] +=  self.network.getLayer(layer_id).getSynapseCost() * self.network.getLayer(layer_id).getSize()
        self.neuron_cost_map[core_coordinate[0]][core_coordinate[1]] += self.network.getLayer(layer_id).getNeuronsCost()
        
            
    
    def mapNeuron (self, layer_id, neuron_id, core_coordinate):
  #map neuron [neuron_id, layer_id] to core core_coordinate
        
        self.count_map[core_coordinate[0]][core_coordinate[1]][layer_id] += 1
        self.spikes_map[core_coordinate[0]][core_coordinate[1]][layer_id] += self.network.getLayer(layer_id).getNeuron(neuron_id)
        self.SOPs_map[core_coordinate[0]][core_coordinate[1]][layer_id] += self.network.getLayer(layer_id).getSOPs() 
        self.synapse_cost_map[core_coordinate[0]][core_coordinate[1]] +=  self.network.getLayer(layer_id).getSynapseCost()
        self.neuron_cost_map[core_coordinate[0]][core_coordinate[1]] += self.network.getLayer(layer_id).isNeuron()     
        

    
    def finalizeMapping (self):
    # Generate target maps


            
        for idx in range (self.network.getSize()):
            for x in range(self.mesh_config[0]):
                for y in range(self.mesh_config[1]):
                    count_map = 0
                    for connection in network.mapDestinations(idx): 
                        count_map += self.count_map[x][y][connection]
                    if(count_map != 0):
                        self.target_map[idx].append(Target((x,y), count_map))
                            
            for x in range(self.mesh_config[0]):
                for y in range(self.mesh_config[1]):
                    if(self.count_map[x][y][idx] != 0):
                       # print(idx)
                        self.source_map[idx].append(Source((x,y), self.count_map[x][y][idx], self.spikes_map[x][y][idx], self.SOPs_map[x][y][idx]))                        

                            
                            
    def getSources (self):
        return self.source_map
    
    def getTargets(self):
        return self.target_map
                            
    def getTargets (self, layer_id):
        return self.target_map[layer_id]
    
    def getSources (self, layer_id):
        return self.source_map [layer_id]    
                    
        
                            
                            
 
    # def isInput (self, layer_id):
    #     return self.input_layer_map[layer_id]
        
traces = TraceGenerator (['data\imagesb0.npy', 'data\hs1b0.npy', 'data\hs2b0.npy']) 
print('Original: ' + str(traces.getOriginalTraces()[0].shape))
print('Average: ' + str(traces.getAverageTraces()[0].shape))
print('Sum over neurons and time = ' + str(np.sum(traces.getAverageTraces()[0])))
print('Max: ' + str(traces.getMaxTraces()[0].shape))
print('Sum over neurons and time = ' + str(np.sum(traces.getMaxTraces()[0])))
print('Average, time average: ' + str(traces.getAverageAverageTraces()[0].shape))
print('Sum over neurons and time = ' + str(np.sum(traces.getAverageAverageTraces()[0])))
print('Average, worst-case time: ' + str(traces.getAverageMaxTraces()[0].shape))
print('Sum over neurons and time = ' + str(np.sum(traces.getAverageMaxTraces()[0])))
print('Max, time-average: ' + str(traces.getMaxAverageTraces()[0].shape))
print('Sum over neurons and time = ' + str(np.sum(traces.getMaxAverageTraces()[0])))
print('Max, worst-timestep: ' + str(traces.getMaxMaxTraces()[0].shape))
print('Sum over neurons and time = ' + str(np.sum(traces.getMaxMaxTraces()[0])))
        
network = Network(traces, output_layers = [20], case_simulation = "Max", time_simulation = "Average")


network.connect(0,1)
network.connect(1,1)
network.connect(1,2)
network.connect(2,2)
network.connect(2,3)

mapper = Mesh_Mapper((2,2), network)
mapper.mapLayer(0,(0,0))
mapper.mapLayer(1,(0,1))
mapper.mapLayer(2,(1,0))
mapper.mapLayer(3,(1,1))
mapper.finalizeMapping()

