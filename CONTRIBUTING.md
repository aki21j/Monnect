# Contributing to Monnect

Thanks for contributing.

## Development Setup

Clone the repository:

    git clone https://github.com/aki21j/Monnect.git
    cd Monnect
    pipx install -e .

## Making Changes

After modifying code:

    pipx uninstall monnect
    pipx install -e .

## Reporting Issues

Please include:
- macOS version
- Output of `monnect doctor`
- Relevant logs
- Steps to reproduce

## Pull Requests

- Keep changes focused
- Update CHANGELOG if needed
- Ensure CLI commands work correctly
