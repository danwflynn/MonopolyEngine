from space import Space


class Node:
    def __init__(self, space: Space):
        self.space = space
        self.next = None
        self.prev = None


class CircularLinkedList:
    def __init__(self):
        self.head = None

    def append(self, space: Space):
        new_node = Node(space)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
            new_node.prev = self.head
        else:
            temp = self.head.prev
            temp.next = new_node
            new_node.prev = temp
            new_node.next = self.head
            self.head.prev = new_node

    def __str__(self):
        if not self.head:
            return "Empty Circular Linked List"
        result = []
        temp = self.head
        while True:
            result.append(str(temp.space.name))
            temp = temp.next
            if temp == self.head:
                break
        return " ->\n".join(result)

