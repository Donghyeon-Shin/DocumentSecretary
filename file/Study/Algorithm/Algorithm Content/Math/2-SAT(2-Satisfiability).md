# Concept
- 2-Satisfiability(2-SAT)은 뜻 그대로 충족 가능성 문제 중 하나로 여러 Boolean 변수들이 괄호(절:Clause)안에는 OR이 밖에는 AND의 논리 연산으로 이루어져있는 CNF(Conjunctive Normal Form)가 참인지 아닌지 파악하는 문제이다.
- Caluse 안에 변수가 최대 2개인 문제를 2-SAT 문제라고 한다.
- 3-SAT 이상인 문제들은 모두 3-SAT으로 표현 가능한데 이러한 문제는 np-Hard 즉, 다항시간 내에 풀 수 없는 문제이다.
- ex) `F(x) = (¬x1 ∨ x2) ∧ (x3 ∨ ¬x2) ∧ (¬x4 ∨ ¬x5) ∧ (¬x5 ∨ x1) ∧ (x3 ∨ x6)`
- [[SCC(Strongly Connected Component)]] 알고리즘을 이용하여 문제를 해결하고 시간 복잡도는 SCC와 같은 O(V+E)이다. / 노드 수(V), 간선 수(E)
# 2-SAT 원리📑[11280 - 2-SAT - 3](https://www.acmicpc.net/problem/11280)
- 변수 p와 q가 있을 때 p가 참일 때 q가 참이라는 뜻의 명제를 p ⇒ q라고 한다.
- Clause 안에는 두 변수가 ∨로 이루어져 있다. 이를 `p ∨ q`라고 할 때, 이 명제가 참이기 위해선 p, q 둘 중 하나만 참이여도 된다. 
- 이를 다시 표현하면 해당 명제가 참이기 위해선 ¬p ⇒ q 이거나 ¬q ⇒ p 이여야 한다.
- 여러 Clause을 이런식으로 표현할 수 있고 이는 단방향 그래프로 나타낼 수 있다.
- 모든 Clause을 단방향 그래프로 표현할 때 SCC로 그룹을 나눌 수 있고 하나의 SCC 그룹에서 ¬p ⇒ p 처럼 하나의 변수가 NOT 형 변수랑 같이 존재하게 된다면 모순이 발생하여 CNF은 거짓이 된다.
#### 🖼️그림으로 이해하기
![[2-SAT Graph.svg]]
# 2-SAT CODE
- NOT형의 변수도 단반향 그래프로 이어주어야 하기 때문에 node를 분리해 `i번째 노드 P의 경우 P : (i-1) * 2, NOT P : (i-1) * 2 + 1 
- NOT의 형태는 음수로 주어지기 때문에 양수로 변환하여야 한다.
- SCC을 통해 그룹을 나누고 모든 변수들에 대해 모순이 없는지 판단(SCC 그룹 : p == NOT p)해야 한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, m, parent[20001], id = 0, mark = 0, numbring[20001] = {0, };
bool finish[20001] = {0, };
stack<int> st;
vector<int> graph[20001];

int not_Trans(int node) {
    if ( node % 2 == 0 ) return node + 1;
    else return node - 1;
}

int dfs(int node) {
    parent[node] = ++id;
    st.push(node);
    int p = parent[node];
    
    for ( int i = 0; i < (int)graph[node].size(); i++ ) {
        int nNode = graph[node][i];
        
        if ( parent[nNode] == 0 ) p = min(p, dfs(nNode));
        else if ( !finish[nNode] ) p = min(p, parent[nNode]);
    }
    
    if ( parent[node] == p ) {
        mark++;
        while ( 1 ) {
            int n = st.top();
            st.pop();
            
            finish[n] = true;
            numbring[n] = mark;
            if ( node == n ) break;
        }
    }
    
    return p;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n >> m;
    for ( int i = 0; i < m; i++ ) {
        int n1, n2;
        cin >> n1 >> n2;
        n1 = ( n1 < 0 ) ? -(n1+1) * 2 + 1 : (n1-1) * 2;
        n2 = ( n2 < 0 ) ? -(n2+1) * 2 + 1 : (n2-1) * 2;
        graph[not_Trans(n1)].push_back(n2);
        graph[not_Trans(n2)].push_back(n1);
    }
    
    
    for ( int i = 0; i <= (n-1) * 2 + 1; i++ ) {
        if ( !finish[i] ) dfs(i);
    }
    
    for ( int i = 1; i <= n ; i++ ) {
        if ( numbring[(i-1) * 2] == numbring[(i-1) * 2 + 1] ) {
            cout << 0;
            return 0;
        }
    }
    cout << 1;
    return 0;
}
```
##### ❓ 예제 Input
	6 8
	-1 2
	3 -2
	-4 -5
	-3 1
	4 -2
	4 -5
	5 6
	-6 5
