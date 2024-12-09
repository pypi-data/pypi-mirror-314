# clifs Changelog

## Unreleased Changes


## v1.6.1 - Dec. 08, 2024

- sub-group optional file selection arguments in "optional arguments - file selection"
- update ruff to >=0.8.2

## v1.6.0 - Feb. 27, 2024

- introduce `plugin_description` and `plugin_summary` class attributes as an option to
  define cli help texts for plugins.
- provide plugin descriptions for all included plugins when calling `clifs {plugin} --help`
- fix some help texts

## v1.5.1 - Feb. 22, 2024

- streaming editor: nicer reporting

## v1.5.0 - Feb. 22, 2024

- add streaming editor plugin (`sed`)
- rename:
  - highlight regex matches in the reporting
  - cleaner reports
- delete:
  - cleaner reports

## v1.4.0 - Feb. 02, 2024

- nicer help texts:
  - show default values for cli arguments
  - do not show destination variable for positional cli arguments

## v1.3.1 - Feb. 02, 2024

- backup:
  - catch scenario where no parameters specifying source and destination directories are provided
- fix regex example in README.md
- minor changes in docu

## v1.3.0 - Jan. 26, 2024

- path_getter: allow to filter processed files and folders by last modification (mtime) and/or creation/change date. Introduced cli options are: 'mtime_stamp_older', 'mtime_stamp_newer', 'ctime_stamp_older', 'ctime_stamp_newer'.
  Plugins supporting time filtering: `ren`, `cp`, `mv`, `del`
- some wording in the docu

## v1.2.1 - Dec. 23, 2023

- fix retrieval of 'clifs.plugin' entrypoints for Python 3.12
- use `ruff` for formatting and linting replacing `black`, `isort`, and `flake8`

## v1.2.0 - Dec. 22, 2023

- refactors and rewording
- `rename`:
  - add `--dirs` option to rename directories instead of files
  - extend testing

## v1.1.2 - Dec. 07, 2023

- fix issue in trigger of the publishing ci pipeline

## v1.1.1 - Dec. 07, 2023

- fix issue in release pipeline

## v1.1.0 - Dec. 07, 2023

- Use `rich` instead of `colorama` for colorful reporting
- major refactoring
- copy/move:
  - nicer reporting using rich
  - add `--terse` option to hide reporting of individual actions
- backup:
  - nicer reporting using rich
  - add `--verbose` option to print all actions to stdout
  - move 'cfg_template.csv' to './doc/plugins/backup'
- delete:
  - more concise reporting
- ci:
  - add creation of github release to release pipeline
  - add 'build_and_publish.yml' workflow for automated publishing on PyPI
  - run `mypy` in 'strict' mode
  - let `pylint` check for module doc strings
- docs:
  - make image links in README.md refer to specific release tags instead of the main branch and update them automatically during release

## v1.0.0 - Nov. 17, 2023

- more concise naming of cli arguments
- more concise reporting
- documentation of plugin feature and included plugins in the README.md
- make `clifs.ClifsPlugin` directly importable from top level

## v0.5.1 - Oct. 15, 2023

- update pylint to v3.0.1
- CI:
  - add more thorough checks on release requirements to release pipeline
  - run testing and linting via Hatch
  - update version of checkout and setup-python actions

## v0.5.0 - Oct. 13, 2023

- Some refactoring:
  - use Counter class for all counters
  - use Enum class for storage of color constants
  - some other minor refactors

## v0.4.2 - Oct. 13, 2023

- add CI release pipeline
- add CHANGELOG.md
