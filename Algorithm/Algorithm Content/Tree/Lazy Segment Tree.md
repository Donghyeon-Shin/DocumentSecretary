# Concept
- [[Segment Tree]]에서 배열의 구간의 변화가 생길 때, 이를 효율적으로 처리하기 위한 후속 자료구조이다.
- Lazy Segment Tree의 핵심은 `Lazy(게으른)`이다. 즉, Lazy Segment는 구간의 변화가 생길 때 그 값을 즉시 갱신하는 것이 아닌 후에 해당 Node를 방문했을 때 갱신한다.
- 쉽게 말해, 구할 범위가 아닌 값에 굳이 업데이트를 해 시간을 낭비하는 것 아니라 이를 뒤로 미루는 것이 Lazy Segment Tree의 핵심이다.
- 일반적인 Segment Tree에서 배열의 길이가 N이고 구간의 변화가 M번 생길 때 시간복잡도는 O(MNlogN)이다.
- Lazy Segment Tree를 이용했을 경우 시간복잡도는 O(MlogN)이다.
# Lazy Segment Tree 원리
- Segment Tree와 `init()` 함수는 같지만, `update()`와 `calcultion()`함수에서 `update_lazy()` 함수(기능)를 추가한다.
- `lazy[node] = 해당 Node에 쌓여있는 변화량`을 놓고 해당 Node를 방문하게 될 시, `SegmentTree[node] += lazy[node] * (end - start + 1)`로 업데이트 해주고 해당 Node의 자식이 있을 시, `lazy[node*2] += lazy[node], lazy[node*2 + 1] += lazy[node]`로 업데이트 한다. 
- `update()`함수에서도 마찬가지로 범위 안에 있는 Node들은 즉시 업데이트하고 그 Node의 자식들은 Lazy을 업데이트 해 연산을 뒤로 미룬다.
#### 🖼️그림으로 이해하기
![[Lazy Segment Tree Graph.svg]]
# Lazy Segment Tree CODE(📑[10999 - 구간 합 구하기 2](https://www.acmicpc.net/problem/10999))
- Segment Tree와 크키가 같은 Lazy Tree를 따로 만들어 Lazy를 관리한다.
- Overflow를 방지하기 위해 `start == end`(Node의 자식이 없을 때)는 자식으로 Lazy값을 전달하지 않게 주의해야 한다.
- Segment Tree, Lazy 모두 계산 과정에서 int범위 이상의 값이 들어올 수 있기 때문에 주어지는 수의 범위, 메모리을 잘 고려하여 자료형을 선언해야 한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, m, k;
long long arr[1000001];
vector<long long> segment_Tree, lazy;

long long init(int node, int start, int end) {
    
    if ( start == end ) return segment_Tree[node] = arr[start];
    int mid = (start + end) / 2;
    return segment_Tree[node] = init(node*2, start, mid) + init(node*2 + 1, mid + 1, end);
    
}

void update_lazy(int node, int start, int end) {
    
    if ( lazy[node] != 0 ) {
        segment_Tree[node] += lazy[node] * (end - start + 1);
        if ( start != end ) {
            lazy[node*2] += lazy[node];
            lazy[node*2 + 1] += lazy[node];
        }
        lazy[node] = 0;
    }
    
}

long long sum(int node, int start, int end, int left, int right) {
    
    update_lazy(node, start, end);
    if ( end < left || right < start ) return 0;
    if ( left <= start && end <= right ) return segment_Tree[node];
    int mid = (start + end) / 2;
    return sum(node*2, start, mid, left, right) + sum(node*2 + 1, mid + 1, end, left, right);
}

