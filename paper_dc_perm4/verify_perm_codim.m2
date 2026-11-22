-- Standalone Macaulay2 verification script (NO built-in 'permanent' call).
-- Status: [KESIN HESAP - HENUZ CALISTIRILMADI] (M2 not installed on local audit host).
-- Run with: M2 --script verify_perm_codim.m2

explicitPerm = (M) -> (
    n := numRows M;
    sum(permutations toList(0..n-1), s -> product(0..n-1, i -> M_(i, s#i)))
);

-- 1. Positive control A: perm_3 => codim Sing(V(perm_3)) == 6 over F_32749
R3 = (ZZ/32749)[x_0..x_8];
X3 = genericMatrix(R3, 3, 3);
J3 = ideal diff(vars R3, explicitPerm X3);
c3 = codim J3;
print("Positive control perm_3 codim(Sing) = " | toString c3);
assert(c3 == 6);

-- 2. Positive control B: det_4 => codim Sing(V(det_4)) == 4 over F_32749 (catches 4x4 sign/indexing errors)
R4d = (ZZ/32749)[x_0..x_15];
X4d = genericMatrix(R4d, 4, 4);
J4d = ideal diff(vars R4d, det X4d);
cd4 = codim J4d;
print("Positive control det_4 codim(Sing) = " | toString cd4);
assert(cd4 == 4);

-- 3. Fixed integer subspaces M_L8 (16x8) and M_L9 (16x9) from np.random.default_rng(2026).integers(-2, 3, ...)
M8 = matrix {
    { 2, -2, -2,  1, -1,  0, -2, -1},
    { 1, -1,  2,  1,  1,  2,  1, -2},
    { 2,  1, -2, -1, -2,  2,  1,  2},
    {-1,  1,  1,  1, -2,  0,  1,  2},
    { 1,  0,  0, -1, -2, -1, -2, -1},
    { 2,  0, -2,  0, -1,  1,  2, -2},
    { 0,  0,  2, -1, -2, -2,  0,  0},
    {-1,  0,  1, -1,  2, -1,  2,  2},
    { 2,  1,  0,  1, -1, -1,  0,  2},
    { 1,  0,  0,  0,  0,  2, -2, -1},
    { 0,  1,  0, -1, -2, -1, -2,  1},
    { 0, -1,  0,  0,  0,  0,  1, -2},
    {-2,  1,  2,  0,  0,  1, -2, -1},
    {-1,  0,  1,  0,  2,  0, -2,  1},
    { 1,  0,  2,  0,  1, -2, -2,  1},
    { 2,  0,  1, -1,  1,  0, -1, -2}
};

M9 = matrix {
    { 2, -2, -2,  1, -1,  0, -2, -1,  1},
    {-1,  2,  1,  1,  2,  1, -2,  2,  1},
    {-2, -1, -2,  2,  1,  2, -1,  1,  1},
    { 1, -2,  0,  1,  2,  1,  0,  0, -1},
    {-2, -1, -2, -1,  2,  0, -2,  0, -1},
    { 1,  2, -2,  0,  0,  2, -1, -2, -2},
    { 0,  0, -1,  0,  1, -1,  2, -1,  2},
    { 2,  2,  1,  0,  1, -1, -1,  0,  2},
    { 1,  0,  0,  0,  0,  2, -2, -1,  0},
    { 1,  0, -1, -2, -1, -2,  1,  0, -1},
    { 0,  0,  0,  0,  1, -2, -2,  1,  2},
    { 0,  0,  1, -2, -1, -1,  0,  1,  0},
    { 2,  0, -2,  1,  1,  0,  2,  0,  1},
    {-2, -2,  1,  2,  0,  1, -1,  1,  0},
    {-1, -2, -2,  2,  0,  2, -1, -2, -1},
    {-1,  1,  1,  1, -1, -1,  0,  1,  0}
};

-- 4. L_8 positive certificate (primes 32749 & 65521) + D=6..9 Hilbert profile matching IMSC [132, 32, 8, 0]
scan({32749, 65521}, p -> (
    R4 = (ZZ/p)[x_0..x_15];
    X4 = genericMatrix(R4, 4, 4);
    J4 = ideal diff(vars R4, explicitPerm X4);
    assert(rank sub(M8, ZZ/p) == 8);
    S8 = (ZZ/p)[t_0..t_7];
    f8 = map(S8, R4, flatten entries(sub(M8, S8) * transpose vars S8));
    I8 = f8 J4;
    c8 = codim I8;
    hf6 = hilbertFunction(6, S8/I8);
    hf7 = hilbertFunction(7, S8/I8);
    hf8 = hilbertFunction(8, S8/I8);
    hf9 = hilbertFunction(9, S8/I8);
    print("L_8 (p=" | toString p | "): codim=" | toString c8 | ", hf(6..9)=" | toString {hf6, hf7, hf8, hf9});
    assert(c8 == 8 and hf6 == 132 and hf7 == 32 and hf8 == 8 and hf9 == 0);
));

-- 5. Negative control: L_9 over F_32749 (must keep dim >= 1 and positive coranks [753, 580] at D=6,7)
R4n = (ZZ/32749)[x_0..x_15];
X4n = genericMatrix(R4n, 4, 4);
J4n = ideal diff(vars R4n, explicitPerm X4n);
assert(rank sub(M9, ZZ/32749) == 9);
S9 = (ZZ/32749)[t_0..t_8];
f9 = map(S9, R4n, flatten entries(sub(M9, S9) * transpose vars S9));
I9 = f9 J4n;
d9 = dim I9;
hf9_6 = hilbertFunction(6, S9/I9);
hf9_7 = hilbertFunction(7, S9/I9);
print("L_9 (p=32749): dim=" | toString d9 | ", hf(6..7)=" | toString {hf9_6, hf9_7});
assert(d9 >= 1 and hf9_6 == 753 and hf9_7 == 580);

-- 6. Optional ambient check (commented due to 16-variable GB cost; uncomment if desired):
-- assert(codim ideal diff(vars R4n, explicitPerm X4n) == 8);

print("ALL MACAULAY2 CHECKS PASSED.");
