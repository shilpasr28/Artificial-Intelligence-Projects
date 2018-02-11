# -*- coding: utf-8 -*-
"""
Created on Wed May 31 20:57:11 2017

@author: SHILPASHREE RAO
Email-id: shilpasr@usc.edu
"""

import sys
with open(sys.argv[2]) as file:
    lines = file.read().splitlines()
    file.close()
    
    method = lines[0]
    fuel = int(lines[1])
    start_name = lines[2]
    dest_name = lines[3]
    graphlines = lines[4:]
    dict_graph = dict()
    for line in graphlines:
        curr = line.split(':')
        curr_node = curr[0]
        curr_map = curr[1].split(',')    
        node_list = []
        for subline in curr_map:
            sub = subline.split('-')
            sub_info = [sub[0][1:], int(sub[1])]
            node_list.append(sub_info)
        dict_graph[curr_node] = node_list

############################################################################### 
#Breadth First Search
#Reference : https://stackoverflow.com/questions/8922060/how-to-trace-the-path-in-a-breadth-first-search

def BFS_func(f, start, dest, graph):
    output = ''
    queue = [[start]]
    queue_cost = [f]
    visited = []
    neighbor_list = [start]
    neighbor_cost = [0]
    frontier = [start]
    
    while queue:
        frontier.pop(0)
        path = queue.pop(0)
        path_cost = queue_cost.pop(0)
        vertex = path[-1]
        visited.append(vertex)
        if vertex == dest:
            for iter in range(len(path)-1):
                output += path[iter] + '-'
            output += path[-1]+' '+str(path_cost)
            out = open("output.txt", "wb")
            out.write(output)
            return                   
        
        neighbor_list = []
        neighbor_cost = []
        for neighbor in graph[vertex]:
            if neighbor[0] not in visited:
                neighbor_list.append(neighbor[0]) 
                neighbor_cost.append(neighbor[1])
        if(len(neighbor_list)==0):
            continue
        sort = sorted(neighbor_list)
        indexes = sorted(range(len(neighbor_list)), key=lambda k: neighbor_list[k])
        sort_fuel = [neighbor_cost[x] for x in indexes]
        it = 0
        for current_neighbor in sort:
            if current_neighbor not in visited and current_neighbor not in frontier:
                new_path = list(path)
                new_path.append(current_neighbor) 
                curr_fuel = path_cost
                if(curr_fuel < sort_fuel[it]):
                    it = it + 1
                    continue
                
                else:                                  
                    queue_cost.append(curr_fuel-sort_fuel[it])
                    queue.append(new_path)
                    frontier.append(current_neighbor)                    
                    it = it + 1
    output = 'No Path'
    out = open("output.txt", "wb")
    out.write(output)
    return                                      

#End of Breadth First Search
###############################################################################

###############################################################################
#Depth First Search

def DFS_func(f, start, dest, graph):
    output = ''
    queue = [[start]]
    queue_cost = [f]
    visited = []
    neighbor_list = [start]
    neighbor_cost = [0]
    frontier = [start]
    
    while queue:
        frontier.pop(0)
        path = queue.pop(0)
        path_cost = queue_cost.pop(0)
        vertex = path[-1]
        visited.append(vertex)
        if vertex == dest:
            for iter in range(len(path)-1):
                output += path[iter] + '-'
            output += path[-1]+' '+str(path_cost)
            out = open("output.txt", "wb")
            out.write(output)
            return                   
        
        neighbor_list = []
        neighbor_cost = []
        for neighbor in graph[vertex]:
            if neighbor[0] not in visited:
                neighbor_list.append(neighbor[0]) 
                neighbor_cost.append(neighbor[1])
        if(len(neighbor_list)==0):
            continue
        sort = sorted(neighbor_list)
        indexes = sorted(range(len(neighbor_list)), key=lambda k: neighbor_list[k])
        sort_fuel = [neighbor_cost[x] for x in indexes]
        it = 0
        list_neighbor_nodes = []
        list_neighbor_costs = []
        frontier_local = []
        for current_neighbor in sort:
            if current_neighbor not in visited:
                new_path = list(path)
                new_path.append(current_neighbor) 
                curr_fuel = path_cost
                if(curr_fuel < sort_fuel[it]):
                    it = it + 1
                    continue
                else:   
                    list_neighbor_nodes.append(new_path)
                    list_neighbor_costs.append(curr_fuel-sort_fuel[it])
                    frontier_local.append(current_neighbor)                               
                    it = it + 1
        queue_cost[0:0] = list_neighbor_costs
        queue[0:0] = list_neighbor_nodes  
        frontier[0:0] = frontier_local
    output = 'No Path'
    out = open("output.txt", "wb")
    out.write(output)
    return                 

#End of Depth First Search
###############################################################################  

###############################################################################
#Uniform Cost Search

def UCS_func(f, start, dest, graph):
    output = ''
    queue = [[start]]
    queue_cost = [0]
    visited = []
    neighbor_list = [start]
    neighbor_cost = [0]
    frontier = [start]
    frontier_cost = {start: 0}
    
    while queue:
        foo1 = frontier.pop(0)
        frontier_cost.pop(foo1)
       
        path = queue.pop(0)
        path_cost = queue_cost.pop(0)
        vertex = path[-1]
        visited.append(vertex)
        if vertex == dest:
            for iter in range(len(path)-1):
                output += path[iter] + '-'
            #output += path[-1]+' '+str(path_cost)
            output += path[-1]+' '+str(f-path_cost)
            
            out = open("output.txt", "wb")
            out.write(output)
            return
        
        neighbor_list = []
        neighbor_cost = []
        for neighbor in graph[vertex]:
            if neighbor[0] not in visited:
                neighbor_list.append(neighbor[0]) 
                neighbor_cost.append(neighbor[1])    
        if(len(neighbor_list)==0):
            continue
        sort_fuel = sorted(neighbor_cost)
        indexes = sorted(range(len(neighbor_cost)), key=lambda k: neighbor_cost[k])
        sort = [neighbor_list[x] for x in indexes]
        it = 0
        for current_neighbor in sort:
            new_path = list(path)
            new_path.append(current_neighbor) 
            curr_fuel = path_cost
            if((f-curr_fuel) < sort_fuel[it]):
                it = it + 1
                continue
            else:   
                if current_neighbor in frontier:
                    for i, j in enumerate(frontier):
                        if j == current_neighbor:
                            if(sort_fuel[it]<frontier_cost[frontier[i]]):
                                frontier[i] = current_neighbor
                                queue[i] = new_path
                                queue_cost[i] = curr_fuel + sort_fuel[it]
                                frontier_cost[frontier[i]] = sort_fuel[it]
                                it = it + 1
                else:                   
                    queue_cost.append(curr_fuel + sort_fuel[it])
                    queue.append(new_path)
                    frontier.append(current_neighbor)
                    queue_cost = sorted(queue_cost)
                    indexes = sorted(range(len(queue_cost)), key=lambda k: queue_cost[k])
                    queue = [queue[x] for x in indexes] 
                    frontier = [frontier[x] for x in indexes]  
                    frontier_cost[current_neighbor] = sort_fuel[it]                                    
                    it = it+1 
    output = 'No Path'
      
    out = open("output.txt", "wb")
    out.write(output) 
    return                     
            
#End of Uniform Cost Search
###############################################################################
                
if method=='BFS':
     BFS_func(fuel, start_name, dest_name, dict_graph) 
elif method=='DFS':
     DFS_func(fuel, start_name, dest_name, dict_graph)
elif method=='UCS':
     UCS_func(fuel, start_name, dest_name, dict_graph)       