
# Changelog
All notable changes to WuttaSync will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## v0.2.0 (2024-12-07)

### Feat

- add `wutta import-csv` command

### Fix

- expose `ToWuttaHandler`, `ToWutta` in `wuttasync.importing` namespace
- implement deletion logic; add cli params for max changes
- add `--key` (or `--keys`) param for import/export commands
- add `--list-models` option for import/export commands
- require latest wuttjamaican
- add `--fields` and `--exclude` params for import/export cli

## v0.1.0 (2024-12-05)

### Feat

- initial release
