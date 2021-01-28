#include <bits/stdc++.h>
using namespace std;
int main()
{
    int a, b;
    cin >> a >> b;
    int cnt = 0;
    int cnt_final = 0;
    for (int i = a; i <= b; i++)
    {
        for (int j = 1; j <= i; j++)
        {
            if (i % j == 0)
                cnt++;
        }
        if (cnt % 2 == 1)
            cnt_final++;
        cnt = 0;
    }
    cout << cnt_final;
    return 0;
}