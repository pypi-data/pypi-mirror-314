# fetch-latest-file

## installing

```bash
pipx install fetch-latest-file
fetch completion -x
```

## configuration

```bash

mkdir -p ~/.fetch_latest_file.d

echo <EOF
[source1]
host = <hostname>
destination = output_filepath
match = regex expression
path = search path on host

[source1]
host = <hostname>
destination = output_filepath
match = regex expression
path = search path on host

EOF > ~/.fetch_latest_file.d/config1
```
