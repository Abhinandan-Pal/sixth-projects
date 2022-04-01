import diff,crdt

myUser = crdt.crdt(1,'A')

def get_CRDT_commands(old_text,new_text):
	global myUser
	add_pos,delete_pos = diff.getDiff(old_text,new_text)
	print(f"newText:{new_text}; add_pos: {add_pos}; delete_pos: {delete_pos}")
	adds = []
	deletes = []
	for add_p in add_pos:
		add_after = myUser.order[add_p[0]]	#Now not to add -1 to get index of prev as 0th loc has startOfFile.
		data = add_p[1]
		current = myUser.self_next_index()
		add = (data,current,add_after)
		adds.append(add)
		myUser.add_element(add)

	for delete_p in delete_pos:
		delete = myUser.order[delete_p+1] #+1 as 0th loc is for startOfFile so actual index starts from 1
		deletes.append(delete)
		myUser.delete_element(delete)

	for add in adds:
		print(f"ADD data: {add[0]}; current: {add[1]}; addAfter: {add[2]}")
	for delete in deletes:
		print(f"DELETE index: {delete};")
	print('\n MY USER:')
	myUser.print_crdt()
