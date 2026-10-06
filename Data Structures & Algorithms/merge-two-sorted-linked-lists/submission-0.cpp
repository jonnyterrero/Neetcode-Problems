class Solution {
public:
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        
        // Temporary node placed before the actual merged list.
        ListNode dummy;

        // tail always points to the last node in the merged list.
        ListNode* tail = &dummy;

        // Continue while both lists still contain nodes.
        while (list1 != nullptr && list2 != nullptr) {

            // Choose the smaller current node.
            if (list1->val <= list2->val) {

                // Attach list1's current node.
                tail->next = list1;

                // Move list1 forward.
                list1 = list1->next;

            } else {

                // Attach list2's current node.
                tail->next = list2;

                // Move list2 forward.
                list2 = list2->next;
            }

            // Move tail to the node we just attached.
            tail = tail->next;
        }

        // At least one list is now empty.
        // Attach whichever list still contains nodes.
        if (list1 != nullptr) {
            tail->next = list1;
        } else {
            tail->next = list2;
        }

        // dummy itself is not part of the answer.
        return dummy.next;
    }
};