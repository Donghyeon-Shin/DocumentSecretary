# Concept
- `Tree`에 **Edge**을 'Heavy Edge'와 'Light Edge'로 나누어 구분하는 알고리즘이다.
- 부모 Node(`u`)와 u의 자식 Node(`v`)를 있는 Edge(`e`)가 있을 때, v의 Sub Tree 크기가 u의 Sub Tree 크기의 1/2 이상일 때 `e`를 **Heavy Edge**라 정의하며 이 이외에는 모두 **Light Edge**이다.
- `Size[Node] : Node의 Sub Tree 크기`라 정의하면 `Heavy Edge는 Size[v] >= Size[u] / 2`를 만족한다. 
- 어떠한 Node에서 Light Edge을 타고 올라갈 경우 `무조건 Sub Tree의 크기가 2배 이상`이 되게 되며 이는 다시 말해 어떠한 Node에서 Root Node로 가는 경우 최대 **logN**개의 Light Edge을 거쳐가게 된다는 것을 뜻한다.
- 특정 Node u와 v가 있을 때 그 둘을 잇는 Light Edge는 최대 **2 * logN**개 이다.
- Edge를 각각 Heavy Edge와 Light Edge를 분리하여 **이어지는 Heavy Edge를 하나의 그룹**으로써 그리고 **Light Edge는 개별적인 그룹**으로써 값을 관리하면 `구간의 Edge`를 효율적으로 관리할 수 있다.
- 쉽게 말해, Edge를 Heavy, Light로 나누고 이어지는 Heavy는 하나의 그룹으로 보면서 Node u와 v를 잇는 Edge들을 하나하나 보는 것이 아닌 각 `Edge 그룹` 별로 처리하는 알고리즘이다.
- [[DFS(Depth-First Search)]]를 이용해 Edge를 Heavy Edge와 Light Edge로 나누기 때문에 `O(N)`의 시간복잡도가 소요된다.
- 각각의 나누어진 Edge들은 구간 계산을 위해 [[Segment Tree]]을 이용하게 되며, `O(logN)`만큼의 시간복잡도가 소요된다.
# HLD 원리
- HLD의 구현은 크게 2가지이다.
	1. Edge를 각각 Heavy Edge와 Light Edge로 나눈다.
		>1.1 [[DFS(Depth-First Search)]] 이용해 `Root Node`부터 탐색을 시작해 각 노드들의 `Sub Tree의 Size`를 계산한다.
		>1.2~3 DFS를 한 번 사용하여 Root Node부터 탐색을 시작해 Hevey Edge를 판별하고 [[ETT(Euler Tour Technique)]]을 이용해 각 Node(또는 Edge)의 구간을 정의한다.
		>**구현의 편의성으로 위해 Heavy  Edge를 `Sub Node 중 가장 Sub Tree의 크기가 큰 노드로 이어진 Edge`로 정의한다.**
	2. 나누어진 Edge를 토대로 구간 계산을 진행한다.
		>2.1 [[Segment Tree]]을 이용해 Edge를 구간마다 업데이트를 진행한다.
		>2.2 DFS로 나누어진 Edge와 ETT로 계산된 해당 Edge의 구간을 보면서 같은 그룹이 나올 때 까지 Light Edge의 구간 계산을 진행하며 해당 Edge를 건넌다.
		>2.3 같은 그룹이라면 해당 Node들의 구간을 고려하여 구간 계산을 진행한다.
		> (* [[LCA(Lowest Common Ancestor)]]로도 구현 가능하나, 개인적으로 코드가 복잡해 선호하진 않는다.)
#### 🖼️그림으로 이해하기
![[HLD Graph.svg]]
# HLD CODE(📑[13510 - 트리와 쿼리 1](https://www.acmicpc.net/problem/13510))
- 앞서 살펴봤듯이 HLD를 구현하기 위해서는 [[DFS(Depth-First Search)]], [[ETT(Euler Tour Technique)]], [[Segment Tree]]를  선행으로 알고 있어야 하기 때문에 난이도가 있는 알고리즘이다.
- 코드를 보고 *Debug* 과정을 손으로 그리면서 생각해보는 것이 이해하는데 많은 도움이 될 것이다.
- 처음 DFS를 하는 과정에서 Parent의 정보를 기록해 놓으면 후에 ETT를 계산하는 과정이나 Light Edge를 건너는 과정에서 활용할 수 있다.
- 그룹(구간)의 편의성을 위해 Heavy Edge를 Edge Vector 맨 앞으로 위치 시킨다. 이렇게 하면 ETT을 계산하는 과정에서 *Heavy Edge의 번호가 연속성*을 가지게 되어 `Segement Tree`
을 활용할 수 있게 된다. *(nNode와 maximumSubTreeNode의 주소를 Swap한다.)*
- 해당 문제에서는 `s[node] = parent[node]와 node를 잇는 Edge의 번호`로 정의하기 때문에 `e[node]`를 구하긴 했지만 사용하지 않아도 문제를 해결 할 수 있다.
- `head[node] = 같은 그룹의 가장 Depth가 낮은 node`로 Edge를 건너는 과정에서 활용되며 ETT를 구하는 과정에서 함께 구한다. *단 초기에 head[Root Node] = 전체 Tree의 Root Node로 init해야 한다.*
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>
#define MAX_SIZE 100001

