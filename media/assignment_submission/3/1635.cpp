#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef long double ld;
typedef vector<int> vi;
typedef vector<ll> vll;
typedef pair<int,int> pii;

#define pb push_back
#define mp make_pair
#define all(x) (x).begin(), (x).end()
#define rall(x) (x).rbegin(), (x).rend() 
#define sz(x) (int) (x).size()
#define sp cout<<" "
#define nl cout<<"\n"
#define nlf cout<<endl

const int MAX_N = 1e6+100;
int INF = 1e9;
ll MOD = 1e9+7;
ld EPS = 1e-9;


template <typename T>
void print_vector(vector<T> v){
    for (auto ele : v)
    {
        cout<<ele<<" ";
    }
    cout<<"\n";
    
}


ll fast_pow(ll n, ll m){
    //returns n^m
    if(m==0){
        return 1ll;
    }
    if(m%2==0){
        ll val = fast_pow(n,m/2)%MOD;
        val = (val*val)%MOD;
        return val;
    }
    else{
        ll val = fast_pow(n,m-1)%MOD;
        val = (n*val)%MOD;
        return val;
    }
}


ll inv(ll x){
    return fast_pow(x,MOD-2);
}

ll gcd(ll a, ll b)
{
    if (a == 0)
        return b;
    return gcd(b % a, a);
}

ll fact(ll n){
    ll ans = 1;
    for (int i = 2; i <= n; i++)
    {
        ans*=i;
        ans%=MOD;
    }
    return ans;
}

bool is_prime(ll n){
    for (int i = 2; i < sqrt(n); i++)
    {
        if(n%i==0){
            return false;
        }
    }
    return true;
}

int dp[MAX_N];
bool ready[MAX_N];

int count(int x, vi & denom){
    if(x<0){
        return 0;
    }
    if(x==0) return 1;
    if(ready[x]){
        return dp[x];
    }
    int best = 0;

    for (auto c : denom)
    {
        if(x<c){
            break;
        }
        if(x==c){
            best++;
            continue;
        }
        best +=count(x-c,denom);
        best%=MOD;
    }
    ready[x] = true;
    dp[x] = best;
    
    return best;

}


void solve(){
    int n,x;scanf("%d %d",&n, &x);
    vi denom(n);
    for (int i = 0; i < n; i++)
    {
        scanf("%d",&denom[i]);
        
    }
    sort(all(denom));

    // vi dp(x+100,0);
    int ans = count(x, denom);
    
    // cout<<ans%MOD;
    printf("%d",ans%MOD);

}

int main() {

    ios::sync_with_stdio(0);
    cin.tie(0);
    solve();
    
}