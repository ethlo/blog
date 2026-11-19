---
date: 2026-10-13
categories:
  - Gateway
  - Performance
share: assets/social/my-own-benchmark-refused-to-publish-my-numbers.png
description: "I built a benchmark that decides by itself whether its numbers can be published. On the run I wanted to publish, it said no."
image: assets/thumbs/my-own-benchmark-refused-to-publish-my-numbers.jpg
---

# My own benchmark refused to publish my numbers

I built a benchmark that decides by itself whether its numbers can be published. On the run I wanted to publish, it said no.

<!-- more -->

I do not trust gateway benchmarks much, mine included. It is too easy to get a nice number. Run the load generator on the same cores as the gateway, leave turbo on, pick the run that looked best, and you have a figure that nobody can reproduce, including you.

So the benchmark for [r7](https://github.com/ethlo/r7) is one command, and it is strict with me.

It measures the published image, by digest, and not something I built on my laptop. wrk and wrk2 are built from pinned commits. The host is tuned first: SMT and turbo off, the `performance` governor, and every other process moved to housekeeping cores. nginx as backend, the gateway and the load generator each get cores of their own. wrk finds the saturation throughput, and wrk2 holds a fixed rate, so the p99 is free of coordinated omission.

There are two baselines. One has no gateway, which shows what the proxy hop costs in total. The other is r7 in the path with no filters and no journal. What a filter or a journal level costs is quoted against the second one, since it has the same topology and the same contention, and the noise cancels.

And every report opens with a verdict, PUBLISHABLE or NOT PUBLISHABLE. A dirty tree, a tuning step that did not apply, a missing run, or a backend that is not at least 10% faster than every r7 row, and the verdict is no.

## The run of 11 October

NOT PUBLISHABLE.

My first reaction was that the verdict was wrong. That is the reaction the verdict is there for, so I read the reasons.

There were three. nginx as a peer had reached the backend's own limit, so its number was the backend's and not nginx's. Spring Cloud Gateway could not hold the fixed 20,000 requests per second at all. And r7 itself could not hold that rate on the browser page with full journaling, where it saturates at 14,900.

None of these is a broken measurement. They are results. A gateway that cannot hold the rate is a finding about the gateway. One of the three was about r7 itself, and I did not enjoy that one.

<svg viewBox="0 0 680 128" role="img" aria-label="API GET, saturation in requests per second on two cores." style="width:100%;max-width:680px;height:auto;font-family:inherit">
<text x="0" y="16" font-size="13" text-anchor="start" fill="currentColor" opacity="0.75">API GET, saturation in requests per second on two cores.</text>
<text x="120" y="49" font-size="13" text-anchor="end" fill="currentColor">nginx</text>
<rect x="130" y="34" width="330.0" height="20" rx="3" fill="currentColor" opacity="0.35"/>
<text x="468.0" y="49" font-size="13" text-anchor="start" fill="currentColor">60,300, the backend's limit</text>
<text x="120" y="79" font-size="13" text-anchor="end" fill="currentColor">r7</text>
<rect x="130" y="64" width="238.6" height="20" rx="3" fill="#4f8cff"/>
<text x="376.6" y="79" font-size="13" text-anchor="start" fill="currentColor">43,600</text>
<text x="120" y="109" font-size="13" text-anchor="end" fill="currentColor">cloud-gateway</text>
<rect x="130" y="94" width="101.8" height="20" rx="3" fill="currentColor" opacity="0.35"/>
<text x="239.8" y="109" font-size="13" text-anchor="start" fill="currentColor">18,600</text>
</svg>

*The nginx bar is the backend's number. That was the first of the three reasons.*

But the rule as I wrote it called them failures. So I had two choices. I could publish anyway and explain. Or I could change the rule, in the open, and show both.

I changed the rule. A peer at the backend's limit and a fixed-rate run above capacity are now marked in the report as results, and do not fail the run. The published page has the original report with its NOT PUBLISHABLE at the top, and next to it the current verdict over the same result files.

## Is that cheating?

It might look like it. I wrote a gate, it stopped me, and I moved the gate.

I do not think it is, since the numbers did not change and both verdicts are there to read. But I notice that I only found the flaw in the rule when it stood between me and a result I wanted. Would I have looked as hard if it had said PUBLISHABLE on a bad run? I hope so.

The numbers come from one run. Every throughput figure carries the spread of its three repeats, and a difference smaller than that spread is not a finding. The [benchmark page](https://r7.ethlo.com/benchmarks/) has all of it.
