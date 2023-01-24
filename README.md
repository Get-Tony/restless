
# Restless

An process management tool.

- [Restless](#restless)
  - [License](#license)
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [For development](#for-development)
    - [For production](#for-production)
  - [Sources](#sources)
    - [demo\_data/roles/common](#demo_datarolescommon)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Requirements

- Python 3.10.0 (or higher)
- Ansible 7.1.0 (or higher)
- lib_standard 1.1.5 (or higher) - see [github.com/get-tony/lib_standard](https://github.com/get-tony/lib_standard)

## Installation

### For development

From the root directory of the package (where the README file is found), run:
> ```pip install -r requirements/dev.txt```

### For production

> ```pip install -r requirements/prod.txt```

## Sources

### demo_data/roles/common

The `common` role was generated with `ansible-galaxy init common` from within the roles directory.
`ansible-galaxy` comes packaged with Ansible.
