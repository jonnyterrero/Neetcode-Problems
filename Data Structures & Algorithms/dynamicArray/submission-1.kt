class DynamicArray(capacity: Int) {

    private var capacity = capacity          // allocated slots in backing array
    private var size = 0                     // logical element count
    private var arr = IntArray(capacity)     // backing array, pre-allocated with 0s

    fun get(i: Int): Int {
        return arr[i]
    }

    fun set(i: Int, n: Int) {
        arr[i] = n
    }

    fun pushback(n: Int) {
        if (size == capacity) {
            resize()
        }
        arr[size] = n
        size++
    }

    fun popback(): Int {
        size--
        return arr[size]
    }

    fun resize() {
        capacity *= 2
        val newArr = IntArray(capacity)
        for (i in 0 until size) {
            newArr[i] = arr[i]
        }
        arr = newArr
    }

    fun getSize(): Int = size

    fun getCapacity(): Int = capacity
}