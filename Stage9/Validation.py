output1="Output1/output1.txt"
output2="Output1/output2.txt"
output3="Output1/output3.txt"
Log1=[]
Log2=[]
Log3=[]
with open(output1, "r") as output1:
    for row in output1.readlines():
        Log1.append(row)
with open(output2, "r") as output2:
    for row in output2.readlines():
        Log2.append(row)
with open(output3, "r") as output3:
    for row in output3.readlines():
        Log3.append(row)

