
# dsort TODOs

- [ ] Make sort order configurable via config file (e.g. TOML file)

- [ ] Support JSON input

    Support JSON input via -f bla.json (JSON format implied from extension)
    or read, then try parsing as json, or yaml

    Read input and parse json or yaml... investigate how
    kubectl seemlessly handles both:
        k create -f - < tests/2/in.yaml
        k create -f - < tests/2/in.json

- [ ] Improve sort functions (key sort and list sort)
    Improved, but still got room for further improvement

- [ ] Make list sorting context aware

    - Define what lists should be sorted based on more than just parent key

- [ ] Improve YAML output handling of multi line strings

    ```
        - 'echo "bob"

      '
    ```
    vs
    ```
        - |
          echo "bob"
    ```

- [ ] Add githooks to run tests on commit or push

- [ ] Add CI/CD
    Github Actions?

- [ ] Push package

- [x] Rewrite to remove global vars
- [x] Add tests
- [x] Make sort order configurable via CLI parameters
    Added -s, --sort-order=name,namespace,image 
    Added -l, --sort-lists=containers,env
    Added -L, --sort-all-lists

- [x] Make cli parameters more consistent with other tooling
    Kinda.  Feel free to comment on the parameter names

- [x] Support JSON output
    (Python dicts maintain insert order, export to YAML/JSON should be trivial)
