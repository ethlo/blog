---
date: 2015-07-28
categories:
  - Home
share: assets/social/a-screen-saver-for-a-chromecast.png
description: "I have a plasma TV and a Chromecast, and they do not like each other."
---

# A screen saver for a Chromecast, to save a plasma TV

I have a plasma TV and a Chromecast, and they do not like each other.

<!-- more -->

When nothing is playing, the Chromecast goes to Backdrop mode. It shows nice photos, and on top of them a clock and some text that never move. A plasma is not very happy about non-moving images over time. The same goes for a paused programme that someone forgot.

There is no setting to turn it off. For a device that is made to sit on a TV all day, that is a strange thing to leave out. So I wrote a small Python script that watches the Chromecast. When it has been in Backdrop, or idle or paused, for too long, the script starts the default player with something random from a list of media URLs. When someone starts to watch something, it gets out of the way.

```text
21:35:23 - Dicovered chromecast devices: ['LivingRoom']
21:35:58 - Discovered idle/paused player
21:36:03 - Discovered active player, resetting idle timer
21:40:43 - Discovered idle/paused player
21:41:43 - Current application has been idle too long, starting screensaver
```

It works with the default media player, NRK TV and TV 2 Sumo. It does not work with Netflix or HBO Nordic. Their media status cannot be read, so the script cannot tell a paused film from a playing one, and I would rather have burn-in than a screen saver in the middle of a film.

It is [castsaver](https://github.com/ethlo/castsaver), built on PyChromecast, which did all the hard work. Not the cleanest code I have written. I spent an evening on a script to protect a TV from a 35 dollar gadget, and I am fine with that.

*Update, November 2026: it ran for a couple of years.*
