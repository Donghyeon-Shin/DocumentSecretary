컨셉: 
- Fenwick Tree는 Segment Tree의 변형 트리로, 구간의 합을 빠르게 구할 수 있는 자료구조이다. 
- Segment Tree와 시간복잡도는 같지만, 공간복잡도는 더 적다.

Fenwick Tree 원리:
- Fenwick Tree는 Segment Tree에서 홀수 인덱스만 표기하며, BIT 연산을 통해 0이 아닌 최하위 비트를 구하여 구간의 합을 구한다.
- 특정 비트(I)를 통해 최하위 비트를 구하는 공식은 i & -i (-i = ~i + 1)이다.
- 구간의 합을 구하기 위해 sum(idx) 함수를 사용하고, update(idx, val) 함수를 사용하여 배열의 idx번째와 해당 idx에 해당되는 모든 구간 값을 업데이트 한다.
- Range Update를 위해 update(l,k)와 update(r+1, -k) 함수를 사용한다.

Fenwick Tree 코드:
- Fenwick Tree를 구현하는 코드는 BIT 연산만 이해한다면 큰 어려움은 없다.
- 부분 합과 구간 합을 잘 구별하여 구현하여야 한다.
- Segment Tree보다 속도 측면에서 빠르지만 응용력이 떨어져 많은 문제에서 사용되진 않는다.

Fenwick Tree 응용문제:
- Fenwick Tree를 응용하여 해결하는 문제들이 존재한다.
- 예시로는 '8217 - 유성'과 '15957 - 음악추천' 문제가 있다.
- '8217 - 유성' 문제는 PBS(Parallel Binary Search)에 Fenwick Tree을 응용한 문제이며, '15957 - 음악추천' 문제는 PBS에서 Fenwick Tree를 응용하는 문제이다.

이러한 Fenwick Tree를 이해하고 활용하여 응용문제를 해결할 수 있다.