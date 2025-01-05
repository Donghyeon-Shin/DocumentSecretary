# Concept
- '정렬되어 있는' 리스트에서 탐색 범위를 절반씩 줄여가며 탐색하는 방법이다.
- 기초적이고 강력한 알고리즘으로 탐색을 필요로 하는 다양한 상황에서 사용된다.
- 리스트의 길이가 n이라고 할 때 시간 복잡도는 O(logn)이다.
# Binary Search 원리
- start(탐색 시작 위치)와 end(탐색 끝 위치), Target(탐색 값)을 Parameter로 가진다.
- start와 end의 중간 지점 mid = (start + end) / 2로 정의하고 이 위치에 있는 값보다 Target의 값이 작다면 end = mid - 1로 Target의 값이 크다면 start = mid + 1로 이동하면서 탐색한다.
- Start > end면 탐색을 종료한다.
#### 🖼️그림으로 이해하기
![[Binary Search Flowchart.svg]]
# Binary Search CODE
- 반복문으로 구현할 수도 있고 재귀로도 구현할 수 있다. 둘 다 큰 상관없기 때문에 두 방법 중 적절한 것을 사용하면 된다.
- Binary Search를 응용하여 Cpp에는 Lower_Bound, Upper_Bound라는 내장 함수가 존재한다.
- Lower_Bound(vector.begin(), vector.end(), target) : target보다 같거나 큰 숫자가 배열 몇 번째에 처음으로 등장하는지 iterator형태로 Return
- Upper_Bound(vector.begin(), vector.end(), target) : target보다 같거나 작은 숫자가 배열 몇 번째에 처음으로 등장하는지 iterator형태로 Return
#### ⌨️ Code(For Loop)
- FOR문으로 구현
```cpp
#include <bits/stdc++.h>

using namespace std;

int main() {
	ios_base::sync_with_stdio(false);
	cin.tie(NULL); cout.tie(NULL);
	
	int arr[10] = {1, 5, 9, 11, 11, 13, 16, 18, 21, 24};
	
	int start, end, mid, target;
	bool flag = false;
	cin >> start >> end >> target;
	
	while ( start <= end ) {
		mid = (start + end) / 2;
		cout << "start : " << arr[start] << ' ' << "mid : " << arr[mid] << ' ' << "end : " << arr[end] << '\n';
		
		if ( target == arr[mid] ) {
			flag = true;
			break;
		} else if ( target < arr[mid] ) end = mid - 1;
		else start = mid + 1;
	}
	
	if ( flag ) cout << mid;
	else cout << "Couldn't Found";
	return 0;
}
```
#### ⌨️ Code(Recursion)
- 재귀 함수로 구현
```cpp
#include <bits/stdc++.h>

using namespace std;

int arr[10] = {1, 5, 9, 11, 11, 13, 16, 18, 21, 24};

int binary_Search(int start, int end, int target) {
	if ( start > end ) return -1;
	
	int mid = (start + end) / 2;
	cout << "start : " << arr[start] << ' ' << "mid : " << arr[mid] << ' ' << "end : " << arr[end] << '\n';
	
	if ( target == arr[mid] ) return mid;
	else if ( target < arr[mid] ) return binary_Search(start, mid-1, target);
	else return binary_Search(mid+1, end, target);
	
	return -1;
}

int main() {
	ios_base::sync_with_stdio(false);
	cin.tie(NULL); cout.tie(NULL);
	
	int start, end, mid, target;
	bool flag = false;
	cin >> start >> end >> target;
	
	cout << binary_Search(start, end, target);
	return 0;
}
```
##### ❓ 예제 Input
	0 9 13
##### ⭐ 예제 Output
	start : 1 mid : 11 end : 24
	start : 13 mid : 18 end : 24
	start : 13 mid : 13 end : 24
	5
# Binary Search 응용문제
### 📑[1920 - 수 찾기](https://www.acmicpc.net/problem/1920)
#### 🔓 KeyPoint
- Binary Search를 이용하는 대표적인 문제이다.
- 주어진 Input 값이 정렬되어 있지 않고 Binary Search는 정렬된 배열 안에서만 작동한다는 것을 유의하며 문제를 풀어야 한다.
#### ⌨️ Code
```cpp
#include <bits/stdc++.h>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    int n, m;
    cin >> n;
    vector<int> arr;
    for ( int i = 0; i < n; i++ ) {
        int num;
        cin >> num;
        arr.push_back(num);
    }
    
    sort(arr.begin(), arr.end());
    
    cin >> m;
    for ( int i = 0; i < m; i++ ) {
        bool flag = false;
        int start = 0, end = n-1, target;
        
        cin >> target;
        while ( start <= end ) {
            int mid = (start + end) / 2;
            if ( target == arr[mid] ) {
                flag = true;
                break;
            } else if ( target < arr[mid] ) end = mid - 1;
            else start = mid + 1;
        }
            
        if ( flag ) cout << 1 << '\n';
        else cout << 0 << '\n';
    }
    return 0;
}
```