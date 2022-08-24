# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt    

MODEL = "LOIHI"


    ## Note: User can define a direction-wise hop model by utilizing HOPS_linkwise array ##
if (MODEL == "LOIHI"):
    SOP_TIME = 3.5 #ns
    SOP_ENERGY = 24 #pJ
    HOP_ENERGY = 4.0 #pJ
    NEURON_UPDATE_TIME = 5.3 #ns
    NEURON_UPDATE_ENERGY = 52 #pJ
    NEURON_SPIKE_TIME = 3.1 #ns    
    NEURON_SPIKE_ENERGY = 29 #pJ

elif (MODEL == "MORPHIC"):
    SOP_TIME = 36 #ns
    SOP_ENERGY = 30 #pJ
    HOP_ENERGY = 9.0 #pJ    
    NEURON_UPDATE_TIME = 0
    NEURON_UPDATE_ENERGY = 0
    NEURON_SPIKE_TIME = 0
    NEURON_SPIKE_ENERGY = 0 
    
WEST = 0
EAST = 1
NORTH = 2
SOUTH = 3

class Tile:
    
    def __init__ (self, tile_model):
        
        self.tile_model = tile_model
        self.SOPs = None
        self.spikes_out = None
        self.spikes_in = None
        self.feedback_spikes = None
        self.fires = None
        self.HOPs_WEST = None
        self.HOPs_EAST = None
        self.HOPs_SOUTH = None
        self.HOPs_NORTH = None    
        self.neuron_mem = 0
        self.synapse_mem = 0
        self.latency = None
        self.energy = None




######## Record activity APIs ###########
    def recordHOPsNorth(self, packet_size):
        if(self.HOPs_NORTH is None):
            self.HOPs_NORTH = packet_size
        else:           
            self.HOPs_NORTH += packet_size

    def recordHOPsSouth(self, packet_size):
        if(self.HOPs_SOUTH is None):
            self.HOPs_SOUTH = packet_size
        else:           
            self.HOPs_SOUTH += packet_size
            
    def recordHOPsWest(self, packet_size):
        if(self.HOPs_WEST is None):
            self.HOPs_WEST = packet_size
        else:           
            self.HOPs_WEST += packet_size

    def recordHOPsEast(self, packet_size):
        if(self.HOPs_EAST is None):
            self.HOPs_EAST = packet_size
        else:           
            self.HOPs_EAST += packet_size            
      
    def recordSOPs(self, SOPs):
        
        if(self.SOPs is None):
            self.SOPs = SOPs
        else:
            self.SOPs += SOPs
            
    def recordSpikeOut(self,  spikeRate):
        if(self.spikes_out is None):
            self.spikes_out = spikeRate            
        else:
            self.spikes_out += spikeRate
            
    def recordSpikeIn(self, spikeRate):
        
        if(self.spikes_in is None):
            self.spikes_in = spikeRate
        else:
            self.spikes_in += spikeRate
            
    def recordFires(self, fireRate):
        if(self.fires is None):
            self.fires = fireRate
        else:
            self.fires += fireRate
             
    def recordSpikesFeedback (self, spikeRate):
        if(self.feedback_spikes is None):
            self.feedback_spikes = spikeRate
        else:
            self.feedback_spikes += spikeRate        
            
    def recordNeurons (self, neurons):
        self.neuron_mem += neurons
    def recordSynapses(self, synapses):
        self.synapse_mem += synapses        
######################################################       
    ### Estimation model wrapper functions #####
        
    def measureLatency(self):
        
        self.tile_model.measureLatency(self)
        
    def measureEnergy(self):
        self.tile_model.measureEnergy(self)
        
#####################################################
        
        ## Plotting functions ##
        
    def plotSpikesIn(self):
        return self.spikes_in
    def plotSpikesInFB(self):
        return self.feedback_spikes
    def plotSpikesInTotal(self):
        return self.spikes_in + self.feedback_spikes    
 
    def plotSpikesOut(self):
        return self.spikes_out
    def plotFires(self):
        return self.fires
    
    def plotNeurons(self):
        return self.neuron_mem
    
    def plotSynapses(self):
        return self.synapse_mem
    
    def plotSOPs (self):
        return self.SOPs
    
    def plotHOPs (self):
        return self.HOPs_EAST + self.HOPs_WEST + self.HOPs_NORTH + self.HOPs_SOUTH
    
    def plotHOPs_West (self):
        return self.HOPs_WEST

    def plotHOPs_East (self):
        return self.HOPs_EAST

    def plotHOPs_North (self):
        return self.HOPs_NORTH
    def plotHOPs_South (self):
        return self.HOPs_SOUTH    
    


    def plotLatency(self):
        pass
        
        
        
        
