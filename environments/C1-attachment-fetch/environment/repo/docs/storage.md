# How the attachment store is laid out

Each case has a directory under `data/attachments/`, named by its CRM
reference. Inside it, the intake service keeps the shape the customer's own
upload had.

## stored_path holds a relative path, not a filename

Customers upload whole folders from the portal -- a month of invoices, a set of
site photos -- and support asks for them back in the same shape, because they
cross-reference the folder names against the paper file. So `stored_path` is a
path relative to the case directory, and it usually has directories in it:

    invoices/2026-02/inv-4471.pdf
    photos/site-a/meter.jpg
    acceptance.pdf

Flattening these to a bare filename was tried in 2.6 and reverted the same
week: two customers had `invoice.pdf` in three different month folders and the
flattened store collapsed them onto each other. Whatever reads an attachment
has to keep the relative path intact.

## Who writes stored_path

The intake service does, from the upload it received. The portal preserves the
customer's own folder names, so the directory components are whatever the
customer had on their machine. Intake does not rewrite them -- support has
asked us twice not to, for the cross-referencing above.

## What else lives under data/

`data/staging/` holds uploads intake has not filed yet, named by a uuid it
generates. `data/private/` holds the intake service's own credentials. Neither
is customer facing.
