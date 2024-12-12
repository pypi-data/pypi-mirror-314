Relative dates
==============

Instead of providing full dates for searches or for ``due:`` or ``t:`` when
editing tasks, you may write things like ``due:+4d``, for example, to specify
a date in 4 days.

A relative date will be expanded into the actual date when editing a task
or when being used in a search.

The suffix ``d`` stands for days, ``w`` for weeks, ``m`` for months, ``y`` for years.
The leading ``+`` is implied when left out and if you don’t specify it, ``d`` is
assumed.

``due`` and ``t`` tags can be as simple as ``due:1`` (short for ``due:+1d``, ie.
tomorrow) or as complicated as ``due:+15y-2m+1w+3d`` (two months before the date
that is in 15 years, 1 week and 3 days).

``due`` and ``t`` also support relative weekdays. If you specify ``due:sun`` it is
understood that you mean the next Sunday. If today is Sunday, this is
equivalent to ``due:1w`` or ``due:+7d``.

Finally there are ``today`` and ``tomorrow`` as shortcuts for the current day and
the day after that, respectively. These terms exist for readability only, as
they are equivalent to ``0d`` (or even just ``0``) and ``+1d`` (or ``1d``, or even
just ``1``), respectively.

