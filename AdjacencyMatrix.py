def getAdjacent(node):
    output = []
    output.append([8, 0])
    output.append([8, 1])
    if(node[1] == 0 or node[1] == 2):
        output.append([node[0], 1])
    else:
        output.append([node[0], 0])
        output.append([node[0], 2])

    if(node[0] == 0):
        if(node[1] == 1):
            output.append([1, 1])
        elif(node[1] == 0):
            output.append([3, 0])
        else:
            output.append([4, 2])
    elif(node[0] == 7):
        if(node[1] == 1):
            output.append([6, 1])
        elif(node[1] == 0):
            output.append([3, 0])
        else:
            output.append([4, 2])
    elif(node[0] == 1):
        if(node[1] == 1):
            output.append([2, 1])
            output.append([0, 1])
        elif(node[1] == 0):
            output.append([3, 1])
        else:
            output.append([4, 1])
    elif(node[0] == 6):
        if(node[1] == 1):
            output.append([5, 1])
            output.append([7, 1])
        elif(node[1] == 0):
            output.append([3, 1])
        else:
            output.append([4, 1])
    elif(node[0] == 2):
        if(node[1] == 1):
            output.append([1, 2])
        elif(node[1] == 0):
            output.append([3, 2])
        else:
            output.append([4, 0])
    elif(node[0] == 5):
        if(node[1] == 1):
            output.append([6, 2])
        elif(node[1] == 0):
            output.append([3, 2])
        else:
            output.append([4, 0])
    elif(node[0] == 3):
        if(node[1] == 1):
            output.append([1, 0])
            output.append([6, 0])
        elif(node[1] == 0):
            output.append([0, 0])
            output.append([7, 0])
        else:
            output.append([2, 0])
            output.append([5, 0])
    elif(node[0] == 4):
        if(node[1] == 1):
            output.append([1, 2])
            output.append([6, 2])
        elif(node[1] == 0):
            output.append([0, 2])
            output.append([7, 2])
        else:
            output.append([2, 2])
            output.append([5, 2])

    return output