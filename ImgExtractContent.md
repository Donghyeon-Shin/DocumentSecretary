HLD(Heavy-Light Decomposition)은 트리 구조에서 간선을 'Heavy Edge'와 'Light Edge'로 나누어 구분하는 알고리즘입니다. 이 알고리즘은 부모 노드(`u`)와 자식 노드(`v`) 간의 간선(`e`)이 있을 때, `v`의 서브 트리 크기가 `u`의 서브 트리 크기의 1/2 이상일 경우 해당 간선을 **Heavy Edge**로 정의하며, 이 외의 경우는 모두 **Light Edge**로 간주합니다.

HLD의 주요 원리는 다음과 같습니다:
1. **Heavy Edge와 Light Edge 구분**: DFS(Depth-First Search)를 사용하여 각 노드의 서브 트리 크기를 계산하고, 이를 바탕으로 Heavy Edge와 Light Edge를 판별합니다.
2. **구간 계산**: 나누어진 Edge를 기반으로 구간 계산을 진행하며, 이를 위해 Segment Tree를 사용합니다.

HLD를 통해 특정 노드 `u`와 `v`를 연결하는 Light Edge는 최대 **2 * logN**개가 될 수 있으며, Light Edge를 타고 올라갈 경우 서브 트리의 크기가 2배 이상 증가하게 됩니다. 이러한 구조를 통해 HLD는 효율적으로 트리의 간선을 관리하고, 구간 쿼리를 수행할 수 있게 됩니다.

HLD의 구현은 복잡하지만, DFS, ETT(Euler Tour Technique), Segment Tree와 같은 기법을 활용하여 효율적인 트리 쿼리 처리를 가능하게 합니다.

DFS(Depth-First Search)는 임의의 노드에서 다음 Branch로 넘어가기 전에 해당 Branch를 완벽하게 탐색하는 방법을 말합니다. 이를 통해 노드의 서브 트리 크기를 계산하고, Heavy Edge와 Light Edge를 판별하는 데 사용됩니다. DFS는 보통 재귀를 이용해 구현되며, 중복 탐색을 방지하기 위해 Visited Array를 사용합니다.

DFS의 구현은 다음과 같습니다:
```cpp
#include <bits/stdc++.h>

using namespace std;

int n; // 노드 개수
int e; // 간선 개수
int start; // 시작 노드
vector<int> graph[10001];
bool visited[10001] = {0, };

void dfs(int node) {
    cout << node << ' ';
    visited[node] = true;
    for ( int i = 0; i < (int)graph[node].size(); i++ ) {
        int nNode = graph[node][i];
        if ( !visited[nNode] ) dfs(nNode);
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n >> e;
    for ( int i = 0; i < e; i++ ) {
        int a, b;
        cin >> a >> b;
        graph[a].push_back(b);
        graph[b].push_back(a);
    }
    cin >> start;
    dfs(start);
    return 0;
}
```

DFS는 다양한 응용 문제에 사용될 수 있습니다. 예를 들어, 그래프 이론 문제인 "유기농 배추"나 "내리막 길" 등에서 DFS를 사용하여 문제를 해결할 수 있습니다.