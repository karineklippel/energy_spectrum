import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import detrend

# ----------------------------------------
# Reading and Preprocessing the Data
# ----------------------------------------
# Reading data
data = np.loadtxt('data_test_spectrum_u.csv', delimiter=',')
time = data[:, 0]
u = data[:, 1]

# Removing linear trend and mean
u = detrend(u)
u_no_mean = u - np.nanmean(u)

# Padding the data to make it periodic
num_zeros = 200
u_zeros = np.pad(u_no_mean, (num_zeros, num_zeros), mode='constant', constant_values=0)
time_zeros = np.append(time, time[-1] + (time[1] - time[0]) * np.arange(1, 401))

# Calculate time interval and length of the data
dt = (time[1] - time[0]).item()
N = len(u_zeros)

# ----------------------------------------
# Fourier Transform and Energy Calculation
# ----------------------------------------
# Apply Fourier transform to the data
u_fft = np.fft.fft(u_zeros)

# Calculate the energy spectrum
energy = np.zeros(N // 2 + 1)
frequencies = np.linspace(0.0, 1 / (2 * dt), N // 2 + 1)

for i in range(N // 2 + 1):
    if i == 0 or i == (N // 2):
        energy[i] = np.abs(u_fft[i])**2 * (dt / N)
    else:
        energy[i] = 2 * np.abs(u_fft[i])**2 * (dt / N)

# ----------------------------------------
# Variance Checking
# ----------------------------------------
# Calculate variance of the original data
variance_original = np.var(u_zeros)

# Calculate the variance of the signal after FFT
variance_fft = float(np.sum(energy) / (dt * N))

# Compare variances
print(f'Original variance: {variance_original:.4f}')
print(f'Variance calculated from FFT: {variance_fft:.4f}')

# ----------------------------------------
# Plot Energy Spectrum
# ----------------------------------------
# Initialize figure
figure, ax = plt.subplots(figsize=(6.5, 5))
figure.subplots_adjust(left=0.150, bottom=0.125, right=0.960, top=0.95)

# Plot energy spectrum
plt.plot(frequencies, energy, color='black', label='Energy Spectrum')

# Add a reference line with slope -5/3
x_ref = np.array([0.5, 35])
y_ref = 5e0 * (x_ref / x_ref[0])**(-5/3)
plt.plot(x_ref, y_ref, '--', color='red', label=r'Slope $-5/3$')
plt.text(3, 0.5, r'$-5/3$', color='red', fontsize=14, ha='left', va='bottom')

# Configure log-log scale and axis labels
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Frequency [1/T]', fontsize=14)
plt.ylabel(r'$S_{u}(f)$', fontsize=14)
plt.ylim(1e-12)  # Adjust y-axis limits

# Customize ticks
ax.tick_params(axis='x', labelsize=14)
ax.tick_params(axis='y', labelsize=14)

# Identify and label the period (inverse of frequency) of the energy peak
top_indices = np.argsort(energy[:])[-1:]
for index in top_indices:
    value = 1 / frequencies[index]
    plt.text(frequencies[index], energy[index], f'{value:.0f}T',
             ha='center', va='bottom', fontsize=14)

# Save the figure
plt.savefig('spectrum_u.png', bbox_inches='tight')

# Show the plot
plt.show()
