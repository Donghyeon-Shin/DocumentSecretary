# Concept
- 3개의 점 A, B, C를 한 직선으로 이었을 때 그 직선의 방향성을 구하는 알고리즘이다.
- 2차원, 3차원에 점들에 대해 CCW 알고리즘을 사용할 수 있다.
- CCW를 이용해 선분교차 여부를 파악할 수도 있고, Convex Hull 알고리즘을 구현할 수도 있다.
- CCW < 0이면 시계 방향, CCW = 0이면 직선, CCW > 0이면 반시계 방향이다.
- 연산 과정 밖에 없기 때문에 시간 복잡도는 O(1)이다.
# CCW 원리
- Vector의 외적을 계산해 직선의 방향성을 알 수 있다.
- 점 A, B, C가 있을 때 점 A, B를 이어 직선 AB를 만들고 점 B, C를 이어 직선 BC를 만들어 이 둘의 직선을 외적한다. ( 두 직선의 방향은 오른손 법칙을 통해 알 수 있다. )
- 행렬식을 외적해서 나온 값이 CCW 값이므로 CCW < 0이면 시계방향,  CCW = 0이면 직선, CCW > 0이면 반시계 방향이다.
#### 🖼️그림으로 이해하기
![[CCW Formula.svg]]

# CCW CODE
- CCW를 계산하는 과정에서 int 범위를 초과하는 경우가 많이 때문에 변수 입력값을 보고 CCW 계산 값의 자료형을 정해야 한다.
- CCW는 외적 계산을 통해 방향성만 알면 되기 때문에 CCW < 0일 때는 -1를 리턴하고 CCW = 0일때는 0을 CCW > 0면 +1를 리턴하도록 함수를 구현하는게 좋다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

typedef long long LL;
LL a1, a2, b1, b2, c1, c2;

struct Point {
    LL x, y;
    Point(LL X = 0, LL Y = 0) : x(X), y(Y) {}
    
    bool operator > (const Point &pp) {
        if ( x != pp.x ) return x > pp.x;
        return y != pp.y;
    }
    
    bool operator >= (const Point &pp) {
        if ( x != pp.x ) return x >= pp.x;
        return y >= pp.y;
    }
    
    bool operator == (const Point &pp) {
        if ( x == pp.x && y == pp.y ) return true;
        return false;
    }
};

int ccw(const Point &p1, const Point &p2, const Point &p3) {
    LL value = 1LL * (p2.x - p1.x) * (p3.y - p1.y) - 1LL * (p2.y - p1.y) * (p3.x - p1.x);
    if ( value > 0 ) return 1;
    if ( value == 0 ) return 0;
    return -1;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    Point p[3];
    cin >> a1 >> a2 >> b1 >> b2 >> c1 >> c2;
    p[0] = Point(a1, a2);
    p[1] = Point(b1, b2);
    p[2] = Point(c1, c2);
    
    cout << ccw(p[0], p[1], p[2]);
    return 0;
}
```
##### ❓ 예제 Input
	0 0 5 3 2 -2
##### ⭐ 예제 Output
	-1
# CCW 응용문제
### 📑[17387 - 선분 교차2](https://www.acmicpc.net/problem/17387)
#### 🔓 KeyPoint
- 두 선분 L1, L2의 끝 점 좌표 A(x1, y1), B(x2, y2), C(x3, y3), D(x4, y4)가 주어졌을 때 이 두 선분들이 서로 교차하는지를 판단하는 문제이다.
- 4개의 점에 A, B, C, D에 대해서 CCW(A,B,C), CCW(A,B,D), CCW(C,D,A), CCW(C,D,B)를 구해 선분 교차를 판단할 수 있다.
- CCW를 4번이나 연산해야 되는 이유는 다음과 같다.
![[Line-segment intersection.svg]]
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

typedef long long LL;

struct Point {
    LL x, y;
    Point(LL X = 0, LL Y = 0) : x(X), y(Y) {}
    
    bool operator > (const Point &pp) {
        if ( x != pp.x ) return x > pp.x;
        return y != pp.y;
    }
    
    bool operator >= (const Point &pp) {
        if ( x != pp.x ) return x >= pp.x;
        return y >= pp.y;
    }
    
    bool operator == (const Point &pp) {
        if ( x == pp.x && y == pp.y ) return true;
        return false;
    }
};

int ccw(const Point &p1, const Point &p2, const Point &p3) {
    LL value = 1LL * (p2.x - p1.x) * (p3.y - p1.y) - 1LL * (p2.y - p1.y) * (p3.x - p1.x);
    if ( value > 0 ) return 1;
    if ( value == 0 ) return 0;
    return -1;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    Point p[4];
    for ( int i = 0; i < 4; i++ ) {
        LL x, y;
        cin >> x >> y;
        p[i] = Point(x, y);
    }
    
    int abc = ccw(p[0],p[1],p[2]), abd = ccw(p[0],p[1],p[3]), cda = ccw(p[2],p[3],p[0]), cdb = ccw(p[2],p[3],p[1]);
    if ( abc * abd <= 0 && cda * cdb <= 0 ) {
        if ( abc * abd == 0 && cda * cdb == 0 ) {
            if ( p[0] > p[1] ) swap(p[0], p[1]);
            if ( p[2] > p[3] ) swap(p[2], p[3]);
            if ( p[3] >= p[0] && p[1] >= p[2] ) cout << 1;
            else cout << 0;
        } else cout << 1;
    } else cout << 0;
    return 0;
}
```
### 📑 [20149 - 선분 교차3](https://www.acmicpc.net/problem/20149)
#### 🔓 KeyPoint
- 선분 교차2와 크게 다른점은 없으나, 추가로 선분이 교차될 시 교차점을 구해야 하는 문제이다.
- 각각 방정식을 세워 교점을 계산해도 되나, 공식이 있기 때문에 이를 이용해도 된다.
![[Intersection points.svg]]
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

