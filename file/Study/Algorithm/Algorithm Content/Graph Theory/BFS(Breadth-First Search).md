# Concept
- 노드 탐색 방법 중 하나로 임의의 노드에서 인접한 노드들을 먼저 탐색하는 방법을 말한다.
- 인접한 노드들을 먼저 탐색하기 때문에 FIFO(선입선출)형 자료구조인 Queue를 사용한다.
- 가중치에 따라 탐색 순서가 달라지는 0-1 BFS도 있는데 이는 Prioirty Queue를 사용한다.
- 보통 Visited Array를 만들어 중복 탐색을 방지한다.
- 노드의 개수 n, 간선의 개수 e이라 할 때 시간 복잡도는 O(n+e)

# BFS 동작 과정
![[BASE TREE.svg]]

✏️ Node 1에서부터 탐색을 시작한다고 하자. 
	Node 1를 기준으로 깊이가 1인 노드들(Node 2와 Node 3)을 탐색한다. 
	그 후 Node1 에서 깊이가 2인 노드들(Node 4, Node 7, Node 8)을 탐색하고 깊이가 3인 노드들, 깊이가 4인 노드들을 차례대로 탐색하여 더 이상 탐색할 수 없을 때까지 반복한다.

이를 Queue로 표현하면 밑 그림처럼 된다.
#### 🖼️그림으로 이해하기
![[BFS Queue.svg]]
# BFS CODE
- BFS는 Queue 자료구조를 이용해 구현한다. 
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n; // node cnt
int e; // edge cnt
int start; // start node
vector<int> graph[10001];
bool visited[10001] = {0, };

void bfs(int node) {
	queue<int> q;
	q.push(node);
	visited[node] = true;
	
	while ( !q.empty() ) {
		int pNode = q.front();
		q.pop();
		cout << pNode << ' ';
		for ( int i = 0; i < (int)graph[pNode].size(); i++ ) {
			int nNode = graph[pNode][i];
			if ( !visited[nNode] ) {
				visited[nNode] = true;
				q.push(nNode);
			}
		}
	}
}

int main() {
	ios_base::sync_with_stdio(false);
	cin.tie(NULL); cout.tie(NULL);
	
	cin >> n >> e;
	for ( int i = 0; i < e; i++ ) {
		int a, b;
		cin >> a >> b;
		graph[a].push_back(b);
		graph[b].push_back(a);
	}
	cin >> start;
	bfs(start);
	return 0;
}
```
##### ❓ 예제 Input
	10
	9
	1 2
	1 3
	2 4
	4 5
	4 6
	3 7
	3 8
	8 9
	8 10
	1
##### ⭐ 예제 Output
	1 2 3 4 7 8 5 6 9 10
# BFS 응용문제
### 📑[2178 - 미로 탐색](https://www.acmicpc.net/problem/2178)
#### 🔓 KeyPoint
- 그래프 (1,1)에서 시작해 (n, m)으로 이동해야 한다. (1,1)를 기준으로 BFS 탐색을 시작하여 갈 수 있는 곳(값이 0인 지점)을 찾아서 현재 값에 1를 더해주면 그 값이 이동할 수 있는 최소 칸 수이다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, m, graph[101][101];
int dx[4] = {1, -1, 0, 0}, dy[4] = {0, 0, -1, 1};

void bfs(int x, int y) {
	queue<pair<int, int>> q;
	q.push({y,x});
	while ( !q.empty() ) {
		int y = q.front().first;
		int x = q.front().second;
		q.pop();
		for ( int i = 0; i < 4; i++ ) {
			int nx = x + dx[i];
			int ny = y + dy[i];
			if ( x <= -1 || x >= m+1 || y <= -1 || y >= n+1 ) continue;
			if ( graph[ny][nx] == 1 ) {
				q.push({ny, nx});
				graph[ny][nx] = graph[y][x] + 1;
			}
		}
	}
}

int main() {
	cin >> n >> m;
	for ( int i = 1; i <= n; i++ ) {
		for ( int j = 1; j <= m; j++ ) {
			scanf("%1d", &graph[i][j]);
		}
	}
	bfs(1,1);
	cout << graph[n][m];
}
```
### 📑[17114 - 하이퍼 토마토](https://www.acmicpc.net/problem/17114)
#### 🔓 KeyPoint
- 좌표를 2차원이 아닌 11차원으로 확장한 문제이다. 인접한 노드들이 2차원보다 많이 때문에 이를 고려해 구현하면 된다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int m, n, o, p, q, r, s, t, u, v, w, day = 0;
queue<tuple<int, int, int, int, int, int, int, int, int, int, int>> ripen;

