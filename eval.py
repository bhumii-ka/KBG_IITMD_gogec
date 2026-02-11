import pandas as pd
import ast
import os
pred = pd.read_csv(r"C:\Users\Bhumika Gupta\OneDrive\Desktop\gogec\final_pipeline\predictions_csv\final_drug_predictions_grouped_all_top30.csv")
gt = pd.read_csv(r"C:\Users\Bhumika Gupta\OneDrive\Desktop\gogec\final_pipeline\data\testing_data.csv")

# parse string → list/set
pred["Drugs"] = pred["Drugs"].apply(ast.literal_eval)
gt["drugs"] = gt["drugs"].apply(ast.literal_eval)

def normalize_doid(x):
    x = str(x)
    x = x.replace("DOID_", "DOID:")
    x = x.replace("DOID:", "DOID:")
    return x
pred["DOID"] = pred["Disease"].apply(normalize_doid)
gt["DOID"] = gt["DOID"].apply(normalize_doid)

pred_dict = dict(zip(pred["DOID"], pred["Drugs"]))
gt_dict = dict(zip(gt["DOID"], gt["drugs"]))

results = []

for doid, gt_drugs in gt_dict.items():
    pred_drugs = set(pred_dict.get(doid, []))

    gt_drugs = set(gt_drugs)
    intersection = gt_drugs & pred_drugs

    recall = len(intersection) / len(gt_drugs) if gt_drugs else 0.0
    hit = int(len(intersection) > 0)

    results.append({
        "DOID": doid,
        "num_gt": len(gt_drugs),
        'num_pred': len(pred_drugs),
        "num_matched": len(intersection),
        "recall": recall,
        "matched_drugs": list(intersection)
    })

eval_df = pd.DataFrame(results)
os.makedirs('eval_results', exist_ok=True)
eval_df.to_csv('eval_results/evaluation_metrics_top30.csv', index=False)
print(eval_df)