##### ⭐ 예제 Output

	0
# 2-SAT 응용문제
### 📑[11281 - 2-SAT - 4](https://www.acmicpc.net/problem/11281)
#### 🔓 KeyPoint
- 2-SAT - 3번에서 CNF가 참이 된다면 그 참이 될 수 있는 변수들 값을 출력하는 문제이다.
- SCC의 값을 기준으로 위상정렬을 한 뒤, 첫 번째 SCC그룹부터 변수에 값이 저장되어 있지 않으면 그 변수에 False값을 넣으면 된다.
- 만약 p ⇒ q일때 p가 True인데 q가 False라면 이 명제 자체가 False가 된다. 하지만 p가 False가 된다면 q의 값에 상관없이 명제는 참이 된다. 
- 따라서 SCC 1번 그룹부터 시작해 지정되지 않은 변수를 False로 그 반대 변수를 True로 설정해준다.
- 이미 p와 !p가 서로 같은 SCC 그룹에 포함되지 않는다고 계산하였기 때문에, 먼저 나온 변수를 False로 설정해 둔다면, False -> True가 될 수 있으나 True -> False가 되는 명제는 될 수 없다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, m, parent[20001], id = 0, mark = 0, numbering[20001], result[10001];
bool finish[20001] = {0, };
stack<int> st;
vector<int> graph[20001];
vector<pair<int,int>> parent_sort;

int tras_Negation(int node) {
    if ( node % 2 == 0 ) return node + 1;
    else return node - 1;
}

