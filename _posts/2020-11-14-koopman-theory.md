---
title: 'Notes on Koopman theory'
layout: post
tags: dynamical-systems machine-learning
---



DMD lets us take \\(\frac{dx}{dt} = f(x, t, \mu)\\),

And approximate it with \\(\frac{dx}{dt} \approx Ax\\)

Typically we want to this because we have access to \\(x\\). But that
doesn&rsquo;t mean that \\(x\\) is the _best_ possible variable to think about the
system. Namely, for instance, \\(f\\) might be very non-linear and
non-amenable to be approximated by a matrix.

Koopman realized, in his 1931 paper _Hamiltonian Systems and
Transformations in Hilbert Space_, that the following applies:

-   If \\(g\\) is the Hilbert space of all possible observables of the state \\(x\\)
-   (Note that his means that \\(g\\) is infinite dimensional, because it
literally consists of all the possible transformations/functions we
can apply to \\(x\\))
-   Then, there exists a linear operator \\(K\_t\\) , such that \\(K\_t g(x\_k) = g(x\_{k+1})\\)

As noted, \\(K\_t\\) is infinite-dimensional. However, there can be
Koopman-invariant subspaces: finite-dimension subspaces that are spanned
by eigen-observable-functions of the Koopman operator. When these
subspaces are hit by the Koopman operator, the result stays in the
subspace - hence the name, Koopman-invariant. If we can find these, we
can approximate the Koopman operator by a finite matrix.

![img](/images/koopman.png)


# Million-dollar question

How do you get \\(g\\)?
