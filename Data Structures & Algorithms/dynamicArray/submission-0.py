class DynamicArray:

    def __init__(self, capacity: int):
        # capacity: number of slots allocated in the backing array
        # size:     number of elements logically stored
        self.capacity = capacity
        self.size = 0
        self.arr = [0] * self.capacity   # backing array, pre-allocated

    def get(self, i: int) -> int:
        # Direct index into backing array — O(1)
        return self.arr[i]

    def set(self, i: int, n: int) -> None:
        # Overwrite slot i — O(1)
        self.arr[i] = n

    def pushback(self, n: int) -> None:
        # If full, double capacity first (amortized O(1))
        if self.size == self.capacity:
            self.resize()
        self.arr[self.size] = n
        self.size += 1

    def popback(self) -> int:
        # Decrement size to logically remove last element — O(1)
        self.size -= 1
        return self.arr[self.size]   # element still physically present

    def resize(self) -> None:
        # Allocate new array of double capacity, copy, swap — O(n)
        self.capacity *= 2
        new_arr = [0] * self.capacity
        for i in range(self.size):
            new_arr[i] = self.arr[i]
        self.arr = new_arr           # old array is garbage collected

    def getSize(self) -> int:
        return self.size

    def getCapacity(self) -> int:
        return self.capacity