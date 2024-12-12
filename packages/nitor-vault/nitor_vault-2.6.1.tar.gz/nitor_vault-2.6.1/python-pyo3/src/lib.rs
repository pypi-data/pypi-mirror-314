use std::borrow::Cow;
use std::sync::LazyLock;

use pyo3::prelude::*;
use pyo3::types::{IntoPyDict, PyDict};
use tokio::runtime::Runtime;

use nitor_vault::cloudformation::CloudFormationStackData;
use nitor_vault::errors::VaultError;
use nitor_vault::VaultConfig as RustVaultConfig;
use nitor_vault::{CreateStackResult, UpdateStackResult, Value, Vault};

static RUNTIME: LazyLock<Runtime> =
    LazyLock::new(|| Runtime::new().expect("Failed to start async runtime."));

#[pyclass]
#[derive(Debug, Default, Clone)]
pub struct VaultConfig {
    #[pyo3(get, set)]
    pub vault_stack: Option<String>,
    #[pyo3(get, set)]
    pub region: Option<String>,
    #[pyo3(get, set)]
    pub bucket: Option<String>,
    #[pyo3(get, set)]
    pub key: Option<String>,
    #[pyo3(get, set)]
    pub prefix: Option<String>,
    #[pyo3(get, set)]
    pub profile: Option<String>,
    #[pyo3(get, set)]
    pub iam_id: Option<String>,
    #[pyo3(get, set)]
    pub iam_secret: Option<String>,
}

#[pymethods]
impl VaultConfig {
    #[new]
    #[must_use]
    #[pyo3(signature = (vault_stack=None, region=None, bucket=None, key=None, prefix=None, profile=None, iam_id=None, iam_secret=None))]
    pub const fn new(
        vault_stack: Option<String>,
        region: Option<String>,
        bucket: Option<String>,
        key: Option<String>,
        prefix: Option<String>,
        profile: Option<String>,
        iam_id: Option<String>,
        iam_secret: Option<String>,
    ) -> Self {
        Self {
            vault_stack,
            region,
            bucket,
            key,
            prefix,
            profile,
            iam_id,
            iam_secret,
        }
    }
}

impl From<VaultConfig> for RustVaultConfig {
    fn from(config: VaultConfig) -> Self {
        Self {
            vault_stack: config.vault_stack,
            region: config.region,
            bucket: config.bucket,
            key: config.key,
            prefix: config.prefix,
            profile: config.profile,
            iam_id: config.iam_id,
            iam_secret: config.iam_secret,
        }
    }
}

#[pyfunction()]
fn delete(name: &str, config: VaultConfig) -> PyResult<()> {
    RUNTIME.block_on(async {
        Ok(Vault::from_config(config.into())
            .await
            .map_err(vault_error_to_anyhow)?
            .delete(name)
            .await
            .map_err(vault_error_to_anyhow)?)
    })
}

#[pyfunction()]
#[allow(clippy::needless_pass_by_value)]
fn delete_many(names: Vec<String>, config: VaultConfig) -> PyResult<()> {
    RUNTIME.block_on(async {
        Ok(Vault::from_config(config.into())
            .await
            .map_err(vault_error_to_anyhow)?
            .delete_many(&names)
            .await
            .map_err(vault_error_to_anyhow)?)
    })
}

#[pyfunction()]
fn direct_decrypt(data: &[u8], config: VaultConfig) -> PyResult<Cow<[u8]>> {
    // Returns Cow<[u8]> instead of Vec since that will get mapped to bytes for the Python side
    // https://pyo3.rs/main/conversions/tables#returning-rust-values-to-python
    RUNTIME.block_on(async {
        let result = Vault::from_config(config.into())
            .await
            .map_err(vault_error_to_anyhow)?
            .direct_decrypt(data)
            .await
            .map_err(vault_error_to_anyhow)?;

        Ok(result.into())
    })
}

#[pyfunction()]
fn direct_encrypt(data: &[u8], config: VaultConfig) -> PyResult<Cow<[u8]>> {
    RUNTIME.block_on(async {
        let result = Vault::from_config(config.into())
            .await
            .map_err(vault_error_to_anyhow)?
            .direct_encrypt(data)
            .await
            .map_err(vault_error_to_anyhow)?;

        Ok(result.into())
    })
}

#[pyfunction()]
fn exists(name: &str, config: VaultConfig) -> PyResult<bool> {
    RUNTIME.block_on(async {
        let result: bool = Vault::from_config(config.into())
            .await
            .map_err(vault_error_to_anyhow)?
            .exists(name)
            .await
            .map_err(vault_error_to_anyhow)?;

        Ok(result)
    })
}

#[pyfunction()]
fn init(config: VaultConfig) -> PyResult<PyObject> {
    let result = RUNTIME.block_on(async {
        Vault::init(
            config.vault_stack,
            config.region,
            config.bucket,
            config.profile,
            config.iam_id,
            config.iam_secret,
        )
        .await
        .map_err(vault_error_to_anyhow)
    })?;
    Python::with_gil(|py| match result {
        CreateStackResult::Exists { data } => {
            let dict = stack_data_to_pydict(py, data, "EXISTS");
            Ok(dict.into())
        }
        CreateStackResult::ExistsWithFailedState { data } => {
            let dict = stack_data_to_pydict(py, data, "EXISTS_WITH_FAILED_STATE");
            Ok(dict.into())
        }
        CreateStackResult::Created {
            stack_name,
            stack_id,
            region,
        } => {
            let key_vals: Vec<(&str, PyObject)> = vec![
                ("result", "CREATED".to_string().to_object(py)),
                ("stack_name", stack_name.to_object(py)),
                ("stack_id", stack_id.to_object(py)),
                ("region", region.to_string().to_object(py)),
            ];
            let dict = key_vals.into_py_dict_bound(py);
            Ok(dict.into())
        }
    })
}

