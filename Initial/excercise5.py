def CelsiusToFarenheit(Cdegree):
    if Cdegree <-273.15:
        return "This temperature does not make sense"
    Fdegree = 1.8* Cdegree +32
    return Fdegree

temperatures = [10,-20,-289,100]
ftemperatures=[]
i=0

for temperature in temperatures:
    ftemperatures.append(CelsiusToFarenheit(temperature))
'''   print(ftemperatures[i], type(ftemperatures[i]))
    i=i+1
'''

file_name = "farenheit_temperatures"
file = open(file_name,"w")
for item in ftemperatures:
    if isinstance(item,float):
        file.write(str(item)+"\n")

file.close()
