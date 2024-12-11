from typing import Optional

import jax 
import jax.numpy as np 
import jax.random as npr
import shapely 

import estimators 
import geometry_utils

key: np.ndarray = npr.PRNGKey(0)
DTYPE: type = np.float32
DOMAIN_BOUNDS: np.ndarray = np.array([0., 0., 1., 1.])
FIBER_LENGTH: np.ndarray = np.array(2e-01)
NUM_FIBERS: int = 25

def random_convex_polygon(key: np.ndarray, num_points: Optional[int] = 7) -> tuple[shapely.Polygon, np.ndarray]: 
    xkey, ykey = npr.split(key)
    points: np.ndarray = np.stack(
    (
            npr.uniform(xkey, (num_points,), minval=DOMAIN_BOUNDS[0], maxval=DOMAIN_BOUNDS[2]), 
            npr.uniform(ykey, (num_points,), minval=DOMAIN_BOUNDS[1], maxval=DOMAIN_BOUNDS[3])
    ), axis=-1)
    convex_hull: shapely.Polygon = shapely.convex_hull(shapely.MultiPoint(points))
    convex_hull_points: np.ndarray = np.array(convex_hull.exterior.coords)[1:]
    return (convex_hull, convex_hull_points)

def fiber_to_line(fiber: np.ndarray) -> shapely.LineString: 
    return shapely.LineString([fiber[0], fiber[1]])

def test_convex_clipping(): 
    fiber_key, polygon_key = npr.split(key)
    convex_hull, convex_hull_points = random_convex_polygon(polygon_key)
    fibers: np.ndarray = estimators.sample(fiber_key, DOMAIN_BOUNDS, NUM_FIBERS, FIBER_LENGTH, dtype=DTYPE)
    shapely_fibers: list[shapely.LineString] = [fiber_to_line(f) for f in fibers]

    clipped_fibers: np.ndarray = geometry_utils.clip_inside_convex_hull(fibers, convex_hull_points[:-1])
    not_collapsed_indices: np.ndarray = np.all(clipped_fibers[:, 1] != clipped_fibers[:, 0], axis=-1)
    clipped_fibers = clipped_fibers[not_collapsed_indices]
    shapely_clipped_fibers: list[np.ndarray] = [] 
    for f in shapely_fibers: 
        intersection_array = np.array(shapely.intersection(f, convex_hull).coords)
        if intersection_array.size > 0: 
            shapely_clipped_fibers.append(intersection_array)

    shapely_clipped_fibers = np.array(shapely_clipped_fibers)
    shapely_clipped_fibers: list[np.ndarray] = [] 
    for fiber in shapely_fibers: 
        intersection_array = np.array(shapely.intersection(fiber, convex_hull).coords)
        if intersection_array.size > 0: 
            shapely_clipped_fibers.append(intersection_array)
    shapely_clipped_fibers: np.ndarray = np.array(shapely_clipped_fibers).astype(DTYPE)
    assert np.allclose(clipped_fibers, shapely_clipped_fibers)