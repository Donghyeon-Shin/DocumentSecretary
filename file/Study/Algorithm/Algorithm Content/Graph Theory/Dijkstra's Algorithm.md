# Concept
- 노드 사이의 최단 경로를 탐색하는 Algorithm이다.
- 특정 노드에서 연결되어 있는 모든 정점간의 최단 경로를 구할 수 있다.
- 음의 간선이 있는 경우에는 Dijkstra Algorithm을 사용할 수 없다.
# Dijkstra's Algorithm 원리
- 노드 간의 간선 거리(비용)을 2차원 배열 dist()()라고 표현한다.
- 처음 dist()()을 INF로 초기화 한 다음 시작 Node를 기준으로 이동 가능한 간선을 업데이트 한다.
- 방문하지 않는 노드를 시작 노드에서 경유하는 과정을 통해 최소 비용으로 업데이트하면서  방문 가능한 모든 노드를 최소 비용으로 업데이트한다.
- Priority Queue를 이용해 [[BFS(Breadth-First Search)]]의 방문 탐색을 이용해 구현 할 수 있다.
#### 🖼️그림으로 이해하기
![[Dijkstra Graph.svg]]
# Dijkstra's Algorithm CODE
- Priority Queue를 이용해 비용이 최소로 연결되어 있는 노드부터 탐색하는 것이 전체 탐색 횟수를 줄일 수 있다.
- Priority Queue는 기본적으로 내림차순으로 정렬이 되기 때문에 오름차순 정렬을 하고 싶으면 음수로 push한 다음 pop할때 다시 -1를 곱해 정수로 만든다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>
#define INF 1e9

using namespace std;

int v,e,k, dist[20001];
vector<pair<int,int>> graph[20001];

