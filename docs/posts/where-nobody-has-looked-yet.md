---
date: 2018-02-05
categories:
  - Geo
---

# Where nobody has looked yet

I do not like software that tracks where people are. I have started on an app that does exactly that.

<!-- more -->

The idea came after a search for a missing person near where I grew up.

In a search, many people walk for many hours. Most of them are volunteers. They are sent out in directions, they come back and they are sent out again. What nobody has in the end is a picture of where they actually walked.

That picture matters for what it does not show. Ground that has been walked ten times does not need an eleventh. What you want to know is where nobody has been. The cold spots.

So the idea is simple. An app on the phone logs where you walk. Everyone in the same search shares a project, and the tracks become a heat map. The places with no heat are where to look closer. It would work for a person, a car or a boat.

<svg viewBox="0 0 680 250" role="img" aria-label="A grid of squares over a search area. Squares that searchers have walked through are shaded, darker for more passes. A cluster of unshaded squares is marked as a cold spot." style="width:100%;max-width:680px;height:auto;font-family:inherit">
<text x="0" y="16" font-size="13" fill="currentColor" opacity="0.75">A sketch of the idea. Shaded squares have been walked, darker for more passes.</text>
<g stroke="currentColor" stroke-opacity="0.25" fill="#4f8cff">
<rect x="0" y="30" width="40" height="40" fill-opacity="0.15"/><rect x="40" y="30" width="40" height="40" fill-opacity="0.3"/><rect x="80" y="30" width="40" height="40" fill-opacity="0.3"/><rect x="120" y="30" width="40" height="40" fill-opacity="0.15"/><rect x="160" y="30" width="40" height="40" fill-opacity="0.15"/><rect x="200" y="30" width="40" height="40" fill-opacity="0.3"/><rect x="240" y="30" width="40" height="40" fill-opacity="0.15"/><rect x="280" y="30" width="40" height="40" fill-opacity="0"/><rect x="320" y="30" width="40" height="40" fill-opacity="0.15"/><rect x="360" y="30" width="40" height="40" fill-opacity="0.15"/>
<rect x="0" y="70" width="40" height="40" fill-opacity="0.3"/><rect x="40" y="70" width="40" height="40" fill-opacity="0.6"/><rect x="80" y="70" width="40" height="40" fill-opacity="0.6"/><rect x="120" y="70" width="40" height="40" fill-opacity="0.3"/><rect x="160" y="70" width="40" height="40" fill-opacity="0.3"/><rect x="200" y="70" width="40" height="40" fill-opacity="0.15"/><rect x="240" y="70" width="40" height="40" fill-opacity="0"/><rect x="280" y="70" width="40" height="40" fill-opacity="0"/><rect x="320" y="70" width="40" height="40" fill-opacity="0"/><rect x="360" y="70" width="40" height="40" fill-opacity="0.15"/>
<rect x="0" y="110" width="40" height="40" fill-opacity="0.3"/><rect x="40" y="110" width="40" height="40" fill-opacity="0.8"/><rect x="80" y="110" width="40" height="40" fill-opacity="0.6"/><rect x="120" y="110" width="40" height="40" fill-opacity="0.6"/><rect x="160" y="110" width="40" height="40" fill-opacity="0.3"/><rect x="200" y="110" width="40" height="40" fill-opacity="0.15"/><rect x="240" y="110" width="40" height="40" fill-opacity="0"/><rect x="280" y="110" width="40" height="40" fill-opacity="0"/><rect x="320" y="110" width="40" height="40" fill-opacity="0.15"/><rect x="360" y="110" width="40" height="40" fill-opacity="0.3"/>
<rect x="0" y="150" width="40" height="40" fill-opacity="0.15"/><rect x="40" y="150" width="40" height="40" fill-opacity="0.3"/><rect x="80" y="150" width="40" height="40" fill-opacity="0.6"/><rect x="120" y="150" width="40" height="40" fill-opacity="0.8"/><rect x="160" y="150" width="40" height="40" fill-opacity="0.6"/><rect x="200" y="150" width="40" height="40" fill-opacity="0.3"/><rect x="240" y="150" width="40" height="40" fill-opacity="0.15"/><rect x="280" y="150" width="40" height="40" fill-opacity="0.15"/><rect x="320" y="150" width="40" height="40" fill-opacity="0.3"/><rect x="360" y="150" width="40" height="40" fill-opacity="0.3"/>
<rect x="0" y="190" width="40" height="40" fill-opacity="0"/><rect x="40" y="190" width="40" height="40" fill-opacity="0.15"/><rect x="80" y="190" width="40" height="40" fill-opacity="0.3"/><rect x="120" y="190" width="40" height="40" fill-opacity="0.3"/><rect x="160" y="190" width="40" height="40" fill-opacity="0.6"/><rect x="200" y="190" width="40" height="40" fill-opacity="0.6"/><rect x="240" y="190" width="40" height="40" fill-opacity="0.3"/><rect x="280" y="190" width="40" height="40" fill-opacity="0.3"/><rect x="320" y="190" width="40" height="40" fill-opacity="0.15"/><rect x="360" y="190" width="40" height="40" fill-opacity="0.15"/>
</g>
<rect x="240" y="70" width="80" height="80" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="6 4"/>
<line x1="320" y1="110" x2="440" y2="110" stroke="currentColor" stroke-opacity="0.6"/>
<text x="448" y="106" font-size="13" fill="currentColor">Nobody has been here.</text>
<text x="448" y="124" font-size="12" fill="currentColor" opacity="0.7">This is where to look closer.</text>
</svg>

## The part I do not like

It is a location tracker. It records where a person is, every few seconds, and sends it to a server. That is the kind of data I argue against collecting in every other setting.

So how do you build that without becoming what you dislike?

My answer so far is that nothing happens by itself. You join one search by scanning a barcode, and by scanning it you agree to share your location with that search. There is no account that follows you around. The tracking belongs to that project and has no reason to exist outside it.

Is that enough? I am not sure. A map of where volunteers walked is harmless in a search. The same data says where each of them was that night, and for how long. It should be coarse, and it should not live longer than the search does.

I have started on it. An Android app first, since that is what I know.

I hope it never gets used. I would still like it to exist.
