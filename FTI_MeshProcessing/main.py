#main script for handling the data
#input file parser
from nastranParser import ParseFTInastran
from nodeListRead import GetNodeCoordinates
from connectivityRead import GetElementData
from buildDataFrame import GetDataFrame

#input file name (has to be according to FTI nastran output)
originalFilename='Project1_OP 10_Stroke-100.00.nas'
#nodalCoordinateFileName='node_coordinates.dat'
#connectivityAndThicknessFileName='output.dat'

#Splits the FTI Nastran file to two sections: Node coordinates and Connectivity
coordsData,connectivityData=ParseFTInastran(originalFilename)

#Gets the coordinates of nodes in a dictionary format {NodeID(int):x(float),y(float),z(float)}
nodeDict=GetNodeCoordinates(coordsData)

#Gets the element conncetivity and thickness in dictionary format
elementDict, thicknessDict = GetElementData(connectivityData)

# Gets the data frame with node Ids as the row labels and then successively x,y,z coordinates and the results in the next column
#                  x           y          z    result
# 1     -1454.515700 -1084.35220 -54.827271  0.999198
# 2     -1419.797100 -1077.53410 -54.777615  0.990615
# 3     -1384.762700 -1067.24020 -55.412125  0.995297
# 4     -1353.041500 -1054.42640 -55.999153  1.015994
# 5     -1322.016500 -1043.86820 -55.716255  1.013573
# 6     -1289.517000 -1034.58290 -56.037441  1.005676

df=GetDataFrame(nodeDict,elementDict,thicknessDict)
df.to_csv('out.csv')
