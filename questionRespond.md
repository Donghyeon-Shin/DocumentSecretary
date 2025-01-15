```cpp
#include <bits/stdc++.h>
#define maxLen 100001

using namespace std;

int n, k, ettCnt = 0, s[maxLen], e[maxLen], singers[maxLen], subTreeRoot[maxLen];
long long j, queryWeight[maxLen], fenwickTree[maxLen];
pair<int,int> queryRange[maxLen];
vector<int> tree[maxLen], songsBasedSinger[maxLen], queryMidValue[maxLen];
vector<pair<long long, int>> query;

void fenwickTree_Update(int idx, long long val) {
    while ( idx <= n ) {
        fenwickTree[idx] += val;
        idx += (idx & -idx);
    }
}

long long fenwickTree_Sum(int idx) {
    long long result = 0;
    while ( idx > 0 ) {
        result += fenwickTree[idx];
        idx -= (idx & -idx);
    }
    return result;
}

void ett(int node) {
    s[node] = ++ettCnt;
    for ( auto nNode : tree[node] ) {
        if ( s[nNode] == 0 ) ett(nNode);
    }
    e[node] = ettCnt;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    cin >> n >> k >> j;
    for ( int i = 2; i <= n; i++ ) {
        int root;
        cin >> root;
        tree[root].push_back(i);
    }
    
    ett(1);
    
    for ( int i = 1; i <= n; i++ ) {
        cin >> singers[i];
        songsBasedSinger[singers[i]].push_back(i);
    }
    
    query.push_back({-1, -1});
    for ( int i = 1; i <= k; i++ ) {
        long long dateTime;
        cin >> dateTime >> subTreeRoot[i] >> queryWeight[i];
        query.push_back({dateTime, i});
    }
    sort(query.begin(), query.end());
    
    for ( int i = 1; i <= k; i++ ) {
        queryRange[i].first = ((int)songsBasedSinger[i].size() == 0 ) ? k+1 : 1;
        queryRange[i].second = k+1;
    }
    
    while ( 1 ) {
        bool flag = false;
        for ( int i = 1; i <= k; i++ ) queryMidValue[i].clear();
        memset(fenwickTree, 0, sizeof(fenwickTree));
        
        for ( int i = 1; i <= k; i++ ) {
            int l = queryRange[i].first, r = queryRange[i].second;
            if ( l < r ) {
                flag = true;
                int mid = (l + r) / 2;
                queryMidValue[mid].push_back(i);
            }
        }
        
        if ( !flag ) break;
        
        for ( int i = 1; i <= k; i++ ) {
            int queryIdx = query[i].second;
            int root = subTreeRoot[queryIdx];
            long long weight = queryWeight[queryIdx];
            
            long long avgWeight = weight / (e[root] - s[root] + 1);
            fenwickTree_Update(s[root], avgWeight);
            fenwickTree_Update(e[root] + 1, -avgWeight);
            
            for ( auto singerIdx : queryMidValue[i] ) {
                long long result = 0;
                int songsCnt = (int)songsBasedSinger[singerIdx].size();
                for ( auto song : songsBasedSinger[singerIdx] ) {
                    result += fenwickTree_Sum(s[song]);
                    if ( result > j * songsCnt ) break;
                }
                if ( result > j * songsCnt ) queryRange[singerIdx].second = i;
                else queryRange[singerIdx].first = i+1;
            }
        }
    }
    
    for ( int i = 1; i <= n; i++ ) {
        int queryIdx = queryRange[singers[i]].first;
        if ( queryIdx == k+1 ) cout << -1 << '\n';
        else cout << query[queryIdx].first << '\n';
    }
    return 0;
}
```