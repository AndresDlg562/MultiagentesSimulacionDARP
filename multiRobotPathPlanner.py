import pickle

from darp import DARP
import numpy as np
from kruskal import Kruskal
import coverage_test as coverage
import sys
import argparse
from PIL import Image
import time

def get_area_map(path, area=0, obs=-1):
    """
    Creates an array from a given png-image(path).
    :param path: path to the png-image
    :param area: non-obstacles tiles value; standard is 0
    :param obs: obstacle tiles value; standard is -1
    :return: an array of area(0) and obstacle(-1) tiles
    """
    le_map = np.array(Image.open(path))
    ma = np.array(le_map).mean(axis=2) != 0
    le_map = np.int8(np.zeros(ma.shape))
    le_map[ma] = area
    le_map[~ma] = obs
    return le_map

def get_area_indices(area, value, inv=False, obstacle=-1):
    """
    Returns area tiles indices that have value
    If inv(erted), returns indices that don't have value
    :param area: array with value and obstacle tiles
    :param value: searched tiles with value
    :param inv: if True: search will be inverted and index of non-value tiles will get returned
    :param obstacle: defines obstacle tiles
    :return:
    """
    try:
        value = int(value)
        if inv:
            return np.concatenate([np.where((area != value))]).T
        return np.concatenate([np.where((area == value))]).T
    except:
        mask = area == value[0]
        if inv:
            mask = area != value[0]
        for v in value[1:]:
            if inv:
                mask &= area != v
            else:
                mask |= area == v
        mask &= area != obstacle
        return np.concatenate([np.where(mask)]).T

class MultiRobotPathPlanner(DARP):
    def __init__(self, nx, ny, notEqualPortions, initial_positions, portions,
                 obs_pos, visualization, MaxIter=80000, CCvariation=0.01,
                 randomLevel=0.0001, dcells=2, importance=False):

        start_time = time.time()
        # Initialize DARP
        self.darp_instance = DARP(nx, ny, notEqualPortions, initial_positions, portions, obs_pos, visualization,
                                  MaxIter=MaxIter, CCvariation=CCvariation,
                                  randomLevel=randomLevel, dcells=dcells,
                                  importance=importance)

        # Divide areas based on robots initial positions
        self.DARP_success , self.iterations = self.darp_instance.divideRegions()

        paths = []
        # Check if solution was found
        if not self.DARP_success:
            print("DARP did not manage to find a solution for the given configuration!")
        else:
            # Iterate for 4 different ways to join edges in MST
            self.mode_to_drone_turns = []
            AllRealPaths_dict = {}
            subCellsAssignment_dict = {}
            for mode in range(1):
                MSTs = self.calculateMSTs(self.darp_instance.BinaryRobotRegions, self.darp_instance.droneNo, self.darp_instance.rows, self.darp_instance.cols, mode)
                AllRealPaths = []
                for r in range(self.darp_instance.droneNo):
                    validNodes = []
                    for node in MSTs[r]:
                        validNodes.append(node.dst)
                        
                    #generate an np grid of size nx*ny that has a 0 in the valid nodes and 1 in the obstacles and 2 in the start
                    BinaryRobotRegion = np.zeros((self.darp_instance.rows, self.darp_instance.cols))
                    for i in range(self.darp_instance.rows):
                        for j in range(self.darp_instance.cols):
                            if (i*self.darp_instance.cols + j) in validNodes:
                                BinaryRobotRegion[i, j] = 0
                            else:
                                BinaryRobotRegion[i, j] = 1
                    BinaryRobotRegion[self.darp_instance.initial_positions[r]] = 2
                    # Calculate the trajectories
                    paths.append(coverage.generate_path(BinaryRobotRegion))
        print(paths)
        self.paths = paths
        



    def calculateMSTs(self, BinaryRobotRegions, droneNo, rows, cols, mode):
        MSTs = []
        for r in range(droneNo):
            k = Kruskal(rows, cols)
            k.initializeGraph(BinaryRobotRegions[r, :, :], True, mode)
            k.performKruskal()
            MSTs.append(k.mst)
        return MSTs


def mainPaths(grid_size, initialPositions, obstaclePositions):
    robots = 2
    initialPositions = [(3,4), (4,5)]
    obstaclePositions = [(1,1),(1,8),(2,4),(2,7),(3,0),(5,8),(9,2)]
    cleanInitialPositions = []
    cleanObstaclePositions = []
    for pos in initialPositions:
        cleanInitialPositions.append(pos[0]*grid_size + pos[1])
    for pos in obstaclePositions:
        cleanObstaclePositions.append(pos[0]*grid_size + pos[1])

    grid_size = 10
    cleanInitialPositions = []
    cleanObstaclePositions = []
    for pos in initialPositions:
        cleanInitialPositions.append(pos[0]*grid_size + pos[1])
    for pos in obstaclePositions:
        cleanObstaclePositions.append(pos[0]*grid_size + pos[1])

    return MultiRobotPathPlanner(10, 10, False, cleanInitialPositions,  [], cleanObstaclePositions, False).paths
    
