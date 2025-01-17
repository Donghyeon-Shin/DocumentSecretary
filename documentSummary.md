컨셉: 
- Fenwick Tree는 Segment Tree의 변형 트리로, 구간의 합을 빠르게 구할 수 있는 자료구조이다. 
- 시간복잡도는 Segment Tree와 같은 O(logN)이지만 공간복잡도는 O(n)으로 Segment Tree보다 더 적다.
- Fenwick Tree는 홀수 인덱스만 표기하며, BIT 연산을 통해 0이 아닌 최하위 비트를 구함으로써 구간의 합을 구한다.

Fenwick Tree 원리:
- Fenwick Tree는 Segment Tree에서 홀수 인덱스만 표기하며, BIT 연산을 통해 0이 아닌 최하위 비트를 구함으로써 구간의 합을 구한다.
- 특정 비트(I)를 통해 최하위 비트를 구하는 공식은 i & -i (-i = ~i + 1)이다.
- Fenwick Tree에 필요한 기능은 sum(idx)와 update(idx, val)이다.
- 특정 비트(i)에 최하위 비트가 0이 되기 전까지 빼면 구간의 합을 구할 수 있고, 특정 비트(i)에 최하위 비트가 특정 값(m) 될 때까지 더하면 구간을 업데이트할 수 있다.
- Range Update를 위해서는 update(l,k)와 update(r+1, -k)를 사용한다.

Fenwick Tree 코드:
- Fenwick Tree를 구현하는 코드는 BIT 연산만 이해한다면 큰 어려움은 없다.
- 부분 합과 구간 합을 구별하여 구현하여야 한다.
- Segment Tree보다 속도 측면에서 빠르지만 응용력이 떨어져 많은 문제에서 사용되진 않는다.

응용문제:
- Fenwick Tree를 응용한 문제로 '8217 - 유성'과 '15957 - 음악추천' 문제가 소개되었다.
- '8217 - 유성' 문제는 PBS(Parallel Binary Search)에 Fenwick Tree을 응용한 문제로, Lazy Segment Tree을 사용하면 시간 초과가 발생하지만 Fenwick Tree를 사용하면 해결할 수 있다.
- '15957 - 음악추천' 문제는 PBS(Parallel Binary Search)에서 Fenwick Tree를 응용하는 문제로, ETT(Euler Tour Technique)을 적용하여 해결할 수 있다.

위의 내용은 Fenwick Tree에 대한 개념과 원리, 코드 구현, 그리고 응용문제에 대한 설명이다. Fenwick Tree를 이해하고 활용하기 위해서는 이러한 내용을 숙지하는 것이 중요하다.