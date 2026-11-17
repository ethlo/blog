---
date: 2026-10-29
categories:
  - Homelab
---

# 661 backups and none of them off-site

At work I would never accept a system without a tested, off-site backup. At home I ran one for years, and it held everything I actually care about.

<!-- more -->

I only found out because I was doing something else. I wanted the home server written down as Ansible, so I could rebuild it if it died. Before changing anything I went through what was there.

Home Assistant had 661 backups. 335 GB of them, on the same SSD as Home Assistant itself. So one dead disk would take the system and every backup of it at the same moment. The disk was also 97% full, and the backups were the reason.

It gets worse. I did have a backup script. I wrote it myself, it zipped things to that same SSD, and I never put it on a timer. I ran it by hand until I stopped, and that turned out to be January 2025.

I also had a cloud remote, rclone to Google Drive through my own OAuth app. That one is almost funny. An app left in "Testing" gets a token that expires after 7 days. So it worked for a week, and then it answered `invalid_grant` to nobody for a very long time.

So I had backups, a backup script and a cloud remote, and no backup.

<svg viewBox="0 0 680 102" role="img" aria-label="Backup data, GB" style="width:100%;max-width:680px;height:auto;font-family:inherit">
<text x="0" y="16" font-size="13" fill="currentColor" opacity="0.75">Backup data, GB</text>
<text x="180" y="49" font-size="13" text-anchor="end" fill="currentColor">Kept on the same SSD</text>
<rect x="190" y="34" width="380.0" height="20" rx="3" fill="currentColor" opacity="0.35"/>
<text x="578.0" y="49" font-size="13" fill="currentColor">335 GB, 661 files</text>
<text x="180" y="79" font-size="13" text-anchor="end" fill="currentColor">Off-site set now</text>
<rect x="190" y="64" width="17.0" height="20" rx="3" fill="#4f8cff"/>
<text x="215.0" y="79" font-size="13" fill="currentColor">15 GB</text>
</svg>

## Why I let it happen

None of this is hard, and that is the uncomfortable part. I know how to do it, and I do it properly for other people's data every day.

I think it is because at work somebody asks. There is a review, an audit, a colleague who wants to see the restore. At home nobody asks, and everything just keeps working, so it feels fine. Home Assistant even helps you feel fine, since it makes a backup every night and keeps all of them. 661 nights of it.

The data at home is the data I cannot get back from anyone. I treated it the worst.

## What I did about it

Home Assistant now keeps 3 backups. A restic snapshot goes off-site every night at 03:30. The databases are dumped properly first, `sqlite3 .backup` for SQLite and `--single-transaction` for MySQL, since copying a live database file gives you something that only looks like a backup. I keep 14 daily, 8 weekly and 12 monthly, and every Sunday 5% of the data is read back.

The whole off-site set is about 15 GB. I had been keeping 335.

The part I care most about is small. The job reports its state to Home Assistant, and I get a notification on anything but `ok`. I also get one when 36 hours pass without a run. The first rule would not have saved me. My old script never failed, it just never ran, and a job that never starts sends no error.

And I still got it wrong on the first try. One path in the backup list no longer existed. restic exits with code 3 on that, my script had `set -e`, and so it would have stopped before pruning old snapshots, every night, quietly. That is the same mistake a third time. It was caught in review before the first run, which says something about reviews and something about me.

## What I still skimp on

The camera recordings are 1.2 TB and live on the RAID only. Too big to send anywhere, I tell myself. The RAID is 83% full.

I would not accept that answer from anyone at work.
