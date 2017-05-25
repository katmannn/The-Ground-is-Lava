#!/usr/bin/python2

import random

#Prim-Jarnik algorithm for maze generation:
#https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_Prim.27s_algorithm


def maze_gen(start_coords=(0,0), n=3, m=3):
    coords = start_coords
    #Mark all nodes as unvisited
    visited = [ [0 for i in range(m)] for k in range(n) ]

    adj_list = [coords]
    edges = []

    visited_count = 0
    start = 1 #Marking start node as special case
    
    while visited_count < n*m: #Until we have visited every node
        #Pop random nodes off the adjacent list until we find an unvisited one
        while True:
            ind = random.randint(0, len(adj_list)-1)
            coords = adj_list.pop(ind)
            if visited[coords[0]][coords[1]] == 0:
                break
        #Mark the node as visited
        visited[coords[0]][coords[1]] = 1
        visited_count += 1

        #This list represents all the candidate edges to add to the
        #MST (The maze). Having popped off coords from the adj_list we know 
        #that it was adjacent to SOME node already visited.
        direct_adj_list = []

        #Look at all possible adjacent cells
        for new_coords in [ (coords[0]+1, coords[1]),
                            (coords[0]-1, coords[1]),
                            (coords[0], coords[1]+1),
                            (coords[0], coords[1]-1) ]:
            #If out of bounds, ignore
            if (new_coords[0] >= n or new_coords[0] < 0) \
                or (new_coords[1] >= m or new_coords[1] < 0):
                pass
            else: 
                #If we find any new, unvisited adjacent nodes,
                #add them to the list (admittedly, a dict would
                #be better for this in terms of complexity, but
                #a list works despite possible repitition of nodes)
                if visited[new_coords[0]][new_coords[1]] == 0:
                    adj_list.append(new_coords)
                #Visited nodes are ones we want to create an edge to
                else:
                    direct_adj_list.append(new_coords)

        #The start node doesn't have any cells to connect to
        if not start:
            #Basically: "Pick a random edge to add to the MST"
            #For a given cell, pick which wall to "break"
            ind = random.randint(0, len(direct_adj_list)-1)
            edges.append( (coords, direct_adj_list[ind]) )

        start = 0
        

    return edges

if __name__ == '__main__':
    e = maze_gen()
    for i in e:
        print i
        
        
            
                
        

