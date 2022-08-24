
# dsort TODOs

- [ ] Support JSON input
    Read input and parse json or yaml... investigate how
    kubectl seemlessly handles both:
        k create -f - < tests/2/in.yaml
        k create -f - < tests/2/in.json


- [ ] Improve sort functions (key sort and list sort)
    Improved, but still got room for further improvement

- [ ] Make sort order configurable via config file (e.g. TOML file)

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

- [ ] Add CI/CD

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
