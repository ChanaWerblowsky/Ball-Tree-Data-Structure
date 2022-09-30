# Chana Werblowsky
# Ball Tree Data Structure

"""
"I hereby certify that this program is solely the result of my own work and is in compliance with the Academic Integrity
policy of the course syllabus and the academic integrity policy of the CS department.”
"""

import random
import math
from heapq import *
import pytest


# Returns euclidian distance between two sets of coordinates
def distance(c1, c2): 

    d = 0   # cumulative sum; initialized to 0
    
    # square the difference between the two points' values at each dimension; sum the results from each dimension
    for i in range(len(c1)): 
        d += ((c1[i] - c2[i]) ** 2)

    # return the square root of the sum
    return math.sqrt(d)

      
# Node class - each node represents hypersphere of given dimensions
class Node(object):
    
    def __init__(self, pivot, radius):
        
        self.pivotCoords = pivot[0]  # tuple of keys
        self.pivotData   = pivot[1]
        
        self.radius = radius  # distance between pivot and farthest point in node
        
        self.leftChild = None
        self.rightChild = None     
         
        
        
    def __str__(self):
        return "(" + str(self.pivotCoords) + ", '" + str(self.pivotData) + "')"


# Ball Tree class
class BallTree(object):
    
    def __init__(self, points, dimensions):
        
        self.__points = points 
        self.__dimensions = dimensions
        self.__root = self.build(self.__points)
        
    
    def getPoints(self):
        return self.__points
       
    
    # Build Ball Tree with given points
    # Returns the root node, or None if tree is empty
    def build(self, points):

        
        # base case: zero points --> return None
        if len(points) == 0:
            return None
        
        
        # base case: one point --> return leaf node
        if len(points) == 1:  
            return Node(points[0], 0)  # leaf has radius of 0
        
        
        # OTHERWISE (more than one point left)...
        
        ### Step 1: Find dimension of greatest spread on which to split the points at this level
        ### Step 2: Find median at dimension of greatest spread to be this node's pivot
        ### Steps 3 & 4: Split points in two according to pivot; determine this node's radius
        ### Step 5: Create this node and recurse down its children
        
        
        
        ## 1.Find dimension of greatest spread:
        
        # list to contain the lowest value at each dimension
        lows = [float('inf')] * self.__dimensions 
        
        # list to contain the highest value at each dimension
        highs = [-float('inf')] * self.__dimensions  
        
        # loop through points, recording highest and lowest vals seen at each dimension
        for p in points:                        # for each point
            for i in range(self.__dimensions):  # for each of point's dimensions
                
                coordVal = p[0][i]  # coord val of current point's i'th dimension
                
                if coordVal < lows[i]:   # if less than seen so far at this dimension,
                    lows[i] = coordVal   # place this point's i'th coord into lows' i'th position
                
                if coordVal > highs[i]:  # if greater than seen so far at this dimension,
                    highs[i] = coordVal  # place this point's i'th coord into highs' i'th position
                
             
        # determine dimension of GS according to lists of lows and highs
        greatestSpread = -float('inf')
        dimensionOfGS = 0
        
        for i in range(self.__dimensions):  # for each dimension:
            
            # difference between high and low values at current dimension (spread)
            difference = highs[i] - lows[i] 
            
            if difference > greatestSpread:  # if greater spread than seen so far,
                greatestSpread = difference  # update greatest spread and
                dimensionOfGS = i            # dimension of greatest spread variables
                
        

        ## 2.Find median at the dimension of greatest spread to be the pivot point:

        # Median of five:
        randomPointList = []
        
        for i in range(5):  # choose 5 random points
            p = random.choice(points)  
            
            # append tuple of (coord at dimension of GS, point) to list
            randomPointList.append((p[0][dimensionOfGS], p))
            
        # sort randomly chosen points on their coord value at the dimension of GS    
        randomPointList.sort()
        
        # get median (i.e. POINT with the medium coord value at dimension of GS)
        median = randomPointList[2][1]
        
        

        ## 3.Split points in two according to the median (to be in its left and right children):
        ## 4.Determine the to-be-node's radius (dist between median and farthest point at this level):
        
        leftPoints = [] 
        rightPoints = []
        
        radius = -float('inf')
        
        # loop through points to determine whether they lie in left or right child
        # AND to find distance from median/pivot to farthest point (radius)
        for p in points:
            
            # if point's coord val at dimension of GS is greater than that of the median,
            if p != median and p[0][dimensionOfGS] <= median[0][dimensionOfGS]:
                leftPoints.append(p)    # point lies in the left child
            
            # otherwise, if it's less than median's coord val,
            elif p != median:       
                rightPoints.append(p)   # point lies in the right child
                
            # update radius if dist between point and median is greater than seen so far   
            dist = distance(median[0], p[0])
            if dist > radius:
                radius = dist
    
        
        ## 5. Finally, create node and recurse down its children:
        
        # create internal node with the determined median and radius
        node = Node(median, radius)
   
        # recurse down left and right children, passing in lists of left and right points
        node.leftChild = self.build(leftPoints)
        node.rightChild = self.build(rightPoints)
    
        
        return node   # return the newly created node


        
    # Wrapper method
    # Returns data associated with query coordinates, or None if no such point in tree
    def findExact(self, queryCoords):
        return self.__findExact(self.__root, queryCoords)
    
        
    # Recursive method    
    def __findExact(self, n, queryCoords):
        
        if n:
            # is this the search point??
            if n.pivotCoords == queryCoords:        
                return n.pivotData
            
            # if not, is the search point within this node's radius??
            if distance(queryCoords, n.pivotCoords) > n.radius:
                # if distance between search point and pivot is greater than node's radius, not in node
                return None   
            
            # if possibly within this ball, recurse down children
            leftAns = self.__findExact(n.leftChild, queryCoords)
            rightAns = self.__findExact(n.rightChild, queryCoords)
            
            # return data that invocation on children returned, or None (implicitly)
            if leftAns: return leftAns
            if rightAns: return rightAns
      
    
    # Wrapper method
    # Returns k nearest neighbors of query point (or as many as could find in tree)
    # If query point itself is in tree, it's the closest neighbor
    def kNearestNeighborsSearch(self, queryCoords, k):
        
        heap = []  # heapq to contain tuples of form (-distance, point)
        
        # fill heapq with as many negative infinity tuples as num of neighbors requested
        for i in range(k):  
            heappush(heap, (-float('inf'), -float('inf')))
   
        # call recursive method:
        kClosest, qRad = self.__kNearestNeighborsSearch(self.__root, queryCoords, heap, float('inf'), k)
        
    
        # then, build up answer list of tuples in the form (positive distance, point)
        # for each of the k nearest neighbors - but only as many as were found
        ansList = []
        
        for i in range(k):
            
            distPointTuple = (heappop(kClosest))  # pop farthest (distance, point) tuple from closest-points heap
            if distPointTuple[0] != -float('inf'):  # if contains an actual point, add it to answer list
                ansList.append((abs(distPointTuple[0]), distPointTuple[1]))
                
        
        ansList.reverse()   # reverse list so that closer points are first
        
        # return list of k nearest neighbors in order of ascending distance from query point
        return ansList

    # Recursive method
    def __kNearestNeighborsSearch(self, n, queryCoords, closestSoFar, queryRadius, k):

        # if this node doesn't exist, or it can't possibly contain any points closer than those in the heapq
        # (node can only potentially contain points closer than seen so far if it overlaps with the query circle)
        if not n or distance(queryCoords, n.pivotCoords) - n.radius > queryRadius:
            
            return closestSoFar, queryRadius  # break out of recursion

        # otherwise, check if this point is closer than closest so far
        dist = distance(queryCoords, n.pivotCoords)
        
        # if pivot itself is closer than farthest of nearest neighbors, 
        if dist < abs(closestSoFar[0][0]):

            heappop(closestSoFar)  # pop farthest point, add current point
            heappush(closestSoFar, (-dist, (n.pivotCoords, n.pivotData)))
            
            queryRadius = abs(closestSoFar[0][0])  # shrink query radius accordingly
            # (query radius is distance between query point and farthest of closest neighbors so far)
        
        
        # then, recurse down left and right children
        closestSoFar, leftRadius = self.__kNearestNeighborsSearch(n.leftChild, queryCoords, closestSoFar, queryRadius, k)
        closestSoFar, rightRadius = self.__kNearestNeighborsSearch(n.rightChild, queryCoords, closestSoFar, queryRadius, k)

        # return heap, queryRadius
        return closestSoFar, abs(closestSoFar[0][0])

    
