# RevealPack Documentation

Welcome to the RevealPack documentation. RevealPack is a command-line interface (CLI) tool for managing and building multiple Reveal.js presentations.

## Motivation

RevealPack is more than just a Reveal.js presentation starter; it's a comprehensive framework for creating suites of presentations that share themes and resources, such as a lecture series or a multi-day seminar. RevealPack abstracts much of the slide deck creation process, allowing for complete control over individual slides or groups of slides within each presentation. 

With RevealPack, you can:
- Create slides individually or group multiple slides in one file.
- Share raw HTML or Markdown slides with others.
- Create section title slides or decorate the `section` tag with YAML headers.
- Serve your presentation during development with live updating for smart automatic rebuilds of changed files.

## Commands

- [`init`](init.md): Initialize the directory structure.
- [`setup`](setup.md): Set up the environment.
- [`build`](build.md): Build the presentations.
- [`serve`](serve.md): Serve the presentations locally.
- [`package`](package.md): Package the presentation for distribution.
- `docs`: View the documentation.

## Installation

### Requirements

- Python >3.9, (>=3.12 recommended)

### Install RevealPack from PyPI

To install RevealPack, run:

```bash
pip install revealpack
```

_Note: Use the appropriate method for your setup, e.g., `pip3` or `python -m pip...`._

## Workflow

### Initial Setup

1. **Choose a Project Directory**: Select a directory for your project. It is recommended to create a Python virtual environment in your chosen directory (`root`) and install RevealPack there, rather than using a global environment.

2. **Initialize the Project**: Navigate your terminal or command window to the root directory, activate your Python 3 environment, and use the `revealpack init` command to initialize the directory for your presentations.

```bash
revealpack init
```

3. **Modify Configuration**: Customize the `config.json` file for your project.

4. **Setup Development Environment**: Set up the presentation development environment with the `revealpack setup` command.

```bash
revealpack setup
```

### Presentation Development Workflow

- **Build Presentations**: Use `revealpack build` to compile your presentations.

```bash
revealpack build
```

  The `revealpack build` command converts slide decks located in the specified source directories into individual presentations, handling everything from copying necessary libraries to compiling themes and generating HTML files. This command processes each subdirectory within the presentation root directory, creating a presentation for each.

  **Options**:
  - `--root <directory>`: Specifies the root directory for the build. Defaults to the current working directory.
  - `--clean`: Performs a clean build by removing all contents of the build directory before starting the build process.
  - `--decks <file or string>`: Specifies a comma-separated list of deck names or a path to a file containing deck names to be built. If this option is provided, a clean build is automatically performed.

  The build process includes injecting custom styles and scripts, compiling SCSS/SASS themes, managing plugins, and generating a table of contents for the presentations. It ensures that all necessary files are included and properly configured, resulting in fully functional Reveal.js presentations.

- **Serve Presentations Locally**: Use `revealpack serve` to start a local server with live reloading for development.

```bash
revealpack serve
```

- **Package Presentations for Distribution**: Use `revealpack package` to package your presentations into a distributable format.

```bash
revealpack package --target-dir <build_directory> [--root <root_directory>] [--no-build] [--clean] [--decks <file_or_string>]
```

  The `revealpack package` command prepares your presentations for distribution by copying the built files to a specified destination directory and setting up the necessary project files, including `package.json`, installer configurations for macOS and Windows, and other required assets.

  **Options**:
  - `--root <directory>`: Specifies the root directory for packaging. Defaults to the current working directory.
  - `--target-dir <directory>`: Specifies the directory where the package will be created. Defaults to the directory specified in `config.json` under `directories.package` or `package_output` if not set.
  - `--no-build`: Skips the build step. This is useful if the build has already been done and you only want to package the results.
  - `--clean`: Performs a clean build before packaging. This ensures that only fresh files are included in the package.
  - `--decks <file or string>`: Specifies a comma-separated list of deck names or a path to a file containing deck names to be built and included in the package. If this option is provided, a clean build is automatically performed.

  The packaging process includes generating a `package.json` file, setting up installer configurations for both macOS and Windows, and creating a `.gitignore` file and a GitHub Actions workflow to automate the build and release process. This ensures that your presentations are ready to be packaged into standalone applications.

For example, to package your presentations without rebuilding, you would run:

```bash
revealpack package --target-dir path/to/new/package --no-build
```

## Development

For more detailed information on development, see the [Developer's Guide](https://revealpack.readthedocs.io/en/latest/dev/).