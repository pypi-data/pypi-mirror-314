"""
Support types for the Tangled Game Engine.
"""
from __future__ import annotations

from enum import IntEnum
from typing import Tuple

class InvalidMoveError(Exception):
    """An exception for an invalid move in the game."""
    pass

class InvalidPlayerError(Exception):
    """An exception for an invalid player trying to join the game."""
    pass

class InvalidGameStateError(Exception):
    """An exception for mismatch between a game state and a Game."""
    pass

class Vertex:
    """
    A vertex in the game graph.
    
    Members:
        state (Vertex.State): The state of the vertex.
        id (int): The id of the vertex.

    Enums:
        State: The state of a vertex.
    """

    class State(IntEnum):
        """
        The state of a vertex.
        Use this to set or interpret the state of a vertex

        Values:
            NONE (int): The vertex has no state (no ownership).
            P1 (int): The vertex is owned by player 1.
            P2 (int): The vertex is owned by player 2.
        """
        NONE = 0
        P1 = 1
        P2 = 2

    state: Vertex.State = State.NONE
    id: int = 0
    
    def __init__(self, node_id: int):
        """Set a vertex in the game graph."""
        self.node_id = node_id
        self.state = Vertex.State.NONE


class Edge:
    """
    An edge in the game graph.

    Members:
        vertices (Tuple[int, int]): The two vertices that the edge connects.
        state (Edge.State): The state of the edge.
    
    Enums:
        State: The state of an edge.
    """

    class State(IntEnum):
        """
        The state of an edge.
        Use this to set or interpret the state of an edge.
        
        Values:
            NONE (int): The edge has not been set.
            NEITHER (int): The edge has no state preference.
            FM (int): The edge prefers FM.
            AFM (int): The edge prefers AFM.
        """

        NONE = 0
        NEITHER = 1
        FM = 2
        AFM = 3
        
    vertices: Tuple[int, int] = None
    state: Edge.State = State.NONE
    
    def __init__(self, node1_id: int, node2_id: int):
        """Set an edge in the game graph."""
        self.vertices = (node1_id, node2_id)
        self.state = Edge.State.NONE


__all__ = ["Vertex", "Edge", "InvalidMoveError", "InvalidPlayerError", "InvalidGameStateError"]
