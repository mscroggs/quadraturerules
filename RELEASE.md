# Making a new release

To make a new release of the quadraturerules library, follow these steps:

1. Open a pull request to increase the version number in [VERSION](VERSION).

2. Wait for the CI to pass and merge the PR.

3. Create a [new tag](https://github.com/mscroggs/quadraturerules/releases/new) on GitHub. The title and tag should be `v{VERSION}`.

4. A Python release should be created automaticaly by the [release](https://github.com/mscroggs/quadraturerules/actions/workflows/release.yml) CI workflow.