#[pyfunction()]
fn list_all(config: VaultConfig) -> PyResult<Vec<String>> {
    RUNTIME.block_on(async {
        let result = Vault::from_config(config.into())
            .await
            .map_err(vault_error_to_anyhow)?
            .all()
            .await
            .map_err(vault_error_to_anyhow)?;

        Ok(result)
    })
}

#[pyfunction()]
fn lookup(name: &str, config: VaultConfig) -> PyResult<Cow<[u8]>> {
    RUNTIME.block_on(async {
        let result: Value = Box::pin(
            Vault::from_config(config.into())
                .await
                .map_err(vault_error_to_anyhow)?
                .lookup(name),
        )
        .await
        .map_err(vault_error_to_anyhow)?;

        Ok(Cow::Owned(result.to_bytes()))
    })
}

#[pyfunction]
/// Run Vault CLI with given args.
fn run(args: Vec<String>) -> PyResult<()> {
    RUNTIME.block_on(async {
        nitor_vault::run_cli_with_args(args).await?;
        Ok(())
    })
}

#[pyfunction()]
fn stack_status(config: VaultConfig) -> PyResult<PyObject> {
    let data = RUNTIME.block_on(async {
        Vault::from_config(config.into())
            .await
            .map_err(vault_error_to_anyhow)?
            .stack_status()
            .await
            .map_err(vault_error_to_anyhow)
    })?;

    Python::with_gil(|py| {
        let dict = stack_data_to_pydict(py, data, "SUCCESS");
        Ok(dict.into())
    })
}

#[pyfunction()]
fn store(name: &str, value: &[u8], config: VaultConfig) -> PyResult<()> {
    RUNTIME.block_on(async {
        Ok(Box::pin(
            Vault::from_config(config.into())
                .await
                .map_err(vault_error_to_anyhow)?
                .store(name, value),
        )
        .await
        .map_err(vault_error_to_anyhow)?)
    })
}

#[pyfunction()]
fn update(config: VaultConfig) -> PyResult<PyObject> {
    let result = RUNTIME.block_on(async {
        Vault::from_config(config.into())
            .await
            .map_err(vault_error_to_anyhow)?
            .update_stack()
            .await
            .map_err(vault_error_to_anyhow)
    })?;

    Python::with_gil(|py| match result {
        UpdateStackResult::UpToDate { data } => {
            let dict = stack_data_to_pydict(py, data, "UP_TO_DATE");
            Ok(dict.into())
        }
        UpdateStackResult::Updated {
            stack_id,
            previous_version,
            new_version,
        } => {
            let key_vals: Vec<(&str, PyObject)> = vec![
                ("result", "UPDATED".to_string().to_object(py)),
                ("stack_id", stack_id.to_object(py)),
                ("previous_version", previous_version.to_object(py)),
                ("new_version", new_version.to_object(py)),
            ];
            let dict = key_vals.into_py_dict_bound(py);
            Ok(dict.into())
        }
    })
}

#[pymodule]
#[pyo3(name = "nitor_vault_rs")]
fn nitor_vault_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<VaultConfig>()?;
    m.add_function(wrap_pyfunction!(delete, m)?)?;
    m.add_function(wrap_pyfunction!(delete_many, m)?)?;
    m.add_function(wrap_pyfunction!(direct_decrypt, m)?)?;
    m.add_function(wrap_pyfunction!(direct_encrypt, m)?)?;
    m.add_function(wrap_pyfunction!(exists, m)?)?;
    m.add_function(wrap_pyfunction!(init, m)?)?;
    m.add_function(wrap_pyfunction!(list_all, m)?)?;
    m.add_function(wrap_pyfunction!(lookup, m)?)?;
    m.add_function(wrap_pyfunction!(run, m)?)?;
    m.add_function(wrap_pyfunction!(stack_status, m)?)?;
    m.add_function(wrap_pyfunction!(store, m)?)?;
    m.add_function(wrap_pyfunction!(update, m)?)?;
    Ok(())
}

/// Convert `VaultError` to `anyhow::Error`
fn vault_error_to_anyhow(err: VaultError) -> anyhow::Error {
    err.into()
}

/// Convert `CloudFormationStackData` to a Python dictionary.
// Lifetime annotations are required due to `&str` usage,
// could be left out if passing a `String` for the result message.
fn stack_data_to_pydict<'a>(
    py: Python<'a>,
    data: CloudFormationStackData,
    result: &'a str,
) -> Bound<'a, PyDict> {
    let key_vals: Vec<(&str, PyObject)> = vec![
        ("result", result.to_string().to_object(py)),
        ("bucket", data.bucket_name.to_object(py)),
        ("key", data.key_arn.to_object(py)),
        (
            "status",
            data.status.map(|status| status.to_string()).to_object(py),
        ),
        ("status_reason", data.status_reason.to_object(py)),
        ("version", data.version.to_object(py)),
    ];
    key_vals.into_py_dict_bound(py)
}
