### MST (최소 스패닝 트리) 요약

1. **개념**
   - 스패닝 트리는 그래프에서 모든 노드가 (n-1)개의 엣지로 연결된 트리를 의미합니다.
   - 최소 스패닝 트리(MST)는 노드에 연결된 엣지 중에서 비용의 합이 최소인 스패닝 트리입니다.
   - MST를 구하기 위해서는 `Union Find`와 Greed Method인 `Kruskal` 알고리즘을 사용합니다.
   - 시간 복잡도는 `O(M*logM)`입니다. (M: 간선의 개수)

2. **MST 원리**
   - 모든 엣지를 비용 기준으로 오름차순 정렬합니다.
   - 비용이 작은 엣지를 순서대로 연결하되, 사이클이 발생하지 않도록 `Union Find`를 통해 연결합니다.

3. **예시 코드 (Kruskal 알고리즘)**
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
   - **예제 Input**
     ```
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
     ```
   - **예제 Output**
     ```
     46
     ```

4. **MST 응용 문제**
   - **문제 1: 별자리 만들기**
     - 별들을 노드로 보고, 별들 간의 거리를 엣지 비용으로 사용합니다. 비용은 직접 계산해야 합니다.
   - **문제 2: 행성 터널**
     - 노드가 x, y, z 좌표를 갖고, 엣지 비용은 `min(x - x', y - y', z - z')`로 계산합니다.

이상으로, MST에 대한 개념과 알고리즘, 예제 코드 및 응용 문제를 요약하였습니다.