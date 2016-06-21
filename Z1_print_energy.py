#!/usr/bin/python
#!/usr/bin/env python
import csv
# Z1 sensor average power total energy consumption calculation

#Declaring the currents as they are in Zoletrias Z1 datasheet
CURRENTS = {
    "voltage" : 3,
    "power_lpm_mA" : 0.05,
    "power_cpu_mA" : 1.8,
    "power_tx_mA"  : 17.4,
    "power_rx_mA"  : 18.8,
    "power_idle_mA": 0.416,
}
#Declaring other vars and arrays
TICKS_PER_SECOND = 32768
EnergyTable = []  # Energy:cpu,lpm,rx,tx,idle
TmpTable = []  
AVG=TOT=Cpu=Lpu=Tx=Rx=TOTtx=AVGtx=TOTtx=TOTrx=0
tmp=[]

#Reading the log file
with open('COOJA.testlog', 'rb') as f:
    for line in f:
    	if line.find(" P ") > 0:
				
		tmp1 = line.split(" ")
		tmp1 = filter(None,tmp1)
		tmp.append(tmp1)

for row in tmp:	
				#check the nodes identidy and start reading
        if row[1] == 'ID:1':
		        Cpu=Cpu+int(row[13])            
		        Lpu=Lpu+int(row[14])
	         	Tx=Tx+int(row[15]) 
	         	Rx=Rx+int(row[16])
             

TmpTable.insert(0, Cpu)
TmpTable.insert(1, Lpu)
TmpTable.insert(2, Tx)
TmpTable.insert(3, Rx)
for i in range(0,4):
    EnergyTable.append(float(TmpTable[i])/TICKS_PER_SECOND)	#From ticks to seconds conversion       	     	                         	

#Calculating the Energy of each state(Cpu,lpu,tx,rx)
EnergyTable[0]= EnergyTable[0]* CURRENTS["power_cpu_mA"]*CURRENTS["voltage"]
EnergyTable[1]= EnergyTable[1]* CURRENTS["power_lpm_mA"]*CURRENTS["voltage"]
EnergyTable[2]= EnergyTable[2]* CURRENTS["power_tx_mA"]*CURRENTS["voltage"]
EnergyTable[3]= EnergyTable[3]* CURRENTS["power_rx_mA"]*CURRENTS["voltage"]

for i in range(0,4):
    AVG = EnergyTable[i] + AVG #adding them all together
    TOT = EnergyTable[i] + TOT
    
print "-----------------------------------------"

AVG=AVG/3480 #Calculating average energy for n minutes of simulation here for 1 hour simulation

print ("Total energy consumption ", TOT ,"mW")
print("The verage power consumption is ","%.6f" % AVG,"mW");       
##########  
