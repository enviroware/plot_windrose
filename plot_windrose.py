# RBI 20191130

import os.path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from windrose import WindroseAxes

def load_aermet_sfc_file(ff):
 
    myfile = open(ff,"r",newline="\n")
    lines = myfile.readlines()
    # Header record
    (latitude,longitude,ua_identifier, sf_identifier, os_identifier, version_date) = [lines[0].split()[i] for i in (0,1,3,5,7,9)]
    
    wind = []
    for line in lines[1:]:
        (year,month,day,j_day,hour,h_sens,u_star,w_star,vptg,zic,zim,lmo,z_zero,bowen,albedo,ws,wd,zref,temp,ztemp,ipcode,pamt,rh,pres,ccvr,wsadj,extra) = line.split()
        if (float(wd) >= 0 and float(ws) >=0):
            wind.append([float(wd),float(ws)])

    myfile.close()
    
    d = {}
    d['wind'] = wind
    d['latitude'] = latitude
    d['longitude'] = longitude

    return d

sfc_file = input("Please enter AERMOD.SFC file name: ")
if not os.path.exists(sfc_file):
    print(sfc_file+" does not exists.")
    exit()

d = load_aermet_sfc_file(sfc_file)
wd = []
ws = []

for pair in d['wind']:
    wd.append(pair[0])
    ws.append(pair[1])


ax = WindroseAxes.from_ax()    
ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white',cmap=cm.hot)
ax.set_legend()
plt.suptitle(sfc_file+"\n LAT:"+d['latitude']+ " / LON: "+d['longitude'])
plt.savefig(sfc_file+".png")
print("Windrose plot saved as "+sfc_file+".png")



