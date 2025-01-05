
# Concept
- 특정 노드(Node)의 모든 하위 Node 또는 상위 Node에 대한 쿼리를 처리하고자 할 때, 사용하는 알고리즘이다.
- List와 다르게 Tree는 구간의 연속성을 가지지 않는다. 따라서 구간에 대한 쿼리를 처리하기 어렵다. 이를 해결하기 위해 [[DFS(Depth-First Search)]]을 사용하여 Tree의 서브 트리 구간을 List 형태로 만들어 구간에 대한 정보를 처리한다.
- Euler Tour Technique 그 자체만으로 문제를 해결하는 경우는 거의 없고 [[Segment Tree]]나 [[Lazy Segment Tree]]같이 구간에 대한 정보가 필요한 알고리즘을 구현하기 위해 사용된다.
- DFS를 통해 구현하기 때문에 시간복잡도는 dfs와 같은 O(n+e) / `노드의 개수 n, 간선의 개수 e`이다.
# Euler Tour Technique 원리
- Root Node에서 시작해 방문 번호(cnt)를 매기기 시작해 DFS를 진행하면서 해당 노드의 `s[node] = node의 진입 방문 번호, e[node] = node의 탈출 방문 번호`를  구하면 된다.
- `s[node]`는 말 그대로 해당 Node가 방문된 번호이고 `e[node]`는 해당 Node의 자식들 중 가장 방문 번호가 늦은 번호이다.
- 모든 Node를 탐색하고 얻은 s,e가 해당 Node의 구간 정보이다.
- DFS만 알고 있다면 이해하는데 어렵지 않은 알고리즘이다.
#### 🖼️그림으로 이해하기
![[ETT Graph.svg]]
# Euler Tour Technique CODE
- DFS는 Root에서 시작해야 하기 때문에 Root Node가 무엇인지 아는 것이 가장 중요하다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, m, cnt = 0, s[100001], e[100001];
vector<int> graph[100001];

