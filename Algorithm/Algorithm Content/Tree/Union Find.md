# Concept
- 여러 노드들을 그룹으로 묶고 특정 노드들이 같은 그룹인지 판단하는 알고리즘이다.
- Union(노드들을 그룹으로 묶는 과정)과 Find(특정 노드들을 같은 그룹인지 판단하는 과정)으로 나눌 수 있다.
- Union Find로만 해결할 수 있는 문제는 거의 없다. Union Find는 여러 문제를 해결하기 위한 보조 도구로 많이 사용된다.
- 시간복잡도는 최적화 여부 및 순서에 따라 다르지만 경로 압축을 하지 않은 Union Find는 노드의 개수를 n이라 할 때 최대 O(n)이 걸린다. 경로 압축을 할 경우 O(logN)이 걸리지만 실질적으로 O(a(N))이라고 한다. `a(x)는 애커만 함수로 x = 2^65536일떄 a(x) = 5가 되기 떄문에 사살싱 상수 시간이라고 볼 수 있다`
# Union Find 원리
- Find는 재귀함수를 통해 부모 노드를 찾는 과정인데 경로 압축이 이루어지지 않으면 트리의 깊이가 l이라면 Find 함수를 실행할때마다 l만큼 연산을 수행한다.
- 이를 줄이기 위해 재귀를 통해 얻은 최종 부모를 모든 자식 노드에 업데이트하는 과정으로 연산 과정을 줄일 수 있다. `return parent[node] = find(parent[node])`
- 만약 `Parent[node] == node`라면 해당 노드가 root 노드이기 때문에 이를 return 한다(종료 조건).
- Union은 각각 노드의 부모 노드를 찾고 이를 이어서 노드를 연결한다. `Union(node1, node2) = parent[node1] = node2 OR parent[node2] = node1`
#### 🖼️그림으로 이해하기
![[Union Find Graph.svg]]
# Union Find CODE
- `Parent[i] = i번째 Node의 부모`를 선언하고 초기에 `Parent[i] = i`로 초기화해 준다.
- Union을 하는 과정에서 Find 함수로 해당 노드들의 부모 노드를 가져와 그 둘을 Union해준다.
- 일반적으로 부모 노드들을 Union하는 과정에서 `번호가 작은 노드가 번호가 큰 노드의 부모가 되도록` 설정해주지만, 상황/문제에 따라 기준을 다르게 할 수도 있다.
#### ⌨️ Code
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