void dijkstra(int start) {
    priority_queue<pair<int,int>> pq;
    dist[start] = 0;
    pq.push({0, start});
    while ( !pq.empty() ) {
        int cost = -pq.top().first;
        int node = pq.top().second;
        pq.pop();

        if ( dist[node] < cost ) continue;

        for ( int i = 0; i < (int)graph[node].size(); i++ ) {
            int n_cost = graph[node][i].first;
            int n_node = graph[node][i].second;

            if ( dist[n_node] > dist[node] + n_cost ) {
                dist[n_node] = dist[node] + n_cost;
                pq.push({-dist[n_node], n_node});
            }
        }
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    cin >> v >> e >> k;
    for ( int i = 0; i < e; i++ ) {
        int n1, n2, cost;
        cin >> n1 >> n2 >> cost;
        graph[n1].push_back({cost, n2});
        graph[n2].push_back({cost, n1});
    }

    fill(dist, dist+v+1, INF);

    dijkstra(k);

    for ( int i = 1; i <= v; i++ ) {
        if ( dist[i] == INF ) cout << "INF" << '\n';
        else cout << dist[i] << '\n'; 
    }
    return 0;
}
```
##### ❓ 예제 Input
	7 12 1
	1 2 3
	1 3 5
	1 4 7
	2 3 2
	2 4 2
	2 5 6
	2 6 1
	3 6 5
	3 7 10
	4 5 3
	5 6 4
	6 7 3 
##### ⭐ 예제 Output
	0
	3
	5
	5
	8
	4
	7
# Dijkstra's Algorithm 응용문제
### 📑[1504 - 특정한 최단 경로](https://www.acmicpc.net/problem/1504)
#### 🔓 KeyPoint
- 특정 노드를 무조건 방문하면서 도착 노드에 가야하는 조건이 추가된 Dijkstra 문제이다.
- 방문해야 하는 노드가 n1, n2라 할 때 최단 거리를 두 개로 나누어 답을 구해야 한다.
- 거리1 : 시작 노드 -> n1 -> n2  / 거리2 : 시작 노드 -> n2 -> n1
- Dijkstra를 두 번 사용하여 거리1과 거리2를 구한 뒤, 최소 값을 찾으면 그것이 답이다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>
#define INF 9876543

using namespace std;

int n, e, dist[801], point[3], v1, v2, result;
vector<pair<int,int>> graph[801];
bool check_v1, check_v2;

void dijkstra(int start) {
    priority_queue<pair<int,int>> pq;
    dist[start] = 0;
    pq.push({0, start});
    while ( !pq.empty() ) {
        int cost = -pq.top().first;
        int node = pq.top().second;
        pq.pop();

        for ( int i = 0; i < (int)graph[node].size(); i++ ) {
            int n_cost = graph[node][i].first;
            int n_node = graph[node][i].second;

            if ( dist[n_node] > dist[node] + n_cost) {
                dist[n_node] = dist[node] + n_cost;
                pq.push({-dist[n_node], n_node});
            }
        }
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    cin >> n >> e;
    for ( int i = 0; i < e; i++ ) {
        int n1, n2, cost;
        cin >> n1 >> n2 >> cost;
        graph[n1].push_back({cost, n2});
        graph[n2].push_back({cost, n1});
    }
    cin >> v1 >> v2;
    fill(dist, dist+n+1, INF);
    dijkstra(1);

    check_v1 = check_v2 = true;

    if ( dist[v1] == INF ) check_v1 = false;
    if ( dist[v2] == INF ) check_v2 = false;

    point[1] = dist[v1];
    point[2] = dist[v2];

    fill(dist, dist+n+1, INF);
    dijkstra(v1);

    if ( check_v1 ) point[1] += dist[v2];
    if ( check_v2 ) {
        point[2] += dist[v2];
        point[2] += dist[n];
    }

    fill(dist, dist+n+1, INF);
    dijkstra(v2);

    if ( check_v1 ) point[1] += dist[n];

    if ( !check_v1 && !check_v2 ) result = -1;
    else result = min(point[1],point[2]);

    if ( result >= INF ) result = -1;
    cout << result;
    return 0;
}
```
### 📑[11779 - 최소비용 구하기2](https://www.acmicpc.net/problem/11779)
#### 🔓 KeyPoint
- Baisc한 Dijkstra 문제에서 최소 거리를 가기 위해 방문한 노드까지 파악해야 되는 문제이다.
- dist가 업데이트 될 때마다 노드끼리 연결되어 있는 정보(connect)도 업데이트한 다음 마지막에 역방향으로 방문한 노드를 탐색하면 된다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>
#define INF (int)1e9

using namespace std;

int n, m, start, arrival, dist[1001], connect[1001];
vector<pair<int,int>> graph[1001];
vector<int> result;

void dijkstra() {
    dist[start] = 0;
    priority_queue<pair<int,int>> pq;
    pq.push({0, start});
    while ( !pq.empty() ) {
        int cost = -pq.top().first;
        int node = pq.top().second;
        pq.pop();
        if ( node == arrival ) return;
        if ( cost > dist[node] ) continue;
        for ( int i = 0; i < (int)graph[node].size(); i++ ) {
            int n_cost = graph[node][i].first;
            int n_node = graph[node][i].second;
            if ( dist[n_node] > cost + n_cost ) {
                connect[n_node] = node;
                dist[n_node] = cost + n_cost;
                pq.push({-dist[n_node], n_node});
            }
        }
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);

    cin >> n >> m;
    for ( int i = 0; i < m; i++ ) {
        int from, to, cost;
        cin >> from >> to >> cost;
        graph[from].push_back({cost, to});
    }
    cin >> start >> arrival;
    fill(dist, dist+n+1, INF);
    dijkstra();
    cout << dist[arrival] << '\n';
    int temp = arrival;
    while ( temp ) {
        result.push_back(temp);
        temp = connect[temp];
    }
    cout << result.size() << '\n';
    for ( int i = (int)result.size()-1; i >= 0; i-- ) cout << result[i] << ' ';
    return 0;
}
```
