import numpy as np

# Set NumPy print options to display with 6 decimal places.
np.set_printoptions(precision=6)

def build_transformation_matrix(unit_cell: np.ndarray) -> np.ndarray:
    """
    Construct the transformation matrix to fractionalize the coordinates.
    
    :param unit_cell: an array containing the unit cell parameters in the order: a, b, c, alpha, beta, gamma
                      (lattice vectors in angstrom, angles in degree)
                      
    :return: a 3x3 transformation matrix.
    """

    if not isinstance(unit_cell, np.ndarray) or unit_cell.shape != (6,):
        raise ValueError("unit_cell must be a numpy array of shape (6,)")
    
    if np.any(unit_cell == 0):
        raise ValueError("Unit cell parameters must be non-zero.")

    # Define unit cell parameters with angles in radians
    a = unit_cell[0]
    b = unit_cell[1]
    c = unit_cell[2]
    alpha = np.deg2rad(unit_cell[3])
    beta = np.deg2rad(unit_cell[4])
    gamma = np.deg2rad(unit_cell[5])

    cos_alpha_star = ((np.cos(beta)) * np.cos(gamma) - np.cos(alpha)) / (np.sin(beta) * np.sin(gamma))
    sin_alpha_star = np.sqrt(1 - cos_alpha_star**2)

    transformation_matrix = np.array([
        [a, b * np.cos(gamma), c * np.cos(beta)],
        [0, b * np.sin(gamma), -c * np.sin(beta) * cos_alpha_star],
        [0, 0, c * np.sin(beta) * sin_alpha_star]
    ], dtype=np.float64)

    return transformation_matrix

def convert_to_fractional_coordinates(cartesian_coords: np.ndarray, unit_cell: np.ndarray) -> np.ndarray:
    """
    Convert an array of atomic Cartesian coordinates to fractional coordinates.

    :param cartesian_coords: An array with lists of xyz coordinates in angstrom of the atoms as elements.
    :param unit_cell: an array containing the unit cell parameters in the order: a, b, c, alpha, beta, gamma
                      (lattice vectors in angstrom, angles in degree)

    :return: A 2D array with the fractional coordinates.
    """

    if not isinstance(cartesian_coords, np.ndarray) or cartesian_coords.ndim != 2 or cartesian_coords.shape[1] != 3:
        raise ValueError("Cartesian_coords must be a numpy array of shape (n, 3) where n is the number of atoms.")

    transformation_matrix = build_transformation_matrix(unit_cell)
    fractional_coordinates = cartesian_coords @ np.linalg.inv(transformation_matrix).T

    return fractional_coordinates

def convert_to_cartesian_coordinates(fractional_coords: np.ndarray, unit_cell: np.ndarray) -> np.ndarray:
    """
    Convert an array of atomic fractional coordinates to Cartesian coordinates.

    :param cartesian_coords: An array with lists of xyz coordinates in angstrom of the atoms as elements.
    :param unit_cell: an array containing the unit cell parameters in the order: a, b, c, alpha, beta, gamma
                      (lattice vectors in angstrom, angles in degree)

    :return: A 2D array with the cartesian coordinates.
    """

    if not isinstance(fractional_coords, np.ndarray) or fractional_coords.ndim != 2 or fractional_coords.shape[1] != 3:
        raise ValueError("fractional_coords must be a numpy array of shape (n, 3) where n is the number of atoms.")

    transformation_matrix = build_transformation_matrix(unit_cell)
    fractional_coordinates = fractional_coords @ transformation_matrix.T

    return fractional_coordinates