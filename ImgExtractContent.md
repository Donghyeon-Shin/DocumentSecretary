MST는 Minimum Spanning Tree의 약자로, 그래프에서 모든 노드를 최소 비용으로 연결하는 트리를 의미합니다. MST를 구하는 방법으로는 크루스칼 알고리즘과 프림 알고리즘이 있으며, 각 알고리즘은 간선의 가중치를 기준으로 최소 비용의 트리를 만들어냅니다. 크루스칼 알고리즘은 간선을 기준으로, 프림 알고리즘은 노드를 기준으로 최소 비용의 트리를 만들어내는데, 각 알고리즘은 시간복잡도가 O(ElogE) 또는 O(V^2)로 효율적으로 동작합니다. MST는 네트워크 설계, 클러스터링, 노드 간 최소 연결 등 다양한 분야에서 활용되며, 각 분야에 따라 적합한 알고리즘과 방법을 선택하여 사용할 수 있습니다.

DFS(Depth-First Search)는 노드 탐색 방법 중 하나로, 임의의 노드에서 다음 Branch로 넘어가기 전에 해당 Branch를 완벽하게 탐색하는 방법을 말합니다. 이는 하나의 Branch씩 탐색하기 때문에 보통 재귀를 이용해 구현하며, 시간 복잡도는 O(n+e)입니다. DFS는 반복문과 재귀를 이용하여 구현하며, 중복 탐색를 방지하는 것이 매우 중요하기 때문에 이를 신경써서 구현하여야 합니다. DFS는 유기농 배추 문제와 내리막 길 문제 등 다양한 응용 문제에서 사용될 수 있습니다.

BFS는 Queue 자료구조를 이용해 구현한다. BFS는 노드 탐색 방법 중 하나로, 임의의 노드에서 인접한 노드들을 먼저 탐색하는 방법을 말합니다. 인접한 노드들을 먼저 탐색하기 때문에 FIFO(선입선출)형 자료구조인 Queue를 사용한다. 가중치에 따라 탐색 순서가 달라지는 0-1 BFS도 있는데 이는 Priority Queue를 사용한다. 보통 Visited Array를 만들어 중복 탐색을 방지한다. 노드의 개수 n, 간선의 개수 e이라 할 때 시간 복잡도는 O(n+e)이다.

BFS 동작 과정은 Node 1에서부터 탐색을 시작하여 깊이 우선 탐색을 진행한다. 이를 Queue로 표현하면 BFS Queue.svg와 같이 된다.

BFS CODE는 Queue 자료구조를 이용해 구현한다. 코드는 다음과 같다.
```cpp
#include <bits/stdc++.h>

using namespace std;

int n; // node cnt
int e; // edge cnt
int start; // start node
vector<int> graph[10001];
bool visited[10001] = {0, };

void bfs(int node) {
	queue<int> q;
	q.push(node);
	visited[node] = true;
	
	while ( !q.empty() ) {
		int pNode = q.front();
		q.pop();
		cout << pNode << ' ';
		for ( int i = 0; i < (int)graph[pNode].size(); i++ ) {
			int nNode = graph[pNode][i];
			if ( !visited[nNode] ) {
				visited[nNode] = true;
				q.push(nNode);
			}
		}
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
	bfs(start);
	return 0;
}
```
예제 Input과 Output은 다음과 같다.
##### ❓ 예제 Input
	10
	9
	1 2
	1 3
	2 4
	4 5
	4 6
	3 7
	3 8
	8 9
	8 10
	1
##### ⭐ 예제 Output
	1 2 3 4 7 8 5 6 9 10

BFS 응용문제로는 2178 - 미로 탐색과 17114 - 하이퍼 토마토가 있다.

Union Find은 여러 노드들을 그룹으로 묶고 특정 노드들이 같은 그룹인지 판단하는 알고리즘입니다. Union(노드들을 그룹으로 묶는 과정)과 Find(특정 노드들을 같은 그룹인지 판단하는 과정)으로 나눌 수 있습니다. Union Find로만 해결할 수 있는 문제는 거의 없으며, 보조 도구로 사용됩니다. 시간복잡도는 최적화 여부 및 순서에 따라 다르지만 경로 압축을 하지 않은 Union Find는 노드의 개수를 n이라 할 때 최대 O(n)이 걸립니다. 경로 압축을 할 경우 O(logN)이 걸리지만 실질적으로 O(a(N))이라고 합니다. `a(x)는 애커만 함수로 x = 2^65536일때 a(x) = 5가 되기 때문에 상수 시간이라고 볼 수 있습니다`

Union Find 원리는 Find는 재귀함수를 통해 부모 노드를 찾는 과정인데 경로 압축이 이루어지지 않으면 트리의 깊이가 l이라면 Find 함수를 실행할 때마다 l만큼 연산을 수행합니다. 이를 줄이기 위해 재귀를 통해 얻은 최종 부모를 모든 자식 노드에 업데이트하는 과정으로 연산 과정을 줄일 수 있습니다. `return parent[node] = find(parent[node])` 만약 `Parent[node] == node`라면 해당 노드가 root 노드이기 때문에 이를 return 합니다(종료 조건). Union은 각각 노드의 부모 노드를 찾고 이를 이어서 노드를 연결합니다. `Union(node1, node2) = parent[node1] = node2 OR parent[node2] = node1`

Union Find CODE는 다음과 같습니다.
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, m, q, parent[10001];

int find(int node) {
    if ( parent[node] == node ) return node;
    return parent[node] = find(parent[node]);
}

void node_Union(int n1, int n2) {

    int n1_root = find(n1);
    int n2_root = find(n2);

    if ( n1_root < n2_root ) parent[n2_root] = n1_root;
    else parent[n1_root] = n2_root;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n >> m >> q;
    for ( int i = 1; i <= n; i++ ) parent[i] = i;
    for ( int i = 0; i < m; i++ ) {
        int a, b;
        cin >> a >> b;
        node_Union(a, b);
    }
    
    for ( int i = 0; i < q; i++ ) {
        int a;
        cin >> a;
        cout << find(a) << '\n';
    }
    return 0;
}
```
##### ❓ 예제 Input
	8 6 4
	1 2
	1 3
	2 4
	3 5
	5 6
	4 7
	3
	7
	6
	8
##### ⭐ 예제 Output
	1
	1
	1
	8

이미지 파일은 크루스칼 알고리즘을 시각적으로 설명하고 있으며, 이를 통해 기존 답변을 보다 명확하게 이해할 수 있습니다.