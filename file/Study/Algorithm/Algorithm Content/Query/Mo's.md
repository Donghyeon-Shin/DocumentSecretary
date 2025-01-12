# Concept
- 업데이트가 없는 구간 쿼리를 처리하는 알고리즘이다.
- 대게 어떤 구간`[s, e]`에 속하는 원소들을 이용해 계산하는 쿼리를 여러 개 처리할 때 사용한다.
- 처음 쿼리 구간을 `[s1, e1]`이라 하고 다음 쿼리 구간을 `[s2, e2]`라고 하면 s1에서 s2까지 이동, e1에서 e2까지의 이동을 최소화하는게 중요하다.
- 구간의 이동을 최소하기 위해선 쿼리를 순선대로 처리하는 것이 아니라 정렬을 해야하기 때문에 Mo's Algorithm은 [[Offline Query]]에 포함된다.
# Mo's Algorithm 원리(📑[13547 - 수열과 쿼리 5](https://www.acmicpc.net/problem/13547))
- 쿼리간의 구간 이동을 최소화하기 위해서는 쿼리의 s, e 기준으로 정렬해야 한다.
- 길이 N인 수열에 대해서 구간 `[s, e]`가 있을 때 정렬 방법은
	1. s<sub>i</sub> / n<sup>0.5</sup> 기준으로 오름차순 정렬 (Sqrt Decomposition)
	2. 1번 값이 같으면 ei 기준으로 오름차순 정렬
