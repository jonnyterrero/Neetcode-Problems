class Solution {
public:
    ListNode* reverseList(ListNode* head) {

        // prev represents the already-reversed portion.
        // Initially there is no previous node.
        ListNode* prev = nullptr;

        // curr is the node we are currently processing.
        ListNode* curr = head;

        while (curr != nullptr) {

            // 1. Save the next node before breaking the link.
            ListNode* next = curr->next;

            // 2. Reverse the current node's pointer.
            curr->next = prev;

            // 3. Move prev forward to the current node.
            prev = curr;

            // 4. Move curr forward using the saved pointer.
            curr = next;
        }

        // prev now points to the old tail,
        // which is the new head.
        return prev;
    }
};