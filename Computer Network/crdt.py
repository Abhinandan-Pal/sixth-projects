class index:
    user_id: int
    count: int
    def __init__(self,user_id,count):
        self.user_id = user_id
        self.count = count
    def __str__(self):
        return f"(uid = {self.user_id}, count = {self.count})"
    
    def isgreater(in1,in2):
        if(in1.count>in2.count):
            return True
        if(in1.user_id>in2.user_id):
            return True
        return False


class add_element:
    data: str
    #before: index
    after: index
    def __init__(self,data,after):
        self.data = data
        #self.before = before
        self.after = after

class crdt:
    doc: dict[index,[str,bool]]
    users_count: dict[int,int]      # user_id -> [count]
    users_name: dict[int, str]  # user_id -> [name]
    order: list[index]
    uid: int
    docStr: str
    adds: list[(str,index,index)]
    deletes: list[index]

    def __init__(self,uid,name):
        id1 =index(0,0)
        self.uid = uid
        self.doc = {id1:['\0',False]}   #indicates start of doc
        self.users_count = {0:0,uid:0}  #count of uid is set as 0 as +1 present in 'self_next_index'
        self.users_name = {0:'root',uid:name}
        self.order = [id1]
        self.docStr = ""
        self.adds = []
        self.deletes = []
        
    
    def add_user(self,id,name):
        # add check to make sure user not already present
        self.users_name[id] = name
        self.users_count[id] = self.users_count[self.uid]

    def get_index(self,in2):
        for i in range(len(self.order)):
            in1 = self.order[i]
            if(in1.count == in2.count) and (in1.user_id == in2.user_id):
                return i
        raise RuntimeError(f'Trying to add after inexistent: {in2}') 
    
    def add_element(self,element):
        
        data: str = element[0]
        current: index = element[1]
        add_after: index = element[2]

        for user in self.users_count.keys():    #notice in diagram it b starts from 4
            if(current.count > self.users_count[user]):
                self.users_count[user] = current.count

        self.doc[current] = [data,True]

        a_pos = self.get_index(add_after) + 1
        while(a_pos< len(self.order) and index.isgreater(self.order[a_pos],current)):
            a_pos += 1

        self.order.insert(a_pos,current)
        #print(f"Succesfully added {data} at {current} after {add_after}")

    def self_next_index(self):
        self.users_count[self.uid] += 1;
        id_t = index(self.uid,self.users_count[self.uid])
        return id_t

    def delete_element(self,current:index):
        self.doc[current][1] = False


    def print_crdt(self):
        for ind in self.order:
            val = self.doc[ind]
            if(val[1]):
                print(val[0])

    def add_element_UI():
        for i in range(len(self.docStr)):
            print(f"{i}:{self.docStr[i]}", end=" ")
        x = input("Enter postion to add after: ")
        add_after = order[x]
        data = input("Enter data to be inserted: ")
        current = self.self_next_index
        add = (data,current,add_after)
        self.adds.append(add)

    def changeAll():
        for add in self.adds:
            self.add_element(add)
    
        #Send adds to all connected devices
        self.adds = []
    
    def recive():
        addsR = []  #recieve it from other
        for add in addsR:
            self.add_element(add)
    
    def connect():
        #connect and obtain user_id and name
        idC = 2
        nameC = 'B'
        self.add_user(idC,nameC)
    
    def delete_element_UI():
        for i in range(len(self.docStr)):
            print(f"{i}:{self.docStr[i]}", end=" ")
        x = input("Enter postion to be deleted: ")
        current = order[x]
        self.deletes.append(current)




# Create 2 users
userA = crdt(1,'A')
userB = crdt(2,'B')
userA.add_user(2,'B')
userB.add_user(1,'A')
adds_A = []
adds_B = []

#add 'a'
add_after = index(0,0)
data = 'a'
current = userA.self_next_index()
add = (data,current,add_after)
adds_A.append(add)

#add 'b'
add_after = index(1,1)
data = 'b'
current = userA.self_next_index()
add = (data,current,add_after)
adds_A.append(add)

# add append of A to both
for add in adds_A:
    userA.add_element(add)

for add in adds_A:
    userB.add_element(add)
adds_A = []




#add 'x'
add_after = index(1,1)
data = 'x'
current = userA.self_next_index()
add = (data,current,add_after)
adds_A.append(add)



#add 'p'
add_after = index(1,1)
data = 'p'
current = userB.self_next_index()
add = (data,current,add_after)
adds_B.append(add)


# add append of A to both
for add in adds_A:
    userA.add_element(add)

for add in adds_A:
    userB.add_element(add)
adds_A = []

# add append of B to both
for add in adds_B:
    userA.add_element(add)

for add in adds_B:
    userB.add_element(add)
adds_A = []

print('\n USER B:')
userB.print_crdt()
print('\n USER A:')
userA.print_crdt()
