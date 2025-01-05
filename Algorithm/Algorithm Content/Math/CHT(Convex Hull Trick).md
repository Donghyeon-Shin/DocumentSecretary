# Concept
- 특정 형태의 점화식을 사용하는 [[DP(Dynamic Programming)]] 문제를 빠르게 계산하는 알고리즘이다.
> 사용 가능한 형태 
> 수열 수열 A<sub>n</sub>  B<sub>n</sub>이 존재하고  j < i 일 때 `DP[i] = min(DP[j] + A[i] * B[j])`을 만족한다.
> 최솟값을 구하는 DP : 수열 B<sub>n</sub>에 대해 B<sub>1</sub> >= B<sub>2</sub> >= B<sub>3</sub> ... >= B<sub>n</sub>을 만족한다. 
> 최댓값을 구하는 DP : 수열 B<sub>n</sub>에 대해 B<sub>1</sub> <= B<sub>2</sub> <= B<sub>3</sub> ... <= B<sub>n</sub>을 만족한다. 
- 이러한 형태에 대해서 `O(nlogn)`의 시간복잡도로 문제를 해결 할 수 있고 수열 A<sub>n</sub>이 A<sub>1</sub> <= A<sub>2</sub> <= A<sub>3</sub> ... <= A<sub>n</sub>을 만족한다면 `O(n)`까지 줄일 수 있다(최솟값 기준).
- 점화식의 형태가 **Convex Hull**을 닮아 Convex Hull Trick이라고 한다. 
# Convex Hull Trick 원리
- `DP[i] = min(DP[j] + A[i] * B[j])`에서 `A[i]`를 x로 놓고 `DP[i]`를 y로 놓게 되면 `y = B[j]x + DP[j]` 같이 1차 함수가 된다.
- B<sub>1</sub> >= B<sub>2</sub> >= B<sub>3</sub> ... >= B<sub>n</sub>을 만족하기 때문에 DP의 모든 1차 함수의 기울기는 점점 감소하는 형태로 나오게 된다.
- DP의 최종 그래프는 모든 1차 함수 중 최소값만 가지는 것이기 때문에 밑에 그림에서 볼 수 있듯이 Convex Hull처럼 나타낼 수 있다. 
![[CHT 그래프 형태.svg]]
- `DP[j]`를 알기 위해서는 1~j-1까지의 모든 DP값을 알아야 하기 때문에 `DP[0]`부터 시작해 Stack을 통해 직선을 순차적으로 만들어야 한다.
- 직선 i번째를 추가할 때는 i-2와 i-1번째 직선의 교점 x(x<sub>q</sub>)과 i-1번째와 i 번째 직선의 교점 x(x<sub>p</sub>)을 비교해 기존 직선을 뺄지 말지 결정 후 추가한다.
> x<sub>p</sub> > x<sub>q</sub> 일 때,
> i-1번째 직선의 범위는 [x<sub>q</sub>,x<sub>p</sub>]이고 i번째 직선의 범위는[x<sub>p</sub>,∞]이다.
> x<sub>p</sub> <= x<sub>q</sub> 일 때,
> i-1번째 직선의 범위는 없기 때문에 i-1번째 직선은 삭제되고 i번째와 i-2번째 직선의 교점 x(x<sub>r</sub>)이라 할 때
> i번째 직선의 범위는  [x<sub>r</sub>,∞]이 된다.

- 이러한 과정을 거쳐 1~n번째 직선을 만들고 삭제하고 이어서 DP 그래프를 만들 수 있다.
- 최종 구하고자 하는 값(x)은 [[Binary Search]]을 통해 해당 위치에 있는 **DP 직선**을 찾고 그 직선에 x값에 대입해 값을 구하면 된다.
#### 🖼️그림으로 이해하기
![[CHT Graph.svg]]

# Convex Hull Trick CODE 📑[13263 - 나무 자르기](https://www.acmicpc.net/problem/13263)
- CHT를 수행하기 위해 일차 방정식 정보를 가진 Struct을 만들어야 한다.
- top : `가장 마지막 직선 Index`을 선언하고 만약 기존 직선을 제거할 때는 기존 위치에 값을 바꾸는 방식으로 진행한다.
- [[Binary Search]]을 이용하여  `A`값의 위치에 있는 직선을 찾고 해당 값을 대입하여 `DP`값을 구하면 된다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, tree_Len[100001], charge_Cost[100001];
long long dp[100001];

struct Linear{
    long long a, b;
    double intersect;
    Linear(long long _a = 0, long long _b = 0, double _intersect = 0) : a(_a), b(_b), intersect(_intersect) {}
};

