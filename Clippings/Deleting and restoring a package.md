---
title: "Deleting and restoring a package"
source: "https://docs.github.com/en/packages/learn-github-packages/deleting-and-restoring-a-package"
author:
published:
created: 2026-04-13
description: "Learn how to delete or restore a package."
tags:
  - "clippings"
---
## Package deletion and restoration support on GitHub

On GitHub if you have the required access, you can delete:

- An entire private package
- An entire public package, if there's not more than 5000 downloads of any version of the package
- A specific version of a private package
- A specific version of a public package, if the package version doesn't have more than 5,000 downloads

On GitHub, you can also restore an entire package or package version, if:

- You restore the package within 30 days of its deletion.
- The same package namespace is still available and not used for a new package.

## Packages API support

You can use the REST API to manage your packages. For more information, see the [REST API endpoints for packages](https://docs.github.com/en/rest/packages).

With registries that support granular permissions, you can use a `GITHUB_TOKEN` in a GitHub Actions workflow to delete or restore packages using the REST API. The token must have `admin` permission to the package. If your workflow publishes a package, the `admin` role is granted by default to the repository where the workflow is stored. For existing packages not published by a workflow, you need to grant the repository the `admin` role to be able to use a GitHub Actions workflow to delete or restore packages using the REST API. For more information, see [Configuring a package's access control and visibility](https://docs.github.com/en/packages/learn-github-packages/configuring-a-packages-access-control-and-visibility#ensuring-workflow-access-to-your-package).

For certain registries, you can use GraphQL to delete a version of a private package.

You cannot use the GitHub Packages GraphQL API with registries that support granular permissions. For the registries that **only** support repository-scoped permissions, and can be used with the GraphQL API, see [About permissions for GitHub Packages](https://docs.github.com/en/packages/learn-github-packages/about-permissions-for-github-packages#permissions-for-repository-scoped-packages).

## Required permissions to delete or restore a package

With registries that support granular permissions, you can choose to allow packages to be scoped to a user or an organization, or linked to a repository.

To delete a package that has granular permissions separate from a repository, such as container images stored at `https://ghcr.io/NAMESPACE/PACKAGE-NAME` or packages stored at `https://npm.pkg.github.com/NAMESPACE/PACKAGE-NAME` (where `NAMESPACE` is the name of the personal account or organization to which the package is scoped), you must have admin access to the package. For more information, see [About permissions for GitHub Packages](https://docs.github.com/en/packages/learn-github-packages/about-permissions-for-github-packages).

For packages that inherit their access permissions from repositories, you can delete a package if you have admin permissions to the repository.

Some registries **only** support repository-scoped packages. For a list of these registries, see [About permissions for GitHub Packages](https://docs.github.com/en/packages/learn-github-packages/about-permissions-for-github-packages#permissions-for-repository-scoped-packages).

## Deleting a package version

### Deleting a version of a repository-scoped package on GitHub

To delete a version of a repository-scoped package, you must have admin permissions to the repository in which the package is published. For more information, see [Required permissions](#required-permissions-to-delete-or-restore-a-package).

1. On GitHub, navigate to the main page of the repository.
2. In the right sidebar of your repository, click **Packages**.
	![Screenshot of the sidebar of a repository page. The "Packages" section is outlined in orange.](https://docs.github.com/assets/cb-208326/mw-1440/images/help/package-registry/packages-from-repo.webp)
3. Search for and then click the name of the package that you want to manage.
4. Under the "Recent Versions" list of packages, click **View and manage all versions**.
	![Screenshot of a package's "Recent Versions" section. Underneath, the "View and manage all versions" link is highlighted with an orange outline.](https://docs.github.com/assets/cb-34949/mw-1440/images/help/package-registry/packages-recent-versions-manage-link.webp)
5. In the list of packages, find the version of the package that you want to delete.
	- *If your package is a container*, to the right of the package version click , then select **Delete version** from the dropdown menu.
		![Screenshot of a package version kebab button, expanded to show the menu. The "Delete version" link in the menu is outlined in orange.](https://docs.github.com/assets/cb-54845/mw-1440/images/help/package-registry/delete-container-package-version.webp)
		- *For types of packages other than containers*, to the right of the package version click **Delete**.
		![Screenshot of a package version with a "Delete" button. The button is highlighted with an orange outline.](https://docs.github.com/assets/cb-38531/mw-1440/images/help/package-registry/delete-noncontainer-package-version.webp)
6. To confirm deletion, type the package name and click **I understand the consequences, delete this version**.

### Deleting a version of a repository-scoped package with GraphQL

For certain registries, you can use GraphQL to delete a version of a private package.

You cannot use the GitHub Packages GraphQL API with registries that support granular permissions. For the registries that **only** support repository-scoped permissions, and can be used with the GraphQL API, see [About permissions for GitHub Packages](https://docs.github.com/en/packages/learn-github-packages/about-permissions-for-github-packages#permissions-for-repository-scoped-packages). For information on using the REST API instead, see the [REST API endpoints for packages](https://docs.github.com/en/rest/packages).

Use the `deletePackageVersion` mutation in the GraphQL API. You must use a personal access token (classic) with the `read:packages`, `delete:packages`, and `repo` scopes. For more information about personal access tokens (classic), see [Introduction to GitHub Packages](https://docs.github.com/en/packages/learn-github-packages/introduction-to-github-packages#authenticating-to-github-packages).

The following example demonstrates how to delete a package version, using a `packageVersionId` of `MDIyOlJlZ2lzdHJ5UGFja2FnZVZlcnNpb243MTExNg`.

```shell
curl -X POST \
-H "Accept: application/vnd.github.package-deletes-preview+json" \
-H "Authorization: bearer TOKEN" \
-d '{"query":"mutation { deletePackageVersion(input:{packageVersionId:\"MDIyOlJlZ2lzdHJ5UGFja2FnZVZlcnNpb243MTExNg==\"}) { success }}"}' \
HOSTNAME/graphql
```

To find all of the private packages you have published to GitHub Packages, along with the version IDs for the packages, you can use the `packages` connection through the `repository` object. You will need a personal access token (classic) with the `read:packages` and `repo` scopes. For more information, see the [`packages`](https://docs.github.com/en/graphql/reference/objects#repository) connection or the [`PackageOwner`](https://docs.github.com/en/graphql/reference/interfaces#packageowner) interface.

For more information about the `deletePackageVersion` mutation, see [Mutations](https://docs.github.com/en/graphql/reference/mutations#deletepackageversion).

You cannot directly delete an entire package using GraphQL, but if you delete every version of a package, the package will no longer show on GitHub.

### Deleting a version of a user-scoped package on GitHub

To delete a specific version of a user-scoped package on GitHub, such as for a Docker image at `ghcr.io`, use these steps. To delete an entire package, see [Deleting an entire user-scoped package on GitHub](#deleting-an-entire-user-scoped-package-on-github).

To review who can delete a package version, see [Required permissions](#required-permissions-to-delete-or-restore-a-package).

1. On GitHub, navigate to the main page of your personal account.
2. In the top right corner of GitHub, click your profile picture, then click **Your profile**.
	![Screenshot of the dropdown menu under @octocat's profile picture. "Your profile" is outlined in dark orange.](https://docs.github.com/assets/cb-13593/mw-1440/images/help/profile/profile-button-avatar-menu-global-nav-update.webp)
3. On your profile page, in the header, click the **Packages** tab.
4. Search for and then click the name of the package that you want to manage.
5. Under the "Recent Versions" list of packages, click **View and manage all versions**.
	![Screenshot of a package's "Recent Versions" section. Underneath, the "View and manage all versions" link is highlighted with an orange outline.](https://docs.github.com/assets/cb-34949/mw-1440/images/help/package-registry/packages-recent-versions-manage-link.webp)
6. In the list of packages, find the version of the package that you want to delete.
	- *If your package is a container*, to the right of the package version click , then select **Delete version** from the dropdown menu.
		![Screenshot of a package version kebab button, expanded to show the menu. The "Delete version" link in the menu is outlined in orange.](https://docs.github.com/assets/cb-54845/mw-1440/images/help/package-registry/delete-container-package-version.webp)
		- *For types of packages other than containers*, to the right of the package version click **Delete**.
		![Screenshot of a package version with a "Delete" button. The button is highlighted with an orange outline.](https://docs.github.com/assets/cb-38531/mw-1440/images/help/package-registry/delete-noncontainer-package-version.webp)
7. In the confirmation box, type the name of the package to confirm you want to delete the chosen version of it.
8. Click **I understand the consequences, delete this version**.

### Deleting a version of an organization-scoped package on GitHub

To delete a specific version of an organization-scoped package on GitHub, such as for a Docker image at `ghcr.io`, use these steps. To delete an entire package, see [Deleting an entire organization-scoped package on GitHub](#deleting-an-entire-organization-scoped-package-on-github).

To review who can delete a package version, see [Required permissions to delete or restore a package](#required-permissions-to-delete-or-restore-a-package).

1. On GitHub, navigate to the main page of your organization.
2. Under your organization name, click the **Packages** tab.
	![Screenshot of @octo-org's profile page. The "Packages" tab is highlighted with an orange outline.](https://docs.github.com/assets/cb-82633/mw-1440/images/help/package-registry/org-tab-for-packages-with-overview-tab.webp)
3. Search for and then click the name of the package that you want to manage.
4. Under the "Recent Versions" list of packages, click **View and manage all versions**.
	![Screenshot of a package's "Recent Versions" section. Underneath, the "View and manage all versions" link is highlighted with an orange outline.](https://docs.github.com/assets/cb-34949/mw-1440/images/help/package-registry/packages-recent-versions-manage-link.webp)
5. In the list of packages, find the version of the package that you want to delete.
	- *If your package is a container*, to the right of the package version click , then select **Delete version** from the dropdown menu.
		![Screenshot of a package version kebab button, expanded to show the menu. The "Delete version" link in the menu is outlined in orange.](https://docs.github.com/assets/cb-54845/mw-1440/images/help/package-registry/delete-container-package-version.webp)
		- *For types of packages other than containers*, to the right of the package version click **Delete**.
		![Screenshot of a package version with a "Delete" button. The button is highlighted with an orange outline.](https://docs.github.com/assets/cb-38531/mw-1440/images/help/package-registry/delete-noncontainer-package-version.webp)
6. In the confirmation box, type the name of the package to confirm you want to delete the chosen version of it.
7. Click **I understand the consequences, delete this version**.

## Deleting an entire package

### Deleting an entire repository-scoped package on GitHub

To delete an entire repository-scoped package, you must have admin permissions to the repository that owns the package. For more information, see [Required permissions](#required-permissions-to-delete-or-restore-a-package).

1. On GitHub, navigate to the main page of the repository.
2. In the right sidebar of your repository, click **Packages**.
	![Screenshot of the sidebar of a repository page. The "Packages" section is outlined in orange.](https://docs.github.com/assets/cb-208326/mw-1440/images/help/package-registry/packages-from-repo.webp)
3. Search for and then click the name of the package that you want to manage.
4. On your package's landing page, on the right-hand side, click **Package settings**.
	![Screenshot of a package's landing page. In the lower right corner, "Package settings" is highlighted with an orange outline.](https://docs.github.com/assets/cb-66752/mw-1440/images/help/package-registry/package-settings.webp)
5. At the bottom of the page, under "Danger Zone", click **Delete this package**.
6. To confirm, review the confirmation message, enter your package name, and click **I understand, delete this package.**

### Deleting an entire user-scoped package on GitHub

To review who can delete a package, see [Required permissions](#required-permissions-to-delete-or-restore-a-package).

1. On GitHub, navigate to the main page of your personal account.
2. In the top right corner of GitHub, click your profile picture, then click **Your profile**.
	![Screenshot of the dropdown menu under @octocat's profile picture. "Your profile" is outlined in dark orange.](https://docs.github.com/assets/cb-13593/mw-1440/images/help/profile/profile-button-avatar-menu-global-nav-update.webp)
3. On your profile page, in the header, click the **Packages** tab.
4. Search for and then click the name of the package that you want to manage.
5. On your package's landing page, on the right-hand side, click **Package settings**.
	![Screenshot of a package's landing page. In the lower right corner, "Package settings" is highlighted with an orange outline.](https://docs.github.com/assets/cb-66752/mw-1440/images/help/package-registry/package-settings.webp)
6. At the bottom of the page, under "Danger zone", click **Delete this package**.
7. In the confirmation box, type the name of the package to confirm you want to delete it.
8. Click **I understand the consequences, delete this package**.

### Deleting an entire organization-scoped package on GitHub

To review who can delete a package, see [Required permissions](#required-permissions-to-delete-or-restore-a-package).

1. On GitHub, navigate to the main page of your organization.
2. Under your organization name, click the **Packages** tab.
	![Screenshot of @octo-org's profile page. The "Packages" tab is highlighted with an orange outline.](https://docs.github.com/assets/cb-82633/mw-1440/images/help/package-registry/org-tab-for-packages-with-overview-tab.webp)
3. Search for and then click the name of the package that you want to manage.
4. On your package's landing page, on the right-hand side, click **Package settings**.
	![Screenshot of a package's landing page. In the lower right corner, "Package settings" is highlighted with an orange outline.](https://docs.github.com/assets/cb-66752/mw-1440/images/help/package-registry/package-settings.webp)
5. At the bottom of the page, under "Danger zone", click **Delete this package**.
6. In the confirmation box, type the name of the package to confirm you want to delete it.
7. Click **I understand the consequences, delete this package**.

## Restoring packages

You can restore a deleted package or version if:

- You restore the package within 30 days of its deletion.
- The same package namespace and version is still available and not reused for a new package.

For example, if you're the user `octocat`, and you have a deleted RubyGems package named `my-package` that was scoped to the repo `octocat/my-repo`, then you can only restore the package if the package namespace `rubygem.pkg.github.com/octocat/my-repo/my-package` is still available, and 30 days have not yet passed.

To restore a deleted package, you must also meet one of these permission requirements:

- For repository-scoped packages: You have admin permissions to the repository in which the deleted package is published.
- For user-account scoped packages: The deleted package is scoped to your personal account.
- For organization-scoped packages: You have admin permissions to the deleted package in the organization to which the package is scoped.

For more information, see [Required permissions](#required-permissions-to-delete-or-restore-a-package).

Once the package is restored, the package will use the same namespace it did before. If the same package namespace is not available, you will not be able to restore your package. In this scenario, to restore the deleted package, you must delete the new package that uses the deleted package's namespace first.

### Restoring a package in an organization

You can restore a deleted package through your organization account settings, as long as the package was in a repository owned by the organization or had granular permissions and was scoped to your organization account.

To review who can restore a package in an organization, see [Required permissions](#required-permissions-to-delete-or-restore-a-package).

1. On GitHub, navigate to the main page of the organization.
2. Under your organization name, click **Settings**. If you cannot see the "Settings" tab, select the dropdown menu, then click **Settings**.
	![Screenshot of the tabs in an organization's profile. The "Settings" tab is outlined in dark orange.](https://docs.github.com/assets/cb-49309/mw-1440/images/help/discussions/org-settings-global-nav-update.webp)
3. On the left, click **Packages**.
4. Under "Deleted Packages", next to the package you want to restore, click **Restore**.
5. To confirm, type the name of the package and click **I understand the consequences, restore this package**.

### Restoring a user-account scoped package

You can restore a deleted package through your personal account settings, if the package was in one of your repositories or scoped to your personal account. For more information, see [Required permissions](#required-permissions-to-delete-or-restore-a-package).

1. In the upper-right corner of any page on GitHub, click your profile picture, then click **Settings**.
2. In the left sidebar, click **Packages**.
3. Under "Deleted Packages", next to the package you want to restore, click **Restore**.
4. To confirm, type the name of the package and click **I understand the consequences, restore this package**.

### Restoring a package version

You can restore a package version from your package's landing page. To review who can restore a package, see [Required permissions](#required-permissions-to-delete-or-restore-a-package).

1. Navigate to your package's landing page.
2. Search for and then click the name of the package that you want to manage.
3. On your package's landing page, on the right-hand side, click **Package settings**.
	![Screenshot of a package's landing page. In the lower right corner, "Package settings" is highlighted with an orange outline.](https://docs.github.com/assets/cb-66752/mw-1440/images/help/package-registry/package-settings.webp)
4. Under the "Recent Versions" list of packages, click **View and manage all versions**.
	![Screenshot of a package's "Recent Versions" section. Underneath, the "View and manage all versions" link is highlighted with an orange outline.](https://docs.github.com/assets/cb-34949/mw-1440/images/help/package-registry/packages-recent-versions-manage-link.webp)
5. At the top right corner of the list of package versions, use the **Select versions view** dropdown and select **Deleted**.
	![Screenshot of a list of package versions. The "Deleted" selection in the versions view is highlighted with an orange outline.](https://docs.github.com/assets/cb-57396/mw-1440/images/help/package-registry/versions-drop-down-menu.webp)
6. Next to the deleted package version you want to restore, click **Restore**.
7. To confirm, click **I understand the consequences, restore this version.**