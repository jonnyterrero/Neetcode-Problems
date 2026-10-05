#include <algorithm>
#include <climits>
#include <vector>

using namespace std;

class Solution {
public:
    double findMedianSortedArrays(vector<int>& nums1,
                                  vector<int>& nums2) {
        // Always binary-search the smaller array.
        // This guarantees O(log(min(m, n))) time.
        if (nums1.size() > nums2.size()) {
            return findMedianSortedArrays(nums2, nums1);
        }

        const int m = static_cast<int>(nums1.size());
        const int n = static_cast<int>(nums2.size());

        // We are searching for how many elements from nums1
        // should belong to the combined left half.
        int left = 0;
        int right = m;

        while (left <= right) {
            // i = number of nums1 elements placed on the left.
            const int i = left + (right - left) / 2;

            // j = number of nums2 elements placed on the left.
            // Together, i + j must contain half the total data.
            const int j = (m + n + 1) / 2 - i;

            // Boundary values around the partition in nums1.
            const int Aleft =
                (i == 0) ? INT_MIN : nums1[i - 1];

            const int Aright =
                (i == m) ? INT_MAX : nums1[i];

            // Boundary values around the partition in nums2.
            const int Bleft =
                (j == 0) ? INT_MIN : nums2[j - 1];

            const int Bright =
                (j == n) ? INT_MAX : nums2[j];

            // Correct partition:
            //
            // every value on the combined left side
            // is <= every value on the combined right side.
            if (Aleft <= Bright && Bleft <= Aright) {

                // Odd total:
                // the left side contains one extra value,
                // so its maximum is the median.
                if ((m + n) % 2 == 1) {
                    return static_cast<double>(
                        max(Aleft, Bleft)
                    );
                }

                // Even total:
                // median = average of the two middle values.
                const int leftMax =
                    max(Aleft, Bleft);

                const int rightMin =
                    min(Aright, Bright);

                return (
                    static_cast<double>(leftMax) +
                    static_cast<double>(rightMin)
                ) / 2.0;
            }

            // Too many nums1 values are on the left.
            // Move nums1's partition to the left.
            if (Aleft > Bright) {
                right = i - 1;
            }

            // Too few nums1 values are on the left.
            // Move nums1's partition to the right.
            else {
                left = i + 1;
            }
        }

        // Given valid sorted input, execution should never reach here.
        return 0.0;
    }
};