double calCul_Intersect(Linear &L1, Linear &L2) {
    return (L2.b - L1.b) / (L1.a - L2.a);
}

Linear line[100001];

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    memset(dp, 0, sizeof(dp));
    
    cin >> n;
    for ( int i = 1; i <= n; i++ ) cin >> tree_Len[i];
    for ( int i = 1; i <= n; i++ ) cin >> charge_Cost[i];
    
    int top = 0;
    for ( int i = 2; i <= n; i++ ) {
        Linear nextLine = Linear(charge_Cost[i-1], dp[i-1]);
        while ( top > 0 ) {
            nextLine.intersect = calCul_Intersect(line[top-1], nextLine);
            if ( line[top-1].intersect < nextLine.intersect ) break;
            top--;
        }
        line[top] = nextLine;
        int target_idx = top;
        
        long long target_X = tree_Len[i];
        if ( target_X < line[top].intersect ) {
            int low = 0, high = top;
            while ( low + 1 < high ) {
                int mid = (low + high) / 2;
                if ( target_X < line[mid].intersect ) high = mid;
                else low = mid;
            }
            target_idx = low;
        }
        top++;
        dp[i] = line[target_idx].a * target_X + line[target_idx].b;
    }
    
    cout << dp[n];
    return 0;
}
```
##### ❓ 예제 Input
	5
	1 2 3 10 20
	5 4 3 2 0
##### ⭐ 예제 Output
	75
# Convex Hull Trick 응용문제
### 📑[4008 - 특공대](https://www.acmicpc.net/problem/4008)
#### 🔓 KeyPoint
- DP 식을 구현하는 과정에서 CHT가 떠오르는 것이 핵심이다.
- `dp[i] = i번째 병사까지 조정했을 때의 최대 전투력`, `S[i] = 1~i까지의 누적합`로 표기할 때 밑처럼 표현 할 수 있다.
> dp[i] = max(dp[j] + a(S[i] - S[j])<sup>2</sup> + b(S[i] - S[j]) + c), (j < i)이다. 이를 전개하면
> = max(dp[j] + S[i]<sup>2</sup>a - 2S[i]S[j]a + S[j]<sup>2</sup>a + S[i]b - S[j]b + c)로 나타낼 수 있고 S[i]<sup>2</sup>a, S[i]b, c는 상수이기 때문에 따로 표기할 수 있다.
> = max(dp[j] - 2S[i]S[j]a + S[j]<sup>2</sup>a - S[j]b ) + S[i]<sup>2</sup>a+ S[i]b + c 에서 S[i]를 x로 치환한다면,
> = max(-2xS[j]a + dp[j] S[j]<sup>2</sup>a - S[j]b ) + S[i]<sup>2</sup>a+ S[i]b + c 즉, max() 안을 1차 함수로 표현할 수 있다.
> 1차 함수의 기울기인 -2xS[j]a에서 a는 음수이기 때문에 전체 함수 기울기는 양수이다.
> a < b 일 때, S[a] < S[b]이기 때문에 j가 커지면서 기울기가 커지므로 CHT를 사용할 수 있다.
- 전체 그래프의 모양은 위 예제(13263-나무자르기)에서 보았던 그래프에서 상하좌우 대칭한 모양이다.
- 단 여기서 주의할 점은 `j = 0`인 경우, 다시 말해 0~i를 모두 한 그룹으로 넣은 경우도 포함해야 한다는 것이고 다시 말해 y = 0인 그래프를 추가해야 한다는 뜻이다.
- 따라서 처음에는 `DP[1] = S[1]`로 놓고 그래프에 수를 대입할 때  그 값이 0보다 작다면 0으로 놓는 식으로 한다. 
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, a, b, c;
long long prefix_Sum[1000001], dp[1000001];

struct Linear {
    long long a, b;
    double intersect;
    Linear(long long _a = 0, long long _b = 0, double _intersect = 0) : a(_a), b(_b), intersect(_intersect) {}
};

double calcul_Intersect(Linear &L1, Linear &L2) {
    return 1.0 * (L2.b - L1.b) / (L1.a - L2.a);
}

long long calcul_Power(long long s) {
    return 1LL * s * s * a + 1LL * s * b + 1LL * c;
}

Linear line[1000001];

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    memset(prefix_Sum, 0, sizeof(prefix_Sum));
    memset(dp, 0, sizeof(dp));
    
    cin >> n >> a >> b >> c;
    for ( int i = 1; i <= n; i++ ) {
        long long num;
        cin >> num;
        prefix_Sum[i] = prefix_Sum[i-1] + num;
    }
    
    int top = 0;
    dp[1] = calcul_Power(prefix_Sum[1]);
    
    for ( int i = 2; i <= n; i++ ) {
        Linear next = Linear(-2 * prefix_Sum[i-1] * a, dp[i-1] + prefix_Sum[i-1] * prefix_Sum[i-1] * a - prefix_Sum[i-1] * b);
        
        while ( top > 0 ) {
            next.intersect = calcul_Intersect(line[top-1], next);
            if ( line[top-1].intersect < next.intersect ) break;
            top--;
        }
        line[top] = next;
        int target_Idx = top;
        long long target_X = prefix_Sum[i];
        if ( target_X < line[top].intersect ) {
            int low = 0, high = top;
            while ( low + 1 < high ) {
                int mid = (low + high) / 2;
                if ( target_X < line[mid].intersect) high = mid;
                else low = mid;
            }
            target_Idx = low;
        }
        
        dp[i] = max(line[target_Idx].a * target_X + line[target_Idx].b, 0LL) + calcul_Power(target_X);
        top++;
    }
    cout << dp[n];
    return 0;
}
```
### 📑[6171 - 땅따먹기](https://www.acmicpc.net/problem/6171)
#### 🔓 KeyPoint
- i번째 땅의 W<sub>i</sub>, H<sub>i</sub>와 j번째 땅의 W<sub>j</sub>, H<sub>j</sub>가 있을 때 W<sub>i</sub> <= W<sub>j</sub> && H<sub>i</sub> <= H<sub>j</sub>라면 i번째 땅은 가격을 계산할 때 영향을 주지 않는다.
- 따라서 땅들의 W값을 기준으로 오름차순 정렬을 한 뒤, 만약 다음 값의 H가 기존 값의 H보다 값이 크거나 같으면 기존에 있던 값을 제거하는 방식으로 땅을 줄여나갈 수 있다.
- 최종적으로 땅은 W기준으로 오름차순, H기준으로 내림차순으로 정렬된다.
- `DP[i] : 1~i번째 땅까지 구매했을 때 최소 값`이라 정의하자.
> dp[i] = max(dp[j] + W[i] * H[j]), (j < i)이다. 
> W[i]를 x로 치환한다면, dp[i] = max(H[j]x + dp[j])이다.
> a < b 일 때, H[a] > H[b]이기 때문에 j가 커지면서 기울기가 작아지므로 CHT를 사용할 수 있다.
- 이렇듯 데이터 주어졌을 때 조건을 고려하여 CHT가 가능한 형태의 전처리 과정을 수행하는 것이 중요하다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n;
pair<int,int> info[50001], ground[50001];
long long dp[50001];

