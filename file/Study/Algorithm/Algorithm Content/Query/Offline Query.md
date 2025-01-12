# Concept
- 쿼리를 순서대로 해결하는 것이 아닌 문제를 빠르게 해결하기 위해 쿼리 순서를 바꾸는 알고리즘이다.
- [[DP(Dynamic Programming)]]처럼 정형화 되어 있는 코드는 존재하지 않고 쿼리 문제를 풀 떄 아이디어의 개념으로써 활용된다.
- 쿼리의 순서를 조정해야 하기 때문에 모든 쿼리의 정보를 다 받은 다음에 처리한다.
# Offline Query 원리 (📑[13306 - 트리](https://www.acmicpc.net/problem/13306))
- 쿼리는 총 2종류(1. node와 node의 부모 사이의 간선을 제거해라, 2. node v, w을 연결하는 경로가 존재하는가?)가 있다. 
- 문제를 순서대로 풀게 되면 2번 쿼리를 진행할때마다 그래프를 탐색해 이어져 있는지를 판단해야 한다.
- 문제의 핵심은 노드가 총 N개가 있을 때 1번의 쿼리가 N-1번 있다는 것이다. 즉, 마지막에는 모든 노드들이 서로 분리되어 있음을 뜻한다.
- 따라서 모든 노드들이 분리되어있는 상태에서 역순으로 쿼리를 실행하며 1번 쿼리의 경우 제거하는 것이 아닌 연결하면서 [[Union Find]]으로 부모 노드를 계속 갱신하고 2번 쿼리의 경우 같은 집합에 속하는지 아닌지만 판단하면 된다.
#### 🖼️그림으로 이해하기
![[Offline Query Graph.svg]]

# Offline Query CODE
- `Offline Query 원리`에서는 이해를 위해 쿼리 번호를 1, 2번으로 나누었지만 실제 문제에서는 0, 1이기 때문에 이를 주의하며 작성하여야 한다.
- 역순으로 쿼리를 진행하면서 부모 Node와 자식 Node를 연결해야 하기 때문에 초기에  `v Array`에 이와 관련된 정보를 저장해놓는다
- 이 문제에서는 쿼리를 역으로 바꿔 풀었지만 역으로 바꾸는 것 이외에도 문제 풀이에 맞춰 다양하게 쿼리 순서를 조정할 수 있다.
- 답은 쿼리 순서로 나와야 하기 때문에 쿼리 순서를 잘 저장해 마지막에 답을 출력할때는 쿼리 순서로 나오도록 한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, q, parent[200001], v[200001];

int find_parent(int node) {
    if ( node == parent[node] ) return node;
    return parent[node] = find_parent(parent[node]);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n >> q;
    for ( int i = 1; i <= n; i++ ) parent[i] = i;
    v[1] = 1;
    for ( int i = 2; i < n+1; i++ ) cin >> v[i];
    stack<tuple<bool,int,int>> query;
    
    for ( int i = 0; i < (n-1)+q; i++ ) {
        bool cmd;
        cin >> cmd;
        if ( cmd ) {
            int a, b;
            cin >> a >> b;
            query.push({cmd, a, b});
        } else {
            int a;
            cin >> a;
            query.push({cmd, a, a});
        }
    }
    
    vector<bool> result;
    
    while ( !query.empty() ) {
        bool cmd;
        int a, b;
        tie(cmd, a, b) = query.top();
        query.pop();
        
        if ( cmd ) {
            if ( find_parent(a) == find_parent(b) ) result.push_back(true);
            else result.push_back(false);
        } else parent[a] = v[a];
    }
    
    for ( int i = (int)result.size() - 1; i >= 0; i-- ) {
        if ( result[i] ) cout << "YES\n";
        else cout << "NO\n";
    }
    return 0;
}
```
##### ❓ 예제 Input
	10 4
	1
	1
	3
	3
	3
	2
	4
	5
	5
	0 5
	0 6
	1 5 8
	0 8
	1 9 10
	0 10
	0 9
	1 9 10
	0 7
	0 4
	1 2 3
	0 3
	0 2
##### ⭐ 예제 Output
	 NO
	 YES
	 NO
	 YES
# Offline Query 응용문제
### 📑[15586 - MooTube(Gold)](https://www.acmicpc.net/problem/15586)
#### 🔓 KeyPoint
- 두 노드가 연결되어 있을 때 연결된 간선 중 최소값이 USADO 값이다.
- 처음에 두 노드간의 연결 정보가 주어지는데 이것을 바로 연결하는 것이 아니라 2번 쿼리에 맞춰서 K값보다 큰 값들만 연결 후 [[Union Find]]을 통해 노드 연결된 개수를 Return 한 것이 추천 동영상 수이다.
- 1, 2번 쿼리를 USDAO(K)값이 큰 값부터 처리할 수 있게 정렬해야 하며, 결과를 쿼리 순서대로 출력 해야하기 때문에 쿼리 순서도 기억해서 출력 양식에 맞게  출력해야한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int N, Q, parent[100001], group_Size[100001], result[100001];
vector<tuple<int, int, int>> query_One, query_Two;

int find_Parent(int node) {
    if ( parent[node] == node ) return node;
    return parent[node] = find_Parent(parent[node]);
}

void union_Parent(int n1, int n2) {
    int Pn1 = find_Parent(n1);
    int Pn2 = find_Parent(n2);
    
    if ( Pn1 == Pn2 ) return;
    
    if ( Pn1 < Pn2 ) {
        parent[Pn2] = Pn1;
        group_Size[Pn1] += group_Size[Pn2];
    } else {
        parent[Pn1] = Pn2;
        group_Size[Pn2] += group_Size[Pn1];
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> N >> Q;
    for ( int i = 1; i <= N; i++ ) {
        parent[i] = i;
        group_Size[i] = 1;
    }
    for( int i = 0; i < N-1; i++ ) {
        int p, q, r;
        cin >> p >> q >> r;
        query_One.push_back({-r, p, q});
    }
    for ( int i = 0; i < Q; i++ ) {
        int k, v;
        cin >> k >> v;
        query_Two.push_back({-k, v, i});
    }
    
    sort(query_One.begin(), query_One.end());
    sort(query_Two.begin(), query_Two.end());
    
    int query_One_Index = 0;
    
    for ( int i = 0; i < (int)query_Two.size(); i++ ) {
        int k, v, index;
        tie(k, v, index) = query_Two[i];
        k *= -1;
        
        for ( int j = query_One_Index; j < (int)query_One.size(); j++ ) {
            int p, q, r;
            tie(r, p, q) = query_One[j];
            r *= -1;
            if ( r >= k ) union_Parent(p, q);
            else {
                query_One_Index = j;
                break;
            }
            
            if ( j + 1 == (int)query_One.size() ) query_One_Index = j+1;
        }
        
        int Pv = find_Parent(v);
        result[index] = group_Size[Pv] - 1;
    }
    
    for ( int i = 0; i < Q; i++) cout << result[i] << '\n';
    return 0;
}
```
