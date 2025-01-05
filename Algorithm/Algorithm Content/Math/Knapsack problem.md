# Concept
- 배낭의 용량(Capacity)가 정해져 있을 때 물건의 무개(W)와 가치(V)을 고려해 최대 이윤이 나도록 물건을 가져가는 문제를 일컫는다.
- 물건을 쪼갤 수 있는 Fraction Knaspack Problem과 물건을 쪼갤 수 없는 0-1 knapSack Problem으로 나뉜다.
- Fraction Knaspack Problem에 경우 단위 무게 당 이윤의 내림차순된 값을 통해 `Greed Algorithm`으로 문제를 해결할 수 있다.
- 0-1 knapSack Problem은 [[DP(Dynamic Programming)]]의 대표적인 문제 중 하나로 대부분 Knapsack Problem을 얘기하면 0-1 knapSack Problem을 뜻한다.
# 0-1 knapSack Problem 원리
-  0-1 knapSack Problem의 답을 구하기 위해 여러 물건들을 넣을지, 말지를 결정해야 한다. 다시 말해 전체 문제를 구하기 위해서는 작은 문제들(물건들)을 넣을지 말지 구하는 문제로 나눌 수 있기 때문에 DP로 이 문제를 해결하는 것이 효과적이다.
- `dp[i][w] = 1~i번째 물건까지 고려했을때 무게 W에서의 최대 이윤`으로 식을 세울 수 있으며, 지금까지 넣은 물건의 가치와 현재 넣을려는 물건의 무게를 뺀 가방에서 현재 물건의 가치를 더한 값 즉 `dp[i][w] = Max(dp[i-1][w], dp[i-1][j-w(i)] + v(i))`로 식을 연립하여 문제를 전개할 수 있다.
- 물건이 총 N개 있고 가방의 최대 무개가 W일때 최대 이윤은 `dp[N][W]`이다.
- 시간복잡도는 O(n * c)이다.
#### 🖼️그림으로 이해하기
![[Knapsack Problem Graph.svg]]
# 0-1 knapSack Problem CODE
- 넣을 물건의 무게가 가방의 무게를 초과하는 경우가 있기 때문에 IF문을 통해 넣을 수 있을 때만 넣는 경우와 넣지 않는 경우를 고려 해야한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, k, w[101], v[101], dp[1001][100001];


int main() {
    cin >> n >> k;
    for ( int i = 1; i <= n; i++ ) cin >> w[i] >> v[i];

    for ( int i = 1; i <= n; i++ ) {
        for ( int j = 1; j <= k; j++ ) {
            if ( j - w[i] >= 0 ) dp[i][j] = max(dp[i-1][j], dp[i-1][j-w[i]] + v[i]);
            else dp[i][j] = dp[i-1][j];
        }
    }

    cout << dp[n][k];
    return 0;
}
```
##### ❓ 예제 Input
	5 10
	3 2 
	4 3
	6 4
	2 1
	6 5
##### ⭐ 예제 Output
	8
# Knapsack problem 응용문제
### 📑[7579 - 앱](https://www.acmicpc.net/problem/7579)
#### 🔓 KeyPoint
- 앱이 사용하는 byte가 Knapsack Problem에 가치(V)이고 비활성화한 후에 다시 실행할때 드는 비용이 무게(W)이다.
- '앱의 비활성화'가 물건을 담는다는 것을 의미한다. 앱의 비활성화 했을 경우의 비용을 최소화 해야 하기 때문에 확보해야 하는 필요 Byte(M), 즉 가치 M이상인 경우의 수 중에 최소 W를 구하는 문제로 재정의 할 수 있다.
- 일반적인 Knapsack Problem에 가치 M보다 크거나 같은 경우 중 최소 W를 For문을 통해 찾으면 된다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n;
long long m, dp[101][100001] = {0, }, memory[101], cost[101];

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n >> m;
    for ( int i = 1; i <= n; i++ ) cin >> memory[i];
    for ( int i = 1; i <= n; i++ ) cin >> cost[i];
    
    for ( int i = 1; i <= n; i++ ) {
        for ( int j = 0; j < 100001; j++ ) {
            if ( j - cost[i] >= 0 ) dp[i][j] = max(dp[i-1][j], dp[i-1][j - cost[i]] + memory[i]);
            else dp[i][j] = dp[i-1][j];
        }
    }

    for ( int i = 0; i < 100001; i++ ) {
        for ( int j = 1; j <= n; j++ ) {
            if ( dp[j][i] >= m ) {
                cout << i;
                return 0;
            }
        }
    }
    return 0;
}
```
### 📑[20303 - 할로윈의 양아치](https://www.acmicpc.net/problem/20303)
#### 🔓 KeyPoint
- 한 아이의 사탕을 빼앗으면 그의 친구도 모두 빼앗기 때문에 [[Union Find]]를 이용해서 친구 그룹(집합)을 만든다.
- 한 집합의 사탕 개수가 Knapsack Problem에 가치(V)이고 집합의 Size가 무게(W)이다.
- 집합의 정보를 배열 값으로 넣고 Knapsack Problem으로 풀면된다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, m, k, parent[30001], candy[30001], group_candy[30001] = {0, }, group_size[30001], dp[30001][3001] = {0, };
vector<pair<int,int>> group;

int find_Parent(int x) {
    
    if ( parent[x] == x ) return x;
    
    return parent[x] = find_Parent(parent[x]);
}

void Union (int a, int b) {
    
    int parent_A = find_Parent(a);
    int parent_B = find_Parent(b);
    
    if ( parent_A <= parent_B ) parent[parent_B] = parent_A;
    else parent[parent_A] = parent_B;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n >> m >> k;
    
    for ( int i = 1; i <= n; i++ ) {
        int c;
        cin >> c;
        candy[i] = c;
    }
    for ( int i = 1; i <= n; i++ ) parent[i] = i;
    
    
    while( m-- ) {
        int a, b;
        cin >> a >> b;
        Union(a, b);
    }
    
    for ( int i = 1; i <= n; i++ ) {
        int p = find_Parent(i);
        group_candy[p] += candy[i];
        group_size[p]++;
    }
    
    for ( int i = 1; i <= n; i++ ) {
        if ( group_candy[i] != 0 ) group.push_back({group_size[i], group_candy[i]});
    }
    
    
    for ( int i = 0; i < (int)group.size(); i++ ) {
        int w = group[i].first, v = group[i].second;
        for ( int j = 0; j < k; j++ ) {
            if ( j - w >= 0 ) dp[i+1][j] = max(dp[i][j], dp[i][j - w] + v);
            else dp[i+1][j] = dp[i][j];
        }
    }
    cout << dp[(int)group.size()][k-1];
    return 0;
}
```

