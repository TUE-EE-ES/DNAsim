# -*- coding: utf-8 -*-

import numpy as np

class TraceGenerator:
    
    def __init__ (self, trace_files):
        
        self.traces_original = []
        # input traces, size [M x N x T] each
        
        self.traces_average = []
        # Average-case trace, size [N x T] each
        
        self.traces_max = []
        # Worst-case trace, size [NxT] 
        
        self.traces_average_average = []
        # Average over time of average-case trace, [N] each
        
        self.traces_average_max = []
        # Worst timestep of average-case trace, [N] each
        
        self.traces_max_average = []
        # Average over timesteps of worst-case trace, [N] each
        
        self.traces_max_max = []
        # Worst timestep of the worst-case trace, [N] each
        
        


        for trace in trace_files:
            trace_file = np.load(trace)
            self.traces_original.append(trace_file)
            
            
            
    def getOriginalTraces(self):
        return self.traces_original
        

                
    def getAverageTraces(self):
        if(len(self.traces_average) == 0):
            for trace_file in self.getOriginalTraces():    
                avg_trace = np.average(trace_file, axis = 0)
                self.traces_average.append(avg_trace)
            
        return self.traces_average
    
    def getAverageAverageTraces(self):
        if(len(self.traces_average_average) == 0):
            for average_trace in self.getAverageTraces():               
                avg_avg_trace = np.average(average_trace, axis = 1)
                self.traces_average_average.append(avg_avg_trace)  
        return self.traces_average_average
    
    
    def getAverageMaxTraces(self):
        if(len(self.traces_average_max) == 0):
            avg_sum_traces = []
            for avg_trace in self.getAverageTraces():
                avg_sum = np.sum(avg_trace, axis = 0)
                if(len(avg_sum_traces) == 0):
                    avg_sum_traces = avg_sum
                else:
                    avg_sum_traces += avg_sum
                    
            max_index = np.argmax(avg_sum_traces)
            for trace_avg in self.getAverageTraces():
                trace_avg_transp = np.swapaxes(trace_avg, 0, 1)
                self.traces_average_max.append(trace_avg_transp[max_index])
        return self.traces_average_max
            
    def getMaxTraces(self):
        
        if(len(self.traces_max) == 0):
            sum_traces = []     
            for trace_file in self.getOriginalTraces():
                sum = np.sum(trace_file, axis = 1)
                sum = np.sum(sum, axis = 1)
                if (len(sum_traces) == 0):
                    sum_traces = sum
                else:
                    sum_traces = sum_traces + sum    
            max_index = np.argmax(sum_traces)                           
            for trace_file in self.getOriginalTraces():
                self.traces_max.append(trace_file[max_index])
        return self.traces_max
    
    def getMaxAverageTraces(self):
        
        if(len(self.traces_max_average) == 0):
            for trace_max in self.getMaxTraces():
                self.traces_max_average.append(np.average(trace_max, axis=1))
        return self.traces_max_average


    def getMaxMaxTraces(self):
        if(len(self.traces_max_max) == 0):
            max_sum = []
            for trace_max in self.getMaxTraces():
                max_sum_i = np.sum(trace_max, axis=0)
                if(len(max_sum) == 0):
                    max_sum = max_sum_i
                else:
                    max_sum += max_sum_i
            max_max_index = np.argmax(max_sum)
            for trace_max in self.getMaxTraces():
                trace_max_transp = np.swapaxes(trace_max, 0, 1)
                self.traces_max_max.append(trace_max_transp[max_max_index])
        return self.traces_max_max
                


            
            
            



                          