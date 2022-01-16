class Solution:
    def maxRunTime(self, n: int, batteries: List[int]) -> int:
        # 5983. Maximum Running Time of N Computers
        # binary search
        # log 10^9 * n
        # check: use most battery first
        batteries.sort()
        def check(x):
            i = 0
            current = 0
            # print("x: ", x)
            for b in batteries:
                if i == n: break
                if b > x:
                    b = x
                if b >= x - current:
                    i += 1
                    current = b - (x - current)
                else:
                    current += b
                # print("state: ", i, current)
                
            return i == n
        
        lo = 0
        hi = sum(batteries) // n + 1
        # [lo, hi)
        # [t, t, t, f, f]
        # find lo == first f
        while lo < hi:
            mid = (lo + hi) // 2
            if check(mid):
                lo = mid + 1
            else:
                hi = mid
        return lo - 1 # last True
