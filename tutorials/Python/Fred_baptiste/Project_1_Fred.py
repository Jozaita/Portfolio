import math

class Polygon:
    def __init__(self,n,r):
        self._n = n
        self._R = r

    @property
    def num_edges(self):
        return self._n

    @property
    def n_vertices(self):
        return self._n

    @property
    def circumradius(self):
        return self._R

    @property
    def interior_angle(self):
        return (self.num_edges-2)*180/self.num_edges

    @property
    def edge_length(self):
        return 2*self.circumradius*math.sin(math.pi/self.num_edges)

    @property
    def apothem(self):
        return self.circumradius*math.cos(math.pi/self.num_edges)

    @property
    def area(self):
        return 0.5*self.num_edges*self.edge_length*self.apothem

    @property
    def perimeter(self):
        return self.num_edges*self.edge_length


    def __repr__(self):
        return f"Polygon({self.num_edges},{self.circumradius})"

    def __eq__(self, other):
        if isinstance(other,Polygon):
            return self.num_edges == other.num_edges and self.circumradius == other.circumradius
        else:
            raise TypeError("Introduce a Polygon")

    def __gt__(self, other):
        if isinstance(other,Polygon):
            return self.num_edges > other.num_edges
        else:
            raise TypeError("Introduce  a Polygon")


class Polygons():
    def __init__(self,n,c):
        self._nmax = n
        self._circumradius = c
        self._polygons = [Polygon(x,c) for x in range(3,n+1)]

    def __len__(self):
        return len(self._polygons)

    def __getitem__(self, item):
        return self._polygons[item]

    @property
    def max_efficiency_polygon(self):
        return sorted(self._polygons,key=lambda x:x.area/x.perimeter)[-1]




## Test for the polygon class, compare with a square
def test_square():
    square = Polygon(4,1)
    print(f"Compare square with {Polygon(4,1)}")
    assert square.num_edges == 4, "Num of edges is not 4"
    assert math.isclose(square.interior_angle,90,
                        rel_tol=1e-3,
                        abs_tol=1e-3),"Interior angle is not 90"
    assert math.isclose(square.edge_length,math.sqrt(2),
                        rel_tol=1e-3,
                        abs_tol=1e-3)
    assert  math.isclose(square.apothem,math.sqrt(2)/2,
                         abs_tol=1e-3,
                         rel_tol=1e-3)
    assert math.isclose(square.area,2,
                        abs_tol=1e-3,
                        rel_tol=1e-3)
    assert math.isclose(square.perimeter,4*math.sqrt(2),
                        abs_tol=1e-3,
                        rel_tol=1e-3)


test_square()

polygon_list = Polygons(5,1)
print(polygon_list.max_efficiency_polygon)


