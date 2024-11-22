#include<bits/stdc++.h>
using namespace std;
int main () {
    set<int> s;
    s.insert(10);
    s.insert(20);
    if (s.find(10) != s.end()) {
        cout<<"found 10"<<endl;
    }
    for(auto &value: s) {
        cout<<value<<endl;
    }
    return 0;
}
