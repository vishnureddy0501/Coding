Prime factors of n
------------------
The version below is O(n) (loop runs till n). Optimized O(sqrt(n)) version is at the bottom.

vector<int> getPrimeFactors(int n){ 
    vector<int> primeFactors; 
    
    for(int i = 2; i <= n; i++){
        if(n % i == 0){
            primeFactors.push_back(i);
        }
        // Continue dividing n by i
        // until it's no longer divisible
        while(n % i == 0){
            n = n / i;
        }
    }
    return primeFactors; 
}
                                
                            

Optimized O(sqrt(n)):
---------------------
After dividing out every factor <= sqrt(n), whatever is left (if > 1) is itself a prime.

vector<int> getPrimeFactors(int n) {
    vector<int> primeFactors;
    for (int i = 2; (long long)i * i <= n; i++) {
        if (n % i == 0) {
            primeFactors.push_back(i);
            while (n % i == 0) n /= i;
        }
    }
    if (n > 1) primeFactors.push_back(n);
    return primeFactors;
}

Many queries? Precompute smallest prime factor (spf) with a sieve, then factorize in O(log n).
(see 06-Resources.md)
