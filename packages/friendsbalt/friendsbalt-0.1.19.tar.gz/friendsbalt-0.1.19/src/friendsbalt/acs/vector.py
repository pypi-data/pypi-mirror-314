class Vector:
    def __init__(self, *args):
        self.components = []
        for arg in args:
            if not isinstance(arg, (int, float)):
                raise ValueError("Vector components must be integers or floats.")
            self.components.append(arg)

        self.dim = len(args)

    @classmethod
    def from_points(cls, p1, p2):
        return Vector(*(b - a for a, b in zip(p1, p2))) 

    def __add__(self, other):
        self._match_dim(other)

        return Vector(*[a + b for a, b in zip(self.components, other.components)])
    
    def __sub__(self, other):
        self._match_dim(other)

        return Vector(*[a - b for a, b in zip(self.components, other.components)])
    
    def __mul__(self, other):
        raise NotImplementedError("Multiplication is not supported for Vector objects.")
    
    def __truediv__(self, other):
        raise NotImplementedError("Division is not supported for Vector objects.")
    
    def __eq__(self, other):
        self._match_dim(other)

        return all(a == b for a, b in zip(self.components, other.components))
    
    def __ne__(self, other):
        return not self == other
    
    def x(self):
        return self.components[0]
    
    def y(self):
        return self.components[1]
    
    def z(self):
        return self.components[2]

    def __repr__(self):
        return f"Vector{self.components}"
    
    def _match_dim(self, other):
        if self.dim < other.dim:
            self._up_dim(other.dim)
        elif self.dim > other.dim:
            other._up_dim(self.dim)

    def _up_dim(self, new_dim):
        if new_dim < self.dim:
            return
        
        self.components += [0] * (new_dim - self.dim)
        self.dim = new_dim

    def dot(self, other):
        self._match_dim(other)

        return sum(a * b for a, b in zip(self.components, other.components))
    
    def cross(self, other):
        if self.dim > 3 or other.dim > 3:
            raise ValueError("Cross product is only supported up to 3-dimensional vectors.")
        
        self._up_dim(3)
        other._up_dim(3)
        
        x = self.y() * other.z() - self.z() * other.y()
        y = self.z() * other.x() - self.x() * other.z()
        z = self.x() * other.y() - self.y() * other.x()
        
        return Vector(x, y, z)
    
    def magnitude(self):
        return sum(comp ** 2 for comp in self.components) ** 0.5
    
    def sq_magnitude(self):
        return sum(comp ** 2 for comp in self.components)
    
    def normalize(self):
        mag = self.magnitude()
        return Vector(*[comp / mag for comp in self.components])