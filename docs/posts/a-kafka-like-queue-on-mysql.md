---
date: 2017-02-10
categories:
  - Java
  - Databases
---

# A Kafka-like queue on MySQL

Everybody knows you should not build a message queue on a database. I just did, and I think it was the right call.

<!-- more -->

What I needed was small. Events have to be kept for a few days. A client that reconnects must be able to say "I have seen up to message 45,610" and get the rest. The volume is a few tens of messages per second.

Kafka does that, and it is what I would pick for real volume. But a Kafka cluster is something you operate. It needs ZooKeeper, monitoring and someone who knows what to do when a broker is unhappy. For tens of messages per second that is absurd, and we already run MySQL.

So [kfka](https://github.com/ethlo/kfka) keeps the part of Kafka I needed. Messages are rows in one table, and the client holds its own offset.

<svg viewBox="0 0 680 136" role="img" aria-label="Messages 45,608 to 45,613 in a row, with the client's last seen id at 45,610 and the following three delivered" style="width:100%;max-width:680px;height:auto;font-family:inherit">
<text x="0" y="16" font-size="13" text-anchor="start" fill="currentColor" opacity="0.75">One table, ordered by id. The client says what it saw last and gets the rest.</text>
<rect x="0" y="40" width="104" height="40" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-opacity="0.4"/>
<text x="52.0" y="65" font-size="14" text-anchor="middle" fill="currentColor" font-family="monospace">45,608</text>
<rect x="115" y="40" width="104" height="40" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-opacity="0.4"/>
<text x="167.0" y="65" font-size="14" text-anchor="middle" fill="currentColor" font-family="monospace">45,609</text>
<rect x="230" y="40" width="104" height="40" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-opacity="0.4"/>
<text x="282.0" y="65" font-size="14" text-anchor="middle" fill="currentColor" font-family="monospace">45,610</text>
<rect x="345" y="40" width="104" height="40" rx="4" fill="#4f8cff" fill-opacity="0.25" stroke="#4f8cff"/>
<text x="397.0" y="65" font-size="14" text-anchor="middle" fill="currentColor" font-family="monospace">45,611</text>
<rect x="460" y="40" width="104" height="40" rx="4" fill="#4f8cff" fill-opacity="0.25" stroke="#4f8cff"/>
<text x="512.0" y="65" font-size="14" text-anchor="middle" fill="currentColor" font-family="monospace">45,612</text>
<rect x="575" y="40" width="104" height="40" rx="4" fill="#4f8cff" fill-opacity="0.25" stroke="#4f8cff"/>
<text x="627.0" y="65" font-size="14" text-anchor="middle" fill="currentColor" font-family="monospace">45,613</text>
<line x1="282.0" y1="86" x2="282.0" y2="108" stroke="currentColor" stroke-opacity="0.6"/>
<text x="282.0" y="126" font-size="12" text-anchor="middle" fill="currentColor">lastSeenMessageId</text>
<line x1="345" y1="98" x2="679" y2="98" stroke="#4f8cff" stroke-width="2"/>
<text x="512.0" y="126" font-size="12" text-anchor="middle" fill="currentColor">delivered on reconnect, then live</text>
</svg>

```java
kfkaManager.addListener((msg) ->
{
    // handle message
},
new KfkaPredicate()
    .topic("chat")
    .lastSeenMessageId(45_610)       // next message will be 45,611
    .addPropertyMatch("userId", 123));
```

A new listener can also rewind, and get up to the last 100 messages before the live ones. That makes it a good fit behind server-sent events and websockets, where the browser drops the connection all the time and wants to continue where it was.

Since it is a table, you can filter on your own columns, here `userId`. Kafka cannot do that for you. Old messages are deleted on a timer after the retention time.

## What it is not

It is not Kafka. There are no partitions and no consumer groups, and the throughput is whatever one MySQL table gives you. If the volume grows by a factor of a hundred, this is the wrong tool and I will have to say so.

I still feel a bit like I am getting away with something.

*Update, November 2026: it never had to be replaced. It has carried every use we have had for it, also for the largest customers.*
