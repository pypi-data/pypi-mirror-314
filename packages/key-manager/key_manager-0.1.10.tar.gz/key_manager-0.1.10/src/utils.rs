use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use pyo3::types::{PyDict, PyList};
use pyo3::{PyResult, create_exception};

use serde_json::{Map, Value};

use jsonwebtoken::{ Algorithm};


create_exception!(utils, UnsupportedAlgorithm, PyValueError);

pub fn parse_algorithm(alg: &str) -> PyResult<Algorithm> {
    match alg {
        "RS256" => Ok(Algorithm::RS256),
        "RS384" => Ok(Algorithm::RS384),
        "RS512" => Ok(Algorithm::RS512),
        "HS256" => Ok(Algorithm::HS256),
        "HS384" => Ok(Algorithm::HS384),
        "HS512" => Ok(Algorithm::HS512),
        "ES256" => Ok(Algorithm::ES256),
        "ES384" => Ok(Algorithm::ES384),
        "PS256" => Ok(Algorithm::PS256),
        "PS384" => Ok(Algorithm::PS384),
        "PS512" => Ok(Algorithm::PS512),
        "EdDSA" => Ok(Algorithm::EdDSA),
        _ => Err(PyErr::new::<UnsupportedAlgorithm, _>(format!(
            "Unsupported algorithm: {}",
            alg
        )))
    }
}

/// Converts Python python dict to a JSON map
pub fn convert_dict_to_map(dict:&Bound<'_, PyDict>) -> PyResult<Map<String, Value>> {
    let mut dict_map = Map::new();

    for (key, value) in dict {
        let key = key
            .extract::<String>()
            .map_err(|_| PyValueError::new_err("Claim key must be a string"))?;

        if let Ok(int_value) = value.extract::<i64>() {
            // Handle integer values
            dict_map.insert(key, Value::Number(int_value.into()));
        } else if let Ok(bool_value) = value.extract::<bool>() {
            // Handle boolean values
            dict_map.insert(key, Value::Bool(bool_value));
        } else if let Ok(list_value) = value.downcast::<PyList>() {
            // Handle list/array values
            let array: Vec<Value> = list_value
                .iter()
                .filter_map(|item| serde_json::to_value(item.extract::<String>().ok()).ok())
                .collect();
            dict_map.insert(key, Value::Array(array));
        } else {
            // Serialize other types as strings
            let value = serde_json::to_value(value.to_string())
                .map_err(|_| PyValueError::new_err("Failed to serialize claim value"))?;
            dict_map.insert(key, value);
        }
    }

    Ok(dict_map)
}




pub fn process_json_value(value: &serde_json::Value, py: Python) -> PyResult<PyObject> {
    match value {
        Value::String(s) => Ok(s.to_object(py)),
        Value::Number(num) => {
            if let Some(i) = num.as_i64() {
                Ok(i.to_object(py))
            } else if let Some(f) = num.as_f64() {
                Ok(f.to_object(py))
            } else {
                Err(PyValueError::new_err("Invalid number format"))
            }
        }
        Value::Bool(b) => Ok(b.to_object(py)),
        Value::Null => Ok(py.None()),
        Value::Array(arr) => {
            let py_list = PyList::empty(py);
            for item in arr {
                let py_item = process_json_value(item, py)?;
                py_list.append(py_item)?;
            }
            Ok(py_list.to_object(py))
        }
        Value::Object(obj) => {
            let py_dict = PyDict::new(py);
            for (key, val) in obj {
                let py_value = process_json_value(val, py)?;
                py_dict.set_item(key, py_value)?;
            }
            Ok(py_dict.to_object(py))
        }
    }
}