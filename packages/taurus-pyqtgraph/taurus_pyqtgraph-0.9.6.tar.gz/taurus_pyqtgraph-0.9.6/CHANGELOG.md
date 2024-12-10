# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).
This file follows the formats and conventions from [keepachangelog.com]

## [Unreleased]
### Added
- Added configuration decimation dialog for querying data to pyhdbpp using the decimation features.

### Fixed
- Modified docker images names to get the correct ones.
- Changed query window for archiving integration,
  instead of querying from the oldest visible date to the oldest known point it will query
  from the oldest visible date to the newer visible date. (!126)
- Commented step of parametrized test that was failing with python3.9 with no apparent reason. (#132)

## 0.9.4
### Added
- Added documentation for the installation and usage of taurus_pyqtgraph. (!124)

### Fixed
- Gitignore file to ignore /public folder on documentation generation.
- Added support for bool, int and float values when rvalue has no magnitude on taurus trend sets.

## 0.9.3

### Added
- Save configuration now saves 3 property configurations to configdict: dynamicRange, leftAxisLogMode and bottomAxisLogMode (#122, !126)

### Fixed
- Handled those attributes that cannot be plotted and the corresponding legend is not added due to the fact that the associated device is down or the attribute doesn't exist. (!123)

## 0.9.2

### Fixed
- General bug fixes

## 0.9.1

### Added
- First release with this changelog being updated.
- Curves names shown at the inspector mode tooltip. (#121, !117)

### Fixed
- Solve bug with statistics dialog. (#125, !118)
- Fix f-string new format to .format style. (!119)

## 0.9.0

### Added
- Added range selector for X Axis view on trends. (#108, !112)
- Added basic "Taurus4 compatible" data file export option. (!113)
- Added new method to taurus trend to set logarithmic mode programmatically. (!115)
- Added pyhdbpp as an optional dependency . (!116)



[keepachangelog.com]: http://keepachangelog.com
[TEP17]: https://github.com/taurus-org/taurus/pull/452
[Unreleased]: https://gitlab.com/taurus-org/taurus_pyqtgraph/-/tree/main




