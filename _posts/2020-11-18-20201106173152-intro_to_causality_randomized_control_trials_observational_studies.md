---
title: 'Intro to causality: Randomized Control Trials & Observational Studies'
layout: post
tags: causality
---



# Potential outcomes

-   Outcome variable \\(Y\_i\\) as a function of action/treatment \\(T\_i\\)
-   Let \\(Y\_i |\_{do(T\_i=t)} := Y\_i(t)\\)
-   Then (for a binary action) the causal effect is \\(Y\_i(1) - Y\_i(0)\\)


## Problem: if we perform do(T=1) we can&rsquo;t observe what would&rsquo;ve happend if do(T=0), and vice-versa


### Idea: Average Treatment Effect

\begin{align}
\mathbb{E}[Y\_i(1) - Y\_i(0)] &= \mathbb{E}[Y(1)] - \mathbb{E}[Y(0)] \\\\\\
&\neq \mathbb{E}[Y|T=1] - \mathbb{E}[Y|T=0]
\end{align}

1.  This is the basis for randomized control trials

-   But for it to be usable, because of confounding, the cause \\(C\\) of \\(Y\\), can&rsquo;t

be a cause of \\(T\\) , i.e., \\(T\\) has to be random.

-   This way, we can use conditional expectations

<!--listend-->

-   Groups have to be comparable: example of drunk people who sleep with shoes on.


# Observational studies


## Problem: we can&rsquo;t always randomize treatment


## Solution: adjust for confounders


### If \\(W\\) is a sufficient adjustment set

\begin{align}
\mathbb{E}[Y(t)|W=w] &:= \mathbb{E}[Y|do(T=t), W=w] \\\\\\
&= \mathbb{E}[Y|t, w]
\end{align}

i.e. we can estimate a causal quantity from a statistical quantity

![img](/images/20201106173152-intro_to_causality_randomized_control_trials_observational_studiesju2yD8.png)


### But what we really want is \\(\mathbb{E}[Y(t)]\\)

Average out \\(W\\) :
\\(
\mathbb{E}[Y(t)] = \mathbb{E}\_W\mathbb{E}[Y|t,W]
\\)


## Set of variables is sufficient adjusment set if it blocks all paths of confounding association

Examples:

![img](/images/20201106173152-intro_to_causality_randomized_control_trials_observational_studiesQcpTVs.png) ![img](/images/20201106173152-intro_to_causality_randomized_control_trials_observational_studiesPcKisY.png)
