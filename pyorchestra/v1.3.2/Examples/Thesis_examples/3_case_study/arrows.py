#solver
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

fig, ax = plt.subplots(2)
ax[0].tick_params(
    axis='both',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    left=False,
    labelbottom=False, # labels along the bottom edge are off
    labelleft=False)

ax[1].tick_params(
    axis='both',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    left=False,
    labelbottom=True, # labels along the bottom edge are off
    labelleft=False)



df = pd.read_csv('result_data.csv')

t = np.linspace(0,70,3000)
methanogens = df['5']
denitrifiers = df['8']

ax[0].plot(t,methanogens, color='k', label=r'$X_{meth}$')
ax[0].plot(t,denitrifiers, color='k', alpha=0.5, label=r'$X_{denitr}$')
ax[0].grid(color='grey')
ax[0].legend(loc='upper right')
ax[1].set_xlabel('time (years)')
ax[0].fill_between([0,8],0,1, color='k',alpha=0.6)
ax[0].fill_between([8,19],0,1, color='k',alpha=0.4)
ax[0].fill_between([19,40],0,1, color='k', alpha=0.2)
ax[0].fill_between([40,70],0,1,color='k',alpha=0.1)

for ii in range(2):
    ax[ii].vlines(8,0,1, color='k',linewidth=3,ls='--')
    ax[ii].vlines(19,0,1, color='k',linewidth=3, ls='--')
    ax[ii].vlines(40,0,1, color='k',linewidth=3, ls='--')
    ax[ii].set_xlim(0,70)
    ax[ii].set_ylim(0,0.015)
ax[1].set_ylim(0,0.012)
    
ax[1].annotate('', xy=(7,0.008), xytext=(1,0.0088), arrowprops=dict(facecolor='black', shrink=0.05))
ax[1].annotate('', xy=(18,0.003), xytext=(9,0.0075), arrowprops=dict(facecolor='black', shrink=0.05))
ax[1].annotate('', xy=(40,0.0071), xytext=(19,0.003), arrowprops=dict(facecolor='black', shrink=0.05))
ax[1].annotate('', xy=(70,0.00), xytext=(41,0.0071), arrowprops=dict(facecolor='black', shrink=0.05))
ax[0].text(2.8,0.012,'1', fontsize=20, fontweight='bold')
ax[0].text(12.2,0.012,'2', fontsize=20, fontweight='bold')
ax[0].text(28,0.012,'3', fontsize=20, fontweight='bold')
ax[0].text(53,0.012,'4', fontsize=20, fontweight='bold')

ax[0].set_title('Detailed figure of methanogens and denitrifiers', fontsize=15)
plt.tight_layout(pad=0.1)

plt.savefig('detailed_anaerobes.pdf')


new = 0.65
old = 0.9
print((new-old)/old * 100)