using namespace std;

int n, m, u[MAX_SIZE], v[MAX_SIZE], w[MAX_SIZE];
int parent[MAX_SIZE] = {0, }, subTreeSize[MAX_SIZE] = {0, }, s[MAX_SIZE], e[MAX_SIZE], head[MAX_SIZE], range_Cnt = 0;
vector<int> adj[MAX_SIZE], segment_Tree;

int calcul_SubTreeSize(int node) {
    subTreeSize[node] = 1;
    for ( int& nNode : adj[node] ) {
        if ( nNode == parent[node] ) continue;
        parent[nNode] = node;
        subTreeSize[node] += calcul_SubTreeSize(nNode);
        int& maximumSubTreeNode = adj[node][0];
        // 서브트리가 가장 큰 자식을 맨 앞으로 옮김 = segment_Tree를 연산할 때 무거운 번호 먼저 방문 하도록 설정
        if ( maximumSubTreeNode == parent[node] || subTreeSize[maximumSubTreeNode] < subTreeSize[nNode] ) swap(maximumSubTreeNode, nNode);
    }
    return subTreeSize[node];
}

void hld(int node) {
    s[node] = ++range_Cnt;
    for ( int &nNode : adj[node] ) {
        if ( nNode == parent[node] ) continue;
        head[nNode] = (nNode == adj[node][0]) ? head[node] : nNode; // *무거운 경로(서브트리가 가장 큼)에 해당하면 head로 같이 묶고 아니면 가벼운 간선으로 만듦 
        hld(nNode);
    }
    e[node] = range_Cnt;
}

void update( int node, int start, int end, int target, int val ) {
    if ( end < target || target < start ) return;
    if ( start == end ) {
        segment_Tree[node] = val;
        return;
    }
    
    int mid = (start + end) / 2;
    update(node*2, start, mid, target, val);
    update(node*2 + 1, mid + 1, end, target, val);
    segment_Tree[node] = max(segment_Tree[node*2], segment_Tree[node*2+1]);
}

int calcul_MaximumEdgeWeight(int node, int start, int end, int left, int right) {
    if ( end < left || right < start ) return 0;
    if ( left <= start && end <= right ) return segment_Tree[node];
    
    int mid = (start + end) / 2;
    return max(calcul_MaximumEdgeWeight(node*2, start, mid, left, right), calcul_MaximumEdgeWeight(node*2+1, mid + 1, end, left, right));
}

