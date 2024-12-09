# QDX-py

Python bindings to qdx-commons, built with [maturin / py03](https://pyo3.rs).

```
NAME
    qdx_py - QDX-Common utilities for python

PACKAGE CONTENTS
    qdx_py

FUNCTIONS
    concat(conformer_1_contents, conformer_2_contents)
        Takes two conformer json strings and concatenates them

    conformer_to_pdb(conformer_contents)
        Returns the pdb string for a qdx conformer json string

    conformer_to_sdf(conformer_contents)

    drop_amino_acids(conformer_contents, amino_acids_to_drop)
        Drops amino acids from a conformer json string

    drop_residues(conformer_contents, residues_to_drop)
        Drops residues from a conformer json string

    formal_charge(conformer_contents, missing_atom_strictness)
        Charges standard amino acids given a conformer json string,

    fragment(conformer_contents, missing_atom_strictness, backbone_steps, terminal_fragment_sidechain_size=None)
        Fragments a conformer, updating the fragment formal charges based on existing atom charges

    fragment_by_label(conformer_contents, missing_atom_strictness)
        Fragments a conformer by atom labels, updating the fragment formal charges based on existing atom charges

    fragment_legacy(conformer_contents, bond_length_tolerance, backbone_steps, terminal_fragment_sidechain_size=None)
        Fragments a conformer, using distance based bond inference instead of pattern based bond inference

    pdb_to_conformer(pdb_contents, keep_residues=None, skip_residues=None)
        Converts a pdb string into an array of qdx conformers as a json string

    sdf_to_conformer(sdf_contents)
```

## Usage

```python
import qdx_py
# get json string of conformer
conformer = qdx_py.pdb_to_conformer(open("../qdx-common/tests/data/6mj7.pdb").read())
# get pdb of conformer
pdb = qdx_py.conformer_to_pdb(conformer)
```

## Developing

```sh
~ setup venv
maturin develop
python
~ import qdx_py
```

## Publishing

```sh
export MATURIN_PYPI_TOKEN=[your token]
maturin publish --manylinux 2_28 --zig -f
```
