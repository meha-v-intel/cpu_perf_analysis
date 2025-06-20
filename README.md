# EMON CPU Performance Visualization

This is a script to visualize and compare CPU performance across multiple AI model workloads — LLaMA 2, LLaMA 3, and DeepSeek — using EMON data.

## Project Structure


emon_comparison_project/

├── combine_emon_metrics.py # Python script for visualizing EMON data

├── README.md # This file

├── output/ # Folder for generated comparison plots

├─────── EMONllama2.xlsx # EMON dataset for LLaMA 2

├─────── EMONllama3.xlsx # EMON dataset for LLaMA 3

└─────── emon_new.xlsx # EMON dataset for DeepSeek


## What This Script Does

- Extracts key CPU performance metrics (e.g., utilization, frequency, CPI, license throttling levels).
- Compares metrics across LLaMA 2, LLaMA 3, and DeepSeek.
- Automatically adjusts:
  - LLaMA models use **system-wide** metrics from `details system view`
  - DeepSeek uses **socket-specific** metrics from `details socket view` (specifically **socket 0**, since only one socket was active).
- Generates clean, dot-and-line charts for each metric.

---

## Requirements

Required libraries: 

```bash
pip install pandas matplotlib openpyxl
