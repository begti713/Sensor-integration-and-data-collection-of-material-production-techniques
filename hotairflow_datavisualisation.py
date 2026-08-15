import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Set global formatting
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['figure.dpi'] = 300

print("Generating Hot Air Graph...")

# 1. Load data
df_hot = pd.read_csv('hotairflow_rawdata.csv.txt')
df_hot['Timestamp'] = pd.to_datetime(df_hot['Timestamp'])

# 2. Setup Figure
fig, ax1_hot = plt.subplots(figsize=(8, 5))

# 3. Left Axis: Temperatures
ax1_hot.set_xlabel('Time', fontweight='bold')
ax1_hot.set_ylabel('Temperature (°C)', fontweight='bold')
ax1_hot.plot(df_hot['Timestamp'], df_hot['Inlet Temp (°C)'], color='#d62728', label='Inlet Temp')
ax1_hot.plot(df_hot['Timestamp'], df_hot['Mould Temp (°C)'], color='#ff7f0e', label='Mould Temp')
ax1_hot.plot(df_hot['Timestamp'], df_hot['Exhaust Temp (°C)'], color='#2ca02c', label='Exhaust Temp')

# 4. Right Axis: Humidity
ax2_hot = ax1_hot.twinx()
ax2_hot.set_ylabel('Humidity (%)', color='#1f77b4', fontweight='bold')
ax2_hot.plot(df_hot['Timestamp'], df_hot['Mould Humidity (%)'], color='#1f77b4', linestyle='--', label='Mould Humidity')
ax2_hot.tick_params(axis='y', labelcolor='#1f77b4')

# 5. Formatting & Layout
ax1_hot.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
fig.autofmt_xdate()
ax1_hot.grid(True, linestyle=':', alpha=0.6)
plt.title('Hot Air Drying: Temp vs Humidity', fontweight='bold')

# 6. Combine legends
lines1_hot, labels1_hot = ax1_hot.get_legend_handles_labels()
lines2_hot, labels2_hot = ax2_hot.get_legend_handles_labels()
ax1_hot.legend(lines1_hot + lines2_hot, labels1_hot + labels2_hot, loc='upper left')

# 7. Export
plt.tight_layout()
plt.savefig('hotair_graph.pdf')
plt.close()

print("Hot air graph successfully generated and saved as 'hotair_graph.pdf'!")