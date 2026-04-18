---
title: "Publishing a package"
source: "https://docs.github.com/en/packages/learn-github-packages/publishing-a-package"
author:
published:
created: 2026-04-13
description: "You can publish a package to GitHub Packages to make the package available for others to download and re-use."
tags:
  - "clippings"
---
## About published packages

You can help people understand and use your package by providing a description and other details like installation and usage instructions on the package page. GitHub provides metadata for each version, such as the publication date, download activity, and recent versions. For an example package page, see [@Codertocat/hello-world-npm](https://github.com/Codertocat/hello-world-npm/packages/10696?version=1.0.1).

You can publish packages in a public repository (public packages) to share with all of GitHub, or in a private repository (private packages) to share with collaborators or an organization. A repository can be connected to more than one package. To prevent confusion, make sure the README and description clearly provide information about each package.

If a new version of a package fixes a security vulnerability, you should publish a security advisory in your repository. GitHub reviews each published security advisory and may use it to send Dependabot alerts to affected repositories. For more information, see [About repository security advisories](https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/about-repository-security-advisories).

## Publishing a package

You can publish a package to GitHub Packages using any supported package client by following the same general guidelines.

1. Create or use an existing personal access token (classic) with the appropriate scopes for the task you want to accomplish. For more information, see [About permissions for GitHub Packages](https://docs.github.com/en/packages/learn-github-packages/about-permissions-for-github-packages).
2. Authenticate to GitHub Packages using your personal access token (classic) and the instructions for your package client.
3. Publish the package using the instructions for your package client.

For instructions specific to your package client, see [Working with a GitHub Packages registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry).

After you publish a package, you can view the package on GitHub. For more information, see [Viewing packages](https://docs.github.com/en/packages/learn-github-packages/viewing-packages).