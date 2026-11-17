---
date: 2013-02-21
categories:
  - Java
  - JPA
share: assets/social/weaving-eclipselink-entities-at-build-time.png
description: "EclipseLink needs to change your entity classes to do lazy loading and change tracking properly. It can do that when the application starts. That sounds convenient. It has been a pain in the neck…"
---

# Weaving EclipseLink entities at build time

EclipseLink needs to change your entity classes to do lazy loading and change tracking properly. It can do that when the application starts. That sounds convenient. It has been a pain in the neck on every server I have set it up on.

<!-- more -->

Load-time weaving needs a Java agent on the JVM command line, or an application server whose class loader does it for you. So how your entities behave depends on how the server was started. Forget the agent on one machine and everything still works, only slower, and with lazy relations that are not lazy. Nothing fails, so nobody notices.

That is the worst kind of failure. The code I tested should be the code that runs, and a startup flag should not decide it.

Static weaving does the same change at build time. The classes in the jar are already woven, and the server needs nothing. EclipseLink ships a tool for it, but wiring it into a Maven build is more XML than it should be, and you have to keep a `persistence.xml` with every entity class listed by hand. The compiler already knows which classes are entities.

So I wrote a plugin for it:

```xml
<plugin>
    <groupId>com.ethlo.persistence.tools</groupId>
    <artifactId>eclipselink-maven-plugin</artifactId>
    <executions>
        <execution>
            <phase>process-classes</phase>
            <goals>
                <goal>weave</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

It finds the entity classes itself, so the `persistence.xml` does not need the list. A second goal, `modelgen`, generates the canonical metamodel without setting up an annotation processor.

It is a small thing. It should have been in EclipseLink. It is [on GitHub](https://github.com/ethlo/eclipselink-maven-plugin).

*Update, November 2026: I am still maintaining it, 13 years later. Most of the work has come from the outside moving, such as Spring Boot 3.1 and the Persistence 3.2 schema. It has never been a problem for me. The early adopters are the ones who get hit.*
