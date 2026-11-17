---
date: 2019-10-01
categories:
  - Java
  - Spring
share: assets/social/scripts-inside-a-running-jvm.png
description: "Every client wants one small thing that no other client wants. It is always a few lines of code, and it never belongs in the main code base."
---

# Scripts inside a running JVM

Every client wants one small thing that no other client wants. It is always a few lines of code, and it never belongs in the main code base.

<!-- more -->

You know the kind. One client needs three API calls done as one, in one transaction. Another needs a report that is too heavy and too odd to be a feature. Say yes to all of it and the core fills up with special cases. Say no and you are the reason the integration is late.

[Lamebda](https://github.com/ethlo/lamebda) is my way of saying yes somewhere else. It is a plugin system for a Spring application. You put a project folder next to the running application, with source files in it, Groovy or Java:

```groovy
@RestController
class MyController {
    @GetMapping("/my/{id}")
    def get(@PathVariable("id") int id) {
        return [requested: id]
    }
}
```

The application compiles it, loads it and serves it under its own path. The script runs inside the JVM, so it can call the same services the core uses, in the same transaction. That is what you cannot get from an integration that lives outside and talks HTTP: several calls that either all happen or do not.

It is used for batching, for transactions across calls, and for the ad-hoc services behind complex and costly reports. The custom code can change every week and the core does not have to be released for it.

## How isolated is it?

Less than it looks. The code is out of the main repository, and that feels clean. But it runs in the same process, with the same database and the same memory. A bad script can take the application down as well as any code in the core can, and it has been through less review.

So the isolation is in the source and in the release cycle. At runtime there is none, and I should not pretend there is.

Each project gets one class loader of its own, so a project can be reloaded as a unit when its files change.

*Update, November 2026: it is a slippery slope. When a component from a script gets registered with other parts of the application, the old class loader cannot be unloaded, and you get `NoClassDefFoundError` after a reload.*
