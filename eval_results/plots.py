import pandas as pd
import ast
runs = {
    "All drugs": pd.read_csv("eval_results\evaluation_metrics_all.csv"),
    "Top 30":pd.read_csv("eval_results\evaluation_metrics_top30.csv"),
    "Common drugs": pd.read_csv("eval_results\evaluation_metrics_common.csv"),
}

summary = []

for name, df in runs.items():
    summary.append({
        "run": name,
        "macro_recall": df["recall"].mean(),
        "micro_recall": df["num_matched"].sum() / df["num_gt"].sum(),
        "hit_rate": (df["num_matched"] > 0).mean(),
        "perfect_rate": (df["recall"] == 1.0).mean()
    })

summary_df = pd.DataFrame(summary)
print(summary_df)

import matplotlib.pyplot as plt

plt.figure()
plt.boxplot(
    [runs[r]["recall"] for r in runs],
    labels=runs.keys()
)
plt.ylabel("Recall per disease")
plt.title("Recall distribution across runs")
plt.savefig('eval_results/recall_boxplot.png')

summary_df.set_index("run")[["macro_recall", "micro_recall"]].plot(
    kind="bar"
)
plt.ylabel("Recall")
plt.title("Macro vs Micro Recall")
plt.xticks(rotation=0)
plt.savefig('eval_results/recall_barplot.png')

summary_df.set_index("run")["hit_rate"].plot(
    kind="bar", ylim=(0,1)
)
plt.title("Fraction of diseases with ≥1 GT drug recovered")
plt.xticks(rotation=0)
plt.savefig('eval_results/hit_rate_barplot.png')

common_doids = set.intersection(
    *(set(df["DOID"]) for df in runs.values())
)
common_doids = sorted(common_doids)
x = range(len(common_doids))
plt.figure(figsize=(12, 6))

# plot GT once (take from any run)
ref_df = list(runs.values())[0].set_index("DOID")
plt.plot(
    x,
    ref_df.loc[common_doids]["num_gt"],
    marker="o",
    linewidth=2,
    label="GT (num_gt)"
)

# plot predictions
for name, df in runs.items():
    df = df.set_index("DOID")
    plt.plot(
        x,
        df.loc[common_doids]["num_pred"],
        label=name
    )

plt.xticks(x, common_doids, rotation=90)
plt.ylabel("Number of drugs")
plt.xlabel("Disease (DOID)")
plt.title("Number of GT drugs vs Predicted drugs per disease")
plt.legend()
plt.tight_layout()
plt.savefig('eval_results/num_drugs_per_disease.png')