int dfs(int node) {
    parent[node] = ++id;
    st.push(node);
    int p = parent[node];
    for ( int i = 0; i < (int)graph[node].size(); i++ ) {
        int nNode = graph[node][i];
        if ( parent[nNode] == 0 ) p = min(p, dfs(nNode));
        else if ( !finish[nNode] ) p = min(p, parent[nNode]);
    }
    
    if ( p == parent[node] ) {
        mark++;
        while ( 1 ) {
            int n = st.top();
            st.pop();
            
            finish[n] = true;
            numbering[n] = mark;
            if ( n == node ) break;
        }
    }
    
    return p;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    memset(result, -1, sizeof(result));
    
    cin >> n >> m;
    for ( int i = 0; i < m; i++ ) {
        int n1, n2;
        cin >> n1 >> n2;
        n1 = ( n1 < 0 ) ? -(n1 + 1) * 2 + 1 : (n1 - 1) * 2;
        n2 = ( n2 < 0 ) ? -(n2 + 1) * 2 + 1 : (n2 - 1) * 2;
        graph[tras_Negation(n1)].push_back(n2);
        graph[tras_Negation(n2)].push_back(n1);
    }
    
    for ( int i = 0; i < 2 * n; i++ ) {
        if ( !finish[i] ) dfs(i);
    }
    
    for ( int i = 1; i <= n; i++ ) {
        if ( numbering[(i - 1) * 2] == numbering[(i-1) * 2 + 1] ) {
            cout << 0;
            return 0;
        }
    }
    
    for ( int i = 0; i < 2 * n; i++ ) parent_sort.push_back({numbering[i], i});
    sort(parent_sort.begin(), parent_sort.end());
    
    for ( int i = n * 2 - 1; i >= 0; i-- ) {
        int curr = parent_sort[i].second;
        if ( result[curr / 2 + 1] == -1 ) result[curr / 2 + 1] = (curr % 2 == 0 ) ? 0 : 1;
    }
    cout << "1\n";
    for ( int i = 1; i <= n; i++ ) cout << result[i] << ' ';
    return 0;
}
```
### 📑[3648 - 아이돌](https://www.acmicpc.net/problem/3648)
#### 🔓 KeyPoint
- 심사위원이 투표를 2장하고 그 두 장 중 최소 하나 이상이 심사에 반영되어야 하기 때문에 2-SAT 문제라고 할 수 있다.
- 심사위원들의 투표(CNF)에서 특정 변수(p)를 무조건 참으로 만족시키게 하기 위해서는 `CNF ∧ (p∨p)`로 변형하면 된다. 이는 CNF를 만족 시키면서 p가 무조건 참이 되는 명제이다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, m, parent[2001], id = 0, mark = 0, numbering[2001] = {0, };
bool finish[2001] = {0, };
stack<int> st;
vector<int> graph[2001];

int not_Transfrom(int node) {
	if ( node % 2 == 0 ) return node+1;
	return node-1;
}

int dfs(int node) {

	parent[node] = ++id;
	st.push(node);
	int p = parent[node];
	
	for ( int i = 0; i < (int)graph[node].size(); i++ ) {
		int nNode = graph[node][i];
		
		if ( parent[nNode] == 0 ) p = min(p, dfs(nNode));
		else if ( !finish[nNode] ) p = min(p, parent[nNode]);
	}

	if ( parent[node] == p ) {
		mark++;
		while ( 1 ) {
			int n = st.top();
			st.pop();
			
			finish[n] = true;
			numbering[n] = mark;
			if ( node == n ) break;
		}
	}
	
	return p;
}

int main() {
	ios_base::sync_with_stdio(false);
	cin.tie(NULL); cout.tie(NULL);
	
	while ( cin >> n >> m ) {
		for ( int i = 0; i < m; i++ ) {
			int n1, n2;
			cin >> n1 >> n2;
			n1 = ( n1 < 0 ) ? -(n1+1) * 2 + 1 : (n1-1) * 2;
			n2 = ( n2 < 0 ) ? -(n2+1) * 2 + 1 : (n2-1) * 2;
			graph[not_Transfrom(n1)].push_back(n2);
			graph[not_Transfrom(n2)].push_back(n1);
		}

		graph[1].push_back(0);
		
		for ( int i = 0; i <= (n-1) * 2 + 1; i++ ) {
			if ( !finish[i] ) dfs(i);
		}
		
		bool check = true;
		
		for ( int i = 1; i <= n; i++ ) {
			if ( numbering[(i-1) * 2] == numbering[(i-1) * 2 + 1]) {
				check = false;
				break;
			}
		}
		
		if ( check ) cout << "yes\n";
		else cout << "no\n";  
		
		id = 0; mark = 0;
		for ( int i = 0; i <= 2000; i++ ) graph[i].clear();
		memset(parent, 0, sizeof(parent));
		memset(numbering, 0, sizeof(numbering));
		memset(finish, 0, sizeof(finish));
		while( !st.empty() ) st.pop();
	}
	return 0;
}
```
### 📑[2519 - 막대기](https://www.acmicpc.net/problem/2519)
#### 🔓 KeyPoint
- 학생이 n명이라 할 때 `n*3`개의 막대기가 존재한다. (학생 : n, 막대기 : m)
- grpah를 연결할 때 not_Transform도 존재해야 하기 때문에 총 `n * 3 * 2`의 node가 필요하다.
- `node의 idx = 6*n + (2 * m + 1)`로 놓을 수 있고 n의 값이 최대 1,000이기 때문에 node의 최대값은 6000이다.
- 명제 px를 `x번 막대기를 제거해야 한다`로 정의할 때 학생마다 3개의 막대기(s1, s2, s3) 중 최대 한 개의 막대기만 제거할 수 있기 때문에 총 6개의 명제를 놓아야 한다.
	- 막대기 1이 제거되면 2,3은 제거하면 안된다.
		s1 -> NOT s2
		s1 -> NOT s3
	- 막대기 2이 제거되면 2,3은 제거하면 안된다.
		s2 -> NOT s1
		s2 -> NOT s3
	- 막대기 3이 제거되면 2,3은 제거하면 안된다.
		s3 -> NOT s1
		s3 -> NOT s2
