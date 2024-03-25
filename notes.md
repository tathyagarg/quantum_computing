1. Let M be the number we are factoring.
2. Pick a < M. If a and M are not coprime, use Euclid's algorithm
3. Let g(x) = a^x (mod M) for x < M
4. Pick n such that M^2 <= 2^n < 2M^2, let N = 2^n
5. Apply U_g on |phi_0> = (1/root N) * sum over x in naturals of |x>, to get |phi_1> = U|phi_0> = (1/root N) * sum over x in naturals of |x,g(x)>
6. Let Z = root(length({ x for g(x) = g* })), g(x) collapses into g*
7. Also, let f(x) = 1 if g(x) = g*, 0 otherwise
8. After measuring,|phi_2> = ((1/Z) * sum over x in naturals of f(x)|x>) * |g*>
9. Apply QFT to get |phi_3> = U_QFT ((1/Z) * sum over x in naturals of f(x)|x>) = (1/Z) * (sum over x{hat} of f{hat}(x{hat})|x{hat}>) and |g*> has been omitted
10. If r divides N, all non-zero components of f{hat} will be at multiples of N/r
11. Otherwise, the amplitudes will be concentrated near |kN/r>
12. Measure the state (1/Z) * (sum over x{hat} in naturals of f{hat}(x{hat})|x{hat}>)
12. If r | N, nu = |kN/r> for k in Naturals => k/r = nu/N
13. Otherwise, we can make a guess by using continued fraction expansion.