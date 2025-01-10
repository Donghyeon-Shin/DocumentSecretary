Main file
- file name: Fenwick Tree.md
- concept: Binary Indexed Tree(BIT)로 구간의 합을 빠르게 구할 수 있는 자료구조로, 공간복잡도가 Segment Tree보다 적다.
- principle: 특정 구간의 합이나 포인트 쿼리를 빠르게 계산할 수 있도록 구간의 최하위 비트만을 활용한 트리의 구조를 가진다.
- example: 구간합, 포인트 쿼리 등을 이용한 Fenwick Tree 구조, 예제 코드와 함께 제공하며, 다양한 활용 코드 포함.

Related files
file 1
- file name: Segment Tree.md
- concept: 이진 트리 구조로 배열의 특정 범위에 대한 정보를 저장하여 구간의 합, 차 등을 빠르게 계산하는데 사용된다.
- content associated with the main file: Segment Tree와 비교하여 Fenwick Tree의 구조적 차이를 설명하고, 각각의 시간, 공간 복잡도 측면에서의 장단점을 분석.

file 2
- file name: Lazy Segment Tree.md
- concept: Segment Tree의 개선된 버전으로, 게으른 업데이트를 적용하여 필요한 시점에만 구간 갱신을 수행하는 방식이다.
- content associated with the main file: Fenwick Tree와 마찬가지로 구간에 대한 효율적 업데이트 방식을 제공하나, 게으른 평가 기법을 활용하여 대량의 데이터 업데이트 시 효율적이다.

file 3
- file name: MST(Minimum Spanning Tree).md
- concept: 그래프에서 모든 노드를 연결하면서, 간선의 총 비용이 최소가 되는 신장 트리를 찾는 알고리즘.
- content associated with the main file: Fenwick Tree는 특정 연결성 및 크기를 가지는 트리로써 MST 알고리즘의 그래프 연산 형태와 응용이 가능.

file 4
- file name: Union Find.md
- concept: Disjoint Set을 표현하는 자료 구조로, 집합간의 합치기 및 포함 여부를 찾는 연산을 효율적으로 지원.
- content associated with the main file: Fenwick Tree와의 직접적 연관보다는 보다 큰 그래프 구조에서의 노드 연결과 집합 연산에서 간접적으로 관련.

file 5
- file name: DP(Dynamic Programming).md
- concept: 동일 문제의 반복을 피하며, 작은 문제의 결과들을 활용해 큰 문제를 해결하는 최적화 기법.
- content associated with the main file: Fenwick Tree도 특정 최적화 문제에서 효율적 해답을 찾을 수 있으나, DP와는 문제 접근 방식에서 근본적 차이 존재.