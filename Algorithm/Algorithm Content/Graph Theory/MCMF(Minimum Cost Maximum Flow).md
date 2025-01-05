# Concept
- 그래프 간선에 유량과 비용이 있을 때 최소 비용으로 최대 유량을 구하는 알고리즘이다.
- [[Maximum Flow (Edmonds-Karp Argorithm)]]에서 간선의 비용 정보가 추가된 내용이다.
- SPFA(Shortest Path Faster Algorithm) 알고리즘을 사용한다.
# SPFA(Shortest Path Faster Algorithm) 원리
- Maximum Flow에서 사용하는 Edmonds-Karp Argorithm와 Bellman-Ford Algorithm(like [[Dijkstra's Algorithm]])을 합친 알고리즘이다.
- queue에 탐색할 Node를 넣는 과정에서 `node 최단 거리 = dist`가 업데이트 되면 Queue에 다시 넣는데, 중복 연산을 피하기 위해 isInQueue Array를 만들어 이미 Queue에 있는 node이면 push하지 않도록 한다.
- Capacity말고도 Cost도 유량의 대칭성을 생각해 역방향을 고려해야 한다.
- MCMF에서 구하고자 하는 결과 값은 최소 비용을 가지는 최대 유량이기 때문에 `result += amount(최소 흐르는 유량) * cost[v][u]`이다. 
- 시간 복잡도는 O(VEf)이지만 이것보단 빨라서 O(E) or O(V+E)라고도 계산한다.

# SPFA CODE(📑[11405 - 책 구매하기](https://www.acmicpc.net/problem/11405))
- Maximum Flow을 잘 파악하고 있으면 구현하는게 크게 어렵지 않다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>
#define INF 1e9
#define SOUR 1
#define SINK 2

using namespace std;

int n, m, capacity[205][205], flow[205][205], cost[205][205], result = 0;
vector<int> adj[205];

void mcmf() {
    while ( 1 ) {
        int dist[205], parent[205];
        bool isInQueue[205];
        fill(dist, dist + 205, INF);
        memset(parent, -1, sizeof(parent));
        memset(isInQueue, 0, sizeof(isInQueue));
        
        queue<int> q;
        q.push(SOUR);
        isInQueue[SOUR] = true;
        dist[SOUR] = 0;
        
        while ( !q.empty() ) {
            int node = q.front();
            q.pop();
            
            isInQueue[node] = false;
            
            for ( int i = 0; i < (int)adj[node].size(); i++ ) {
                int nNode = adj[node][i];
                
                if ( capacity[node][nNode] - flow[node][nNode] > 0 && dist[nNode] > dist[node] + cost[node][nNode] ) {
                    dist[nNode] = dist[node] + cost[node][nNode];
                    parent[nNode] = node;
                    if ( !isInQueue[nNode] ) {
                        isInQueue[nNode] = true;
                        q.push(nNode);
                    }
                }
            }
        }
        
        if ( parent[SINK] == -1 ) break;
        
        int amount = INF;
        for ( int i = SINK; i != SOUR; i = parent[i] ) amount = min(amount, capacity[parent[i]][i] - flow[parent[i]][i]);
        for ( int i = SINK; i != SOUR; i = parent[i] ) {
            result += amount * cost[parent[i]][i];
            flow[parent[i]][i] += amount;
            flow[i][parent[i]] -= amount;
        }
        
        // cout << "DONE";
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n >> m;
    for ( int i = 3; i < 3 + n; i++ ) {
        cin >> capacity[SOUR][i];
        adj[SOUR].push_back(i);
        adj[i].push_back(SOUR);
    }
    
    for ( int i = 3 + n; i < 3 + n + m; i++ ) {
        cin >> capacity[i][SINK];
        adj[i].push_back(SINK);
        adj[SINK].push_back(i);
    }
    
    for ( int i = 3 + n; i < 3 + n + m; i++ ) {
        for ( int j = 3; j < 3 + n; j++ ) {
            cin >> cost[j][i];
            cost[i][j] = -cost[j][i];
            capacity[j][i] = INF;
            adj[i].push_back(j);
            adj[j].push_back(i);
        }
    }
    
    mcmf();
    cout << result;
    return 0;
}
```
##### ❓ 예제 Input
	4 4
	3 2 4 2
	5 3 2 1
	5 6 2 1
	3 7 4 1
	2 10 3 1
	10 20 30 1
##### ⭐ 예제 Output
	30
# MCMF 응용문제
### 📑[11408 - 열혈강호5](https://www.acmicpc.net/problem/11408  )
#### 🔓 KeyPoint
- 열혈강호3(Maximum Flow)에서 Cost만 추가한 Basic한 MCMF 문제이다.
- 위 코드를 숙지하고 있으면 크게 어렵지 않게 구현할 수 있다.
- Source, Sink, 직원, 일 총 4개의 그룹으로 나눠야 하기 때문에 이를 신경써서 구현하면 된다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>
#define SOUR 1
#define SINK 2
#define INF 1e9

using namespace std;

int n, m, capacity[805][805], flow[805][805], cost[805][805], parent[805], dist[805], result_Cnt = 0, result_Cost = 0;
bool isInQueue[805];
vector<int> adj[805];

void mcmf() {
    while ( 1 ) {
        fill(dist, dist+805, INF);
        memset(isInQueue, 0, sizeof(isInQueue));
        memset(parent, -1, sizeof(parent));
        dist[SOUR] = 0;
        
        queue<int> q;
        q.push(SOUR);
        isInQueue[SOUR] = true;
        
        while ( !q.empty() ) {
            int node = q.front();
            q.pop();
            isInQueue[node] = false;
            
            for ( int i = 0; i < (int)adj[node].size(); i++) {
                int nNode = adj[node][i];
                
                if ( capacity[node][nNode] - flow[node][nNode] > 0 && dist[nNode] > dist[node] + cost[node][nNode] ) {
                    dist[nNode] = dist[node] + cost[node][nNode];
                    parent[nNode] = node;
                    if ( !isInQueue[nNode] ) {
                        isInQueue[nNode] = true;
                        q.push(nNode);
                    }
                }
            }
        }
        
        if ( parent[SINK] == -1 ) break;
        
        int amount = INF;
        for ( int i = SINK; i != SOUR; i = parent[i] ) amount = min(amount, capacity[parent[i]][i] - flow[parent[i]][i]);
        for ( int i = SINK; i != SOUR; i = parent[i] ) {
            result_Cost += amount * cost[parent[i]][i];
            flow[parent[i]][i] += amount;
            flow[i][parent[i]] -= amount;
        }
        
        result_Cnt++;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    memset(flow, 0, sizeof(flow));
    
    cin >> n >> m;
    for ( int i = 3; i < 3 + n; i++ ) {
        capacity[SOUR][i] = 1;
        adj[SOUR].push_back(i);
        adj[i].push_back(SOUR);
    }
    
    for ( int i = 3 + n; i < 3 + n + m; i++ ) {
        capacity[i][SINK] = 1;
        adj[SINK].push_back(i);
        adj[i].push_back(SINK);
    }
    
    for ( int i = 3; i < 3 + n; i++ ) {
        int cnt;
        cin >> cnt;
        for ( int j = 0; j < cnt; j++ ) {
            int work, weight;
            cin >> work >> weight;
            capacity[i][2+n+work] = 1;
            cost[i][2+n+work] = weight;
            cost[2+n+work][i] = -weight;
            adj[i].push_back(2+n+work);
            adj[2+n+work].push_back(i);
        }
    }
    
    mcmf();
    cout << result_Cnt << '\n' << result_Cost; 
    return 0;
}
```
### 📑[3640 - 제독](https://www.acmicpc.net/problem/3640)
#### 🔓 KeyPoint
- 노드 분리와 연결이 까다로운 MCMF 문제
- 방문한 정점을 두 번 방문하면 안되기 때문에 하나의 정점을 두 개로 분리해 나누어진 정점들을 용량 1로 설정해 두면 한 곳에서 유량을 흘렀을 때 두 번째에는 방문할 수 없게 된다.
- 한 정점의 번호(v)를 `in : (v-1) * 2,  out : (v-1) * 2 + 1`로 번호를 나눈다.
- 두 정점을 v, u를 이을때는 `v_out : (v-1) * 2 + 1 , u_in : (u-1) * 2`에 연결하여야 한다.
- 두 전함이 이동하기 때문에 유량 탐색을 두 번만 진행하면 된다.
- Source와 Sink는 노드 번호 v * 2, v * 2 + 1를 가지고 각각 시작 노드 in과 끝 노드 out에 Capacity 2를 가지게 한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>
#define INF 1e9

using namespace std;

int v, e;

struct Edge {
    int to, capacity, flow, cost;
    Edge* reverse;
    Edge(int _to, int _capcity, int _cost = 0, int _flow = 0) : to(_to), capacity(_capcity), flow(_flow), cost(_cost) {}
    
    int residual() { return capacity - flow; }
    
    void let_Flow(int amount) {
        flow += amount;
        reverse->flow -= amount;
    } 
};

vector<Edge*> adj[2002];

void make_Edge(int inNum, int outNum, int capacity, int cost) {
    Edge* inToOut = new Edge(outNum, capacity, cost);
    Edge* outToIn = new Edge(inNum, 0, -cost);
    
    inToOut->reverse = outToIn;
    outToIn->reverse = inToOut;
    
    adj[inNum].push_back(inToOut);
    adj[outNum].push_back(outToIn);
}

int MCMF(int sour, int sink) {
    int result = 0, t = 2;
    while ( t-- ) {
        int parent[2002], dist[2002];
        bool isInQueue[2002];
        Edge* nodeToEdge[2002];
        
        fill(dist, dist+2002, INF);
        memset(parent, -1, sizeof(parent));
        memset(isInQueue, 0, sizeof(isInQueue));
        
        dist[sour] = 0;
        parent[sour] = sour;
        queue<int> q;
        q.push(sour);
        isInQueue[sour] = true;
        
        while ( !q.empty() ) {
            int node = q.front();
            q.pop();
            
            isInQueue[node] = false;
            
            for ( int i = 0; i < (int)adj[node].size(); i++ ) {
                Edge* e = adj[node][i];
                int nNode = e->to;
                
                if ( e->residual() > 0 && dist[nNode] > dist[node] + e->cost ) {
                    dist[nNode] = dist[node] + e->cost;
                    parent[nNode] = node;
                    nodeToEdge[nNode] = e;
                    
                    if ( !isInQueue[nNode] ) {
                        isInQueue[nNode] = true;
                        q.push(nNode);
                    }
                }
            }
        }
        
        if ( parent[sink] == -1 ) return -1;
        
        for ( int i = sink; i != sour; i = parent[i] ) {
            Edge* e = nodeToEdge[i];
            result += e->cost;
            e->let_Flow(1);
        }
    }
    
    return result;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    while ( cin >> v >> e ) {
        for ( int i = 0; i < 2002; i++ ) adj[i].clear();
		// Source : 2*v, Sink : 2*v + 1
        make_Edge(0, 1, 2, 0); // 시작 노드 in, out 연결
        make_Edge(2 * (v-1), 2 * (v-1) + 1, 2, 0); //도착 노드 in, out 연결
        make_Edge(2 * v, 0, 2, 0); // Source, 시작 노드 in 연결
        make_Edge(2 * (v-1) + 1, 2*v+1, 2, 0); // 도착 노드 out, Sink 연결
        
        for ( int i = 2; i < 2*v; i += 2 ) make_Edge(i, i + 1, 1, 0);
        
        for ( int i = 0; i < e; i++ ) {
            int a, b, c;
            cin >> a >> b >> c;
            make_Edge(2 * (a-1) + 1, 2 * (b-1), 1, c);
        }
        
        cout << MCMF(2*v, 2*v+1) << '\n';
    }
    return 0;
}
```
