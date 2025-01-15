HLD의 응용문제 코드 예시는 다음과 같습니다. 이 코드는 트리 구조에서 두 노드 사이의 연결 여부를 판단하는 문제를 해결하기 위해 작성되었습니다. 

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

이 코드는 HLD(Heavy-Light Decomposition) 알고리즘을 사용하여 트리의 두 노드 간의 연결 여부를 판단하는 문제를 해결합니다. 각 노드의 서브트리 크기를 계산하고, HLD를 통해 간선을 그룹화하여 세그먼트 트리를 사용하여 연결 상태를 관리합니다.