HLD(Heavy-Light Decomposition)의 정의는 트리 구조에서 간선을 'Heavy Edge'와 'Light Edge'로 나누어 구분하는 알고리즘입니다. 이 알고리즘은 부모 노드(`u`)와 자식 노드(`v`) 간의 간선(`e`)이 있을 때, `v`의 서브 트리 크기가 `u`의 서브 트리 크기의 1/2 이상일 경우 해당 간선을 **Heavy Edge**로 정의하며, 이 외의 경우는 모두 **Light Edge**로 간주합니다. 

HLD의 주요 원리는 다음과 같습니다:
1. **Heavy Edge와 Light Edge 구분**: DFS(Depth-First Search)를 사용하여 각 노드의 서브 트리 크기를 계산하고, 이를 바탕으로 Heavy Edge와 Light Edge를 판별합니다.
2. **구간 계산**: 나누어진 Edge를 기반으로 구간 계산을 진행하며, 이를 위해 Segment Tree를 사용합니다.

HLD를 통해 특정 노드 `u`와 `v`를 연결하는 Light Edge는 최대 **2 * logN**개가 될 수 있으며, Light Edge를 타고 올라갈 경우 서브 트리의 크기가 2배 이상 증가하게 됩니다. 이러한 구조를 통해 HLD는 효율적으로 트리의 간선을 관리하고, 구간 쿼리를 수행할 수 있게 됩니다. 

HLD의 구현은 복잡하지만, DFS, ETT(Euler Tour Technique), Segment Tree와 같은 기법을 활용하여 효율적인 트리 쿼리 처리를 가능하게 합니다.