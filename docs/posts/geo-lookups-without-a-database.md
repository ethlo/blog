---
date: 2017-10-24
categories:
  - Java
  - Geo
share: assets/social/geo-lookups-without-a-database.png
description: "In May I imported the world into MySQL. In October I deleted the database, and the library got simpler."
---

# Geo lookups without a database

In May I imported the world into MySQL. In October I deleted the database, and the library got simpler.

<!-- more -->

The data is the world. GeoNames has the places, with their names, coordinates and the hierarchy from continent down to town. GeoLite2 maps IP ranges to locations. I wanted one library that answers the simple questions: where is this IP, what is near this point, is this town inside that county.

I put it in a database, as I do with data. Import the files, add spatial indexes, write queries. It worked, and it had all the usual company. A schema, an import that took its time, encoding trouble on the build server, and a database that had to be running before a single test could.

Then I looked at what the data is. It changes when I download a new file, and at no other time. Nobody writes to it. There are no transactions and no concurrent updates, and nothing has to survive a crash, since the source files are still there.

Everything a database is good at, I was not using. I was using it as a slow way to read a file.

The commit log from October tells the rest:

```text
2017-10-13 Load IP and locations into memory for maximum performance
2017-10-16 All geometry is removed from DB, and using inmem+file instead
2017-10-22 Rempved all SQL databases and use pure in.memory structures and files
2017-10-23 Now writing a dedicated MBR file on data import to make loading/startup a lot faster
```

[geodata](https://github.com/ethlo/geodata) now reads its data from files into structures made for each question. IP ranges are sorted, so a lookup is a binary search. For "what is near this point", each boundary has a bounding rectangle, and those are checked before any real geometry is touched. The whole thing is a few hundred megabytes.

## It turned into something else

I should admit that this stopped being about geo data somewhere along the way. Once the database was gone, every lookup became a question of which structure fits, and I spent more time on that than the library needed.

For deployment it paid off. There is nothing to install and nothing to migrate.

A database is still the right answer when the data changes. This data does not.
