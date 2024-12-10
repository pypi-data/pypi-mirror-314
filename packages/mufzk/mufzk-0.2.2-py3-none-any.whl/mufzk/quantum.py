import numpy as np
from scipy.linalg import qr


# randomly create a NxN-dimensional unitary operator
def random_unitary(num_qubits=1, dtype="float"):
    assert num_qubits >= 1, f"num_qubits should be greater than or equal to 1."
    if dtype == "float":
        N = int(2 ** num_qubits)
        H = np.random.randn(N, N)
        Q, R = qr(H)
    elif dtype == "complex":
        N = int(2 ** num_qubits)
        H_real = np.random.randn(N, N)
        H_imag = np.random.randn(N, N)
        Q, R = qr(H_real + 1j*H_imag)
    else:
        raise AttributeError(f"dtype should be either 'float' or 'complex', not {dtype}")
    return Q


# randomly create a N-dimensional quantum state
def random_state(num_qubits=1, dtype="float"):
    assert num_qubits >= 1, f"num_qubits should be greater than or equal to 1."
    if dtype == "float":
        angle = 2 * np.pi * np.random.random()
        state = np.array([np.cos(angle), np.sin(angle)])
        if num_qubits == 1:
            return state
        else:
            for _ in range(num_qubits - 1):
                angle = 2 * np.pi * np.random.random()
                state = np.kron(state, np.array([np.cos(angle), np.sin(angle)]))
            return state
    elif dtype == "complex":
        return random_state(num_qubits) + 1j * random_state(num_qubits)
    else:
        raise AttributeError(f"dtype should be either 'float' or 'complex', not {dtype}")


def print_statevector(statevector, decimals=3):
    n = len(statevector.dims())
    N = int(2 ** n)
    data = statevector.data
    const = np.round(data[0], decimals)
    sv_str = f"{const} |{bin(0)[2:].zfill(n)}⟩"
    for i in range(1, N):
        const = np.round(data[i], decimals)
        if const.real < 0:
            sv_str += f" - {-1 * const} |{bin(i)[2:].zfill(n)}⟩"
        else:
            sv_str += f" + {const} |{bin(i)[2:].zfill(n)}⟩"
    print(sv_str)
