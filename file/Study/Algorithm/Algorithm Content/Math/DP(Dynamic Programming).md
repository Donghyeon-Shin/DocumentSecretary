# Concept
- 하나의 큰 문제를 여러 개의 작은 문제로 나누어서 그 결과를 합쳐 큰 문제를 해결하는 알고리즘 방법이다. 동적 계획법이라고도 한다.
- DP는 정형화 되어 있는 코드가 존재하지 않고 특정 문제를 풀 때 아이디어의 개념으로써 활용된다.
- 보통 하나의 함수로 나누어지는 경우 DP를 사용해 해결 할 수 있다.
- 재귀방식(Navie Recursion)과 아이디어가 유사하지만 큰 문제를 작은 문제로 나누어지면서 같은 계산이 반복된다면 DP를 아니라면 Recursion을 사용한다.
- 수학적으로 일반항을 구하는 과정을 생각하면 된다.
# Dynamic Programming 원리
- DP는 큰 문제를 반복되는 작은 문제로 나누어 과정과 이를 합치는 과정이 필요하다.
- 보통 Array를 통해 작은 문제의 답을 저장하고 나중에 큰 문제를 해결함에 있어 저장했었던 Array를 조합하여 답을 도출한다.
- DP는 문제를 해결하는 방법론이기 때문에 문제에 따라 로직이 다르기 때문에 항상 문제를 볼 때 DP로 해결할 수 있는지 없는지를 판단하는게 중요하다.
#### 🖼️그림으로 이해하기
![[DP Graph.svg]]
# Dynamic Programming CODE
- DP 문제 중 가장 대표적인 Fibonacci Number를 구하는 문제이다.
- F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2)
- 큰 문제 - F(8), 작은 문제들 F(1)~F(7)
- F(7) = F(6) + F(5) / F(6)  = F(5) + F(4) 등등 작은 문제들을 합쳐 큰 문제의 답을 구하는 과정이 핗필요하다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, arr[100];

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n;
    arr[0] = 0;
    arr[1] = 1;
    
    for ( int i = 2; i <= n; i++ ) arr[i] = arr[i-1] + arr[i-2];
    for ( int i = 0; i <= n; i++ ) cout << arr[i] << ' ';
    return 0;
}
```
##### ❓ 예제 Input
	8
##### ⭐ 예제 Output
	0 1 1 2 3 5 8 13 21

# Dynamic Programming 응용문제
### 📑[14002 - 가장 긴 증가하는 부분 수열 4](https://www.acmicpc.net/problem/14002)
#### 🔓 KeyPoint
- 가장 긴 증가하는 부분 수열(LIS)는 대표적인 DP문제이다.
- dp[n] = 1~n번째까지 가장 긴 부분 수열의 길이이다.
- 2중 For문으로 dp[n] = max(dp[1 ~ n-1]) + 1로 구한다.
- 수열의 값을 출력할 때는 역으로 dp값이 큰 순서대로 넣은 후 다시 역으로 출력하면 된다. 
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, maximum = 0, len = 0, position, arr[1001], dp[1001];
vector<int> result;

int main() {
    cin >> n;
    for ( int i = 1; i <= n; i++ ) {cin >> arr[i]; dp[i] = 1;}

    for ( int i = 1; i <= n; i++ ) {
        len = 0;
        for ( int j = 1; j < i; j++ ) {
            if ( arr[i] > arr[j] ) len = max(dp[j], len);
        }
        len++;
        dp[i] = len;
        if ( maximum < len ) {
            maximum = len;
            position = i;
        }
    }

    for ( int i = position; i >= 1; i-- ) {
        if ( dp[i] == maximum ) {
            result.push_back(arr[i]);
            maximum--;
        }
    }
    vector<int>::iterator iter;
    cout << result.size() << '\n';
    for ( iter = result.end() - 1; iter >= result.begin(); iter-- ) cout << *iter << ' ';
    return 0;
}
```
### 📑[1006 - 습격자 초라기](https://www.acmicpc.net/problem/1006)
#### 🔓 KeyPoint
- 단순 2차원 배열이 아닌 원형으로 된 배열을 다루는 문제이다.
- `dp[i][j]` = i번째 열에서 j번째 경우일때 최소 배치 수를 의미한다.
- 초소의 모양은 3가지가 나올 수 있고 한 초소가 인접한 장소도 커버 가능하기 때문에 이를 고려해 여러 경우로 나누어 코드를 구현하여야 한다.
- 원형이기 때문에 마지막 열과 처음 열이 연결되어 있음을 인지하고 이를 고려해 마지막과 처음을 연결하여 한 초소를 짓는 경우도 따로 구해 최소값을 구해야 한다.
![[Choragi the Raider.svg]]
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int t, n, w;
int arr[10001][3] = {0, }, dp[10001][3] = {0, };

void Permeate(int start) {

    for ( int i = start; i <= n; i++ ) {
        dp[i][0] = min(dp[i-1][1] + 1, dp[i-1][2] + 1);
        if ( arr[i][1] + arr[i][2] <= w ) dp[i][0] = min(dp[i][0], dp[i-1][0] + 1);
        if ( i > 1 && arr[i-1][1] + arr[i][1] <= w && arr[i-1][2] + arr[i][2] <= w ) dp[i][0] = min(dp[i][0], dp[i-2][0] + 2);
        dp[i][1] = dp[i][0] + 1;
        if ( arr[i][1] + arr[i+1][1] <= w ) dp[i][1] = min(dp[i][1], dp[i-1][2] + 1);
        dp[i][2] = dp[i][0] + 1;
        if ( arr[i][2] + arr[i+1][2] <= w ) dp[i][2] = min(dp[i][2], dp[i-1][1] + 1);
    }
};


int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> t;
    while ( t-- ) {
        cin >> n >> w;
    
        for ( int i = 1; i <= 2; i++ ) {
            for ( int j = 1; j <= n; j++ ) cin >> arr[j][i];
        }
        
        dp[0][0] = 0;
        dp[0][1] = 1;
        dp[0][2] = 1;
        Permeate(1);
        
        int result = dp[n][0];
        
        if ( n > 1 ) {
            if ( arr[1][1] + arr[n][1] <= w ) {
                dp[1][0] = 1;
                dp[1][1] = 2;
                if ( arr[1][2] + arr[2][2] <= w ) dp[1][2] = 1;
                else dp[1][2] = 2;
                
                Permeate(2);
                result = min(result, dp[n-1][2] + 1);
            }
            
            if ( arr[1][2] + arr[n][2] <= w ) {
                dp[1][0] = 1;
                dp[1][2] = 2;
                if ( arr[1][1] + arr[2][1] <= w ) dp[1][1] = 1;
                else dp[1][1] = 2;
                Permeate(2);
                result = min(result, dp[n-1][1] + 1);            
            }
            
            if ( arr[1][1] + arr[n][1] <= w && arr[1][2] + arr[n][2] <= w ) {
                dp[1][0] = 0;
                dp[1][1] = 1;
                dp[1][2] = 1;
                Permeate(2);
                result = min(result, dp[n-1][0] + 2);
            }           
        }
        cout << result << '\n';
    }
    return 0;
}
```