########################################################################################################################
###################################################### TESTING #########################################################
########################################################################################################################

# Fake BallTree Class 
# Performs the same operations as does the real BallTree class, albeit via brute force

class FakeBallTree(object):

    def __init__(self, points):     
        
        self.__points = points  # list of tuples in the form ([coords], data)
        
    # Accessor method - returns point list
    def getPoints(self):
        return self.__points
        
    # Returns data associated with query coordinates
    def findExact(self, coords):
        
        for p in self.__points:
        
            if p[0] == coords:   # if this point's coords match query coords, 
                return p[1]      # return point's data
            
        # return None otherwise    
            
    # Returns k nearest neighbors to query point
    def knnSearch(self, coords, k):
        
        distHeap = []
        
        for p in self.__points:
            
            # compute distance from point to search point
            dist = distance(coords, p[0])  # p[0] = the current point's coords
            
            
            # add point to heap with its distance
            heappush(distHeap, (dist, p))
            
        # once all points have been added to heap, pop top k items 
        # (those closest to search point) and return them as a list
        
        ansList = []
        for i in range(k):
            if len(distHeap) != 0:
                p = heappop(distHeap)
                ansList.append((p[0], p[1]))  # (distance, point)
            
        return ansList


## UTILITY FUNCTION:
# Returns list of specified num points (tuples), each of specified dimension
def randomPoints(num, dimensions):
    
    points = []
    
    for i in range(num):
        coords = []
        for j in range(dimensions):
            coords.append(random.uniform(-1000, 1000))    
            
        ## data
        data = random.random()  
    
        points.append((coords, data))
        
    return points


