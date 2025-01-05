
# Concept
- [[Segment Tree]]형태로 각 노드의 값은 해당 노드의 구간에 있는 원소들이 정렬된 List값을 가진다.
- Leaf Node는 하나의 원소만 가지고 있으며 Parent Node로 올라가며 각각의 Node의 원소들을 합치면 된다.
- 합치는 과정에서 각각의 Node들의 원소들은 정렬되어 있기 때문에 Merge방식으로 정렬할 수 있으며 이는 `O(logN)`의 시간복잡도가 소요된다. (n : 정렬할 원소 개수)
# Merge Sort Tree 원리
- [[Segment Tree]] 구조를 가지지만, Node의 값이 List인 것이 특징이다.
- `init()`함수에서 `start == end`상황 즉, Leaf Node일 때는 구간이 하나이기 때문에 List에 하나의 값만 push한 상황에서 return하고 Leaf Node가 아닐 때는 각 Node의 자식 노드의 List에 값들을 합쳐 정렬된 List를 만든다.
#### 🖼️그림으로 이해하기
![[Merge Sort Tree Graph.svg]]
# Merge Sort Tree CODE(📑[13537 - 수열과 쿼리 1](https://www.acmicpc.net/problem/13537))
- C++의 STL에 merge라는 함수를 재공하기 떄문에 이를 이용하면 쉽게 구현할 수 있다.
- Node 값 즉, List의 크기는 Node의 자식 Node들이 크기를 합한 값이다. 
- 메모리를 효율적으로 사용하기 위해 List의 크기를 미리 정하지 말고 Resize를 통해 후에 업데이트 한다.
- Merge Sort Tree의 대부분 문제는 해당 Node에서 특정 값이 몇 번째에 있는지 구하는 것이기 때문에, `Lower_Bound() / Upper_Bound()`을 이용해 해당 인덱스를 구하면 된다.
- 현재 Code에는 Array 구간보다 큰 구간의 Node에 `0`값이 들어간다. 이는 문제에서 Array의 값들이 1보다 크기 때문이라 따로 구현 안 한것일 뿐, 만약 Array의 0 값이 들어가면 Array의 들어갈 수 있는 값들 중 가장 작은 값보다 작게 빈 값을 설정해줘야 된다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, m;
vector<int> mergeSort_Tree[1 << 18], arr;

void init(int node, int start, int end) {
    vector<int> &cur = mergeSort_Tree[node];
    if ( start == end ) {
        cur.push_back(arr[start]);
        return;
    }
    
    int mid = (start + end) / 2;
    init(node * 2, start, mid);
    init(node * 2 + 1, mid + 1, end);
    
    vector<int> &left = mergeSort_Tree[node*2], &right = mergeSort_Tree[node*2 + 1];
    cur.resize((int)left.size() + (int)right.size());
    merge(left.begin(), left.end(), right.begin(), right.end(), cur.begin());
} 

