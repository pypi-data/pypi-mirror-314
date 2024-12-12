#![allow(clippy::unused_unit)]
use polars::prelude::*;
use pyo3_polars::derive::polars_expr;
use std::fs::read_to_string;

#[polars_expr(output_type=Boolean)]
fn umbrella_lokup(inputs: &[Series]) -> PolarsResult<Series> {
    let cisco_umbrella: Vec<String> = get_cisco_umbrella("top-1m.csv");

    let ca: &StringChunked = inputs[0].str()?;
    let out: BooleanChunked = ca.apply_nonnull_values_generic(
        DataType::Boolean, |x| cisco_umbrella.contains(&x.to_string())
    );
    Ok(out.into_series())
}

fn get_cisco_umbrella(filename: &str) -> Vec<String> {
    let mut result = Vec::new();

    for line in read_to_string(filename).unwrap().lines() {
        let line_string = line.to_string();

        let parts = line_string.split(",");

        let collection: Vec<&str> = parts.collect();

        result.push(collection[1].to_string());
    }

    result
}
