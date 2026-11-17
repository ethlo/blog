---
date: 2026-09-19
categories:
  - Gateway
---

# Five bugs in my own gateway in one day

On 18 September I filed five bugs against my own gateway. I had not found any of them myself. An AI review did, in code I have run since 2023.

<!-- more -->

I had not expected much. The code is not new, it has been reviewed, and it has carried real traffic for years.

This is what I got.

A write to the file that captures request and response bodies could be short. `AsynchronousFileChannel.write` is allowed to write only part of the buffer, and my code completed after one callback. The rest was never written. So the tail of a captured body could be missing, with no error.

Upstream services that were removed from the configuration kept serving their routes. Forever, until restart.

An upstream that closed the connection in the middle of a response left buffer files behind, and the access log said 200 for a response the client never got in full.

A malformed `Content-Type` header threw an exception in the logging code, so the request that most deserved a log entry got none.

And the ClickHouse connection pool was never closed.

## What bothers me

Look at the first one. This gateway exists to answer what a client sent us. And the capture could drop the end of the body without telling anyone. That is the one promise it makes.

I know that a write can be short. Everyone who has done I/O knows that. I still wrote the code as if it could not, and then read it many times without seeing it. It works in every test, since a short write to a local file almost never happens.

A person reviewing that code reads what it does. The machine seems to read what the API is allowed to do, and has the patience to check each call against it. I do not have that patience on the fifth file.

## What I take from it

AI reviews are powerful. I say that with a smiley, and with some discomfort.

The second bug is worth a note of its own. It was a regression from another fix, and it was caught in the review of that fix. Before, the route map was wiped on every refresh, which cleaned up removed services as a side effect of a bug. I fixed the bug and lost the side effect.

All five are fixed.
