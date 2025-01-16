Lazy Segment Tree의 응용 문제에 대한 코드는 다음과 같습니다. 

### Lazy Segment Tree CODE (📑[10999 - 구간 합 구하기 2](https://www.acmicpc.net/problem/10999))
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

### Lazy Segment Tree 응용문제
#### 📑[16975 - 수열과 쿼리 21](https://www.acmicpc.net/problem/16975)
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

#### 📑[2934 - LRH 식물](https://www.acmicpc.net/problem/2934)
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
이 코드는 Lazy Segment Tree를 사용하여 구간 업데이트 및 쿼리를 효율적으로 처리하는 방법을 보여줍니다. 각 문제의 요구 사항에 맞게 Lazy Segment Tree를 활용하여 성능을 최적화할 수 있습니다.