################## PYTESTS ####################


# Make sure that point lists in real and fake ball trees match
def test_pointList():
    
    # create real and fake ball trees with same random points
    points = randomPoints(100, 3)
    
    b = BallTree(points, 3)
    f = FakeBallTree(points)    
    
    assert b.getPoints() == f.getPoints()
    
    # repeat with points of higher dimensions
    points = randomPoints(100, 7)
    
    b = BallTree(points, 7)
    f = FakeBallTree(points)    
    
    assert b.getPoints() == f.getPoints()    


# Test that findExact successfully returns the data of the one point in the tree
def test_superSimpleFind():
    
    b = BallTree([([3, 4], 'a')], 2)
    f = FakeBallTree([([3, 4], 'a')])

    assert b.findExact([3, 4]) == 'a'
    assert f.findExact([3, 4]) == b.findExact([3, 4])


# Test that findExact works correctly with coordinates of few dimensions  
def test_findExactFewDimensions():
    
    # 3 dimensions:
    points = randomPoints(100, 3)
    
    b = BallTree(points, 3)
    f = FakeBallTree(points)
    
    # assert that each point that's supposed to be in Ball Tree is found 
    for p in points:  
        assert b.findExact(p[0]) is not None
        
        # assert that correct data is returned
        assert b.findExact(p[0]) == f.findExact(p[0])
        
        
    # 5 dimensions:
    points = randomPoints(80, 5)
    
    b = BallTree(points, 5)
    f = FakeBallTree(points)
    
    # assert that each point that's supposed to be in Ball Tree is found
    for p in points:  
        assert b.findExact(p[0]) is not None
        
        # assert that correct data is returned
        assert b.findExact(p[0]) == f.findExact(p[0])


# Test that findExact works correctly with coordinates of many (up to 10) dimensions       
def test_findExactHigherDimensions():
    
    # 7 dimensions
    points = randomPoints(70, 7)
    
    b = BallTree(points, 7)
    f = FakeBallTree(points)
    
    # assert that each point that's supposed to be in Ball Tree is found 
    for p in points:  
        assert b.findExact(p[0]) is not None
        assert b.findExact(p[0]) == f.findExact(p[0])  # and correct data is returned
    
    
    # 9 dimensions
    points = randomPoints(60, 9)
    
    b = BallTree(points, 9)
    f = FakeBallTree(points)
    
    # assert that each point that's supposed to be in Ball Tree is found
    for p in points:  
        assert b.findExact(p[0]) is not None
        assert b.findExact(p[0]) == f.findExact(p[0])  # and correct data is returned
        
    
    # 10 dimensions
    points = randomPoints(40, 10)
    
    b = BallTree(points, 10)
    f = FakeBallTree(points)
    
    # assert that each point that's supposed to be in Ball Tree is found
    for p in points:  
        assert b.findExact(p[0]) is not None
        assert b.findExact(p[0]) == f.findExact(p[0])  # and correct data is returned
        

