---
date: 2026-11-09
categories:
  - AI
---

# Rules that make an AI agent useful on side projects

I have more side projects moving now than I ever had, since an AI agent does most of the typing. For a while I also had more things that did not work than I ever had.

<!-- more -->

The agent is fast and it is confident. It tells you a thing is built, and it is, in the sense that the code exists. Whether it runs is another matter.

So the projects have rules now. They are not clever. Most of them are what I would tell a new developer in the first week.

**Never claim something is built unless it was run.** This is the first one and the one that changed the most. "Done" has to come with what was run and what came out. A test that only prints a number is not a test.

**Decisions are written down, with the reason.** One file per decision, dated. The game project has 84 of them. The agent starts every session without memory, so without these it will propose the idea I rejected last week, with the same good arguments.

**Findings go in a dated file.** What was tried, what came out, kept or not. This includes the dead ends, and those are the most valuable. The same project has 202 experiment notes.

**A design note is history.** It says how we got here. It is read for the why and never as a description of the code as it is now.

**One command builds it and one command tests it**, and both are in the file the agent reads first.

## None of this is about AI

Decision records, a lab notebook and "it is not done until it runs" are things I have known for a long time. I have also skipped them on my own projects for just as long, since I was the only one there and I remembered.

The agent does not remember, so I had to write it down. And now my side projects are better documented than a good part of what I have been paid to build.

That is a bit embarrassing.
