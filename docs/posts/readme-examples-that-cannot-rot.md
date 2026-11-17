---
date: 2024-02-12
categories:
  - Java
---

# README examples that cannot rot

I change my APIs a lot. I like to work on the API and the implementation at the same time, and move things until they feel right. The README is what pays for that.

<!-- more -->

An example in a README is code that no compiler sees. Rename a method and the tests fail, the build fails, and the README says nothing. It keeps showing the old name to everyone who visits, and those are the people who know the least about the library and trust the README the most.

I have shipped wrong examples that way. The honest fix is to be more careful, and I know myself well enough to not rely on that.

So the examples are now tests. They live in a package under `src/test/java`, they compile and they run. [source-extractor-maven-plugin](https://github.com/ethlo/source-extractor-maven-plugin) reads those files at build time, takes the body of each method, and puts it into the README through a template.

```java
/**
 * The simplest and fastest way to parse an RFC-3339 timestamp by far!
 */
@Test
void parseRfc3339()
{
    final String text = "2012-12-27T19:07:22.123456789-03:00";
    final OffsetDateTime dateTime = ITU.parseDateTime(text);
    assertThat(dateTime.toString()).isEqualTo(text);
}
```

The method name becomes the heading, the Javadoc becomes the description, and the body becomes the code block, with a link to the line in the source. The README in the repository root is generated, and the one I edit is a template.

It took three days from the first commit to a release, and [itu](https://github.com/ethlo/itu) had its README rebuilt from it the same week.

## What it does to the examples

There is a cost. An example written as a test looks like a test. It has assertions in it, and it shows what the library returns by asserting it, where a hand-written example would have a comment. Some of mine read a bit stiff now.

It is also opinionated. It does one thing, in the way I wanted it, with Maven.

I will take stiff and correct.