# Test exactFind when search point cannot be found in tree
def test_findExactNotThere():
    
    # 100 points, 2 dimensions
    points = randomPoints(100, 2)
    
    b = BallTree(points, 2)
    f = FakeBallTree(points) 
    
    # search for 40 points that can't possibly be in tree
    for i in range(40):
        c1 = random.randint(2000, 3000)
        c2 = random.randint(-3000, -2000)   
        
        # assert that they aren't mistakenly 'found'
        assert b.findExact([c1, c2]) is None
        assert b.findExact([c1, c2]) == f.findExact([c1, c2])
        
    
    # 50 points, 6 dimensions    
    points = randomPoints(50, 6)
    
    b = BallTree(points, 6)
    f = FakeBallTree(points) 
    
    # search for 40 points that can't possibly be in tree
    for i in range(40):
        c1 = random.randint(2000, 3000)
        c2 = random.randint(-3000, -2000)
        c3 = random.randint(4000, 5000)    
        c4 = random.randint(2000, 3000)
        c5 = random.randint(-3000, -2000)
        c6 = random.randint(4000, 5000)   
        
        # assert that they aren't mistakenly 'found'
        assert b.findExact([c1, c2, c3, c4, c5, c6]) is None
        assert b.findExact([c1, c2, c3, c4, c5, c6]) == f.findExact([c1, c2, c3, c4, c5, c6])    

    
# Test findExact when tree is empty
def test_findExactEmptyTree():
   
    points = []  # empty point list
    
    # 3 dimensions
    b = BallTree(points, 3)
    f = FakeBallTree(points)  
    
    for i in range(30): 
        c1 = random.randint(-1000, 1000)
        c2 = random.randint(-1000, 1000)
        c3 = random.randint(-1000, 1000)
        
        assert b.findExact([c1, c2, c3]) is None
        assert b.findExact([c1, c2, c3]) == f.findExact((c1, c2, c3))
    
    
    # 6 dimensions
    b = BallTree(points, 6)
    f = FakeBallTree(points)          
    
    for i in range(10):
        c1 = random.randint(-1000, 1000)
        c2 = random.randint(-1000, 1000)
        c3 = random.randint(-1000, 1000)
        c4 = random.randint(-1000, 1000)
        c5 = random.randint(-1000, 1000)
        c6 = random.randint(-1000, 1000)
        
        assert b.findExact([c1, c2, c3, c4, c5, c6]) is None
        assert b.findExact([c1, c2, c3, c4, c5, c6]) == f.findExact([c1, c2, c3, c4, c5, c6])
                

# Test findExact when tree has 10000 points
def test_findExactHighlyPopulatedTree():
    
    # 3 dimensions:
    points = randomPoints(10000, 3)
    
    b = BallTree(points, 3)
    f = FakeBallTree(points)
    
    # assert that each point that's supposed to be in Ball Tree is found 
    for p in points:  
        assert b.findExact(p[0]) is not None
        
        # assert that correct data is returned
        assert b.findExact(p[0]) == f.findExact(p[0])
        
        
    # 5 dimensions:
    points = randomPoints(1000, 5)
    
    b = BallTree(points, 5)
    f = FakeBallTree(points)
    
    # assert that each point that's supposed to be in Ball Tree is found
    for p in points:  
        assert b.findExact(p[0]) is not None
        
        # assert that correct data is returned
        assert b.findExact(p[0]) == f.findExact(p[0])    


# Test that k nearest neighbor search works properly
def test_knnSearch():

    for j in range(1000):
        points = randomPoints(25, 5)

        b = BallTree(points, 5)
        f = FakeBallTree(points)

        # random point to be query point
        searchPoint = randomPoints(1, 5)

        # find 3 nearest neighbors
        bAns = b.kNearestNeighborsSearch(searchPoint[0][0], 3)
        fAns = f.knnSearch(searchPoint[0][0], 3)

        for i in range(len(bAns)):                # for each of the nearest points:
            assert bAns[i][0]    == fAns[i][0]      # assert that distances match
            assert bAns[i][1][0] == fAns[i][1][0]   # assert that coords match
            assert bAns[i][1][1] == fAns[i][1][1]   # assert that data matches
        

