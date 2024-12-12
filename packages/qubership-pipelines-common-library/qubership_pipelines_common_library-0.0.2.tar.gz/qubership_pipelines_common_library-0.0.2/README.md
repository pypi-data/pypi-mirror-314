# Qubership Pipelines Common Library

Common open-source python library of clients used by Qubership pipelines/modules

## Structure

Library is presented as a set of [clients](docs/Clients.md), as well as a standalone CLI tool with predefined operations (e.g. `qubership-pipelines-common-library get_file`)


## Installation

* Add the following section to your dependencies to add Qubership library as a dependency in your project:
  ```toml
  [tool.poetry.dependencies]
  qubership-pipelines-common-library = "*"
  ```

* Or you can install it via `pip`:
  ```bash
  pip install qubership-pipelines-common-library
  ```
  
  After installing, it will be available as a standalone CLI tool in your env:
  ```bash
  qubership-pipelines-common-library --help
  ```