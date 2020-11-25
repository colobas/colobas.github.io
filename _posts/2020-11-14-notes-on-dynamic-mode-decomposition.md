---
title: 'Notes on Dynamic Mode Decomposition'
layout: post
tags: algebra dynamical-system control
---

\#+ DATE: 2019-05-25
\#+ FILETAGS: :decomposition:algebra:dynamical-systems:control:



#

These are notes I made to sum up my learnings from watching these two
videos about Dynamic Mode Decomposition, by Prof. J. Nathan Kutz:

-   [Part I](https://www.youtube.com/watch?v=bYfGVQ1Sg98)
-   [Part II](https://www.youtube.com/watch?v=KAau5TBU0Sc)

I highly recommend watching them!


# Important concepts

There are some key concepts you should be familiar with to understand
DMD. I was a bit rusty on these, so I&rsquo;m taking the chance to refresh the
most important parts here too

If you feel comfortable on those two topics, feel free to skip


## Linear Dynamical Systems


###

Let \\(x(t)\\) represent an observation at time \\(t\\) of a system that evolves
in continuous time, and \\(x\_t\\) represent an observation at time \\(t\\) of a
system that evolves in discrete time.


###

Then, a Linear Dynamical System is one where the following applies
(respectively for continous and discrete time):

\\[ \frac{d\vec{x(t)}}{dt} = A\vec{x(t)} \\]

or

\\[ \vec{x\_{t+1}} = A\vec{x\_t} \\]

It can be shown that, the general solution to this differential equation
is:

\\[ \vec{x\_t} = e^{tA}\vec{x\_0} \\]


###

Check [this link](http://ee263.stanford.edu/lectures/expm.pdf) from
one of Prof. Stephen Boyd&rsquo;s courses, for a good explanation of this.


## Singular Value Decomposition

SVD is a way to factorize any (m x n) matrix into 3 matrices:

\\[ A = U\Sigma V^T \\]


###

The matrices have the following shapes

-   \\(A\\) is (m x n)
-   \\(U\\) is (m x m) and orthonormal
-   \\(\Sigma\\) is (m x n) and diagonal
-   \\(V^T\\) is (n x n) and orthonormal


###

Here&rsquo;s a good reference from the
[SVD
Wikipedia page](https://en.wikipedia.org/wiki/Singular_value_decomposition) :

**\*\***
SVD lends itself to useful interpretations. Say A is a matrix of gene
expressions for people, where each column represents the gene expression
values for one person.

1.

Then the matrix U will contain the &ldquo;eigenpeople&rdquo;: the main directions of
variation in the &ldquo;people&rdquo;-space.


###

[Prof. Gilbert Strang&rsquo;s
video](https://www.youtube.com/watch?v=mBcLRGuAFUk) is another great resource to understand SVD.


###

Also, for a quick hint on the relationship between SVD and PCA, check
[this Math StackExchange
answer](https://math.stackexchange.com/a/3871)


# Dynamic Mode Decomposition

DMD&rsquo;s goal:

Given observations of a dynamical system, obtain the matrix A that
best describes it.


##

Let \\(X\\) be a (n x m) matrix, of m observations with n dimensions, from
time t=1 to time t=m-1. Let \\(X'\\) be a (n x m) matrix, of m observations
with n dimensions, from time t=2 to time t=m.


##

We&rsquo;re trying to find A such that \\(X' = AX\\)


###

Problem: X is possibly very high-dimensional.
Solution (assumption): X and A have low-rank structure.

****\*****
Taking this, we do  \\(U\Sigma V^T = SVD(X)\\)

****\*****
With the low-rank assumption, we can approximate:
\\(X = U\_r \Sigma\_r {V\_r}^T\\), where the subscript \\(r\\) means we&rsquo;re using
only the \\(r\\) most important components. (The assumption&rsquo;s corollary is
that these are enough to represent the whole \\(X\\)). To choose this \\(r\\),
we look at the singular values in \\(\Sigma\\) and decide based on their
magnitudes - for instance, if the first 3 singular values are orders
of magnitude bigger than the remaining ones, we would do \\(r=3\\).

1.

\\(A = X' X^+\\) which implies \\(A = X' V\_r {\Sigma\_r}^{-1} {U\_r}^T\\) (where
\\(X^+\\) is the pseudo-inverse of \\(X\\))

2.

Now, rather than working with a big matrix A, we&rsquo;re interested in
working with smaller matrices. For that we use a similarity transform.
(Recall that similar matrices have the same eigenvalues):

-   \\(Ã = U^+ A U\\)
-   \\(Ã = U^+ X' V \Sigma^{-1} U^T U = U^+ X' V \Sigma^{-1}\\)

3.  We then find the eigenvalues and eigenvectors of \\(Ã\\):

\\(ÃW = W\Lambda\\), where \\(W\\) has the eigenvectors of \\(Ã\\) on its
columns, and \\(\Lambda\\) is diagonal with the eigenvalues of \\(Ã\\) as
its diagonal

4.

Finally, we want to bring the eigenvectors and eigenvalues of \\(Ã\\) back
into the original coordinate system:

1.  \\(\Phi = X'V\Sigma^{-1} W\\)

2.  This allows us to rewrite our dynamical system:

1.  \\(\vec{x\_t} = \sum\_{k=1}^r \vec{\phi\_k} e^{\omega\_k t} b\_k\\)

2.

This formulation allows us to think of the dynamical system in terms
of the DMD modes (the \\(\phi\_k\\)) which I like to regard as
&ldquo;eigenslices&rdquo;, and their respective oscillatory profiles (the
\\(e^{\omega\_k t}\\) terms), which explain the time dynamics of each DMD
mode.

3.

Important remark: in a true linear dynamical system, the \\(\omega\_k\\)
would have no real part, just imaginary, i.e. they would be pure
oscillators. However, since in general we&rsquo;re approximating a
non-linear system with a linear one, the \\(\omega\_k\\) we obtain will
almost always have a real part, although a really small one,
depending on the data. This means that we can&rsquo;t use DMD to describe
the system in the long-term, since the real part of the \\(\omega\_k\\)
will cause the approximated system to either dampen out (if the real
part is negative) or blow up (if the real part is positive).