struct Point {
    long long x, y;
    Point(long long X = 0, long long Y = 0) : x(X), y(Y) {}
    bool operator > (const Point &pp) {
        if ( x != pp.x ) return x > pp.x;
        else return y > pp.y;
    }

    bool operator >= (const Point &pp) {
        if ( x != pp.x ) return x >= pp.x;
        else return y >= pp.y;
    }    
    
    bool operator==(const Point &pp ) {
        if ( x == pp.x && y == pp.y ) return 1;
        else return 0;
    }
};

int ccw(const Point &p1, const Point &p2, const Point &p3) {
    long long value = 1LL * (p2.x - p1.x) * (p3.y - p1.y) - 1LL * (p2.y - p1.y) * (p3.x - p1.x);
    if ( value < 0 ) return -1;
    else if ( value > 0 ) return 1;
    else return 0;
}

void print_Intersect(Point &p1, Point &p2, Point &p3, Point &p4) {
    double d = (p1.x - p2.x) * (p3.y - p4.y) - (p1.y - p2.y) * (p3.x - p4.x);
    
    if ( d == 0 ) {
        if ( p1 == p4 && p1 >= p3 ) cout << p1.x << ' ' << p1.y;
        else if ( p2 == p3 && p3 >= p1 ) cout << p2.x << ' ' << p2.y;
    } else {
        double px = (p1.x * p2.y - p1.y * p2.x ) * (p3.x - p4.x) - (p1.x - p2.x) * (p3.x * p4.y - p3.y * p4.x);
        double py = (p1.x * p2.y - p1.y * p2.x ) * (p3.y - p4.y) - (p1.y - p2.y) * (p3.x * p4.y - p3.y * p4.x);
        double x = px / d;
        double y = py / d;
        cout << fixed;
        cout.precision(9);
        cout << x << ' ' << y;
    }   
    
}

int n;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    Point p[4];
    
    for ( int i = 0; i < 4; i++ ) {
        long long x, y;
        cin >> x >> y;
        p[i] = Point(x, y);
    }
    
    int ccw_A = ccw(p[0], p[1], p[2]) * ccw(p[0], p[1], p[3]);
    int ccw_B = ccw(p[2], p[3], p[0]) * ccw(p[2], p[3], p[1]);

    if ( ccw_A <= 0 && ccw_B <= 0 ) {
        if ( ccw_A == 0 && ccw_B == 0 ) {
            Point a, b, c, d;
            if ( p[0] > p[1] ) swap(p[0], p[1]);
            if ( p[2] > p[3] ) swap(p[2], p[3]);
            
            if ( p[3] >= p[0] && p[1] >= p[2] ) {
                cout << "1\n";
                print_Intersect(p[0], p[1], p[2], p[3]);
            } else cout << "0";
        } else {
            cout << "1\n";
            print_Intersect(p[0], p[1], p[2], p[3]);
        }
    } else cout << "0";
    return 0;
}
```