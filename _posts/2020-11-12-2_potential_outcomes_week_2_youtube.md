---
title: '2 - Potential Outcomes (Week 2) - YouTube'
layout: post
tags: causality
---



# Potential outcomes

-   Goal: infer effect of treatment/policy on some outcome


# Notation

-   \\(T\\) observed treatment
-   \\(Y\\) observed outcome
-   \\(i\\) subscript to denote a specific unit/individual
-   \\(Y\_i|\_{do(T\_i=1)} := Y\_i(1)\\) potential outcome under treatment

Given this:

-   Causal effect: \\(Y\_i(1) - Y\_i(0)\\)


# Fundamental problem of causal inference

-   Causal effect isn&rsquo;t observable, because only one option is taken
-   Factual (observed) vs Counterfactual (not observed)
-   Similar to a missing-data problem


# Getting around the fundamental problem

-   Idea: average treatment effect
-   \\(\mathbb{E}[Y(1) - Y(0)] = \mathbb{E}[Y(1)] - \mathbb{E}[Y(0)]\\)
-   Problem: \\(\mathbb{E}[Y(t)] \neq \mathbb{E}[Y|T=t]\\)
-   Association is not causation (drunk people sleep with shoes on, but it&rsquo;s
not the shoes that cause the headache)
![img](./img/2_potential_outcomes_week_2_youtubeYY301v.png)
-   So we can&rsquo;t compute the expectation&#x2026; (unless we can make the equality hold)


# Identifiability

-   When you can compute a causal quantity from a statistical quantity


# What assumptions would make ATE equal to the associational difference?


## Unconfoundedness


### Ignorability / exchangeability: Y(1),Y(0) independent from T (statistically)

-   Randomized Control Trials assure this assumption

![img](/home/colobas/org/knowledge-base/img/2_potential_outcomes_week_2_youtube3lBBwQ.png)

-   For example: a RCT would &ldquo;remove&rdquo; the edge between confounder X and treatment T, in this case


### Conditional echangeability

-   Y(1), Y(0) independent from T, given X
-   Conditioning on X in the above scenario would &ldquo;block&rdquo; the confounding
-   &ldquo;Controlling for X&rdquo;
-   This allows one to start with
\\(\mathbb{E}[Y(1) - Y(0)|X] = \mathbb{E}[E|T=1, X] - \mathbb{E}[Y|T=0, X]\\),
and then average over X to obtain our desired estimate:
\\(\mathbb{E}[Y(1) - Y(0)] = \mathbb{E}\_X\mathbb{E}[Y(1) - Y(0)|X]\\)


### Unconfoundedness is an untestable assumption

-   Can&rsquo;t know about unobserved confounders


## Positiviy

-   Overlap across controlled for dimensions
-   Positivity vs Unconfoundedness trade-off


## No interference

-   Potential outcome \\(Y\_i\\) depends exclusively on \\(T\_i\\), (even if \\(T\_{i+1}\\) could
also conceivably influence \\(T\_i\\), e.g. I get a dog & my friend gets a dog, but
my happiness is only a function of me getting a dog)


## Consistency

-   \\(T = t \rightarrow Y = Y(t)\\)
-   All treatments are equal.
-   E.g. &ldquo;I get a dog&rdquo; is equal to &ldquo;I get a golden retriever&rdquo; and &ldquo;I get a chihuahua&rdquo;


# In summary

![img](/home/colobas/org/knowledge-base/img/2_potential_outcomes_week_2_youtubepu2P17.png)


# Example problem: effect of sodium intake on blood pressure

-   Outcome \\(Y\\): (systolic) blood pressure
-   Treatment: sodium intake (1 if > 3.5mg, else 0)
-   Covariates X: age and amount of protein excreted in urine
-   Ground truth: ATE = 1.05

\begin{align}
\mathbb{E}[Y(1) - Y(0)] &= \mathbb{E}\_X\big[\mathbb{E}[Y| T = 1, X] - \mathbb{E}[Y| T = 0, X] \big] \\\\\\
&= \frac{1}{n} \sum\_x \big[ \mathbb{E}[Y| T = 1, X] - \mathbb{E}[Y| T = 0, X  \big]
\end{align}

-   Model \\(\mathbb{E}[Y|T=t, X]\\), for instance with a linear regression
-   Estimate: ~0.85
-   Naïve (non-causal) estimate: 5.33
