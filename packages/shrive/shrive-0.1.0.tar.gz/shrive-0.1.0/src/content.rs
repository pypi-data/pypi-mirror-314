// src/content.rs
// The module "content" contains the functions that create the table of contents and individual story files.
use std::fs;
use std::io::{self, BufRead, Write};
use std::path::{Path, PathBuf};

/// The function `create_table_of_contents` in Rust creates a table of contents markdown file for a
/// given folder path and list of stories.
/// 
/// Arguments:
/// 
/// * `path`: The `path` parameter is a `PathBuf` type, which represents a path to a file or directory
/// in the file system. In this function, it is used to specify the location where the table of contents
/// file will be created and to derive the folder name from it.
/// * `stories`: A vector of strings representing the titles of stories or chapters that you want to
/// include in the table of contents.
/// 
/// Returns:
/// 
/// The function `create_table_of_contents` returns a result of type `io::Result<()>`.
pub fn create_table_of_contents(path: PathBuf, stories: Vec<String>) -> io::Result<()> {
    let folder_name = path.file_name()
        .ok_or_else(|| io::Error::new(io::ErrorKind::InvalidInput, "Invalid folder name"))?
        .to_str().ok_or_else(|| io::Error::new(io::ErrorKind::InvalidInput, "Invalid folder name"))?;
    println!("Folder name: {}", folder_name);

    let toc_path = path.join("table_of_contents.md");
    println!("Table of Contents path: {:?}", toc_path);

    let mut toc_file = fs::File::create(&toc_path)?;
    println!("Table of Contents file created successfully");

    writeln!(toc_file, "# {}\n", folder_name)?;
    writeln!(toc_file, "")?;
    for story in stories {
        writeln!(toc_file, "> - {}", story)?;
    }
    writeln!(toc_file, "")?;
    println!("Table of Contents written successfully");

    Ok(())
}

/// The `create_story_files` function in Rust reads a file, extracts specific story sections based on
/// titles, and creates separate Markdown files for each extracted story.
/// 
/// Arguments:
/// 
/// * `path`: The `path` parameter in the `create_story_files` function represents the directory where
/// the story files will be created. It is of type `PathBuf`, which is a buffer type for working with
/// file paths. This parameter specifies the location where the new story files will be saved.
/// * `titles`: The `titles` parameter in the `create_story_files` function is a vector of strings that
/// contains the titles of the stories you want to extract from the content read from a file. Each title
/// in the `titles` vector is used to identify the beginning of a story in the content and to create
/// * `file_path`: The `file_path` parameter in the `create_story_files` function is a reference to a
/// `Path` that specifies the location of the file to be opened and read for content. This path is used
/// to open a file, read its contents, and then process the content based on the provided `
/// 
/// Returns:
/// 
/// The function `create_story_files` returns a result of type `io::Result<()>`.
pub fn create_story_files(path: PathBuf, titles: Vec<String>, file_path: &Path) -> io::Result<()> {
    let file = fs::File::open(file_path)?;
    let reader = io::BufReader::new(file);
    let content: Vec<String> = reader.lines().collect::<Result<_, _>>()?;

    for title in &titles {
        let mut occurrences = 0;
        let mut story_text = String::new();
        let mut in_story = false;
        let mut last_line_blank = false;

        for line in &content {
            if line.trim() == title {
                occurrences += 1;
                if occurrences == 2 {
                    in_story = true;
                    continue;
                }
            }

            if in_story {
                if titles.contains(&line.trim().to_string()) {
                    break;
                }
                if line.trim().is_empty() {
                    if !last_line_blank {
                        story_text.push_str(line);
                        story_text.push('\n');
                        last_line_blank = true;
                    }
                } else {
                    story_text.push_str(line);
                    story_text.push('\n');
                    last_line_blank = false;
                }
            }
        }

        if in_story {
            let file_name = format!("{}.md", title.replace(" ", "_").to_lowercase());
            let file_path = path.join(file_name);
            let mut file = fs::File::create(file_path)?;
            writeln!(file, "# {}\n", title)?;
            file.write_all(story_text.as_bytes())?;
        }
    }

    Ok(())
}
