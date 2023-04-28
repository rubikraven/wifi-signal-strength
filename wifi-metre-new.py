import math
import time
import pywifi

import matplotlib.pyplot as plt

def calculate_distance(signal_strength, frequency):
    return 10 ** ((27.55 - (20 * math.log10(frequency)) + abs(signal_strength)) / 20)

wifi = pywifi.PyWiFi()

iface = wifi.interfaces()[0]

iface.scan()
time.sleep(5)  # Scan işlemi için zaman tanıyın
scan_results = iface.scan_results()

modem_distances = []

for cell in scan_results:
    ssid = cell.ssid
    signal_strength = cell.signal
    frequency = cell.freq
    distance = calculate_distance(signal_strength, frequency)
    modem_distances.append((ssid, distance))

# Tahmini uzaklığa göre sonuçları sıralayın
modem_distances.sort(key=lambda x: x[1])

# Tüm WiFi modemlerinin uzaklıklarını düzenli bir şekilde yazdırın
print("{:<20} {:<15} {:<10} {:<15}".format("SSID", "Signal (dBm)", "Frequency (MHz)", "Distance (m)"))
print("-" * 60)
for ssid, distance in modem_distances:
    cell = next(filter(lambda c: c.ssid == ssid, scan_results))
    print("{:<20} {:<15} {:<10} {:<15.2f}".format(ssid, cell.signal, cell.freq, distance))

# WiFi modemlerinin tahmini uzaklıklarını grafiksel olarak görselleştirin
ssids = [item[0] for item in modem_distances]
distances = [item[1] for item in modem_distances]

plt.barh(ssids, distances)
plt.xlabel("Uzaklık (m)")
plt.ylabel("WiFi Modemleri")
plt.title("WiFi Modemlerinin Tahmini Uzaklıkları")
plt.show()
