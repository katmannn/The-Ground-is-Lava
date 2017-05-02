#!/usr/bin/python2

import random

def maze_gen(start_coords=(0,0), n=3, m=3):
    coords = start_coords
    visited = [ [0 for i in range(m)] for k in range(n) ]

    adj_list = [coords]
    edges = []

    visited_count = 0
    start = 1
    
    while visited_count < n*m:
        while True:
            ind = random.randint(0, len(adj_list)-1)
            coords = adj_list.pop(ind)
            if visited[coords[0]][coords[1]] == 0:
                break
        visited[coords[0]][coords[1]] = 1
        visited_count += 1
        direct_adj_list = []
        for new_coords in [ (coords[0]+1, coords[1]),
                            (coords[0]-1, coords[1]),
                            (coords[0], coords[1]+1),
                            (coords[0], coords[1]-1) ]:
            #print(new_coords)
            if (new_coords[0] >= n or new_coords[0] < 0) \
                or (new_coords[1] >= m or new_coords[1] < 0):
                pass
            else: 
                if visited[new_coords[0]][new_coords[1]] == 0:
                    adj_list.append(new_coords)
                else:
                    direct_adj_list.append(new_coords)

        if not start:
            ind = random.randint(0, len(direct_adj_list)-1)
            edges.append( (coords, direct_adj_list[ind]) )

        start = 0
        

    return edges

if __name__ == '__main__':
    e = maze_gen()
    for i in e:
        print i
        
        
            
                
        

