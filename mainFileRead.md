# Concept
- `Binary Indexed Tree(BIT)`라고도 불린다.
- [[Segment Tree]]의 변형 트리로 구간의 합을 빠르게 구할 수 있다는 특징이 있다.
- 시간복잡도는 Segment Tree와 같은 `O(logN)`이지만 공간복잡도는 `O(n)`으로 Segment Tree보다 더 적다.
- 시간복잡도 자체는 Segment Tree와 같다고 해도 실제론 조금 더 빠르게 작동하게 되는데 선형적으로 `Lazy Segment Tree ≒ 2 * Segment Tree / Segment Tree ≒ 2 * Fenwick Tree`이다.
# Fenwick Tree 원리
- Fenwick Tree는 Segment Tree에서 홀수 인덱스만 표기한다.(밑 그림 참조)
- 모든 구간들은  BIT 연산을 통해 0이 아닌 최하위 비트(같은 높이의 맨좌측 비트)를 구함으로써 해결할 수 있다. 
- 특정 비트(I)를 통해 최하위 비트를 구하는 공식은 `i & -i (-i = ~i + 1)`이다.
- ex) i = (1101)2 -> ~i = (0010)2 -> -i = (0011)2 -> i & -i = (0001)2
#### 🖼️Segment Tree와 Fenwick Tree 구조 비교
![[Fenwick Tree Struct Graph.svg]]
- Fenwick Tree에 필요한 기능은 크게 2가지가 있다.
	1. sum(idx) : `[1~idx]` 범위에 있는 값들의 합을 Return 한다.
	2. update(idx, val) :  배열의 idx번째와 해당 idx에 해당되는 모든 구간 값을 업데이트 한다.
- 특정 비트(i)에 최하위 비트가 0이 되기 전까지 빼면 구간의 합을 구할 수 있다. `i -= (i & -i)`
- 특정 비트(i)에 최하위 비트가 특정 값(m) 될 때까지 더하면 구간을 업데이트  할 수 있다. `i += (i & -i)`
- 특정 구간 `[l,r]`의 합을 구하기 위해서 **sum(r) - sum(l-1)** 로 계산한다.
- sum을 하는 과정은 오른쪽 대각선으로 올라가는 것이고, update는 왼쪽 위로 올라가는 과정으로 생각하면 이해하기 편하다.
- Range Update 즉, `[l,r]` 의 값에 k를 더하기 하기 위해서 **update(l,k) , update(r+1, -k)** 료 계산한다.
	- 이러한 계산은 Point Query`(array[idx])`를 편하게 구하기 위함이다.
	- Point Query 을 구하기 위해선 단순히 sum(idx)을 구하면 된다.
	- update(l,k)는 `[l,m]`까지의 모든 부분 합에 k를 더하기 된다. 
	- update(r+1, -k)는 `[r+1,m]까지의 모든 부분 합에 -k를 더하기 된다. 
	- 두 개의 연산을 통해 `l~r`까지의 부분 합만 k가 더해지게 된다.
#### 🖼️그림으로 이해하기(Partial Sum)
![[Fenwick Tree Partial Sum Graph.svg]]
#### 🖼️그림으로 이해하기(Range Update & Point Query)
![[Fenwick Tree Range Update & Point Query Graph.svg]]
# Fenwick Tree CODE
- BIT 연산만 이해한다면 구현하는데 큰 어려움은 없다.
- 부분 합과 구간 합을 잘 구별하며 구현하여야 한다.
- Segment Tree보다 속도 측면에서 빠르지만 응용력이 떨어져 많은 문제에서 사용되진 않는다.
#### ⌨️ Code(Partial sum)
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, q, fenwickTree[100001];

void fenwickTree_Update(int idx, int val) {
    while ( idx <= n ) {
        fenwickTree[idx] += val;
        idx += (idx & -idx);
    }
}

int fenwickTree_Sum(int idx) {
    int result = 0;
    while ( idx > 0 ) {
        result += fenwickTree[idx];
        idx -= (idx & -idx);
    }
    return result;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n >> q;
    
    while ( q-- ) {
        int cmd;
        cin >> cmd;
        if ( cmd == 1 ) {
            int idx, val;
            cin >> idx >> val;
            fenwickTree_Update(idx, val);
        } else if ( cmd == 2 ) {
            int idx;
            cin >> idx;
            cout << fenwickTree_Sum(idx) << '\n';
        }
    }
    return 0;
}
```
##### ❓ 예제 Input
	8 8
	1 3 10
	1 2 5
	1 5 5
	1 8 7
	2 3
	2 5
	3 4 5
	3 1 8
##### ⭐ 예제 Output
	15
	20
	5
	27
#### ⌨️ Code(Range Update & Point Query)

