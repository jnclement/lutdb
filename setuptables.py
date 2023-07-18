import lutdb_utils as lu

racklist = ["_1E1","_1W1","_3A1","_3A6","_3C1","_3C9","_1W3","_1E3","_2E2","_2W2"]
nslotlist = [1,2,3,6,7,8,12,13,14,17,18,19]
sslotlist = [1,2,3,7,8,12,13,14,18,19]
for i in range(len(racklist)):
    for j in range(4):
        slotlist = []
        if i < 4:
            slotlist = sslotlist
        else:
            slotlist = nslotlist
        for slot in slotlist:
            lu.create_board_table(racklist[i], j, slot)
            lu.file_lut_to_db("E169000","default.txt",racklist[i],j,slot)
            
