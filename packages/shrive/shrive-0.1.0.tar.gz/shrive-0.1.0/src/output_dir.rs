// src/output_dir.rs
// The module "output_dir" contains the function that creates a folder in the output directory based on the input file name.
use std::fs;
use std::io;
use std::path::{Path, PathBuf};

/// The function `create_folder_in_output_dir` takes an input file path, extracts the base name,
/// converts it to a folder name format, creates a folder in the output directory with that name, and
/// returns the path to the created folder.
/// 
/// Arguments:
/// 
/// * `input_file`: The function `create_folder_in_output_dir` takes a reference to a `Path` as input,
/// which represents the path to a file. The function then extracts the file name from the input path,
/// processes it to create a folder name, creates a new directory in the "src/output" directory with
/// 
/// Returns:
/// 
/// The function `create_folder_in_output_dir` returns a `Result` containing a `PathBuf`. The `PathBuf`
/// represents the path to the newly created folder in the output directory.
pub fn create_folder_in_output_dir(input_file: &Path) -> io::Result<PathBuf> {
    let input_file_str = input_file.to_str().ok_or_else(|| io::Error::new(io::ErrorKind::InvalidInput, "Invalid file path"))?;
    println!("Selected file: {}", input_file_str);

    let file_name = input_file.file_name().ok_or_else(|| io::Error::new(io::ErrorKind::InvalidInput, "Invalid file name"))?
        .to_str().ok_or_else(|| io::Error::new(io::ErrorKind::InvalidInput, "Invalid file name"))?;
    println!("File name: {}", file_name);

    let base_name = file_name.trim_end_matches(".txt");
    println!("Base name: {}", base_name);

    let folder_name = base_name
        .replace("_", " ")
        .split_whitespace()
        .map(|word| {
            let mut c = word.chars();
            match c.next() {
                None => String::new(),
                Some(f) => f.to_uppercase().collect::<String>() + c.as_str(),
            }
        })
        .collect::<Vec<String>>()
        .join(" ");
    println!("Folder name: {}", folder_name);

    let output_dir = Path::new("src/output").join(folder_name);
    println!("Output directory: {:?}", output_dir);

    fs::create_dir_all(&output_dir)?;
    println!("Folder created successfully");

    Ok(output_dir)
}
