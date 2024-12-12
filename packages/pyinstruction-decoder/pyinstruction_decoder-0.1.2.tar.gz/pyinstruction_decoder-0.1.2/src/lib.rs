use std::{collections::HashSet, env, path::PathBuf, vec};

use instruction_decoder::Decoder;
use pyo3::{exceptions::PyValueError, prelude::*};
use regex::Regex;

#[macro_use]
extern crate load_file;

/// A Python module implemented in Rust.
#[pymodule(name = "_pyinstruction_decoder")]
fn pyinstruction_decoder(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyDecoder>()?;
    m.add_function(wrap_pyfunction!(get_riscvdecoder, m)?)?;
    Ok(())
}

#[pyclass]
struct PyDecoder(Decoder);

#[pymethods]
impl PyDecoder {
    #[new]
    fn py_new(instruction_set_tomls: Vec<String>) -> PyResult<Self> {
        match Decoder::new(&instruction_set_tomls) {
            Ok(d) => Ok(Self(d)),
            Err(errs) => Err(PyValueError::new_err(errs)),
        }
    }

    fn decode_from_string(&self, instruction: String, bit_width: usize) -> PyResult<String> {
        match self.0.decode_from_string(instruction.as_str(), bit_width) {
            Ok(s) => Ok(s),
            Err(s) => Err(PyValueError::new_err(s)),
        }
    }

    fn decode(&self, instruction: u128, bit_width: usize) -> PyResult<String> {
        match self.0.decode(instruction, bit_width) {
            Ok(s) => Ok(s),
            Err(s) => Err(PyValueError::new_err(s)),
        }
    }

    fn decode_from_bytes(&self, instruction: Vec<u8>, bit_width: usize) -> PyResult<String> {
        match self.0.decode_from_bytes(instruction, bit_width) {
            Ok(s) => Ok(s),
            Err(s) => Err(PyValueError::new_err(s)),
        }
    }
}

