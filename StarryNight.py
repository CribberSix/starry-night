import pygame
import sys
import random
import numpy as np


class StarryNight:
    def __init__(self, width, height, number_of_nodes=50, surface=pygame.display.get_surface()):
        self.width = width
        self.height = height
        self.screen = surface

        self.clock = pygame.time.Clock()
        self.col_background = (31, 71, 87)

        # Schritte: (28,23,21)
        self.col_node_1 = (255, 255, 255)
        self.col_node_2 = (227, 232, 234)
        self.col_node_3 = (199, 209, 213)
        self.col_node_4 = (171, 186, 192)
        self.col_node_5 = (143, 163, 171)
        self.col_node_6 = (115, 140, 150)
        self.col_node_7 = (87, 117, 129)
        self.col_node_8 = (59, 94, 108)
        self.col_node_9 = (31, 71, 87)
        self.col_linkage = (33, 127, 158)
        self.col_triangle = (30, 76, 94)

        self.nodeArray = []
        self.connectedNodes = []
        self.nodeMovement = []
        self.movement_max = 2
        self.nodeCount = number_of_nodes
        self.max_connections = 4
        self.lower_linkage_bound_one = 250
        self.lower_linkage_bound_two = 170

    def create_nodes(self):
        for i in range(self.nodeCount):
            self.nodeArray.append(
                [random.randint(0, self.width), random.randint(0, self.height)])  # create a list of randomly distributed nodes
            speed = [random.randint(-self.movement_max, self.movement_max),
                     random.randint(-self.movement_max, self.movement_max)]
            if speed[0] == 0 and speed[1] == 0:  # no node should not move at all.
                speed[1] = 1
            self.nodeMovement.append(speed)  # each node has its movement (x & y)
            self.connectedNodes.append([i, 0])  # create a list to keep track of nodes which are connected

    def closest_distance(self, x, y):
        return np.sqrt(((x[0] - y[0]) ** 2) + ((x[1] - y[1]) ** 2))

    def get_two_neighbour_nodes(self, node_index):
        shortest_dist_len_one = 10000000000
        shortest_dist_len_two = 10000000000
        shortest_dist_len_three = 10000000000
        shortest_dist_index_one = None
        shortest_dist_index_two = None
        shortest_dist_index_three = None

        cp = self.nodeArray[node_index]
        for index, node in enumerate(self.nodeArray):
            if node != cp:
                current_dist = self.closest_distance(cp, self.nodeArray[index])
                if current_dist < shortest_dist_len_one:
                    shortest_dist_len_three = shortest_dist_len_two
                    shortest_dist_len_two = shortest_dist_len_one
                    shortest_dist_len_one = current_dist

                    shortest_dist_index_three = shortest_dist_index_two
                    shortest_dist_index_two = shortest_dist_index_one
                    shortest_dist_index_one = index

        # Connections which are too long are deleted
        if (shortest_dist_len_three - shortest_dist_len_one) > self.lower_linkage_bound_one:
            shortest_dist_index_three = None
        if (shortest_dist_len_two - shortest_dist_len_one) > self.lower_linkage_bound_two:
            shortest_dist_index_two = None

        return node_index, shortest_dist_index_one, shortest_dist_index_two, shortest_dist_index_three

    def render(self):
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Move nodes
        for i in range(0, self.nodeCount):
            self.nodeArray[i][0] += self.nodeMovement[i][0]
            self.nodeArray[i][1] += self.nodeMovement[i][1]  # random.randint(-5,5)
            if self.nodeArray[i][0] < 0 or self.nodeArray[i][0] > self.width:
                self.nodeMovement[i][0] = self.nodeMovement[i][0] * (-1)
            if self.nodeArray[i][1] < 0 or self.nodeArray[i][1] > self.height:
                self.nodeMovement[i][1] = self.nodeMovement[i][1] * (-1)

        # Reset connection counter
        for i in range(self.nodeCount):
            self.connectedNodes[i][1] = 0

        # Draw triangles
        for i in range(0, self.nodeCount):
            (a, b, c, d) = self.get_two_neighbour_nodes(i)

            if None not in [a, b, c]:
                pygame.draw.polygon(self.screen, self.col_triangle,
                                    [self.nodeArray[a], self.nodeArray[b], self.nodeArray[c]], 0)

        # Draw lines to the two closest nodes and around triangles
        for i in range(self.nodeCount):
            (a, b, c, d) = self.get_two_neighbour_nodes(i)

            if b is not None:  # and connectedNodes[b][1] < max_connections:
                pygame.draw.line(self.screen, self.col_linkage, self.nodeArray[a], self.nodeArray[b], 1)
                self.connectedNodes[b][1] += 1

            if c is not None and self.connectedNodes[c][1] < self.max_connections:
                pygame.draw.line(self.screen, self.col_linkage, self.nodeArray[a], self.nodeArray[c], 1)
                self.connectedNodes[c][1] += 1

            if d is not None and self.connectedNodes[d][1] < self.max_connections:
                pygame.draw.line(self.screen, self.col_linkage, self.nodeArray[a], self.nodeArray[d], 1)
                self.connectedNodes[d][1] += 1

            if None not in [b, c]:
                pygame.draw.line(self.screen, self.col_linkage, self.nodeArray[b], self.nodeArray[c], 1)

        # Draw all nodes
        for circle in self.nodeArray:
            # TODO: reduce based on col_node array
            pygame.draw.circle(self.screen, self.col_node_9, (circle[0], circle[1]), 9)
            pygame.draw.circle(self.screen, self.col_node_8, (circle[0], circle[1]), 8)
            pygame.draw.circle(self.screen, self.col_node_7, (circle[0], circle[1]), 7)
            pygame.draw.circle(self.screen, self.col_node_6, (circle[0], circle[1]), 6)
            pygame.draw.circle(self.screen, self.col_node_5, (circle[0], circle[1]), 5)
            pygame.draw.circle(self.screen, self.col_node_4, (circle[0], circle[1]), 4)
            pygame.draw.circle(self.screen, self.col_node_3, (circle[0], circle[1]), 3)
            pygame.draw.circle(self.screen, self.col_node_2, (circle[0], circle[1]), 2)
            pygame.draw.circle(self.screen, self.col_node_1, (circle[0], circle[1]), 1)

        self.clock.tick(20)
