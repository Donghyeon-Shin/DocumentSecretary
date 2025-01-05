# Concept
- 
# PBS 원리
- 
#### 🖼️그림으로 이해하기
![[]]
# PBS CODE(📑[1396 - 크루스칼의 공](https://www.acmicpc.net/problem/1396))
- 
#### ⌨️ Code
- 각 쿼리마다 구간`[1,m]`까지의 간선이 연결되어 있을 때 두 노드 x, y가 이어져 있는가를 해결하면 된다.
- 
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, m, q;
int parent[100001], parentSize[100001];
pair<int,int> answer[100001];
pair<int,int> query[100001];
pair<int,int> query_Range[100001];
vector<tuple<int,int,int>> graph;
vector<int> queryMidValue[100001];

int findParent(int node) {
    if ( node == parent[node] ) return node;
    else return parent[node] = findParent(parent[node]);
}

void unionEdge(int n1, int n2) {
    n1 = findParent(n1);
    n2 = findParent(n2);
   
    if ( n1 != n2 ) {
        if ( parentSize[n1] > parentSize[n2] ) swap(n1, n2);
        parentSize[n2] += parentSize[n1];
        parent[n1] = n2;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
   
    cin >> n >> m;
    for ( int i = 0; i < m; i++ ) {
        int a, b, c;
        cin >> a >> b >> c;
        graph.push_back({c, a, b});
    }
    sort(graph.begin(), graph.end());
   
    cin >> q;
    for ( int i = 0; i < q; i++ ) {
        int x, y;
        cin >> x >> y;
        query[i].first = x; query[i].second = y;
        // query_Range[i].first : leftValue, query_Range[i].second : rightValue
        query_Range[i].first = 1; query_Range[i].second = m;
        answer[i].first = -1; answer[i].second = -1;
    }
   
    while ( 1 ) {
        bool flag = false;
        for ( int i = 1; i <= m; i++ ) queryMidValue[i].clear();
       
        for ( int i = 0; i < q; i++ ) {
            int queryLeftValue = query_Range[i].first;
            int queryRightValue = query_Range[i].second;
            if ( queryLeftValue <= queryRightValue ) {
                flag = true;
                queryMidValue[(queryLeftValue + queryRightValue) / 2].push_back(i);
            }
        }
       
        if ( !flag ) break;
        for ( int i = 1; i <= n; i++ ) {
            parent[i] = i;
            parentSize[i] = 1;
        }
       
        int midValue = 1;
       
        for ( auto grpahElement : graph ) {
            int c = get<0>(grpahElement), a = get<1>(grpahElement), b = get<2>(grpahElement);
            unionEdge(a, b);
           
            for ( auto queryMidIndex : queryMidValue[midValue] ) {
                int x = query[queryMidIndex].first, y = query[queryMidIndex].second;
                if ( findParent(x) == findParent(y) ) {
                    answer[queryMidIndex].first = c;
                    answer[queryMidIndex].second = parentSize[findParent(x)];
                    query_Range[queryMidIndex].second = midValue - 1;
                } else query_Range[queryMidIndex].first = midValue + 1;
            }
            midValue++;
        }
    }
   
    for ( int i = 0; i < q; i++ ) {
        pair<int,int> ansElement = answer[i];
        int x = ansElement.first, y = ansElement.second;
        if ( x == -1 ) cout << -1 << '\n';
        else cout << x << ' ' << y << '\n';
    }
    return 0;
}
```
##### ❓ 예제 Input
	5 4
	1 2 1
	2 3 2
	3 4 4
	4 5 3
	2
	1 5
	2 3
##### ⭐ 예제 Output
	4 5
	2 3
# PBS 응용문제
### 📑[5542 - JOI 국가의 행사](https://www.acmicpc.net/problem/5542)
#### 🔓 KeyPoint
- 
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>
#define INF 1e9

using namespace std;

int n, m, k, q;
int dist[100001], answer[100001], parent[100001], nodeRank[100001];
vector<pair<int,int>> edge[200001], edgeInfo;
vector<tuple<int,int,int>> edgeInfoSortedByDist;
set<int> query[100001];
priority_queue<pair<int,int>> pq;

int findParent(int node) {
    if ( node == parent[node] ) return node;
    return parent[node] = findParent(parent[node]);
}

void nodeUnion(int n1, int n2) {
    n1 = findParent(n1);
    n2 = findParent(n2);
   
    if ( n1 == n2 ) return;
   
    if ( nodeRank[n1] < nodeRank[n2] ) parent[n1] = n2;
    else if ( nodeRank[n1] > nodeRank[n2] ) parent[n2] = n1;
    else {
        if ( n1 < n2 ) {
            nodeRank[n2]++;
            parent[n1] = n2;
        } else {
            nodeRank[n1]++;
            parent[n2] = n1;
        }        
    }
}

void dijkstra() {
    while ( !pq.empty() ) {
        int cost = -pq.top().first;
        int node = pq.top().second;
        pq.pop();
       
        if ( dist[node] < cost ) continue;
       
        for ( auto nodeInfo : edge[node] ) {
            int nNode = nodeInfo.first;
            int nCost = nodeInfo.second;
            if ( dist[node] + nCost < dist[nNode] ) {
                dist[nNode] = dist[node] + nCost;
                pq.push({-dist[nNode], nNode});
            }
        }
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
   
    cin >> n >> m >> k >> q;
    for ( int i = 0; i < m; i++ ) {
        int n1, n2, cost;
        cin >> n1 >> n2 >> cost;
        edge[n1].push_back({n2, cost});
        edge[n2].push_back({n1, cost});
        edgeInfo.push_back({n1, n2});
    }
   
    fill(dist, dist+100001, INF);
    fill(answer, answer+100001, -1);
   
    for ( int i = 0; i < k; i++ ) {
        int festivalNode;
        cin >> festivalNode;
        dist[festivalNode] = 0;
        pq.push({0, festivalNode});
    }
   
    dijkstra();
    
    for ( int i = 0; i < m; i++ ) {
        int n1 = edgeInfo[i].first;
        int n2 = edgeInfo[i].second;
       
        int minimumFestivalDist = min(dist[n1], dist[n2]);
        edgeInfoSortedByDist.push_back({minimumFestivalDist, n1, n2});
    }
    sort(edgeInfoSortedByDist.begin(), edgeInfoSortedByDist.end());
    reverse(edgeInfoSortedByDist.begin(), edgeInfoSortedByDist.end());
   
    for ( int i = 0; i < q; i++ ) {
        int startNode, endNode;
        cin >> startNode >> endNode;
        query[startNode].insert(i);
        query[endNode].insert(i);
    }
   
    for ( int i = 1; i <= n; i++ ) parent[i] = i;
    
    for ( auto edge : edgeInfoSortedByDist ) {
        int cost = get<0>(edge);
        int n1 = get<1>(edge);
        int n2 = get<2>(edge);

        n1 = findParent(n1);
        n2 = findParent(n2);
       
        if ( n1 == n2 ) continue;
        
        if ( nodeRank[n1] > nodeRank[n2] || (nodeRank[n1] == nodeRank[n2] && n2 < n1) ) swap(n1, n2);
        
        for ( auto iter = query[n1].begin(); iter != query[n1].end(); iter++ ) {
            int queryIdx = (*iter);
            if ( query[n2].count(queryIdx) != 0 ) answer[queryIdx] = cost;
            query[n2].insert(queryIdx);
        }
        nodeUnion(n1, n2);
    }
    
    for ( int i = 0; i < q; i++ ) cout << answer[i] << '\n';
    return 0;
}
```
### 📑[16074 - Mountaineers](https://www.acmicpc.net/problem/16074)
#### 🔓 KeyPoint
- 
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, m, q, maxmumHeight = -1, mountain[501][501], parent[250501];
pair<int,int> query[100001], queryRange[100001];
vector<int> queryMidValue[1000001];
vector<pair<int,int>> graph[1000001];

int edgeIndexing(int x, int y) {
    return (500 * x + y);
}

int findParent(int edge) {
    if ( parent[edge] == edge) return edge;
    return parent[edge] = findParent(parent[edge]);
}

void edgeUnion(int e1, int e2) {
    e1 = findParent(e1);
    e2 = findParent(e2);
   
    if ( e1 != e2 ) parent[e1] = e2;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
   
    cin >> m >> n >> q;
    for ( int i = 1; i <= m; i++ ) {
        for ( int j = 1; j <= n; j++ ) {
            cin >> mountain[i][j];
            maxmumHeight = max(maxmumHeight, mountain[i][j]);
        }
    }
 
    for ( int i = 1; i <= m; i++ ) {
        for ( int j = 1; j <= n; j++ ) {
            int presentIdx = edgeIndexing(i, j);
            if ( i + 1 <= m ) {
                int nextIdx = edgeIndexing(i+1, j);
                int greaterHeight = max(mountain[i][j], mountain[i+1][j]);
                graph[greaterHeight].push_back({presentIdx, nextIdx});
            }
           
            if ( j + 1 <= n ) {
                int nextIdx = edgeIndexing(i, j+1);
                int greaterHeight = max(mountain[i][j], mountain[i][j+1]);
                graph[greaterHeight].push_back({presentIdx, nextIdx});
            }
        }
    }

    for ( int i = 0; i < q; i++ ) {
        int x1, y1, x2, y2;
        cin >> x1 >> y1 >> x2 >> y2;
        int startIdx = edgeIndexing(x1, y1);
        int endIdx = edgeIndexing(x2, y2);
        query[i].first = startIdx; query[i].second = endIdx;
        if ( startIdx == endIdx ) queryRange[i].first = queryRange[i].second = mountain[startIdx/500][startIdx%500];
        else {
            queryRange[i].first = 1; 
            queryRange[i].second = maxmumHeight;
        }
    }

    while ( 1 ) {
        bool flag = false;
        
        for ( int i = 0; i <= 1000000; i++ ) queryMidValue[i].clear();
       
        for ( int i = 0; i < q; i++ ) {
            int queryLeftValue = queryRange[i].first;
            int queryRightValue = queryRange[i].second;
           
            if ( queryLeftValue < queryRightValue ) {
                flag = true;
                queryMidValue[(queryLeftValue + queryRightValue) / 2].push_back(i);
            }
        }
        
        if ( !flag ) break;
       
        for ( int i = 1; i < 250501; i++ ) parent[i] = i;

        for ( int midValue = 1; midValue <= maxmumHeight; midValue++ ) {
            for ( auto edge : graph[midValue] ) {
                int presentIdx = edge.first;
                int nextIdx = edge.second;
                edgeUnion(presentIdx, nextIdx);
            }
            
            for ( auto queryMidIndex : queryMidValue[midValue] ) {
                int startIdx = query[queryMidIndex].first;
                int endIdx = query[queryMidIndex].second;
               
                if ( findParent(startIdx) == findParent(endIdx) ) queryRange[queryMidIndex].second = midValue;
                else queryRange[queryMidIndex].first = midValue + 1;
            }
        }
    }
    
    for ( int i = 0; i < q; i++ ) cout << (queryRange[i].first + queryRange[i].second) / 2 << '\n';
    return 0;
}
```