#[pyfunction]
#[pyo3(signature = (isa_str="RV32I".to_string()))]
fn get_riscvdecoder(isa_str: String) -> PyResult<PyDecoder> {
    let tomlfolder = match env::var("PYINSTRUCTION_DECODER_TOMLPATH") {
        Ok(value) => value,
        Err(_) => return Err(PyValueError::new_err("environment variable PYINSTRUCTION_DECODER_TOMLPATH not set, most likely python could not run sysconfig.get_config_var(\"userbase\") correctly")),
    };

    let (legacy, suffix) = if let Some(isa_short) = isa_str.strip_prefix("RV32") {
        (true, isa_short)
    } else if let Some(isa_short) = isa_str.strip_prefix("RV64") {
        (false, isa_short)
    } else {
        return Err(PyValueError::new_err(format!(
            "isa_str '{}' does not start with RV32 or RV64",
            isa_str
        )));
    };
    let tomls = if suffix == "All" {
        if legacy {
            vec![
                load_str!(format!("{}/RV32I.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV32M.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV32A.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV32C.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV32F.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RVV.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV32_Zicsr.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zifencei.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zvbb.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zvbc.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zvkg.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zvkned.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zvknha.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zvknhb.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zvksed.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zvksh.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zba.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV32_Zbb.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zbc.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV32_Zbs.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zihintntl.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zimop.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zicond.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zawrs.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV32_Zacas.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zfh.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV32_Zfa.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV32_Zbkb.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zbkc.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zbkx.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV32_Zkne.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV32_Zknd.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zknh.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zksed.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zksh.toml", tomlfolder).as_str()).to_string(),
            ]
        } else {
            vec![
                load_str!(format!("{}/RV64I.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV64M.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV64A.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV64C.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV64D.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RVV.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV32_Zicsr.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zifencei.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zvbb.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zvbc.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zvkg.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zvkned.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zvknha.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zvknhb.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zvksed.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zvksh.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zba.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV64_Zbb.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zbc.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV64_Zbs.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zihintntl.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zimop.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zicond.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zawrs.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV64_Zacas.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zfh.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV64_Zfa.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV64_Zbkb.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zbkc.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zbkx.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV64_Zkne.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV64_Zknd.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zknh.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zksed.toml", tomlfolder).as_str()).to_string(),
                load_str!(format!("{}/RV_Zksh.toml", tomlfolder).as_str()).to_string(),
            ]
        }
    } else {
        let extensions = Regex::new(r"[A-Z][a-z]*").unwrap();
        let mut errors = vec![];
        let potential_tomls = extensions
            .find_iter(suffix)
            .filter_map(|extension| match extension.as_str() {
                "I" => {
                    if legacy {
                        Some(vec![load_str!(
                            format!("{}/RV32I.toml", tomlfolder).as_str()
                        )])
                    } else {
                        Some(vec![load_str!(
                            format!("{}/RV64I.toml", tomlfolder).as_str()
                        )])
                    }
                }
                "M" => {
                    if legacy {
                        Some(vec![load_str!(
                            format!("{}/RV32M.toml", tomlfolder).as_str()
                        )])
                    } else {
                        Some(vec![load_str!(
                            format!("{}/RV64M.toml", tomlfolder).as_str()
                        )])
                    }
                }
                "A" => {
                    if legacy {
                        Some(vec![load_str!(
                            format!("{}/RV32A.toml", tomlfolder).as_str()
                        )])
                    } else {
                        Some(vec![load_str!(
                            format!("{}/RV64A.toml", tomlfolder).as_str()
                        )])
                    }
                }
                "C" => {
                    if legacy {
                        Some(vec![load_str!(
                            format!("{}/RV32C.toml", tomlfolder).as_str()
                        )])
                    } else {
                        Some(vec![load_str!(
                            format!("{}/RV64C.toml", tomlfolder).as_str()
                        )])
                    }
                }
                "F" => {
                    if legacy {
                        Some(vec![
                            load_str!(format!("{}/RV32_Zicsr.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV32F.toml", tomlfolder).as_str()),
                        ])
                    } else {
                        errors.push("RV64F does not exist, try RV64D or RV32F instead".to_string());
                        None
                    }
                }
                "D" => {
                    if legacy {
                        errors.push("RV32D does not exist, try RV64D or RV32F instead".to_string());
                        None
                    } else {
                        Some(vec![
                            load_str!(format!("{}/RV32_Zicsr.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV64D.toml", tomlfolder).as_str()),
                        ])
                    }
                }
                "Zicsr" => Some(vec![load_str!(
                    format!("{}/RV32_Zicsr.toml", tomlfolder).as_str()
                )]),
                "Zifencei" => Some(vec![load_str!(
                    format!("{}/RV_Zifencei.toml", tomlfolder).as_str()
                )]),
                "G" => {
                    if legacy {
                        Some(vec![
                            load_str!(format!("{}/RV32I.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV32M.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV32A.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV32F.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RVV.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV32_Zicsr.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV_Zifencei.toml", tomlfolder).as_str()),
                        ])
                    } else {
                        Some(vec![
                            load_str!(format!("{}/RV64I.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV64M.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV64A.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV64D.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RVV.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV32_Zicsr.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV_Zifencei.toml", tomlfolder).as_str()),
                        ])
                    }
                }
                "V" => Some(vec![load_str!(format!("{}/RVV.toml", tomlfolder).as_str())]),
                "Zvbb" => Some(vec![load_str!(
                    format!("{}/RV_Zvbb.toml", tomlfolder).as_str()
                )]),
                "Zvbc" => Some(vec![load_str!(
                    format!("{}/RV_Zvbc.toml", tomlfolder).as_str()
                )]),
                "Zvkg" => Some(vec![load_str!(
                    format!("{}/RV_Zvkg.toml", tomlfolder).as_str()
                )]),
                "Zvkned" => Some(vec![load_str!(
                    format!("{}/RV_Zvkned.toml", tomlfolder).as_str()
                )]),
                "Zvknha" => Some(vec![load_str!(
                    format!("{}/RV_Zvknha.toml", tomlfolder).as_str()
                )]),
                "Zvknhb" => Some(vec![load_str!(
                    format!("{}/RV_Zvknhb.toml", tomlfolder).as_str()
                )]),
                "Zvksed" => Some(vec![load_str!(
                    format!("{}/RV_Zvksed.toml", tomlfolder).as_str()
                )]),
                "Zvksh" => Some(vec![load_str!(
                    format!("{}/RV_Zvksh.toml", tomlfolder).as_str()
                )]),
                "B" => {
                    if legacy {
                        Some(vec![
                            load_str!(format!("{}/RV_Zba.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV32_Zbb.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV_Zbc.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV32_Zbs.toml", tomlfolder).as_str()),
                        ])
                    } else {
                        Some(vec![
                            load_str!(format!("{}/RV_Zba.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV64_Zbb.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV_Zbc.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV64_Zbs.toml", tomlfolder).as_str()),
                        ])
                    }
                }
                "Zihintntl" => Some(vec![load_str!(
                    format!("{}/RV_Zihintntl.toml", tomlfolder).as_str()
                )]),
                "Zimop" => Some(vec![load_str!(
                    format!("{}/RV_Zimop.toml", tomlfolder).as_str()
                )]),
                "Zicond" => Some(vec![load_str!(
                    format!("{}/RV_Zicond.toml", tomlfolder).as_str()
                )]),
                "Zba" => Some(vec![load_str!(
                    format!("{}/RV_Zba.toml", tomlfolder).as_str()
                )]),
                "Zbb" => {
                    if legacy {
                        Some(vec![load_str!(
                            format!("{}/RV32_Zbb.toml", tomlfolder).as_str()
                        )])
                    } else {
                        Some(vec![load_str!(
                            format!("{}/RV64_Zbb.toml", tomlfolder).as_str()
                        )])
                    }
                }
                "Zbc" => Some(vec![load_str!(
                    format!("{}/RV_Zbc.toml", tomlfolder).as_str()
                )]),
                "Zbs" => {
                    if legacy {
                        Some(vec![load_str!(
                            format!("{}/RV32_Zbs.toml", tomlfolder).as_str()
                        )])
                    } else {
                        Some(vec![load_str!(
                            format!("{}/RV64_Zbs.toml", tomlfolder).as_str()
                        )])
                    }
                }
                "Zawrs" => Some(vec![load_str!(
                    format!("{}/RV_Zawrs.toml", tomlfolder).as_str()
                )]),
                "Zacas" => {
                    if legacy {
                        Some(vec![load_str!(
                            format!("{}/RV32_Zacas.toml", tomlfolder).as_str()
                        )])
                    } else {
                        Some(vec![load_str!(
                            format!("{}/RV64_Zacas.toml", tomlfolder).as_str()
                        )])
                    }
                }
                "Zfh" => Some(vec![load_str!(
                    format!("{}/RV_Zfh.toml", tomlfolder).as_str()
                )]),
                "Zfa" => {
                    if legacy {
                        Some(vec![load_str!(
                            format!("{}/RV32_Zfa.toml", tomlfolder).as_str()
                        )])
                    } else {
                        Some(vec![load_str!(
                            format!("{}/RV64_Zfa.toml", tomlfolder).as_str()
                        )])
                    }
                }
                "Zbkb" => {
                    if legacy {
                        Some(vec![load_str!(
                            format!("{}/RV32_Zbkb.toml", tomlfolder).as_str()
                        )])
                    } else {
                        Some(vec![load_str!(
                            format!("{}/RV64_Zbkb.toml", tomlfolder).as_str()
                        )])
                    }
                }
                "Zbkc" => Some(vec![load_str!(
                    format!("{}/RV_Zbkc.toml", tomlfolder).as_str()
                )]),
                "Zbkx" => Some(vec![load_str!(
                    format!("{}/RV_Zbkx.toml", tomlfolder).as_str()
                )]),
                "Zkne" => {
                    if legacy {
                        Some(vec![load_str!(
                            format!("{}/RV32_Zkne.toml", tomlfolder).as_str()
                        )])
                    } else {
                        Some(vec![load_str!(
                            format!("{}/RV64_Zkne.toml", tomlfolder).as_str()
                        )])
                    }
                }
                "Zknd" => {
                    if legacy {
                        Some(vec![load_str!(
                            format!("{}/RV32_Zknd.toml", tomlfolder).as_str()
                        )])
                    } else {
                        Some(vec![load_str!(
                            format!("{}/RV64_Zknd.toml", tomlfolder).as_str()
                        )])
                    }
                }
                "Zknh" => Some(vec![load_str!(
                    format!("{}/RV_Zknh.toml", tomlfolder).as_str()
                )]),
                "Zk" => {
                    if legacy {
                        Some(vec![
                            load_str!(format!("{}/RV32_Zbkb.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV_Zbkc.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV_Zbkx.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV32_Zkne.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV32_Zknd.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV_Zknh.toml", tomlfolder).as_str()),
                        ])
                    } else {
                        Some(vec![
                            load_str!(format!("{}/RV64_Zbkb.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV_Zbkc.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV_Zbkx.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV64_Zkne.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV64_Zknd.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV_Zknh.toml", tomlfolder).as_str()),
                        ])
                    }
                }
                "Zkn" => {
                    if legacy {
                        Some(vec![
                            load_str!(format!("{}/RV32_Zbkb.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV_Zbkc.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV_Zbkx.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV32_Zkne.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV32_Zknd.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV_Zknh.toml", tomlfolder).as_str()),
                        ])
                    } else {
                        Some(vec![
                            load_str!(format!("{}/RV64_Zbkb.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV_Zbkc.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV_Zbkx.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV64_Zkne.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV64_Zknd.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV_Zknh.toml", tomlfolder).as_str()),
                        ])
                    }
                }
                "Zks" => {
                    if legacy {
                        Some(vec![
                            load_str!(format!("{}/RV32_Zbkb.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV_Zbkc.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV_Zbkx.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV_Zksed.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV_Zksh.toml", tomlfolder).as_str()),
                        ])
                    } else {
                        Some(vec![
                            load_str!(format!("{}/RV64_Zbkb.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV_Zbkc.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV_Zbkx.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV_Zksed.toml", tomlfolder).as_str()),
                            load_str!(format!("{}/RV_Zksh.toml", tomlfolder).as_str()),
                        ])
                    }
                }
                "All" => {
                    errors.push(
                        "'All' suffix is not allowed in combination with any other suffixes"
                            .to_string(),
                    );
                    None
                }
                other => {
                    errors.push(format!("Extension {} not recognized in {}", other, isa_str));
                    None
                }
            })
            .flatten()
            .collect::<HashSet<_>>()
            .into_iter()
            .map(str::to_string)
            .collect::<Vec<String>>();
        if errors.is_empty() {
            if potential_tomls.is_empty() {
                return Err(PyValueError::new_err(format!(
                    "No extension found in {}",
                    isa_str
                )));
            } else {
                potential_tomls
            }
        } else {
            return Err(PyValueError::new_err(errors));
        }
    };

    PyDecoder::py_new(tomls)
}
