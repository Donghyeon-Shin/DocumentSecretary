HLD(Heavy Light Decomposition)을 배우기 위해서는 다음과 같은 지식이 필요합니다:

1. **트리 구조 이해**: HLD는 트리 구조에서 작동하는 알고리즘이므로, 트리의 기본 개념과 구조를 이해해야 합니다. 특히, 부모 노드와 자식 노드의 관계, 서브트리의 개념을 알아야 합니다.

2. **DFS(Depth-First Search)**: HLD의 구현 과정에서 DFS를 사용하여 각 노드의 서브트리 크기를 계산하고, Heavy Edge와 Light Edge를 구분하는 데 필요합니다. DFS의 작동 방식과 재귀적 호출에 대한 이해가 필수적입니다.

3. **서브트리 크기 계산**: 각 노드의 서브트리 크기를 계산하는 방법을 알아야 합니다. 이는 HLD에서 Heavy Edge를 정의하는 데 중요한 역할을 합니다.

4. **Euler Tour Technique(ETT)**: HLD에서는 ETT를 사용하여 각 노드 또는 엣지의 구간을 정의합니다. ETT의 개념과 구현 방법을 이해해야 합니다.

5. **Segment Tree**: HLD의 구간 계산을 위해 Segment Tree를 사용합니다. Segment Tree의 구조와 업데이트 및 쿼리 방법을 이해해야 합니다.

6. **LCA(Lowest Common Ancestor)**: HLD의 구현에서 LCA를 사용할 수 있지만, 코드가 복잡해질 수 있으므로 개인적으로 선호하지 않는다고 언급되어 있습니다. LCA의 개념과 활용 방법도 알고 있으면 좋습니다. LCA를 구하는 방법에는 여러가지 방법이 있으며, 주로 DFS와 DP를 이용하여 구현합니다.

7. **시간 복잡도**: HLD의 시간 복잡도에 대한 이해가 필요합니다. DFS는 O(N)의 시간 복잡도를 가지며, Segment Tree의 쿼리 및 업데이트는 O(logN)입니다.

또한, DFS(Depth-First Search)의 개념과 구현 방법에 대한 보충 내용이 있습니다. DFS는 재귀를 이용하여 구현되며, 중복 탐색을 방지하기 위해 Visited Array를 사용합니다. 또한, DFS의 응용문제로는 "유기농 배추"와 "내리막 길" 문제가 있습니다. "유기농 배추" 문제는 그래프 이론에 DFS를 사용하는 대표적인 문제이며, "내리막 길" 문제는 DFS와 DP를 결합하여 해결할 수 있는 문제입니다.

Euler Tour Technique(ETT)은 Root Node에서 시작해 방문 번호(cnt)를 매기기 시작해 DFS를 진행하면서 해당 노드의 `s[node] = node의 진입 방문 번호, e[node] = node의 탈출 방문 번호`를  구하면 된다. `s[node]`는 해당 Node가 방문된 번호이고 `e[node]`는 해당 Node의 자식들 중 가장 방문 번호가 늦은 번호이다. 모든 Node를 탐색하고 얻은 s,e가 해당 Node의 구간 정보이다. DFS만 알고 있다면 이해하는데 어렵지 않은 알고리즘이다.

Euler Tour Technique CODE는 다음과 같다.
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, m, cnt = 0, s[100001], e[100001];
vector<int> graph[100001];

