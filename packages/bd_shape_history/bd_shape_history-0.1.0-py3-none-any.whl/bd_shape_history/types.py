try:

    import build123d as bd

    Part = bd.Part
    Face = bd.Face
    Edge = bd.Edge
    Shape = bd.Shape

except ImportError:

    Part = object
    Face = object
    Edge = object
    Shape = object
