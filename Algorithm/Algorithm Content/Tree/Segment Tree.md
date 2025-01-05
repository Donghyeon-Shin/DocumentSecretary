# Concept
- Node 값에 배열의 범위를 가진 이진 Tree Struct의 일종이다.
- `배열의 범위`는 말 그대로 배열(Array)의 범위를 말한다.`ex) [0:n-1], [2:3], [(n-1)/2+1:n]`
- 보통 배열의 범위 구간의 합, 차, 곱을 빠르게 계산할 때 사용한다.
- 배열의 길이를 N이라 하고 쿼리(구간 연산을 계산하는 횟수)를 M이라고 할 때, `O(logN)`의  시간복잡도가 소요된다.
# Segment Tree 원리
- 배열의 길이를 N이라 할 때 Segment Tree의 root는 배열 0~n-1에 대한 정보를 가지고 있다.
- root의 child는 각각 0 ~ N/2, N/2 + 1 ~ N-1까지의 정보를 가지고 있고 그의 자식들도 각각 부모의 1 / 2의 정보를 나눠 가지고 있다.
- 보통, node의 index를 0번부터 시작하지만 Segment Tree의 경우 node의 index가 1번부터 시작하게 된다.
- root index를 1로 설정할 경우, node의 `left child index = node * 2, right child index = node * 2 + 1`가 되기 때문에 구현을 보다 편하게 할 수 있다.
- Segment Tree에 필요한 기능은 크게 3가지가 있다.
	1. init() : 배열에 있는 값들을 범위에 맞춰 Segment Tree에 넣는다.
	2. update() : 배열 값에 변화가 있는 경우 이에 맞춰 Segmet Tree 값을 바꾼다.
	3. calculation() : 배열 범위에 맞는 값을 Segment Tree에서 찾아 연산해 Return 한다.
#### 🖼️그림으로 이해하기
![[Segment Tree Graph.svg]]
# Segment Tree CODE (📑[2042 - 구간 합 구하기](https://www.acmicpc.net/problem/2042))
- Tree Height는 `log2(n)`이고 Tree Size의 경우 `(Tree Height+1) ^ 2`이다.
- Parameter `start, end`는 각각 배열 범위의 시작, 끝을 의미한다.
- `start == end`는 leaf Node를 의미하고` 해당 범위의 값 = array[start]`이다.
- root 노드에서 시작해 다음 두 child 범위는 `child_One : start ~ (start+end) / 2, child_Two : (start+end) / 2 + 1 ~ end`이다.
- 배열에 범위(left~right)에 맞는 Segment Tree Node는 `left <= start && end <= right `이다,
- 만약 `end < left || right < start`라면 해당 Node가 범위에 포함되지 않는 것이기 때문에 return 0을 한다.
#### ⌨️ Code
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
##### ❓ 예제 Input
	12 3 3
	1 2 3 4 5 6 7 8 9 10 11 12
	2 1 12
	1 7 100
	1 4 12
	2 4 7
	1 1 12
	2 1 12 
##### ⭐ 예제 Output
	78
	123
	190
# Segment Tree 응용문제
### 📑[6549 - 히스토그램에서 가장 큰 직사각형](https://www.acmicpc.net/problem/6549)
#### 🔓 KeyPoint
- Segment Tree의 값은 배열 범위 중 Height가 가장 작은 index이다.
- 함수 `getLowHeightIndex()`를 통해 주어진 범위(left~right) 중 가장 작은 Height의 index(LowHeightIndex)를 구한다.
- `직사각형의 넓이 = height[LowHeightIndex] * (left + right -1)`로 구할 수 있다.
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
### 📑[2243 - 사탕상자](https://www.acmicpc.net/problem/2243)
#### 🔓 KeyPoint
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
