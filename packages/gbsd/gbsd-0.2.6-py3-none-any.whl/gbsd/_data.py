"""Holds useful data such as scattering lengths."""
import numpy as np

# Bound coherent scattering lengths, in fm, from https://www.ncnr.nist.gov/resources/n-lengths/
NEUTRON_SCATTERING_LENGTHS = {
    "Si": 4.1491,
    "O": 5.803,
}

# From http://lampx.tugraz.at/~hadley/ss1/crystaldiffraction/atomicformfactors/formfactors.php
XRAY_FORM_FACTOR_PARAMS = {
    "Si": {
        "a": [6.2915, 3.0353, 1.9891, 1.541],
        "b": [2.4386, 32.3337, 0.6785, 81.6937],
        "c": [1.1407]
    },
    "O": {
        "a": [3.0485, 2.2868, 1.5463, 0.867],
        "b": [13.2771, 5.7011, 0.3239, 32.9089],
        "c": [0.2508],
    }
}