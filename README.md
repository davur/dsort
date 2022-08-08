# dsort - sorts YAML/JSON according to a configurable preference

Inspired by the following reddit post:
https://www.reddit.com/r/kubernetes/comments/whx38u/standards_are_there_for_a_reason_or_perhaps_i/

Programmed live on Twitch [davur_](https://www.twitch.tv/davur_).


# Prerequisites

- Python3
- docopt, PyYAML (`pip install -r requirements`)

# Usage

```
Usage:
  dsort.py <command> [-dhv] [<file>...]

Options:
  -d, --debug           Print debug information
  -h, --help            Show this screen.
  -v, --version         Show version.
```

# Features

1. Sorts YAML keys alphabetically, _except_ for keys specified in config.

	```Python
	config = ['apiVersion', 'kind', 'metadata', 'name', 'namespace', 'image']
	```
   
   These keys are brought to the top of their respective stansas.

2. Sorts _some_ list elements by their `"name"`-value (if present)

	```Python
	sort_lists = ['containers', 'env']
	```



# Example

```bash
$ cat example.yaml
```

```YAML
kind: ConfigMap
apiVersion: v1
data:
  default.yaml: |-
    a: yabba
    b: dabba
metadata:
  labels:
    env: qa
    owner: me
  name: config-file
  namespace: cloudflared
```

```bash
$ cat example.yaml | python dsort.py yaml
```

```YAML
apiVersion: v1
kind: ConfigMap
metadata:
  name: config-file
  namespace: cloudflared
  labels:
    env: qa
    owner: me
data:
  default.yaml: 'a: yabba

    b: dabba'
```
