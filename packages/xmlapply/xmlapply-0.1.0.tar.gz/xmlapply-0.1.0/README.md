# xmlapply

**xmlapply** is a command-line tool for applying file changes defined in an XML specification to a target project directory. 


Changes can include creating, updating, or deleting files. 

credit idea: https://github.com/mckaywrigley/o1-xml-parser


## workflow

### prereqs

- install `code2prompt`
  - cargo install code2prompt

### setup


`git clone https://github.com/darinkishore/xmlapply.git`

`cd xmlapply`

`mkdir -p ~/templates` (or wherever you wanna put your templates)

`cp o1.hbs ~/templates/`

### Workflow

Okay, so you're working on a project. 

Want to use o1 to help.

go to project directory, run

`xmlapply use-dir` to indicate that you're working on the project in that directory now.

for whatever directory you want to include in your query as context, (inlcuding the root `.`)

`code2prompt --template ~/templates/o1.hbs $dir`

Give that to o1, wait however long it takes, copy that to your clipboard, then run `xmlapply apply`. 


## Table of Contents

- [xmlapply](#xmlapply)
  - [workflow](#workflow)
    - [prereqs](#prereqs)
    - [setup](#setup)
    - [Workflow](#workflow-1)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [How It Works](#how-it-works)
  - [Installation](#installation)
- [Apply changes from a file](#apply-changes-from-a-file)
- [Apply changes from clipboard content (if you have copied XML)](#apply-changes-from-clipboard-content-if-you-have-copied-xml)
- [Copy XML content to clipboard, then:](#copy-xml-content-to-clipboard-then)

## Features

- **XML-Defined Changes:** Define file operations in an XML file. Operations supported:
  - **CREATE**: Create new files and write provided content.
  - **UPDATE**: Overwrite existing files with new content.
  - **DELETE**: Remove specified files.
- **Clipboard Support:** If an XML file is not provided, **xmlapply** can read the XML content directly from your clipboard.
- **Configurable Default Directory:** Set a global default directory to avoid specifying the target directory each time.
- **Dry-Run Mode:** Preview changes without actually modifying any files.

## How It Works

1. **Parse XML:** **xmlapply** reads an XML file (or clipboard content) to determine which files to create, update, or delete.
2. **Apply Changes:** It then executes the requested operations against a target directory, ensuring that no changes are made outside of the intended project directory.
3. **Configuration Management:** A simple YAML config file in your home directory (`~/.xmlapply.yml`) stores your default project directory.

## Installation

**Prerequisites:**  
- Python 3.8+  
- [pip](https://pip.pypa.io/en/stable/installing/)

**Install from Source:**

```bash
git clone https://github.com/yourusername/xmlapply.git
cd xmlapply
pip install .

This will install xmlapply as a CLI command on your system (assuming ~/.local/bin or equivalent is on your PATH).

Usage

Basic Command Structure:

xmlapply [COMMAND] [OPTIONS]

Applying Changes

Use the apply command to apply changes defined in an XML file or from the clipboard:

# Apply changes from a file
xmlapply apply --file /path/to/changes.xml --directory /path/to/project

# Apply changes from clipboard content (if you have copied XML)
xmlapply apply

If no --directory is provided, xmlapply will use the configured default directory. If no --file is provided, xmlapply will attempt to read XML from the clipboard.

Changing the Default Directory

To set or update the default directory:

xmlapply set_dir /path/to/my/project

Once set, you can omit the --directory option when running apply.

Viewing Configuration

To view the current configuration:

xmlapply show_config

Dry Runs

Use --dry-run to preview changes without making them:

xmlapply apply --file changes.xml --dry-run

This will show you which operations would have been performed.

XML Format

The tool expects an XML structure like:

<root>
  <changed_files>
    <file>
      <file_summary>Initial creation of README</file_summary>
      <file_operation>CREATE</file_operation>
      <file_path>docs/README.md</file_path>
      <file_code>This is the README content</file_code>
    </file>
    <file>
      <file_summary>Remove obsolete config</file_summary>
      <file_operation>DELETE</file_operation>
      <file_path>config/old_config.yml</file_path>
    </file>
  </changed_files>
</root>

Required Fields:
	•	<file_operation>: CREATE, UPDATE, or DELETE
	•	<file_path>: Relative path within the project directory

Optional Fields:
	•	<file_summary>: A short description of the change.
	•	<file_code>: The content to write when creating or updating a file.

Configuration

xmlapply stores configuration in a YAML file located at ~/.xmlapply.yml. The primary configuration value is default_directory.

Example ~/.xmlapply.yml:

default_directory: /Users/username/Projects/mydefaultproject

You typically won’t need to edit this file directly; use the set_dir command instead.

Examples

1. Apply from a file directly:

xmlapply apply --file test.xml --directory /Users/darin/Projects/myproject

2. Apply changes from clipboard to the default directory:

# Copy XML content to clipboard, then:
xmlapply apply

3. Preview what would happen (no actual changes):

xmlapply apply --file edge_cases.xml --dry-run

Development

This repository includes:
	•	CLI Tool: src/xmlapply/cli.py
	•	Parser: src/xmlapply/parser.py for parsing XML structures into Python data classes.
	•	Applier: src/xmlapply/apply.py for applying changes to the filesystem.
	•	Configuration: src/xmlapply/config.py for reading and writing default directory settings.
	•	Core Module Init: src/xmlapply/__init__.py defines the package interface.
	•	Examples & Tests: test.xml and edge_cases.xml provide sample XML inputs.

For development, ensure you have requirements.txt dependencies installed:

pip install -r requirements.txt

You can run the hello.py script to confirm the environment is set up:

python hello.py

Expected output:

Hello from xmlapply!

License

This project is distributed under the terms of the MIT license. See LICENSE for details.

