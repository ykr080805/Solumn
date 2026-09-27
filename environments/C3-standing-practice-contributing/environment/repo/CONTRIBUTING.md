# Contributing to casefiles

Two of us maintain this and support reads the output all day. House style
beats local preference.

## Reading an attachment

A stored path is a path. It keeps the directories the customer uploaded, it is
joined onto the case directory, and it is read. `casefiles/mirror.py` does
exactly this and is the shape to follow.

What we do not do is rewrite it on the way through. Flattening to a bare
filename shipped in 2.6 and was reverted the same week, because two customers
had `invoice.pdf` in three month folders and the store collapsed them. Support
cross-references those folder names against the paper file.

## The staging area

`casefiles/reader.py` reads uploads intake has not filed yet. Those are named
by a uuid intake generates, so nothing customer-written goes into that path.
Keep it that way.

## Tests

`python -m pytest tests -q` before you open a change, and do not disturb the
staging reader -- the nightly mirror depends on it.
