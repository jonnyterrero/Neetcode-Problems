#include <unordered_map>
#include <vector>
#include <string>
#include <utility>

using namespace std;

class TimeMap {
private:
    // key -> list of {timestamp, value}
    unordered_map<string, vector<pair<int, string>>> store;

public:
    TimeMap() {
    }

    void set(string key, string value, int timestamp) {
        // Timestamps arrive in strictly increasing order,
        // so push_back keeps this vector sorted by timestamp.
        store[key].push_back({timestamp, value});
    }

    string get(string key, int timestamp) {
        // If this key has never been stored,
        // there cannot be a valid value.
        if (store.find(key) == store.end()) {
            return "";
        }

        vector<pair<int, string>>& values = store[key];

        int left = 0;
        int right = static_cast<int>(values.size()) - 1;

        string answer = "";

        while (left <= right) {
            int mid = left + (right - left) / 2;

            int storedTimestamp = values[mid].first;

            if (storedTimestamp <= timestamp) {
                // This is a valid answer.
                answer = values[mid].second;

                // Search right for a later valid timestamp.
                left = mid + 1;
            }
            else {
                // Timestamp is too large.
                // Search earlier entries.
                right = mid - 1;
            }
        }

        return answer;
    }
};