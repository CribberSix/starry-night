import pygame
import sys
import random
import numpy as np


class StarryNight:
    def __init__(self, number_of_nodes=50, surface=None):

        self.width, self.height = pygame.display.get_surface().get_size()
        self.screen = pygame.display.get_surface() if surface is None else surface

        # Create color-spectrum of nodes (= stars)
        start = (255, 255, 255)
        self.colors_node = []
        for i in range(9):
            self.colors_node.append(start)
            start = (start[0] - 28, start[1] - 23, start[2] - 21)
        self.colors_node.reverse()  # brightest node comes last / on top.

        self.col_linkage = (33, 127, 158)
        self.col_triangle = (30, 76, 94)

        self.nodeArray = []
        self.connectedNodes = []
        self.nodeMovement = []
        self.speed_limit = 2
        self.nodeCount = number_of_nodes
        self.max_connections = 4
        self.lower_linkage_bound_one = 250
        self.lower_linkage_bound_two = 170
        self.create_nodes()

    def render(self):
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Calculation
        self.move_nodes()
        self.reset_connections()

        # Rendering
        self.draw_connection_triangles()
        self.draw_connection_lines()
        self.draw_nodes()

    def create_nodes(self):
        """
        Create a list of randomly distributed nodes with random velocities.
        """
        for i in range(self.nodeCount):
            self.nodeArray.append(
                [random.randint(0, self.width), random.randint(0, self.height)]
            )
            speed = [
                random.randint(-self.speed_limit, self.speed_limit),
                random.randint(-self.speed_limit, self.speed_limit),
            ]
            if speed[0] == 0 and speed[1] == 0:  # no node should not move at all.
                speed[1] = 1
            self.nodeMovement.append(speed)  # each node has its movement (x & y)
            self.connectedNodes.append(
                [i, 0]
            )  # create a list to keep track of nodes which are connected

    @staticmethod
    def calculate_distance(node_1, node_2):
        return np.sqrt(((node_1[0] - node_2[0]) ** 2) + ((node_1[1] - node_2[1]) ** 2))

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
                current_dist = self.calculate_distance(cp, self.nodeArray[index])
                if current_dist < shortest_dist_len_one:
                    shortest_dist_len_three = shortest_dist_len_two
                    shortest_dist_len_two = shortest_dist_len_one
                    shortest_dist_len_one = current_dist

                    shortest_dist_index_three = shortest_dist_index_two
                    shortest_dist_index_two = shortest_dist_index_one
                    shortest_dist_index_one = index

        # Connections which are too long are deleted
        if (
            shortest_dist_len_three - shortest_dist_len_one
        ) > self.lower_linkage_bound_one:
            shortest_dist_index_three = None
        if (
            shortest_dist_len_two - shortest_dist_len_one
        ) > self.lower_linkage_bound_two:
            shortest_dist_index_two = None

        return (
            node_index,
            shortest_dist_index_one,
            shortest_dist_index_two,
            shortest_dist_index_three,
        )

    def draw_nodes(self):
        # Draw all nodes
        for circle in self.nodeArray:
            for i, color in enumerate(self.colors_node):
                pygame.draw.circle(
                    self.screen,
                    color,
                    (circle[0], circle[1]),
                    len(self.colors_node) - i,
                )

    def move_nodes(self):
        # Move nodes
        for i in range(0, self.nodeCount):
            self.nodeArray[i][0] += self.nodeMovement[i][0]
            self.nodeArray[i][1] += self.nodeMovement[i][1]
            if self.nodeArray[i][0] < 0 or self.nodeArray[i][0] > self.width:
                self.nodeMovement[i][0] = self.nodeMovement[i][0] * (-1)
            if self.nodeArray[i][1] < 0 or self.nodeArray[i][1] > self.height:
                self.nodeMovement[i][1] = self.nodeMovement[i][1] * (-1)

    def reset_connections(self):
        """
        Reset connections between nodes
        """
        for i in range(self.nodeCount):
            self.connectedNodes[i][1] = 0

    def draw_connection_triangles(self):
        for i in range(0, self.nodeCount):
            (a, b, c, d) = self.get_two_neighbour_nodes(i)

            if None not in [a, b, c]:
                pygame.draw.polygon(
                    self.screen,
                    self.col_triangle,
                    [self.nodeArray[a], self.nodeArray[b], self.nodeArray[c]],
                    0,
                )

    def draw_connection_lines(self):

        # Draw lines to the two closest nodes and around triangles
        for i in range(self.nodeCount):
            (a, b, c, d) = self.get_two_neighbour_nodes(i)

            if b is not None:  # and connectedNodes[b][1] < max_connections:
                pygame.draw.line(
                    self.screen,
                    self.col_linkage,
                    self.nodeArray[a],
                    self.nodeArray[b],
                    1,
                )
                self.connectedNodes[b][1] += 1

            if c is not None and self.connectedNodes[c][1] < self.max_connections:
                pygame.draw.line(
                    self.screen,
                    self.col_linkage,
                    self.nodeArray[a],
                    self.nodeArray[c],
                    1,
                )
                self.connectedNodes[c][1] += 1

            if d is not None and self.connectedNodes[d][1] < self.max_connections:
                pygame.draw.line(
                    self.screen,
                    self.col_linkage,
                    self.nodeArray[a],
                    self.nodeArray[d],
                    1,
                )
                self.connectedNodes[d][1] += 1

            if None not in [b, c]:
                pygame.draw.line(
                    self.screen,
                    self.col_linkage,
                    self.nodeArray[b],
                    self.nodeArray[c],
                    1,
                )
