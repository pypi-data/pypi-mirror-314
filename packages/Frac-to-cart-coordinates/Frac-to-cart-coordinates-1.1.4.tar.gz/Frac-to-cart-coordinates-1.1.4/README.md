# `Frac-to-cart-coordinates`

The `Frac-to-cart-coordinates` package allows users to easily convert atomic coordinates from Cartesian to fractional format and *vice versa*, based on the unit cell parameters.

## Overview

In crystallography, atomic positions within a crystal's unit cell can be described using:
- **Fractional coordinates** $(x/a, y/b, z/c)$, which refer to the natural axes \(a, b, c\), scaled by their respective unit cell lengths.
- **Orthogonal coordinates** $(X, Y, Z)$, which use a right-angled Cartesian system with distances measured in Ångstroms.

For triclinic unit cells, the relationship between these coordinate systems involves a transformation matrix with non-trivial elements.

This implementation follows the methodology described on Jon Cooper's website, [fractorth](https://ic50.org/fractorth/). It relies on the fundamental principles of spherical trigonometry (see [implementation_details](/implementation_details/implementation_details.pdf)).

## Installation
Run the following command in your terminal:

```bash
pip install Frac-to-cart-coordinates
```

Make sure you have numpy installed and Python 3.6 or higher.

## Usage

### Importing the Module

```python
from Fractocart import convert_to_fractional_coordinates, convert_to_cartesian_coordinates
```

### Functions

1. **Convert to Fractional Coordinates**

   ```python
   fractional_coords = convert_to_fractional_coordinates(cartesian_coords, unit_cell)
   ````

2. **Convert to Cartesian Coordinates**

    ```python
    cartesian_coords = convert_to_cartesian_coordinates(fractional_coords, unit_cell)
    ````

## Contributing

Contributions are welcome! To contribute:
1. Clone the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a merge request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


    