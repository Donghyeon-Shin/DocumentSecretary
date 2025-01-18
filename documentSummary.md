Spanning Tree는 그래프에서 Node의 개수가 n이라고 했을 때 모든 Node들이 (n-1)개의 Edge로 연결되어 있는 Tree를 뜻합니다. Spanning Tree는 DFS(Depth-First Search)나 BFS(Breadth-First Search)로 Node을 탐색하며 구할 수 있으며, 이때 Spanning Tree는 사이클이 포함되서는 안됩니다. 또한, Minimum Spanning Tree는 Nodes에 연결되어 있는 Edges 중 Cost를 고려하여 Spanning Tree 중 가장 Cost의 합이 적은 Tree를 말합니다. Minimum Spanning Tree를 구하기 위해서 Union Find와 Greed Method인 `Kruskal`알고리즘을 사용하며, MST의 시간복잡도는 `O(M*logM)`이 됩니다. (M : 간선의 개수)

MST의 원리는 모든 Edges의 Cost를 기준으로 오름차순으로 정렬한 후, Cost가 작은 Edge 순서대로 이어서 Spanning Tree를 만드는 것입니다. 이 과정에서 사이클이 만들어지면 안되기 때문에 Union Find를 통해 Disjoint Set을 만들고, 두 정점이 다른 집합에 있다면 해당 간선을 연결하도록 합니다.

MST의 코드는 Vector 자료구조를 이용하여 Edge의 정보를 넣는데, 간선의 비용을 기준으로 정렬을 하기 때문에 Cost를 먼저 넣어주어야 합니다. Edge을 선택하는 과정에서 간선의 개수가 n-1개를 넘어서면 안되기 때문에 `kruskal()`에서 간선의 개수가 n-1이 되면 함수를 종료합니다.

또한, MST의 응용문제로는 별자리 만들기와 행성 터널 문제가 있습니다. 이들은 각각 Priority Queue 자료구조와 좌표를 이용한 MST 알고리즘을 사용하여 해결할 수 있습니다.

이러한 내용들을 토대로 MST 알고리즘과 그 응용 문제들에 대해 자세히 설명하였습니다.