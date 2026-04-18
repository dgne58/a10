---
title: "Low-rank approximation - Wikipedia"
source: "https://en.wikipedia.org/wiki/Low-rank_approximation"
author:
  - "[[Contributors to Wikimedia projects]]"
published: 2012-01-09
created: 2026-04-13
description:
tags:
  - "clippings"
---
In mathematics, **low-rank approximation** refers to the process of approximating a given [matrix](https://en.wikipedia.org/wiki/Matrix_\(mathematics\) "Matrix (mathematics)") by a matrix of lower [rank](https://en.wikipedia.org/wiki/Rank_\(linear_algebra\) "Rank (linear algebra)"). More precisely, it is a [minimization](https://en.wikipedia.org/wiki/Mathematical_optimization "Mathematical optimization") problem, in which the [cost function](https://en.wikipedia.org/wiki/Loss_function "Loss function") measures the fit between a given matrix (the data) and an approximating matrix (the optimization variable), subject to a constraint that the approximating matrix has reduced rank. The problem is used for [mathematical modeling](https://en.wikipedia.org/wiki/Mathematical_model "Mathematical model") and [data compression](https://en.wikipedia.org/wiki/Data_compression "Data compression"). The rank constraint is related to a constraint on the complexity of a model that fits the data. In applications, often there are other constraints on the approximating matrix apart from the rank constraint, e.g., [non-negativity](https://en.wikipedia.org/wiki/Nonnegative_matrix_factorization "Nonnegative matrix factorization") and [Hankel structure](https://en.wikipedia.org/wiki/Hankel_matrix "Hankel matrix").

Low-rank approximation is closely related to numerous other techniques, including [principal component analysis](https://en.wikipedia.org/wiki/Principal_component_analysis "Principal component analysis"), [factor analysis](https://en.wikipedia.org/wiki/Factor_analysis "Factor analysis"), [total least squares](https://en.wikipedia.org/wiki/Total_least_squares "Total least squares"), [latent semantic analysis](https://en.wikipedia.org/wiki/Latent_semantic_analysis "Latent semantic analysis"), [orthogonal regression](https://en.wikipedia.org/wiki/Orthogonal_regression "Orthogonal regression"), and [dynamic mode decomposition](https://en.wikipedia.org/wiki/Dynamic_mode_decomposition "Dynamic mode decomposition").

## Definition

Given

- structure specification ${\displaystyle {\mathcal {S}}:\mathbb {R} ^{n_{p}}\to \mathbb {R} ^{m\times n}}$,
- vector of structure parameters ${\displaystyle p\in \mathbb {R} ^{n_{p}}}$,
- [norm](https://en.wikipedia.org/wiki/Norm_\(mathematics\) "Norm (mathematics)") ${\displaystyle \|\cdot \|}$, and
- desired rank ${\displaystyle r}$,

${\displaystyle {\text{minimize}}\quad {\text{over }}{\widehat {p}}\quad \|p-{\widehat {p}}\|\quad {\text{subject to}}\quad \operatorname {rank} {\big (}{\mathcal {S}}({\widehat {p}}){\big )}\leq r.}$

## Applications

- Linear [system identification](https://en.wikipedia.org/wiki/System_identification "System identification"), in which case the approximating matrix is [Hankel structured](https://en.wikipedia.org/wiki/Hankel_matrix "Hankel matrix").
- [Machine learning](https://en.wikipedia.org/wiki/Machine_learning "Machine learning"), in which case the approximating matrix is nonlinearly structured.
- [Recommender systems](https://en.wikipedia.org/wiki/Recommender_system "Recommender system"), in which cases the [data matrix](https://en.wikipedia.org/wiki/Data_Matrix "Data Matrix") has [missing values](https://en.wikipedia.org/wiki/Missing_values "Missing values") and the approximation is [categorical](https://en.wikipedia.org/wiki/Categorical_data "Categorical data").
- Distance [matrix completion](https://en.wikipedia.org/wiki/Matrix_completion "Matrix completion"), in which case there is a positive definiteness constraint.
- [Natural language processing](https://en.wikipedia.org/wiki/Natural_language_processing "Natural language processing"), in which case the approximation is [nonnegative](https://en.wikipedia.org/wiki/Nonnegative_matrix "Nonnegative matrix").
- [Computer algebra](https://en.wikipedia.org/wiki/Computer_algebra "Computer algebra"), in which case the approximation is [Sylvester structured](https://en.wikipedia.org/wiki/Sylvester_matrix "Sylvester matrix").
- [Matrix product states](https://en.wikipedia.org/wiki/Matrix_product_state "Matrix product state"), in which case the approximation is usually rescaled to have fixed Frobenius norm.

## Basic low-rank approximation problem

The unstructured problem with fit measured by the [Frobenius norm](https://en.wikipedia.org/wiki/Frobenius_norm "Frobenius norm"), i.e.,

${\displaystyle {\text{minimize}}\quad {\text{over }}{\widehat {D}}\quad \|D-{\widehat {D}}\|_{\text{F}}\quad {\text{subject to}}\quad \operatorname {rank} {\big (}{\widehat {D}}{\big )}\leq r}$

has an analytic solution in terms of the [singular value decomposition](https://en.wikipedia.org/wiki/Singular_value_decomposition "Singular value decomposition") of the data matrix. The result is referred to as the matrix approximation lemma or **Eckart–Young–Mirsky theorem**. This problem was originally solved by [Erhard Schmidt](https://en.wikipedia.org/wiki/Erhard_Schmidt "Erhard Schmidt") [^1] in the infinite dimensional context of integral operators (although his methods easily generalize to arbitrary compact operators on [Hilbert spaces](https://en.wikipedia.org/wiki/Hilbert_space "Hilbert space")) and later rediscovered by [C. Eckart](https://en.wikipedia.org/wiki/Carl_Eckart "Carl Eckart") and [G. Young](https://en.wikipedia.org/wiki/Gale_J._Young "Gale J. Young").[^2] [L. Mirsky](https://en.wikipedia.org/wiki/Leon_Mirsky "Leon Mirsky") generalized the result to arbitrary unitarily invariant norms.[^3] Let

${\displaystyle D=U\Sigma V^{\top }\in \mathbb {R} ^{m\times n},\quad m\geq n}$

be the singular value decomposition of ${\displaystyle D}$, where ${\displaystyle \Sigma =:\operatorname {diag} (\sigma _{1},\ldots ,\sigma _{r})}$, where ${\displaystyle r\leq \min\{m,n\}=n}$, is the ${\displaystyle m\times n}$ rectangular diagonal matrix with ${\displaystyle r}$ non-zero singular values ${\displaystyle \sigma _{1}\geq \ldots \geq \sigma _{r}>\sigma _{r+1}=\ldots =\sigma _{n}=0}$. For a given ${\displaystyle k\in \{1,\dots ,r\}}$, partition ${\displaystyle U}$, ${\displaystyle \Sigma }$, and ${\displaystyle V}$ as follows:

${\displaystyle U=:{\begin{bmatrix}U_{1}&U_{2}\end{bmatrix}},\quad \Sigma =:{\begin{bmatrix}\Sigma _{1}&0\\0&\Sigma _{2}\end{bmatrix}},\quad {\text{and}}\quad V=:{\begin{bmatrix}V_{1}&V_{2}\end{bmatrix}},}$

where ${\displaystyle U_{1}}$ is ${\displaystyle m\times k}$, ${\displaystyle \Sigma _{1}}$ is ${\displaystyle k\times k}$, and ${\displaystyle V_{1}}$ is ${\displaystyle n\times k}$. Then the rank ${\displaystyle k}$ matrix

${\displaystyle {\widehat {D}}^{*}:=U_{1}\Sigma _{1}V_{1}^{\top },}$

obtained from the truncated singular value decomposition is such that

${\displaystyle \|D-{\widehat {D}}^{*}\|_{\text{F}}=\min _{\operatorname {rank} ({\widehat {D}})\leq k}\|D-{\widehat {D}}\|_{\text{F}}={\sqrt {\sigma _{k+1}^{2}+\cdots +\sigma _{r}^{2}}}.}$

The minimizer ${\displaystyle {\widehat {D}}^{*}}$ is unique if and only if ${\displaystyle \sigma _{k}>\sigma _{k+1}}$.

## Proof of Eckart–Young–Mirsky theorem (for spectral norm)

Let ${\displaystyle A\in \mathbb {R} ^{m\times n}}$ be a real (possibly rectangular) matrix with ${\displaystyle m\leq n}$. Suppose that

${\displaystyle A=U\Sigma V^{\top }}$

is the [singular value decomposition](https://en.wikipedia.org/wiki/Singular_value_decomposition "Singular value decomposition") of ${\displaystyle A}$. Recall that ${\displaystyle U}$ and ${\displaystyle V}$ are [orthogonal](https://en.wikipedia.org/wiki/Orthogonal_matrix "Orthogonal matrix") matrices, and ${\displaystyle \Sigma }$ is an ${\displaystyle m\times n}$ [diagonal](https://en.wikipedia.org/wiki/Diagonal_matrix "Diagonal matrix") matrix with entries ${\displaystyle (\sigma _{1},\sigma _{2},\cdots ,\sigma _{m})}$ such that ${\displaystyle \sigma _{1}\geq \sigma _{2}\geq \cdots \geq \sigma _{m}\geq 0}$.

We claim that the best rank- ${\displaystyle k}$ approximation to ${\displaystyle A}$ in the spectral norm, denoted by ${\displaystyle \|\cdot \|_{2}}$, is given by

${\displaystyle A_{k}:=\sum _{i=1}^{k}\sigma _{i}u_{i}v_{i}^{\top }}$

where ${\displaystyle u_{i}}$ and ${\displaystyle v_{i}}$ denote the ${\displaystyle i}$ th column of ${\displaystyle U}$ and ${\displaystyle V}$, respectively.

First, note that we have

${\displaystyle \|A-A_{k}\|_{2}=\left\|\sum _{i=1}^{\color {red}{n}}\sigma _{i}u_{i}v_{i}^{\top }-\sum _{i=1}^{\color {red}{k}}\sigma _{i}u_{i}v_{i}^{\top }\right\|_{2}=\left\|\sum _{i=\color {red}{k+1}}^{n}\sigma _{i}u_{i}v_{i}^{\top }\right\|_{2}=\sigma _{k+1}}$

Therefore, we need to show that if ${\displaystyle B_{k}=XY^{\top }}$ where ${\displaystyle X}$ and ${\displaystyle Y}$ have ${\displaystyle k}$ columns then ${\displaystyle \|A-A_{k}\|_{2}=\sigma _{k+1}\leq \|A-B_{k}\|_{2}}$.

Since ${\displaystyle Y}$ has ${\displaystyle k}$ columns, then there must be a nontrivial [linear combination](https://en.wikipedia.org/wiki/Linear_combination "Linear combination") of the first ${\displaystyle k+1}$ columns of ${\displaystyle V}$, i.e.,

${\displaystyle w=\gamma _{1}v_{1}+\cdots +\gamma _{k+1}v_{k+1},}$

such that ${\displaystyle Y^{\top }w=0}$. [Without loss of generality](https://en.wikipedia.org/wiki/Without_loss_of_generality "Without loss of generality"), we can scale ${\displaystyle w}$ so that ${\displaystyle \|w\|_{2}=1}$ or (equivalently) ${\displaystyle \gamma _{1}^{2}+\cdots +\gamma _{k+1}^{2}=1}$. Therefore,

${\displaystyle \|A-B_{k}\|_{2}^{2}\geq \|(A-B_{k})w\|_{2}^{2}=\|Aw\|_{2}^{2}=\gamma _{1}^{2}\sigma _{1}^{2}+\cdots +\gamma _{k+1}^{2}\sigma _{k+1}^{2}\geq \sigma _{k+1}^{2}.}$

The result follows by taking the [square root](https://en.wikipedia.org/wiki/Square_root "Square root") of both sides of the above inequality.

## Proof of Eckart–Young–Mirsky theorem (for Frobenius norm)

Let ${\displaystyle A\in \mathbb {R} ^{m\times n}}$ be a real (possibly rectangular) matrix with ${\displaystyle m\leq n}$. Suppose that

${\displaystyle A=U\Sigma V^{\top }}$

is the [singular value decomposition](https://en.wikipedia.org/wiki/Singular_value_decomposition "Singular value decomposition") of ${\displaystyle A}$.

We claim that the best rank ${\displaystyle k}$ approximation to ${\displaystyle A}$ in the Frobenius norm, denoted by ${\displaystyle \|\cdot \|_{F}}$, is given by

${\displaystyle A_{k}=\sum _{i=1}^{k}\sigma _{i}u_{i}v_{i}^{\top }}$

where ${\displaystyle u_{i}}$ and ${\displaystyle v_{i}}$ denote the ${\displaystyle i}$ th column of ${\displaystyle U}$ and ${\displaystyle V}$, respectively.

First, note that we have

${\displaystyle \|A-A_{k}\|_{F}^{2}=\left\|\sum _{i=k+1}^{n}\sigma _{i}u_{i}v_{i}^{\top }\right\|_{F}^{2}=\sum _{i=k+1}^{n}\sigma _{i}^{2}}$

Therefore, we need to show that if ${\displaystyle B_{k}=XY^{\top }}$ where ${\displaystyle X}$ and ${\displaystyle Y}$ have ${\displaystyle k}$ columns then

${\displaystyle \|A-A_{k}\|_{F}^{2}=\sum _{i=k+1}^{n}\sigma _{i}^{2}\leq \|A-B_{k}\|_{F}^{2}.}$

By the [triangle inequality](https://en.wikipedia.org/wiki/Triangle_inequality "Triangle inequality") with the spectral norm, if ${\displaystyle A=A'+A''}$ then ${\displaystyle \sigma _{1}(A)\leq \sigma _{1}(A')+\sigma _{1}(A'')}$. Suppose ${\displaystyle A'_{k}}$ and ${\displaystyle A''_{k}}$ respectively denote the rank ${\displaystyle k}$ approximation to ${\displaystyle A'}$ and ${\displaystyle A''}$ by SVD method described above. Then, for any ${\displaystyle i,j\geq 1}$

${\displaystyle {\begin{aligned}\sigma _{i}(A')+\sigma _{j}(A'')&=\sigma _{1}(A'-A'_{i-1})+\sigma _{1}(A''-A''_{j-1})\\&\geq \sigma _{1}(A-A'_{i-1}-A''_{j-1})\\&\geq \sigma _{1}(A-A_{i+j-2})\qquad ({\text{since }}{\rm {rank}}(A'_{i-1}+A''_{j-1})\leq i+j-2))\\&=\sigma _{i+j-1}(A).\end{aligned}}}$

Since ${\displaystyle \sigma _{k+1}(B_{k})=0}$, when ${\displaystyle A'=A-B_{k}}$ and ${\displaystyle A''=B_{k}}$ we conclude that for ${\displaystyle i\geq 1,j=k+1}$

${\displaystyle \sigma _{i}(A-B_{k})\geq \sigma _{k+i}(A).}$

Therefore,

${\displaystyle \|A-B_{k}\|_{F}^{2}=\sum _{i=1}^{n}\sigma _{i}(A-B_{k})^{2}\geq \sum _{i=k+1}^{n}\sigma _{i}(A)^{2}=\|A-A_{k}\|_{F}^{2},}$

as required.

## Weighted low-rank approximation problems

The Frobenius norm weights uniformly all elements of the approximation error ${\displaystyle D-{\widehat {D}}}$. Prior knowledge about distribution of the errors can be taken into account by considering the weighted low-rank approximation problem

${\displaystyle {\text{minimize}}\quad {\text{over }}{\widehat {D}}\quad \operatorname {vec} (D-{\widehat {D}})^{\top }W\operatorname {vec} (D-{\widehat {D}})\quad {\text{subject to}}\quad \operatorname {rank} ({\widehat {D}})\leq r,}$

where ${\displaystyle {\text{vec}}(A)}$ [vectorizes](https://en.wikipedia.org/wiki/Vectorization_\(mathematics\) "Vectorization (mathematics)") the matrix ${\displaystyle A}$ column wise and ${\displaystyle W}$ is a given positive (semi)definite weight matrix.

The general weighted low-rank approximation problem does not admit an analytic solution in terms of the singular value decomposition and is solved by local optimization methods, which provide no guarantee that a globally optimal solution is found.

In case of uncorrelated weights, weighted low-rank approximation problem also can be formulated in this way:[^4] [^5] for a non-negative matrix ${\displaystyle W}$ and a matrix ${\displaystyle A}$ we want to minimize ${\displaystyle \sum _{i,j}(W_{i,j}(A_{i,j}-B_{i,j}))^{2}}$ over matrices, ${\displaystyle B}$, of rank at most ${\displaystyle r}$.

## Entry-wise Lp low-rank approximation problems

Let ${\displaystyle \|A\|_{p}=\left(\sum _{i,j}|A_{i,j}^{p}|\right)^{1/p}}$. For ${\displaystyle p=2}$, the fastest algorithm runs in ${\displaystyle nnz(A)+n\cdot poly(k/\epsilon )}$ time.[^6] [^7] One of the important ideas been used is called Oblivious Subspace Embedding (OSE), it is first proposed by Sarlos.[^8]

For ${\displaystyle p=1}$, it is known that this entry-wise L1 norm is more robust than the Frobenius norm in the presence of outliers and is indicated in models where Gaussian assumptions on the noise may not apply. It is natural to seek to minimize ${\displaystyle \|B-A\|_{1}}$.[^9] For ${\displaystyle p=0}$ and ${\displaystyle p\geq 1}$, there are some algorithms with provable guarantees.[^10] [^11]

## Distance low-rank approximation problem

Let ${\displaystyle P=\{p_{1},\ldots ,p_{m}\}}$ and ${\displaystyle Q=\{q_{1},\ldots ,q_{n}\}}$ be two point sets in an arbitrary [metric space](https://en.wikipedia.org/wiki/Metric_space "Metric space"). Let ${\displaystyle A}$ represent the ${\displaystyle m\times n}$ matrix where ${\displaystyle A_{i,j}=dist(p_{i},q_{i})}$. Such distances matrices are commonly computed in software packages and have applications to learning image manifolds, [handwriting recognition](https://en.wikipedia.org/wiki/Handwriting_recognition "Handwriting recognition"), and multi-dimensional unfolding. In an attempt to reduce their description size,[^12] [^13] one can study low rank approximation of such matrices.

## Distributed/Streaming low-rank approximation problem

The low-rank approximation problems in the distributed and streaming setting has been considered in.[^14]

## Image and kernel representations of the rank constraints

Using the equivalences

${\displaystyle \operatorname {rank} ({\widehat {D}})\leq r\quad \iff \quad {\text{there are }}P\in \mathbb {R} ^{m\times r}{\text{ and }}L\in \mathbb {R} ^{r\times n}{\text{ such that }}{\widehat {D}}=PL}$

and

${\displaystyle \operatorname {rank} ({\widehat {D}})\leq r\quad \iff \quad {\text{there is full row rank }}R\in \mathbb {R} ^{m-r\times m}{\text{ such that }}R{\widehat {D}}=0}$

the weighted low-rank approximation problem becomes equivalent to the parameter optimization problems

${\displaystyle {\text{minimize}}\quad {\text{over }}{\widehat {D}},P{\text{ and }}L\quad \operatorname {vec} ^{\top }(D-{\widehat {D}})W\operatorname {vec} (D-{\widehat {D}})\quad {\text{subject to}}\quad {\widehat {D}}=PL}$

and

${\displaystyle {\text{minimize}}\quad {\text{over }}{\widehat {D}}{\text{ and }}R\quad \operatorname {vec} ^{\top }(D-{\widehat {D}})W\operatorname {vec} (D-{\widehat {D}})\quad {\text{subject to}}\quad R{\widehat {D}}=0\quad {\text{and}}\quad RR^{\top }=I_{r},}$

where ${\displaystyle I_{r}}$ is the [identity matrix](https://en.wikipedia.org/wiki/Identity_matrix "Identity matrix") of size ${\displaystyle r}$.

## Alternating projections algorithm

The image representation of the rank constraint suggests a parameter optimization method in which the cost function is minimized alternatively over one of the variables (${\displaystyle P}$ or ${\displaystyle L}$) with the other one fixed. Although simultaneous minimization over both ${\displaystyle P}$ and ${\displaystyle L}$ is a difficult [biconvex optimization](https://en.wikipedia.org/wiki/Biconvex_optimization "Biconvex optimization") problem, minimization over one of the variables alone is a [linear least squares](https://en.wikipedia.org/wiki/Linear_least_squares_\(mathematics\) "Linear least squares (mathematics)") problem and can be solved globally and efficiently.

The resulting optimization algorithm (called alternating projections) is globally convergent with a linear convergence rate to a locally optimal solution of the weighted low-rank approximation problem. Starting value for the ${\displaystyle P}$ (or ${\displaystyle L}$) parameter should be given. The iteration is stopped when a user defined convergence condition is satisfied.

[Matlab](https://en.wikipedia.org/wiki/Matlab "Matlab") implementation of the alternating projections algorithm for weighted low-rank approximation:

```
function [dh, f] = wlra_ap(d, w, p, tol, maxiter)
[m, n] = size(d); r = size(p, 2); f = inf;
for i = 2:maxiter
    % minimization over L
    bp = kron(eye(n), p);
    vl = (bp' * w * bp) \ bp' * w * d(:);
    l  = reshape(vl, r, n);
    % minimization over P
    bl = kron(l', eye(m));
    vp = (bl' * w * bl) \ bl' * w * d(:);
    p  = reshape(vp, m, r);
    % check exit condition
    dh = p * l; dd = d - dh;
    f(i) = dd(:)' * w * dd(:);
    if abs(f(i - 1) - f(i)) < tol, break, end
endfor
```

## Variable projections algorithm

The alternating projections algorithm exploits the fact that the low rank approximation problem, parameterized in the image form, is bilinear in the variables ${\displaystyle P}$ or ${\displaystyle L}$. The bilinear nature of the problem is effectively used in an alternative approach, called variable projections.[^15]

Consider again the weighted low rank approximation problem, parameterized in the image form. Minimization with respect to the ${\displaystyle L}$ variable (a linear least squares problem) leads to the closed form expression of the [approximation error](https://en.wikipedia.org/wiki/Approximation_error "Approximation error") as a function of ${\displaystyle P}$

${\displaystyle f(P)={\sqrt {\operatorname {vec} ^{\top }(D){\Big (}W-W(I_{n}\otimes P){\big (}(I_{n}\otimes P)^{\top }W(I_{n}\otimes P){\big )}^{-1}(I_{n}\otimes P)^{\top }W{\Big )}\operatorname {vec} (D)}}.}$

The original problem is therefore equivalent to the [nonlinear least squares problem](https://en.wikipedia.org/wiki/Least_squares#Non-linear_least_squares "Least squares") of minimizing ${\displaystyle f(P)}$ with respect to ${\displaystyle P}$. For this purpose standard optimization methods, e.g. the [Levenberg-Marquardt algorithm](https://en.wikipedia.org/wiki/Levenberg-Marquardt_algorithm "Levenberg-Marquardt algorithm") can be used.

[Matlab](https://en.wikipedia.org/wiki/Matlab "Matlab") implementation of the variable projections algorithm for weighted low-rank approximation:

```
function [dh, f] = wlra_varpro(d, w, p, tol, maxiter)
prob = optimset(); prob.solver = 'lsqnonlin';
prob.options = optimset('MaxIter', maxiter, 'TolFun', tol); 
prob.x0 = p; prob.objective = @(p) cost_fun(p, d, w);
[p, f ] = lsqnonlin(prob); 
[f, vl] = cost_fun(p, d, w); 
dh = p * reshape(vl, size(p, 2), size(d, 2));

function [f, vl] = cost_fun(p, d, w)
bp = kron(eye(size(d, 2)), p);
vl = (bp' * w * bp) \ bp' * w * d(:);
f = d(:)' * w * (d(:) - bp * vl);
```

The variable projections approach can be applied also to low rank approximation problems parameterized in the kernel form. The method is effective when the number of eliminated variables is much larger than the number of optimization variables left at the stage of the nonlinear least squares minimization. Such problems occur in system identification, parameterized in the kernel form, where the eliminated variables are the approximating trajectory and the remaining variables are the model parameters. In the context of [linear time-invariant systems](https://en.wikipedia.org/wiki/LTI_system_theory "LTI system theory"), the elimination step is equivalent to [Kalman smoothing](https://en.wikipedia.org/wiki/Kalman_filter "Kalman filter").

## A Variant: convex-restricted low rank approximation

Usually, we want our new solution not only to be of low rank, but also satisfy other convex constraints due to application requirements. Our interested problem would be as follows,

${\displaystyle {\text{minimize}}\quad {\text{over }}{\widehat {p}}\quad \|p-{\widehat {p}}\|\quad {\text{subject to}}\quad \operatorname {rank} {\big (}{\mathcal {S}}({\widehat {p}}){\big )}\leq r{\text{ and }}g({\widehat {p}})\leq 0}$

This problem has many real world applications, including to recover a good solution from an inexact ([semidefinite programming](https://en.wikipedia.org/wiki/Semidefinite_programming "Semidefinite programming")) relaxation. If additional constraint ${\displaystyle g({\widehat {p}})\leq 0}$ is linear, like we require all elements to be nonnegative, the problem is called structured low rank approximation.[^16] The more general form is named convex-restricted low rank approximation.

This problem is helpful in solving many problems. However, it is challenging due to the combination of the convex and nonconvex (low-rank) constraints. Different techniques were developed based on different realizations of ${\displaystyle g({\widehat {p}})\leq 0}$. However, the Alternating Direction Method of Multipliers (ADMM) can be applied to solve the nonconvex problem with convex objective function, rank constraints and other convex constraints,[^17] and is thus suitable to solve our above problem. Moreover, unlike the general nonconvex problems, ADMM will guarantee to converge a feasible solution as long as its dual variable converges in the iterations.

[^1]: E. Schmidt, Zur Theorie der linearen und nichtlinearen Integralgleichungen, Math. Annalen 63 (1907), 433-476. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1007/BF01449770](https://doi.org/10.1007%2FBF01449770)

[^2]: C. Eckart, G. Young, The approximation of one matrix by another of lower rank. Psychometrika, Volume 1, 1936, Pages 211–8. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1007/BF02288367](https://doi.org/10.1007%2FBF02288367)

[^3]: L. Mirsky, Symmetric gauge functions and unitarily invariant norms, Q.J. Math. 11 (1960), 50-59. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1093/qmath/11.1.50](https://doi.org/10.1093%2Fqmath%2F11.1.50)

[^4]: Srebro, Nathan; Jaakkola, Tommi (2003). [*Weighted Low-Rank Approximations*](https://www.aaai.org/Papers/ICML/2003/ICML03-094.pdf) (PDF). ICML'03.

[^5]: Razenshteyn, Ilya; Song, Zhao; Woodruff, David P. (2016). [*Weighted Low Rank Approximations with Provable Guarantees*](https://dl.acm.org/citation.cfm?id=2897639). STOC '16 Proceedings of the forty-eighth annual ACM symposium on Theory of Computing.

[^6]: Clarkson, Kenneth L.; Woodruff, David P. (2013). *Low Rank Approximation and Regression in Input Sparsity Time*. STOC '13 Proceedings of the forty-fifth annual ACM symposium on Theory of Computing. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[1207.6365](https://arxiv.org/abs/1207.6365).

[^7]: Nelson, Jelani; Nguyen, Huy L. (2013). *OSNAP: Faster numerical linear algebra algorithms via sparser subspace embeddings*. FOCS '13. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[1211.1002](https://arxiv.org/abs/1211.1002).

[^8]: Sarlos, Tamas (2006). *Improved approximation algorithms for large matrices via random projections*. FOCS'06.

[^9]: Song, Zhao; Woodruff, David P.; Zhong, Peilin (2017). *Low Rank Approximation with Entrywise L1-Norm Error*. STOC '17 Proceedings of the forty-ninth annual ACM symposium on Theory of Computing. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[1611.00898](https://arxiv.org/abs/1611.00898).

[^10]: Bringmann, Karl; Kolev, Pavel; Woodruff, David P. (2017). *Approximation Algorithms for L0-Low Rank Approximation*. NIPS'17. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[1710.11253](https://arxiv.org/abs/1710.11253).

[^11]: Chierichetti, Flavio; Gollapudi, Sreenivas; Kumar, Ravi; Lattanzi, Silvio; Panigrahy, Rina; Woodruff, David P. (2017). *Algorithms for Lp Low-Rank Approximation*. ICML'17. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[1705.06730](https://arxiv.org/abs/1705.06730).

[^12]: Bakshi, Ainesh L.; Woodruff, David P. (2018). *Sublinear Time Low-Rank Approximation of Distance Matrices*. NeurIPS. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[1809.06986](https://arxiv.org/abs/1809.06986).

[^13]: Indyk, Piotr; Vakilian, Ali; Wagner, Tal; Woodruff, David P. (2019). *Sample-Optimal Low-Rank Approximation of Distance Matrices*. COLT.

[^14]: Boutsidis, Christos; Woodruff, David P.; Zhong, Peilin (2016). *Optimal Principal Component Analysis in Distributed and Streaming Models*. STOC. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[1504.06729](https://arxiv.org/abs/1504.06729).

[^15]: G. Golub and V. Pereyra, Separable nonlinear least squares: the variable projection method and its applications, Institute of Physics, Inverse Problems, Volume 19, 2003, Pages 1-26.

[^16]: Chu, Moody T.; Funderlic, Robert E.; Plemmons, Robert J. (2003). ["structured low-rank approximation"](https://doi.org/10.1016%2FS0024-3795%2802%2900505-0). *Linear Algebra and Its Applications*. **366**: 157–172. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1016/S0024-3795(02)00505-0](https://doi.org/10.1016%2FS0024-3795%2802%2900505-0).

[^17]: ["A General System for Heuristic Solution of Convex Problems over Nonconvex Sets"](https://stanford.edu/~boyd/papers/pdf/ncvx.pdf) (PDF).