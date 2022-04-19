import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# labels = ['one', 'two', 'tree', 'four', 'five']
# crit = [0, 0 ,0, 0, 1]
# high = [0, 0, 0, 0, 0]
# medium = [1, 1, 4, 2, 5]
# low = [5, 2, 3, 0,5]

# x = np.arange(len(labels))  # the label locations
# width = 0.15  # the width of the bars

# fig, ax = plt.subplots()
# rects1 = ax.bar(x - width*2+width/2, crit, width, label='crit')
# rects2 = ax.bar(x - width+width/2, high, width, label='high')
# rects3 = ax.bar(x +width/2, medium, width, label='medium')
# rects4 = ax.bar(x + width+width/2, low, width, label='low')

# # Add some text for labels, title and custom x-axis tick labels, etc.

# ax.set_title('Incident Summary 2022')
# ax.set_xticks(x, labels)
# ax.legend()

# ax.bar_label(rects1, padding=3)
# ax.bar_label(rects2, padding=3)
# ax.bar_label(rects3, padding=3)
# ax.bar_label(rects4, padding=3)


# fig.tight_layout()

# plt.show()



arrays = [['Jan', 'Jan', 'Jan', 'Feb', 'Feb', 'Feb'],
          ['inbound', 'outbound', 'port', 'inbound', 'outbound', 'port']]
colums = pd.MultiIndex.from_tuples(list(zip(*arrays)))
index = ['crit','high','med','low']
df = pd.DataFrame(np.random.randint(0, 1, size=(len(index), len(arrays[1]))),index=index, columns=colums)
df.loc[df['Jan']['inbound'],'crit'] = '1' 
print(df)