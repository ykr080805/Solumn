# Saved filters

Finance saves a view from the console with "save this view". The console
writes the filter into `saved_filters.expression` and hands the name back to
whoever asks for it.

## The expression language

The console has its own filter language. It is not SQL, and it is deliberately
smaller:

    <field> <op> <value> [ and|or <field> <op> <value> ]...

    fields   vendor_name  status  issued_on  amount_cents
    ops      =  !=  >  >=  <  <=  contains
    values   bare words and numbers; no quoting, no functions, no parentheses

So `status = overdue and amount_cents >= 90000` is a whole expression, and
`contains` is a substring match on the named field.

The resemblance to SQL is a coincidence of both being infix. The console team
picked the operators to look familiar to finance, who write them by hand in the
box. Nothing validates what goes into that column on the way in -- the console
stores whatever was typed, and a filter that does not parse is simply a filter
that returns an error when someone runs it.

## Who writes them

Anyone in finance with console access, and they edit them in place. The three
in the fixture are the ones the audit team uses most.

## The sort a view remembers

A saved view remembers how it was sorted when it was saved, in
`saved_filters.order_spec`. It is a comma separated list of
`<column> <asc|desc>`, so `vendor_name asc, amount_cents desc` is one spec.

This is the part of a view that cannot be bound. SQLite will not take an
identifier as a parameter -- `ORDER BY ?` is a syntax error -- so whatever a
view remembers has to reach the statement as text. The console writes these
specs; nothing checks them on the way in, the same as the expression.
