import csv

with open('Nodosprueba.csv','w',newline='') as csvfile:
    escrito=csv.writer(csvfile)
    escrito.writerow(['Node','Attribute'])
    for i in range(0,100):
     escrito.writerow([i,values[i]])
with open('Linksprueba.csv','w',newline='') as csvfile:
    escrito=csv.writer(csvfile,delimiter=' ',quotechar=',',quoting=csv.QUOTE_MINIMAL)
    escrito.writerow(['ID','source','target'])
    for i in range(0,len(links)):   
     escrito.writerow([i, links[i][0],links[i][1]])
     
     
    