class Tile_DSD_Model:
    
    def __init__ (self):
        pass
    
        
    def measureLatency (self, tile):
        return SOP_TIME * tile.SOPs + NEURON_UPDATE_TIME * tile.neuron_mem + NEURON_SPIKE_TIME * tile.spikes
    
    def measureEnergy (self, tile):
        return HOP_ENERGY * tile.HOPs + SOP_ENERGY * tile.SOPs + NEURON_UPDATE_ENERGY * tile.neuron_mem + NEURON_SPIKE_ENERGY * tile.spikes
    
    # def spike_Size_Model (self, spikeRate, target_count):
        
    #     ## Use this function to define spike packet information (e.g spike header, etc)
    #     ## No conversions implemented, 1 spike = 1 unit, 1 target = 1 unit (e.g 1 unit = 16 bits packet)
    #     return spikeRate + target_count
    
##########################################
        
    
class NoC:
    
    
    def __init__ (self, mesh_dimensions, NoC_model, tile_model):
        
        self.NoC_model = NoC_model
        
        self.x = mesh_dimensions[0]
        self.y = mesh_dimensions[1]
        
        self.tile_array = []
        for x in range (self.x):
            tile_array1D = []
            for y in range(self.y):
                tile_array1D.append(Tile(tile_model))
            self.tile_array.append(tile_array1D)
            
    
    def getTile(self, tile_coordinate):
        
        return self.tile_array[tile_coordinate[0]][tile_coordinate[1]]
    
    def issue_fast_transactions (self, layer_sources, layer_targets):
        
        self.NoC_model.execute(self, layer_sources, layer_targets)

    def plotSpikesIn (self, publish = None, legends = True):
        fig2, ax2 = plt.subplots()                  
        plt.ylabel('Spike in') 
        bar_plot = []
        labels = []
        for j in range(self.y):
            for i in range(1, self.x):
                plot = self.getTile((i,j)).plotSpikesIn()
                if(plot.shape == (1,)):
                    bar_plot.append(plot.item(0))
                    labels.append('('+str(i)+', '+str(j) + ')')
                else:
                    ax2.plot(plot, label = '('+str(i)+', '+str(j)+')')
        if(len(bar_plot) == 0):
            plt.xlabel('Algorithmic timestep')            
            if (legends):
                ax2.legend()
        else:
            plt.xlabel('Core id')
            ax2.bar(labels, bar_plot)
        if (publish != None):
            plt.savefig('Experiment_'+str(publish) + '_spikes_in.pdf')
        return plt                       
    
    def plotSpikesInFB (self, publish = None, legends = True):
        fig2, ax2 = plt.subplots()                  
        plt.ylabel('FB Spikes') 
        bar_plot = []
        labels = []
        for j in range(self.y):
            for i in range(1, self.x):
                plot = self.getTile((i,j)).plotSpikesInFB()
                if(plot.shape == (1,)):
                    bar_plot.append(plot.item(0))
                    labels.append('('+str(i)+', '+str(j) + ')')
                else:
                    ax2.plot(plot, label = '('+str(i)+', '+str(j)+')')
        if(len(bar_plot) == 0):
            plt.xlabel('Algorithmic timestep')            
            if (legends):
                ax2.legend()
        else:
            plt.xlabel('Core id')
            ax2.bar(labels, bar_plot)
        if (publish != None):
            plt.savefig('Experiment_'+str(publish) + '_spikes_fb.pdf')
        return plt  
    
    def plotSpikesInTotal (self, publish = None, legends = True):
        fig2, ax2 = plt.subplots()                  
        plt.ylabel('Spike in total') 
        bar_plot = []
        labels = []
        for j in range(self.y):
            for i in range(1, self.x):
                plot = self.getTile((i,j)).plotSpikesInTotal()
                if(plot.shape == (1,)):
                    bar_plot.append(plot.item(0))
                    labels.append('('+str(i)+', '+str(j) + ')')
                else:
                    ax2.plot(plot, label = '('+str(i)+', '+str(j)+')')
        if(len(bar_plot) == 0):
            plt.xlabel('Algorithmic timestep')            
            if (legends):
                ax2.legend()
        else:
            plt.xlabel('Core id')
            ax2.bar(labels, bar_plot)
        if (publish != None):
            plt.savefig('Experiment_'+str(publish) + '_spikes_in_total.pdf')
        return plt      
    
    def plotSpikesOut (self, publish = None, legends = True):
        fig2, ax2 = plt.subplots()                  
        plt.ylabel('Spikes out') 
        plt.xlabel('Algorithmic timestep')
        bar_plot = []
        labels = []

        for j in range(self.y):
            for i in range(1, self.x):
                plot = self.getTile((i,j)).plotSpikesOut()
                if(plot.shape == (1,)):
                    bar_plot.append(plot.item(0))
                    labels.append('('+str(i)+', '+str(j) + ')')
                else:
                    ax2.plot(plot, label = '('+str(i)+', '+str(j)+')')
        if(len(bar_plot) == 0):
            plt.xlabel('Algorithmic timestep')            
            if (legends):
                ax2.legend()
        else:
            plt.xlabel('Core id')
            ax2.bar(labels, bar_plot)
        if (publish != None):
            plt.savefig('Experiment_'+str(publish) + '_spikes_out.pdf')
        return plt         
                   

    def plotFires (self, publish = None, legends = True):
        fig2, ax2 = plt.subplots()                  
        plt.ylabel('Fires') 
        plt.xlabel('Algorithmic timestep')
        bar_plot = []
        labels = []

        for j in range(self.y):
            for i in range(1, self.x):
                plot = self.getTile((i,j)).plotFires()
                if(plot.shape == (1,)):
                    bar_plot.append(plot.item(0))
                    labels.append('('+str(i)+', '+str(j) + ')')
                else:
                    ax2.plot(plot, label = '('+str(i)+', '+str(j)+')')
        if(len(bar_plot) == 0):
            plt.xlabel('Algorithmic timestep')            
            if (legends):
                ax2.legend()
        else:
            plt.xlabel('Core id')
            ax2.bar(labels, bar_plot)
        if (publish != None):
            plt.savefig('Experiment_'+str(publish) + '_fires.pdf')
        return plt 
    
    def plotSOPs (self, publish = None, legends = True):
        fig2, ax2 = plt.subplots()                  
        plt.ylabel('SOPs') 
        bar_plot = []
        labels = []
        for j in range(self.y):
            for i in range(1, self.x):
                plot = self.getTile((i,j)).plotSOPs()
                if(plot.shape == (1,)):
                    bar_plot.append(plot.item(0))
                    labels.append('('+str(i)+', '+str(j) + ')')
                else:
                    ax2.plot(plot, label = '('+str(i)+', '+str(j)+')')
        if(len(bar_plot) == 0):
            plt.xlabel('Algorithmic timestep')            
            if (legends):
                ax2.legend()
        else:
            plt.xlabel('Core id')
            ax2.bar(labels, bar_plot)
        if (publish != None):
            plt.savefig('Experiment_'+str(publish) + '_SOPs.pdf')
        return plt     
    
    def plotHOPs (self, publish = None, legends = True):
        fig2, ax2 = plt.subplots()                  
        plt.ylabel('HOPs') 
        bar_plot = []
        labels = []
        for j in range(self.y):
            for i in range(1, self.x):
                plot = self.getTile((i,j)).plotHOPs()
                if(plot.shape == (1,)):
                    bar_plot.append(plot.item(0))
                    labels.append('('+str(i)+', '+str(j) + ')')
                else:
                    ax2.plot(plot, label = '('+str(i)+', '+str(j)+')')
        if(len(bar_plot) == 0):
            plt.xlabel('Algorithmic timestep')            
            if (legends):
                ax2.legend()
        else:
            plt.xlabel('Core id')
            ax2.bar(labels, bar_plot)
        if (publish != None):
            plt.savefig('Experiment_'+str(publish) + '_HOPs.pdf')
        return plt  
   
    def plotNeurons (self, publish = None):
        fig2, ax2 = plt.subplots()                  
        plt.ylabel('Neurons') 
        bar_plot = []
        labels = []
        for j in range(self.y):
            for i in range(1, self.x):
                plot = self.getTile((i,j)).plotNeurons()
                bar_plot.append(plot.item(0))
                labels.append('('+str(i)+', '+str(j) + ')')

        plt.xlabel('Core id')
        ax2.bar(labels, bar_plot)
        if (publish != None):
            plt.savefig('Experiment_'+str(publish) + '_neurons.pdf')
        return plt 

    def plotSynapses (self, publish = None):
        fig2, ax2 = plt.subplots()                  
        plt.ylabel('Synapses') 
        bar_plot = []
        labels = []
        for j in range(self.y):
            for i in range(1, self.x):
                plot = self.getTile((i,j)).plotSynapses()
                bar_plot.append(plot.item(0))
                labels.append('('+str(i)+', '+str(j) + ')')

        plt.xlabel('Core id')
        ax2.bar(labels, bar_plot)
        if (publish != None):
            plt.savefig('Experiment_'+str(publish) + '_synapses.pdf')
        return plt 

    def plotLinks (self, link_index, publish = None, legends = True):
        fig2, ax2 = plt.subplots()                  
        plt.ylabel('Hops') 
        plt.xlabel('Algorithmic timestep') 
        if(link_index == 1):
            plot_title = 'East'
        elif(link_index == 0):
            plot_title = 'West'
        elif(link_index == 2):
            plot_title = 'North'
        elif(link_index == 3):
            plot_title = 'South'
        plt.title(plot_title)
        plt.ylabel('HOPs') 
        bar_plot = []
        labels = []
        for j in range(self.y):
            for i in range(1, self.x):
                if(link_index == 0):
                    plot = self.getTile((i,j)).plotHOPs_West()
                elif(link_index == 1):
                    plot = self.getTile((i,j)).plotHOPs_East()
                elif(link_index == 2):
                    plot = self.getTile((i,j)).plotHOPs_North()
                elif(link_index == 3):
                    plot = self.getTile((i,j)).plotHOPs_South()                    
                if(plot.shape == (1,)):
                    bar_plot.append(plot.item(0))
                    labels.append('('+str(i)+', '+str(j) + ')')
                else:
                    ax2.plot(plot, label = '('+str(i)+', '+str(j)+')')
        if(len(bar_plot) == 0):
            plt.xlabel('Algorithmic timestep')            
            if (legends):
                ax2.legend()
        else:
            plt.xlabel('Core id')
            ax2.bar(labels, bar_plot)
        if (publish != None):
            plt.savefig('Experiment_'+str(publish) + '_HOPs_link_' + plot_title + '.pdf')
        return plt  
    
