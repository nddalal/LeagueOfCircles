# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 14:01:35 2019

@author: nihar
"""

#Adapted from
#https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
class Node():
    def __init__(self, parent = None, position = None):
        self.parent = parent
        self.position = position
        
        self.g = 0
        self.h = 0
        self.f = 0
        
    def __eq__(self, other):
        return isinstance(other, Node) and self.position == other.position
#Adapted from  the PSEUDOCODE FROM
#https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
    
#TO BE AS SPECIFIC AS POSSIBLE: I LOOKED AT THE PSEUDO CODE, AND THE NODE CLASS
#I DID THE REST MYSELF    
    
def aStar(app, start, end):
    
    directions = [(-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), 
                  (1, 0), (1, 1)]
    
    #Create Start and End Nodes
    startNode = Node(None, start)
    startNode.g = startNode.h = startNode.f = 0  
    endNode = Node(None, end)
    endNode.g = endNode.h = endNode.f = 0
    
    #Initialize open and closed lists
    openList = [startNode]
    closedList = []
    
    while openList != []:
        
        #Get current node
        currentNode = openList[0]
        currentIndex = 0
        for node in openList:
            if node.f < currentNode.f:
                currentNode = node
                currentIndex = openList.index(node)
                
            
                
        openList.pop(currentIndex)
        closedList.append(currentNode)
        #when we've reached our destination, we return a path of cells that we
        #travelled to reach there. 
        if currentNode == endNode:
            path = []
            current = currentNode
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] #return the reverse path
        
        children = []
        for drow,dcol in directions:
            nodePosition = (currentNode.position[0]+drow, 
                            currentNode.position[1]+dcol)
            if (nodePosition[0]<= app.rows-1 and nodePosition[0]>=0 and 
                nodePosition[1]<= app.cols-1 and nodePosition[1]>=0 and 
                app.board[nodePosition[0]][nodePosition[1]] == 0):
                newNode = Node(currentNode, nodePosition)
                children.append(newNode)
        
        
        for child in children:
            
            for node in closedList:
                if child == node:
                    continue
                
            child.g = currentNode.g + 1
            child.h = ((child.position[0]-endNode.position[0])**2+
                       (child.position[1]-endNode.position[1])**2)
            child.f = child.g + child.h
            
            for node in openList:
                if child == node and child.g>node.g:
                    continue
                
            openList.append(child)
