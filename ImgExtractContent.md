Fenwick Tree는 Segment Tree와 유사한 구간 합을 빠르게 구할 수 있는 자료구조로, Segment Tree와 같은 시간복잡도인 O(logN)을 가지지만 공간복잡도가 더 적은 특징을 가지고 있습니다. Fenwick Tree는 홀수 인덱스만을 이용하여 구현되며, BIT 연산을 통해 0이 아닌 최하위 비트를 구하여 구간의 합을 구합니다. Fenwick Tree에는 sum(idx)와 update(idx, val)이라는 두 가지 기능이 있으며, 이를 통해 구간의 합을 구하거나 배열의 값을 업데이트할 수 있습니다. 또한, Range Update와 Point Query를 통해 특정 구간의 값을 업데이트하거나 특정 지점의 값을 구할 수 있습니다.

위의 내용을 바탕으로 Fenwick Tree를 응용한 코드는 다음과 같습니다.

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

또한, Fenwick Tree를 응용한 문제의 코드는 다음과 같습니다.

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

이와 같이 Fenwick Tree를 응용한 코드를 통해 구간 합을 빠르게 구할 수 있으며, 다양한 문제에 적용할 수 있습니다. Fenwick Tree는 구간 합을 빠르게 구할 수 있는 자료구조로, Segment Tree와 같은 시간복잡도인 O(logN)을 가지지만 공간복잡도가 더 적은 특징을 가지고 있습니다. 또한, Fenwick Tree를 응용한 코드를 통해 구간의 합을 구하거나 배열의 값을 업데이트할 수 있으며, Range Update와 Point Query를 통해 특정 구간의 값을 업데이트하거나 특정 지점의 값을 구할 수 있습니다.