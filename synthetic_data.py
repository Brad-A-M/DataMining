from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import matplotlib.pyplot as plt
import random as rand
from descartes.patch import PolygonPatch
import pandas as pd

class SyntheticData:
    def __init__(self, num_polygons, num_pts, num_noise_pts, max_sides):
        rand.seed(100)
        offset = int(100/num_polygons)
        self.point_assignments = pd.DataFrame()
        polygons = self.generate_polygons(num_polygons, max_sides, offset)
        points = self.generate_points(num_pts, polygons)
        noise_points = self.generate_noise_points(num_noise_pts, polygons)
        self.plot(polygons, points, noise_points)

    def generate_polygons(self, n, max_sides, offset):
        # create n by n grid and only allow at most one polygon in each square
        polygons = []
        polygon_locations = []
        while(n > 0):
            x = rand.randint(0, n)
            y = rand.randint(0, n)
            if (x,y) not in polygon_locations:
                polygon_locations.append((x,y))
                num_sides = rand.randint(3, max_sides)
                polygon_pts = []

                for i in range(0, num_sides):
                    x_pt = rand.randint(0, offset) + offset * x
                    y_pt = rand.randint(0, offset) + offset * y
                    polygon_pts.append((x_pt, y_pt))
                    i += 1

                polygon = Polygon(polygon_pts)
                # Only draw a polygon if it is valid (no intersecting edges)
                if(polygon.is_valid):
                    polygons.append(polygon)
                    n -= 1
        return polygons

    def generate_points(self, num_pts, polygons):
        points = []
        for p_index, polygon in enumerate(polygons):
            n = num_pts
            minx, miny, maxx, maxy = polygon.bounds
            while n > 0:
                pnt = Point(rand.uniform(minx, maxx), rand.uniform(miny, maxy))
                # Only add a point if is in a polygon
                if polygon.contains(pnt):
                    points.append(pnt)
                    # add 1 to polygon index for the polygon name since 0 is reserved for pts outside polys
                    self.point_assignments = self.point_assignments.append(
                        {'polygon' : p_index + 1, 'x' : pnt.x, 'y' : pnt.y}, ignore_index = True)
                    n -= 1
        return points
    
    def generate_noise_points(self, num_pts, polygons):
        points = []
        n = num_pts
        while n > 0:
            outside_polygon = True
            pnt = Point(rand.uniform(0, 100), rand.uniform(0, 100))
            for polygon in polygons:
                # Only add a point if is not in a polygon
                if polygon.contains(pnt):
                    outside_polygon = False
                    break
            if outside_polygon:
                points.append(pnt)
                self.point_assignments = self.point_assignments.append(
                    {'polygon' : 0, 'x' : pnt.x, 'y' : pnt.y}, ignore_index = True)
                n -= 1
        return points
    
    def plot(self, polygons, points, noise_points):
        fig = plt.figure(1, figsize=(9,9), dpi=90)
        ax = fig.add_subplot(111)
        for polygon in polygons:
            patch = PolygonPatch(polygon, facecolor='b', edgecolor='b',
                            alpha=0.5, zorder=2)
            ax.add_patch(patch)

        for point in points:
            ax.scatter(point.x, point.y)
        
        for point in noise_points:
            ax.scatter(point.x, point.y)

        ax.set_title("Polygons with internal points and noise points")
        plt.axis([0, 120, 0, 120])
        plt.show()