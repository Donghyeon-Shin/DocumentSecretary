DFS(Depth First Search)는 노드 탐색 방법 중 하나로, 임의의 노드에서 다음 Branch로 넘어가기 전에 해당 Branch를 완벽하게 탐색하는 방법을 말합니다. DFS는 하나의 Branch씩 탐색하기 때문에 보통 재귀를 이용해 구현됩니다. BFS와 마찬가지로 Visited Array를 사용하여 중복 탐색을 방지합니다. 노드의 개수 n, 간선의 개수 e일 때 시간 복잡도는 O(n+e)입니다.

DFS의 원리는 다음과 같습니다. 예를 들어 Node 1에서 탐색을 시작한다고 가정했을 때, Node 1을 기준으로 왼쪽 Branch부터 탐색하여 Node 2, Node 4, Node 5가 순서대로 호출됩니다. 그 다음 재귀를 통해 Node 4로 돌아가 오른쪽 Branch에 있는 Node 6을 탐색합니다. Node 6은 다음 Branch가 없기 때문에 다른 Branch가 있는 Node 1번까지 올라가 Node 3을 탐색합니다. 이러한 방식은 더 이상 탐색할 수 없을 때까지 반복됩니다.

DFS는 반복문과 재귀를 이용하여 구현되며, 중복 탐색을 방지하는 것이 매우 중요합니다. 아래는 DFS의 C++ 코드 예시입니다:

```cpp
#include <bits/stdc++.h>

using namespace std;

int n; // node cnt
int e; // edge cnt
int start; // start node
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

DFS는 다양한 문제에 응용될 수 있습니다. 예를 들어, 유기농 배추 문제(1012)에서는 DFS를 사용하여 그래프 이론을 적용하고, 방문한 좌표에 Graph 값을 1에서 0으로 바꿈으로써 중복 탐색을 방지했습니다. 내리막 길 문제(1520)에서는 DFS와 DP를 결합하여 문제를 해결했습니다. 

이처럼 DFS는 그래프 탐색에 매우 유용한 알고리즘입니다.