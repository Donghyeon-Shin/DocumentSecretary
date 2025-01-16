HLD(Heavy-Light Decomposition)은 트리 구조에서 간선을 'Heavy Edge'와 'Light Edge'로 나누어 구분하는 알고리즘입니다. 이 알고리즘은 부모 노드(`u`)와 자식 노드(`v`) 간의 간선(`e`)이 있을 때, `v`의 서브 트리 크기가 `u`의 서브 트리 크기의 1/2 이상일 경우 해당 간선을 **Heavy Edge**로 정의하며, 이 외의 경우는 모두 **Light Edge**로 간주합니다.

HLD의 주요 원리는 다음과 같습니다:
1. **Heavy Edge와 Light Edge 구분**: DFS(Depth-First Search)를 사용하여 각 노드의 서브 트리 크기를 계산하고, 이를 바탕으로 Heavy Edge와 Light Edge를 판별합니다.
2. **구간 계산**: 나누어진 Edge를 기반으로 구간 계산을 진행하며, 이를 위해 Segment Tree를 사용합니다.

HLD를 통해 특정 노드 `u`와 `v`를 연결하는 Light Edge는 최대 **2 * logN**개가 될 수 있으며, Light Edge를 타고 올라갈 경우 서브 트리의 크기가 2배 이상 증가하게 됩니다. 이러한 구조를 통해 HLD는 효율적으로 트리의 간선을 관리하고, 구간 쿼리를 수행할 수 있게 됩니다.

HLD의 구현은 복잡하지만, DFS, ETT(Euler Tour Technique), Segment Tree와 같은 기법을 활용하여 효율적인 트리 쿼리 처리를 가능하게 합니다.

ETT(Euler Tour Technique)는 Root Node에서 시작해 방문 번호(cnt)를 매기기 시작해 DFS를 진행하면서 해당 노드의 `s[node] = node의 진입 방문 번호, e[node] = node의 탈출 방문 번호`를  구하면 됩니다. DFS를 통해 구현하기 때문에 시간복잡도는 dfs와 같은 O(n+e) / `노드의 개수 n, 간선의 개수 e`이며, ETT를 사용하는 코드는 다음과 같습니다:

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

ETT의 응용문제로는 2820 - 자동차 공장과 18227 - 성대나라의 물탱크 문제가 있습니다. 이를 해결하기 위해 Segment Tree나 Lazy Segment Tree를 사용하여 구간 정보를 처리하고, DFS를 통해 ETT를 구한 뒤 문제를 해결합니다.

LCA(Lowest Common Ancestor)는 트리에서 두 노드의 최소 공통 조상을 찾는 알고리즘입니다. LCA를 구하는 방법에는 여러가지 방법이 있으며, 대부분 2번 방법을 이용해 LCA를 구합니다. LCA의 원리는 `level[i] = i번 노드의 깊이`와 `parent[i][j] = i의 2^j의 부모`의 정보를 토대로 찾게됩니다. LCA를 구하는 코드는 다음과 같습니다:

```cpp
#include <bits/stdc++.h>
#define MAX_HEIGHT 18

using namespace std;

int n, m, level[100001], parent[100001][MAX_HEIGHT];
vector<int> graph[100001];

void dfs(int node, int height, int p) {

    level[node] = height;
    parent[node][0] = p;
    for ( int i = 1; i < MAX_HEIGHT; i++ ) parent[node][i] = parent[parent[node][i-1]][i-1];
    
    for ( int i = 0; i < (int)graph[node].size(); i++ ) {
        int nNode = graph[node][i];
        if ( level[nNode] == -1 ) dfs(nNode, height+1, node);
    }
}

int get_Common_Ancestor(int n1, int n2) {
    
    if ( n1 == 1 || n2 == 1 ) return 1;
    
    if ( level[n1] != level[n2] ) {
        for ( int i = MAX_HEIGHT - 1; i >= 0; i-- ) {
            if ( level[parent[n1][i]] >= level[n2] ) n1 = parent[n1][i];
        }
    }
    
    int result = n1;
    if ( n1 != n2 ) {
        for ( int i = MAX_HEIGHT - 1; i >= 0; i-- ) {
            if ( parent[n1][i] != parent[n2][i] ) {
                n1 = parent[n1][i];
                n2 = parent[n2][i];
            }
            result = parent[n1][i];
        }
    }
    
    return result;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    memset(level, -1, sizeof(level));
    
    cin >> n;
    for ( int i = 0; i < n-1; i++ ) {
        int n1, n2;
        cin >> n1 >> n2;
        graph[n1].push_back(n2);
        graph[n2].push_back(n1);
    }
    
    dfs(1, 1, 0);
    
    cin >> m;
    for ( int i = 0; i < m; i++ ) {
        int n1, n2;
        cin >> n1 >> n2;
        if ( level[n1] > level[n2] ) cout << get_Common_Ancestor(n1, n2) << '\n';
        else cout << get_Common_Ancestor(n2, n1) << '\n';
    }
    return 0;
}
```

LCA의 응용문제로는 1761 - 정점들의 거리와 3176 - 도로 네트워크 문제가 있습니다. LCA를 구하는 대표적인 문제이며, 이를 해결하기 위해 DFS를 통해 LCA를 구한 뒤 문제를 해결합니다.