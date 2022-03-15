
import matplotlib.pyplot as plt

data = {'milk': 45, 'water': 25, 'oil': 0}
data_without_zero = {k:v for k,v in data.items() if v>0}
names = list(data_without_zero.keys())
values = list(data_without_zero.values())

plt.pie(values, labels=names, legends=data )
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 0),
                    fancybox=True, shadow=True, ncol=4)
plt.show()