- 모든 막대기 중 [[CCW(Counter Clock Wise)]] 알고리즘을 사용하여 겹치는 막대기(s1, s2)를 찾고 이를 `NOT s1 -> s2, NOT s2 -> s1`의 명제로 놓는다.
- 이어진 모든 명제를 토대로 2-SAT 알고리즘을 이용하면 문제를 해결할 수 있다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, parent[6001], id = 0, mark = 0, numbering[6001];
bool finish[6001] = {0, };
pair<int,int> point[6001][2];
stack<int> st;
vector<int> graph[6001], result;
vector<pair<int,int>> parent_sort;

int tras_Negation(int node) {
    if ( node % 2 == 0 ) return node - 1;
    else return node + 1;
}

int ccw(int x1, int y1, int x2, int y2, int x3, int y3) {
    int val = (x2 - x1) * (y3 - y2) - (x3 - x2) * (y2 - y1);
    if ( val < 0 ) return -1;
    else if ( val > 0 ) return 1;
    else return 0;
}

bool isIntersect(pair<int,int> p1[2], pair<int,int> p2[2]) {
    int x1, y1, x2, y2, x3, y3, x4, y4;
    tie(x1, y1) = p1[0];
    tie(x2, y2) = p1[1];
    tie(x3, y3) = p2[0];
    tie(x4, y4) = p2[1];
    
    int r1 = ccw(x1, y1, x2, y2, x3, y3);
    int r2 = ccw(x1, y1, x2, y2, x4, y4);
    int r3 = ccw(x3, y3, x4, y4, x1, y1);
    int r4 = ccw(x3, y3, x4, y4, x2, y2);
    
    return (r1 * r2 < 0) && (r3 * r4 < 0);
}

int dfs(int node) {
    parent[node] = ++id;
    st.push(node);
    int p = parent[node];
    for ( int i = 0; i < (int)graph[node].size(); i++ ) {
        int nNode = graph[node][i];
        if ( parent[nNode] == 0 ) p = min(p, dfs(nNode));
        else if ( !finish[nNode] ) p = min(p, parent[nNode]);
    }
    
    if ( p == parent[node] ) {
        mark++;
        while ( 1 ) {
            int n = st.top();
            st.pop();
            
            finish[n] = true;
            numbering[n] = mark;
            if ( n == node ) break;
        }
    }
    
    return p;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n;
    for ( int i = 0; i < n; i++ ) {
        for ( int j = 0; j < 3; j++ ) {
            int x1, y1, x2, y2;
            cin >> x1 >> y1 >> x2 >> y2;
            point[6*i + 2*j + 1][0].first = x1;
            point[6*i + 2*j + 1][0].second = y1;
            point[6*i + 2*j + 1][1].first = x2;
            point[6*i + 2*j + 1][1].second = y2;
        }
    }
    
    // 학생이 최대 한 개만 제거 가능하도록 graph 연결
    for ( int i = 0; i < n; i++ ) {
        graph[6*i + 1].push_back(tras_Negation(6*i + 3));
        graph[6*i + 1].push_back(tras_Negation(6*i + 5));
        graph[6*i + 3].push_back(tras_Negation(6*i + 1));
        graph[6*i + 3].push_back(tras_Negation(6*i + 5));
        graph[6*i + 5].push_back(tras_Negation(6*i + 1));
        graph[6*i + 5].push_back(tras_Negation(6*i + 3));
    }
    
    // 막대기가 겹칠 경우 제거 가능하도록 graph 연결
    for ( int i = 1; i <= 6*n; i += 2 ) {
        for ( int j = i + 2; j <= 6*n; j += 2 ) {
            if ( isIntersect(point[i], point[j]) ) {
                graph[tras_Negation(i)].push_back(j);
                graph[tras_Negation(j)].push_back(i);
            }
        }
    }
    
    for ( int i = 1; i <= 6 * n; i++ ) {
        if ( !finish[i] ) dfs(i);
    }
    
    for ( int i = 1; i <= 6 * n; i += 2 ) {
        if ( numbering[i] == numbering[tras_Negation(i)] ) {
            cout << -1;
            return 0;
        }
        if ( numbering[i] < numbering[tras_Negation(i)] ) result.push_back(i / 2 + 1);
    }
    cout << (int)result.size() << '\n';
    for ( auto i : result ) cout << i << ' ';
    return 0;
}
```