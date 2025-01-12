# Concept
- 2차원 좌표 평면에 위에 존재하는 여러 점들 중 일부를 이용하여 모든 점을 포함하는 볼록 다각형을 말한다.
- 볼록 다각형이란, 경계의 두 점을 잇는 어떤 선분도 다각형 외부로 나가지 않는 단순 다각형 이다.
- Convex Hull을 구하기 위해선 모든 점들을 탐색하여 해당 점이 다격형의 선분으로 포함될지 안될지를 판단해야 한다.
- Convex Hull의 대표적인 알고리즘은 Graham's Scan이다.

# Graham's Scan 원리
- Graham's Scan의 작동 방식을 알기 위해선 [[CCW(Counter Clock Wise)]] 작동 방식이 선행되어야 한다.
- 우선 2차원 배열의 점들을 탐색하기 용이하게 모든 점들을 정렬한다.
- 점의 정렬 방식은 가장 작은 점을 기준으로 상대 위치를 기준으로 반시계 방향 정렬한다. 
- Stack Structure를 사용해 처음 두 점 a, b를 넣는다.
- 모든 점을 탐색하면서 stack에 최상 단에 있는 두 점 a, b 그리고 다음 점 c와 연산을 통해 CCW를 하면서 CCW > 0면 b점을 다시 Stack으로 CCW <= 0이면 CCW > 0일때까지 Stack의 점을 빼면서 볼록한 지점을 찾는다.
- CCW > 0이거나 Stack의 점이 1개 밖에 없다면 다음 점을 Stack에 넣고 다시 연산한다.
- 모든 점을 다 탐색한다면 Stack에 있는 점들이 Convex Hull을 이루는 점들이다.
- 시간 복잡도는 탐색과 반복 CCW 연산을 통한 O(nlogn)이다.
#### 🖼️그림으로 이해하기
![[Graham's Scan Graph.svg]]

# Graham's Scan CODE
- Grahman's Scan 구현에서 중요한 것은 상대 위치를 기준으로 정렬한 후 탐색을 진행하는 것이다.
- 상대 위치를 파악하기 위해서 비교연산자 '<'를 Operator Overloading 해주면 된다.
- 상대 위치가 같을 경우 y좌표 기준으로 정렬, 그 후 x좌표로 정렬한다.
- 가장 작은 점을 기준으로 상대 정렬을 하는 것이기 때문에 처음에 정렬 후(처음엔 상대 위치가 다 0이기 때문에 상대 정렬 연산이 같다.) 처음 점 기준 상대 위치를 구하고 상대 정렬을 해주면 된다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

typedef long long LL;

int n, l;
stack<int> st;

struct Point {
    LL x, y, p, q;
    Point(int X = 0, int Y = 0) : x(X), y(Y), p(1), q(0) {}
    
    bool operator < ( const Point &pp ) {
        if ( 1LL * pp.p * q != 1LL * p * pp.q ) return 1LL * pp.p * q < 1LL * p * pp.q;
        if ( y != pp.y ) return y < pp.y;
        return x < pp.x;
    }
};

LL ccw( const Point &d1, const Point &d2, const Point &d3 ) {
    return 1LL * ( d1.x * d2.y + d2.x * d3.y + d3.x * d1.y - d2.x * d1.y - d3.x * d2.y - d1.x * d3.y );
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> n;
    Point dot[n];
    
    for ( int i = 0; i < n; i++ ) {
        LL x, y;
        cin >> x >> y;
        dot[i] = Point(x, y);
    }
    
    sort(dot, dot + n);
    
    for ( int i = 1; i < n; i++ ) {
        dot[i].p = dot[i].x - dot[0].x;
        dot[i].q = dot[i].y - dot[0].y;
    }
    
    sort(dot+1, dot+n);
    
    st.push(0);
    st.push(1);
    int nDot = 2;
    
    while ( nDot < n ) {
        while ( (int)st.size() >= 2 ) {
            int d1, d2;
            d1 = st.top();
            st.pop();
            d2 = st.top();
            
            if ( ccw(dot[d2], dot[d1], dot[nDot]) > 0 ) {
                st.push(d1);
                break;
            }
        }
        st.push(nDot++);
    }
    
    cout << st.size();
    return 0;
}
```
##### ❓ 예제 Input
	8
	1 1
	1 2
	1 3
	2 1
	2 2
	2 3
	3 1
	3 2
##### ⭐ 예제 Output
	1 3
	2 3
	3 2 
	3 1
	1 1
# Convex Hull 응용문제
### 📑[9240 - 로버트 후드](https://www.acmicpc.net/problem/9240)
#### 🔓 KeyPoint
- 2차원 좌표 중 거리가 최대인 두 점은 Convex Hull을 이루는 점들 중 하나이다.
- 따라서 Convex Hull을 구한 뒤 Convex Hull 모든 점들의 거리 중 최대 거리를 구한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

typedef long long LL;

struct Point{
    LL x, y, p, q;
    Point(LL X = 0, LL Y = 0) : x(X), y(Y), p(1), q(0) {}
    bool operator < (const Point &pp ) {
        if ( 1LL * pp.p * q != 1LL * p * pp.q ) return 1LL * pp.p * q < 1LL * p * pp.q;
        if ( y != pp.y ) return y < pp.y;
        return x < pp.x;
    }
    
};

LL dist(const Point &p1, const Point &p2) {
    LL x = p1.x - p2.x;
    LL y = p1.y - p2.y;
    return 1LL * x * x + 1LL * y * y;
}

int ccw(const Point &p1, const Point &p2, const Point &p3) {
    LL value = 1LL * (p2.x - p1.x) * (p3.y - p1.y) - 1LL * (p2.y - p1.y) * (p3.x - p1.x);
    if ( value > 0 ) return 1;
    else if ( value == 0 ) return 0;
    else return -1;
}

int c;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    cin >> c;
    Point p[c];
    for ( int i = 0; i < c; i++ ) {
        LL x, y;
        cin >> x >> y;
        p[i] = Point(x, y);
    }
    
    sort(p, p+c);
    
    for ( int i = 1; i < c; i++ ) {
        p[i].p = p[i].x - p[0].x;
        p[i].q = p[i].y - p[0].y;
    }
    
    sort(p+1, p+c);
    
    stack<int> st;
    st.push(0);
    st.push(1);
    
    int nPoint = 2;
    
    while ( nPoint < c ) {
        while ( (int)st.size() >= 2 ) {
            int p1 = st.top();
            st.pop();
            int p2 = st.top();
            
            if ( ccw(p[p2], p[p1], p[nPoint]) > 0 ) {
                st.push(p1);
                break;
            }
        }
        st.push(nPoint++);
    }
    
    int st_Size = (int)st.size();
    
    Point convex_Hull[st_Size];
    
    for ( int i = st_Size-1; i >= 0; i-- ) {
        convex_Hull[i] = p[st.top()];
        st.pop();
    }
    
    int p1 = 0, p2 = 1;
    LL maximum = dist(convex_Hull[p1], convex_Hull[p2]);
    
    for ( int i = 0; i < st_Size*2; i++ ) {
        int nP1 = (p1+1) % st_Size;
        int nP2 = (p2+1) % st_Size;
        
        Point nP = Point(convex_Hull[nP2].x - (convex_Hull[p2].x - convex_Hull[nP1].x), convex_Hull[nP2].y - (convex_Hull[p2].y - convex_Hull[nP1].y));
        
        int ccw_Result = ccw(convex_Hull[p1], convex_Hull[nP1], nP);
        
        if ( ccw_Result >= 0 ) p2 = nP2;
        else p1 = nP1;
        
        maximum = max(maximum, dist(convex_Hull[p1], convex_Hull[p2]));
    }
    
    cout << fixed;
    cout.precision(6);
    cout << sqrt(maximum);
    return 0;
}
```
### 📑[17403 - 가장 높고 넓은 성](https://www.acmicpc.net/problem/17403)
#### 🔓 KeyPoint
- Convex Hull을 구하고 그 점들을 제외한 후 다시 Convex Hull을 구하면서 모든 점들을 여러 개의 Convex Hull로 만드는 문제이다.
- 단순히 반복하면 되지만, 그 구현이 생각보다 까다로운 문제이다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

typedef long long LL;

struct Point{
    LL x, y, p, q;
    int idx;
    Point(LL X = 0, LL Y = 0, int IDX = 0) : x(X), y(Y), p(1), q(0), idx(IDX) {}
    bool operator < (const Point &pp) {
        if ( 1LL * pp.p * q != 1LL * p * pp.q ) return 1LL * pp.p * q < 1LL * p * pp.q;
        if ( y != pp.y ) return y < pp.y;
        return x < pp.x;
    }
};

LL ccw(const Point &p1, const Point &p2, const Point &p3) {
    LL value = 1LL * (p2.x - p1.x) * (p3.y - p1.y) - 1LL * (p2.y - p1.y) * (p3.x - p1.x);
    if ( value < 0 ) return -1;
    else if ( value > 0 ) return 1;
    else return 0;
}

int n, level[1001] = {0, }, l = 1;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
   
    cin >> n;
    vector<Point> p;
   
    for ( int i = 0; i < n; i++ ) {
        LL x, y;
        cin >> x >> y;
        p.push_back(Point(x, y, i));
    }
   
    while ( 1 ) {
        int min_X = 1e9, min_Y = 1e9, target = 0;
        for ( int i = 0; i < (int)p.size(); i++ ) {
            if ( ( min_Y > p[i].y ) || ( min_Y == p[i].y && min_X > p[i].x) ) {
                target = i;
                min_X = p[i].x;
                min_Y = p[i].y;
            }
        }
        swap(p[target], p[0]);
       
        for ( int i = 1; i < (int)p.size(); i++ ) {
            p[i].p = p[i].x - p[0].x;
            p[i].q = p[i].y - p[0].y;
        }
       
        sort(++p.begin(), p.end());
       
        stack<int> st;
        st.push(0);
        st.push(1);
       
        int nPoint = 2;
       
        while ( nPoint < (int)p.size() ) {
            while ( (int)st.size() >= 2 ) {
                int p1 = st.top();
                st.pop();
                int p2 = st.top();
                if ( ccw(p[p2], p[p1], p[nPoint]) > 0 ) {
                    st.push(p1);
                    break;
                }
            }
            st.push(nPoint++);
        }
       
        if ( (int)st.size() <= 2 ) break;
        
        bool visited[(int)p.size()] = {0, };
        vector<Point> nP;
        
        while ( !st.empty() ) {
            int t = st.top();
            visited[t] = true;
            level[p[t].idx] = l;
            st.pop();
        }
       
        for ( int i = 0; i < (int)p.size(); i++ ) {
            if ( !visited[i] ) nP.push_back(p[i]);
        }
        
        p.clear();
        p = nP;
       
        if ( (int)p.size() <= 2 ) break;
        l++;
    }

    for ( int i = 0; i < n; i++ ) cout << level[i] << ' ';
    return 0;
}
```
