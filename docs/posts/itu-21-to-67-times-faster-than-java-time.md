---
date: 2026-09-23
categories:
  - Java
  - Performance
---

# Parsing ISO-8601 21 to 67 times faster than java.time

In September 2026 I spent three days making a date parser faster. It already took less than a microsecond.

<!-- more -->

ITU is my library for the timestamps machines send each other, RFC 3339 and the ISO-8601 subset around it. It has existed since 2017.

After the three days, 1.16.0 parses a timestamp in 18 to 28 ns. `java.time` needs 542 to 577 ns for the same input on the same JDK. That is 21 to 30 times faster, and lenient parsing ends up 46 to 67 times faster. Nothing is allocated when you parse from a `char[]` or `byte[]`.

<svg viewBox="0 0 680 342" role="img" aria-label="Slowest input per operation, ns/op. Lower is better." style="width:100%;max-width:680px;height:auto;font-family:inherit">
<text x="0" y="16" font-size="13" fill="currentColor" opacity="0.75">Slowest input per operation, ns/op. Lower is better.</text>
<text x="180" y="49" font-size="13" text-anchor="end" fill="currentColor">parse, ITU</text>
<rect x="190" y="34" width="13.5" height="20" rx="3" fill="#4f8cff"/>
<text x="211.5" y="49" font-size="13" fill="currentColor">28 ns</text>
<text x="180" y="79" font-size="13" text-anchor="end" fill="currentColor">parse, JDK</text>
<rect x="190" y="64" width="278.2" height="20" rx="3" fill="currentColor" opacity="0.35"/>
<text x="476.2" y="79" font-size="13" fill="currentColor">577 ns</text>
<text x="180" y="109" font-size="13" text-anchor="end" fill="currentColor">parseLenient, ITU</text>
<rect x="190" y="94" width="8.2" height="20" rx="3" fill="#4f8cff"/>
<text x="206.2" y="109" font-size="13" fill="currentColor">17 ns</text>
<text x="180" y="139" font-size="13" text-anchor="end" fill="currentColor">parseLenient, JDK</text>
<rect x="190" y="124" width="380.0" height="20" rx="3" fill="currentColor" opacity="0.35"/>
<text x="578.0" y="139" font-size="13" fill="currentColor">788 ns</text>
<text x="180" y="169" font-size="13" text-anchor="end" fill="currentColor">formatSeconds, ITU</text>
<rect x="190" y="154" width="7.7" height="20" rx="3" fill="#4f8cff"/>
<text x="205.7" y="169" font-size="13" fill="currentColor">16 ns</text>
<text x="180" y="199" font-size="13" text-anchor="end" fill="currentColor">formatSeconds, JDK</text>
<rect x="190" y="184" width="48.2" height="20" rx="3" fill="currentColor" opacity="0.35"/>
<text x="246.2" y="199" font-size="13" fill="currentColor">100 ns</text>
<text x="180" y="229" font-size="13" text-anchor="end" fill="currentColor">formatNanos, ITU</text>
<rect x="190" y="214" width="15.9" height="20" rx="3" fill="#4f8cff"/>
<text x="213.9" y="229" font-size="13" fill="currentColor">33 ns</text>
<text x="180" y="259" font-size="13" text-anchor="end" fill="currentColor">formatNanos, JDK</text>
<rect x="190" y="244" width="55.5" height="20" rx="3" fill="currentColor" opacity="0.35"/>
<text x="253.5" y="259" font-size="13" fill="currentColor">115 ns</text>
<text x="180" y="289" font-size="13" text-anchor="end" fill="currentColor">parseDuration, ITU</text>
<rect x="190" y="274" width="25.1" height="20" rx="3" fill="#4f8cff"/>
<text x="223.1" y="289" font-size="13" fill="currentColor">52 ns</text>
<text x="180" y="319" font-size="13" text-anchor="end" fill="currentColor">parseDuration, JDK</text>
<rect x="190" y="304" width="119.1" height="20" rx="3" fill="currentColor" opacity="0.35"/>
<text x="317.1" y="319" font-size="13" fill="currentColor">247 ns</text>
</svg>

Measured with JMH on an i9-13900H laptop on JDK 25.0.4. The [full report](https://ethlo.github.io/date-time-wars/) has every input with error bars.

## Does it matter?

For one timestamp, no, it does not. Half a microsecond is nothing.

I tell people to measure before they optimise, and to stop when it is fast enough. By that rule I should have stopped years ago. I did not, since I like this kind of work, and I will not pretend the reason is better than that.

There is a real case too. A service that parses several timestamps per request, or a phone that parses thousands in one sync, pays that half microsecond every time. But that is the excuse and not the reason.

## Throwing away the numbers

I have tuned this parser several times over the years. Each time I measured, kept what helped and threw away the numbers.

So I could not say what I had already tried. This time I kept a log of every attempt with its numbers, kept or not. It has a section called "Dead ends, do not retry without a new reason". Writing fields into the buffer as soon as they were parsed is in there. It looked obvious and gained nothing.

For someone who goes on about measuring, that took a long time to learn.

## How it got fast

No single trick. The parser knows the format, so it reads digits at fixed positions instead of asking a formatter what comes next. An input of 19 characters or more takes a path with no per-field length checks. Dates are converted to day counts with Ben Joffe's algorithm. When formatting, digits are written two at a time from a table, straight into the caller's buffer.

Validation is the odd one. `isValid` on bad input is hundreds of times faster than the JDK, and it is not due to anything clever. The JDK builds an exception with a stack trace to tell you no. ITU returns false.

## Where it loses

Formatting a duration is on par with the JDK, and slower for some inputs. It is in the report with the rest.

ITU also does less. No locales, no patterns, no calendars other than ISO. If you need those, this is not the library. And `Instant.parse`, the fastest built-in path, is in the benchmark too, so the comparison is not against the slowest thing I could find.

The benchmarks are in [date-time-wars](https://github.com/ethlo/date-time-wars). Run them on your own hardware before you believe mine.
