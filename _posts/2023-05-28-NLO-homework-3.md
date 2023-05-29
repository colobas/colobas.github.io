---
math: true
author:
- |
  Guilherme Pires\
  75432
bibliography:
- /home/colobas/org/biblio.bib
date: 2023-05-28
title:
- NLO - homework 3
- Non-linear Optimization - Homework 3
---

# 48 - Robot vacuum 

An ellipsoid can alternatively be parameterized by
$E = \{c + \Sigma^{1/2} u : {\lVert u \rVert}_2 \leq 1 \}$. We can
intersect it with the polyhedron constraints:

$$\begin{aligned}
\sup_{ {\lVert u \rVert}_2 \leq 1} {a_i}^T (c + \Sigma^{1/2} u) &\leq b_i \\
{a_i}^T c + \sup_{ {\lVert u \rVert}_2 \leq 1} {a_i}^T \Sigma^{1/2} u &\leq b_i \\
{a_i}^T c + \sup_{ {\lVert u \rVert}_2 \leq 1} \big((\Sigma^{1/2})^T a_i^T\big)^T u &\leq b_i \\
{a_i}^T c + \sup_{ {\lVert u \rVert}_2 \leq 1} \big(\Sigma^{1/2} a_i^T\big)^T u &\leq b_i \label{step4} && \text{Because $\Sigma^{1/2}$ is symmetric}\\
{a_i}^T c + \left\lVert\Sigma^{1/2} a_i \right\rVert_{2} &\leq b_i \label{step5} \\
{a_i}^T c + \left\lVert\Sigma^{1/2} a_i \right\rVert_{2} - b_i &\leq 0
\end{aligned}$$

The step from ([\[step4\]](#step4){reference-type="ref"
reference="step4"}) to ([\[step5\]](#step5){reference-type="ref"
reference="step5"}) can be understood by observing that the supremum of
$(\Sigma^{1/2} a_i^T)^T u$ w.r.t $u$ is reached when $u$ is parallel to
$(\Sigma^{1/2} a_i)^T$. Since $u$ is a unit vector, we can rewrite it as
$\frac{\Sigma^{1/2} a_i}{\left\lVert\Sigma^{1/2} a_i \right\rVert_{2} }$
and do

$$\begin{aligned}
(\Sigma^{1/2} a_i)^T \frac{\Sigma^{1/2} a_i}{\left\lVert\Sigma^{1/2} a_i \right\rVert_{2} } \
&= \frac{ {\left\lVert\Sigma^{1/2} a_i \right\rVert_{2} }^2}{\left\lVert\Sigma^{1/2} a_i \right\rVert_{2} } \\
&= \left\lVert\Sigma^{1/2} a_i \right\rVert_{2}
\end{aligned}$$

So we obtain a linear constraint for each column of $A$, and can thus
write the LP:

$$\begin{aligned}
& \min_{c} & & - e^T c \\
& \textrm{s.t.} & & {a_i}^T c + \left\lVert\Sigma^{1/2} a_i \right\rVert_{2} - b_i \leq 0, i \in \{1,\ldots,m\}
\end{aligned}$$

