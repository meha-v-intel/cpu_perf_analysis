import pandas as pd
import matplotlib.pyplot as plt
import os

# ------------------------------
# File and Model Setup
# ------------------------------

EMON_FILES = {
    "LLaMA 2": "cpu_perf_analysis/data/EMONllama2.xlsx",
    "LLaMA 3": "cpu_perf_analysis/data/EMONllama3.xlsx",
    "DeepSeek": "cpu_perf_analysis/data/emon_new.xlsx"
}

MODEL_SHEET_MAP = {
    "LLaMA 2": "details system view",
    "LLaMA 3": "details system view",
    "DeepSeek": "details socket view"
}

# ------------------------------
# Metric Base Definitions
# ------------------------------
# Define metrics ONCE using the system-wide column name (no socket suffix)

BASE_METRICS = [
    "metric_CPU utilization %",
    "metric_CPU operating frequency (in GHz)",
    "metric_CPU utilization% in kernel mode",
    "metric_CPI",
    "metric_core % cycles in license throttle",
    "metric_core % cycles in license level 1",
    "metric_core % cycles in license level 2",
    "metric_core % cycles in license level 3",
    "metric_core % cycles in license level 4",
    "metric_core % cycles in license level 5",
    "metric_core % cycles in license level 6"

]

# X-axis column (represents time)
X_AXIS_COLUMN = "A"

# Output folder
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------------
# Metric Routing Logic
# ------------------------------

def get_metric_map():
    """Generates full model-to-metric mapping with socket suffix for DeepSeek."""
    metric_map = {}
    for base_metric in BASE_METRICS:
        label = base_metric.replace("metric_", "").replace(" in ", " ").strip().title()
        model_sources = {}
        for model, filepath in EMON_FILES.items():
            sheet = MODEL_SHEET_MAP[model]
            if model == "DeepSeek":
                column = f"{base_metric} (socket 0)"
            else:
                column = base_metric
            model_sources[model] = (sheet, column, None)
        metric_map[label] = model_sources
    return metric_map

# ------------------------------
# Data Extraction
# ------------------------------

def extract_data(file_path, sheet_name, y_col, filter_dict=None):
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=0)
    if filter_dict:
        for key, val in filter_dict.items():
            df = df[df[key] == val]
    try:
        x = df[X_AXIS_COLUMN] if not X_AXIS_COLUMN.isalpha() else df.iloc[:, 0]
        y = df[y_col]
    except Exception as e:
        raise ValueError(f"Missing expected column in '{sheet_name}': {e}")
    return pd.DataFrame({"X": x, "Y": y}).dropna()

# ------------------------------
# Plotting Logic
# ------------------------------

def plot_combined_metric(metric_label, model_sources):
    plt.figure(figsize=(10, 6))
    plotted = False

    for model_name, file_path in EMON_FILES.items():
        if model_name not in model_sources:
            continue
        sheet_name, y_col, filters = model_sources[model_name]
        try:
            df = extract_data(file_path, sheet_name, y_col, filters)
            plt.plot(df["X"], df["Y"], marker='o', markersize=3, linewidth=1, label=model_name)
            plotted = True
        except Exception as e:
            print(f"[!] Error extracting '{metric_label}' for {model_name}: {e}")

    if plotted:
        plt.title(metric_label)
        plt.xlabel("Time / Sample Index")
        plt.ylabel(metric_label)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        output_path = os.path.join(OUTPUT_DIR, f"{metric_label.replace(' ', '_')}.png")
        plt.savefig(output_path)
        plt.close()
        print(f"[✓] Saved plot: {output_path}")
    else:
        print(f"[!] Skipped plotting '{metric_label}' (no data extracted)")

# ------------------------------
# Main Runner
# ------------------------------

def main():
    metric_map = get_metric_map()
    for label, model_config in metric_map.items():
        plot_combined_metric(label, model_config)

if __name__ == "__main__":
    main()
