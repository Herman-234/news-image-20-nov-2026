# The World in One Day — Friday, 20 November 2026

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Herman-234/news-image-20-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Herman-234/news-image-20-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261120)

One image summing up the world's news of Friday 20 November 2026, for the
[news-image-20261120 bounty on make.fun](https://make.fun/bounty/news-image-20261120).

## The twelve stories

1. **Lead — Trump pushes Iran call to 2027.** President says he will "see what
   happens" after January 1 — no rush on the Gulf call.
2. **GTA VI: $2.36bn in one day.** Sensor Tower: 24.6m copies sold — the biggest
   entertainment debut ever.
3. **Cyclone Akvan slams Odisha.** Landfall near Gopalpur at noon; 3 lakh
   evacuated, 423 rescue teams out.
4. **Europe ready to talk to Russia.** Leaders say they are ready for
   negotiations to end the war in Ukraine.
5. **Hayabusa2 drops asteroid landing.** Engine trouble forces Japan's probe to
   abandon its touchdown plan.
6. **Modi meets William and Kate.** PM hosts the Prince and Princess of Wales in
   New Delhi; talks on India–UK ties.
7. **In Brief — Cricket:** Nicholls 113* as New Zealand reach 243/5 on day one
   against India in Wellington.
8. **In Brief — Senegal:** Dozens missing after a migrant boat sinks off the coast.
9. **In Brief — AI:** Anthropic's valuation reportedly reaches $1.5 trillion.
10. **In Brief — Cincinnati:** Fiona the hippo dies at Cincinnati Zoo.
11. **In Brief — Markets:** Sensex up 1.21% and Nifty up 1.14% in a strong rally.
12. **In Brief — Defence:** India signs a Rs 1,976-crore deal with Israel
    Aerospace Industries.

## How it is built

`render.py` draws `entry.png` (1024x1024, under 1 MiB) with Pillow and the
DejaVu fonts — navy masthead, a White House hero with the "DECISION MOVED TO
2027" callout, five story cards, and an In Brief panel. `main.py` verifies the
PNG (signature, size, dimensions, recorded SHA-256) and copies it to
`/output/entry.png`. Python 3.13 standard library plus Pillow only; no network.

```sh
python3 render.py   # draws entry.png
python3 main.py     # verifies and copies it to /output/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
