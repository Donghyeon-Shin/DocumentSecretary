# Concept
- 길이가 N인 수열(배열)이 있을 때 구간을 **√n**개인 그룹으로 나누고 특정 쿼리를 수행하는 알고리즘이다.
- 쿼리를 이용하는 문제에서 가끔 사용되며 구간에 대해 `변경, 계산`에 대해 O(√n)의  시간복잡도가 소요된다.
# Square Root Decomposition 원리
- 배열 `A[]`을 √n개로 나누어 그룹  `Group[]` 배열로 해당 구간의 특정 값(Ex 총합, 최댓값, 최솟값)을 관리한다.
- 특정 구간 `[S,E]`가 있을 때 해당되는 `Group[]`에 구간은 `[S/√n or E/√n]`으로 표현할 수 있다.
- `Square Root Decomposition` 연산은 특정 Idx의 `A[]`값을 바꾸는 **변경**과 구간`[l,r]`에서 특정 값을 구하는 **계산**으로 나눌 수 있다.
- 배열 `A[]`의 **Idx** 위치에 값이 **v**로 변경되었을 경우(**변경**),
	>1. 배열 A[Idx] = v로 값을 수정한다.
	>2. Group의 번호를 구한다. GroupIdx = Idx / √n
	>3. Idx의 구간의 [S,E)을 구한다. S = GroupIdx * √n, E = S + √n
	>4. [S, E)까지 A[]을 탐색하면서  Group[]을 업데이트 한다.
- 구간 `[l,r]`가 주어졌을 때 특정 값을 구하는 경우(**계산**),
	>1. l과 r가 같은 구간이라면, [l,r] 구간만큼 A[]을 탐색해 특정 값을 구한다.
	>2. l과 r가 다른 구간이라면,
	>	2.1. `[l,(l/√n)*√n + √n)` 만큼 A[]을 탐색해 특정 값을 구한다.
	>	2.2. `[r/√n)*√n,r]` 만큼 A[]을 탐색해 특정 값을 구한다.
	>	2.3. l~r 사이의 구간만큼 Group[]을 탐색해 특정 값을 구한다.
#### 🖼️그림으로 이해하기
![[Square Root Decompositon Graph.svg]]
# Square Root Decomposition CODE
- 구간 `[l, s]`가 주어졌을 때, 최대 값을 구하는 문제이다.
- 처음 `group[]` 배열을 각각 그룹의 최댓값으로 초기화 해주고
- **변경**과 **계산**은 위에서 설명한 것처럼 구현한다.
- 원리만 이해하면 구현하는데 큰 어려움은 없다.
- 만약 group의 크기를 직접 정해야 하는 경우, n이 √n로 나누어 떨어지는 경우 말고는 **(√n + 1)** 로 설정해야 함에 유의하자.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int A[100001], group[100001] = {0, }, A_Cnt, G_Size, query;

void group_Init() {
    for ( int i = 0; i < A_Cnt; i++ ) {
        if ( i % G_Size == 0 ) group[i/G_Size] = A[i];
        else group[i/G_Size] = max(group[i/G_Size], A[i]);
    }
}

void changeValue(int idx, int val) {
    A[idx] = val;
    int idxGroup = idx / G_Size;
    int start = idxGroup * G_Size;
    int end = (start + G_Size) > A_Cnt ? A_Cnt : (start + G_Size);
    group[idxGroup] = A[start];
    for ( int i = start; i < end; i++ ) group[idxGroup] = max(group[idxGroup], A[i]);
}

