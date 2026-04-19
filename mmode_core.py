"""
m-mode unitary decomposition (NumPy only). Extracted from unitary_decomposition.ipynb.
"""

from __future__ import annotations

import json
from typing import Any

import numpy as np


def random_unitary(n: int, rng: np.random.Generator | None = None) -> np.ndarray:
    if rng is None:
        rng = np.random.default_rng()
    X = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    Q, R = np.linalg.qr(X)
    d = np.diagonal(R)
    ph = d / np.abs(d)
    return Q * ph


def rq_decomposition(A: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return (R, Q) with A = R @ Q, R upper triangular, Q unitary."""
    A_rev = np.flipud(np.fliplr(A))
    Q, R = np.linalg.qr(A_rev.T)
    R = R.T
    Q = Q.T
    R = np.flipud(np.fliplr(R))
    Q = np.flipud(np.fliplr(Q))
    return R, Q


def embed_mx_m(Q: np.ndarray, n: int, indices: list[int]) -> np.ndarray:
    U = np.eye(n, dtype=complex)
    for a, i in enumerate(indices):
        for b, j in enumerate(indices):
            U[i, j] = Q[a, b]
    return U


def _first_m_nonzero_cols_in_row(
    U: np.ndarray, row: int, m: int, tol: float, j_max: int
) -> list[int]:
    cols = []
    for j in range(0, j_max + 1):
        if abs(U[row, j]) > tol:
            cols.append(j)
        if len(cols) == m:
            break
    return cols


def mmode_with_steps(
    U: np.ndarray,
    m: int,
    tol: float = 1e-12,
    max_iter_per_row: int = 10000,
) -> tuple[list[np.ndarray], list[tuple[list[int], np.ndarray]], np.ndarray]:
    """
    For each row i = n-1..1, while subdiagonal part of row i is nonzero:
    take the first m nonzero entries in columns 0..i, RQ -> apply U <- U * embed(Q)^H.
    Requires m >= 2.
    """
    if m < 2:
        raise ValueError(
            "m-mode requires m >= 2 (the m = 2 case is the Reck decomposition)."
        )
    U = U.copy().astype(complex)
    n = U.shape[0]
    steps = [U.copy()]
    ops: list[tuple[list[int], np.ndarray]] = []

    for i in range(n - 1, 0, -1):
        it = 0
        while it < max_iter_per_row:
            it += 1
            if np.max(np.abs(U[i, :i])) <= tol:
                break
            cols = _first_m_nonzero_cols_in_row(U, i, m, tol, i)
            mm = len(cols)
            if mm == 0:
                break
            rows = list(range(i - mm + 1, i + 1))
            A = U[np.ix_(rows, cols)]
            _R, Q = rq_decomposition(A)
            Q_full = embed_mx_m(Q, n, cols)
            U = U @ Q_full.conj().T
            steps.append(U.copy())
            ops.append((list(cols), Q.copy()))

        if it >= max_iter_per_row:
            raise RuntimeError(f"m-mode: row {i} did not clear within max_iter_per_row")

    D = U
    return steps, ops, D


def mmode_decomposition(
    U: np.ndarray,
    m: int,
    tol: float = 1e-12,
    max_iter_per_row: int = 10000,
) -> tuple[list[tuple[list[int], np.ndarray]], np.ndarray]:
    _steps, ops, D = mmode_with_steps(U, m, tol=tol, max_iter_per_row=max_iter_per_row)
    return ops, D


def reconstruct_from_D_mmode(
    ops: list[tuple[list[int], np.ndarray]], D: np.ndarray, n: int
) -> np.ndarray:
    """U = U0 @ Q1^H @ Q2^H @ ...  =>  U0 = U @ Qk @ Q_{k-1} @ ..."""
    U_rec = D.copy().astype(complex)
    for cols, Q in reversed(ops):
        Q_full = embed_mx_m(Q, n, cols)
        U_rec = U_rec @ Q_full
    return U_rec


def fidelity(U: np.ndarray, V: np.ndarray) -> float:
    return float(np.abs(np.trace(U.conj().T @ V)) / U.shape[0])


def complex_matrix_to_nested(z: np.ndarray) -> list[list[list[float]]]:
    """2D complex array -> [[[re, im], ...], ...] for JSON."""
    return [[[float(x.real), float(x.imag)] for x in row] for row in z]


def run_decomposition_jsonable(
    U: np.ndarray,
    m: int,
    tol: float = 1e-12,
    max_iter_per_row: int = 10000,
    include_steps: bool = False,
) -> dict[str, Any]:
    """
    Run m-mode decomposition and return a JSON-friendly dict.
    If include_steps is True, include intermediate U copies (can be large).
    """
    U = np.asarray(U, dtype=complex)
    if U.ndim != 2 or U.shape[0] != U.shape[1]:
        raise ValueError("U must be a square matrix")
    n = U.shape[0]

    steps, ops, D = mmode_with_steps(
        U, m, tol=tol, max_iter_per_row=max_iter_per_row
    )

    step_payload: list[dict[str, Any]] = []
    for cols, Q in ops:
        Q_emd = embed_mx_m(Q, n, cols)
        step_payload.append(
            {
                "cols": cols,
                "Q": complex_matrix_to_nested(Q),
                "Q_emd": complex_matrix_to_nested(Q_emd),
            }
        )

    out: dict[str, Any] = {
        "success": True,
        "n": n,
        "m": m,
        "num_ops": len(ops),
        "steps": step_payload,
        "D": complex_matrix_to_nested(D),
    }
    if include_steps:
        out["intermediate_U"] = [complex_matrix_to_nested(s) for s in steps]
    return out


def parse_U_from_json(text: str) -> np.ndarray:
    """Parse JSON: [[[re, im], ...], ...] per row, or real matrix [[...], ...]."""
    data = json.loads(text)
    return _json_to_matrix(data)


def random_unitary_json(n: int, seed: int | None = None) -> str:
    """Return JSON string of [[[re,im],...],...] for random Haar-like unitary."""
    rng = np.random.default_rng(seed)
    U = random_unitary(n, rng=rng)
    return json.dumps(complex_matrix_to_nested(U))


def api_decompose(matrix_json: str, m: int, tol: float = 1e-12) -> str:
    """Parse U from JSON string, run decomposition, return JSON result string."""
    U = parse_U_from_json(matrix_json)
    r = run_decomposition_jsonable(U, m, tol=tol)
    return json.dumps(r)


def _json_to_matrix(data: Any) -> np.ndarray:
    if not isinstance(data, list) or not data:
        raise ValueError("Expected a non-empty JSON array (matrix rows)")
    row0 = data[0]
    # Format: each entry is [re, im]
    if isinstance(row0, list) and row0 and isinstance(row0[0], list):
        # [[re,im], [re,im], ...] per row
        rows = []
        for row in data:
            if not isinstance(row, list):
                raise ValueError("Invalid row")
            rows.append([complex(x[0], x[1]) for x in row])
        return np.array(rows, dtype=complex)
    # Format: each entry is a single number (real) or [re, im] per cell — try real matrix
    if isinstance(row0, list) and row0 and isinstance(row0[0], (int, float)):
        return np.array(data, dtype=complex)
    raise ValueError(
        "Unsupported JSON matrix format. Use [[[re,im],...],...] for complex entries."
    )
