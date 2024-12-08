use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use pyo3::types::{PyDict, PyList};
use pyo3::{PyResult, create_exception};

use serde_json::{Map, Value};

use jsonwebtoken::{ Algorithm};

use uuid::Uuid;

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
        // Ensure the key is a string
        let key = key
            .extract::<String>()
            .map_err(|_| PyValueError::new_err("Claim key must be a string"))?;

        if let Ok(int_value) = value.extract::<i64>() {
            // Handle integer values
            dict_map.insert(key, Value::Number(int_value.into()));
        } else if let Ok(bool_value) = value.extract::<bool>() {
            // Handle boolean values
            dict_map.insert(key, Value::Bool(bool_value));
        } else if let Ok(uuid_str) = value.extract::<String>() {
            // Handle UUIDs from strings
            if let Ok(uuid_value) = Uuid::parse_str(&uuid_str) {
                dict_map.insert(key, Value::String(uuid_value.to_string()));
            } else {
                return Err(PyValueError::new_err(format!("Invalid UUID for key '{}'", key)));
            }
        } else if let Ok(list_value) = value.downcast::<PyList>() {
            // Handle list/array values
            let array: Vec<Value> = list_value
                .iter()
                .map(|item| convert_py_to_json(&item))
                .collect::<Result<_, _>>()?;
            dict_map.insert(key, Value::Array(array));
        } else if let Ok(string_value) = value.extract::<String>() {
            // Handle string values
            dict_map.insert(key, Value::String(string_value));
        } else {
            // Serialize other types as strings
            let json_value = serde_json::to_value(value.to_string())
                .map_err(|_| PyValueError::new_err("Failed to serialize claim value"))?;
            dict_map.insert(key, json_value);
        }
    }

    Ok(dict_map)
}

pub fn convert_py_to_json(value: &Bound<'_, PyAny>) -> PyResult<Value> {
    if let Ok(int_value) = value.extract::<i64>() {
        Ok(Value::Number(int_value.into()))
    } else if let Ok(bool_value) = value.extract::<bool>() {
        Ok(Value::Bool(bool_value))
    } else if let Ok(uuid_str) = value.extract::<String>() {
        if let Ok(uuid_value) = Uuid::parse_str(&uuid_str) {
            Ok(Value::String(uuid_value.to_string()))
        } else {
            Err(PyValueError::new_err("Invalid UUID in list"))
        }
    } else if let Ok(string_value) = value.extract::<String>() {
        Ok(Value::String(string_value))
    } else if let Ok(py_list) = value.downcast::<PyList>() {
        let array: Vec<Value> = py_list
            .iter()
            .map(|item| convert_py_to_json(&item))
            .collect::<Result<_, _>>()?;
        Ok(Value::Array(array))
    } else {
        Ok(Value::String(value.to_string()))
    }
}