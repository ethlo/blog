---
date: 2017-02-27
categories:
  - Java
  - Performance
---

# Why I wrote my own date-time parser

`1488153600`. Is that seconds or milliseconds? You find out when the date lands in 1970 or in the year 49,000. APIs send timestamps like that since a number is fast to parse. I wanted to see how much of that is real, so I wrote a parser this weekend.

<!-- more -->

It covers a very small part of date and time handling. I have not touched calendars or time zone rules. `java.time` does those, and does them well. What I wrote reads and writes one format, the one in RFC 3339:

```text
2017-12-27T23:45:32Z
2017-12-27T23:45:32.999Z
2017-12-27T18:45:32.999999-05:00
```

That is the format an API should use for a timestamp. It has been a standard since 2002, and still many do not. There are endless APIs with their own date formats, and there are the ones that gave up and send epoch numbers.

I understand the epoch people, and they are who this is for. A number is fast to read. A formatted timestamp goes through a general pattern parser that can handle any format you give it, and you pay for that on every field of every message. So you get a number that nobody can read in a log.

So the argument for the unreadable format is speed. I wanted to see how much of that is real.

The parser in [itu](https://github.com/ethlo/itu) knows the format in advance. The year is in the first four characters and the month in the next two after the dash. There is no pattern to interpret, so it reads digits at fixed positions and checks them.

<svg viewBox="0 0 680 172" role="img" aria-label="Timestamps parsed per second, in millions. Higher is better." style="width:100%;max-width:680px;height:auto;font-family:inherit">
<text x="0" y="16" font-size="13" fill="currentColor" opacity="0.75">Timestamps parsed per second, in millions. Higher is better.</text>
<text x="180" y="49" font-size="13" text-anchor="end" fill="currentColor">java.time (Java 8)</text>
<rect x="190" y="34" width="13.3" height="20" rx="3" fill="currentColor" opacity="0.35"/>
<text x="211.3" y="49" font-size="13" fill="currentColor">0.55</text>
<text x="180" y="79" font-size="13" text-anchor="end" fill="currentColor">java.util (Java 7)</text>
<rect x="190" y="64" width="18.1" height="20" rx="3" fill="currentColor" opacity="0.35"/>
<text x="216.1" y="79" font-size="13" fill="currentColor">0.74</text>
<text x="180" y="109" font-size="13" text-anchor="end" fill="currentColor">Apache FastDateFormat</text>
<rect x="190" y="94" width="26.3" height="20" rx="3" fill="currentColor" opacity="0.35"/>
<text x="224.3" y="109" font-size="13" fill="currentColor">1.08</text>
<text x="180" y="139" font-size="13" text-anchor="end" fill="currentColor">itu</text>
<rect x="190" y="124" width="380" height="20" rx="3" fill="#4f8cff"/>
<text x="578" y="139" font-size="13" fill="currentColor">15.6</text>
</svg>

Formatting went from about 2 million per second to 12.7 million.

I do not fully trust these numbers. It is a loop with a timer around it, on my machine, and I wrote both the parser and the test. The two older ones were also given a single hard-coded format, which is kinder to them than real use. But a factor of 28 over `java.time` does not come from measuring badly.

So the speed argument for epoch numbers is mostly an argument about one slow parser. With that gone, you can send a timestamp that a person can read.

The first rule of date and time handling is that you do not write your own, and I still agree with it. This is one format. `java.time` does the rest.
