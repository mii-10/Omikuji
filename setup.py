import pickle
Limit = []
OldYoubi = 10



with open('Temp/Limit.binaryfile', 'wb')as Box_Limit:
    pickle.dump(Limit, Box_Limit)

with open('Temp/OldYoubi.binaryfile', 'wb')as Box_OldYoubi:
    pickle.dump(OldYoubi, Box_OldYoubi)