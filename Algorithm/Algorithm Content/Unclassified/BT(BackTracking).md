# Concept
- 해를 찾아가는 과정에서 Recursion과 [[DFS(Depth-First Search)]]을 사용하여 여러 경로를 탐색하면서 해당 경로가 안되는 경우 그 경로를 제거해 올바른 경로를 찾는 알고리즘을 말한다.
- 여러 경로를 만들고 그 과정에서 올바르지 않는 경로를 제거하는 것을 `가지치기(pruning)`라고 하고 올바른 경로가 될 가능성이 있는 경로를 `유망하다(promising)`고 말한다.
- 일반 [[DFS(Depth-First Search)]]의 경우 탐색할 수 있는 모든 깊이/Node를 탐색하는 방법이지만 BT는 모든 경로 중 특정 조건에 맞는 경로를 탐색한다는 것에 차이가 있다.
- BT에서 중요한 것은 `가지치기`이다.  가지치기가 시간복잡도를 결정하기 때문인데, 가지치기가 효율적으로 진행되지 않으면 O(N!)이나 무한 Loop가 생길 수도 있다.
# BT 원리(📑[15649 - N과 M(1)](https://www.acmicpc.net/problem/15649))
- BT는 기본적인 Recursion의 형태를 가지고 있다. 즉, call과 return condition(종료조건)를 가지고 있다.
- call의 조건은 `가지치기` 조건이며 종료조건이 되면 올바른 경로에 도달했다는 뜻이다
- 문제에 따라 `가지치기` 조건과 종료조건이 다르기 때문에 이를 고려하여 구현하여야 한다.
- `N과 M(1)` 문제의 `가지치기` 조건은 중복된 방문이며 종료조건은 수열의 개수(m)이 채워진 경우이다.
- 중복된 방문을 채크하기 위해 따로 수에 대한 방문 배열을 만든다.
#### 🖼️그림으로 이해하기
![[BT Graph.svg]]
# BT CODE
- DFS에서 중복 탐색을 방지하기 위해 `visited` Array를 사용한다. 다음 노드(next) 탐색에서 같은 곳은 탐색하지 않게 `visited[next] = true`한 뒤 탐색하고 해당 경로의 탐색을 모두 진행했다면 다시 `visited[next] = false`로 해 다른 경로에 next를 탐색할 수 있게 설정해 주어야 한다.
- Recursion을 사용할 때는 종료 조건을 올바르게 설정해주어야 한다. BT에서 종료조건은 보통 모든 조건을 만족한 올바른 경로가 있을 때이다.
- 해당 문제에서는 올바른 경로가 되면 바로 결과를 출력하도록 하였다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, m, arr[9];
bool visited[9];

void bt(int len) {
    if ( len == m ) {
        for ( int i = 1; i <= m; i++ ) cout << arr[i] << ' ';
        cout << '\n';
        return;
    }

    for ( int i = 1; i <= n; i++ ) {
        if ( !visited[i] ) {
            visited[i] = true;
            arr[len+1] = i;
            bt(len+1);
            visited[i] = false;
        }
    }
}

int main() {
    cin >> n >> m;
    memset(visited, false, sizeof(bool)*9);
    bt(0);
    return 0;
}
```
##### ❓ 예제 Input
	4 3
##### ⭐ 예제 Output
	1 2 3
	1 2 4
	1 3 2
	1 3 4
	1 4 2
	1 4 3
	2 1 3
	2 1 4
	2 3 1
	2 3 4
	2 4 1
	2 4 3
	3 1 2
	3 1 4
	3 2 1
	3 2 4
	3 4 1
	3 4 2
	4 1 2
	4 1 3
	4 2 1
	4 2 3
	4 3 1
	4 3 2
# BT 응용문제
### 📑[9663 - N-Queen](https://www.acmicpc.net/problem/9663)
#### 🔓 KeyPoint
- 2D-Array로 할 경우 가지치기 조건을 연산하는데 O(n^2)이 걸리기 때문에 시간안에 이 문제를 해결할 수 없다.
- Queen의 경우 한 줄에 하나의 말 밖에 놓을 수 없기 때문에 이를 이용해서 `Array[row] = column` 즉,  Array에 Column 값을 넣어 같은 row, column에 Queen을 놓을 수 없게 한다.
- 2차원 배열에서 같은 대각선에 있을 때 row, column의 식은 `row1 - row2 == abs(column1 - column2)`식으로 표현 할 수 있다. 따라서 이 또한 고려하면 1D-Array 만으로도 `가지치기` 조건을 구할 수 있다.
- 위 식들을 사용하면 O(n)만큼 가지치기 연산을 수행 할 수 있다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, queen[15], cnt = 0;
bool check;

void bt(int row) {
    if ( row == n ) {
        cnt++;
        return;
    }

    for ( int i = 0; i < n; i++ ) {
        queen[row] = i;
        check = true;
        for ( int j = 0; j < row; j++ ) {
            if ( queen[j] == queen[row] || row - j == abs(queen[row] - queen[j]) ) check = false;
        }

        if ( check ) bt(row+1);
    }
}

int main() {
    cin >> n;
    bt(0);
    cout << cnt;
    return 0;
}
```
### 📑[1799 - 비숍](https://www.acmicpc.net/problem/1799)
#### 🔓 KeyPoint
- 비숍은 Queen과 다르게 대각선 지역으로만 이동할 수 있다. 이는 다시 말해, 채스 판의 흰색과 검은 색 부분에 있는 비숍들은 서로 영향을 받지 않는다는 뜻이다.
- BT의 시작을 흰색 부분과 검은색 부분으로 총 두 번 시행하며, Recursion에서 다음 Node로 이동할 때도 서로 영향을 받는 Node로만 이동하도록 설정하여야 한다.
- 또한 배치할 수 있는 가장 많은 비숍의 개수를 구하는 것이기 때문에 종료 조건에서 가능한 모든 경로 중 최대 값을 구하도록 해야한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, result = 0, answer = 0;
bool graph[10][10], right_cross[20] = {0, }, left_cross[20] = {0, };

void bt(int row, int col, int cnt) {
    
    if ( row >= n ) {
        col++;
        if ( row % 2 == 0 ) row = 1;
        else row = 0;
    }
    
    if ( col >= n ) {
        col = 0;
        result = max(cnt, result);
        return;
    }
    
    if ( graph[row][col] && !right_cross[row+col] && !left_cross[col-row+(n-1)] ) {
        right_cross[row+col] = 1;
        left_cross[col-row+(n-1)] = 1;
        bt(row+2, col, cnt+1);
        right_cross[row+col] = 0;
        left_cross[col-row+(n-1)] = 0;            
    }
    bt(row+2, col, cnt);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n;
    for ( int i = 0; i < n; i++ ) {
        for ( int j = 0; j < n; j++ ) cin >> graph[i][j];
    }
    
    bt(0, 0, 0);
    answer += result;
    result = 0;
    bt(1, 0, 0);
    answer += result;
    cout << answer;
    return 0;
}
```
