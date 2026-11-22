/*
 * Exact pure-uint64 modular sparse-to-echelon rank engine over F_p (p <= 65535, p prime).
 * Fully hardened against invalid inputs, memory overflows, and out-of-bounds CSR indexing.
 *
 * MEMORY MODEL:
 * - Input is sparse in CSR format (row_ptr, col_idx, vals) with explicit length 'nnz'.
 * - Echelon basis U is stored in a DENSE ncols x ncols uint64_t matrix.
 *   Memory requirement for U: ncols^2 * sizeof(uint64_t) bytes.
 *   For ncols = 12,870, this requires ~1.325 GB RAM.
 */
#include <stdint.h>
#include <stdlib.h>

static int is_prime_uint16(uint64_t p) {
    if (p < 2) return 0;
    if (p == 2 || p == 3) return 1;
    if ((p % 2) == 0 || (p % 3) == 0) return 0;
    for (uint64_t d = 5; d * d <= p; d += 6) {
        if ((p % d) == 0 || (p % (d + 2)) == 0) return 0;
    }
    return 1;
}

static uint64_t mod_pow(uint64_t a, uint64_t e, uint64_t p) {
    uint64_t r = 1;
    a %= p;
    while (e) {
        if (e & 1) r = (r * a) % p;
        a = (a * a) % p;
        e >>= 1;
    }
    return r;
}

int64_t exact_csr_rank_mod_p(
    const int64_t *row_ptr,
    const int64_t *col_idx,
    const int64_t *vals,
    int64_t nrows,
    int64_t ncols,
    int64_t nnz,
    int64_t p
) {
    /* 1. Strict Contract & Precondition Checks */
    if (p <= 1 || p > 65535) return -1;
    if (!is_prime_uint16((uint64_t)p)) return -2; /* Fermat inversion requires prime modulus */
    if (nrows < 0 || ncols < 0 || nnz < 0) return -3;
    if (!row_ptr) return -4;
    if (nnz > 0 && (!col_idx || !vals)) return -4;

    /* Base case: Empty matrix contract */
    if (nrows == 0 || ncols == 0) {
        if (nnz != 0 || row_ptr[0] != 0) return -5;
        return 0;
    }

    /* 2. CSR Index and Monotonicity Validation */
    if (row_ptr[0] != 0) return -5;
    for (int64_t r = 0; r < nrows; r++) {
        if (row_ptr[r] < 0 || row_ptr[r] > row_ptr[r + 1] || row_ptr[r + 1] > nnz) {
            return -5;
        }
    }
    if (row_ptr[nrows] != nnz) return -5;

    /* 3. Strict Size_t Overflow Checks for Dynamic Allocations */
    size_t sz_ncols = (size_t)ncols;
    if ((int64_t)sz_ncols != ncols) return -6; /* Safe cast to size_t */

    if (sz_ncols > SIZE_MAX / sizeof(int64_t)) return -7;
    if (sz_ncols > SIZE_MAX / sizeof(uint64_t)) return -7;
    if (sz_ncols > 0 && sz_ncols > SIZE_MAX / sz_ncols) return -7;
    size_t u_size = sz_ncols * sz_ncols;
    if (u_size > SIZE_MAX / sizeof(uint64_t)) return -7;

    /* 4. Memory Allocations */
    int64_t *piv_row_idx = (int64_t *)malloc(sz_ncols * sizeof(int64_t));
    if (!piv_row_idx) return -10;
    for (size_t c = 0; c < sz_ncols; c++) piv_row_idx[c] = -1;

    uint64_t *U = (uint64_t *)calloc(u_size, sizeof(uint64_t));
    int64_t *u_end = (int64_t *)calloc(sz_ncols, sizeof(int64_t));
    uint64_t *cur = (uint64_t *)calloc(sz_ncols, sizeof(uint64_t));
    if (!U || !u_end || !cur) {
        free(piv_row_idx); free(U); free(u_end); free(cur);
        return -10;
    }

    uint64_t P = (uint64_t)p;
    int64_t rank = 0;

    /* 5. Row Reduction via Dense Echelon Storage */
    for (int64_t r = 0; r < nrows; r++) {
        int64_t start = row_ptr[r];
        int64_t end = row_ptr[r + 1];
        if (start >= end) continue;

        int64_t first = ncols, last = -1;
        for (int64_t idx = start; idx < end; idx++) {
            int64_t c = col_idx[idx];
            if (c < 0 || c >= ncols) {
                /* Column index out of bounds */
                free(piv_row_idx); free(U); free(u_end); free(cur);
                return -8;
            }
            int64_t v = vals[idx] % p;
            if (v < 0) v += p;
            if (v != 0) {
                cur[c] = (cur[c] + (uint64_t)v) % P;
                if (c < first) first = c;
                if (c > last) last = c;
            }
        }
        if (last < 0) continue;
        while (first <= last && cur[first] == 0) first++;
        if (first > last) continue;

        while (first <= last && piv_row_idx[first] >= 0) {
            uint64_t coeff = cur[first];
            int64_t pr = piv_row_idx[first];
            const uint64_t *prow = U + (size_t)pr * sz_ncols;
            int64_t pend = u_end[pr];
            if (pend > last) last = pend;
            uint64_t neg_c = P - coeff;
            cur[first] = 0;
            for (int64_t c = first + 1; c <= pend; c++) {
                uint64_t pv = prow[c];
                if (pv) {
                    cur[c] = (cur[c] + neg_c * pv) % P;
                }
            }
            int64_t nf = first + 1;
            while (nf <= last && cur[nf] == 0) nf++;
            first = nf;
        }

        if (first <= last) {
            uint64_t inv = mod_pow(cur[first], P - 2, P);
            uint64_t *dst = U + (size_t)rank * sz_ncols;
            int64_t new_last = first;
            dst[first] = 1;
            cur[first] = 0;
            for (int64_t c = first + 1; c <= last; c++) {
                uint64_t cv = cur[c];
                if (cv) {
                    cur[c] = 0;
                    uint64_t val = (cv * inv) % P;
                    if (val) {
                        dst[c] = val;
                        new_last = c;
                    }
                }
            }
            u_end[rank] = new_last;
            piv_row_idx[first] = rank;
            rank++;
            if (rank == ncols) break;
        }
    }

    free(piv_row_idx);
    free(U);
    free(u_end);
    free(cur);
    return rank;
}
