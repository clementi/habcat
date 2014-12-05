class BoundingCube(object):
    def __init__(self, center, dist):
        self._center = center
        self._dist = dist

    def get_x_bounds(self):
        return self._center[0] - self._dist, self._center[0] + self._dist

    def get_y_bounds(self):
        return self._center[1] - self._dist, self._center[1] + self._dist

    def get_z_bounds(self):
        return self._center[2] - self._dist, self._center[2] + self._dist