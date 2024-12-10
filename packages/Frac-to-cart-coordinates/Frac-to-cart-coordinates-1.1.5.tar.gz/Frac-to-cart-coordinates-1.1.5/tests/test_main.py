import unittest
import numpy as np

import sys
from pathlib import Path

# Add the parent directory of the current script to sys.path
current_path = Path(__file__).resolve()
parent_directory = current_path.parent.parent  # Go up two levels to the base directory
sys.path.append(str(parent_directory))

from Fractocart.main import convert_to_fractional_coordinates, convert_to_cartesian_coordinates

from test_arrays.dihydroazulene import unit_cell_DHA, cartesian_coordinates_DHA, fractional_coordinates_DHA
from test_arrays.anil import unit_cell_anil, cartesian_coordinates_anil, fractional_coordinates_anil
from test_arrays.sio2 import unit_cell_sio2, cartesian_coordinates_sio2, fractional_coordinates_sio2


class TestCoordinateConversion(unittest.TestCase):
    """
    Unit tests for the coordinate conversion functions in the Fractocart module.
    This class tests the conversion between Cartesian and fractional coordinates,
    as well as handling of invalid inputs and edge cases.


    To set the examples, the required precision was assesed by running single point energy and
    static polarizability calculations on the test systems using the CRYSTAL23 code.
    """

    def setUp(self):
        """
        Set up the unit cell parameters and test data for the coordinate conversion tests.
        Initializes the unit cell, Cartesian coordinates, and expected fractional coordinates.
        """

        self.examples = [
            (fractional_coordinates_anil, unit_cell_anil, cartesian_coordinates_anil),
            (fractional_coordinates_DHA, unit_cell_DHA, cartesian_coordinates_DHA),
            (fractional_coordinates_sio2, unit_cell_sio2, cartesian_coordinates_sio2),
        ]

    def test_convert_to_cartesian_coordinates(self):
        """
        Test the conversion from fractional coordinates to Cartesian coordinates.
        Asserts that the result matches the original Cartesian coordinates within a tolerance.
        """

        for fractional_coords, unit_cell, expected_cartesian_coords in self.examples:
            result = convert_to_cartesian_coordinates(fractional_coords, unit_cell)
            np.testing.assert_almost_equal(result, expected_cartesian_coords, decimal=5,
                                        err_msg=f"Failed for {fractional_coords} with unit cell {unit_cell}")
            
    def test_convert_to_fractional_coordinates(self):
        """
        Test the conversion from Cartesian coordinates to fractional coordinates.
        Asserts that the result matches the original fractional coordinates within a tolerance.
        """

        for expected_fractional_coords, unit_cell, cartesian_coords in self.examples:
            result = convert_to_fractional_coordinates(cartesian_coords, unit_cell)
            np.testing.assert_almost_equal(result, expected_fractional_coords, decimal=5,
                                        err_msg=f"Failed for {cartesian_coords} with unit cell {unit_cell}")

    def test_invalid_cartesian_input(self):
        """
        Test the conversion function with invalid Cartesian input.
        Asserts that a ValueError is raised when the input does not have the correct shape.
        """

        with self.assertRaises(ValueError):
            convert_to_fractional_coordinates(np.array([[1.0, 2.0]]), unit_cell_anil)

    def test_invalid_fractional_input(self):
        """
        Test the conversion function with invalid fractional input.
        Asserts that a ValueError is raised when the input does not have the correct shape.
        """

        with self.assertRaises(ValueError):
            convert_to_cartesian_coordinates(np.array([[0.2, 0.4]]), unit_cell_anil)

    def test_zero_param_unit_cell(self):
        """
        Test the conversion function with a zero-length unit cell.
        Asserts that a ValueError is raised when the unit cell contains a zero length.
        """

        zero_unit_cell = np.array([0.0, 5.0, 5.0, 90.0, 90.0, 90.0])
        with self.assertRaises(ValueError):
            convert_to_fractional_coordinates(cartesian_coordinates_anil, zero_unit_cell)
