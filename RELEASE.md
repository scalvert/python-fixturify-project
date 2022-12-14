# Releasing a new version

Building a new version of the application contains steps:

- Bump the version of your package `poetry version <version>`. You can pass the new version explicitly, or a rule such as `major`, `minor`, or `patch`. For more details, refer to the [Semantic Versions](https://semver.org/) standard.
- Make a commit to `GitHub`.
- Create a `GitHub release`.
- And... publish π `poetry publish --build`

## π Releases

You can see the list of available releases on the [GitHub Releases](https://github.com/scalvert/python-fixturify-project/releases) page.

We follow [Semantic Versions](https://semver.org/) specification.

We use [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). As pull requests are merged, a draft release is kept up-to-date listing the changes, ready to publish when youβre ready. With the categories option, you can categorize pull requests in release notes using labels.

### List of labels and corresponding titles

|               **Label**               |  **Title in Releases**  |
| :-----------------------------------: | :---------------------: |
|       `enhancement`, `feature`        |       π Features       |
| `bug`, `refactoring`, `bugfix`, `fix` | π§ Fixes & Refactoring  |
|       `build`, `ci`, `testing`        | π¦ Build System & CI/CD |
|              `breaking`               |   π₯ Breaking Changes   |
|            `documentation`            |    π Documentation     |
|            `dependencies`             | β¬οΈ Dependencies updates |

You can update it in [`release-drafter.yml`](https://github.com/scalvert/python-fixturify-project/blob/main/.github/release-drafter.yml).

GitHub creates the `bug`, `enhancement`, and `documentation` labels for you. Dependabot creates the `dependencies` label. Create the remaining labels on the Issues tab of your GitHub repository, when you need them.
