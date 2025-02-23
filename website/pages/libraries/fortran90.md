# Fortran 90 library

The source code of the quadraturerules Fortran 90 library can be downloaded from the
[latest release on GitHub](https://github.com/quadraturerules/quadraturerules/releases/latest/).

The library's tests can be built by running:

```bash
gfortran test.f90 -o test
./test
```

## Usage

The library's function `single_integral_quadrature` can be used to get the points and weights
of quadrature rules. For example the following snippet will create an order 3 Xiao--Gimbutas rule on a
triangle:

```fortran
use quadraturerules
real, allocatable :: points(:,:), weights(:)

call single_integral_quadrature(QR_GaussLegendre, QR_Interval, 5, points, weights)
```

Note that the points returned by the library are represented using
[barycentric coordinates](/barycentric.md).

## Generating the library
The Fortran 90 quadraturerules library can be generated from the templates in the online encyclopedia
of quadrature rules GitHub repo. First clone the repo and move into the library directory:

```bash
git clone https://github.com/quadraturerules/quadraturerules.git
cd quadraturerules/library
```

The Fortran 90 library can then be generated by running:

```bash
python build.py fortran90
```

This will create a directory called fortran90.build containing the Fortran 90 source code.
