class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups={}

        for word in strs:
            # 26 slots for letters a through z
            count =[0] *26

            #Count each character in the word
            for char in word:
                index = ord(char) - ord ('a')
                count[index] +=1

            #Lists connot be dictionary kets, so conver to tuples
            key = tuple(count)
            
            # Add word to the correct anagram group
            if key not in groups:
                groups[key] =[]

            groups[key].append(word)
        # Return only the grouped lists
        return list(groups.values())