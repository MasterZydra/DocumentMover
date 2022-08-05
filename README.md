# Document Mover
DocumentMover is a command line tool that automatically moves files in directories. Rules determine where the files get moved.

This command line tool is supposed to replace the [DocumentDropper](https://github.com/MasterZydra/DocumentDropper). The DocumentDropper is a tool written in Delphi and can not run on Linux. So this tool is written in Python3 with the advantage that Python is available on every mayor OS.

## Usage
`DocumentMover.py [-h] [-p PATH]`

Options:  
`-h`, `--help` show this help message and exit  
`-p` path to the folder with config file

**Examples:**  
`> python3 DocumentMover.py --help`

`> python3 DocumentMover.py -p /home/MasterZydra/Documents/Archive`

## Configuration
The configuration is done in `.documentMover` files.

**Example file `.documentMover`**
```TOML
[Source.source_name]
Path=/my/path/to/src
Recursively=yes # Optional - Default value is 'no'

[Destination.dest_name]
Path=/my/path/to/dest

[Rule.rule_name]
Selector=file_starts_with # Regex
Destination=dest_name # Must match with a existing destination
Subfolder=subfolder/in/destination/folder # Optional - Default value is ''
```