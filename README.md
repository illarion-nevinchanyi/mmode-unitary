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

## GitHub: create a new repository

1. Log in to [GitHub](https://github.com) in the browser.
2. Click **+** (top right) → **New repository**.
3. Choose a **Repository name** (e.g. `mmode-unitary-web`).
4. Set **Public** (or Private if you prefer).
5. **Do not** add a README, `.gitignore`, or license *on GitHub* if you already have files locally (avoids merge conflicts). You can add a license later.
6. Click **Create repository**.

GitHub will show commands; use the **“push an existing repository from the command line”** section below if you already ran `git init` locally.

## GitHub: push this folder (first time)

In a terminal, from **this project directory**:

```bash
cd /path/to/mmode-unitary-web

git init
git add .
git commit -m "Initial commit: m-mode unitary decomposition web tool"

# Use your GitHub username and repo name:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

If you use **SSH** instead of HTTPS:

```bash
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

After the first push, later changes are:

```bash
git add .
git commit -m "Describe your change"
git push
```

## GitHub Pages (optional public URL)

1. On the repo: **Settings** → **Pages** (left sidebar).
2. Under **Build and deployment** → **Source**: choose **Deploy from a branch**.
3. **Branch**: `main`, folder **`/ (root)`**, then **Save**.
4. After a minute, the site is at `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/` (exact URL is shown on the Pages settings).

Ensure `index.html` is at the repository root (it is in this layout).

## License

Add a `LICENSE` file in the repo if you want to specify terms (e.g. MIT). The scientific method remains governed by the original paper’s context; this tool is separate implementation work.
