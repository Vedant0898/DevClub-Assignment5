#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

void print_vector(vector<int> v){
    for (auto ele : v)
    {
        cout<<ele<<" ";
    }
    cout<<"\n";
    
}

void solve(){
    ll n; cin>>n;
    while(n!=1){
        cout<<n<<" ";
        if(n&1){
            n=3*n+1;
        }
        else{
            n=n/2;
        }
    }
    cout<<n;
}

int main() {

    ios::sync_with_stdio(0);
    cin.tie(0);
    solve();
    
}