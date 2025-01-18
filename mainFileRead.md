# Concept
- Spanning Tree는 그래프에서 Node의 개수가 n이라고 했을 때 모든 Node들이 (n-1)개의 Edge로 연결되어 있는 Tree를 뜻한다.
- Spanning Tree는 [[DFS(Depth-First Search)]]나 [[BFS(Breadth-First Search)]]로 Node을 탐색하며 구할 수 있다. 이때 Spanning Tree는 사이클이 포함되서는 안된다.
- Minimum Spanning Tree는 Nodes에 연결되어 있는 Edges 중 Cost를 고려하여 Spanning Tree 중 가장 Cost의 합이 적은 Tree를 말한다.
- Minimum Spanning Tree를 구하기 위해서 [[Union Find]]와 Greed Method인 `Kruskal`알고리즘을 사용한다.
- MST의 시간복잡도는 `O(M*logM)`이다. (M : 간선의 개수)
# MST 원리
- 모든 Edges의 Cost를 기준으로 오름차순으로 정렬한다, 그 후 Cost가 작은 Edge 순서대로 이어서 Spanning Tree를 만든다.
- 이 과정에서 사이클이 만들어지면 안되기 때문에 [[Union Find]]를 통해 `Disjoint Set`을 만들고, 두 정점이 다른 집합에 있다면 해당 간선을 연결하도록 한다.
#### 🖼️그림으로 이해하기
![[MST Graph.svg]]
# MST CODE(📑[1197 - 최소 스패닝 트리](https://www.acmicpc.net/problem/1197))
- Vector 자료구조를 이용하여 Edge의 정보를 넣는데 간선의 비용을 기준으로 정렬을 하기 때문에 Cost를 먼저 넣어주어야 한다.
- Edge을 선택하는 과정에서 간선의 개수가 n-1개를 넘어서면 안되기 때문에 `kruskal()`에서 간선의 개수가 n-1이 되면 함수를 종료한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int v, e, parent[10001], weight_sum = 0, cnt = 0;
vector<tuple<int,int,int>> tree;

int find_root(int node) {
    if ( parent[node] == node ) return node;
    return parent[node] = find_root(parent[node]);
}

void union_root(int n1, int n2) {

    int n1_root = find_root(n1);
    int n2_root = find_root(n2);

    if ( n1_root != n2_root ) parent[n2_root] = n1_root;

}

