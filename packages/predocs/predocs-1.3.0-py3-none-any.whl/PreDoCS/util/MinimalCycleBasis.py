"""
This module is translated from the MinimalCycleBasis-module from the 'Geometric Tools' library (https://www.geometrictools.com/).
The original algorithm is written in C++ and described in http://www.geometrictools.com/Documentation/MinimalCycleBasis.pdf.
In PreDoCS this class is used to find the cells in the discreet cross section geometry.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import networkx as nx
from PreDoCS.util.vector import Vector
from PreDoCS.util.Logging import get_module_logger
log = get_module_logger(__name__)


class MinimalCycleBasis(object):
    """
    Python implementation of 'Geometric Tools' MinimalCycleBasis class.
    
    Attributes
    ----------
    _graph: networkx.Graph
        The underlaying graph.
    _forest: list(Tree)
        The resulting list of trees.
    """
    
    class Tree(object):
        """
        Represents the tree of cycles for one component of the graph.
        
        Attributes
        ----------
        cycle: list(Vertex)
            List of vertices of the cycle. First and last element are the same vertex.
        children: list(Tree)
            List of subtrees of the tree (subcycles).
        """
        def __init__(self):
            self.cycle = []
            self.children = []
    
    
    class Vertex(object):
        """
        Represents a vertex of a planar graph.
        The MinimalCycleBasis algorithm has to clone some vertices,
        so id identifies a vertex at a position (multiple vertices can have the same id) and hash is unique for all vertices.
        
        Attributes
        ----------
        _instance_counter: int (static, default=0)
            Global instance counter. Required for unique id's.
        _id: int
            ID of the vertex (multiple vertices can have the same id).
        _hash: int
            Hash of the vertex (unique for all vertices).
        _position: Vector
            Two dimensional position of the vertex.
        _visited: int
            Visited flag. 0: unvisited, 1: discovered, 2: finished
        """
        
        _instance_counter = 0
        
        def __init__(self, position):
            """
            Constructor.
            
            Parameters
            ----------
            position: Vector
                Two dimensional position of the vertex.
            
            Raises
            ------
            AssertionError
                Raise if position is not two dimensional.
            """
            self._id = MinimalCycleBasis.Vertex._instance_counter
            self._hash = MinimalCycleBasis.Vertex._instance_counter
            MinimalCycleBasis.Vertex._instance_counter = MinimalCycleBasis.Vertex._instance_counter + 1
            
            assert len(position) == 2 # Zweidimensionaler Vektor
            self._position = position
            
            self._visited = 0
        
        def copy(self):
            """
            Returns a copy of the vertex (all data copied, except the hash).
            
            Returns
            -------
            Vertex
                The new vertex.
            """
            vert = MinimalCycleBasis.Vertex(self._position)
            vert._id = self._id
            vert._visited = self._visited
            return vert
            
        def __hash__(self):
            return self._hash
        
        def __repr__(self):
            return "<MinimalCycleBasis.Vertex id:%s position:%s hash:%s>" % (self._id, self.position, self._hash)
        
        @property
        def id(self):
            return int(self._id)
        
        @property
        def visited(self):
            return self._visited
        
        @visited.setter
        def visited(self, value):
            self._visited = value
        
        @property
        def position(self):
            return self._position
        
        @position.setter
        def position(self, value):
            self._position = value
        
        def __eq__(self, other):
            """
            Overrides the '=='-operator. Compares the id's of the vertices.
            
            Returns
            -------
            bool
                True, the id's of self and other are equal. None, if other is not an instance of Vertex.
            """
            if isinstance(other, MinimalCycleBasis.Vertex):
                return self.id == other.id
            else:
                return None
        
        def __lt__(self, other):
            """
            Overrides the '<'-operator. Compares the id's of the vertices.
        
            Returns
            -------
            bool
                True, if id of self is smaller than id of other. None, if other is not an instance of Vertex.
            """
            if isinstance(other, MinimalCycleBasis.Vertex):
                return self.id < other.id
            else:
                return None


    def __init__(self, graph):
        """
        Computes the minimal cycle basis of the given graph.
        
        Parameters
        ----------
        graph: networkx.Graph
            Underlaying Graph. All nodes have to be instances of Vertex.
        """
        self._graph = nx.Graph(graph)
        if len(self._graph.nodes()) == 0 or len(self._graph.edges()) == 0:
            return
        
        # Each node has to be a Vertex
        for node in self._graph.nodes():
            if not isinstance(node, MinimalCycleBasis.Vertex):
                raise RuntimeError('Each node has to be a MinimalCycleBasis.Vertex')

        # Get the connected components of the graph.  The 'visited' flags are
        # 0 (unvisited), 1 (discovered), 2 (finished).  The Vertex constructor
        # sets all 'visited' flags to 0.
        components = []
        for  vInitial in self._graph.nodes():
            if vInitial.visited == 0:
                #component = []
                component = self._DepthFirstSearch(vInitial)
                components.append(component)
        
        
        # The depth-first search is used later for collecting vertices for
        # subgraphs that are detached from the main graph, so the 'visited'
        # flags must be reset to zero after component finding.
        for vertex in self._graph.nodes():
            vertex.visited = 0

        # Get the primitives for the components.
        forest = []
        for component in components:
            forest.append(self._ExtractBasis(component))
            
        self._forest = forest
            
    def _DepthFirstSearch(self, vInitial):
        """
        The constructor uses GetComponents(...) and _DepthFirstSearch(...) to
        get the connected components of the graph implied by the input 'edges'.
        Recursive processing uses only _DepthFirstSearch(...) to collect
        vertices of the subgraphs of the original graph.
        
        Parameters
        ----------
        vInitial: Vertex
            Initial Vertex where the search starts.
        Returns
        -------
        list(Vertex)
            All vertices can be reached starting at vInitial.
        """
        component = []
        vStack = [vInitial]
        
        while len(vStack) > 0:
            vertex = vStack[-1]
            vertex.visited = 1
            i = 0
            neighbors = list(self._graph.neighbors(vertex))
            for adjacent in neighbors:
                if adjacent and adjacent.visited == 0:
                    vStack.append(adjacent)
                    break
                i = i + 1
            
            if i == len(neighbors):
                vertex.visited = 2
                component.append(vertex)
                vStack.pop()
        
        return component
                    
    def _ExtractBasis(self, component):
        """
        Support for traversing a simply connected component of the graph.
        
        Parameters
        ----------
        component: list(Vertex) (in/out)
            The component.
        
        Returns
        -------
        Tree
            The tree of the given component.
        """
        # The root will not have its 'cycle' member set.  The children are
        # the cycle trees extracted from the component.
        tree = MinimalCycleBasis.Tree()
        while len(component) > 0:
            #elements = [ data['attr'] for (n1, n2, data) in self._graph.edges(data=True) if ((n1 in component) or (n2 in component)) ]
            #PreDoCS.CrossSectionAnalysis.Debug.Element.plot_profile_segment(component, elements)
            #plt.show()
            self._RemoveFilaments(component)
            #elements = [ data['attr'] for (n1, n2, data) in self._graph.edges(data=True) if ((n1 in component) or (n2 in component)) ]
            #Debug.Element.plot_profile_segment(component, elements)
            #plt.show()
            if len(component) > 0:
                tree_ = self._ExtractCycleFromComponent(component)
                #elements = [ data['attr'] for (n1, n2, data) in self._graph.edges(data=True) if ((n1 in component) or (n2 in component)) ]
                #Debug.Element.plot_profile_segment(component, elements)
                #plt.show()
                tree.children.append(tree_)
                
        if len(tree.cycle) == 0 and len(tree.children) == 1:
            # Replace the parent by the child to avoid having two empty
            # cycles in parent/child.
            child = tree.children[0]
            tree.cycle = child.cycle
            tree.children = child.children

        return tree
    
    def _RemoveFilaments(self, component):
        """
        Remove all filaments of a given component.
        
        Parameters
        ----------
        component: list(Vertex) (in/out)
            The component.
        """
        # Locate all filament endpoints, which are vertices, each having exactly
        # one adjacent vertex.
        endpoints = [ v for v in component if len(list(self._graph.neighbors(v))) == 1 ]
        #component_new = list(component)
        
        if len(endpoints) > 0:
            # Remove the filaments from the component.  If a filament has two
            # endpoints, each having one adjacent vertex, the adjacency set of
            # the final visited vertex become empty.  We must test for that
            # condition before starting a new filament removal.
            for vertex in endpoints:
                if len(list(self._graph.neighbors(vertex))) == 1:
                    # Traverse the filament and remove the vertices.
                    while len(list(self._graph.neighbors(vertex))) == 1:
                        # Break the connection between the two vertices.
                        adjacent = next(self._graph.neighbors(vertex))
                        self._graph.remove_node(vertex)
                        # Traverse to the adjacent vertex.
                        vertex = adjacent
    
            # At this time the component is either empty (it was a union of
            # polylines) or it has no filaments and at least one cycle.  Remove
            # the isolated vertices generated by filament extraction.
            
            to_remove = []
            for vertex in component:
                if (vertex not in self._graph) or (len(list(self._graph.neighbors(vertex))) == 0):
                    to_remove.append(vertex)
            for vertex in to_remove:
                component.remove(vertex)

    def _ExtractCycleFromComponent(self, component):
        """
        Extract the cycles from a component.
        
        Parameters
        ----------
        component: list(Vertex) (in/out)
            The component.
        
        Returns
        -------
        Tree
            The tree of cycles of the component.
        """
        # Search for the left-most vertex of the component.  If two or more
        # vertices attain minimum x-value, select the one that has minimum
        # y-value.
        minVertex = component[0]
        for vertex in component:
            if vertex.position < minVertex.position:
                minVertex = vertex
    
        # Traverse the closed walk, duplicating the starting vertex as the
        # last vertex.
        closedWalk = []
        vCurr = minVertex
        vStart = vCurr
        closedWalk.append(vStart)
        vAdj = self._GetClockwiseMost(None, vStart)
        while vAdj != vStart:
            closedWalk.append(vAdj)
            vNext = self._GetCounterclockwiseMost(vCurr, vAdj)
            vCurr = vAdj
            vAdj = vNext
        closedWalk.append(vStart)
    
        # Recursively process the closed walk to extract cycles.
        tree = self._ExtractCycleFromClosedWalk(closedWalk)
    
        # The isolated vertices generated by cycle removal are also removed from
        # the component.
        to_remove = []
        for vertex in component:
            if (vertex not in self._graph) or (len(list(self._graph.neighbors(vertex))) == 0):
                to_remove.append(vertex)
        for vertex in to_remove:
            component.remove(vertex)
    
        return tree
        
    def _ExtractCycleFromClosedWalk(self, closedWalk):
        """
        Extract the cycles from a closed walk.
        
        Parameters
        ----------
        closedWalk: list(Vertex) (in/out)
            The closed walk.
        
        Returns
        -------
        Tree
            The tree of cycles of the closed walk.
        """
        tree = MinimalCycleBasis.Tree()
        duplicates = {} # dict(Vertex, int)
        detachments = set() # set(int)
        numClosedWalk = len(closedWalk)
        i = 1
        while i < numClosedWalk - 1:# i in range(1, numClosedWalk - 1):
            if not closedWalk[i] in duplicates:
                # We have not yet visited this vertex.
                duplicates[closedWalk[i]] = i
                continue
    
            # The vertex has been visited previously.  Collapse the closed walk
            # by removing the subwalk sharing this vertex.  Note that the vertex
            # is pointed to by closedWalk[diter->second] and closedWalk[i].
            iMin = duplicates[closedWalk[i]]
            iMax = i
            detachments.add(iMin)
            for j in range(iMin + 1, iMax):
                vertex = closedWalk[j]
                duplicates.pop(vertex)
                detachments.remove(j)
            
            closedWalk_remove = closedWalk[iMin + 1: iMax + 1]
            for vertex in closedWalk_remove:
                closedWalk.remove(vertex)
            numClosedWalk = len(closedWalk)
            i = iMin + 1
    
        if numClosedWalk > 3:
            # We do not know whether closedWalk[0] is a detachment point.  To
            # determine this, we must test for any edges strictly contained by
            # the wedge formed by the edges <closedWalk[0],closedWalk[N-1]> and
            # <closedWalk[0],closedWalk[1]>.  However, we must execute this test
            # even for the known detachment points.  The ensuing logic is designed
            # to handle this and reduce the amount of code, so we insert
            # closedWalk[0] into the detachment set and will ignore it later if
            # it actually is not.
            detachments.add(0)
    
            # Detach subgraphs from the vertices of the cycle.
            for i in detachments:
                original = closedWalk[i]
                maxVertex = closedWalk[i + 1]
                minVertex= closedWalk[numClosedWalk - 2]
                if i > 0:
                    minVertex = closedWalk[i - 1]
                    
                dMin = minVertex.position - original.position
                dMax = maxVertex.position - original.position
                
                isConvex = dMax[0] * dMin[1] >= dMax[1] * dMin[0]
                
                inWedge = set() # set(Vertex)
                adjacent = set(self._graph.neighbors(original))  # set(Vertex)
                for vertex in adjacent:
                    if vertex == minVertex or vertex == maxVertex:
                        continue

                    dVer = vertex.position - original.position
                    
                    containsVertex = False
                    if isConvex:
                        containsVertex =\
                            dVer[0] * dMin[1] > dVer[1] * dMin[0] and\
                            dVer[0] * dMax[1] < dVer[1] * dMax[0]
                    else:
                        containsVertex =\
                            (dVer[0] * dMin[1] > dVer[1] * dMin[0]) or\
                            (dVer[0] * dMax[1] < dVer[1] * dMax[0])
                    
                    if containsVertex:
                        inWedge.add(vertex)
    
                if len(inWedge) > 0:
                    # The clone will manage the adjacents for 'original' that lie
                    # inside the wedge defined by the first and last edges of the
                    # subgraph rooted at 'original'.  The sorting is in the
                    # clockwise direction.
                    clone = original.copy()
                    self._graph.add_node(clone)
    
                    # Detach the edges inside the wedge.
                    for vertex in inWedge:
                        data = self._graph.get_edge_data(vertex, original)
                        self._graph.remove_edge(vertex, original)
                        self._graph.add_edge(vertex, clone, element=data)
    
                    # Get the subgraph (it is a single connected component).
                    component = self._DepthFirstSearch(clone)
    
                    # Extract the cycles of the subgraph.
                    tree.children.append(self._ExtractBasis(component))

                # else the candidate was closedWalk[0] and it has no subgraph
                # to detach.
            tree.cycle = self._ExtractCycle(closedWalk)
        else:
            # Detach the subgraph from vertex closedWalk[0]; the subgraph
            # is attached via a filament.
            original = closedWalk[0]
            adjacent = closedWalk[1]
    
            clone = original.copy()
            self._graph.add_node(clone)
            
            data = self._graph.get_edge_data(original, adjacent)
            self._graph.remove_edge(original, adjacent)
            self._graph.add_edge(clone, adjacent, **data)
    
            # Get the subgraph (it is a single connected component).
            component = self._DepthFirstSearch(clone)
    
            # Extract the cycles of the subgraph.
            tree.children.append(self._ExtractBasis(component))
            if len(tree.cycle) == 0 and len(tree.children) == 1:
                # Replace the parent by the child to avoid having two empty
                # cycles in parent/child.
                child = tree.children[0]
                tree.cycle = child.cycle
                tree.children = child.children
    
        return tree
    
    def _ExtractCycle(self, closedWalk):
        """
        Extract one cycle from a closed walk.
        
        Parameters
        ----------
        closedWalk: list(Vertex)
            The closed walk.
        
        Returns
        -------
        list(Vertex)
            The cycle.
        """
        # TODO:  This logic was designed not to remove filaments after the
        # cycle deletion is complete.  Modify this to allow filament removal.
    
        # The closed walk is a cycle.
        cycle = list(closedWalk)
        
        # The clockwise-most edge is always removable.
        v0 = closedWalk[0]
        v1 = closedWalk[1]
        vBranch = None
        if len(list(self._graph.neighbors(v0))) > 2:
            vBranch = v0
            
        self._graph.remove_edge(v0, v1)
    
        # Remove edges while traversing counterclockwise.
        while v1 != vBranch and len(list(self._graph.neighbors(v1))) == 1:
            adj = next(self._graph.neighbors(v1))
            self._graph.remove_edge(v1, adj)
            v1 = adj
    
        if v1 != v0:
            # If v1 had exactly 3 adjacent vertices, removal of the CCW edge
            # that shared v1 leads to v1 having 2 adjacent vertices.  When
            # the CW removal occurs and we reach v1, the edge deletion will
            # lead to v1 having 1 adjacent vertex, making it a filament
            # endpoints.  We must ensure we do not delete v1 in this case,
            # allowing the recursive algorithm to handle the filament later.
            vBranch = v1
    
            # Remove edges while traversing clockwise.
            while v0 != vBranch and len(list(self._graph.neighbors(v0))) == 1:
                v1 = next(self._graph.neighbors(v0))
                self._graph.remove_edge(v0, v1)
                v0 = v1
        # else the cycle is its own connected component.
        
        #elements = [ data['attr'] for (n1, n2, data) in self._graph.edges(data=True) if ((n1 in cycle) or (n2 in cycle)) ]
        #PreDoCS.CrossSectionAnalysis.Debug.Element.plot_profile_segment(cycle, elements)
        #plt.show()
        
        return cycle
            
    def _GetClockwiseMost(self, vPrev, vCurr):
        """
        Returns the clockwise most vertex from a given vertex.
        
        Parameters
        ----------
        vPrev: Vertex
            Previous vertex.
        vCurr: Vertex
            Current vertex.
        
        Returns
        -------
        Vertex
            clockwise most vertex.
        """
        vNext = None
        vCurrConvex = False
        dCurr = Vector([0., -1.])
        if vPrev:
            dCurr = vCurr.position - vPrev.position
        dNext = Vector([0., 0.])
    
        for vAdj in self._graph.neighbors(vCurr):
            # vAdj is a vertex adjacent to vCurr.  No backtracking is allowed.
            if vAdj == vPrev:
                continue
    
            # Compute the potential direction to move in.
            dAdj = vAdj.position - vCurr.position
    
            # Select the first candidate.
            if not vNext:
                vNext = vAdj
                dNext = dAdj
                vCurrConvex = (dNext[0] * dCurr[1] <= dNext[1] * dCurr[0])
                continue
    
            # Update if the next candidate is clockwise of the current
            # clockwise-most vertex.
            if vCurrConvex:
                if (dCurr[0] * dAdj[1] < dCurr[1] * dAdj[0] or\
                    dNext[0] * dAdj[1] < dNext[1] * dAdj[0]):
                    vNext = vAdj
                    dNext = dAdj
                    vCurrConvex = (dNext[0] * dCurr[1] <= dNext[1] * dCurr[0])
            else:
                if (dCurr[0] * dAdj[1] < dCurr[1] * dAdj[0] and\
                    dNext[0] * dAdj[1] < dNext[1] * dAdj[0]):
                    vNext = vAdj
                    dNext = dAdj
                    vCurrConvex = (dNext[0] * dCurr[1] < dNext[1] * dCurr[0])

        return vNext
    
    def _GetCounterclockwiseMost(self, vPrev, vCurr):
        """
        Returns the counterclockwise most vertex from a given vertex.
        
        Parameters
        ----------
        vPrev: Vertex
            Previous vertex.
        vCurr: Vertex
            Current vertex.
        
        Returns
        -------
        Vertex
            counterclockwise most vertex.
        """
        vNext = None
        vCurrConvex = False
        dCurr = Vector([0., -1.])
        if vPrev:
            dCurr = vCurr.position - vPrev.position
        dNext = Vector([0., 0.])
    
        for vAdj in self._graph.neighbors(vCurr):
            # vAdj is a vertex adjacent to vCurr.  No backtracking is allowed.
            if vAdj == vPrev:
                continue
    
            # Compute the potential direction to move in.
            dAdj = vAdj.position - vCurr.position
    
            # Select the first candidate.
            if not vNext:
                vNext = vAdj
                dNext = dAdj
                vCurrConvex = (dNext[0] * dCurr[1] <= dNext[1] * dCurr[0])
                continue
    
            # Select the next candidate if it is counterclockwise of the current
            # counterclockwise-most vertex.
            if vCurrConvex:
                if (dCurr[0] * dAdj[1] > dCurr[1] * dAdj[0] and\
                    dNext[0] * dAdj[1] > dNext[1] * dAdj[0]):
                    vNext = vAdj
                    dNext = dAdj
                    vCurrConvex = (dNext[0] * dCurr[1] <= dNext[1] * dCurr[0])
            else:
                if (dCurr[0] * dAdj[1] > dCurr[1] * dAdj[0] or\
                    dNext[0] * dAdj[1] > dNext[1] * dAdj[0]):
                    vNext = vAdj
                    dNext = dAdj
                    vCurrConvex = (dNext[0] * dCurr[1] <= dNext[1] * dCurr[0])

        return vNext
    
    @staticmethod
    def _get_faces_form_forest(forest):
        """
        Searches recursively all faces of a cycle forest.
        
        Parameters
        ----------
        forest: list(Tree)
            The given forest.
        
        Returns
        -------
        list(list(Vertex))
            List of all faces.
        """
        faces = []
        for tree in forest:
            if len(tree.children) == 0 and len(tree.cycle) > 2:
                faces.append(tree.cycle)
            else:
                faces = faces + MinimalCycleBasis._get_faces_form_forest(tree.children)
        return faces
    
    def get_forest(self):
        """
        Returns a list of cycle trees for the graph.
        
        Returns
        -------
        list(Tree)
            List of all trees.
        """
        return self._forest
    
    def get_faces(self):
        """
        Returns all faces of the graph.

        Returns
        -------
        list(list(Vertex))
            List of all faces.
        """
        return MinimalCycleBasis._get_faces_form_forest(self._forest)
