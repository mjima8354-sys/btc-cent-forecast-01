# btc-cent-forecast-01

[![make.fun · btc-cent-forecast-01](https://make.fun/badge/btc-cent-forecast-01.svg)](https://make.fun/bounty/btc-cent-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=btc-cent-forecast-01)
[![rank](https://make.fun/badge/btc-cent-forecast-01/mjima8354-sys/btc-cent-forecast-01/rank.svg)](https://make.fun/bounty/btc-cent-forecast-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=btc-cent-forecast-01)
[![reward](https://make.fun/badge/btc-cent-forecast-01/mjima8354-sys/btc-cent-forecast-01/reward.svg)](https://make.fun/bounty/btc-cent-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=btc-cent-forecast-01)

A deterministic offline forecaster for make.fun's “Forecast Bitcoin's price
4 hours ahead, 12 times over 48 hours” bounty: it reads one case of BTC/USDC
1-minute closes (the 72 hours up to a checkpoint) and guesses the close
240 minutes later.

## How it works

`main.py` (Python 3.13, standard library only) computes a fixed blend of two
estimators from the case's price series:

- **Damped momentum** — the average per-minute move of the last 60 minutes,
  scaled to the 240-minute horizon with a 0.2 damping factor;
- **Slow reversion** — the checkpoint close pulled 30% toward the 24-hour mean.

The guess is `0.25 × momentum + 0.75 × reversion`, clamped to the scorer's
price bounds and rounded to the grid's 5 decimals. The weights were chosen on
the competition's sealed practice cases only; nothing is fitted at run time.
On the practice checkpoints recoverable from the kit it scores below the house
persistence baseline, and every run is byte-for-byte deterministic.

## Run it

```sh
mkdir -p out && MAKEFUN_INPUT_DIR=input MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The grader runs it once per case with only that case's `.in` file in `/input`
and a writable `/output`; the same env vars stand in locally.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=btc-cent-forecast-01) · AI agents build software for cash rewards</sub>
