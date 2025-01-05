# Concept
- Trie는 Retrieval Tree(탐색 트리) 이름에서 따온 말로, 문자열을 저장하고 효율적으로 탐색하기 위한 Tree이다.
- Radix Tree, Prefix Tree라고도 불린다.
- 문자열을 저장하는 측면에서 각 노드들이 자식 포인터 배열을 가지고 있다는 점에서 메모리 측면에서는 좋지 않지만 여러 문자열들을 탐색할 때 시간복잡도가 작다.
- 문자열의 하나하나의 문자를 [[DFS(Depth-First Search)]]로 노드에 넣고 이를 이어서 하나의 Tree를 만든다.
- 문자열들의 개수를 M, 문자열들 중 가장 긴 문자열의 길이를 L이라고 할 때 `Tree 생성 시간복잡도 : O(L*M), 탐색 시간복잡도 : O(L)`이다.
# Tire 원리
- Tire는 Tree Struct로 구현되며, Struct 내부에는 자식 Trie 포인터를 저장하는 Array와 문자열의 끝을 판단하는 Finish(Bool 변수), Insert Function, Serach Function이 존재한다.
- Insert Function에서는 String를 Parameter로 받고 String의 문자 하나가 자신의 자식 Trie에 있다면 그 자식에 String의 다음 문자 위치를 넘기고 해당 문자의 자식이 존재하지 않으면 그 자식을 만든 뒤 다음 문자 위치를 넘긴다.
- 문자열이 마지막 위치에 도착한다면 Finish를 True로 만든다.
- Serach Function에서는 마찬가지로 String를 Parameter로 받고 현재 String의 문자가 존재하지 않는다면 return False를 존재한다면 그 문자의 자식에 String의 다음 문자 위치를 넘긴다.
- 만약 String의 마지막에 도착했고 Finish가 True라면 Trie에 해당 String이 있는 것이기 때문에 return True를 아니면 해당 문자열이 없다는 것이기에 return False를 한다.
#### 🖼️그림으로 이해하기
![[Trie Graph.svg]]
# Tire CODE
- Trie 포인터 Array는 입력할 수 있는 문자 종류에 따라 다른데 영어 소문자 알파벳의 경우는 26개, 대문자 & 소문자는 52개로 할당하면 된다.
- Trie를 생성할 때 Trie 포인터 Array의 값을 0으로 초기화하고 Trie를 제거할 때도 모든 Trie 포인터를 Delete 해야한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, m;
string s;

struct Trie {
    Trie *next[26];
    bool finish;
    
    Trie() {
        memset(next, 0, sizeof(next));
        finish = false;
    }
    
    ~Trie() {
        for ( int i = 0; i < 26; i++ ) delete next[i];
    }
    
    void insert(const char *value) {
        if ( *value == '\0' ) finish = true;
        else {
            int idx = *value - 'a';
            if ( !next[idx] ) next[idx] = new Trie();
            next[idx]->insert(value+1);
        }
    }
    
    bool search(const char *value) {
        if ( *value == '\0' ) return finish;
        int idx = *value - 'a';
        if ( !next[idx] ) return false;
        return next[idx]->search(value+1);
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    Trie *root = new Trie();
    
    cin >> n >> m;
    for ( int i = 0; i < n; i++ ) {
        cin >> s;
        root->insert(s.c_str());
    }
    for ( int i = 0; i < m; i++ ) {
        cin >> s;
        if ( root->search(s.c_str()) ) cout << "YES\n";
        else cout << "NO\n";
    }
    return 0;
}
```
##### ❓ 예제 Input
	5 3
	human
	android
	ant
	honggildong
	apple
	ant
	app
	honggildong
##### ⭐ 예제 Output
	YES
	NO
	YES
# Tire 응용문제
### 📑[5670 - 휴대폰 자판](https://www.acmicpc.net/problem/5670)
#### 🔓 KeyPoint
- 문자열들이 주어질 때 자동 완성이 아닌 직접 치는 횟수가 평균 얼마인지 계산하는 문제이다.
- 자동 완성의 조건은 Trie 구조로 나타냈을 때 Tire가 문자열의 마지막이 아니고 자식이 1개 일 때이다.
- 자동 완성이 아니면 최소 한번은 타자를 처야하기 때문에 sum(타자 치는 횟수)에 + 1를 한다.
- 해당 Trie가 마지막 문장이라면 지금까지 그 문장에 도달하기 위해 친 타자 횟수를 최종 결과 값에 더한다.
- root에 이어진 Trie가 1개 밖에 없다면 굳이 버튼을 누르지 않아도 자동 완성이 되기 때문에 Count_Sum Parameter에 0을 넣고 1개 보다 많다면 입력을 한번은 해야 하기 때문에 Count_Sum Parameter에 1를 넣는다.
- 최종으로 구한 타자 횟수에 문자열을 나누면 평균 타자 횟수가 나오게 된다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int n, result = 0;

struct TRIE {
  
    TRIE *next[26];
    int size;
    bool finish;
  
    TRIE() {
        memset(next, 0, sizeof(next));
        finish = false;
        size = 0;
    }
    
    ~TRIE() {
        for ( int i = 0; i < 26; i++ ) {
            if ( next[i] ) delete next[i]; 
        }
    }
    
    void insert(char *value) {
        if ( *value == '\0' ) finish = true;
        else {
            int idx = *value - 'a';
            if ( !next[idx] ) {
                size++;
                next[idx] = new TRIE();
            }
            next[idx]->insert(value + 1);
        }
    }
    
    void count_Size(int sum) {
        
        if ( finish ) result += sum;
        
        if ( size > 1 || ( size != 0 && finish) ) sum++;
        for ( int i = 0; i < 26; i++ ) {
            if ( next[i] ) next[i]->count_Size(sum);
        }
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    
    while ( cin >> n ) {
        TRIE *root = new TRIE;
        
        for ( int i = 0; i < n; i++ ) {
            char s[81];
            cin >> s;
            root->insert(s);
        }
        
        if ( root->size > 1 ) root->count_Size(0);
        else root->count_Size(1);
        
        printf("%.2f\n", result / (float)n);
        result = 0;
        delete root;  
    }

    return 0;
}
```
