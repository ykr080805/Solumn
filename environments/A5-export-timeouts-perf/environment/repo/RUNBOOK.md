# casebundle runbook

On-call notes for the support log bundler. Keep this in sync with the code.

## Why the archive steps use wildcards

The log directories hold rotated files (`app.log`, `app.log.1`, `app.log.2.gz`)
alongside scratch files the collector leaves behind. Archive steps select what
they want with a wildcard rather than enumerating the directory, so that a new
rotation suffix does not need a code change.

Some accounts have more than one collector writing into the same directory, and
the CRM writes those as a brace group: Harrow Water's case 5 carries
`{app,pump}.log`, meaning the two named files and nothing else. Support edits
these in the CRM whenever a site gains or loses a collector, so the set is not
fixed and not ours to enumerate.

## Retention

`cases.retention_days` is advisory. The cleanup job reads it; the bundler and
the exporter do not.

## Where the case index comes from

`cases` is written by the CRM sync job every fifteen minutes. Support agents
edit case fields in the CRM, so `ref`, `account` and `include_glob` are
whatever the CRM last handed us. Nothing in this repo writes to that table.
