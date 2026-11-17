---
date: 2026-11-17
categories:
  - 3D printing
share: assets/social/a-k2-firmware-update-deletes-your-config-and-your-root.png
description: "I rooted my printer, changed its config, and then got annoyed when a firmware update did not respect my changes."
---

# A K2 firmware update deletes your config and your root

I rooted my printer, changed its config, and then got annoyed when a firmware update did not respect my changes.

<!-- more -->

That is not a fair complaint, and I know it. The update was still sloppy.

On 17 November I updated the K2 Pro to 1.1.8.3. Afterwards the printer sat in an error state and would not print. Klipper said:

```text
Include file printdrop.cfg does not exist
```

The update had reset the factory config files and deleted the one file that was mine. But it kept `printer.cfg`, and that file still had my line in it:

```text
[include printdrop.cfg]
```

So it removed the file and kept the reference to it. Either choice alone would have been fine. Keep both and nothing breaks. Remove both and I lose my macros but the printer starts. Half of each gives a printer that halts at startup.

Root was gone too. The SSH host key had changed and my key was refused.

## The fix

The Moonraker file API still works after the update, without root. So recovery is one upload of the missing file to the config folder, and then `FIRMWARE_RESTART`. A plain `RESTART` is not enough.

Klipper came back as ready, and the calibration from 1 November was still there, since it lives in `printer.cfg`.

## What I do now

I assume every update will do the same. The config file lives in my own repo and not only on the printer, and putting it back takes a minute.

If you have added an include of your own to a K2, check that you have a copy of the file somewhere else before you press update.
