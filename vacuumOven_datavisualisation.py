import pandas as pd
import matplotlib.pyplot as plt

# Set global formatting
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['figure.dpi'] = 300

print("Generating Vacuum Oven Graph with numerical time...")

# 1. Load data
df_vac = pd.read_csv('vacuum_rawdata.csv')

# 2. Setup Figure
fig, ax1_vac = plt.subplots(figsize=(8, 5))

# 3. Left Axis: Temperatures
ax1_vac.set_xlabel('Time (Minutes)', fontweight='bold')
ax1_vac.set_ylabel('Temperature (°C)', fontweight='bold')

ax1_vac.plot(df_vac['Time (min)'], df_vac['Oven Temp (°C)'], color='#d62728', label='Oven Temp')
ax1_vac.plot(df_vac['Time (min)'], df_vac['Shelf Temp (°C)'], color='#ff7f0e', label='Shelf Temp')
ax1_vac.plot(df_vac['Time (min)'], df_vac['Core Temp (°C)'], color='#2ca02c', label='Core Temp')

# Force X-axis to start at 0 and end at 5
ax1_vac.set_xlim(0, 5)

# 4. Right Axis: Vacuum Pressure
ax2_vac = ax1_vac.twinx()
ax2_vac.set_ylabel('Absolute Pressure (mBar)', color='#1f77b4', fontweight='bold')
ax2_vac.plot(df_vac['Time (min)'], df_vac['Vacuum Level (mBar)'], color='#1f77b4', linestyle='--', label='Vacuum Level')
ax2_vac.tick_params(axis='y', labelcolor='#1f77b4')

# Force Y-axis for vacuum to stay between 0 and 1100 (since atmospheric is ~1013)
ax2_vac.set_ylim(0, 1100)

# 5. Formatting & Layout
ax1_vac.grid(True, linestyle=':', alpha=0.6)
plt.title('Vacuum Oven Drying: Temp vs Pressure', fontweight='bold', pad=15)

# 6. Combine legends
lines1_vac, labels1_vac = ax1_vac.get_legend_handles_labels()
lines2_vac, labels2_vac = ax2_vac.get_legend_handles_labels()
# Placed the legend in the center right so it doesn't overlap the steep vacuum curve
ax1_vac.legend(lines1_vac + lines2_vac, labels1_vac + labels2_vac, loc='center right')

# 7. Export
plt.tight_layout()
plt.savefig('vacuum_graph_updated.pdf')
plt.close()

print("Graph successfully generated and saved as 'vacuum_graph_updated.pdf'!")