void dfs(int node) {
    s[node] = ++cnt;
    for ( auto nNode : graph[node] ) {
        if ( s[nNode] == 0 ) dfs(nNode);
    }
    e[node] = cnt;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n >> m;
    for ( int i = 0; i < m; i++ ) {
        int n1, n2;
        cin >> n1 >> n2;
        graph[n1].push_back(n2);
    }
    
    int root = 1;
    dfs(root);
    
    for ( int i = 1; i <= n; i++ ) cout << "Node " << i << " : " << s[i] << ' ' << e[i] << '\n';
    return 0;
}
```

Euler Tour Technique은 응용문제로 "자동차 공장" 문제와 "성대나라의 물탱크" 문제가 있다. "자동차 공장" 문제는 회사 조직도가 Tree형태로 주어지고, 특정 직원의 월급이 변화하면 그 직원의 부하 직원(자식 Node) 또한 변화한다. Tree에 구간 정보를 처리해야기 때문에 ETT를 사용해야 한다. "성대나라의 물탱크" 문제는 수도(Root)에서 각 도시까지의 물탱크가 Tree형태로 연결되어 있고, 자식 도시의 물탱크는 현재 도시(Node)의 + 1 물을 채우기 때문에 이를 Segment Tree로 풀 수 있다.

# Segment Tree
- Node 값에 배열의 범위를 가진 이진 Tree Struct의 일종이다.
- `배열의 범위`는 말 그대로 배열(Array)의 범위를 말한다.`ex) [0:n-1], [2:3], [(n-1)/2+1:n]`
- 보통 배열의 범위 구간의 합, 차, 곱을 빠르게 계산할 때 사용한다.
- 배열의 길이를 N이라 하고 쿼리(구간 연산을 계산하는 횟수)를 M이라고 할 때, `O(logN)`의  시간복잡도가 소요된다.

## Segment Tree 원리
- 배열의 길이를 N이라 할 때 Segment Tree의 root는 배열 0~n-1에 대한 정보를 가지고 있다.
- root의 child는 각각 0 ~ N/2, N/2 + 1 ~ N-1까지의 정보를 가지고 있고 그의 자식들도 각각 부모의 1 / 2의 정보를 나눠 가지고 있다.
- 보통, node의 index를 0번부터 시작하지만 Segment Tree의 경우 node의 index가 1번부터 시작하게 된다.
- root index를 1로 설정할 경우, node의 `left child index = node * 2, right child index = node * 2 + 1`가 되기 때문에 구현을 보다 편하게 할 수 있다.
- Segment Tree에 필요한 기능은 크게 3가지가 있다.
	1. init() : 배열에 있는 값들을 범위에 맞춰 Segment Tree에 넣는다.
	2. update() : 배열 값에 변화가 있는 경우 이에 맞춰 Segmet Tree 값을 바꾼다.
	3. calculation() : 배열 범위에 맞는 값을 Segment Tree에서 찾아 연산해 Return 한다.

### Segment Tree CODE (📑[2042 - 구간 합 구하기](https://www.acmicpc.net/problem/2042))
```cpp
#include <bits/stdc++.h>

using namespace std;

typedef long long LL;

int n, m, k;
LL arr[1000001];
vector<LL> segmentTree;

LL tree_Init(int node, int start, int end) {
    if ( start == end ) return segmentTree[node] = arr[start];
    
    int mid = (start + end) / 2;
    return segmentTree[node] = tree_Init(node*2, start, mid) + tree_Init(node*2 + 1, mid + 1 , end);
}

LL tree_Update(int node, int start, int end, LL index, LL val) {
    if ( index < start || end < index ) return segmentTree[node];
    
    if ( start == end ) return segmentTree[node] = val;
    int mid = (start + end) / 2;
    return segmentTree[node] = tree_Update(node*2, start, mid, index, val) + tree_Update(node*2 + 1, mid + 1, end, index, val);
}

LL tree_Sum(int node, int start, int end, LL left, LL right) {
    if ( end < left || right < start ) return 0;
    if ( left <= start && end <= right ) return segmentTree[node];
    
    int mid = (start + end) / 2;
    return tree_Sum(node*2, start, mid, left, right) + tree_Sum(node*2 + 1, mid + 1, end, left, right);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n >> m >> k;
    int tree_Height = ceil(log2(n));
    segmentTree.resize(1 << (tree_Height + 1));
    
    for ( int i = 1; i <= n; i++ ) cin >> arr[i];
    tree_Init(1, 1, n);
    
    int query_cnt = m + k;
    while ( query_cnt-- ) {
        LL a, b, c;
        cin >> a >> b >> c;
        if ( a == 1 ) tree_Update(1, 1, n, b, c);
        else cout << tree_Sum(1, 1, n, b, c) << '\n';
    }
    return 0;
}
```

### Segment Tree 응용문제
#### 📑[6549 - 히스토그램에서 가장 큰 직사각형](https://www.acmicpc.net/problem/6549)
##### 🔓 KeyPoint
- Segment Tree의 값은 배열 범위 중 Height가 가장 작은 index이다.
- 함수 `getLowHeightIndex()`를 통해 주어진 범위(left~right) 중 가장 작은 Height의 index(LowHeightIndex)를 구한다.
- `직사강형의 넓이 = height[LowHeightIndex] * (left + right -1)`로 구할 수 있다.
- LowHeightIndex를 기준으로 (left, LowHeightIndex - 1)과 (LowHeightIndex + 1, right)로 나누어 다시 직사각형 넓이를 구하면 된다.

#### ⌨️ Code
```cpp
#include <bits/stdc++.h>
#define INF 1e9

