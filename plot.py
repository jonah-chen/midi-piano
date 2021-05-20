import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from run import outfile

f = pd.read_csv(outfile)
plt.plot(f["test1"])
plt.plot(f["test2"])
plt.show()