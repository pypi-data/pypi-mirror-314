// src/lib.rs
// A crate for extracting contents from a text file containing a story collection and creating a table of contents and individual story files.
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use std::path::Path;

mod output_dir;
use output_dir::create_folder_in_output_dir;

mod content;
use content::{create_table_of_contents, create_story_files};

#[pyfunction]
fn process_file(input_file: &str) -> PyResult<()> {
    // Call the internal implementation function
    process_file_impl(Path::new(input_file)).map_err(|e| {
        pyo3::exceptions::PyIOError::new_err(format!("Error processing file: {}", e))
    })
}

fn process_file_impl(input_file: &Path) -> Result<(), Box<dyn std::error::Error>> {
    let path = create_folder_in_output_dir(input_file)?;
    let stories = extract_contents(input_file)?;
    create_table_of_contents(path.clone(), stories.clone())?;
    create_story_files(path, stories, input_file)?;
    Ok(())
}

fn extract_contents(file_path: &Path) -> std::io::Result<Vec<String>> {
    use std::fs::File;
    use std::io::{self, BufRead};
    let file = File::open(file_path)?;
    let reader = io::BufReader::new(file);
    let mut titles = Vec::new();
    let mut in_contents = false;

    for line in reader.lines() {
        let line = line?;
        if line.trim() == "Contents" {
            in_contents = true;
            continue;
        }
        if in_contents {
            if line.trim().is_empty() {
                continue;
            }
            if titles.contains(&line.trim().to_string()) {
                break;
            }
            titles.push(line.trim().to_string());
        }
    }

    Ok(titles)
}

#[pymodule]
fn shrive(_py: Python, m: &PyModule) -> PyResult<()> {
    // Register the `process_file` function with the Python module
    m.add_function(wrap_pyfunction!(process_file, m)?)?;
    Ok(())
}
