import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
from os import listdir
from sys import argv
import pylab

#This program plots all files at once and saves one image

M=float(argv[1])
offset=2 #number of points to ignore near origin


# plot t =0 data in red
data0 = pylab.loadtxt("w_data/w_000000.txt")
plt.plot(data0[offset:,0]/M, data0[offset:,1]*M, '--', lw=3, color=[1,0,0], label="t/M=0")


#plot the last data point
files=listdir("w_data")
times=[int(i[2:-4]) for i in files]
times.sort()
last_t = times[-1]
last_toM = float(last_t)
data_last = pylab.loadtxt("w_data/w_"+str(last_t).zfill(6)+".txt")
#plt.plot(data_last[offset:,0]/M, data_last[offset:,1]*M, '--', lw=3, color=[0,0,0], label="t/M="+str(int(last_toM))+"(last)")




# plot other time-averaged data
files_temp=listdir("t_ave/")
files=[]
for i in files_temp:
	if(i[:5]=="w_ave"):
		files.append(i)
files.sort()
n=len(files)


data=[]
times1=[]
for num,i in enumerate(files):
	data.append(np.loadtxt("t_ave/"+i))
	data[num]=data[num][data[num][:,0].argsort()]
	#print(i)
	times1.append(i[5:-4])

times=[str(int(t)).zfill(6) for t in times1]


for i in range(0,n,150):             
	blues=[float(3*(n-i))/(5*n),float(4*(n-i))/(5*n),float((n-i))/n]     
	plt.plot(data[i][offset:,0]/M,data[i][offset:,1]*M,lw=2, color=blues, label="t/M="+str(int(times[i]))) 


x=np.linspace(150,300,101)
x_tail = (np.abs(data[n-1][offset:,0]/M-x[-1])).argmin()
def curve(x):
	return M*0.000025*(x*M/1000)**(-3/2)
curve_offset = curve(x[-1])-data[n-1][offset:,1][x_tail]*M




plt.plot(x,curve(x)+curve_offset, '--', lw=6, color=(0,0,0,.9)) #, label="r^-3/2")

plt.xlim(0,400)
plt.ylim(0,1.3e-4*M)
plt.xlabel(r'$r/M$')
plt.ylabel(r'$\Omega \times M$')
plt.title("Evolution of Omega")
plt.annotate(r'$\sim r^{-3/2}$',xy=(225,0.0002),fontsize=18)
plt.legend()
#plt.show()
plt.savefig("png_ave/AllTimes.png")
