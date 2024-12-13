from typing import List, Self
from .types import Part, Face, Edge, Shape

COLOR_FACE_DEFAULT = 'Gray'
COLOR_FACE_ADDED = 'Green'
COLOR_FACE_MODIFIED = 'DarkOliveGreen'

COLOR_EDGE_DEFAULT = 'Black'
COLOR_EDGE_ADDED = 'LimeGreen'
COLOR_EDGE_MODIFIED = 'Olive'

def get_label(part: Shape) -> str:
    return hex(hash(part))[2:]


class Step:
    def __init__(self, label: str, obj: Part) -> None:
        self.label = label
        self.object = obj

        self.faces = {get_label(f): f for f in obj.faces()}
        self.edges = {get_label(e): e for e in obj.edges()}
        self.vertices = {get_label(v): v for v in obj.vertices()}

        Step.labelise({**self.faces, **self.edges, **self.vertices})

    @staticmethod
    def labelise(shapes_dict):
        for shape_label, shape in shapes_dict.items():
            shape.label = shape_label

    def get_faces(self) -> List[Face]:
        return list(self.faces.values())

    def get_edges(self) -> List[Edge]:
        return list(self.edges.values())

    def get_faces_and_edges(self) -> List[Edge|Face]:
        return self.get_faces() + self.get_edges()

    def is_very_new_face(self, step: Self, face: Face) -> bool:
        for edge in face.edges():
            if get_label(edge) in step.edges:
                return False
        return True

    def is_very_new_edge(self, step: Self, edge: Edge):
        for vertex in edge.vertices():
            if get_label(vertex) in step.vertices:
                return False
        return True

    def colorize_faces_diff(self, that_step: Self|None) -> None:
        for face_label, face in self.faces.items():
            if not that_step:
                face.color = COLOR_FACE_ADDED
            elif face_label in that_step.faces:
                face.color = COLOR_FACE_DEFAULT
            elif self.is_very_new_face(that_step, face):
                face.color = COLOR_FACE_ADDED
            else:
                face.color = COLOR_FACE_MODIFIED

    def colorize_edges_diff(self, that_step: Self|None) -> None:
        for edge_label, edge in self.edges.items():
            if not that_step:
                edge.color = COLOR_EDGE_ADDED
            elif edge_label in that_step.edges:
                edge.color = COLOR_EDGE_DEFAULT
            elif self.is_very_new_edge(that_step, edge):
                edge.color = COLOR_EDGE_ADDED
            else:
                edge.color = COLOR_EDGE_MODIFIED
