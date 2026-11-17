---
date: 2014-10-28
categories:
  - Archive
share: assets/social/gtx-970-overclocking.png
description: "This page was created to try to distill the information from more than 5,000 forum posts."
---

# NVIDIA GTX 970 overclocking

This page was created to try to distill the information from more than 5,000 forum posts.

<!-- more -->

!!! warning

    The information/software/data here is for informational purposes only and any and all actions are on your very own risk! Playing with software tweaks and BIOS updates may brick your card and certainly void your warranty. You have been warned.

In general the BIOS can now be flashed without signature-check limitations that hindered the flashing of bioses initially. Users are reporting various luck of running a custom bios, but the consensus seems to be that the gain is very minor at this point. Some people lucky in the silicon lottery have reported speeds close to 1600 MHz core and 8100 MHz memory, but this seems very rare. The average seems to lie between ~1400 MHz to ~1550 MHz.

## Contenders

| Card | Bioses | Power limit | Voltage | Fan speed | Description |
|---|---|---|---|---|---|
| Gigabyte G1 Gaming | [Original](http://www.techpowerup.com/vgabios/index.php?architecture=NVIDIA&manufacturer=Gigabyte&model=GTX+970&interface=&memType=&memSize=&did=10de-13c2--) | 380W | 1.31V (bios modded) | 1100 RPM+ to 100% | Currently deemed the best overclocker, **even though no ability to overvolt yet**. Seems that overvolting is causing instability and driver crashes. [[1]](http://www.overclock.net/t/1514085/official-nvidia-gtx-970-owners-club/5040#post_23054751) |
| MSI Gaming 4G | [Original](http://www.techpowerup.com/vgabios/index.php?architecture=NVIDIA&manufacturer=MSI&model=GTX+970&interface=&memType=&memSize=&did=10de-13c2--), newvoltsMSI.rom - Gives higher voltage (but not power limit)[?] | 220W | 1.31V (bios modded) | 0% to 100% | Very good overclocker, possibly held back by the power limit that seemingly cannot be raised yet. Running with max voltage (1.31V) yielded a weak 20 MHz more in stable overclock. |

## Software

| Name | Size | Version | Release date | Description |
|---|---|---|---|---|
| nvflash | 792 KB | 5.190.0.1 | N/A | See below |
| [GPU-Z](http://www.techpowerup.com/gpuz/) | N/A | N/A | N/A | Useful for extracting current BIOS and reading GPU information in real-time. Has nice OSD |
| Kepler Bios Tweaker | N/A | 1.27 | N/A | Editor for Kepler BIOS (NVIDIA 7xx-series cards) |
| Maxwell Bios Tweaker | 102KB | 1.31 | 2014-10-26 | Maxwell II BIOS (NVIDIA 9xx-series cards). Changelog: 1.31 - Improved Fan-Control and fixed Voltage Settings. 1.30 - Initial public release(?) |

nvflash: First uninstall your video driver, then run:

```
nvflash -6 [file.rom]
```

If you have more than one card and want to flash a specific one:

```
nvflash --list
```

Look at the index number (0, 1, 2, 3) and then

```
nvflash -6 --index
```

## SLI different voltage trick

When running in SLI it seems that one card will be running with much lower voltage. To fix this one can offset the core clock with about +20MHz to +35MHz on the card that runs with the highest voltage.

## Measuring voltage

There has been several users reporting that the reported voltage by CPU-Z or other software is not giving correct results.

- [overclock.net, user 'Doza'](http://www.overclock.net/t/1514085/official-nvidia-gtx-970-owners-club/5000#post_23053495)
- [overclock.net, user 'Edkiefer'](http://www.overclock.net/t/1517316/extract-and-flash-gtx-970-and-980-firmware-gpuz-test-build-and-new-nvflash-5-190/300#post_23053840)

If you have a digital multimeter you can also measure the voltage here yourself. Connect the black probe to any metal on your case and the red probe to one of the two solder points, not sure if it's the upper or lower one. Don't cause a short circuit by touching both at the same time with your probe.

## "Dead card"

Try to switch from UEFI to Legacy in your mobo bios for the PCIe lane. If that doesn't work well RMA time I guess. [[1]](http://www.overclock.net/t/1514085/official-nvidia-gtx-970-owners-club/5060#post_23055194)

## Testing

Simple to use software, making it easy to repeat and compare results between runs is necessary when establishing stability and performance.

- [3DMark](http://www.futuremark.com/benchmarks/3dmark) - Firestrike / Firestrike extreme. Very stressful test that usually will discover if something is off
- [Valley benchmark](https://unigine.com/products/valley/) - Nice and simple test that can run in endless loop

## Links

- [Overclock.net - [Official] NVIDIA GTX 970 Owner's Club](http://www.overclock.net/t/1514085/official-nvidia-gtx-970-owners-club)
- [Overclock.net - Extract and Flash GTX 970 and 980 Firmware](http://www.overclock.net/t/1517316/extract-and-flash-gtx-970-and-980-firmware-gpuz-test-build-and-new-nvflash-5-190)
