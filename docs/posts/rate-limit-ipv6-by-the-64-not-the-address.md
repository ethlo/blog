---
date: 2026-09-30
categories:
  - Gateway
  - Security
share: assets/social/rate-limit-ipv6-by-the-64-not-the-address.png
description: "My gateway had a rate limiter that did nothing for IPv6 clients. I wrote it, and I should have known better."
image: assets/thumbs/rate-limit-ipv6-by-the-64-not-the-address.jpg
---

# Rate limit IPv6 by the /64, not the address

My gateway had a rate limiter that did nothing for IPv6 clients. I wrote it, and I should have known better.

<!-- more -->

The limiter in r7 is a token bucket per client, and the client was the IP address. For IPv4 that is fine. One address is roughly one client, or one office behind NAT.

For IPv6 it is wrong, and not by a little. A subscriber is normally given a whole /64. That is 2⁶⁴ addresses, about 18 quintillion, and the client can use any of them. So a client that wants to get past the limit takes a new address for every request, and gets a new, full bucket each time.

<svg viewBox="0 0 680 130" role="img" aria-label="An IPv6 address split into the 64 bits the provider assigns and the 64 bits the client picks" style="width:100%;max-width:680px;height:auto;font-family:inherit">
<text x="0" y="16" font-size="13" text-anchor="start" fill="currentColor" opacity="0.75">An IPv6 address. Documentation prefix, not a real one.</text>
<rect x="0" y="34" width="336" height="44" rx="4" fill="#4f8cff" fill-opacity="0.25" stroke="#4f8cff"/>
<rect x="344" y="34" width="336" height="44" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-opacity="0.4"/>
<text x="168" y="62" font-size="17" text-anchor="middle" fill="currentColor" font-family="monospace">2001:0db8:1234:5678</text>
<text x="512" y="62" font-size="17" text-anchor="middle" fill="currentColor" font-family="monospace">xxxx:xxxx:xxxx:xxxx</text>
<text x="168" y="100" font-size="13" text-anchor="middle" fill="currentColor">64 bits from the provider</text>
<text x="512" y="100" font-size="13" text-anchor="middle" fill="currentColor">64 bits the client picks</text>
<text x="168" y="120" font-size="12" text-anchor="middle" fill="currentColor" opacity="0.7">one subscriber, and now one bucket</text>
<text x="512" y="120" font-size="12" text-anchor="middle" fill="currentColor" opacity="0.7">was one bucket per value</text>
</svg>

It is worse than no limit. The limiter keeps a bucket per address in memory, up to `max_buckets`. So the same client that walks past the limit also fills the table and pushes out the buckets of everyone else.

This is kinda humiliating. It is not obscure. I have known how IPv6 addresses are handed out for years, and I still wrote "per address" without thinking, the way I have always done it for IPv4.

## The fix

IPv6 clients are now keyed by the leading 64 bits. IPv4 clients are keyed by the full address as before.

```yaml
rate_limiter:
  capacity: 100
  refill_tokens: 100
  refill_period: 1s
  ipv6_prefix_length: 64
```

64 is the default, so you do not have to set it. You can lower it to 56 or 48 if you see providers that hand out more than a /64 per customer.

It was fixed before the first beta. If you have a rate limiter of your own, look at what it uses as the key.
