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

## Bring preferred keys to the top

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

## Sort configured lists by `name` attribute

`containers` and `env` lists are sorted by `name` value.

```bash
$ cat example2.yaml
```

```YAML
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: nginx
  name: nginx
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: nginx
    spec:
      containers:
      - command:
        - sh
        - -c
        - |
          echo "bob"
        env:
        - name: BOB
          value: bill
        - name: ROBERT
        - name: BOBBY
          value: bill
        image: nginx
        imagePullPolicy: Always
        name: nginx
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
      - image: ubuntu
        name: main
```

```bash
$ cat example2.yaml | python dsort.py yaml
```

```YAML
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  namespace: default
  labels:
    app: nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: nginx
    spec:
      containers:
      - name: main
        image: ubuntu
      - name: nginx
        image: nginx
        command:
        - sh
        - -c
        - 'echo "bob"

          '
        env:
        - name: BOB
          value: bill
        - name: BOBBY
          value: bill
        - name: ROBERT
        imagePullPolicy: Always
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
```
