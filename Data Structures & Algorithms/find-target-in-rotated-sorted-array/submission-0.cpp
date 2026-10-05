class Solution {
public:
    int search(vector<int>& nums, int target) {

        // Search boundaries
        int left = 0;
        int right = nums.size() - 1;

        while (left <= right) {

            // Find the middle index.
            // This form avoids potential overflow from (left + right) / 2.
            int mid = left + (right - left) / 2;

            // Target found.
            if (nums[mid] == target) {
                return mid;
            }

            // CASE 1:
            // Left half [left ... mid] is sorted.
            if (nums[left] <= nums[mid]) {

                // Check whether target lies inside the sorted left half.
                if (nums[left] <= target && target < nums[mid]) {

                    // Target must be to the left.
                    right = mid - 1;

                } else {

                    // Target must be to the right.
                    left = mid + 1;
                }
            }

            // CASE 2:
            // Right half [mid ... right] is sorted.
            else {

                // Check whether target lies inside the sorted right half.
                if (nums[mid] < target && target <= nums[right]) {

                    // Target must be to the right.
                    left = mid + 1;

                } else {

                    // Target must be to the left.
                    right = mid - 1;
                }
            }
        }

        // Search space is empty, so target does not exist.
        return -1;
    }
};