void kruskal() {

    for ( int i = 0; i < (int)tree.size(); i++ ) {
        int cost = get<0>(tree[i]);
        int n1 = get<1>(tree[i]);
        int n2 = get<2>(tree[i]);

        if ( find_root(n1) == find_root(n2) ) continue;

        weight_sum += cost;
        cnt++;
        union_root(n1, n2);

        if ( cnt == v - 1 ) return;
    }

}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);

    cin >> v >> e;
    for ( int i = 0; i < e; i++ ) {
        int n1, n2, cost;
        cin >> n1 >> n2 >> cost;
        tree.push_back({cost,n1,n2});
    }
    
    for ( int i = 1; i <= v; i++ ) parent[i] = i;

    sort(tree.begin(), tree.end());

    kruskal();
    cout << weight_sum;
    return 0;
}
```
##### ❓ 예제 Input
	8 15
	1 2 8
	1 5 12
	1 6 10
	2 4 4
	2 3 6
	2 5 14
	3 4 16
	3 7 8
	4 5 7
	4 7 12
	5 6 6
	5 7 5
	5 8 30
	6 8 10
	7 8 20
##### ⭐ 예제 Output
	46

# MST 응용문제
### 📑[4386 - 별자리 만들기](https://www.acmicpc.net/problem/4386)
#### 🔓 KeyPoint
- 별들이 각각의 Node가 되고 별들 사이의 거리가 간선의 Cost가 된다. Cost가 Input으로 주어지는 것이 아닌 직접 구하는 것임에  유의해야 한다.
- Input 데이터를 넣을 때마다 정렬이 될 수 있게 Vector 자료 구조가 아닌 Priority Queue 자료구조를 이용했고 Priority Queue의 경우 기본이 내림차순이기 때문에 `Cost *= -1`를 하여 오름차순으로 정렬될 수 있게 하였다.
- 오차 범위가 10<sup>-2</sup>이기 때문에 출력 부분을 별도로 설정해주어야 한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, parent[100];
double result = 0;
vector<pair<double, double>> v;
priority_queue<tuple<double, int, int>> pq;

int find_root(int node) {
    if ( parent[node] == node ) return node;
    else return parent[node] = find_root(parent[node]);
}

void union_root(int n1, int n2) {
    int n1_root = find_root(n1);
    int n2_root = find_root(n2);
    
    if ( n1_root != n2_root ) parent[n2_root] = n1_root;
} 

void kruskal() {
    while ( !pq.empty() ) {
        double cost;
        int n1, n2;
        tie(cost, n1, n2) = pq.top();
        cost *= -1;
        pq.pop();
        
        if ( find_root(n1) == find_root(n2) ) continue;
        result += cost;
        union_root(n1, n2);
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n;
    for ( int i = 0; i < n; i++ ) {
        parent[i] = i;
        double x, y;
        cin >> x >> y;
        v.push_back({x, y});
        for ( int j = 0; j < (int)v.size() -1; j++ ) {
            double px, py;
            tie(px, py) = v[j];
            double cost = sqrt(pow(px-x, 2) + pow(py-y, 2));
            pq.push({-cost, i, j});
        }
    }
    
    kruskal();
    cout << fixed;
    cout.precision(2);
    cout << result;
    return 0;
}
```
### 📑[2887 - 행성 터널](https://www.acmicpc.net/problem/2887)
#### 🔓 KeyPoint
- 노드들은 각각 x, y, z,의 좌표를 가지고 있으며 이 노드들을 연결하는 Edge의 Cost를 계산하는 방법은 `min(x - x', y - y', z - z')`이다.
- 각각 노드들을 연결하는 Edge의 Cost를 구해도 되지만, 이럴 경우 계산 양이 많아지게 된다.
- 노드들의 x, y, z 값들을 오름차순 정렬하고 정렬 기준, 바로 `인접해 있는 노드들의 사이의 거리`만 구하면 된다. 
- 예를 들어 n1, n2, n3의 x값들이 각각 1, 5, 10이라고 하자. 만약 3개 노드들의 y, z값들의 차이가 커 x값들의 연결 비용이 최소 비용 즉, Edge의 Cost가 된다고 할 때, `n1 - n2를 연결하는 비용(4)과 n2 - n3를 연결하는 비용(5)`이 MST의 비용인 것이다. 인접하지 않는 `n1 - n3의 연결 비용은 9`이기 때문에 n2와 n3 사이의 Edge를 선택해야 하는 것이다. 따라서 인접한 노드들끼리만 비교해도 MST를 구할 수 있다.
- Priority Queue를 사용해 인접한 노드들의 x, y, z 값을 넣어주고 MST를 구해주면 된다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, parent[100001];
long long result = 0;
priority_queue<tuple<int, int, int>> pq;
vector<pair<int,int>> x_Base, y_Base, z_Base;

int find_root(int node) {
    if ( parent[node] == node ) return parent[node];
    return parent[node] = find_root(parent[node]);
}

void union_root(int n1, int n2) {
    int n1_root = find_root(n1);
    int n2_root = find_root(n2);
    
    if ( n1_root != n2_root ) parent[n2_root] = n1_root;
}

void kruskal() {
    
    while ( !pq.empty() ) {
        int cost, n1, n2;
        tie(cost, n1, n2) = pq.top();
        cost *= -1;
        pq.pop();
        
        if ( find_root(n1) == find_root(n2) ) continue;
        result += cost;
        union_root(n1, n2);
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n;
    
    for ( int i = 1; i <= n; i++ ) parent[i] = i;
    
    for ( int i = 1; i <= n; i++ ) {
        int x, y, z;
        cin >> x >>  y >> z;
        x_Base.push_back({x, i});
        y_Base.push_back({y, i});
        z_Base.push_back({z, i});
    }
    sort(x_Base.begin(), x_Base.end());
    sort(y_Base.begin(), y_Base.end());
    sort(z_Base.begin(), z_Base.end());
    
    for ( int i = 0; i < n-1; i++ ) {
        pq.push({-(x_Base[i+1].first - x_Base[i].first), x_Base[i].second, x_Base[i+1].second});
        pq.push({-(y_Base[i+1].first - y_Base[i].first), y_Base[i].second, y_Base[i+1].second});
        pq.push({-(z_Base[i+1].first - z_Base[i].first), z_Base[i].second, z_Base[i+1].second});
    }
    
    kruskal();
    
    cout << result;
    return 0;
}
```