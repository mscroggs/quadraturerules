Welcome to the online encyclopedia of quadrature rules, a reference website that lists a number of quadrature rules.
Each quadrature rule is indexed using Q followed by a six-digit number, for example [Q000001](/Q000001).

You can view the [full list of quadrature rules included in this encyclopedia](/rules.html) or view the [list of all pages in the encyclopedia](sitemap.md).

## What is a quadrature rule?
Quadrature rules are sets of points and weights that are used to approximate integrals. If \(\{\vec{p}_0,\dots,\vec{p}_{n-1}\}\subset\mathbb{R}^d\) and \(\{w_0,\dots,w_{n-1}\}\subset\mathbb{R}\)
are the points and weights (repectively) of the quadrature rule for a single integral, then:

$$\int f(x)\,\mathrm{d}x \approx \sum_{i=0}^{n-1}f(\vec{p}_i)w_i$$

The points that make up the quadrature rules in this encyclopedia are represented using [barycentric coordinates](barycentric.md).

## Libraries

All of the quadrature rules included in the online encylopedia of quadrature rules are included in the quadraturerules library, which is available in the following languages

* [Python](https://pypi.org/project/quadraturerules/)
* [Rust](https://crates.io/crates/quadraturerules)
