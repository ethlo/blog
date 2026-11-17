---
date: 2003-05-02
categories:
  - Archive
share: assets/social/sleepy-news-system.png
description: "A news system in Python, built on XML files instead of a database. Project in the course Programming for the web, spring 2003."
---

# Project: SleePy

A news system in Python, built on XML files instead of a database. Project in the course Programming for the web, spring 2003.

<!-- more -->

## Concept (29.01.2003)

I want to make a system that makes it possible to post news, articles and so on. In other words what is needed to run a news site for any topic. Since there are systems for this already, like newspro which I have used myself, I will try to make a system for importing these into my own system, and store them as xml.

Further, a system for authentication will be needed, so that only admins/superusers can post/edit news, articles or similar. Since I don't know exactly how much time this will take, it is hard to say what may get added or maybe removed in favour of something else.

The idea is that the user of the system does not need to know how to code, write html or have any technical knowledge about the Internet.

The system will be built on flat files, which means XML. I could have built it on a database too, but where is the challenge in that!? =] By using flat files you can get away with cheaper web hosting, and in smaller systems like this one, performance will not suffer enough to become a problem.

Other than that there is not much to say. It may not be the most original project, but it is something I need for my own use, so it could be interesting to see how far I manage to get...

## Detailed description (26.03.2003)

### The news format

To try to stay on good terms with the standards, the standard set by the dublincore project is followed as far as possible. They define only 15 tags that are supposed to cover what is needed to handle/maintain metadata. Since XML is aiming to be/already is the standard for exchanging information between different systems, the point is to follow the standards that have been set.

For all the details see: <http://dublincore.org/>

### Functionality

This is functionality that is coming/already implemented:

NNTP news support:

- Fetch news from an NNTP server
- The group to fetch from can be chosen freely, but has to follow the same standard as NTB's newsgroups.
- Present headlines/headlines with lead/the whole news item.

General functions for news:

- Search by keyword
- Get news by date
- Post news
- Edit news
- Delete news
- Post comments on news
- News is stored in categories per day.

Framework/settings:

- Almost all of the site will be template based. These templates will be built on XSLT/XHTML.
- Python will be used to do the transformations.
- Settings are stored as a separate xml document and can be edited by hand if wanted. Hopefully there will be time to finish the planned web interface for settings.

Users:

- There are 3 types of users:
    - guest - Can only post comments. Can become members themselves.
    - user - the above, plus being able to post news and edit their own posted news. Created by admin.
    - admin - the above, plus making changes to settings. Created by admin.
- Users are authenticated with cookies if they have logged in before.

Storing data:

- News data is stored in the same format as the news posted on the site, namely XML. The news is stored in its own file, one per day, e.g. '030325_ntb.utenriks.nytt.xml', or '030325_development.xml'.
- Settings are, as mentioned above, stored in an XML file.

Presentation:

- The pages are built as XHTML pages following the strictest standard, XHTML 1.1 Strict.
- Styles are maintained with CSS(2) and the structure of the pages with the template solution mentioned above.

Other:

- This project will try to do what can be done to keep the performance of the system up. A bit of 'intelligence' will probably be added to the system for fetching data from the NNTP server and so on, to reduce the load on the server..
- No database will be used, to keep the cost of web hosting low.

## The code

The CGI interface to the web is the script slee.py. This script receives all input from the user through the web pages. That means all calls to code go through this script.
It mostly consists of checking input, and checking that the user has access to the requested information, or to run a command.

```python
#!c:\python22\python.exe

#############################################################
#                                                           #
#   Part of SleePy news posting system                      #
#   Author: Morten Haraldsen 2003. All rights reserved.     #
#                                                           #
#   Description: This script is the cgi frontend,           #
#   and the only script that interferes with the user       #
#                                                           #
#############################################################

# Standard
import cgi, cgitb, string, os, time, re
from time import strftime

# My own modules
import sleepysettings, msg, login, sleepytemplate, sleepycounter, sleepycomments, sleepynews
```
