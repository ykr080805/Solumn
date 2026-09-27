# Abandoned levers

`A1x-profile-table` is the command-template lever: a table of archive command
strings that `bundler.py` and `maintenance.py` both used, on the theory that
GPT-5.5 was pattern-matching on repository conventions. It was validated and
rolled out, and the model ignored the table entirely -- it wrote its own
correctly quoted `find | tar` pipeline. The negative result is why the design
moved to brace expansion instead, so the run is kept here.

The script that applies it is `tools/strengthen_pull.py`.
