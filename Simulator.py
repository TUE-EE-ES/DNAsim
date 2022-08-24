# -*- coding: utf-8 -*-

from DNAsim.Mapper import *
from DNAsim.Hardware import *
        
        
class Simulator:

    def __init__ (self, mapper, hardware_model):
    # Note: Mapping should be already FINALIZED (mapper.finalizeMapping())
        self.mapper = mapper
        self.hardware_model = hardware_model
        self.transaction_queue = []

    def fast_run(self):

        for layer_id in range(self.mapper.network.getSize()):
            if(not self.mapper.network.getLayer(layer_id).isOutput()):
                layer_sources = self.mapper.getSources(layer_id)
                layer_targets = self.mapper.getTargets(layer_id)
                self.hardware_model.issue_fast_transactions(layer_sources, layer_targets)

    def slow_run(self):
        
        for layer_id in range(self.mapper.network.getSize()):
            layer_sources = self.mapper.getSources(layer_id)
            layer_targets = self.mapper.getTargets(layer_id)
            self.hardware_model.issue_slow_transactions(layer_sources, layer_targets, self.transaction_queue)
        
        while(self.transaction_queue):
            transaction = self.transaction_queue.pop()            
            self.hardware_model.push_transaction(transaction, self.transaction_queue)
            
        
        
    def plot(self):
        self.hardware_model.plotNeurons()
        self.hardware_model.plotSynapses()
        self.hardware_model.plotSOPs()        
        self.hardware_model.plotSpikesInTotal()        
        self.hardware_model.plotSpikesIn()
        self.hardware_model.plotSpikesInFB()  
        self.hardware_model.plotSpikesOut()
        self.hardware_model.plotFires()        
        self.hardware_model.plotHOPs()        
        self.hardware_model.plotLinks(0)
        self.hardware_model.plotLinks(1)
        self.hardware_model.plotLinks(2)
        self.hardware_model.plotLinks(3)        
        
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
network = Network(traces, output_layers = [20], case_simulation = "Average", time_simulation = "None")

network.connect(0,1)
network.connect(1,1)
network.connect(1,2)
network.connect(2,2)
network.connect(2,3)

mapper_1 = Mesh_Mapper((4,3), network)
mapper_1.mapLayer(0,(0,0))
mapper_1.mapLayer(3,(0,0))
for i in range (21):
    mapper_1.mapNeuron(1, i, (1,0))
    mapper_1.mapNeuron(1, i + 21, (2,0))
    mapper_1.mapNeuron(1, i + 2*21, (3,0))
    mapper_1.mapNeuron(1, i + 3*21, (1,1))
    mapper_1.mapNeuron(1, i + 4*21, (2,1))
    mapper_1.mapNeuron(1, i + 5*21, (3,1))
mapper_1.mapNeuron(1, 126, (1,0))
mapper_1.mapNeuron(1, 127, (2,0))

for i in range (64):
    mapper_1.mapNeuron(2, 2*i, (1,2))
    mapper_1.mapNeuron(2, 2*i+1, (2,2))

    

mapper_1.finalizeMapping()

noc = NoC ((4,3), NoC_DSD_Model(), Tile_DSD_Model())

sim = Simulator(mapper_1, noc)
sim.fast_run()
sim.plot()




