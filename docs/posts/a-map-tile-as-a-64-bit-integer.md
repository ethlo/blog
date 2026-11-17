---
date: 2018-05-15
categories:
  - Java
  - Geo
---

# A map tile as a 64-bit integer

I want to know where users are, and I do not want to know where users are.

<!-- more -->

Both are true. Aggregates by area are useful: how many, where, when. An exact position per user is a liability. It is sensitive, and once it is stored it has to be protected for as long as it exists.

A quadkey solves most of this. It comes from the Bing Maps tile system. The world is one square, split in four, and each of those in four again. Every split adds one digit from 0 to 3, so a position at zoom level 18 is a string of 18 digits:

<svg viewBox="0 0 680 290" role="img" aria-label="A square split in four three times, with tile 213 marked" style="width:100%;max-width:680px;height:auto;font-family:inherit">
<text x="0" y="16" font-size="13" text-anchor="start" fill="currentColor" opacity="0.75">Each split adds one digit. The tile 213 is inside 21, which is inside 2.</text>
<rect x="20" y="36" width="120" height="120" fill="none" stroke="currentColor" stroke-opacity="0.5"/>
<text x="80.0" y="103.0" font-size="20" text-anchor="middle" fill="currentColor" opacity="0.85">0</text>
<rect x="140" y="36" width="120" height="120" fill="none" stroke="currentColor" stroke-opacity="0.5"/>
<text x="200.0" y="103.0" font-size="20" text-anchor="middle" fill="currentColor" opacity="0.85">1</text>
<rect x="20" y="156" width="120" height="120" fill="#4f8cff" fill-opacity="0.25" stroke="currentColor" stroke-opacity="0.5"/>
<rect x="140" y="156" width="120" height="120" fill="none" stroke="currentColor" stroke-opacity="0.5"/>
<text x="200.0" y="223.0" font-size="20" text-anchor="middle" fill="currentColor" opacity="0.85">3</text>
<rect x="20" y="156" width="60" height="60" fill="none" stroke="currentColor" stroke-opacity="0.5"/>
<text x="50.0" y="190.9" font-size="14" text-anchor="middle" fill="currentColor" opacity="0.85">20</text>
<rect x="80" y="156" width="60" height="60" fill="#4f8cff" fill-opacity="0.25" stroke="currentColor" stroke-opacity="0.5"/>
<rect x="20" y="216" width="60" height="60" fill="none" stroke="currentColor" stroke-opacity="0.5"/>
<text x="50.0" y="250.9" font-size="14" text-anchor="middle" fill="currentColor" opacity="0.85">22</text>
<rect x="80" y="216" width="60" height="60" fill="none" stroke="currentColor" stroke-opacity="0.5"/>
<text x="110.0" y="250.9" font-size="14" text-anchor="middle" fill="currentColor" opacity="0.85">23</text>
<rect x="80" y="156" width="30" height="30" fill="none" stroke="currentColor" stroke-opacity="0.5"/>
<rect x="110" y="156" width="30" height="30" fill="none" stroke="currentColor" stroke-opacity="0.5"/>
<rect x="80" y="186" width="30" height="30" fill="none" stroke="currentColor" stroke-opacity="0.5"/>
<rect x="110" y="186" width="30" height="30" fill="none" stroke="currentColor" stroke-opacity="0.5"/>
<rect x="110" y="186" width="30" height="30" fill="#4f8cff"/>
<text x="320" y="70" font-size="12" text-anchor="start" fill="currentColor" opacity="0.6">Key</text>
<text x="470" y="70" font-size="12" text-anchor="start" fill="currentColor" opacity="0.6">As bits</text>
<text x="320" y="100" font-size="18" text-anchor="start" fill="currentColor" font-family="monospace">2</text>
<text x="470" y="100" font-size="18" text-anchor="start" fill="currentColor" font-family="monospace">10</text>
<text x="320" y="134" font-size="18" text-anchor="start" fill="currentColor" font-family="monospace">21</text>
<text x="470" y="134" font-size="18" text-anchor="start" fill="currentColor" font-family="monospace">10 01</text>
<text x="320" y="168" font-size="18" text-anchor="start" fill="currentColor" font-family="monospace">213</text>
<text x="470" y="168" font-size="18" text-anchor="start" fill="currentColor" font-family="monospace">10 01 11</text>
<line x1="140" y1="201.0" x2="308" y2="162" stroke="#4f8cff" stroke-width="1.5"/>
<text x="320" y="214" font-size="12" text-anchor="start" fill="currentColor" opacity="0.75">Two bits per digit. A shorter key is a larger square,</text>
<text x="320" y="232" font-size="12" text-anchor="start" fill="currentColor" opacity="0.75">and a prefix of every key inside it.</text>
</svg>

```java
final Coordinate c = new Coordinate(40.757678, -73.969558);
QuadKey qk = new QuadKey(c, 18);     // about 0.6 m per pixel
qk.getAsString();                    // "032010110132031203"
qk.getAsLong();                      // 15104861027
```

Two things follow from how it is built.

A tile's key is a prefix of every tile inside it. So "is this point inside that square" is a prefix check, and on the integer form it is plain arithmetic. That makes it a good database index. A range scan on one indexed column finds everything in an area, with no spatial extension.

```java
QuadKey qk = new QuadKey(c1, 16);
qk.contains(c2);                     // true
```

And the precision is something you choose. Cut the key at a lower zoom level and the position becomes a square of a few hundred meters, or a few kilometers. You store the square. The exact position is never written down, so it cannot leak later.

That is the part I like. It is not anonymisation, and I will not call it that. A square with one person in it is still that person. But it lets me decide the resolution up front, and keep what the aggregate needs and no more.

[jquad](https://github.com/ethlo/jquad) is a small Java library for this. Each digit takes 2 bits, so a key fits in a 64-bit integer with room to spare.
