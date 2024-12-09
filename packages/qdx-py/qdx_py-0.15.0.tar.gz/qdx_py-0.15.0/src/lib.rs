mod qdx;

use pyo3::prelude::*;

/// QDX-Common utilities for python
#[pymodule]
mod qdx_py {
    #[pymodule_export]
    use crate::qdx::{
        concat, conformer_to_pdb, conformer_to_sdf, drop_amino_acids, drop_residues, find_amino_acid,
        formal_charge, fragment, fragment_by_label, fragment_legacy, pdb_to_conformer, sdf_to_conformer, pdb_to_trc
    };

    use super::*;

    #[pymodule_init]
    fn init(m: &Bound<'_, PyModule>) -> PyResult<()> {
        m.add("__version__", env!("CARGO_PKG_VERSION"))?;
        Ok(())
    }
}