int get_Index(int node, int start, int end, int left, int right, int target) {
    if ( end < left || right < start ) return 0;
    if ( left <= start && end <= right ) return lower_bound(mergeSort_Tree[node].begin(), mergeSort_Tree[node].end(), target) - mergeSort_Tree[node].begin();
    
    int mid = (start + end) / 2;
    int result = get_Index(node * 2, start, mid, left, right, target) + get_Index(node * 2 + 1, mid + 1, end, left, right, target);
    return result;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n;
    for ( int i = 0; i < n; i++ ) {
        int num;
        cin >> num;
        arr.push_back(num);
    }
    
    init(1, 0, n-1);
    
    cin >> m;
    for ( int q = 0; q < m; q++ ) {
        int i, j, k;
        cin >> i >> j >> k;
        cout << j - i + 1 - get_Index(1, 0, n-1, i-1, j-1, k+1) << '\n';
    }
    return 0;
}
```
##### ❓ 예제 Input
	13
	0 1 2 3 4 5 6 7 8 9 10 11 12
	3
	3 5 1
	8 10 10
	1 12 7
##### ⭐ 예제 Output
	3
	0
	4
# Merge Sort Tree 응용문제
### 📑[15899 - 트리와 색깔](https://www.acmicpc.net/problem/15899)
#### 🔓 KeyPoint
- Tree의 구간을 나누기 위해 [[ETT(Euler Tour Technique)]]를 이용해야 한다.
- Tree의 서브 Tree 중 색깔이 c 이하인 정점의 개수를 새야하기 때문에 Merge Sort Tree를 사용하면 된다.
- `c 이하인 정점`을 찾아야 하기 때문에 Lower_Bound에서 c + 1 값을 찾아서 반환해야 한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>
#define MOD 1000000007

using namespace std;

int n, m, c, node_Color[200001], trans_Node[200001], cnt = 0, s[200001] = {0, }, e[200001] = {0, }, result = 0;
vector<int> mergeSort_Tree[1 << 19], adj[200001];

void dfs(int node) {
    s[node] = ++cnt;
    for ( int nNode : adj[node] ) {
        if ( s[nNode] == 0 ) dfs(nNode);
    }
    e[node] = cnt;
}

void init(int node, int start, int end) {
    vector<int> &cur = mergeSort_Tree[node];
    if ( start == end ) {
        cur.push_back(trans_Node[start]);
        return;
    }
    
    int mid = (start + end) / 2;
    init(node*2, start, mid);
    init(node*2 + 1, mid + 1, end);
    
    vector<int> &left = mergeSort_Tree[node*2];
    vector<int> &right = mergeSort_Tree[node*2 + 1];
    cur.resize((int)left.size() + (int)right.size());
    merge(left.begin(), left.end(), right.begin(), right.end(), cur.begin());
}

int get_Index(int node, int start, int end, int left, int right, int target) {
    if ( end < left || right < start ) return 0;
    if ( left <= start && end <= right ) {
        return lower_bound(mergeSort_Tree[node].begin(), mergeSort_Tree[node].end(), target+1) - mergeSort_Tree[node].begin();
    }
    
    int mid = (start + end) / 2;
    return get_Index(node*2, start, mid, left, right, target) + get_Index(node*2 + 1, mid + 1, end, left, right, target);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n >> m >> c;
    
    for ( int i = 1; i <= n; i++ ) cin >> node_Color[i];
    for ( int i = 0; i < n-1; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    
    dfs(1);
    for ( int i = 1; i <= n; i++ ) trans_Node[s[i]] = node_Color[i];
    init(1, 1, n);
    
    for ( int i = 0; i < m; i++ ) {
        int a, b;
        cin >> a >> b;
        result += (get_Index(1, 1, n, s[a], e[a], b)) % MOD;
        result %= MOD;
    }
    cout << result;
    return 0;
}
```
### 📑[14446 - Promotion Counting](https://www.acmicpc.net/problem/14446)
#### 🔓 KeyPoint
- 트리와 색깔 문제와 마찬가지로 Tree 구조를 가진 Input의 구간을 구하기 위해 [[ETT(Euler Tour Technique)]]을 이용해야 한다.
- 초기 Tree의 값이 int범위를 초과할 수 있기 때문에 long long형을 사용한다.
- 구하는 값은 자기 자신을 포함 하면 안되기 때문에 현재 Node를 i라고 한다면 `s[i] + 1 ~ e[i]`중 Node의 값보다 작은 값을 가지고 있는 Node의 개수를 구하면 된다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, cnt = 0, s[100001] = {0, }, e[100001] = {0, };
long long p[100001], trans_Node[100001];
vector<int> adj[100001], mergeSort_Tree[1 << 18];

void dfs(int node) {
    s[node] = ++cnt;
    for ( int nNode : adj[node] ) {
        if ( s[nNode] == 0 ) dfs(nNode);
    }
    e[node] = cnt;
}

void init(int node, int start, int end) {
    vector<int> &cur = mergeSort_Tree[node];
    if ( start == end ) {
        cur.push_back(trans_Node[start]);
        return;
    }
    
    int mid = (start + end) / 2;
    init(node*2, start, mid);
    init(node*2 + 1, mid + 1, end);
    
    vector<int> &left = mergeSort_Tree[node*2];
    vector<int> &right = mergeSort_Tree[node*2 + 1];
    cur.resize((int)left.size() + (int)right.size());
    merge(left.begin(), left.end(), right.begin(), right.end(), cur.begin());
}

int calcul_Cnt(int node, int start, int end, int left, int right, int target) {
    if ( end < left || right < start ) return 0;
    if ( left <= start && end <= right ) {
        return lower_bound(mergeSort_Tree[node].begin(), mergeSort_Tree[node].end(), target) - mergeSort_Tree[node].begin();   
    }
    
    int mid = (start + end) / 2;
    return calcul_Cnt(node*2, start, mid, left, right, target) + calcul_Cnt(node*2 + 1, mid+1, end, left, right, target);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n;
    for ( int i = 1; i <= n; i++ ) cin >> p[i];
    for ( int i = 2; i <= n; i++ ) {
        int parent;
        cin >> parent;
        adj[parent].push_back(i);
    }
    
    dfs(1);
    for ( int i = 1; i <= n; i++ ) trans_Node[s[i]] = p[i];
    init(1, 1, n);
    
    for ( int i = 1; i <= n; i++ ) {
        cout << (e[i] - s[i]) - calcul_Cnt(1, 1, n, s[i] + 1, e[i], trans_Node[s[i]]) << '\n';
    }
    return 0;
}
```
