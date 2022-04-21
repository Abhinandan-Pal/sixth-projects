import diff
import crdt


def get_CRDT_commands(self_crdt, old_text, new_text):
    add_pos, delete_pos = diff.getDiff(old_text, new_text)
    print(f"oldText: {old_text}; newText:{new_text}; add_pos: {add_pos}; delete_pos: {delete_pos}")
    adds = []
    deletes = []
    for add_p in add_pos:
        # Now not to add -1 to get index of prev as 0th loc has startOfFile.
        add_after = self_crdt.order[add_p[0]]
        data = add_p[1]
        current = self_crdt.self_next_index()
        add = (data, current, add_after)
        adds.append(add)
        self_crdt.add_element(add)

    for delete_p in delete_pos:
        # +1 as 0th loc is for startOfFile so actual index starts from 1
        delete = self_crdt.order[delete_p+1]
        deletes.append(delete)
        self_crdt.delete_element(delete)

    for add in adds:
        print(f"ADD data: {add[0]}; current: {add[1]}; addAfter: {add[2]}")
    for delete in deletes:
        print(f"DELETE index: {delete};")
    print('\n MY USER:')
    self_crdt.print_crdt()

    return adds, deletes


def connect():
    pass


def send(old_text, new_text):
    add_pos, delete_pos = get_CRDT_commands(old_text, new_text)


def recieve():
    add_pos, delete_pos = 3, 4
    for add_p in add_pos:
        myUser.add_element(add_p)

    for delete_p in delete_pos:
        myUser.delete_element(delete_p)


# https://stackoverflow.com/questions/47391774/python-send-and-receive-objects-through-sockets
