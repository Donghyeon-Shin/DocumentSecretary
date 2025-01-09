Main file
- file name: HLD(Heavy Light Decomposition).md
- concept: Tree의 Edge를 'Heavy Edge'와 'Light Edge'로 나누어 구분하는 알고리즘이다. 부모 Node와 자식 Node를 잇는 Edge의 크기에 따라 Edge를 분류하여 구간의 Edge를 효율적으로 관리한다.
- principle: Edge를 각각 Heavy Edge와 Light Edge로 나누는 것이며, 이어지는 Heavy Edge를 하나의 그룹으로 보고, 이 그룹의 구간을 정의하여 효율적인 구간 계산을 진행한다.
- example:
  - `O(N)`의 시간복잡도를 가지는 DFS를 이용하여 Edge를 분류
  - ETT(Euler Tour Technique)와 Segment Tree를 이용하여 구간 계산을 빠르게 처리
  - [[13510 - 트리와 쿼리 1]] 문제에서 적용 예시

Related files

file 1
- file name: DFS(Depth-First Search).md
- concept: 노드 탐색 방법 중 하나로, 하나의 Branch씩 탐색하기 때문에 보통 재귀를 이용해 구현된다.
- content associated with the main file: DFS가 HLD의 Heavy Edge와 Light Edge를 나누는 데 사용되며, `O(N)`의 시간복잡도로 Sub Tree 크기를 계산하는 데 핵심적인 역할을 한다.

file 2
- file name: Segment Tree.md
- concept: Node 값에 배열의 범위를 가진 이진 Tree 구조로 주로 배열의 범위 구간의 합, 차, 곱을 계산하는 데 사용된다.
- content associated with the main file: 각 나누어진 Edge들의 구간 계산에 Segment Tree가 사용되며, HLD의 구간 계산 최적화에 중요한 요소로 작용한다.

file 3
- file name: ETT(Euler Tour Technique).md
- concept: 특정 노드의 하위 또는 상위 Node에 대한 쿼리를 처리하기 위해 DFS를 사용하여 Tree의 서브 트리 구간을 List 형태로 변환하는 기법이다.
- content associated with the main file: ETT를 통해 정의된 구간을 바탕으로 HLD의 구현에서 각 Node의 구간을 설정하고, 구간 계산에 ETT로 정의된 값을 사용한다.

file 4
- file name: LCA(Lowest Common Ancestor).md
- concept: 주어진 Tree 안에서 두 노드의 최소 공통 조상을 찾는 알고리즘으로, DP를 이용한 효율적인 탐색이 가능하다.
- content associated with the main file: HLD와 LCA는 서로 다른 문제를 해결하기 위한 알고리즘으로, HLD 구현 시 [[LCA]]를 사용하여 노드의 조상을 찾을 수 있으나, 코드를 복잡하게 만들어 선호하지 않는 방식으로 언급되었다.