- 1번을 기준으로 정렬하는 이유는 구간 안에서의 이동이 구간 밖으로의 이동보다 이동 횟수가 적기 때문이다.
- 정렬된 쿼리를 순서대로 진행하는데 s<sub>i</sub> > s<sub>j</sub> (i < j)이면 시작 구간을 늘리고 s<sub>i</sub> < s<sub>j</sub> (i < j)이면 시작 구간을 줄인다. 또 e<sub>i</sub> < e<sub>j</sub> (i < j)이면 끝 구간을 늘리고 e<sub>i</sub> > e<sub>j</sub> (i < j)이면 끝 구간을 줄인다.
- `수열과 쿼리 5`은 구간 쿼리가 주어졌을 때 그 구간 사이에 존재하는 서로 다른 수의 개수를 출력하는 것이다.
#### 🖼️그림으로 이해하기
![[Mo's Graph.svg]]
# Mo's Algorithm CODE
- Query Struct을 만들어 각 쿼리에 대한 구간 `[s,e]`과 몇 번째 쿼리인지를 저장한다.
- Query Struct에 Operator overloading을 해 sort함수가 작동하도록 구현한다.
- 쿼리를 계산에 유리하게 정렬했기 때문에, 답을 출력할 때는 다시 순서에 맞게 출력해줘야 한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, k = 0, m, arr[100001], cnt[1000001], result = 0, query_Ans[100001];

struct Query{
    int s, e, idx;
    
    Query(int S = 0, int E = 0, int Idx = 0) : s(S), e(E), idx(Idx) {}
    
    bool operator < (const Query &q ) {
        if ( s / k != q.s / k ) return s / k < q.s / k;
        return e < q.e;
    }
};

void plusVal(int s, int e) {
    for ( int i = s; i <= e; i++ ) {
        if ( cnt[arr[i]] == 0 ) result++;
        cnt[arr[i]]++;
    }
}

void delVal(int s, int e) {
    for ( int i = s; i <= e; i++ ) {
        cnt[arr[i]]--;
        if(cnt[arr[i]] == 0 ) result--;
    }
}

Query query[100001];

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    memset(cnt, 0, sizeof(cnt));
    
    cin >> n;
    k = sqrt(n);
    
    for ( int i = 1; i <= n; i++ ) cin >> arr[i];
    cin >> m;
    for ( int i = 1; i <= m; i++ ) {
        int I, J;
        cin >> I >> J;
        query[i] = Query(I, J, i);
    }
    
    sort(query + 1, query + 1 + m);
    
    int s = query[1].s, e = query[1].e, idx = query[1].idx;

    for ( int i = s; i <= e; i++ ) {
        if ( cnt[arr[i]] == 0 ) result++;
        cnt[arr[i]]++;
    }
    
    query_Ans[idx] = result;
    
    for ( int i = 2; i <= m; i++ ) {
        int ns, ne, nIndex;
        ns = query[i].s;
        ne = query[i].e;
        nIndex = query[i].idx;
        
        if ( ns < s ) plusVal(ns, s-1);
        else if ( ns > s ) delVal(s, ns-1);
        
        if ( ne < e ) delVal(ne+1, e);
        else if ( ne > e ) plusVal(e+1, ne);
        
        s = ns;
        e = ne;
        query_Ans[nIndex] = result;
    }
    
    for ( int i = 1; i <= m; i++ ) cout << query_Ans[i] << '\n';
    return 0;
}
```
##### ❓ 예제 Input
	9
	5 1 5 5 2 5 1 5 3
	5
	1 2
	3 4
	5 8
	1 9
	2 5
##### ⭐ 예제 Output
	2
	1
	3
	4
	3
# Mo's Algorithm 응용문제
### 📑[2912 - 백설공주와 난쟁이](https://www.acmicpc.net/problem/2912)
#### 🔓 KeyPoint
- 사진(쿼리)가 주어졌을 때, 사진 속 난쟁이 모자의 수가 절반 이상 같은 모자라면 '예쁜 사진', 그렇지 않으면 '예쁘지 않은 사진'이다.
- 사진은 `[s, e]`로만 이루어져 있기 때문에 Mo's Algorithm을 사용하기 적합하다.
- `Cnt[i] = [s, e]범위에 있는 모자 종류 i의 수`로 놓고 범위를 늘릴 때는 해당 범위에 있는 난쟁이 모자 수를 '+'하고 범위를 줄일 때는 해당 범위에 있는 난쟁이 모자 수를 '-'한다.
- 절반 이상인 모자를 찾는 것은 cnt배열에서 모든 모자 종류를 Search해 절반 이상인 것이다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, k = 0, m, c, dwarf[300001], cnt[10001], answer[10001];

struct Query{
    int s, e, idx;
    Query(int S = 0, int E = 0, int Idx = 0) : s(S), e(E), idx(Idx) {}
    bool operator < (const Query &q ) {
        if ( s / k != q.s / k ) return s / k < q.s / k;
        return e < q.e;
    }
};

Query query[10001];

void plus_Val(int s, int e) {
    for ( int i = s; i <= e; i++ ) cnt[dwarf[i]]++;
}

void minus_Val(int s, int e) {
    for ( int i = s; i <= e; i++ ) cnt[dwarf[i]]--;
}

int isGoodPhoto(int s, int e) {
    for ( int i = 1; i <= c; i++ ) {
        if ( cnt[i] * 2 > (e-s) + 1 ) return i;
    }
    return 0;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n >> c;
    k = sqrt(n);
    for ( int i = 1; i <= n; i++ ) cin >> dwarf[i];
    cin >> m;
    for ( int i = 1; i <= m; i++ ) {
        int a, b;
        cin >> a >> b;
        query[i] = Query(a, b, i);
    }
    
    sort(query + 1, query + 1 + m);
    
    int s = query[1].s, e = query[1].e, idx = query[1].idx;
    plus_Val(s, e);
    answer[idx] = isGoodPhoto(s, e);
    
    for ( int i = 2; i <= m; i++ ) {
        int ns, ne, nIdx;
        ns = query[i].s; ne = query[i].e; nIdx = query[i].idx;
        
        if ( ns < s ) plus_Val(ns, s-1);
        else if ( ns > s ) minus_Val(s, ns-1);
        
        if ( ne > e ) plus_Val(e+1, ne);
        else if ( ne < e ) minus_Val(ne+1, e);
        
        s = ns; e = ne; idx = nIdx;
        answer[idx] = isGoodPhoto(s, e);
    }
    
    for ( int i = 1; i <= m; i++ ) {
        if ( answer[i] == 0 ) cout << "no\n";
        else {
            cout << "yes " << answer[i] << '\n';
        }
    }
    return 0;
}
```
### 📑[12999 - 화려한 마을3](https://www.acmicpc.net/problem/12999)
#### 🔓 KeyPoint
- 페인트의 밝기의 범위는 (-100,000 <= p <= 100,000 )이다. 밝기 종류 별로 개수를 구해야 하기 때문에 `cnt[i] = [s,e]범위에 있는 밝기 i번째 집의 개수`로 놓는다.
- 음수인 밝기가 존재하기 때문에 음수의 경우 절댓값을 양수의 경우 현재 밝기 + 100,000을 한다.
- 밝기가 가장 많이 등장하는 빈도수를 찾는 것이 핵심 문제이기 때문에 `count_Frequen[i] = i번째 밝기 수(cnt)의 빈도수`를 만들어야 한다.
- 범위를 늘릴 때는 해당 범위에 있는 밝기 수(Cnt)가 0이 아닐 시 해당 밝기 수에 해당하는 빈도수(count_Frequen)값을 하나 빼주고 밝기 수를 하나 증가 한 다음, 그 수에 해당하는 빈도수 값을 늘려주어야 한다. 또한 늘어난 빈도수 값이랑 현재 가장 많은 빈도수 값이랑 무엇이 더 많은지 채크해 업데이트 해야 한다.
- 범위를 줄일 때는 해당 범위에 있는 밝기 수의 빈도수를 줄이고 밝기 수를 줄이면 된다. 또한 줄어든 밝기 수의 빈도수를 증가시킨다. 만약 가장 빈도수가 많은 밝기 수가 줄어든거라면, 빈도수를 하나 낮춘다.(빈도수가 4인 밝기 3이 없어졌다면, 밝기 3의 개수(cnt)가 줄어들면서 빈도수가 3이 되었을 것이기 때문이다.)
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, q, k, arr[100001], cnt[200001] = {0, }, count_Frequen[200001] = {0, }, answer[100001], result = 0;

struct Query{
    int s, e, idx;
    Query( int _S = 0, int _E = 0, int _Idx = 0) : s(_S), e(_E), idx(_Idx) {}

    bool operator < (const Query &q) {
        if ( s / k != q.s / k ) return s / k < q.s / k;
        return e < q.e;
    } 
};

Query query[100001];

void plus_Val(int s, int e) {
    for ( int i = s; i <= e; i++ ) {
        if ( cnt[arr[i]] != 0 ) count_Frequen[cnt[arr[i]]]--;
        cnt[arr[i]]++;
        count_Frequen[cnt[arr[i]]]++;
        result = max(result, cnt[arr[i]]);
    }
}

void minus_Val(int s, int e) {
    for( int i = s; i <= e; i++ ) {
        count_Frequen[cnt[arr[i]]]--;
        cnt[arr[i]]--;
        count_Frequen[cnt[arr[i]]]++;
        if(count_Frequen[result] == 0 ) result--;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n >> q;
    k = sqrt(n);
    
    for ( int i = 1; i <= n; i++ ) {
        int paint;
        cin >> paint;
        arr[i] = (paint > 0) ? 100000 + paint : abs(paint); 
    }
    
    for ( int i = 1; i <= q; i++ ) {
        int I, J;
        cin >> I >> J;
        query[i] = Query(I, J, i);
    }
    sort(query + 1, query + 1 + q);
    
    int s = query[1].s, e = query[1].e, idx = query[1].idx;
    plus_Val(s, e);
    answer[idx] = result;
    
    for ( int i = 2; i <= q; i++ ) {
        int ns = query[i].s, ne = query[i].e, nIdx = query[i].idx;
        
        if ( ns < s ) plus_Val(ns, s-1);
        else if ( ns > s ) minus_Val(s, ns-1);
        
        if ( ne > e ) plus_Val(e+1, ne);
        else if ( ne < e ) minus_Val(ne+1, e);
        
        s = ns; e = ne; idx = nIdx;
        answer[idx] = result;
    }
    
    for ( int i = 1; i <= q; i++ ) cout << answer[i] << '\n';
    return 0;
}
```
