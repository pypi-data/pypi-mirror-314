# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.3] - 2024-12-09

- Add formatting to `--dry_run` output to more easily create shell script. 
- Quote-escape the command output for `--dry_run` and strip on execution.
- Add tests.

## [1.3.2] - 2024-11-07

- Support both Pydantic 1 and Pydantic 2.

## [1.3.1] - 2024-10-24

- Add `--uvpip` option to make `uv pip install` commands.
- Include placeholder for future `method=uv.tool` stanza.

## [1.3.0] - 2024-10-22

- Attempt to use keyring in pull-private-deps.
- Provide clearer error on fallback with no tokens.
- Note `uv` in ppinfo.

## [1.2.2] - 2024-10-17

- Fix docker tag.
- Avoid showing tokens with `--dry_run`

## [1.2.1] - 2024-10-16

- Update docs.

## [1.2.0] - 2024-10-16

- Validate toml configuration using Pydantic model
- Support multiple installation methods

## [1.1.0] - 2024-10-09

- Clean up docs for public release.

## [1.0.2] - 2024-10-09

- Various pipeline bugfixes.

## [1.0.0] - 2024-10-08

- Imported previous versions with working local pipeline.

## [0.0.0] - 2024-10-07

- Initialized project using [GDA-Cookiecutter](https://gitlab.geomdata.com/geomdata/gda-cookiecutter)
