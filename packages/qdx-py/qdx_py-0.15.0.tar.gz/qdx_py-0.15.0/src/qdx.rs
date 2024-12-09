use std::collections::HashSet;

use pyo3::{exceptions::PyRuntimeError, prelude::*};
use qdx_common::{AtomCheckStrictness, Conformer};

/// Converts a pdb string into an array of qdx conformers as a json string
#[pyfunction]
pub fn pdb_to_conformer(
    pdb_contents: String,
    keep_residues: Option<HashSet<String>>,
    skip_residues: Option<HashSet<String>>,
) -> PyResult<String> {
    serde_json::to_string(
        &qdx_common::convert::pdb::from_pdb(pdb_contents, keep_residues, skip_residues)
            .map_err(|e| PyRuntimeError::new_err(e.to_string()))?,
    )
    .map_err(|e| PyRuntimeError::new_err(e.to_string()))
}

/// Converts a pdb string into trc format
#[pyfunction]
pub fn pdb_to_trc(
    pdb_contents: String,
    keep_residues: Option<HashSet<String>>,
    skip_residues: Option<HashSet<String>>,
) -> PyResult<String> {
    let conformer_json = pdb_to_conformer(pdb_contents, keep_residues, skip_residues)?;

    let conformers: serde_json::Value = serde_json::from_str(&conformer_json)
        .map_err(|e| PyRuntimeError::new_err(format!("Failed to parse JSON: {}", e)))?;

    if let Some(first_conformer) = conformers.as_array().and_then(|arr| arr.get(0)) {
        let conformer: qdx_common::conformer::Conformer = serde_json::from_value(first_conformer.clone())
            .map_err(|e| PyRuntimeError::new_err(format!("Failed to deserialize Conformer: {}", e)))?;

        let trc = qdx_common::compat::conformer_to_trc(conformer);
        serde_json::to_string(&trc)
            .map_err(|e| PyRuntimeError::new_err(format!("Failed to serialize TRC: {}", e)))
    } else {
        Err(PyErr::new::<PyRuntimeError, _>("No conformer data found in the array"))
    }
}


/// Returns the pdb string for a qdx conformer json string
#[pyfunction]
pub fn conformer_to_pdb(conformer_contents: String) -> PyResult<String> {
    Ok(qdx_common::convert::pdb::to_pdb(
        &serde_json::from_str(&conformer_contents)
            .map_err(|e| PyRuntimeError::new_err(e.to_string()))?,
    ))
}

#[pyfunction]
pub fn sdf_to_conformer(sdf_contents: String) -> PyResult<String> {
    let conformer = qdx_common::convert::sdf::from_sdf(&sdf_contents)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;
    let conformer_serialized =
        serde_json::to_string(&conformer).map_err(|e| PyRuntimeError::new_err(e.to_string()))?;
    Ok(conformer_serialized)
}

#[pyfunction]
pub fn conformer_to_sdf(conformer_contents: String) -> PyResult<String> {
    let conformer: Conformer = serde_json::from_str(&conformer_contents)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;
    let sdf_serialized = qdx_common::convert::sdf::to_sdf(&conformer)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;
    Ok(sdf_serialized)
}

/// Takes two conformer json strings and concatenates them
#[pyfunction]
pub fn concat(conformer_1_contents: String, conformer_2_contents: String) -> PyResult<String> {
    let mut conformer_1: Conformer = serde_json::from_str(&conformer_1_contents)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    let conformer_2: Conformer = serde_json::from_str(&conformer_2_contents)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;
    conformer_1.extend(conformer_2);

    serde_json::to_string(&conformer_1).map_err(|e| PyRuntimeError::new_err(e.to_string()))
}

/// Drops amino acids from a conformer json string
#[pyfunction]
pub fn drop_amino_acids(
    conformer_contents: String,
    amino_acids_to_drop: Vec<usize>,
) -> PyResult<String> {
    let mut conformer: Conformer = serde_json::from_str(&conformer_contents)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    conformer.drop_amino_acids(&amino_acids_to_drop);

    serde_json::to_string(&conformer).map_err(|e| PyRuntimeError::new_err(e.to_string()))
}

