---
date: 2026-10-02
categories:
  - Gateway
---

# Why r7 moved from Undertow to Helidon Níma

r7 now runs every request on a virtual thread of its own, the upstream call included. To get that I replaced the HTTP server under it, five months in and a week and a half before the first beta.

<!-- more -->

r7 started on Undertow. It is a good server. I had no bug to point at, and no number that forced the move.

What I had was an execution model I liked better. In Helidon Níma every request runs on a virtual thread of its own, the upstream call included. The code for a request reads from top to bottom: read the request, run the filters, call the upstream, write the response. It blocks where it waits, and that is fine, since a blocked virtual thread costs almost nothing.

There are no worker pools to size and no handoff between an I/O thread and a worker. There is also no reactive chain. I have written a gateway on a reactive stack before, and a stack trace from it tells you very little about what your code was doing. Debugging it is a pain in the neck.

For a gateway that people extend with their own filters, that matters more than a few percent. A filter is plain Java that runs on the request's thread. If it blocks, it blocks that request and nothing else.

## What it took

Less than I feared, and the reason is boring. The request guards and the tests had already been made server-neutral, so the end-to-end suite could run against both servers. When it was green on Helidon, Undertow went out, with its own settings: the read timeout, the proxy client and the "advanced" block.

Swapping the server this late is something I would question in a review. But it was before the first beta, with nobody depending on the old settings, and that door closes on release day.
