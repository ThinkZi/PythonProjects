import math
import numpy as np
#Global Coordinates
i0=np.array([1,0,0])
j0=np.array([0,1,0])
k0=np.array([0,0,1])

#Tipping
tip=np.array([0.495, 0.000, 0.869])

#rotation axis
rA=np.cross(k0,tip)
nrA=rA/np.linalg.norm(rA)

#ANGLE BETWEEN TIP AND Z
def angBetVec(u,v):
    c=np.dot(u,v)/np.linalg.norm(u)/np.linalg.norm(v)
    angle=np.arccos(np.clip(c,-1,1))
    return angle
#rotation matrix https://en.wikipedia.org/wiki/Transformation_matrix
def rotMatrix(Teta,rotAx):
    #rotAx: unit rotation angle
    #Teta: rotation angle
    cosTeta=np.cos(Teta)
    sinTeta=np.sin(Teta)
    l=rotAx[0]
    m=rotAx[1]
    n=rotAx[2]
    row1=[l*l*(1-cosTeta)+cosTeta, m*l*(1-cosTeta)-n*sinTeta, n*l*(1-cosTeta)+m*sinTeta]
    row2=[l*m*(1-cosTeta)+n*sinTeta, m*m*(1-cosTeta)+cosTeta, n*m*(1-cosTeta)-l*sinTeta]
    row3=[l*n*(1-cosTeta)-m*sinTeta, m*n*(1-cosTeta)+l*sinTeta, n*n*(1-cosTeta)+cosTeta]
    return np.array([row1,row2,row3])

rotmat=rotMatrix(angBetVec(tip,k0),nrA)

print(tip)
i1=100*rotmat.dot(i0)
j1=100*rotmat.dot(j0)
k1=100*rotmat.dot(k0)

np.savetxt('ijk.txt',(i1,j1,k1), delimiter=',', newline='\n',fmt='%10.5f')


print(i1)
print(j1)
print(k1)