/// Drops residues from a conformer json string
#[pyfunction]
pub fn drop_residues(conformer_contents: String, residues_to_drop: Vec<usize>) -> PyResult<String> {
    let mut conformer: Conformer = serde_json::from_str(&conformer_contents)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    conformer.drop_residues(&residues_to_drop);

    serde_json::to_string(&conformer).map_err(|e| PyRuntimeError::new_err(e.to_string()))
}

/// Charges standard amino acids given a conformer json string,
#[pyfunction]
pub fn formal_charge(
    conformer_contents: String,
    missing_atom_strictness: String,
) -> PyResult<String> {
    let mut conformer: Conformer = serde_json::from_str(&conformer_contents)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    let strictness: AtomCheckStrictness =
        serde_json::from_str(&format!("\"{missing_atom_strictness}\""))
            .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    conformer
        .perceive_bonds(strictness)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    conformer
        .perceive_formal_charges()
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    conformer.topology.assign_fragment_charges();

    serde_json::to_string(&conformer).map_err(|e| PyRuntimeError::new_err(e.to_string()))
}

/// Fragments a conformer, updating the fragment formal charges based on existing atom charges
#[pyfunction]
pub fn fragment(
    conformer_contents: String,
    missing_atom_strictness: String,
    backbone_steps: usize,
    terminal_fragment_sidechain_size: Option<usize>,
) -> PyResult<String> {
    let mut conformer: Conformer = serde_json::from_str(&conformer_contents)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    let strictness: AtomCheckStrictness =
        serde_json::from_str(&format!("\"{missing_atom_strictness}\""))
            .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    conformer
        .perceive_bonds(strictness)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    conformer.topology.fragments =
        Some(conformer.fragment(backbone_steps, terminal_fragment_sidechain_size));

    conformer.topology.assign_fragment_charges();

    serde_json::to_string(&conformer).map_err(|e| PyRuntimeError::new_err(e.to_string()))
}

/// Fragments a conformer by atom labels, updating the fragment formal charges based on existing atom charges
#[pyfunction]
pub fn fragment_by_label(
    conformer_contents: String,
    missing_atom_strictness: String,
) -> PyResult<String> {
    let mut conformer: Conformer = serde_json::from_str(&conformer_contents)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    let strictness: AtomCheckStrictness =
        serde_json::from_str(&format!("\"{missing_atom_strictness}\""))
            .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    conformer
        .perceive_bonds(strictness)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    conformer
        .perceive_formal_charges()
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    conformer
        .fragment_by_label()
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;
    conformer.topology.assign_fragment_charges();

    assert!(conformer.is_valid());

    serde_json::to_string(&conformer).map_err(|e| PyRuntimeError::new_err(e.to_string()))
}

/// Fragments a conformer, using distance based bond inference instead of pattern based bond inference
#[pyfunction]
pub fn fragment_legacy(
    conformer_contents: String,
    bond_length_tolerance: f32,
    backbone_steps: usize,
    terminal_fragment_sidechain_size: Option<usize>,
) -> PyResult<String> {
    let mut conformer: Conformer = serde_json::from_str(&conformer_contents)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    conformer.topology.connectivity = Some(
        conformer
            .topology
            .implicit_connectivity(bond_length_tolerance),
    );

    conformer.topology.fragments =
        Some(conformer.fragment(backbone_steps, terminal_fragment_sidechain_size));

    conformer.topology.fragment_charges = conformer.topology.explicit_fragment_charges();

    serde_json::to_string(&conformer).map_err(|e| PyRuntimeError::new_err(e.to_string()))
}

#[pyfunction]
pub fn find_amino_acid(
    conformer: String,
    amino_acid_seq_id: i32,
    amino_acid_insertion_code: Option<String>,
) -> PyResult<String> {
    let mut conformer: Conformer = serde_json::from_str(&conformer)
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    conformer.find_amino_acid(amino_acid_seq_id, amino_acid_insertion_code.as_deref())
             .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

    serde_json::to_string(&conformer).map_err(|e| PyRuntimeError::new_err(e.to_string()))
}
