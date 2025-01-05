# Concept
- 무방향 그래프에서 특정 점 또는 선을 제거했을 때 한 개의 **Conponent**가 두 개 이상으로 증가하는 것을 뜻한다.
- 단절점과 단절선은 사이에 있는 점들은 해당 값이 존재해야만 서로 연결될 수 있으므로 한 개의 Coponent를 이루기 위해 필수적이다.
- [[DFS(Depth-First Search)]] 스패닝 트리를 이용해 구할 수 있으며 시간복잡도는 `정점의 개수 : V`라 할 때 O(V)이다.
# Articulation Points And Bridges 원리 
### Articulation Points 원리
- 특정 점 V가 단절점이기 위해서는 두 가지 특징 중 하나를 만족해야 한다.
> 1. V가 Root Node일 때 연속으로 방문되지 않은 자식이 2개 이상이라면, 해당 노드는 단절점이다.
> 2. V가 Root Node가 아니고 방문되지 않은 자식들의 탐색 경로가 V보다 먼저 탐색된 노드로 갈 수 없는 경우, 해당 노드는 단절점이다.
- [[DFS(Depth-First Search)]] 스패닝 트리를 만든 뒤, 방문 순서를 매겨준다.
- 모든 노드마다 **low** 값을 만들어 저장하는데, low의 초기 값은 방문 순서이다.
- `low = min(먼저 방문된 노트들 중 가장 작은 먼저 방문된 노드 번호, 방문되지 않는 노드들 중 가장 작은 low값)`로 low가 지속적으로 업데이트 된다.
- 특정 노드(V)에서 아직 방문되지 않는 노드로 탐색 할 때는 방문되지 않는 노드로부터 low값을 return 받게 되는데, 만약 **V의 방문 번호보다 low값이 크거나 같은** 노드가 있다면 해당 노드는 V를 거치지 않고는 다른 노드로 갈 수 없기 때문에 V는 단절점이다.
#### 🖼️그림으로 이해하기(Articulation Points)
![[Articulation Points graph.svg]]
### Articulation Bridges 원리
- 특정 간선 E가 단절선이기 위해서는 한가지 특성을 만족해야 한다.
> 1. 노드 A와 아직 방문되지 않은 노드 B가 E로 연결되어 있을 때, B가 V가 아닌 간선으로 먼저 탐색된 노드로 갈 수 없는 경우, 해당 노드는 단절선이다.
- 단절점과 마찬가지로 [[DFS(Depth-First Search)]] 스패닝 트리를 만든 뒤, 방문 순서를 매겨준다.
- Tree Edge가 아닌 간선들은 단절선이 될 수 없기 때문에 따로 연산하지 않는다.
- 모든 노드마다 **low** 값을 만들어 저장하는데, 단절점과 다르게 부모 노드의 방문 번호는 영향을 주지 않게 한다.
- 특정 노드(V)에서 아직 방문되지 않는 노드로 탐색 할 때는 방문되지 않는 노드로부터 low값을 return 받게 되는데, 만약 **V의 방문 번호보다 low값이 큰** 노드가 있다면 그 둘을 잇는 간선 E를 거치지 않고는 서로가 다른 노드로 갈 수 없기 때문에 E는 단절선이다.
#### 🖼️그림으로 이해하기(Articulation Bridges)
![[Articulation Bridges graph.svg]]

# Articulation Points And Bridges CODE
- Points와 Bridges의 조건이 비슷하면서 조금 다르기 때문에 항상 조건에 유의하여 구현해야 한다.
- 무방향 그래프이기 때문에 간선을 이어줄 때 양방향으로 값을 넣어주어야 한다.
- Articulation Points에서는 DFS를 탐색할 때 해당 노드가 Root 노드인지 파악해야 하고 Articulation Bridges에서는 해당 노드의 다음 노드가 부모 노드인지 파악해야 한다.
- 구현하는 과정에서 주어진 그래프가 하나로 이어져 있다는 보장이 없기 때문에 방문 번호(초기값 -1)를 이용해 모든 노드를 탐색할 수 있도록 한다.
#### ⌨️ Articulation Points Code 📑[11266 - 단절점](https://www.acmicpc.net/problem/11266)
```cpp
#include <bits/stdc++.h>

using namespace std;

int v, e, discover[10001], number = 0, cnt = 0;;
bool articul_Point[10001] = {0, };
vector<int> graph[10001];

int dfs(int node, bool isRoot) {
    
    discover[node] = ++number;
    int result = discover[node];
    int child = 0;
    
    for ( int i = 0; i < (int)graph[node].size(); i++ ) {
        int nNode = graph[node][i];
        if ( discover[nNode] == -1 ) {
            child++;
            int val = dfs(nNode, false);
            if ( !isRoot && val >= discover[node] && !articul_Point[node] ) {
                cnt++;
                articul_Point[node] = true;   
            }
            result = min(result, val);
        } else result = min(result, discover[nNode]);
    }
    
    if ( isRoot && child >= 2 && !articul_Point[node] ) {
        cnt++;
        articul_Point[node] = true;
    }
    return result;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    memset(discover, -1, sizeof(discover));
    
    cin >> v >> e;
    for ( int i = 0; i < e; i++ ) {
        int n1, n2;
        cin >> n1 >> n2;
        graph[n1].push_back(n2);
        graph[n2].push_back(n1);
    }
    
    for ( int i = 1; i <= v; i++ ) {
        if ( discover[i] == -1 ) dfs(i, true);
    }
    
    cout << cnt << '\n';
    for ( int i = 1; i <= v; i++ ) {
        if ( articul_Point[i] ) cout << i << ' ';
    }
    return 0;
}
```
##### ❓ 예제 Input
	9 10
	1 2
	2 3
	2 4
	3 4
	4 5
	4 8
	5 6
	6 7
	6 8
	8 9
##### ⭐ 예제 Output
	4
	2 4 6 8
#### ⌨️ Articulation Bridges Code 📑[11400 - 단절선](https://www.acmicpc.net/problem/11400)
```cpp
#include <bits/stdc++.h>

using namespace std;

int v, e, discover[100001], cnt = 0;
vector<int> graph[100001];
vector<pair<int,int>> result;

int dfs(int node, int parent)  {

    discover[node] = ++cnt;
    int least = discover[node];
    
    for ( int i = 0; i < (int)graph[node].size(); i++ ) {
        int nNode = graph[node][i];
        
        if ( nNode == parent ) continue;
        if ( discover[nNode] == -1) {
            int low = dfs(nNode, node);
            if ( low > discover[node] ) result.push_back({min(node, nNode), max(node, nNode)});
            least = min(low, least);
        } else least = min(discover[nNode], least); 
    }
    return least;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    memset(discover, -1, sizeof(discover));
    
    cin >> v >> e;
    for ( int i = 0; i < e; i++ ) {
        int n1, n2;
        cin >> n1 >> n2;
        graph[n1].push_back(n2);
        graph[n2].push_back(n1);
    }
    
    for ( int i = 1; i <= v; i++ ) {
        if ( discover[i] == -1 ) dfs(i, 0);
    }
    
    sort(result.begin(), result.end());
    cout << (int)result.size() << '\n';
    for ( int i = 0; i < (int)result.size(); i++ ) cout << result[i].first << ' ' << result[i].second << '\n';
    return 0;
}
```
##### ❓ 예제 Input
	9 10
	1 2
	2 3
	2 4
	3 4
	4 5
	4 8
	5 6
	6 7
	6 8
	8 9
##### ⭐ 예제 Output
	3
	1 2
	6 7
	8 9