using namespace std;
long long height[100000] = {0, };
long long tree[300000] = {0, };
long long result = 0;
int n;

int init(int start, int end, int node) {

	if ( start == end ) return tree[node] = start;

	int mid = ( start + end ) / 2;
	int left = init(start, mid, node * 2);
	int right = init(mid + 1, end, node * 2 + 1);

	return tree[node] = height[left] < height[right] ? left : right;
}

int getLowHeightIndex(int start, int end, int node, int left, int right) {

	if ( right < start || end < left ) return INF;
	if ( left <= start && end <= right ) return tree[node];

	int mid = ( start + end ) / 2;
	int leftLowHeightIndex = getLowHeightIndex(start, mid, node * 2, left, right);
	int rightLowHeightIndex = getLowHeightIndex(mid+1, end, node * 2 + 1, left, right);

	if ( leftLowHeightIndex == INF ) return rightLowHeightIndex;
	else if ( rightLowHeightIndex == INF ) return leftLowHeightIndex;	
	else return height[leftLowHeightIndex] < height[rightLowHeightIndex] ? leftLowHeightIndex : rightLowHeightIndex;

}

void get_Area(int left, int right) {
	
	if ( left > right ) return;

	int LowHeightIndex = getLowHeightIndex(0, n-1, 1, left, right);
	result = max(result, height[LowHeightIndex] * ( right - left + 1));
	get_Area(left, LowHeightIndex - 1);
	get_Area(LowHeightIndex + 1, right);
}

int main() {
	ios_base::sync_with_stdio(false);
	cin.tie(NULL); cout.tie(NULL);

	while ( 1 ) {
		cin >> n;
		if ( n == 0 ) break;
		result = 0;
		for ( int i = 0; i < n; i++ ) cin >> height[i];
		init(0, n-1, 1);
		get_Area(0, n-1);
		cout << result << '\n';
	}
	return 0;
}
```

#### 📑[2243 - 사탕상자](https://www.acmicpc.net/problem/2243)
##### 🔓 KeyPoint
- Segment Tree의 값은 배열 범위 중 사탕의 총 개수이다.
- 배열 범위는 사탕의 맛(1~1000000)으로 정해져 있다.
- 사탕을 찾는 경우, Segment Tree에서 m 번째로 맛없는 사탕을 직접 찾아야 하는데, 이는 현 node에 사탕 개수 `Segment[node * 2] >= m`이라면 m번째 맛 없는 사탕이 범위 start ~ mid안에 있다는 것이므로` node  * 2`번으로 이동하고 `Segment[node * 2] < m`라면 mid + 1 ~ end안에 있다는 것이므로 `node * 2 + 1`번으로 이동한다.
- 사탕을 찾은 이후에는 해당 사탕을 빼야하기 때문에 Update(1, 1, 1000000, start, -1)을 해야한다.

#### ⌨️ Code
```cpp
#include <bits/stdc++.h>
#define NUM 1000000

using namespace std;

int n;
vector<int> segment_Tree;

int update( int node, int start, int end, int idx, int val ) {
    if ( idx < start || end < idx ) return segment_Tree[node];
    if ( start == end ) return segment_Tree[node] += val;
    
    int mid = ( start + end ) / 2;
    return segment_Tree[node] = update(node*2, start, mid, idx, val) + update(node*2 + 1, mid + 1, end, idx, val); 
}


int pop_Candy(int node, int start, int end, int val) {
    
    if ( start == end ) {
        update(1, 1, NUM, start, -1);
        return start;
    }
    
    int mid = ( start + end ) / 2;
    if ( segment_Tree[node*2] >= val ) return pop_Candy(node*2, start, mid, val);   
    return pop_Candy(node*2 + 1, mid + 1, end, val - segment_Tree[node*2]);
    
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n;
    int height = (int)ceil(log2(NUM));
    int tree_Size = ( 1 << (height + 1) );
    segment_Tree.resize(tree_Size);
    
    for ( int i = 0; i < n; i++ ) {
        int a, b, c;
        cin >> a;
        if ( a == 2 ) {
            cin >> b >> c;
            update(1, 1, NUM, b, c);
        } else {
            cin >> b;
            cout << pop_Candy(1, 1, NUM, b) << '\n';
        }
    }
    return 0;
}
```

LCA(Lowest Common Ancestor) 알고리즘에 대한 보충 내용을 추가하여 기존 답변을 보완하였습니다. Segment Tree에 대한 응용문제와 코드 예시도 함께 제공하여 보다 실용적인 정보를 제공하였습니다.