void dfs(int node) {
    s[node] = ++cnt;
    for ( auto nNode : graph[node] ) {
        if ( s[nNode] == 0 ) dfs(nNode);
    }
    e[node] = cnt;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n >> m;
    for ( int i = 0; i < m; i++ ) {
        int n1, n2;
        cin >> n1 >> n2;
        graph[n1].push_back(n2);
    }
    
    int root = 1;
    dfs(root);
    
    for ( int i = 1; i <= n; i++ ) cout << "Node " << i << " : " << s[i] << ' ' << e[i] << '\n';
    return 0;
}
```
##### ❓ 예제 Input
	8 7
	1 2
	1 3
	1 4
	3 5
	4 6
	4 7
	7 8
##### ⭐ 예제 Output
	Node 1 : 1 8
	Node 2 : 2 2
	Node 3 : 3 4
	Node 4 : 5 8
	Node 5 : 4 4
	Node 6 : 6 6
	Node 7 : 7 8
	Node 8 : 8 8

# Euler Tour Technique 응용문제
### 📑[2820 - 자동차 공장](https://www.acmicpc.net/problem/2820)
#### 🔓 KeyPoint
- 회사 조직도가 Tree형태로 주어지고, 특정 직원의 월급이 변화하면 그 직원의 부하 직원(자식 Node) 또한 변화한다.
- Tree에 구간 정보를 처리해야기 때문에 ETT를 사용해야 한다.
- 특정 범위 전체의 값이 변화하기 때문에 [[Lazy Segment Tree]]를 구현해야 한다.
- DFS를 통해 ETT를 구하고 `S, E`를 바탕으로 Lazy Segment Tree를 만든다.
- `init()`할 때 기존 Node 번호를 사용하는 것이 아닌 `S[node]`번호를 사용해야 함에 주의한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, m, cnt = 0, s[500001] = {0, }, e[500001] = {0, };
long long pay[500001], trasform_Node[500001];
vector<int> adj[500001];
vector<long long> segment_Tree, lazy;

void dfs(int node) {
    s[node] = ++cnt;
    for ( auto nNode : adj[node] ) {
        if ( s[nNode] == 0 ) dfs(nNode);
    }
    e[node] = cnt;
}

long long init(int node, int start, int end) {
    if ( start == end ) return segment_Tree[node] = trasform_Node[start];
    int mid = (start + end) / 2;
    return segment_Tree[node] = init(node*2, start, mid) + init(node*2 + 1, mid + 1, end);
}

void update_Lazy(int node, int start, int end) {
    if ( lazy[node] != 0 ) {
        segment_Tree[node] += 1LL * lazy[node] * (end - start + 1);
        if ( start != end ) {
            lazy[node * 2] += lazy[node];
            lazy[node * 2 + 1] += lazy[node];
        }
        lazy[node] = 0;
    }
}

void update_Range(int node, int start, int end, int left, int right, long long diff) {
    update_Lazy(node, start, end);
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
    update_Range(node*2, start, mid, left, right, diff);
    update_Range(node*2 + 1, mid + 1, end, left, right, diff);
    segment_Tree[node] = segment_Tree[node*2] + segment_Tree[node*2 + 1];
}

long long calcul_Pay(int node, int start, int end, int target) {
    update_Lazy(node, start, end);
    if ( end < target || target < start ) return 0;
    if ( start == end ) return segment_Tree[node];
    int mid = (start + end) / 2;
    return calcul_Pay(node*2, start, mid, target) + calcul_Pay(node*2 + 1, mid + 1, end, target);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n >> m;
    int height = (int)ceil(log2(n));
    int tree_Size = ( 1 << (height + 1));
    segment_Tree.resize(tree_Size);
    lazy.resize(tree_Size);
    
    cin >> pay[1];
    for ( int i = 2; i <= n; i++ ) {
        long long parent;
        cin >> pay[i] >> parent;
        adj[parent].push_back(i);
    }
    
    dfs(1);
    for ( int i = 1; i <= n; i++ ) trasform_Node[s[i]] = pay[i];
    init(1, 1, n);
    for ( int i = 0; i < m; i++ ) {
        char q;
        cin >> q;
        if ( q == 'p' ) {
            int a;
            long long x;
            cin >> a >> x;
            update_Range(1, 1, n, s[a] + 1, e[a], x);
        } else {
            int a;
            cin >> a;
            cout << calcul_Pay(1, 1, n, s[a]) << '\n';
        }
    }
    return 0;
}
```
### 📑[18227 - 성대나라의 물탱크](https://www.acmicpc.net/problem/18227)
#### 🔓 KeyPoint
- 수도(Root)에서 각 도시까지의 물탱크가 Tree형태로 연결되어 있다.
- 자식 도시의 물탱크는 현재 도시(Node)의 + 1 물을 채우기 때문에 이를 Lazy Segment Tree로 오해할 수 있으나, `Root에서부터 그 Node까지의 깊이`는 항상 일정하다.
- 따라서 `Node의 물의 양 = Node의 모든 자식 도시들의 방문 수 * Root에서부터 그 Node까지의 깊이`으로 표현이 가능해 [[Segment Tree]]로 문제를 풀 수 있다.
- ETT를 구하면서 `depth[node] = Root에서부터 그 Node까지의 깊이`도 구한다.
- 특정 수도에 물을 넣을 때 Segment Tree로 그 노드의 방문 횟수를 기록한 뒤 물에 양을 구하는 퀴에서만 `Node의 모든 자식 도시들의 방문 수 * depth[node]`를 해주면 된다.
- 물의 값이 int범위를 초과할 수 있기에 long long 자료형을 사용해준다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, c, k, q, s[200001] = {0, }, e[200001] = {0, };
long long cnt = 0, depth[200001] = {0, };
bool visited[200001] = {0, };
vector<int> adj[200001];
vector<long long> segment_Tree;

void dfs(int node) {
    s[node] = ++cnt;
    for ( auto nNode : adj[node] ) {
        if ( !visited[nNode] ) {
            visited[nNode] = true;
            depth[nNode] = depth[node] + 1;
            dfs(nNode);
        }
    }
    e[node] = cnt;
}

long long update(int node, int start, int end, int left, int right) {
    if ( end < left || right < start ) return 0;
    if ( left <= start && end <= right ) return ++segment_Tree[node];
    
    int mid = (start + end) / 2;
    update(node*2, start, mid, left, right);
    update(node*2 + 1, mid + 1 , end, left, right);
    return segment_Tree[node] = segment_Tree[node*2] + segment_Tree[node*2 + 1];
}

long long sum(int node, int start, int end, int left, int right) {
    if ( end < left || right < start ) return 0;
    if ( left <= start && end <= right ) return segment_Tree[node];
    
    int mid = (start + end) / 2;
    return sum(node*2, start, mid, left, right) + sum(node*2 + 1, mid + 1, end, left, right);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n >> c;
    for ( int i = 0; i < n-1; i++ ) {
        int x, y;
        cin >> x >> y;
        adj[x].push_back(y);
        adj[y].push_back(x);
    }
    
    int height = (int)ceil(log2(n));
    int tree_Size = ( 1 << (height + 1));
    segment_Tree.resize(tree_Size);
    
    visited[c] = true;
    depth[c] = 1;
    dfs(c);
    
    cin >> q;
    while ( q-- ) {
        int cmd, a;
        cin >> cmd >> a;
        if ( cmd == 1 ) update(1, 1, n, s[a], s[a]);
        else cout << 1LL * depth[a] * sum(1, 1, n, s[a], e[a]) << '\n';
    }
    return 0;
}
```
