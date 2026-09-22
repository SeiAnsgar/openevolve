"""
zeit, energy, latency

für jede kategorie ein diagramm, in dem wird jeweils zigzag und openevo vergleichen


"""


import matplotlib.pyplot as plt

category_runtime = ["ZigZag; resnet18", "OpenEvo; resnet18", "ZigZag; resnet50", "OpenEvo; resnet50"]
values_runtime = [66, 772, 156, 1572]


#resnet18
#opt: latency
category_energy = ["ZigZag", "OpenEvo_20iter","OpenEvo_50iter", "OpenEvo_100iter"]
values_energy = [4.99e+09, 5.60169e+10, 1.2743175656e+10, 6.874653309e+09]

category_latency = ["ZigZag", "OpenEvo_20iter","OpenEvo_50iter", "OpenEvo_100iter"]
values_latency = [5.60e+06, 1.64296328e+08, 1.3302049e+07, 7.810371e+06]

#opt: energy
category_energy_e = ["ZigZag", "OpenEvo_20iter","OpenEvo_50iter", "OpenEvo_100iter"]
values_energy_e = [9.04e+09, 7.53e+09, 0, 6.874653309e+09]

category_latency_e = ["ZigZag", "OpenEvo_20iter","OpenEvo_50iter", "OpenEvo_100iter"]
values_latency_e = [1.58e+07, 8.61e+06, 0, 7.810371e+06]




fig, axs = plt.subplots(1, 2, figsize=(10, 4))

axs[0].bar(category_energy, values_energy)
axs[0].set_title("Energy consumption")
axs[0].set_xlabel("Variant")
axs[0].set_ylabel("Energy")
axs[0].tick_params(axis="x", rotation=45)

axs[1].bar(category_latency, values_latency)
axs[1].set_title("Latency")
axs[1].set_xlabel("Variant")
axs[1].set_ylabel("Latency")
axs[1].tick_params(axis="x", rotation=45)

axs[0].bar(category_energy_e, values_energy_e)
axs[0].set_title("Energy consumption")
axs[0].set_xlabel("Variant")
axs[0].set_ylabel("Energy")
axs[0].tick_params(axis="x", rotation=45)

axs[1].bar(category_latency_e, values_latency_e)
axs[1].set_title("Latency")
axs[1].set_xlabel("Variant")
axs[1].set_ylabel("Latency")
axs[1].tick_params(axis="x", rotation=45)

fig.tight_layout()

plt.savefig("benchmark.png", dpi=300)
