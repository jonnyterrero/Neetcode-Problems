# Definition for a pair.
# class Pair:
#     def __init__(self, key: int, value: str):
#         self.key = key
#         self.value = value
class Solution:
    def insertionSort(self, pairs: List[Pair]) -> List[List[Pair]]:
        result = []

        for i in range(len(pairs)):
            current = pairs[i]
            j=i-1
            
            #shift larger keys one position to the right
            while j >=0 and pairs[j].key > current.key:
                pairs[j + 1] = pairs[j]
                j -=1

            #Insert current pair into its correct position
            pairs[j + 1]= current

            #Store a copy of the current array state
            result.append(pairs[:])

        return result