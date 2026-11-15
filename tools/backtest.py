#!/usr/bin/env python3
"""Backtest script for btc-cent-forecast-01 comparing persistence vs main.py forecast."""

import os
import json
import sys
import glob

# Ensure we can import main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import main

INPUT_DIR = os.environ.get("MAKEFUN_INPUT_DIR", "/root/.gemini/tmp/btc-cent-forecast-01/input")
HORIZON = 240

def run_backtest():
    case_files = sorted(glob.glob(os.path.join(INPUT_DIR, "p0*.in")))
    if not case_files:
        print(f"No case files found in {INPUT_DIR}")
        return

    total_pers_err = 0.0
    total_fore_err = 0.0
    total_count = 0

    print(f"{'Case':<6} | {'Count':<6} | {'Persistence MAE':<16} | {'Forecaster MAE':<16} | {'Diff (%)':<10}")
    print("-" * 65)

    for path in case_files:
        case_id = os.path.basename(path)[:-3]
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        prices = data["markets"][0]["prices"]
        
        # Walk checkpoint over every minute where we have at least 1440 history and +240 future
        start_idx = max(1440, main.REV_WINDOW)
        end_idx = len(prices) - HORIZON - 1
        if start_idx >= end_idx:
            # fallback if series is shorter
            start_idx = 100
            end_idx = len(prices) - HORIZON - 1
        
        pers_abs_err = 0.0
        fore_abs_err = 0.0
        count = 0

        for i in range(start_idx, end_idx + 1):
            history = prices[:i]
            target = prices[i + HORIZON]
            
            # persistence guess: last price in history
            pers_guess = history[-1]
            pers_abs_err += abs(pers_guess - target)
            
            # forecaster guess
            try:
                fore_guess = main.forecast(history)
            except Exception as e:
                print(f"Error at {case_id} index {i}: {e}")
                fore_guess = pers_guess
            fore_abs_err += abs(fore_guess - target)
            count += 1

        if count > 0:
            p_mae = pers_abs_err / count
            f_mae = fore_abs_err / count
            diff_pct = (f_mae - p_mae) / p_mae * 100
            print(f"{case_id:<6} | {count:<6} | {p_mae:<16.3f} | {f_mae:<16.3f} | {diff_pct:<+10.2f}%")
            total_pers_err += pers_abs_err
            total_fore_err += fore_abs_err
            total_count += count

    if total_count > 0:
        overall_p = total_pers_err / total_count
        overall_f = total_fore_err / total_count
        overall_diff = (overall_f - overall_p) / overall_p * 100
        print("-" * 65)
        print(f"{'OVERALL':<6} | {total_count:<6} | {overall_p:<16.3f} | {overall_f:<16.3f} | {overall_diff:<+10.2f}%")

if __name__ == "__main__":
    run_backtest()