To use my solution, we need to compute $\Sigma^{1/2}$. Luckily it is
2x2, so there is a straightforward formula
(<https://en.wikipedia.org/wiki/Square_root_of_a_2_by_2_matrix>).

For the given matrix $\Sigma$, its square-root (computed by the linked
method) is $$\begin{aligned}
\begin{bmatrix}
 1.0603   & -0.342025 \\
-0.342025 &  2.9397
\end{bmatrix}
\end{aligned}$$

See below the implementation, using CVXPY:

    import cvxpy as cp
    import numpy as np

    c = cp.Variable(2)
    A = np.array([
        [1, 1],
        [1, -1]
    ])
    b = np.array([10, 10])
    e = np.array([1, 0])

    sigma_sqrt = np.array([
        [1.0603, -0.342025],
        [-0.342025,  2.9397],
    ])

    # sqrt of validation sigma
    #sigma_sqrt = np.array([
    #    [1.3572 , 0.76605],
    #    [0.76605, 2.6428 ]
    #])

    constraints = [
        A[i].T @ c + np.linalg.norm(sigma_sqrt @ A[i], ord=2) - b[i] <= 0
        for i in range(2)
    ]

    prob = cp.Problem(cp.Minimize(-e.T @ c), constraints)
    prob.solve()

    # Print result.
    print("The optimal value is", prob.value)
    print("A solution c is", c.value)

    The optimal value is -6.8680318592201335
    A solution c is [6.86803186 0.43681798]

# 54 - Data rates 

The objective function is linear, and most of the constraints are
affine. The only problematic constraint is the budget constraint. I want
to decouple the cost constraints from one another, because they have a
tricky non-linearity. So introducing auxiliary variables $z_i$, we can
rewrite the budget constraint as

$$\begin{aligned}
\begin{cases}
\alpha_i x_i + \frac{\beta_i}{2}\max\{0, x_i - \frac{C_i}{2}\}^2 \leq z_i, i=1,...,5 \\
\sum_{i=1}^5 z_i \leq B
\end{cases}
\end{aligned}$$

Rearranging the first inequality:

::: empheq
align \_i x_i + {0, x_i - }\^2 &z_i\
{0, x_i - }\^2 &(z_i - \_i x_i)
:::

We can now use the equivalence shown in the lectures and write, with new
auxiliary variables $y_i$:

::: empheq
align {0, x_i - } y_i []{#ineq1 label="ineq1"}\
y_i\^2 (z_i - \_i x_i) []{#ineq2 label="ineq2"}
:::

Let us focus on inequality ([\[ineq2\]](#ineq2){reference-type="ref"
reference="ineq2"})

$$\begin{aligned}
y_i^2 &\leq \underbrace{(z_i - \alpha_i x_i)\frac{2}{\beta_i} }_{\geq 0\text{, since~$\alpha_i x_i \geq 0$ and $\alpha_i x_i \leq z_i$} }
\end{aligned}$$

So we can use the "key fact" from the lectures and write:

$$\begin{aligned}
\left\lVert\begin{bmatrix} 2y_i \\ (z_i - \alpha_i x_i)\frac{2}{\beta_i} - 1\end{bmatrix}\right\rVert_2 &\leq  (z_i - \alpha_i x_i)\frac{2}{\beta_i} + 1
\end{aligned}$$

Which is a valid constraint for a SOCP. Now, addressing
([\[ineq1\]](#ineq1){reference-type="ref" reference="ineq1"}), we can
simply rewrite it as:

$$\begin{aligned}
0 \leq y_i \\
x_i - \frac{C_i}{2} \leq y_i
\end{aligned}$$

So we arrive at the final form for our optimization problem, which we
have shown can be cast as a SOCP:

$$\begin{aligned}
& \max_{r, x_1, ..., x_5, z_1, ..., z_5, y_1, ..., y_5} & & r \\
& \text{subject to} & & \\
& & & r = x_1 + x_2 \\
& & & x_1 + x_3 = x_4 \\
& & & x_2 = x_3 + x_5 \\
& & & x_4 + x_5 = r \\
& & & x_i \geq 0 \\
& & & x_i \leq C_i \\
& & & \sum_{i=1}^5 z_i \leq B \\
& & & \left\lVert\begin{bmatrix} 2y_i \\ (z_i - \alpha_i x_i)\frac{2}{\beta_i} - 1\end{bmatrix}\right\rVert_2 &\leq  (z_i - \alpha_i x_i)\frac{2}{\beta_i} + 1, i = 1, ..., 5 \\
& & & 0 \leq y_i \\
& & & x_i - \frac{C_i}{2} \leq y_i, i = 1, ..., 5 \\
\end{aligned}$$

Rewritten in the canonical form:

$$\begin{aligned}
& \min_{r, x_1, ..., x_5, z_1, ..., z_5, y_1, ..., y_5} & & -r \\
& \text{subject to} & & \\
& & & r - x_1 - x_2 = 0 \\
& & & x_1 + x_3 - x_4 = 0 \\
& & & x_2 - x_3 - x_5 = 0 \\
& & & x_4 + x_5 - r = 0 \\
& & & -x_i \leq 0 \\
& & & x_i - C_i \leq 0 \\
& & & \sum_{i=1}^5 z_i - B \leq 0 \\
& & & \left\lVert\begin{bmatrix} 2y_i \\ (z_i - \alpha_i x_i)\frac{2}{\beta_i} - 1\end{bmatrix}\right\rVert_2 &\leq  (z_i - \alpha_i x_i)\frac{2}{\beta_i} + 1, i = 1, ..., 5 \\
& & & -y_i \leq 0 \\
& & & x_i - \frac{C_i}{2} - y_i \leq 0, i = 1, ..., 5 \\
\end{aligned}$$

See below the implementation and solution in CVXPY

    import cvxpy as cp
    import numpy as np

    r = cp.Variable(1)
    x = cp.Variable(5)

    # to give the flow constraints in vector form
    vec_r = cp.reshape(r, (1, 1))
    vec_x = cp.reshape(x, (5, 1))
    flow_vars = cp.reshape(cp.vstack((vec_r, vec_x)), 6)

    # auxiliary vars
    y = cp.Variable(5)
    z = cp.Variable(5)

    B = 15.
    alpha = np.array([2., 1., 5., 3., 1.])
    beta = np.array([2., 2., 0.5, 2., 1.])
    C = np.array([10., 6., 8., 10., 8.])

    F = np.array([
        # r  x1  x2  x3  x4  x5
        [ 1, -1, -1,  0,  0,  0],
        [ 0,  1,  0,  1, -1,  0],
        [ 0,  0,  1, -1,  0, -1],
        [-1,  0,  0,  0,  1,  1],
    ])

    ones = np.ones(5)

    constraints = [
        F @ flow_vars <= 0,
        ones @ z <= B,
        y >= 0,
        x - C/2 - y <= 0,
        x >= 0,
        x <= C
    ]

    constraints += [
        cp.pnorm(
            cp.vstack((2*y[i],
                      (z[i] - alpha[i]*x[i])*2/beta[i] - 1)),
            p=2
        ) <= (z[i] - alpha[i]*x[i])*2/beta[i] + 1
        for i in range(5)
    ]

    prob = cp.Problem(cp.Minimize(-r), constraints)
    prob.solve()

    # Print result.
    print("The optimal value r is", r.value)
    print("The optimal link x is", x.value)

    The optimal value r is [5.23333333]
    The optimal link x is [8.99999988e-01 4.33333334e+00 5.11970231e-11 8.99999988e-01
     4.33333334e+00]

# 61 - Optimal linear estimators for uncertain covariance 

We can rewrite the cost function (omitting the supremum specification
for brevity) as:

$$\begin{aligned}
\sup\Big\{
\begin{bmatrix}
s^T & -1 & r
\end{bmatrix}
\begin{bmatrix}
\Sigma + \mu \mu^T & \mu \\
\mu & 1 \\
\end{bmatrix}
\begin{bmatrix}
s \\
-1 \\
r
\end{bmatrix}
\Big\} &=
\sup\Big\{
\begin{bmatrix}
s^T & -1 & r
\end{bmatrix}
\begin{bmatrix}
\sum_{k=1}^K \pi_k \Sigma_k + \mu \mu^T & \mu \\
\mu & 1 \\
\end{bmatrix}
\begin{bmatrix}
s \\
-1 \\
r
\end{bmatrix}
\Big\} \\
&=
\sup\Big\{
\begin{bmatrix}
s^T & -1 & r
\end{bmatrix}
\begin{bmatrix}
\mu \mu^T & \mu \\
\mu & 1 \\
\end{bmatrix}
\begin{bmatrix}
s \\
-1 \\
r
\end{bmatrix} +
s^T \big( \sum_{k=1}^K \pi_k \Sigma_k\big) s
\Big\} \\
&=
\begin{bmatrix}
s^T & -1 & r
\end{bmatrix}
\begin{bmatrix}
\mu \mu^T & \mu \\
\mu & 1 \\
\end{bmatrix}
\begin{bmatrix}
s \\
-1 \\
r
\end{bmatrix} +
\sup\Big\{
s^T \big( \sum_{k=1}^K \pi_k \Sigma_k\big) s
\Big\} \label{supr1} \\
&=
\begin{bmatrix}
s^T & -1 & r
\end{bmatrix}
\begin{bmatrix}
\mu \mu^T & \mu \\
\mu & 1 \\
\end{bmatrix}
\begin{bmatrix}
s \\
-1 \\
r
\end{bmatrix} +
\sup\Big\{
\sum_{k=1}^K \pi_k s^T \Sigma_k s
\Big\} \\
&=
\begin{bmatrix}
s^T & -1 & r
\end{bmatrix}
\begin{bmatrix}
\mu \mu^T & \mu \\
\mu & 1 \\
\end{bmatrix}
\begin{bmatrix}
s \\
-1 \\
r
\end{bmatrix} +
\max\Big\{s^T \Sigma_k s \Big\}
\end{aligned}$$

In ([\[supr1\]](#supr1){reference-type="ref" reference="supr1"}) I move
the supremum in, because $\begin{bmatrix}
\mu \mu^T & \mu \\
\mu & 1 \\
\end{bmatrix}$ is positive semi-definite and so the first term is
$\geq 0$, and independent from the $\Sigma_k$. To take the final step,
we use the fact that all of the $\Sigma_k$ are p.s.d. (since they are
covariance matrices), and so all of the summands are $\ge$ 0, and since
$\sum \pi_k = 1$ and $\pi_k \geq 0$, the supremum is reached when we put
all of the "mass" of $\pi$ in the term with the largest value.

Now, introducing two epigraph variables, we can rewrite the problem:

$$\begin{aligned}
& \min_{s, r, t_1, t_2} & & t_1 + t_2 \\
& \text{subject to} & & \\
& & & \begin{bmatrix}
s^T & -1 & r
\end{bmatrix}
\begin{bmatrix}
\mu \mu^T & \mu \\
\mu & 1 \\
\end{bmatrix}
\begin{bmatrix}
s \\
-1 \\
r
\end{bmatrix} \leq t_1 \\
& & & \max\Big\{s^T \Sigma_k s \Big\} \leq t_2
\end{aligned}$$

Using the fact that
$\max\{a_1, ..., a_K\} \leq \epsilon \leftrightarrow a_i \leq \epsilon,\ i = 1,...,K$,
we can substitute the second inequality by $K$ inequalities:

$$\begin{aligned}
& \min_{s, r, t_1, t_2} & & t_1 + t_2 \\
& \text{subject to} & & \\
& & & \begin{bmatrix}
s^T & -1 & r
\end{bmatrix}
\begin{bmatrix}
\mu \mu^T & \mu \\
\mu & 1 \\
\end{bmatrix}
\begin{bmatrix}
s \\
-1 \\
r
\end{bmatrix} \leq t_1 \\
& & & s^T \Sigma_k s \leq t_2,\ k = 1,..,K
\end{aligned}$$

which is a QCQP.
