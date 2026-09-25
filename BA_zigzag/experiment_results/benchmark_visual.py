import sys
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def parse_yaml_file(filepath):
    """
    Liest die angegebene Datei ein und extrahiert dynamisch alle Test-Blöcke
    (z. B. test_1_energy, test_2_latency, test_3_latency, etc.).
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Fehler: Die Datei '{filepath}' wurde nicht gefunden.")
        sys.exit(1)

    # Trenne die Blöcke an allen Stellen, an denen 'test_<ID>_<GOAL>:' am Zeilenanfang steht
    test_blocks = re.split(r'\n(?=test_\d+_\w+:)', text)
    records = []
    
    for block in test_blocks:
        block = block.strip()
        if not block:
            continue
        
        # Name des Tests (z. B. test_1_energy, test_3_latency)
        test_name = block.splitlines()[0].split(':')[0].strip()
        
        # Workload & Optimierungsziel auslesen
        workload_m = re.search(r'workload:\s*"?([^"\n\.]+)', block)
        opt_goal_m = re.search(r'opt_goal:\s*"?([^"\n]+)"?', block)
        
        workload = workload_m.group(1).strip() if workload_m else test_name
        opt_goal = opt_goal_m.group(1).strip() if opt_goal_m else "unknown"
        
        # Extrahieren von OpenEvolve-Einträgen
        oe_matches = re.findall(
            r'OpenEvolve:.*?number_of_iterations:\s*(\d+).*?metrics:\s*energy:\s*([\d\.e\+\-]*).*?latency:\s*([\d\.e\+\-]*)',
            block, re.DOTALL
        )
        for iters, e_str, l_str in oe_matches:
            records.append({
                "test_name": test_name,
                "workload": workload,
                "opt_goal": opt_goal,
                "framework": f"OpenEvolve ({iters} iter)",
                "energy": float(e_str) if e_str.strip() else np.nan,
                "latency": float(l_str) if l_str.strip() else np.nan
            })
            
        # Extrahieren von ZigZag-Einträgen
        zz_matches = re.findall(
            r'ZigZag:.*?metrics:\s*energy:\s*([\d\.e\+\-]*).*?latency:\s*([\d\.e\+\-]*)',
            block, re.DOTALL
        )
        for e_str, l_str in zz_matches:
            records.append({
                "test_name": test_name,
                "workload": workload,
                "opt_goal": opt_goal,
                "framework": "ZigZag",
                "energy": float(e_str) if e_str.strip() else np.nan,
                "latency": float(l_str) if l_str.strip() else np.nan
            })
            
    return pd.DataFrame(records)


def plot_results(df, output_filename="benchmark_comparison.png"):
    """
    Erstellt dynamisch Balkendiagramme für die Optimierungsziele 'energy' und 'latency'.
    """
    if df.empty:
        print("Keine gültigen Messdaten in der Datei gefunden.")
        return

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Farbpalette für verschiedene Frameworks / Konfigurationen
    color_palette = ["#2b5c8f", "#3690c0", "#67a9cf", "#e6550d", "#78c679", "#8c510a"]

    # -------------------------------------------------------------
    # 1. Diagramm: Optimierungsziel "energy"
    # -------------------------------------------------------------
    df_energy = df[df["opt_goal"] == "energy"]
    if not df_energy.empty:
        workloads = sorted(df_energy["workload"].unique())
        frameworks = sorted(df_energy["framework"].unique())
        
        x = np.arange(len(workloads))
        width = 0.8 / max(len(frameworks), 1)
        
        ax1 = axes[0]
        for i, fw in enumerate(frameworks):
            sub = df_energy[df_energy["framework"] == fw]
            vals = [
                sub[sub["workload"] == w]["energy"].values[0] 
                if len(sub[sub["workload"] == w]) > 0 else np.nan 
                for w in workloads
            ]
            vals_scaled = [v / 1e9 if pd.notna(v) else 0 for v in vals]
            
            rects = ax1.bar(
                x + (i - len(frameworks)/2 + 0.5) * width, 
                vals_scaled, width, 
                label=fw, 
                color=color_palette[i % len(color_palette)]
            )
            
            # Zahlenwerte über den Balken einblenden
            for rect, orig_v in zip(rects, vals):
                if pd.notna(orig_v) and orig_v > 0:
                    h = rect.get_height()
                    ax1.annotate(f'{h:.2f}e9',
                                xy=(rect.get_x() + rect.get_width() / 2, h),
                                xytext=(0, 3),
                                textcoords="offset points",
                                ha='center', va='bottom', fontsize=8)

        ax1.set_title("Optimierungsziel: Energy\n(Gemessener Energieverbrauch)", fontsize=12, fontweight='bold')
        ax1.set_ylabel("Energy (1e9)", fontsize=10)
        ax1.set_xticks(x)
        ax1.set_xticklabels(workloads, rotation=15 if len(workloads) > 3 else 0)
        ax1.legend(title="Framework / Config")
        ax1.grid(axis='y', linestyle='--', alpha=0.6)

    # -------------------------------------------------------------
    # 2. Diagramm: Optimierungsziel "latency"
    # -------------------------------------------------------------
    df_latency = df[df["opt_goal"] == "latency"]
    if not df_latency.empty:
        workloads_l = sorted(df_latency["workload"].unique())
        frameworks_l = sorted(df_latency["framework"].unique())
        
        x2 = np.arange(len(workloads_l))
        width_l = 0.8 / max(len(frameworks_l), 1)
        
        ax2 = axes[1]
        for i, fw in enumerate(frameworks_l):
            sub = df_latency[df_latency["framework"] == fw]
            vals = [
                sub[sub["workload"] == w]["latency"].values[0] 
                if len(sub[sub["workload"] == w]) > 0 else np.nan 
                for w in workloads_l
            ]
            vals_scaled = [v / 1e6 if pd.notna(v) else 0 for v in vals]
            
            rects = ax2.bar(
                x2 + (i - len(frameworks_l)/2 + 0.5) * width_l, 
                vals_scaled, width_l, 
                label=fw, 
                color=color_palette[i % len(color_palette)]
            )
            
            for rect, orig_v in zip(rects, vals):
                if pd.notna(orig_v) and orig_v > 0:
                    h = rect.get_height()
                    ax2.annotate(f'{h:.2f}M',
                                xy=(rect.get_x() + rect.get_width() / 2, h),
                                xytext=(0, 3),
                                textcoords="offset points",
                                ha='center', va='bottom', fontsize=8)

        ax2.set_title("Optimierungsziel: Latency\n(Gemessene Latenz)", fontsize=12, fontweight='bold')
        ax2.set_ylabel("Latency (Millionen / 1e6)", fontsize=10)
        ax2.set_xticks(x2)
        ax2.set_xticklabels(workloads_l, rotation=15 if len(workloads_l) > 3 else 0)
        ax2.legend(title="Framework / Config")
        ax2.grid(axis='y', linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.savefig(output_filename, dpi=300)
    print(f"Diagramm erfolgreich unter '{output_filename}' gespeichert.")
    plt.show()


if __name__ == "__main__":
    # Pfad zur YAML-Datei: Kann als Konsolenparameter übergeben werden ODER hier direkt gesetzt werden
    if len(sys.argv) > 1:
        yaml_filepath = sys.argv[1]
    else:
        yaml_filepath = "results.yaml"  # <-- Hier Deinen Dateipfad eintragen!

    print(f"Lese Daten aus '{yaml_filepath}'...")
    df = parse_yaml_file(yaml_filepath)
    plot_results(df)