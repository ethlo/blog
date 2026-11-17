---
date: 2026-11-12
categories:
  - Homelab
share: assets/social/the-home-network-as-a-yaml-file.png
description: "I have replaced the router and the core switch at home, and neither was set up by hand. The whole network is now one YAML file and an Ansible playbook."
---

# The home network as a YAML file

I have replaced the router and the core switch at home, and neither was set up by hand. The whole network is now one YAML file and an Ansible playbook.

<!-- more -->

The old setup was a consumer mesh router doing everything, and a switch that could only be set up by clicking in a web page. It worked. I also had no idea what I had clicked in it over the years, and which of those clicks the house depended on.

That is what bothered me. I had already put the home server in a repository, so it can be rebuilt from nothing. The network under it was the one part that only existed as settings inside a box.

So there is a new router and a new core switch, both MikroTik, and neither is set up by hand. One file describes the network: the devices, their fixed leases and names, and the rules. An Ansible playbook applies it to both boxes over their API.

```bash
ansible-playbook network.yml --check --diff     # dry run
ansible-playbook network.yml --diff
```

<svg viewBox="0 0 680 190" role="img" aria-label="The ISP box connects to the router. The router feeds the cameras over PoE and the core switch. The core switch connects the home server at 10 gigabit and the Wi-Fi access point." style="width:100%;max-width:680px;height:auto;font-family:inherit">
<g fill="none" stroke="currentColor" stroke-opacity="0.5">
<rect x="0" y="70" width="110" height="44" rx="5"/>
<rect x="390" y="12" width="140" height="44" rx="5"/>
<rect x="390" y="134" width="140" height="44" rx="5"/>
<rect x="560" y="70" width="120" height="44" rx="5"/>
<line x1="110" y1="92" x2="170" y2="92"/><line x1="290" y1="92" x2="390" y2="92"/>
<line x1="460" y1="70" x2="460" y2="56"/><line x1="460" y1="114" x2="460" y2="134"/>
<line x1="230" y1="114" x2="230" y2="156"/>
</g>
<rect x="170" y="70" width="120" height="44" rx="5" fill="#4f8cff" fill-opacity="0.25" stroke="#4f8cff"/>
<rect x="390" y="70" width="140" height="44" rx="5" fill="#4f8cff" fill-opacity="0.25" stroke="#4f8cff"/>
<line x1="530" y1="92" x2="560" y2="92" stroke="currentColor" stroke-opacity="0.5"/>
<g font-size="13" fill="currentColor" text-anchor="middle">
<text x="55" y="97">ISP box</text><text x="230" y="97">Router</text><text x="460" y="97">Core switch</text>
<text x="460" y="39">Home server, 10G</text><text x="460" y="161">Wi-Fi access point</text><text x="620" y="97">The rest</text>
<text x="230" y="174">Cameras, PoE</text>
</g>
<text x="340" y="84" font-size="11" text-anchor="middle" fill="currentColor" opacity="0.6">trunk</text>
</svg>

*The two blue boxes are set up from the file.*

## The switch-over

This was the part I was nervous about. You cannot test a router change from behind the router you are changing.

So the new router first ran in a staging mode, on its factory network, next to the old one. I could plug a laptop into it and check that it gave out addresses, answered DNS and reached the internet, while the house still ran on the old router. The switch-over was then one variable changed from `staging` to `final`, a playbook run, and some cables moved in the right order. The plan allowed for 15 to 30 minutes without internet.

What broke? Nothing really. The game server did not answer from inside the house afterwards, and that was all.

Two things I would tell someone doing the same. Give the old router a fixed address of its own when it becomes an access point, so it can never take the new router's address. And keep a way in that does not depend on the config being right. Each box still answers on its factory address from a cable until I remove that on purpose.

## Is it over-engineering?

For a network with one router, probably yes. I would say so if someone showed it to me at work. Nobody needs a dry run to add a DHCP lease.

But I can read the whole network in one file now, and see in a diff what changed and when. The next time something stops working, there is a file and a history to look at, where before there was only my memory.