# Test knn search on empty tree
def test_knnSearchEmptyTree():
    
    points = []  # empty point list
    
    b = BallTree(points, 5)
    f = FakeBallTree(points)
    
    for i in range(20):
    
        # random point to be query point
        searchPoint = randomPoints(1, 5)
        
        assert b.kNearestNeighborsSearch(searchPoint[0][0], 3) == []
        assert b.kNearestNeighborsSearch(searchPoint[0][0], 3) == f.knnSearch(searchPoint[0][0], 3)
    

# Test that knn search behaves correctly when there are fewer points in tree than the k requested
def test_knnSearchTooFewPoints():
    
    # only 2 points
    points = randomPoints(2, 5)
    
    b = BallTree(points, 5)
    f = FakeBallTree(points)
    
    # random point to be query point
    searchPoint = randomPoints(1, 5)    

    assert len(b.kNearestNeighborsSearch(searchPoint[0][0], 5)) == 2
    assert b.kNearestNeighborsSearch(searchPoint[0][0], 5) == f.knnSearch(searchPoint[0][0], 5)
    
    
# Test knn search on highly populated tree
def test_knnSearchPopulatedTree():

    points = randomPoints(1000, 5)

    b = BallTree(points, 5)
    f = FakeBallTree(points)

    # random point to be query point
    searchPoint = randomPoints(1, 5)

    # find 3 nearest neighbors
    bAns = b.kNearestNeighborsSearch(searchPoint[0][0], 3)
    fAns = f.knnSearch(searchPoint[0][0], 3)

    for i in range(len(bAns)):                # for each of the nearest points:
        assert bAns[i][0]    == fAns[i][0]      # assert that distances match
        assert bAns[i][1][0] == fAns[i][1][0]   # assert that coords match
        assert bAns[i][1][1] == fAns[i][1][1]   # assert that data matches


# Test knn search on points of 10 dimensions
def test_knnSearchHigherDimensions():
    points = randomPoints(25, 10)

    b = BallTree(points, 10)
    f = FakeBallTree(points)

    # random point to be query point
    searchPoint = randomPoints(1, 10)

    # find 3 nearest neighbors
    bAns = b.kNearestNeighborsSearch(searchPoint[0][0], 3)
    fAns = f.knnSearch(searchPoint[0][0], 3)

    for i in range(len(bAns)):              # for each of the nearest points:
        assert bAns[i][0]    == fAns[i][0]     # assert that distances match
        assert bAns[i][1][0] == fAns[i][1][0]  # assert that coords match
        assert bAns[i][1][1] == fAns[i][1][1]  # assert that data matches


# Test knn search when a greater number of neighbors are requested
def test_knnSearchMoreNeighbors():

    points = randomPoints(100, 5)

    b = BallTree(points, 5)
    f = FakeBallTree(points)

    # random point to be query point
    searchPoint = randomPoints(1, 5)

    # find 6 nearest neighbors
    bAns = b.kNearestNeighborsSearch(searchPoint[0][0], 6)
    fAns = f.knnSearch(searchPoint[0][0], 6)

    for i in range(len(bAns)):              # for each of the nearest points:
        assert bAns[i][0]    == fAns[i][0]     # assert that distances match
        assert bAns[i][1][0] == fAns[i][1][0]  # assert that coords match
        assert bAns[i][1][1] == fAns[i][1][1]  # assert that data matches

    #####

    # NEW random query point
    searchPoint = randomPoints(1, 5)

    # find 20 nearest neighbors
    bAns = b.kNearestNeighborsSearch(searchPoint[0][0], 20)
    fAns = f.knnSearch(searchPoint[0][0], 20)

    for i in range(len(bAns)):  # for each of the nearest points:
        assert bAns[i][0] == fAns[i][0]  # assert that distances match
        assert bAns[i][1][0] == fAns[i][1][0]  # assert that coords match
        assert bAns[i][1][1] == fAns[i][1][1]  # assert that data matches



pytest.main(["-v", "-s", "BallTree.py"])
