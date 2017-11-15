#FTI nastran Parser
def ParseFTInastran(originalFilename):
    with open(originalFilename) as f:
        contents1,splitPhrase,contents2 = f.read().partition('CONNECTING CARDS')
#    with open(nodalCoordinateFileName,'w') as f:
#        f.write(contents1)
#    with open(connectivityAndThicknessFileName,'w') as f:
#        f.write(contents2)
#    print(splitPhrase)
    return contents1, contents2
