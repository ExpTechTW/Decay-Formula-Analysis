import matplotlib.pyplot as plt
import seaborn as sns
import math
import re
import os

data_list = []

file_list = os.listdir("./data")

count = 0

for filename in file_list:
    with open("./data/{}".format(filename), 'r', encoding='utf-8') as file:
        text = file.read()

        lon = float(re.search(r'Lon:(.*?)°E', text).group(1))
        lat = float(re.search(r'Lat:(.*?)°N', text).group(1))
        depth = float(re.search(r'Depth:(.*?)km', text).group(1))
        mag = float(re.search(r'Mag:(.*?)\n', text).group(1))

        line = text.split("\n")

        for i in line:
            if (i.find("Stacode") == -1):
                continue
            _line = i.split(",")
            _lon = float(_line[2].replace("Stalon=", ""))
            _lat = float(_line[3].replace("Stalat=", ""))
            _pga = float(_line[13].replace("PGA(SUM)=", ""))
            dist_surface = math.sqrt(((lat - _lat) * 111)**2 + ((
                lon - _lon) * 101)**2)
            dist = math.sqrt(dist_surface**2 + depth**2)
            # pga = 12.44 * math.exp(1.31 * mag) * math.pow(dist, -1.837)
            pga = 1.657 * math.exp(
                1.533 * mag) * math.pow(dist, -1.607)
            data_list.append({
                "actual": _pga,
                "estimate": pga
            })
            count += 1

print(count)

actual_values = [item["actual"] for item in data_list]
estimate_values = [item["estimate"] for item in data_list]

plt.figure(figsize=(8, 8))
sns.scatterplot(x=actual_values, y=estimate_values, s=50)

plt.plot([min(actual_values + estimate_values), max(actual_values + estimate_values)],
         [min(actual_values + estimate_values),
          max(actual_values + estimate_values)],
         color='red', linestyle='--')

plt.title('Actual & Estimate')
plt.xlabel('Actual')
plt.ylabel('Estimate')
plt.grid(True)
plt.tight_layout()
plt.show()
