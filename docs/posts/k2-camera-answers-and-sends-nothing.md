---
date: 2026-11-18
draft: true
categories:
  - 3D printing
share: assets/social/k2-camera-answers-and-sends-nothing.png
description: "The Creality K2 Pro is good hardware with cheap software on it. The camera is where I ran into that."
---

# The K2 camera answers every offer and then sends nothing

The Creality K2 Pro is good hardware with cheap software on it. The camera is where I ran into that.

<!-- more -->

I wanted the camera in my own print page, without the Creality cloud. The printer has a local stream over WebRTC, and the signalling is as simple as it gets: one POST with the offer as base64 JSON, and the answer comes back the same way. None of it is documented.

On 1 November I had an answer, a negotiated H264 track and no frames. ICE completed on my side, and the DTLS ClientHello got no reply. Chrome and aiortc failed the same way. Meanwhile Creality's phone app showed video through the cloud.

I tried the token-protected endpoint on 443, `sendrecv` instead of `recvonly`, a LAN-only candidate, and waiting 170 seconds in case the start was slow. Every attempt got a 200 and a valid answer, and then nothing. The printer never says no.

So I parked it behind a flag and blamed the firmware. That was wrong, but only half wrong.

## The stream was there all along

Creality Print for Linux shows the local video on the same firmware. So my offer was the problem. I captured its traffic with tcpdump and compared.

The printer wants the ICE candidates as the last lines of the SDP, after `ice-ufrag` and `ice-pwd`, numbered and with a generation. Browsers and aiortc put them earlier. That is valid, and the printer then never learns where to send. This is what a browser sends:

```text
m=video 9 UDP/TLS/RTP/SAVPF 96
c=IN IP4 0.0.0.0
a=candidate:1 1 udp 2113937151 3f6a.local 51234 typ host
a=ice-ufrag:Xk2p
a=ice-pwd:...
a=rtpmap:96 H264/90000
```

And this is what the printer reads:

```text
m=video 9 UDP/TLS/RTP/SAVPF 96
c=IN IP4 0.0.0.0
a=ice-ufrag:Xk2p
a=ice-pwd:...
a=rtpmap:96 H264/90000
a=candidate:0 1 udp 2113937151 192.0.2.10 51234 typ host generation 0
```

It also wants RSA cipher suites in the DTLS handshake, since its certificate is RSA. aiortc only offers ECDSA, so the handshake dies with alert 40. And it cannot look up the `something.local` names browsers hide their address behind, so I swap in the address the request came from.

The whole rewrite of the offer is this:

```python
def fix_offer(sdp: str, client_ip: str | None = None) -> str:
    lines = sdp.splitlines()
    candidates = [l for l in lines if l.startswith("a=candidate:")]
    rest = [l for l in lines if not l.startswith(("a=candidate:", "a=end-of-candidates"))]
    for i, line in enumerate(candidates):
        line = re.sub(r"^a=candidate:\S+", f"a=candidate:{i}", line)
        if client_ip:
            line = re.sub(r" \S+\.local (\d+ typ host)", rf" {client_ip} \1", line)
        rest.append(line if " generation " in line else line + " generation 0")
    return "\r\n".join(rest) + "\r\n"
```

The answer needs fixing too. The printer answers with a payload type it was never offered, and splits the H264 `fmtp` over two lines. aiortc keeps the last line, loses `packetization-mode=1` and finds no common codec.

One part was on my side. aiortc 1.10.1 never decoded the stream. 1.16.0 does, and the first frame arrives after about 6 seconds.

## Cheap software

This looks like a WebRTC stack that was tested against one client, their own, and shipped when that worked. It reads the SDP in the order their client writes it. It is not a parser so much as an expectation.

I can live with that. What kept it parked for two weeks is the 200. An offer the printer cannot use gets the same friendly answer as one it can, so every wrong guess looks like a right one. One error message would have made this an evening.

The annoying part is that the camera is fine, and so is the rest of the machine. Somebody did careful work on the hardware. Then the software got whatever time was left.

Tested on one K2 Pro on firmware 1.1.8.3. Not on the K1 or the K2 Plus. The direct path only works where the browser can reach the printer, so through a tunnel I relay the frames as MJPEG at about 5 fps instead.