int query(int n1, int n2) {
    int result = 0;
    while ( head[n1] != head[n2] ) {
        if ( subTreeSize[head[n1]] < subTreeSize[head[n2]] ) swap(n1, n2);
        result = max(result, calcul_MaximumEdgeWeight(1, 1, n, s[head[n2]], s[n2]));
        n2 = parent[head[n2]];
    }
    if ( s[n1] > s[n2] ) swap(n1, n2);
    result = max(result, calcul_MaximumEdgeWeight(1, 1, n, s[n1] + 1, s[n2]));
    return result;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n;
    int height = int(ceil(log2(n)));
    int tree_Size = (1 << (height + 1));
    segment_Tree.resize(tree_Size);
    
    for ( int i = 1; i < n; i++ ) {
        cin >> u[i] >> v[i] >> w[i];
        adj[u[i]].push_back(v[i]);
        adj[v[i]].push_back(u[i]);
    }
    
    head[1] = 1; // head init of Root Node
    calcul_SubTreeSize(1);
    hld(1);
    
    for ( int i = 1; i < n; i++ ) {
        if ( parent[u[i]] == v[i] ) swap(u[i], v[i]);
        update(1, 1, n, s[v[i]], w[i]);
    }
    
    cin >> m;
    while ( m-- ) {
        int q, a, b;
        cin >> q >> a >> b;
        if ( q == 1 ) {
            if ( parent[u[a]] == v[a] ) swap(u[a], v[a]);
            update(1, 1, n, s[v[a]], b);
        } else cout << query(a, b) << '\n';
    }
    return 0;
}
```
##### ❓ 예제 Input
	11
	1 2 5
	2 3 3
	3 5 18
	3 6 21
	2 4 1
	1 7 7
	7 8 2
	8 9 3
	8 10 9
	10 11 13
	4
	2 8 11
	2 3 10
	1 5 100
	2 11 4
##### ⭐ 예제 Output
	13
	9
	100
# HLD 응용문제
### 📑[13309 - 트리](https://www.acmicpc.net/problem/13309)
#### 🔓 KeyPoint
- 예제(📑[13510 - 트리와 쿼리 1](https://www.acmicpc.net/problem/13510))에서 본 문제랑 근본은 같다.
- 두 Node 사이를 연결하는 Edge가 존재하는지 판단하기 위해 `Bool 타입`에 Segment Tree 구현한다.
- 모든 간선이 연결되어 있기 때문에 처음 Segment Tree는 모두 1(True)로 초기화한다.
- Edge를 제거할 때는 해당 Edge의 번호를 0으로 업데이트 하면 된다.
- 두 노드의 구간에 대해서 Segment Tree의 값이 `1`이 나오면 두 노드를 잇는 Edge가 존재하는 것이고 `0`이 나오면 없는 것이다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>
#define MAX_SIZE 200001


using namespace std;

int n, q, head[MAX_SIZE] = {0, }, subTreeSize[MAX_SIZE] = {0 }, parent[MAX_SIZE] = {0, }, s[MAX_SIZE], e[MAX_SIZE], rangeCnt = 0;
vector<int> adj[MAX_SIZE], boolSegmentTree;

int calcul_SubTreeSize(int node) {
    subTreeSize[node] = 1;
    for ( int& nNode : adj[node] ) {
        if ( nNode == parent[node] ) continue;
        parent[nNode] = node;
        subTreeSize[node] += calcul_SubTreeSize(nNode);
        int& maximumSubTreeNode = adj[node][0];
        if ( maximumSubTreeNode == parent[node] || subTreeSize[maximumSubTreeNode] < subTreeSize[nNode] ) swap(maximumSubTreeNode, nNode);
    }
    return subTreeSize[node];
}
void hld(int node) {
    s[node] = ++rangeCnt;
    for ( auto nNode : adj[node] ) {
        if ( nNode == parent[node] ) continue;
        head[nNode] = (nNode == adj[node][0]) ? head[node] : nNode;
        hld(nNode);
    }
    e[node] = rangeCnt;
}

bool init(int node, int start, int end) {
    if ( start == end ) return boolSegmentTree[node] = 1;
    int mid = (start + end) / 2;
    return boolSegmentTree[node] = (init(node*2, start, mid) && init(node*2 + 1, mid + 1, end));
}

bool calcul_Connect(int node, int start, int end, int left, int right) {
    if ( end < left || right < start ) return 1;
    if ( left <= start && end <= right ) return boolSegmentTree[node];
    
    int mid = (start + end) / 2;
    return (calcul_Connect(node*2, start, mid, left, right) && calcul_Connect(node*2 + 1, mid + 1, end, left, right));
}

bool IsConnectedTwoNodes(int n1, int n2) {
    bool result = 1;
    while ( head[n1] != head[n2] ) {
        if ( subTreeSize[head[n1]] < subTreeSize[head[n2]] ) swap(n1, n2);
        result &= calcul_Connect(1, 1, n, s[head[n2]], s[n2]);
        n2 = parent[head[n2]];
        
    }
    if ( s[n1] > s[n2] ) swap(n1, n2);
    result &= calcul_Connect(1, 1, n, s[n1] + 1, s[n2]);
    return result;
}

void removeEdgeInSegmentTree(int node, int start, int end, int target) {
    if ( end < target || target < start ) return;
    if ( start == end ) {
        boolSegmentTree[node] = 0;
        return;
    }
    
    int mid = (start + end) / 2;
    removeEdgeInSegmentTree(node*2, start, mid, target);
    removeEdgeInSegmentTree(node*2 + 1, mid + 1, end, target);
    boolSegmentTree[node] = (boolSegmentTree[node*2] && boolSegmentTree[node*2 + 1]);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n >> q;
    
    int height = int(ceil(log2(n)));
    int tree_Size = ( 1 << (height + 1));
    boolSegmentTree.resize(tree_Size);
    
    for ( int i = 2; i <= n; i++ ) {
        int node;
        cin >> node;
        adj[node].push_back(i);
        adj[i].push_back(node);
    }
    
    head[1] = 1;
    calcul_SubTreeSize(1);
    hld(1);
    init(1, 1, n);

    while ( q-- ) {
        int v1, v2;
        bool IsRemoveEdge;
        
        cin >> v1 >> v2 >> IsRemoveEdge;
        if ( IsConnectedTwoNodes(v1, v2) ) {
            cout << "YES\n";
            if ( IsRemoveEdge ) removeEdgeInSegmentTree(1, 1, n, s[v1]);
        } else {
            cout << "NO\n";
            if ( IsRemoveEdge ) removeEdgeInSegmentTree(1, 1, n, s[v2]);
        }
    }
    return 0;
}
```