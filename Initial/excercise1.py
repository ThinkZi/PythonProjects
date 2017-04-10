def CelsiusToFarenheit(Cdegree):
    Fdegree = 1.8* Cdegree +32
    return Fdegree

degree = input("Enter the temperature in celsius: ")
Cdegree=float(degree)

if Cdegree > -273.15:
    print("So it is", CelsiusToFarenheit(Cdegree), "degrees Farenheit.")
else:
    print("Temperature cannot be less than -273.15")
