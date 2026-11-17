---
date: 2026-11-06
categories:
  - Home Assistant
---

# The school's weekly plan in Home Assistant, without AI

I use AI for nearly everything I build these days. For reading my children's weekly plans from school I chose not to, and I think that was right.

<!-- more -->

The school sends a weekly plan for each class. It comes as a PDF or a Word file attached to a message in the guardian portal. To know that Thursday is a trip and gym is moved, you log in with BankID, find the message, open the attachment and read a table. Every week, per child. BankID is what you sign a loan with. Here it guards a timetable.

I wanted it in the family calendar in Home Assistant.

The portal has no public API, so the integration uses the one the portal's own web page uses. It is read-only. It never replies, never marks anything as read and never answers a form.

## Why not a language model?

Reading a table out of a PDF and making calendar events is the kind of task you would hand to a language model today. I did not, for three reasons.

It is about children. The plans and messages have names in them, and I do not want to send that to a service to save myself some parsing.

It has to be the same every time. A parser that reads a plan gives the same events tomorrow as today. And when it cannot read a plan, it gives nothing. A model would give me something that looks right. A wrong gym day is worse than a missing one.

And the plans are not that varied. A plan is a table with the weekdays as columns. What is the same every day is left out, and what differs becomes an event. Rows that say when school ends give the end of the day, and the homework columns give homework.

So it is a script. Each file is read once.

## What that costs

The honest downside is that it only reads the layouts it has seen. A teacher who makes the plan in a new way gets a plan that comes out wrong, or not at all. A model would likely cope with that, and my parser needs a new test fixture.

PDFs are also not tables. They are text placed at positions, and the table is something your eye makes. The parser reads the text in layout mode and finds the columns again from the spacing, which is as fragile as it sounds.

I still think it is the right trade here. It is boring and predictable, and the data stays at home.

Logging in was the hard part, to be honest. BankID needs a real browser, and Home Assistant cannot log in by itself. So there is a Chromium container next to it, and you log in there from your phone. It is [on GitHub](https://github.com/ethlo/ha-visma-skole) if you are a parent in the same portal.
