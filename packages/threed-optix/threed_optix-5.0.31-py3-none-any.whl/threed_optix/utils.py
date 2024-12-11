import numpy as np
from scipy.stats import norm
import cv2
import threed_optix.package_utils.vars as v
# import matlabparser as mpars
# import threed_optix.package_utils.matlab as mt
import re
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from typing import List
import math
from threed_optix.package_utils.vars import eQuickFocus
import threed_optix as tdo

def wavelengths_normal_distribution(mean_wavelength, std_dev, num_wavelengths):
    wavelengths = {}
    wavelengths_list = np.linspace(mean_wavelength - 3 * std_dev, mean_wavelength + 3 * std_dev, num_wavelengths)
    weights =  norm.pdf(wavelengths_list, mean_wavelength, std_dev)
    sum_of_weights = np.sum(weights)

    for i in range(num_wavelengths):
        wavelength = wavelengths_list[i]
        weight = weights[i] * (v.WEIGHTS_RANGE[1] - v.WEIGHTS_RANGE[0]) / sum_of_weights + v.WEIGHTS_RANGE[0]
        weight = np.maximum(v.WEIGHTS_RANGE[0], np.minimum(v.WEIGHTS_RANGE[1], weight))
        wavelengths[wavelength] = weight

    return wavelengths

def wavelengths_uniform_distribution(min_wavelength, max_wavelength, num_wavelengths):
    wavelengths = {}
    wavelengths_list = np.linspace(min_wavelength, max_wavelength, num_wavelengths)
    weight = 1.0 / num_wavelengths  # Equal weight for each wavelength

    for wavelength in wavelengths_list:
        wavelengths[wavelength] = weight

    return wavelengths

