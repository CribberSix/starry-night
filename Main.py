import pygame
import sys
import random
import numpy as np

# Window
(width, height) = (1200, 800)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Starry Night v0.1')

clock=pygame.time.Clock()
col_background = (31,71,87) # Schritte: (28,23,21)
col_node_1 = (255,255,255)
col_node_2 = (227,232,234)
col_node_3 = (199,209,213)
col_node_4 = (171,186,192)
col_node_5 = (143,163,171)
col_node_6 = (115,140,150)
col_node_7 = (87,117,129)
col_node_8 = (59,94,108)
col_node_9 = (31,71,87)
col_linkage = (33,127,158)
col_triangle = (30,76,94)

nodeArray = []
connectedNodes = []
nodeMovement = []
movement_max = 2
nodeCount = 50
max_connections = 4
lower_linkage_bound_one = 250
lower_linkage_bound_two = 170


for i in range(nodeCount):
    nodeArray.append([random.randint(0, width), random.randint(0, height)]) # create a list of randomly distributed nodes
    speed = [random.randint(-movement_max, movement_max), random.randint(-movement_max, movement_max)]
    if speed[0] == 0 and speed[1] == 0: # no node should not move at all.
        speed[1] = 1
    nodeMovement.append(speed) # each node has its movement (x & y)
    connectedNodes.append([i, 0]) # create a list to keep track of nodes which are connected


def closest_distance(x, y):
    return np.sqrt(((x[0] - y[0])**2) + ((x[1] - y[1])**2))


def get_two_neighbour_nodes(node_index):

    shortest_dist_len_one = 10000000000
    shortest_dist_len_two = 10000000000
    shortest_dist_len_three = 10000000000
    shortest_dist_index_one = None
    shortest_dist_index_two = None
    shortest_dist_index_three = None

    cp = nodeArray[node_index]
    for  index, node in enumerate(nodeArray):
        if node != cp:
            current_dist = closest_distance(cp, nodeArray[index])
            if current_dist < shortest_dist_len_one:

                shortest_dist_len_three = shortest_dist_len_two
                shortest_dist_len_two = shortest_dist_len_one
                shortest_dist_len_one = current_dist

                shortest_dist_index_three = shortest_dist_index_two
                shortest_dist_index_two = shortest_dist_index_one
                shortest_dist_index_one = index

    # Connections which are too long are deleted
    if  (shortest_dist_len_three - shortest_dist_len_one) > lower_linkage_bound_one:
        shortest_dist_index_three = None
    if  (shortest_dist_len_two - shortest_dist_len_one) > lower_linkage_bound_two:
       shortest_dist_index_two = None

    return(node_index, shortest_dist_index_one, shortest_dist_index_two, shortest_dist_index_three)

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(col_background)

    # Move nodes
    for i in range(0,nodeCount):
        nodeArray[i][0] += nodeMovement[i][0]
        nodeArray[i][1] += nodeMovement[i][1] # random.randint(-5,5)
        if nodeArray[i][0] < 0 or nodeArray[i][0] > width:
            nodeMovement[i][0] = nodeMovement[i][0] * (-1)
        if nodeArray[i][1] < 0 or nodeArray[i][1] > height:
            nodeMovement[i][1] = nodeMovement[i][1] * (-1)

    # Reset connection counter
    for i in range(nodeCount):
        connectedNodes[i][1] = 0

    # Draw triangles
    for i in range(0,nodeCount):
        (a,b,c,d) = get_two_neighbour_nodes(i)

        if (None not in [a,b,c]):
            pygame.draw.polygon(screen, col_triangle, [nodeArray[a], nodeArray[b], nodeArray[c]], 0)

     # Draw lines to the two closest nodes and around triangles
    for i in range(nodeCount):
        (a,b,c,d) = get_two_neighbour_nodes(i)

        if b is not None :#and connectedNodes[b][1] < max_connections:
            pygame.draw.line(screen, col_linkage, nodeArray[a], nodeArray[b], 1)
            connectedNodes[b][1] +=1

        if c is not None and connectedNodes[c][1] < max_connections:
            pygame.draw.line(screen, col_linkage, nodeArray[a], nodeArray[c], 1)
            connectedNodes[c][1] +=1

        if d is not None and connectedNodes[d][1] < max_connections:
            pygame.draw.line(screen, col_linkage, nodeArray[a], nodeArray[d], 1)
            connectedNodes[d][1] +=1

        if None not in [b,c]:
            pygame.draw.line(screen, col_linkage, nodeArray[b], nodeArray[c], 1)

    # Draw all nodes
    for circle in nodeArray:
        pygame.draw.circle(screen, col_node_9, (circle[0], circle[1]), 9)
        pygame.draw.circle(screen, col_node_8, (circle[0], circle[1]), 8)
        pygame.draw.circle(screen, col_node_7, (circle[0], circle[1]), 7)
        pygame.draw.circle(screen, col_node_6, (circle[0], circle[1]), 6)
        pygame.draw.circle(screen, col_node_5, (circle[0], circle[1]), 5)
        pygame.draw.circle(screen, col_node_4, (circle[0], circle[1]), 4)
        pygame.draw.circle(screen, col_node_3, (circle[0], circle[1]), 3)
        pygame.draw.circle(screen, col_node_2, (circle[0], circle[1]), 2)
        pygame.draw.circle(screen, col_node_1, (circle[0], circle[1]), 1)

    pygame.display.flip()
    clock.tick(20)