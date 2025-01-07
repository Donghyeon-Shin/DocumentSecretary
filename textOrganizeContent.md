Main file
- file name: Fenwick Tree.md
- concept: 
  - `Binary Indexed Tree(BIT)`로 알려져 있으며, 후계 구간의 합을 효율적으로 계산하는 자료구조이다.
  - 시간복잡도는 `O(logN)`이고 공간복잡도는 `O(N)`으로 Segment Tree보다 적은 메모리를 소모한다.
- principle: 
  - Fenwick Tree는 최하위 비트를 이용하여 구간의 합을 구한다. 특정 비트(i)에 대해 최하위 비트를 구하는 것은 `i & -i`로 수행한다.
  - `sum(idx)`와 `update(idx, val)`의 두 가지 주요 연산을 지원한다.
- example: 
  ```cpp
  // Fenwick Tree 구현 예시 코드
  #include <bits/stdc++.h>
  using namespace std;
  int n, q, fenwickTree[100001];
  
  void fenwickTree_Update(int idx, int val) {
      while (idx <= n) {
          fenwickTree[idx] += val;
          idx += (idx & -idx);
      }
  }
  
  int fenwickTree_Sum(int idx) {
      int result = 0;
      while (idx > 0) {
          result += fenwickTree[idx];
          idx -= (idx & -idx);
      }
      return result;
  }
  ```

Related files
file 1
- file name: Segment Tree.md
- concept: 
  - Node 값을 가진 이진 Tree로 배열의 범위를 처리하며, 구간의 합, 차, 곱을 계산하는 자료구조이다.
  - 시간복잡도는 `O(logN)`이다.
- Content associated with the main file: 
  - Segment Tree는 root에서 시작하여 각 노드가 배열 범위의 정보를 보유한다.
  - 필요한 주요 기능은 `init()`, `update()`, `calculation()`이 있다.
- example:
  ```cpp
  // Segment Tree 구현 예시 코드
  #include <bits/stdc++.h>
  using namespace std;
  typedef long long LL;
  
  int n, m, k;
  LL arr[1000001];
  vector<LL> segmentTree;
  
  LL tree_Init(int node, int start, int end) {
      if (start == end) return segmentTree[node] = arr[start];
      int mid = (start + end) / 2;
      return segmentTree[node] = tree_Init(node * 2, start, mid) + tree_Init(node * 2 + 1, mid + 1, end);
  }
  ```

file 2
- file name: Lazy Segment Tree.md
- concept:
  - Segment Tree의 구간 변화 처리를 미루는 방법으로, Lazy에 의해 업데이트를 지연시킨다.
  - 시간복잡도는 `O(MlogN)`으로, 범위 업데이트를 효율적으로 처리 가능하다.
- Content associated with the main file:
  - `update()`와 `calcultion()`에서 Lazy 동작을 통해 리프노드가 아닐 경우 업데이트를 수행하지 않을 수 있다.
- example:
  ```cpp
  // Lazy Segment Tree 구현 예시 코드
  #include <bits/stdc++.h>
  using namespace std;
  
  int n, m, k;
  long long arr[1000001];
  vector<long long> segment_Tree, lazy;
  
  long long init(int node, int start, int end) {
      if (start == end) return segment_Tree[node] = arr[start];
      int mid = (start + end) / 2;
      return segment_Tree[node] = init(node*2, start, mid) + init(node*2 + 1, mid + 1, end);
  }
  ```

file 3
- file name: ETT(Euler Tour Technique).md
- concept:
  - 트리 기반 문제에서 노드를 선형 배열로 변환하여 구간 쿼리를 지원하는 기법이다.
  - 시간 및 공간 효율성이 높고 Lazy Segment Tree와 결합하여 사용할 수 있다.
- Content associated with the main file:
  - 주로 이분 탐색과 조합되어 사용하며 Tree의 높이를 줄이는 방식으로 노드를 관리한다.
- example:
  ```cpp
  // ETT 기본 구조 예시 코드
  #include <bits/stdc++.h>
  using namespace std;
  
  void eulerTour(int node, vector<int>& eulerArr) {
      // 방문한 노드를 eulerArr에 추가
      eulerArr.push_back(node);
      // 각 자식 노드에 대해 재귀 호출
      for (auto child : tree[node]) {
          eulerTour(child, eulerArr);
      }
  }
  ```