def calculate_spot_size(intensity_matrix):
    # Convert the intensity matrix to uint8 type for processing
    intensity_image = np.array(intensity_matrix, dtype=np.uint8)

    # Apply thresholding to extract the spot
    _, thresholded = cv2.threshold(intensity_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Find contours of the spot
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Assuming the largest contour corresponds to the spot
    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        # Calculate the minimum enclosing circle around the contour
        (_, _), radius = cv2.minEnclosingCircle(largest_contour)
        # Calculate diameter from radius
        spot_diameter = 2 * radius
        return spot_diameter

    return float('inf')

def center_of_energy_mass(matrix):
    total_mass = sum(sum(row) for row in matrix)

    center_row = sum(i * sum(row) for i, row in enumerate(matrix, start=1)) / total_mass
    center_col = sum(j * matrix[i-1][j-1] for i, row in enumerate(matrix, start=1) for j in range(1, len(row)+1)) / total_mass

    return (center_col, center_row)

def encircled_energy(matrix, percent = 0.9):
    center_point = center_of_energy_mass(matrix)
    # Generate a grid of indices
    indices = np.indices(matrix.shape)

    # Calculate distances from each point in the matrix to the center point
    distances = np.sqrt((indices[0] - center_point[0])**2 + (indices[1] - center_point[1])**2)

    # Flatten the distances and spot matrix for sorting
    flat_distances = distances.flatten()
    flat_spot_matrix = matrix.flatten()

    # Get the indices of the distances within the potential circle
    inside_circle_indices = flat_distances <= flat_distances.max()

    # Sort the relevant distances and corresponding spot matrix values
    sorted_indices = np.argsort(flat_distances[inside_circle_indices])
    sorted_distances = flat_distances[inside_circle_indices][sorted_indices]
    sorted_spot_matrix = flat_spot_matrix[inside_circle_indices][sorted_indices]

    # Calculate cumulative distribution of energy
    cumulative_energy = np.cumsum(sorted_spot_matrix)

    # Find the index where cumulative energy exceeds 90%
    threshold_index = np.argmax(cumulative_energy >= percent * cumulative_energy[-1])

    # Use the distance at the threshold index as the radius
    radius = sorted_distances[threshold_index]

    return radius, center_point

def absolute_pixel_size(resolution, size):
    # Calculate pixel size for width and height
    pixel_size_width = size[0] / resolution[0]
    pixel_size_height = size[1] / resolution[1]

    return (pixel_size_width, pixel_size_height)

def visualize_spot(matrix, center_point, radius):
    plt.figure(figsize=(10, 10))
    plt.imshow(matrix)
    plt.scatter(center_point[1], center_point[0], marker='x', color='red')
    plt.gca().add_patch(plt.Circle((center_point[1], center_point[0]), radius, color='red', fill=False))
    plt.show()

def visualize_matrix(matrix, interactive = False, title = None):
    '''
    Visualize a specific matrix from the results.

    Args:
        matrix: Results matrix you want to visualize
        interactive (bool, default False): Toggle interactive results visualization
        title (str, default None): Title for the results

    Returns:
        None
    '''
    if interactive:
        fig = px.imshow(matrix, color_continuous_scale = v.COLOR_SCALE)
        if title:
            fig.update_layout(title_text = title)
        fig.show()

    else:
        plt.figure(figsize=(10, 10))
        plt.imshow(matrix)
        if title:
            plt.title(title)
        plt.show()

    return

def visualize_results(results: pd.DataFrame, polarization = 'X', light_source_id = 'Total', wavelength = None, interactive = False):
    '''
    Visualize analysis results.

    Args:
        results: The results that are returned from .run() method
        polarization (str, default 'X'): The type of polarization of the results. 'X', 'Y', 'Z' or 'None'
        light_source_id (str, default Total): The light source you want to see the results of, showing all by default
        wavelength (float, default None): The wavelength which you want to see the results of, showing all by default
        interactive (bool, default False): Toggle interactive results visualization
    Returns:
        None
    '''
    spot_target_key = 'spot_target_kind' if light_source_id == 'Total' else 'spot_target'
    if(wavelength is not None):
        wavelength = float(wavelength)
        visualize_matrix(np.sum(results[(results[spot_target_key] == light_source_id) &
                                        (results['polarization'] == polarization) &
                                        np.isclose(results['wl'], wavelength)]['data']), interactive=interactive)
    else:
        visualize_matrix(np.sum(results[(results[spot_target_key] == light_source_id) & (results['polarization'] == polarization)]['data']), interactive=interactive)

    return None

def quick_focus(ray_table: tdo.analyses.RayTable, point:list[float], detector: tdo.parts.Detector) -> None:
    '''
    Quick focus for detector

    Args:
        ray_table (RayTable): The Ray table results when using setup.run()
        point (list of length 3): A point in the setup which is atmost 10 mm away from a light ray. The point should be in the vacinity of the true focus point same as in the website. If a given point is too far, an error will occur.
        detector (threed_optix detector object): The detector object which you want to focus

    Returns:
        None
    '''
    QuickFocusHelpers._validate_input(p_point=point,p_ray_table=ray_table,p_detector=detector)
    origin_surfaces, target_surfaces = QuickFocusHelpers._find_rays_in_sphere(p_ray_table=ray_table,
                                                                       p_point=point)

    chief_ray,chief_rays, relevant_rays = QuickFocusHelpers._find_relevent_rays(p_ray_table= ray_table,
                                                            p_target_surfaces = target_surfaces,
                                                            p_origin_surfaces = origin_surfaces)

    relevant_ray_datos = [QuickFocusHelpers._get_ray_data(ray) for ray in relevant_rays]
    relevant_rays_start_points = np.array([ray_data['start_point'] for ray_data in relevant_ray_datos])
    relevant_rays_end_points = np.array([ray_data['end_point'] for ray_data in relevant_ray_datos])

    # Calculate direction vectors for each ray and normalize them
    rays_directions = relevant_rays_end_points - relevant_rays_start_points
    distances = np.linalg.norm(rays_directions, axis=1, keepdims=True)
    rays_directions = rays_directions / distances  # Normalize directions

    chief_ray_data = QuickFocusHelpers._get_ray_data(chief_ray)
    chief_start_point,chief_direction = chief_ray_data['start_point'], chief_ray_data['direction']
    initial_pose = QuickFocusHelpers._calculate_end_with_orientation(start = chief_start_point,direction = chief_direction)

    segment_start = chief_start_point
    segment_end = chief_ray_data['end_point']

    best_pose = QuickFocusHelpers._find_best_pose(p_chief_ray_data=chief_ray_data,
                                p_start_points=relevant_rays_start_points,
                                p_directions=rays_directions,
                                p_segment_start=segment_start,
                                p_segment_end=segment_end,
                                p_chief_direction=chief_direction,
                                p_detector=detector,
                                p_initial_pose=initial_pose,
                                p_relevant_rays=relevant_rays)

    detector.change_pose(best_pose)

    return

class QuickFocusHelpers:
    @staticmethod
    def _validate_input(p_ray_table: tdo.analyses.RayTable, p_point:list[float], p_detector: tdo.parts.Detector) -> None:
        if (not isinstance(p_point, list) or len(p_point) != 3 or not isinstance(p_ray_table,tdo.analyses.RayTable) or not isinstance(p_detector, tdo.parts.Detector)):
            raise Exception("Invalid input! Input should be:\npoint: list[3]\nray_table: RayTable object\ndetector: Detector object")
        return

    @staticmethod
    def _find_rays_in_sphere(p_ray_table: tdo.analyses.RayTable, p_point: list[float]):
        origin_surfaces = set()
        target_surfaces = set()
        in_sphere = 0

        for ray in p_ray_table.iterrows():
            ray_data = QuickFocusHelpers._get_ray_data(ray)
            ray_start_point,ray_end_point,ray_direction = ray_data['start_point'],ray_data['end_point'],ray_data['direction']

            is_in_sphere =QuickFocusHelpers._ray_intersects_sphere(p_ray_start = ray_start_point,
                                                    p_ray_end = ray_end_point,
                                                    p_sphere_center_point = p_point,
                                                    p_sphere_radius = v.eQuickFocus.QUICK_FOCUS_RADIUS,
                                                    p_ray_direction = ray_direction,
                                                    p_end_surface= ray[eQuickFocus.RAY_DATA_IDX]['surface'])

            if is_in_sphere:
                target_surfaces.add(ray[eQuickFocus.RAY_DATA_IDX]['surface'])
                origin_surfaces.add(ray[eQuickFocus.RAY_DATA_IDX]['origin_surface'])
                in_sphere += 1
        if in_sphere == 0:
            raise ValueError("0 Rays were found near the input point, please enter a different point.")

        return origin_surfaces, target_surfaces

    @staticmethod
    def _find_relevent_rays(p_ray_table:tdo.analyses.RayTable, p_target_surfaces, p_origin_surfaces):
        relevant_rays = []
        chief_ray = None
        chief_rays = []

        for ray in p_ray_table.iterrows():
            if ray[eQuickFocus.RAY_DATA_IDX]['surface'] in p_target_surfaces and ray[eQuickFocus.RAY_DATA_IDX]['origin_surface'] in p_origin_surfaces:
                relevant_rays.append(ray)
                if "chief_ray" in ray[eQuickFocus.RAY_DATA_IDX]['light_source']:
                    chief_ray = ray
                    chief_rays.append(ray)

        return chief_ray,chief_rays, relevant_rays

    @staticmethod
    def _get_ray_data(p_ray) -> dict[str:float]:
        data = {}
        data["start_point"] = [p_ray[eQuickFocus.RAY_DATA_IDX]['Ox'],p_ray[eQuickFocus.RAY_DATA_IDX]['Oy'],p_ray[eQuickFocus.RAY_DATA_IDX]['Oz']]
        data["direction"] = [p_ray[eQuickFocus.RAY_DATA_IDX]['Dx'],p_ray[eQuickFocus.RAY_DATA_IDX]['Dy'],p_ray[eQuickFocus.RAY_DATA_IDX]['Dz']]
        data["end_point"] = [p_ray[eQuickFocus.RAY_DATA_IDX]['Hx'],p_ray[eQuickFocus.RAY_DATA_IDX]['Hy'],p_ray[eQuickFocus.RAY_DATA_IDX]['Hz']] if p_ray[eQuickFocus.RAY_DATA_IDX]['surface'] != -1 else QuickFocusHelpers._calculate_endpoint(start=data['start_point'], direction=data['direction'])

        return data

    @staticmethod
    def _find_best_pose(p_chief_ray_data,
                        p_start_points,
                        p_directions,
                        p_relevant_rays,
                        p_detector,
                        p_segment_start,
                        p_segment_end,
                        p_chief_direction,
                        p_initial_pose) -> list[float]:

        best_pose = p_initial_pose
        segment_len = QuickFocusHelpers._calculate_distance(p_segment_start,p_segment_end,p_chief_direction)

        while(segment_len > 0.001):
            best_pose = QuickFocusHelpers._calculate_min_rms_position(p_segment_start = p_segment_start,
                                                                p_segment_end = p_segment_end,
                                                                p_chief_ray_data = p_chief_ray_data,
                                                                p_start_points = p_start_points,
                                                                p_directions=p_directions,
                                                                p_relevant_rays = p_relevant_rays,
                                                                p_current_best_pose=best_pose,
                                                                p_detector = p_detector)
            segment_len /= 10
            p_segment_end = np.add(best_pose[:3], np.multiply(p_chief_direction,segment_len))
            p_segment_start = np.subtract(best_pose[:3] , np.multiply(p_chief_direction,segment_len))

        return best_pose

    @staticmethod
    def _ray_intersects_sphere(
        p_ray_start: list[float],
        p_ray_end: list[float],
        p_sphere_center_point: list[float],
        p_ray_direction: list[int],
        p_end_surface: int | str,
        p_sphere_radius: float
    ) -> bool:
        """
        Determine if a ray (line segment) intersects with a sphere.

        Args:
            p_ray_start (list[float]): Start point of the ray [x, y, z].
            p_ray_end (list[float]): End point of the ray [x, y, z].
            p_sphere_center_point (list[float]): Center of the sphere [x, y, z].
            p_ray_direction (list[int]): Direction of the ray (unused if p_end_surface != -1).
            p_end_surface (int | str): Determines if p_ray_end should be recalculated.
            p_sphere_radius (float): Radius of the sphere.

        Returns:
            bool: True if the ray intersects the sphere, False otherwise.
        """
        # If no hit surface for ray, calculate an end point based on direction and start point
        if p_end_surface == -1:
            p_ray_end = QuickFocusHelpers._calculate_endpoint(start=p_ray_start, direction=p_ray_direction)

        # Ensure inputs are mutable lists
        p_ray_start = list(p_ray_start)
        p_ray_end = list(p_ray_end)
        p_sphere_center_point = list(p_sphere_center_point)

        # Direction vector of the ray
        a_ray_direction = np.subtract(p_ray_end, p_ray_start)

        # Calculate the vector from the ray's start to the sphere's center (start - center)
        start_to_point = [p_ray_start[i] - p_sphere_center_point[i] for i in range(3)]

        # Quadratic coefficients
        a = np.dot(a_ray_direction, a_ray_direction)
        b = 2 * np.dot(a_ray_direction, start_to_point)
        c = np.dot(start_to_point, start_to_point) - p_sphere_radius**2

        # Solve the quadratic equation a*t^2 + b*t + c = 0
        discriminant = b**2 - 4*a*c

        if discriminant < 0:
            # No real roots, the line does not intersect the sphere
            return False

        # Calculate the roots (parametric values t1 and t2)
        sqrt_discriminant = np.sqrt(discriminant)
        t1 = (-b - sqrt_discriminant) / (2 * a)
        t2 = (-b + sqrt_discriminant) / (2 * a)

        # Check if either t1 or t2 lies within the range [0, 1]
        in_sphere = (0 <= t1 <= 1) or (0 <= t2 <= 1)

        return in_sphere

    @staticmethod
    def _calculate_endpoint(start: list[float], direction: list[int], max_distance = v.eQuickFocus.MAX_DISTANCE_TRACING) -> list[float]:
        # Convert start and direction to numpy arrays for vector calculations
        start = np.array(start)
        direction = np.array(direction)

        # Normalize the direction vector
        direction /= np.linalg.norm(direction)

        # Scale the direction by the max distance to get the endpoint
        end = start + direction * max_distance

        return end.tolist()

    @staticmethod
    def _calculate_end_with_orientation(start: list[float], direction: list[float]) -> list[float]:

        end = QuickFocusHelpers._calculate_endpoint(start=start, direction= direction)

        # Calculate orientation angles based on the direction vector
        # Alpha (pitch), Beta (yaw), Gamma (roll)
        alpha = -1 * np.arctan2(direction[1], direction[2])  # Rotation around X-axis (pitch)
        beta = -1 *np.arctan2(-direction[0], np.sqrt(direction[1]**2 + direction[2]**2))  # Rotation around Y-axis (yaw)
        gamma = 0  # Rotation around Z-axis (roll), assuming no twist

        # Convert angles from radians to degrees for easier interpretation
        alpha = np.degrees(alpha)
        beta = np.degrees(beta)
        gamma = np.degrees(gamma)

        # Return end point and orientation angles
        return [end[0], end[1], end[2], alpha, beta, gamma]

    @staticmethod
    def _calculate_min_rms_position(
        p_chief_ray_data: dict,
        p_segment_start: list,
        p_segment_end: list,
        p_relevant_rays: list,
        p_directions: list,
        p_start_points: list,
        p_current_best_pose: list,
        p_detector: tdo.parts.Detector,
        p_segments: int = v.eQuickFocus.NUM_SEGMENTS
        ) -> list[float]:

        chief_direction = np.array(p_chief_ray_data['direction'])
        total_distance = QuickFocusHelpers._calculate_distance(p_segment_start,p_segment_end,chief_direction)
        segment_length = total_distance / p_segments

        # Initialize variables to track minimal radius and corresponding point
        min_rms = float('inf')
        min_radius_point = None

        # Iterate over each segment along the chief ray
        for i in range(p_segments):
            # Calculate the midpoint of the current segment on the chief ray path
            segment_center = np.add(p_segment_start, np.multiply(chief_direction, (segment_length * i)))

            detector_intersection_points = [QuickFocusHelpers._get_ray_surface_intersection(ray_origin = ray_start,
                                                                ray_direction = ray_direction,
                                                                surface_position = segment_center,
                                                                surface_normal = np.multiply(chief_direction ,(-1)),
                                                                width = p_detector.size[0] * 2,
                                                                height = p_detector.size[1] * 2) for ray_direction,ray_start in zip(p_directions,p_start_points)]

            centroid = QuickFocusHelpers._find_centroid(detector_intersection_points, p_relevant_rays)
            rms = QuickFocusHelpers._calc_rms(centroid,detector_intersection_points)

            if(rms < min_rms):
                min_rms = rms
                min_radius_point = segment_center
        # Return the point on the chief ray path with minimal radius and given detector angle
        new_detector_pose = list(min_radius_point) + p_current_best_pose[3:]
        return new_detector_pose

    @staticmethod
    def _get_ray_surface_intersection(ray_origin, ray_direction,
                                    surface_position, surface_normal,
                                    width: float, height: float) -> list[float] | None:
        """
        Calculate the intersection of a ray with a rectangular surface.

        Args:
            ray_origin (list[float]): Origin of the ray [x, y, z].
            ray_direction (list[float]): Direction of the ray [x, y, z] (should be normalized).
            surface_position (list[float]): Position of the surface's center [x, y, z].
            surface_normal (list[float]): Normal vector of the surface [x, y, z] (normalized).
            width (float): Width of the rectangular surface.
            height (float): Height of the rectangular surface.

        Returns:
            list[float] or None: Intersection point [x, y, z] or None if no intersection.
        """
        # Normalize ray direction
        ray_direction = ray_direction / np.linalg.norm(ray_direction)

        # Calculate denominator for ray-plane intersection
        denominator = np.dot(ray_direction, surface_normal)

        # If the denominator is close to zero, the ray is parallel to the surface
        if abs(denominator) < 1e-6:
            return None  # No intersection

        # Calculate the t parameter for the ray-plane intersection
        difference = np.subtract(surface_position, ray_origin)
        t = np.dot(difference, surface_normal) / denominator

        # If t is negative, the intersection is behind the ray's origin
        if t < 0:
            return None  # No intersection

        # Calculate the intersection point
        intersection_point = np.add(ray_origin, np.multiply(ray_direction, t))

        # Dynamically compute the surface's local u and v vectors
        arbitrary_vector = [1, 0, 0] if abs(surface_normal[0]) < 1 else [0, 1, 0]
        u_vector = np.cross(surface_normal, arbitrary_vector)
        u_vector = u_vector / np.linalg.norm(u_vector)  # Normalize

        v_vector = np.cross(surface_normal, u_vector)
        v_vector = v_vector / np.linalg.norm(v_vector)  # Normalize

        # Project the intersection point onto the surface's local basis
        local_point = np.subtract(intersection_point, surface_position)
        u_distance = np.dot(local_point, u_vector)
        v_distance = np.dot(local_point, v_vector)

        # Check if the intersection point lies within the surface bounds
        if abs(u_distance) <= width / 2 and abs(v_distance) <= height / 2:
            return intersection_point  # Intersection point is within the bounds

        return None  # Intersection point is outside the bounds

    @staticmethod
    def _calculate_distance(p_start, p_end, p_direction) -> float:
        if len(p_start) != 3 or len(p_end) != 3 or len(p_direction) != 3:
            raise ValueError("All input lists must have exactly 3 elements.")

        # Calculate difference vector
        diff = [p_end[i] - p_start[i] for i in range(3)]

        # Normalize direction
        direction_norm = np.linalg.norm(p_direction)
        if direction_norm == 0:
            raise ValueError("Direction vector cannot be zero.")
        p_direction = [d / direction_norm for d in p_direction]

        # Project diff onto direction
        projection_length = sum(diff[i] * p_direction[i] for i in range(3))

        return abs(projection_length)

    def _calculate_ray_intensity(p_ray) -> float:
        """
        Calculate the ray intensity given the p- and s-amplitudes and Fresnel coefficients.

        Args:
            Ap (float): The p amplitude of the ray.
            As (float): The s amplitude of the ray.
            f_p (float): Fresnel coefficient for p-polarization.
            f_s (float): Fresnel coefficient for s-polarization.

        Returns:
            float: The intensity of the ray.
        """
        intensity = (p_ray[eQuickFocus.RAY_DATA_IDX]['f_p'] * p_ray[eQuickFocus.RAY_DATA_IDX]['Ap'])**2 + (p_ray[eQuickFocus.RAY_DATA_IDX]['f_s'] * p_ray[eQuickFocus.RAY_DATA_IDX]['As'])**2
        return intensity

    @staticmethod
    def _find_centroid(p_intersection_points,p_rays) -> list[float]:
        a_weighted_coordinate_x = 0
        a_weighted_coordinate_y = 0
        total_intensity = 0

        for hit,ray in zip(p_intersection_points,p_rays):
            if hit is None:
                continue

            intensity = QuickFocusHelpers._calculate_ray_intensity(ray)
            a_weighted_coordinate_x += hit[eQuickFocus.X_VAL_IDX] * intensity
            a_weighted_coordinate_y += hit[eQuickFocus.Y_VAL_IDX] * intensity
            total_intensity += intensity

        if total_intensity == 0:
            return [-float('inf'),-float('inf')]
        a_x_centroid = a_weighted_coordinate_x / total_intensity
        a_y_centroid = a_weighted_coordinate_y / total_intensity

        return [a_x_centroid, a_y_centroid]

    @staticmethod
    def _calc_rms(p_centroid_data, p_detector_intersection_points) -> float:

        total_sum = 0

        for point in p_detector_intersection_points:
            if point is None:
                continue

            total_sum += (point[eQuickFocus.X_VAL_IDX] - p_centroid_data[eQuickFocus.X_VAL_IDX]) ** 2
            total_sum += (point[eQuickFocus.Y_VAL_IDX] - p_centroid_data[eQuickFocus.Y_VAL_IDX]) ** 2

        if(total_sum == 0):
            return float("inf")

        return math.sqrt(total_sum / len(p_detector_intersection_points))
