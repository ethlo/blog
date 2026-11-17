---
date: 2023-09-15
categories:
  - RC racing
share: assets/social/race-standings-from-lap-times-alone.png
description: "RC racing has timing that tells you one thing: when each car crossed the line. I wanted to know who was ahead in the middle of a lap, and you cannot know that. It turns out you can get close enough."
---

# Race standings from lap times alone

RC racing has timing that tells you one thing: when each car crossed the line. I wanted to know who was ahead in the middle of a lap, and you cannot know that. It turns out you can get close enough.

<!-- more -->

In real motorsport you get GPS and sector times. In RC there is a loop at start/finish, and a list of lap times per driver afterwards. I film my races, and a video of one car going round is not very interesting to anyone but me. With the standing and the gap to the car ahead on screen, it is.

So the question was how much you can tell from lap times alone.

More than I thought. Add up a driver's laps and you know exactly when they crossed the line each time. Do that for everyone and you know the order and the gaps at every crossing. Between the crossings you do not know anything, so there I assume each car spends the lap at an even pace. That is wrong in every single lap, since nobody drives evenly, and somebody always crashes.

It was surprisingly good anyway. The errors are inside one lap and they are corrected at the next crossing, so they never build up.

## Subtitles as an overlay

I did not want to write a video overlay. So [LapStats](https://github.com/ethlo/lapstats) writes an SRT file, the plain subtitle format, with the stats every time the driver passes start/finish. Any player can show it and YouTube takes it as it is. There is a JavaScript and HTML renderer as well, for when it should look better.

The data comes from MyRCM, the timing system used at the races.

[One with rendering](https://youtu.be/mcqrM_6t5hk), and [one with subtitles](https://youtu.be/wvPF6nZTDqk). I think it made the videos much more interesting to watch. That may say more about the videos.

<div style="position:relative;padding-bottom:56.25%;height:0;margin:1em 0"><iframe src="https://www.youtube-nocookie.com/embed/mcqrM_6t5hk" title="Race video with rendered standings" loading="lazy" allowfullscreen style="position:absolute;top:0;left:0;width:100%;height:100%;border:0"></iframe></div>
