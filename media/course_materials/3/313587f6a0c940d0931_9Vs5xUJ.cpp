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
    ll y,x; cin>>y>>x;
    ll ans;
    if(y>x){
        if(y&1){
            ans = (y-1)*(y-1)+x;
        }
        else{
            ans = y*y-x+1;
        }
    }
    else{
        if(x&1){
            ans = x*x-y+1;
        }
        else{
            ans = (x-1)*(x-1)+y;
        }
    }

    cout<<ans<<"\n";

}

int main() {

    ios::sync_with_stdio(0);
    cin.tie(0);
    ll t;
    cin>>t;
    while(t--){
        solve();
    }
}