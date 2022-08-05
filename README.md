# Document Mover

**Example**
```conf
[Source.source_name]
Path=/my/path/to/src
Recursively='yes' # Optional - Default value is 'no'

[Destination.dest_name]
Path=/my/path/to/dest

[Rule.rule_name]
Selector=file_starts_with*
Destination=dest_name
```