struct Linear{
    long long a, b;
    double intersect;
    Linear(long long _a = 0, long long _b = 0, double _intersect = 0) : a(_a), b(_b), intersect(_intersect) {}
};

Linear line[50001];

double calcul_Intersect(Linear &L1, Linear &L2) {
    return 1.0 * (L2.b - L1.b) / (L1.a - L2.a);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    memset(dp, 0, sizeof(dp));
    
    cin >> n;
    for ( int i = 1; i <= n; i++ ) {
        int w, h;
        cin >> w >> h;
        info[i] = {w, h};
    }
    
    sort(info + 1, info + n + 1);
    
    int g_Idx = 1;
    for ( int i = 1; i <= n; i++ ) {
        while ( g_Idx > 1 && ground[g_Idx-1].second <= info[i].second ) g_Idx--;
        ground[g_Idx++] = info[i];
    }
    
    g_Idx--;
    int top = 0;
    for ( int i = 1; i <= g_Idx; i++ ) {
        Linear next = Linear(ground[i].second,dp[i-1]);
        
        while ( top > 0 ) {
            next.intersect = calcul_Intersect(line[top-1], next);
            if ( line[top-1].intersect < next.intersect ) break;
            top--;
        }
        
        line[top] = next;
        long long target_X = ground[i].first;
        long long target_Idx = top;
        
        if ( target_X < line[top].intersect ) {
            int low = 0, high = top;
            while ( low + 1 < high ) {
                int mid = (low + high) / 2;
                if ( target_X < line[mid].intersect ) high = mid;
                else low = mid;
            }
            target_Idx = low;
        }
        
        dp[i] = target_X * line[target_Idx].a + line[target_Idx].b;
        top++;
    }
    
    cout << dp[g_Idx];
    return 0;
}
```
