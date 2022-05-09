# MCBizMod

`mcbizmod` is a package meant to help create advanced business case opportunities leveraging distributions.

## Contributors
- Zuccarelli, Eugenio *(<ZuccarelliE@aetna.com>)*
- Goldberg, Eli *(<GoldbergE@cvshealth.com>)*

## Installation

**TODO: Update the installation section to leverage PyPi and pip install.**
In your environment, run

```
pip install --upgrade git+https://github.aetna.com/clinical-product-analytics/mcbizmod.git --user
```

If you want to install a specific branch:

```
pip install --upgrade git+https://github.aetna.com/clinical-product-analytics/mcbizmod.git@<BRANCH> --user
```

## Tests
To run unit tests:
```
python3 tests/<test_name>.py
```

## Why do we care about business cases and distributions? 
Oftentimes when people make a business cases, they make static or fixed assumptions about the behavior. While convenient, this is a bad idea. Here's where distributions come in.

Ultimately, each parameter isn't static; it's a distribution of possibilities for which we need to determine the fraction of times that we'll fail on a PLAN level and need to pay fees back. 

In many real-world applications, we have to deal with complex probability distributions on complicated high-dimensional spaces. On rare occasions, it is possible to sample exactly from the distribution of interest, but typically exact sampling is difficult. Further, high-dimensional spaces are very large, and distributions on these spaces are hard to visualize, making it difficult to even guess where the regions of high probability are located. As a result, it may be challenging to even design a reasonable proposal distribution to use with importance sampling.

Markov chain Monte Carlo (MCMC) is a sampling technique that works well in many situations like this. However, this is NOT a conditional distribution (or Gibbs) sampling tool!! This is for several reasons:
1. We usually don't have enough information to set an appropriate prior.

2. Where we do, we could set that prior. However, we don't know the conditional effect on the distribution from the most critical variables, namely engagement and the treatment effect. Thus, it's likely better to assume absolute ignorance rather than create a partially broken conditional probability chain. This mimicks typical business cases (which obviously don't use markov-chain-based distribution sampling methods). 

To make this simple task a bit easier, we've built a basic dataclass constructor to track the assumptions made and make your business cases repeatable, inspectable, and (more) accurate. Or at least, wrong in a quantifiable way :).


## What are some of the fundamental 'tenants' of using mcbizmod? 

1. Pull your population directly from data whenever possible.
    
2. Where possible, _use the whole distribution_. 
    - Data is data. It's wild, but you benefit from using the whole distribution because IT'S data! 
    
3. When in doubt, use lognormal distributions to estimate. 
    - Most biologic phenomena follow a lognormal distribution (this came from a colleague of mine [lognormal and bioscience](https://stat.ethz.ch/~stahel/lognormal/bioscience.pdf)). 

## What are some fundamental design principles when contributing to this repo? 
1. Follow the [PEP-8](https://www.python.org/dev/peps/pep-0008/) syntax guide for your code, specifically focused on the following:
    * Function names should reflect usage instead of implementation.
    * Function and variable names should be of the `lowercase_with_underscore` style. 
    * Globally-used names should be of the `UPPERCASE_WITH_UNDERSCORE` style.
2. Minimize dependencies.
3. Where possible, avoid list comprehensions. They have a _smell_. 
4. Leverage the power of logging (although we don't, here).
5. Most of all: Keep it simple and smartly objective.
