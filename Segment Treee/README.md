线段树(Segment Tree)擅长处理区间。线段树是一棵完美二叉树，树上的每个节点都维护一个区间。根维护的是整个区间，每个节点维护的是父亲的区间二等分后的其中一个子区间。对区间的操作的时间复杂度为`O(log n)`。

## 基于节点的线段树

[LC307](https://leetcode-cn.com/problems/range-sum-query-mutable)

```cpp
class SegmentTreeNode {
private:
    unique_ptr<SegmentTreeNode> left = nullptr, right = nullptr;
    int start = 0, end = 0;
    int val = 0;
public:
    SegmentTreeNode(int value, int start_, int end_): val(value), start(start_), end(end_) {}
    SegmentTreeNode(int start_, int end_): start(start_), end(end_) {}
    static unique_ptr<SegmentTreeNode> buildTree(const vector<int>& nums, int i, int j) {
        if (i == j) {
            return make_unique<SegmentTreeNode>(nums[i], i, j);
        } else {
            int mid = i + (j - i) / 2;
            auto ret = make_unique<SegmentTreeNode>(i, j);
            ret->left = buildTree(nums, i, mid);
            ret->right = buildTree(nums, mid + 1, j);
            ret->val = ret->left->val + ret->right->val;
            return ret;
        }
    }
    int queryRange(int i, int j) const {
        if (i == start && j == end) {
            return val;
        } else {
            int mid = start + (end - start) / 2;
            if (j <= mid) {
                return left->queryRange(i, j);
            } else if (i > mid) {
                return right->queryRange(i, j);
            } else {
                return left->queryRange(i, mid) + right->queryRange(mid + 1, j);
            }
        }
    }
    void update(int index, int value) {
        if (start == index && index == end) {
            val = value;
        } else {
            int mid = start + (end - start) / 2;
            if (mid >= index) {
                left->update(index, value);
            } else {
                right->update(index, value);
            }
            val = left->val + right->val;
        }
    }
};

class NumArray {
    unique_ptr<SegmentTreeNode> root = nullptr;
    int n = 0;
public:
    NumArray(vector<int>& nums) {
        if (nums.empty()) return;
        n = nums.size();
        root = SegmentTreeNode::buildTree(nums, 0, nums.size() - 1);
    }
    
    void update(int i, int val) {
        if (i >= n || i < 0) return;
        root->update(i, val);
    }
    
    int sumRange(int i, int j) {
        if (i < 0 || j >= n || j < i) return 0;
        return root->queryRange(i, j);
    }
};

/**
 * Your NumArray object will be instantiated and called as such:
 * NumArray* obj = new NumArray(nums);
 * obj->update(i,val);
 * int param_2 = obj->sumRange(i,j);
 */
```

## 更通用的模版，max sum min

```cpp
class SegmentTreeNode {
    private:
        unique_ptr<SegmentTreeNode> left = nullptr, right = nullptr;
        int start = 0, end = 0;
        int val = 0;
        static int op(int a, int b) {
            return min(a, b);
        }
    public:
        SegmentTreeNode(int value, int start_, int end_): val(value), start(start_), end(end_) {}
        SegmentTreeNode(int start_, int end_): start(start_), end(end_) {}
        static unique_ptr<SegmentTreeNode> buildTree(const vector<int>& nums, int i, int j) {
            if (i == j) {
                return make_unique<SegmentTreeNode>(nums[i], i, j);
            } else {
                int mid = i + (j - i) / 2;
                auto ret = make_unique<SegmentTreeNode>(i, j);
                ret->left = buildTree(nums, i, mid);
                ret->right = buildTree(nums, mid + 1, j);
                ret->val = op(ret->left->val, ret->right->val);
                return ret;
            }
        }
        int queryRange(int i, int j) const {
            if (i == start && j == end) {
                return val;
            } else {
                int mid = start + (end - start) / 2;
                if (j <= mid) {
                    return left->queryRange(i, j);
                } else if (i > mid) {
                    return right->queryRange(i, j);
                } else {
                    return op(left->queryRange(i, mid), right->queryRange(mid + 1, j));
                }
            }
        }
        void update(int index, int value) {
            if (start == index && index == end) {
                val = value;
            } else {
                int mid = start + (end - start) / 2;
                if (mid >= index) {
                    left->update(index, value);
                } else {
                    right->update(index, value);
                }
                val = op(left->val, right->val);
            }
        }
    };
```

## 返回下标的线段树

```cpp
using pii = pair<int, int>;
class SegmentTreeNode {
private:
    unique_ptr<SegmentTreeNode> left = nullptr, right = nullptr;
    int start = 0, end = 0;
    pii val = {0, 0};
    static pii op(pii a, pii b) {
        return min(a, b);
    }
public:
    SegmentTreeNode(pii value, int start_, int end_): val(value), start(start_), end(end_) {}
    SegmentTreeNode(int start_, int end_): start(start_), end(end_) {}
    static unique_ptr<SegmentTreeNode> buildTree(const vector<pii>& nums, int i, int j) {
        if (i == j) {
            return make_unique<SegmentTreeNode>(nums[i], i, j);
        } else {
            int mid = i + (j - i) / 2;
            auto ret = make_unique<SegmentTreeNode>(i, j);
            ret->left = buildTree(nums, i, mid);
            ret->right = buildTree(nums, mid + 1, j);
            ret->val = op(ret->left->val, ret->right->val);
            return ret;
        }
    }
    pii queryRange(int i, int j) const {
        if (i == start && j == end) {
            return val;
        } else {
            int mid = start + (end - start) / 2;
            if (j <= mid) {
                return left->queryRange(i, j);
            } else if (i > mid) {
                return right->queryRange(i, j);
            } else {
                return op(left->queryRange(i, mid), right->queryRange(mid + 1, j));
            }
        }
    }
    void update(int index, pii value) {
        if (start == index && index == end) {
            val = value;
        } else {
            int mid = start + (end - start) / 2;
            if (mid >= index) {
                left->update(index, value);
            } else {
                right->update(index, value);
            }
            val = op(left->val, right->val);
        }
    }
};
class Solution {
public:
    int minNumberOperations(vector<int>& target) {
        const int n = target.size();
        vector<pii> targetIndex;
        targetIndex.reserve(n);
        for (int i = 0; i < n; ++i) {
            targetIndex.push_back({target[i], i});
        }
        auto st = SegmentTreeNode::buildTree(targetIndex, 0, n - 1);
        int ans = 0;
        function<void(const int, const int, const int)> divide = [&](const int left, const int right, const int base) -> void {
            if (left > right) return;
            else if (left == right) {
                ans += target[left] - base;
            } else {
                auto [midValue, midIndex] = st->queryRange(left, right);
                ans += target[midIndex] - base;
                divide(left, midIndex - 1, target[midIndex]);
                divide(midIndex + 1, right, target[midIndex]);
            }
        };
        divide(0, n - 1, 0);
        return ans;
    }
};
```

## Range Minimum Query (RMQ)

```cpp
#include<limits>
#include<algorithm>

using namespace std;

const int MAX_N = 1 << 17;

// 存储线段树的全局数组
int n, dat[2 * MAX_N - 1];

// 初始化
void init(int n_) {
    // 为简单起见，把元素个数扩大到2的幂
    n = 1;
    while (n < n_) n *= 2;

    // 把所有的值都设为INT_MAX
    for (int i = 0; i < 2 * n - 1; i++) {
        dat[i] = numeric_limits<int>::max();
    }
}

// 把第k个值(0-indexed)更新为a
void update(int k, int a) {
    // 叶子节点
    k += n - 1;
    dat[k] = a;
    // 向上更新
    while (k > 0) {
        k = (k - 1) / 2;
        dat[k] = min(dat[2 * k + 1], dat[2 * k + 2]);
    }
}

// 求[a, b)的最小值
// 后面的参数是为了计算起来方便而转入的。
// k 是节点的编号, l, r表示这个节点对应的是[l, r)区间。
// 在外部调用时，用query(a, b, 0, 0, n)
int query(int a, int b, int k, int l, int r) {
    // 如果[a, b) 和 [l, r)不相交，则返回INT_MAX
    if (r <= a || b <= l)
        return numeric_limits<int>::max();
    // 如果[a, b)完全包含[1, r), 则返回当前节点的值
    if (a <= l && r <= b)
        return dat[k];
    else {
        // 否则返回两个儿子中值的较小者
        int vl = query(a, b, k * 2 + 1, l, l + (r - l) / 2);
        int vr = query(a, b, k * 2 + 2, l + (r - l) / 2, r);
        return min(vl, vr);
    }
}
```

## 基于稀疏表(Sparse Table)的线段树

查询效率`O(1)`,
预处理的时间空间复杂度均为`O(nlogn)`,
更新也不高效。
