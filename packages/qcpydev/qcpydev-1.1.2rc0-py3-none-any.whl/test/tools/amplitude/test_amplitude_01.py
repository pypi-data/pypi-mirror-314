from qcpy import quantumcircuit, amplitude
import numpy as np
def inc(size: int):
    qc = quantumcircuit(qubits = size)
    return amplitude(qc).flatten()

def test_01a():
    assert (
        inc(1) == np.array([ 1+0j, 0+0j ], "F")
    ).all(), "test_01a Failed on Amplitude"

def test_01b():
    assert (
        inc(2) == np.array([ 1+0j, 0+0j, 0+0j, 0+0j ], "F")
    ).all(), "test_01b Failed on Amplitude"

def test_01c():
    assert (
        inc(3) == np.array([ 1+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j ], "F")
    ).all(), "test_01c Failed on Amplitude"

def test_01d():
    assert (
        inc(4) == np.array([ 1+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j ], "F")
    ).all(), "test_01d Failed on Amplitude"

def test_01e():
    assert (
        inc(5) == np.array([ 1+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j, 0+0j ], "F")
    ).all(), "test_01e Failed on Amplitude"
