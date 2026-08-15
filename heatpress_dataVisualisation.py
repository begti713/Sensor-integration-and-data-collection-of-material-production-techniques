import pandas as pd
import matplotlib.pyplot as plt

# Set global formatting for publication
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['figure.dpi'] = 300

print("Generating Heat Press Graph with numerical time...")

# 1. Load data
df_press = pd.read_csv('heatpress_rawdata.csv')

# 2. Setup Figure
fig, ax1_press = plt.subplots(figsize=(8, 5))

# 3. Left Axis: Temperatures
ax1_press.set_xlabel('Time (Minutes)', fontweight='bold')
ax1_press.set_ylabel('Temperature (°C)', fontweight='bold')

# Plotting the three heat press temperature zones
ax1_press.plot(df_press['Time (min)'], df_press['Heatpress Temp (°C)'], color='#d62728', label='Press Temp')
ax1_press.plot(df_press['Time (min)'], df_press['Mould Temp (°C)'], color='#ff7f0e', label='Mould Temp')
ax1_press.plot(df_press['Time (min)'], df_press['Core Temp (°C)'], color='#2ca02c', label='Core Temp')

# Force X-axis to start at 0 and end at 5
ax1_press.set_xlim(0, 5)

# 4. Right Axis: Humidity
ax2_press = ax1_press.twinx()
ax2_press.set_ylabel('Core Humidity (%)', color='#1f77b4', fontweight='bold')
ax2_press.plot(df_press['Time (min)'], df_press['Core Material Humidity (%)'], color='#1f77b4', linestyle='--', label='Core Humidity')
ax2_press.tick_params(axis='y', labelcolor='#1f77b4')

# Force Y-axis for humidity to stay between 0 and 100
ax2_press.set_ylim(0, 100)

# 5. Formatting & Layout
ax1_press.grid(True, linestyle=':', alpha=0.6)
plt.title('Heat Press Drying: Temp vs Humidity', fontweight='bold', pad=15)

# 6. Combine legends
lines1_press, labels1_press = ax1_press.get_legend_handles_labels()
lines2_press, labels2_press = ax2_press.get_legend_handles_labels()
ax1_press.legend(lines1_press + lines2_press, labels1_press + labels2_press, loc='center right')

# 7. Export
plt.tight_layout()
plt.savefig('heatpress_graph_updated.pdf')
plt.close()

print("Graph successfully generated and saved as 'heatpress_graph_updated.pdf'!")