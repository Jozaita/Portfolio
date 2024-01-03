import math

class Polygon:
    def __init__(self,n,r):
        self._n = n
        self._R = r
        self._interior_angle = None
        self._edge_length = None
        self._apothem = None
        self._area = None
        self._perimeter = None

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
        if self._interior_angle == None:
            self._interior_angle =  (self.num_edges-2)*180/self.num_edges

        return self._interior_angle

    @property
    def edge_length(self):
        if self._edge_length == None:
            self._edge_length = 2*self.circumradius*math.sin(math.pi/self.num_edges)

        return self._edge_length

    @property
    def apothem(self):
        if self._apothem == None:
            self._apothem = self.circumradius*math.cos(math.pi/self.num_edges)
        return self._apothem

    @property
    def area(self):
        if self._area == None:
            self._area = 0.5*self.num_edges*self.edge_length*self.apothem
        return self._area

    @property
    def perimeter(self):
        if self._perimeter == None:
            self._perimeter = self.num_edges*self.edge_length
        return self._perimeter


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


class Polygons:
    def __init__(self,n,c):
        if n < 3:
            raise ValueError("Polygons have at least 3 sides!")
        self._nmax = n
        self._circumradius = c


    def __iter__(self):
        return self.PolygonIterator(self._nmax,self._circumradius)

    class PolygonIterator:
        def __init__(self,n,R):
            if n < 3:
                raise ValueError("Polygons have at least 3 sides !")
            self._nmax = n
            self._circumradius = R
            self.i = 3

        def __iter__(self):
            return self

        def __next__(self):
            if self.i > self._nmax:
                raise StopIteration
            else:
                result = Polygon(self.i,self._circumradius)
                self.i += 1
                return result

    @property
    def max_efficiency_polygon(self):
        return sorted(self,key=lambda x:x.area/x.perimeter)[-1]




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
for p in polygon_list:
    print(p)
print(polygon_list.max_efficiency_polygon)