```cpp
#include <bits/stdc++.h>

using namespace std;

int n, q, fenwickTree[100001];

void fenwickTree_Update(int idx, int val) {
    while ( idx <= n ) {
        fenwickTree[idx] += val;
        idx += (idx & -idx);
    }
}

int fenwickTree_Sum(int idx) {
    int result = 0;
    while ( idx > 0 ) {
        result += fenwickTree[idx];
        idx -= (idx & -idx);
    }
    return result;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n >> q;
    while ( q-- ) {
        int cmd;
        cin >> cmd;
        if ( cmd == 1 ) {
            int l, r, val;
            cin >> l >> r >> val;
            fenwickTree_Update(l, val);
            fenwickTree_Update(r+1, -val);
        } else if ( cmd == 2 ) {
            int idx;
            cin >> idx;
            cout << fenwickTree_Sum(idx) << '\n';
        }
    }
    return 0;
}
```
##### ❓ 예제 Input
	8 7
	1 1 5 10
	2 5
	1 2 2 5
	2 2
	1 1 8 7
	2 1
	2 2
##### ⭐ 예제 Output
	10
	15
	17
	22
# Fenwick Tree 응용문제
### 📑[8217 - 유성](https://www.acmicpc.net/problem/8217)
#### 🔓 KeyPoint
- [[PBS(Parallel Binary Search)]]에 Fenwick Tree을 응용한 문제이다.
- 구간의 합이 쿼리가 주어질 때 이를 이용하여 각 국가의 할당량이 몇 번째 쿼리가 될 때 채워지는지를 구하면 된다.
- 각 국가마다 `특정 일(D) 안에 할당량을 채울 수 있는가?`라는 이분 탐색을 병렬로 진행하면 문제를 풀 수 있다.
- 이분 탐색을 진행하는 과정에서 할당량을 구하기 위해 [[Lazy Segment Tree]]을 사용하게 되면 **시간 초과**기 된다.
- 시간 초과를 해결하기 위해 Lazy가 아닌 Fenwick Tree를 이용하면 이를 해결할 수 있다.
- Fenwick 중 구간의 합을 구하기기 때문에 Range Update & Point Query을 이용한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, m, q, countryQuota[300001];
long long fenwickTree[300001];
pair<int,int> queryRange[300001];
tuple<bool,int,int,long long> query[300001];
vector<int> countryArea[300001], queryMidValue[300001];

void fenwickTree_Update(int idx, long long val) {
    while ( idx <= m ) {
        fenwickTree[idx] += val;
        idx += (idx & -idx);
    }
}

