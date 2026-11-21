# Republic of Tarnovia — Passport Spread

[![the-passport-page-of-a-countr-2-20261121-0318](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/AndryXSad/the-passport-page-of-a-countr-2-20261121-0318/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/AndryXSad/the-passport-page-of-a-countr-2-20261121-0318/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)

One open passport spread for a country that does not exist: the Republic
of Tarnovia, a mountain republic whose capital is Tarnograd.

The left page is the data page of Elena Mara Kovac — born 12 June 1996 in
Tarnograd, a licensed mountain guide (North Ridge, cat. II) — with a
drawn portrait, bilingual field labels (English / Tarnovian), a signature,
and a machine-readable zone with correct ICAO Doc 9303 check digits
(passport TN 4829137, issued 14 Mar 2024, expires 13 Mar 2034). The right
page is the visas page: a single-entry Dravaria visa (18 Sep – 17 Oct
2024, issued in Tarnograd for a mountain-guiding contract), entry and exit
stamps from Ostmark (2–9 May 2024) and Dravaria (18 Sep – 2 Oct 2024), a
fee stamp (45 taler), and the document's telling detail — a condition of
issue requiring a Mountain Pass Permit for any route above 2,000 m, with a
licensed guide compulsory on the North Ridge in winter (Permit
No. MP-77-0142).

Every date agrees: no stamp predates the passport, the visa was issued
before the Dravaria trip, and each entry stamp has a matching exit stamp.
The guilloche lines, watermark emblem and ghost portrait are the
document's security print.

## How it is made

`main.py` renders the spread from scratch with PIL (DejaVu fonts) into
`entry.png` — 1024×1024, deterministic: the same run always produces the
same bytes. When the grader sets `MAKEFUN_OUTPUT_DIR`, the image is
written there and nowhere else. If PIL is unavailable, `main.py` falls
back to copying the pre-rendered `entry.png` shipped in this repository.

## Run it

```sh
python3 main.py                                # renders entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py         # renders entry.png into out/
```

## License

MIT — see [LICENSE](LICENSE).
