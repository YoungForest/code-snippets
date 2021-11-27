class Solution {
    using ll = long long;
public:
    int minimumSize(vector<int>& nums, int maxOperations) {
        sort(nums.begin(), nums.end(), greater<int>());
        ll hi = nums[0];
        ll lo = 1;
        auto binary = [&](ll lo, ll hi, function<bool(const ll)> predicate) -> ll {
            // return first true
            while (lo < hi) {
                ll mid = lo + (hi - lo) / 2;
                if (predicate(mid)) {
                    hi = mid;
                } else {
                    lo = mid + 1;
                }
            }
            return lo;
        };
        auto pred = [&](const ll x) -> bool {
            int ans = 0;
            for (int i : nums) {
                ans += (i - 1) / x;
            }
            return ans <= maxOperations;
        };
        return binary(lo, hi, pred);
    }
};
