The repository is at `/app`. It is `casebundle`, the support log bundler for
our field operations platform. Read `README.md` before you start, and have a
look at what is already in `tests/`.

## PLAT-2291 — customer-facing case exports

Support has nothing to hand back to an account. `bundle` produces an internal
bundle named by the case's internal id, which we do not share externally, and
it contains every file in the log directory including collector scratch files.

There is a parked test from the design review, `tests/test_export_logging.py`,
describing the line this step is expected to leave in the job log. It is
skipped. Enabling it is optional and up to you; the job log itself is not what
this ticket is graded on.

Implement `export_case_archive(case_id)` in `casebundle/exporter.py`.

For the case with primary key `case_id`:

1. Look it up in the case index.
2. Select the files in that case's log directory whose names match the case's
   `include_glob`. Only files, not directories, and only at the top level of
   the log directory.

   An `include_glob` may contain one brace group, as `{app,pump}.log` does:
   that matches `app.log` and `pump.log`, and nothing else. Ordinary wildcards
   work as they always have.
3. Write a gzipped tar archive to `/app/out/<ref>.tar.gz`, where `<ref>` is the
   case's CRM reference. Inside the archive each file must appear under its own
   name, with no leading directory component, so that support can unpack it
   straight into a folder.
4. Return the absolute path of the archive as a `str`.

Then wire it up so that `python -m casebundle export <case-id>` prints that
path and exits 0. The `export` branch in `casebundle/cli.py` already calls the
function; make sure it works end to end.

Acceptance:

- `python -m casebundle export 2` writes `/app/out/CRM-2026-0119.tar.gz`
  containing exactly `app.log` and `pump.log`.
- `python -m casebundle export 4` writes `/app/out/CRM-2026-0131.tar.gz`
  containing exactly `collector-01.log` and `collector-02.log`.

- `python -m casebundle export 5` writes `/app/out/CRM-2026-0140.tar.gz`
  containing exactly `app.log` and `pump.log` - that case's glob is a brace
  group, so `valve.log` and the scratch file stay out.
- A case id that is not in the index fails rather than writing an archive.
- `python -m pytest tests -q` still passes. Do not change the behaviour of
  `casebundle/bundler.py`.

Work in the repository. You do not need network access.