int getMaxValueLtoR(int l, int r) {
    int maximum = A[l];
    
    if ( l / G_Size == r / G_Size ) {
        for ( int i = l + 1; i <= r; i++ ) maximum = max(maximum, A[i]);
        return maximum;
    }
    int lStart = l, lEnd = (l / G_Size) * G_Size + G_Size;
    int rStart = (r / G_Size) * G_Size, rEnd = r;
    for ( int i = lStart; i < lEnd; i++ ) maximum = max(maximum, A[i]);
    for ( int i = rStart; i <= rEnd; i++ ) maximum = max(maximum, A[i]);
    
    int gStart = l / G_Size, gEnd = r / G_Size;
    for ( int i = gStart; i <= gEnd; i++ ) maximum = max(maximum, A[i]);
    
    return maximum;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> A_Cnt;
    for ( int i = 0; i < A_Cnt; i++ ) cin >> A[i];
    G_Size = (int)sqrt(A_Cnt);
    group_Init();
    
    cin >> query;
    while ( query-- ) {
        int cmd;
        cin >> cmd;
        if ( cmd == 1 ) {
            int idx, val;
            cin >> idx >> val;
            changeValue(idx, val);
        } else {
            int l, r;
            cin >> l >> r;
            cout << getMaxValueLtoR(l, r) << '\n';
        }
    }
    return 0;
}
```
##### ❓ 예제 Input
	10
	0 1 2 3 4 5 6 7 8 9
	5
	1 5 100
	1 4 1
	2 3 7
	1 5 5
	2 0 9
##### ⭐ 예제 Output
	100
	9
# Square Root Decomposition 응용문제
### 📑[13546 - 수열과 쿼리 4](https://www.acmicpc.net/problem/13546)
#### 🔓 KeyPoint
- l <= x , y <= r && Ax = Ay같은 값 x, y에 대해서 x-y의 idx가 가장 큰 수를 구하는 쿼리를 계산하는 문제이다.
- [[Mo's]] 알고리즘으로 쿼리를 처리하면서 Ax 값을 `list[arr[x]] = Ax의 인덱스`에 넣어 해당 값의 처음 값과 끝 값을 빼 길이를 구하여 해당 길이를 cnt에 넣어 쿼리를 계산하는 방식을 이용한다.
- 1 <= Ak <= 100,000을 가지기 때문에 이를 Brute force로 구하게 될 시 시간 안에 해결 할 수 없다.
- `Square Root Decomposition`을 이용하여 cnt가 존재하는 구간을 역순으로 빠르게 찾아 구하는게 핵심이다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, sqrtN, k, m, arr[101010], cnt[101010] = {0, }, sqrtCnt[102010] = {0, }, result[101010];
list<int> pos[101010];

struct Query {
    int s, e, idx;
    Query(int S = 0, int E = 0, int Idx = 0) : s(S), e(E), idx(Idx) {}
    bool operator < (const Query &q) {
        if ( s / sqrtN != q.s / sqrtN ) return s / sqrtN < q.s / sqrtN;
        return e < q.e;
    }
};

Query query[101010];

void plusVal(int s, int e, bool isFrontPush) {
    if ( isFrontPush ) {
        s *= -1;
        e *= -1;
    }
    
    for ( int i = s; i <= e; i++ ) {
        int absI = abs(i), val;
        list<int> &dq = pos[arr[absI]];
        if ( !dq.empty() ) {
            val = dq.back() - dq.front();
            cnt[val]--; sqrtCnt[val/sqrtN]--;
        }
        
        if ( isFrontPush ) dq.push_front(absI);
        else dq.push_back(absI);
        
        val = dq.back() - dq.front();
        cnt[val]++; sqrtCnt[val/sqrtN]++;
    }
}

void minusVal(int s, int e, bool isFrontPop) {
    if ( !isFrontPop ) {
        s *= -1;
        e *= -1;
    }
    
    for ( int i = s; i <= e; i++ ) {
        int absI = abs(i), val;
        list<int> &dq = pos[arr[absI]];
        val = dq.back() - dq.front();
        cnt[val]--; sqrtCnt[val/sqrtN]--;
        
        if ( isFrontPop ) dq.pop_front();
        else dq.pop_back();
        
        if ( !dq.empty() ) {
            val = dq.back() - dq.front();
            cnt[val]++; sqrtCnt[val/sqrtN]++;
        }
    }
}

int getQueryVal() {
    for ( int i = (101010 / sqrtN + 9); i >= 0; i-- ) {
        if ( sqrtCnt[i] != 0 ) {
            for ( int j = sqrtN-1; j >= 0; j-- ) {
                if ( cnt[i * sqrtN + j] != 0 ) return i * sqrtN + j;
            }
        }
    }
    return -1;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n >> k;
    sqrtN = sqrt(n);
    for ( int i = 1; i <= n; i++ ) cin >> arr[i];
    cin >> m;
    for ( int i = 1; i <= m; i++ ) {
        int s, e;
        cin >> s >> e;
        query[i] = Query(s, e, i);
    }
    
    sort(query + 1 , query + 1 + m);
    int s, e, idx;
    tie(s, e, idx) = tie(query[1].s, query[1].e, query[1].idx);
    plusVal(s, e, false);
    result[idx] = getQueryVal();
    
    for ( int i = 2; i <= m; i++ ) {
        int ns, ne, nIdx;
        tie(ns, ne, nIdx) = tie(query[i].s, query[i].e, query[i].idx);
        
        if ( ns < s ) plusVal(s-1, ns, true);
        if ( ne > e ) plusVal(e+1, ne, false);
        if ( ns > s ) minusVal(s, ns-1, true);
        if ( ne < e ) minusVal(e, ne+1, false);
        
        s = ns; e = ne;
        result[nIdx] = getQueryVal(); 
    }
    
    for ( int i = 1; i <= m; i++ ) cout << result[i] << '\n';
    return 0;
}
```
### 📑[13545 - 수열과 쿼리 0](https://www.acmicpc.net/problem/13545)
#### 🔓 KeyPoint
- '수열과 쿼리 4' 문제와 비슷하게 [[Mo's]] 알고리즘에 제곱분할법을 합친 문제이다.
-  Ai~Aj가 0인 수열은 A1~Ai-1 = A1~Aj 값과 같다는 뜻이다.
- 이를 활용하여 쿼리 구간(s, e)를 변형하여 (s-1, e)로 바꾸고 쿼리를 계산하면 된다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, sqrtN, m, arr[101010], prefixSum[202020], cnt[202020] = {0, }, sqrtCnt[202020] = {0, }, result[101010];
list<int> pos[202020];

struct Query{
    int s, e, idx;
    Query(int S = 0, int E = 0, int Idx = 0) : s(S), e(E), idx(Idx) {}
    bool operator < (const Query &q) {
        if ( s / sqrtN != q.s / sqrtN ) return s / sqrtN < q.s / sqrtN;
        return e < q.e;
    }
};

Query query[101010];

void plusVal(int s, int e, bool IsFrontPush) {
    if ( IsFrontPush ) {
        s *= -1;
        e *= -1;
    }
    
    for ( int i = s; i <= e; i++ ) {
        int absI = abs(i), val;
        list<int> &dq = pos[prefixSum[absI]];
        if ( !dq.empty() ) {
            val = dq.back() - dq.front();
            cnt[val]--; sqrtCnt[val/sqrtN]--;
        }
        
        if ( IsFrontPush ) dq.push_front(absI);
        else dq.push_back(absI);
        
        val = dq.back() - dq.front();
        cnt[val]++; sqrtCnt[val/sqrtN]++;
    }
}

void minusVal(int s, int e, bool IsFrontPop) {
    if ( !IsFrontPop ) {
        s *= -1;
        e *= -1;
    }
    
    for ( int i = s; i <= e; i++ ) {
        int absI = abs(i), val;
        list<int> &dq = pos[prefixSum[absI]];
        val = dq.back() - dq.front();
        cnt[val]--; sqrtCnt[val/sqrtN]--;
    
        if ( IsFrontPop ) dq.pop_front();
        else dq.pop_back();
        
        if ( !dq.empty() ) {
            val = dq.back() - dq.front();
            cnt[val]++; sqrtCnt[val/sqrtN]++;
        }
    }
}

int getQueryVal() {
    for ( int i = (202020 / sqrtN + 9); i >= 0; i-- ) {
        if ( sqrtCnt[i] != 0 ) {
            for ( int j = sqrtN-1; j >= 0; j-- ) {
                if ( cnt[i * sqrtN + j] != 0 ) return i * sqrtN + j;
            }
        }
    }
    return -1;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n;
    sqrtN = sqrt(n);
    arr[0] = 0;
    for ( int i = 1; i <= n; i++ ) cin >> arr[i];
    prefixSum[1] = arr[1];
    for ( int i = 2; i <= n; i++ ) prefixSum[i] = prefixSum[i-1] + arr[i];
    for ( int i = 0; i <= n; i++ ) prefixSum[i] += 100000;
    cin >> m;
    
    for ( int i = 1; i <= m; i++ ) {
        int s, e;
        cin >> s >> e;
        query[i] = Query(s-1, e, i);
    }
    
    sort(query + 1,  query + 1 + m);
    int s, e, idx;
    tie(s, e, idx) = tie(query[1].s, query[1].e, query[1].idx);
    plusVal(s, e, false);
    result[idx] = getQueryVal();
    
    for ( int i = 2; i <= m; i++ ) {
        int ns, ne, nIdx;
        tie(ns, ne, nIdx) = tie(query[i].s, query[i].e, query[i].idx);
        
        
        if ( ns < s ) plusVal(s-1, ns, true);
        if ( ne > e ) plusVal(e+1, ne, false);
        if ( ns > s ) minusVal(s, ns-1, true);
        if ( ne < e ) minusVal(e, ne+1, false);
        
        s = ns; e = ne;
        result[nIdx] = getQueryVal();
    }
    
    for ( int i = 1; i <= m; i++ ) cout << result[i] << '\n';
    return 0;
}
```