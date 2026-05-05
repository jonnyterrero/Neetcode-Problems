class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None

class LinkedList:
    def __init__(self):
        """
        Initialize an empty singly linked list.
        we use a dummy node to simplify insertion/removal at the head.
        """     
        self.head = ListNode(-1) #dummy node
        self.tail = self.head   #tail starts at dummy beccause of list
        self.size = 0

    def get (self, i):
        """
        Return the value of the ith node, 0-indexed.
        If i is out of bounds, return -1.
        """
        if i < 0 or i >= self.size:
            return -1

        curr = self.head.next #first real node

        for _ in range(i):
            curr = curr.next
        return curr.val

    def insertHead(self, val):
        """
        Insert a new node at the head of the list.
        """
        new_node = ListNode(val)

        # Insert directly after dummy
        new_node.next = self.head.next
        self.head.next = new_node

        #If this was the first real node, it is also the tail
        if self.size == 0:
            self.tail = new_node
        self.size += 1

    def insertTail(self, val):
        """
        Insert a new node at the tail of the list.
        """
        new_node = ListNode(val)
        self.tail.next = new_node
        self.tail = new_node
        self.size += 1

    def remove(self, i):
        """
        Remove the ith node, 0-indexed.
        Return True if removal succeeds.
        Return false if index is out of bounds.
        """
        if i < 0 or i >= self.size:
            return False
        prev = self.head

        #move prev to node before index i
        for _ in range(i):
            prev = prev.next
        node_to_remove = prev.next
        prev.next = node_to_remove.next
        # If we removed the tail, update tail
        if node_to_remove == self.tail:
            self.tail = prev

        self.size -= 1
        return True
        
    def getValues(self):
        """
        Return all linked list values from head to tail as an arry.
        """
        values = []
        curr = self.head.next

        while curr:
            values.append(curr.val)
            curr = curr.next
        return values