# Developer Guide

All contributions to RenderCV are welcome!

The source code is thoroughly documented and well-commented, making it an enjoyable read and easy to understand. A detailed documentation of the source code is available in the [reference](../reference/index.md).


## Getting Started

There are two ways of developing RenderCV: locally or with GitHub Codespaces.

### Develop Locally

1. Ensure that you have Python version 3.10 or higher.
2. Install [Hatch](https://hatch.pypa.io/latest/), as it is the project manager for RenderCV. The installation guide for Hatch can be found [here](https://hatch.pypa.io/latest/install/#installation).
3. Clone the repository recursively (because TinyTeX is being used as a submodule) with the following command.
    ```bash
    git clone --recursive https://github.com/rendercv/rendercv.git
    ```
4. Go to the `rendercv` directory.
    ```bash
    cd rendercv
    ```
5. RenderCV uses three virtual environments:
    -  `default`: For the development and testing. It contains packages like [Ruff](https://github.com/astral-sh/ruff), [Black](https://github.com/psf/black), [pytest](https://github.com/pytest-dev/pytest) etc.
    -  `docs`: For building the documentation.

    Create the virtual environments with the following commands.

    ```bash
    hatch env create default
    hatch env create docs
    ```

6. To use the virtual environments, either

    - Activate one of the virtual environments with one of the following commands.
        ```bash
        hatch shell default
        ```

        ```bash
        hatch shell docs
        ```

    - Select one of the virtual environments in your Integrated Development Environment (IDE).

        === "Visual Studio Code"

            - Press `Ctrl+Shift+P`.
            - Type `Python: Select Interpreter`.
            - Select one of the virtual environments created by Hatch.

        === "Other"

            To be added.

### Develop with GitHub Codespaces

1.  [Fork](https://github.com/rendercv/rendercv/fork) the repository.
2.  Navigate to the forked repository.
3.  Click the <> **Code** button, then click the **Codespaces** tab, and then click **Create codespace on main**.

Then, [Visual Studio Code for the Web](https://code.visualstudio.com/docs/editor/vscode-web) will be opened with a ready-to-use development environment.

This is done with [Development containers](https://containers.dev/), and the environment is defined in the [`.devcontainer/devcontainer.json`](https://github.com/rendercv/rendercv/blob/main/.devcontainer/devcontainer.json) file. Dev containers can also be run locally using various [supporting tools and editors](https://containers.dev/supporting).

## Available Commands

These commands are defined in the [`pyproject.toml`](https://github.com/rendercv/rendercv/blob/main/pyproject.toml) file.

- Format the code with [Black](https://github.com/psf/black) and [Ruff](https://github.com/astral-sh/ruff)
    ```bash
    hatch run format
    ```
- Lint the code with [Ruff](https://github.com/astral-sh/ruff)
    ```bash
    hatch run lint
    ```
- Run [pre-commit](https://pre-commit.com/)
    ```bash
    hatch run precommit
    ```
- Check the types with [Pyright](https://github.com/RobertCraigie/pyright-python)
    ```bash
    hatch run check-types
    ```
- Run the tests
    ```bash
    hatch run test
    ```
- Run the tests and generate a coverage report
    ```bash
    hatch run test-and-report
    ```
- Start the development server for the documentation
    ```bash
    hatch run docs:serve
    ```
- Build the documentation
    ```bash
    hatch run docs:build
    ```
- Update [schema.json](https://github.com/rendercv/rendercv/blob/main/schema.json)
    ```bash
    hatch run docs:update-schema
    ```
- Update [`examples`](https://github.com/rendercv/rendercv/tree/main/examples) folder
    ```bash
    hatch run docs:update-examples
    ```
- Update figures of the entry types in the "[Structure of the YAML Input File](https://docs.rendercv.com/user_guide/structure_of_the_yaml_input_file/)"
    ```bash
    hatch run docs:update-entry-figures
    ```

## About [`pyproject.toml`](https://github.com/rendercv/rendercv/blob/main/pyproject.toml)

[`pyproject.toml`](https://github.com/rendercv/rendercv/blob/main/pyproject.toml) contains the metadata, dependencies, and tools required for the project. Please read through the file to understand the project's technical details.
