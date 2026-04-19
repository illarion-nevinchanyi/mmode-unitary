# m-mode unitary decomposition (browser)

Interactive web page to decompose an \(n\times n\) **unitary matrix** using the **m-mode** (embedded RQ / Tetris) procedure. The same numerics as the NumPy notebook run in the browser via **[Pyodide](https://pyodide.org/)** and **[NumPy](https://numpy.org/)**.

**Author / implementation:** Illarion Nevinchanyi (student, TU Wien) — contact: [e11844409@student.tuwien.ac.at](mailto:e11844409@student.tuwien.ac.at).

**Method (citation):** J. Arends *et al.*, “Decomposing large unitaries into multimode devices of arbitrary size,” *Phys. Rev. Research* **6**, L012043 (2024). [DOI: 10.1103/PhysRevResearch.6.L012043](https://doi.org/10.1103/PhysRevResearch.6.L012043)

## Contents

| File | Role |
|------|------|
| [`index.html`](index.html) | Single-page UI: matrix input, random unitary, decomposition, **Q̃<sub>k</sub><sup>†</sup>** tables, circuit schematic, JSON export |
| [`mmode_core.py`](mmode_core.py) | Pure NumPy: `mmode_with_steps`, JSON helpers (loaded by Pyodide at runtime) |

## Run locally

You must serve the folder over **HTTP** (the page `fetch`es `mmode_core.py` and loads WebAssembly). Opening `index.html` as `file://` usually fails.

```bash
cd mmode-unitary-web   # or path to this folder
python3 -m http.server 8765
```

Open **http://127.0.0.1:8765/** in your browser. The first load may take a minute while Pyodide downloads; later visits use the cache.