void update_range(int node, int start, int end, int left, int right, long long diff) {
    
    update_lazy(node, start, end);
    if ( end < left || right < start ) return;
    
    if ( left <= start && end <= right ) {
        segment_Tree[node] += diff*(end - start + 1);
        if ( start != end ) {
            lazy[node*2] += diff;
            lazy[node*2 + 1] += diff;
        }
        return;
    }
    int mid = (start + end) / 2;
    update_range(node*2, start, mid, left, right, diff);
    update_range(node*2 + 1, mid + 1, end, left, right, diff);
    segment_Tree[node] = segment_Tree[node*2] + segment_Tree[node*2 + 1];
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n >> m >> k;
    int oper = m + k;
    int height = (int)ceil(log2(n));
    int Tree_size = ( 1 << (height + 1));
    segment_Tree.resize(Tree_size);
    lazy.resize(Tree_size);
    for ( int i = 1; i <= n; i++ ) cin >> arr[i];
    init(1, 1, n);
    
    while ( oper-- ) {
        long long a, b, c, d;
        cin >> a;
        if ( a == 1 ) {
            cin >> b >> c >> d;
            update_range(1, 1, n, b, c, d);
        } else {
            cin >> b >> c;
            cout << sum(1, 1, n, b, c) << '\n';
        }
    }
    return 0;
}
```
##### ❓ 예제 Input
	12 3 3
	1 2 3 4 5 6 7 8 9 10 11 12
	2 1 12
	1 1 4 4
	1 5 7 12
	2 4 7
	1 1 12 10
	2 1 12 
##### ⭐ 예제 Output
	78
	62
	250
# Lazy Segment Tree 응용문제
### 📑[16975 - 수열과 쿼리 21](https://www.acmicpc.net/problem/16975)
#### 🔓 KeyPoint
- 위 예제 CODE랑 99% 흡사한 문제다.
- 퀴리 출력은 Array의 값이 하나지만, Update하는 과정에서 Array의 배열을 다루기 때문에 Lazy Segment Tree가 필요하다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, m;
long long arr[100000];
vector<long long> segment_Tree, lazy;

long long init(int node, int start, int end) {
    if ( start == end ) return segment_Tree[node] = arr[start];
    int mid = (start + end) / 2;
    return segment_Tree[node] = init(node*2, start, mid) + init(node*2 + 1, mid + 1, end);
}

void update_lazy(int node, int start, int end) {
    if ( lazy[node] != 0 ) {
        segment_Tree[node] += lazy[node] * (end - start + 1);
        if ( start != end ) {
            lazy[node*2] += lazy[node];
            lazy[node*2 + 1] += lazy[node];
        }
        lazy[node] = 0;
    }
}

void update(int node, int start, int end, int left, int right, long long diff) {
    
    update_lazy(node, start, end);
    
    if ( end < left || right < start ) return;
    if ( left <= start && end <= right ) {
        segment_Tree[node] += diff * (end - start + 1);
        if ( start != end ) {
            lazy[node * 2] += diff;
            lazy[node * 2 + 1] += diff;
        }
        return;
    }
    
    int mid = (start + end) / 2;
    update(node*2, start, mid, left, right, diff);
    update(node*2 + 1, mid + 1, end, left, right, diff);
    segment_Tree[node] = segment_Tree[node*2] + segment_Tree[node*2 + 1];    
}

void print_x(int node, int start, int end, int left, int right) {
    
    update_lazy(node, start, end);
    
    if ( end < left || right < start ) return;
    if ( left <= start && end <= right ) {
        cout << segment_Tree[node] << '\n';
        return;
    }
    
    int mid = (start + end) / 2;
    print_x(node*2, start, mid, left, right);
    print_x(node*2 + 1, mid + 1, end, left, right);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n;
    for ( int i = 0; i < n; i++ ) cin >> arr[i];
    
    int height = (int)ceil(log2(n));
    int tree_Size = ( 1 << ( height + 1) );
    segment_Tree.resize(tree_Size);
    lazy.resize(tree_Size);
    
    init(1, 0, n-1);
    
    cin >> m;
    while ( m-- ) {
        int cmd;
        cin >> cmd;
        if ( cmd == 1 ) {
            int i, j, k;
            cin >> i >> j >> k;
            update(1, 0, n-1, i-1, j-1, k);
        } else {
            int x;
            cin >> x;
            print_x(1, 0, n-1, x-1, x-1);
        }
    }
    return 0;
}
```
### 📑[2934 - LRH 식물](https://www.acmicpc.net/problem/2934)
#### 🔓 KeyPoint
- LRH 식물끼리 교차하는 경우, 꽃이 한 봉우리씩 피게 된다. 꽃이 교차한다는 뜻은 꽃을 심은 위치(L, R)에 전에 심은 꽃이 있다는 뜻이다.
- 다음 날 심은 꽃은 전날 심은 꽃보다 높이가 1 크기 때문에, 꽃 봉우리가 접할려면 심은 위치 L이 같거나 R이 같은 경우다. 
- 꽃 봉우리는 접하면 나오지 않기 때문에 `Array[L+1] ~ Array[R-1]`에 꽃이 있다는 뜻인 `+ 1`를 한 뒤, 다음 꽃을 심었을 때 `Array[L], Array[R]`의 합을 구하게 되면 그 값만큼 기존 꽃과 겹친다는 뜻이기 때문에 해당 합만큼 꽃 봉우리가 더 핀다.
#### ⌨️ Code
- Index를 0~n까지로 잡았기 때문에 모든 Index를 넣는 과정에서 -1를 했기 때문에 이에 유의해자.
```cpp
#include <bits/stdc++.h>

using namespace std;

int n;
long long flower = 0;
vector<long long> segment_Tree, lazy;

void update_lazy(int node, int start, int end) {
    if ( lazy[node] != 0 ) {
        segment_Tree[node] += lazy[node] * (end-start+1);
        if ( start != end ) {
            lazy[node*2] += lazy[node];
            lazy[node*2+1] += lazy[node];
        }
        lazy[node] = 0;
    }
}

void update(int node, int start, int end, int left, int right, int diff) {
    
    update_lazy(node, start, end);
    
    if ( end < left || right < start ) return;
    if ( left <= start && end <= right ) {
        segment_Tree[node] += diff * (end-start+1);
        if ( start != end ) {
            lazy[node*2] += diff;
            lazy[node*2+1] += diff;
        }
        return;
    }
    
    int mid = (start+end) / 2;
    update(node*2, start, mid, left, right, diff);
    update(node*2 + 1, mid+1, end, left, right, diff);
    segment_Tree[node] = segment_Tree[node*2] + segment_Tree[node*2 + 1];
}

void get_Flower(int node, int start, int end, int left, int right) {
    
    update_lazy(node, start, end);
    
    if ( end < left || right < start ) return;
    if ( left <= start && end <= right ) {
        flower += segment_Tree[node];
        if ( segment_Tree[node] != 0 ) update(1, 0, 100000, start, end, -segment_Tree[node]);
        return;
    }
    
    int mid = (start+end) / 2;
    get_Flower(node*2, start, mid, left, right);
    get_Flower(node*2 + 1, mid+1, end, left, right);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n;
    int height = (int)ceil(log2(100001));
    int tree_Size = ( 1 << (height + 1));
    segment_Tree.resize(tree_Size);
    lazy.resize(tree_Size);
    
    for ( int i = 0; i < n; i++ ) {
        int l, r;
        flower = 0;
        cin >> l >> r;
        
        get_Flower(1, 0, 100000, l-1, l-1);
        get_Flower(1, 0, 100000, r-1, r-1);
        
        cout << flower << '\n';
        if ( r - l != 1 ) update(1, 0, 100000, l, r-2, 1);
    }
    return 0;
}
```