long long fenwickTree_Sum(int idx) {
    long long result = 0;
    while ( idx > 0 ) {
        result += fenwickTree[idx];
        idx -= (idx & -idx);
    }
    return result;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n >> m;
    for ( int i = 1; i <= m; i++ ) {
        int num;
        cin >> num;
        countryArea[num].push_back(i);
    }
    
    for ( int i = 1; i <= n; i++ ) cin >> countryQuota[i];
    
    cin >> q;
    for ( int i = 1; i <= q; i++ ) {
        int l, r;
        long long a;
        bool isLeftBiggerThanRight = false;
        cin >> l >> r >> a;
        if ( l > r ) {
            isLeftBiggerThanRight = true;
            swap(l, r);
        }
        query[i] = {isLeftBiggerThanRight, l, r, a};
    }
    
    for ( int i = 1; i <= n; i++ ) {
        queryRange[i].first = 1; queryRange[i].second = q + 1;
    }
    
    while ( 1 ) {
        bool flag = false;
        memset(fenwickTree, 0, sizeof(fenwickTree));
        
        for ( int i = 0; i <= q; i++ ) queryMidValue[i].clear();
        
        for ( int i = 1; i <= n; i++ ) {
            if ( queryRange[i].first < queryRange[i].second ) {
                flag = true;
                int mid = (queryRange[i].first + queryRange[i].second) / 2;
                queryMidValue[mid].push_back(i);
            }
        }
        
        if ( !flag ) break;
        
        for ( int i = 1; i <= q; i++ ) {
            bool isLeftBiggerThanRight = get<0>(query[i]);
            int queryL = get<1>(query[i]);
            int queryR = get<2>(query[i]);
            long long queryVal = get<3>(query[i]);
            
            if ( isLeftBiggerThanRight ) {
                fenwickTree_Update(1, queryVal);
                fenwickTree_Update(queryL+1, -queryVal);
                fenwickTree_Update(queryR, queryVal);
            } else {
                fenwickTree_Update(queryL, queryVal);
                fenwickTree_Update(queryR + 1, -queryVal);
            }
            
            for ( auto nodeIdx : queryMidValue[i] ) {
                long long result = 0;
                for ( auto node : countryArea[nodeIdx] ) {
                    result += fenwickTree_Sum(node);
                    if ( result >= countryQuota[nodeIdx] ) break;
                }
                if ( result >= countryQuota[nodeIdx] ) queryRange[nodeIdx].second = i;
                else queryRange[nodeIdx].first = i+1;
            }
        }
    }
    
    for ( int i = 1; i <= n; i++ ) {
        if ( queryRange[i].first == q + 1 ) cout << "NIE\n";
        else cout << queryRange[i].first << '\n';
    }
    return 0;
}
```
### 📑[15957 - 음악추천](https://www.acmicpc.net/problem/15957)
#### 🔓 KeyPoint
- 마찬가지로 [[PBS(Parallel Binary Search)]]에서 Fenwick Tree를 응용하는 문제이다.
- 문제의 조건이 매우 많고 복잡하기 때문에 여러 개의 틀로 문제를 나누어 푸는 것이 좋다.
- 주어지는 값들이 Tree 형태로 주어져있고 해당 Tree에 구간의 합을 적용해야 하기 때문에 [[ETT(Euler Tour Technique)]]을 적용해야 한다.
- 최종적으로 구하는 것이 **목표점수를 초과하는 시점** 이기 떄문에 각각의 가수들이 `특정 시점(K)에 목표 점수를 넘는가?`를 이분탐색 기준으로 잡고 이분 병렬 탐색을 진행하여야 한다.
- Fenwick Tree에서 각 Point 값을 sum하는 과정에서 이미 목표 점수를 넘었으면 계산을 더 이상 하지 않고 값을 넘겨야 시간 초과를 방지할 수 있다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>
#define maxLen 100001

using namespace std;

int n, k, ettCnt = 0, s[maxLen], e[maxLen], singers[maxLen], subTreeRoot[maxLen];
long long j, queryWeight[maxLen], fenwickTree[maxLen];
pair<int,int> queryRange[maxLen];
vector<int> tree[maxLen], songsBasedSinger[maxLen], queryMidValue[maxLen];
vector<pair<long long, int>> query;

void fenwickTree_Update(int idx, long long val) {
    while ( idx <= n ) {
        fenwickTree[idx] += val;
        idx += (idx & -idx);
    }
}

long long fenwickTree_Sum(int idx) {
    long long result = 0;
    while ( idx > 0 ) {
        result += fenwickTree[idx];
        idx -= (idx & -idx);
    }
    return result;
}

void ett(int node) {
    s[node] = ++ettCnt;
    for ( auto nNode : tree[node] ) {
        if ( s[nNode] == 0 ) ett(nNode);
    }
    e[node] = ettCnt;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    cin >> n >> k >> j;
    for ( int i = 2; i <= n; i++ ) {
        int root;
        cin >> root;
        tree[root].push_back(i);
    }
    
    ett(1);
    
    for ( int i = 1; i <= n; i++ ) {
        cin >> singers[i];
        songsBasedSinger[singers[i]].push_back(i);
    }
    
    query.push_back({-1, -1});
    for ( int i = 1; i <= k; i++ ) {
        long long dateTime;
        cin >> dateTime >> subTreeRoot[i] >> queryWeight[i];
        query.push_back({dateTime, i});
    }
    sort(query.begin(), query.end());
    
    for ( int i = 1; i <= k; i++ ) {
        queryRange[i].first = ((int)songsBasedSinger[i].size() == 0 ) ? k+1 : 1;
        queryRange[i].second = k+1;
    }
    
    while ( 1 ) {
        bool flag = false;
        for ( int i = 1; i <= k; i++ ) queryMidValue[i].clear();
        memset(fenwickTree, 0, sizeof(fenwickTree));
        
        for ( int i = 1; i <= k; i++ ) {
            int l = queryRange[i].first, r = queryRange[i].second;
            if ( l < r ) {
                flag = true;
                int mid = (l + r) / 2;
                queryMidValue[mid].push_back(i);
            }
        }
        
        if ( !flag ) break;
        
        for ( int i = 1; i <= k; i++ ) {
            int queryIdx = query[i].second;
            int root = subTreeRoot[queryIdx];
            long long weight = queryWeight[queryIdx];
            
            long long avgWeight = weight / (e[root] - s[root] + 1);
            fenwickTree_Update(s[root], avgWeight);
            fenwickTree_Update(e[root] + 1, -avgWeight);
            
            for ( auto singerIdx : queryMidValue[i] ) {
                long long result = 0;
                int songsCnt = (int)songsBasedSinger[singerIdx].size();
                for ( auto song : songsBasedSinger[singerIdx] ) {
                    result += fenwickTree_Sum(s[song]);
                    if ( result > j * songsCnt ) break;
                }
                if ( result > j * songsCnt ) queryRange[singerIdx].second = i;
                else queryRange[singerIdx].first = i+1;
            }
        }
    }
    
    for ( int i = 1; i <= n; i++ ) {
        int queryIdx = queryRange[singers[i]].first;
        if