CASTING_MODE = "MULTI"
SPIKE_SIZE = 2 #Bytes
ROUTE_OVERHEAD = 2 #Bytes
class NoC_DSD_Model:
    
    def __init__ (self):
        pass
    
    def execute(self, NoC, layer_sources, layer_targets):
        if (CASTING_MODE == "MULTI"):
            self.execute_multicast(NoC, layer_sources, layer_targets)
        


    def execute_multicast(self, NoC, layer_sources, layer_targets):
        
    # Parallelizable implementation of multicast XY routing
        
        for x in range(NoC.x):
            for y in range(NoC.y):
                SOPs = np.zeros(layer_sources[0].spikerate.shape)
                HOPs_east = np.zeros(layer_sources[0].spikerate.shape)
                HOPs_west = np.zeros(layer_sources[0].spikerate.shape)
                HOPs_north = np.zeros(layer_sources[0].spikerate.shape)
                HOPs_south = np.zeros(layer_sources[0].spikerate.shape)
                spikes_in = np.zeros(layer_sources[0].spikerate.shape)
                feedback_spikes = np.zeros(layer_sources[0].spikerate.shape)
                
                spikes_out = np.zeros(layer_sources[0].spikerate.shape)
                fire_rate = np.zeros(layer_sources[0].spikerate.shape)
 
                synapses = np.zeros(layer_sources[0].spikerate.shape)
                neurons = np.zeros(layer_sources[0].spikerate.shape)
            
                c = (x,y)
                    
                # print(c)
                for source in layer_sources:
                    
                    spike_overhead = 0
                    s = source.core_coordinate

                    if(c[0] == s[0] and c[1] == s[1]):
                        fb_flag = False
                        fire_rate += source.spikerate
                        neurons += source.count
                        for target in layer_targets:
                            t = target.core_coordinate
                            if(t == s):
                                SOPs += source.spikerate * target.count
                                synapses += source.count * target.count
                                fb_flag = True

                            else:
                                spike_overhead += 1
                        if(spike_overhead != 0):
                            spikes_out += (source.spikerate * SPIKE_SIZE) + (spike_overhead * ROUTE_OVERHEAD)
                        if(fb_flag):
                            feedback_spikes += source.spikerate * SPIKE_SIZE
                    elif(s[1] == c[1]):                           
                        if(s[0] > c[0]):
                            for target in layer_targets:
                                t = target.core_coordinate                        
                                if (c[0] >= t[0]):
                                    spike_overhead += 1
                                    if(c == t):
                                        spikes_in += source.spikerate * SPIKE_SIZE
                                        SOPs += source.spikerate * target.count
                                        synapses += source.count * target.count
                            if(spike_overhead != 0):
                                HOPs_east += (source.spikerate * SPIKE_SIZE) + (spike_overhead * ROUTE_OVERHEAD)
                        else:                        
                            for target in layer_targets:
                                t = target.core_coordinate
                                if (c[0] <= t[0]):
                                    
                                    spike_overhead += 1
                                    if(c == t):
                                        spikes_in += source.spikerate * SPIKE_SIZE
                                        SOPs += source.spikerate * target.count
                                        synapses += source.count * target.count
                                        
                            if(spike_overhead != 0):
                                HOPs_west += (source.spikerate * SPIKE_SIZE) + (spike_overhead * ROUTE_OVERHEAD)                                            
                    else:
                        for target in layer_targets:
                            t = target.core_coordinate
                            if(c[0] == t[0]):
                                if(s[1] > c[1] and c[1] >= t[1]):
                                    spike_overhead += 1
                                    if (c[1] == t[1]):
                                        spikes_in += source.spikerate * SPIKE_SIZE
                                        SOPs += source.spikerate * target.count
                                        synapses += source.count * target.count
                                        
                                elif (s[1] < c[1] and c[1] <= t[1]):
                                    spike_overhead += 1
                                    if (c[1] == t[1]):
                                        spikes_in += source.spikerate * SPIKE_SIZE
                                        SOPs += source.spikerate * target.count
                                        synapses += source.count * target.count
                            
                        if(s[1] < c[1]):
                            HOPs_north += (source.spikerate * SPIKE_SIZE * (spike_overhead != 0)) + (spike_overhead * ROUTE_OVERHEAD)
                        else:
                            HOPs_south += (source.spikerate * SPIKE_SIZE * (spike_overhead != 0)) + (spike_overhead * ROUTE_OVERHEAD)
                
                
                #print(HOPs_east)

                #print(HOPs_west)
                #print(NoC.getTile(c).plotHOPs_West())
                NoC.getTile(c).recordHOPsWest(HOPs_west)
                #print(NoC.getTile(c).plotHOPs_West())
                NoC.getTile(c).recordHOPsEast(HOPs_east)
                #print(NoC.getTile(c).plotHOPs_West())
                NoC.getTile(c).recordHOPsNorth(HOPs_north)
                #print(NoC.getTile(c).plotHOPs_West())
                NoC.getTile(c).recordHOPsSouth(HOPs_south)
                #print(NoC.getTile(c).plotHOPs_West())
                NoC.getTile(c).recordSOPs(SOPs)
                NoC.getTile(c).recordSpikeOut(spikes_out)
                NoC.getTile(c).recordSpikeIn(spikes_in)
                NoC.getTile(c).recordSpikesFeedback(feedback_spikes)
                NoC.getTile(c).recordFires(fire_rate)
                
                NoC.getTile(c).recordSynapses(synapses)
                NoC.getTile(c).recordNeurons(neurons)
                
                
                
                                
                    
                                            
                                            
                                    
                                
                                
                        
                                    
    
                                    
                                
        
        
        

class Spike_Message:
    
    def __init__ (self, source_node, target_nodes, latency = None, current_node = None):
        if (latency is None):
            self.latency = 0
        else:
            self.latency = latency
        if (current_node is None):
            self.current_node = source_node
        else:
            self.current_node = current_node
        self.target_nodes = target_nodes
        self.source_node = source_node

    def __gt__(self, other):
        return self.latency > other.latency

        
    def incrementLatency(self, latency):
        self.latency += latency
        
    def setLatency(self, latency):
        self.latency = latency
        
    def move (self, new_node):
        self.current_node = new_node
        



            
            
        
        
            
            
        

        
        