int da[22] = {-1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int db[22] = {0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int dc[22] = {0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int dd[22] = {0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int de[22] = {0, 0, 0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int df[22] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int dg[22] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0};
int dh[22] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0};
int di[22] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0};
int dj[22] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1, 0, 0};
int dk[22] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1};

int main() {
	ios_base::sync_with_stdio(false);
	cin.tie(NULL); cout.tie(NULL);
	
	cin >> m >> n >> o >> p >> q >> r >> s >> t >> u >> v >> w;
	int graph[w][v][u][t][s][r][q][p][o][n][m];
	
	memset(graph, 0, sizeof(graph));
	
	for ( int a = 0; a < w; a++ ) {
		for ( int b = 0; b < v; b++ ) {
			for ( int c = 0; c < u; c++ ) {
				for ( int d = 0; d < t; d++ ) {
					for ( int e = 0; e < s; e++ ) {
						for ( int f = 0; f < r; f++ ) {
							for ( int g = 0; g < q; g++ ) {
								for ( int h = 0; h < p; h++ ) {
									for (int i = 0; i < o; i++ ) {
										for ( int j = 0; j < n; j++ ) {
											for ( int k = 0; k < m; k++ ) {
												cin >> graph[a][b][c][d][e][f][g][h][i][j][k];
												if ( graph[a][b][c][d][e][f][g][h][i][j][k] == 1 ) ripen.push({a, b, c, d, e, f, g, h, i, j ,k});
											}
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}
	while ( 1 ) {
		queue<tuple<int, int, int, int, int, int, int, int, int, int, int>> temp;
	
		while ( !ripen.empty() ) {
			int a, b, c, d, e, f, g, h, i, j, k;
			tie(a, b, c, d, e, f, g, h, i, j, k) = ripen.front();
			ripen.pop();
			
			for ( int x = 0; x < 22; x++ ) {
				int na = a + da[x];
				int nb = b + db[x];
				int nc = c + dc[x];
				int nd = d + dd[x];
				int ne = e + de[x];
				int nf = f + df[x];
				int ng = g + dg[x];
				int nh = h + dh[x];
				int ni = i + di[x];
				int nj = j + dj[x];
				int nk = k + dk[x];
				
				if ( na < 0 || na >= w || nb < 0 || nb >= v || nc < 0 || nc >= u || nd < 0 || nd >= t || ne < 0 || ne >= s || nf < 0 || nf >= r || ng < 0 || ng >= q || nh < 0 || nh >= p || ni < 0 || ni >= o || nj < 0 || nj >= n || nk < 0 || nk >= m  ) continue;
				if ( graph[na][nb][nc][nd][ne][nf][ng][nh][ni][nj][nk] == 0 ) {
					graph[na][nb][nc][nd][ne][nf][ng][nh][ni][nj][nk] = 1;
					temp.push({na, nb, nc, nd, ne, nf, ng, nh, ni, nj, nk});
				}
			}
		}
		
		if ( temp.empty() ) break;
		day++;
		ripen = temp;
	}
	
	for ( int a = 0; a < w; a++ ) {
		for ( int b = 0; b < v; b++ ) {
			for ( int c = 0; c < u; c++ ) {
				for ( int d = 0; d < t; d++ ) {
					for ( int e = 0; e < s; e++ ) {
						for ( int f = 0; f < r; f++ ) {
							for ( int g = 0; g < q; g++ ) {
								for ( int h = 0; h < p; h++ ) {
									for (int i = 0; i < o; i++ ) {
										for ( int j = 0; j < n; j++ ) {
											for ( int k = 0; k < m; k++ ) {
												if ( graph[a][b][c][d][e][f][g][h][i][j][k] == 0 ) {
													day = -1;
													break;
												}
											}
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}
	
	cout << day;
	return 0;
}
```