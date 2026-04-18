---
title: "Connecting a repository to a package"
source: "https://docs.github.com/en/packages/learn-github-packages/connecting-a-repository-to-a-package"
author:
published:
created: 2026-04-13
description: "You can connect a repository to a package on GitHub."
tags:
  - "clippings"
---
When you publish a package that is scoped to a personal account or an organization, the package is not linked to a repository by default. If you connect a package to a repository, the package's landing page will show information and links from the repository, such as the README. You can also choose to have the package inherit its access permissions from the linked repository. For more information, see [Configuring a package's access control and visibility](https://docs.github.com/en/packages/learn-github-packages/configuring-a-packages-access-control-and-visibility).

## Connecting a repository to a user-scoped package on GitHub

1. On GitHub, navigate to the main page of your personal account.
2. In the top right corner of GitHub, click your profile picture, then click **Your profile**.
	![Screenshot of the dropdown menu under @octocat's profile picture. "Your profile" is outlined in dark orange.](https://docs.github.com/assets/cb-13593/mw-1440/images/help/profile/profile-button-avatar-menu-global-nav-update.webp)
3. On your profile page, in the header, click the **Packages** tab.
4. Search for and then click the name of the package that you want to manage.
5. Under your package versions, click **Connect repository**.
6. Select a repository to link to the package, then click **Connect repository**.

## Connecting a repository to an organization-scoped package on GitHub

1. On GitHub, navigate to the main page of your organization.
2. Under your organization name, click the **Packages** tab.
	![Screenshot of @octo-org's profile page. The "Packages" tab is highlighted with an orange outline.](https://docs.github.com/assets/cb-82633/mw-1440/images/help/package-registry/org-tab-for-packages-with-overview-tab.webp)
3. Search for and then click the name of the package that you want to manage.
4. Under your package versions, click **Connect repository**.
5. Select a repository to link to the package, then click **Connect repository**.

## Connecting a repository to a container image using the command line

1. In your Dockerfile, add this line, replacing `OWNER` and `REPO` with your details:
	```shell
	LABEL org.opencontainers.image.source=https://github.com/OWNER/REPO
	```
	For example, if you're the user `octocat` and own `my-repo` you would add this line to your Dockerfile:
	```shell
	LABEL org.opencontainers.image.source=https://github.com/octocat/my-repo
	```
	For more information, see [LABEL](https://docs.docker.com/engine/reference/builder/#label) in the official Docker documentation and [Pre-defined Annotation Keys](https://github.com/opencontainers/image-spec/blob/main/annotations.md#pre-defined-annotation-keys) in the `opencontainers/image-spec` repository.
2. Build your container image. This example builds an image from the Dockerfile in the current directory and assigns the image name `hello_docker`.
	```shell
	docker build -t hello_docker .
	```
3. Optionally, review the details of the Docker image you just created.
	```shell
	$ docker images
	> REPOSITORY          TAG         IMAGE ID       CREATED         SIZE
	> hello_docker        latest      142e665b1faa   5 seconds ago   125MB
	> redis               latest      afb5e116cac0   3 months ago    111MB
	> alpine              latest      a6215f271958   5 months ago    5.29MB
	```
4. Assign a name and hosting destination to your Docker image.
	```shell
	docker tag IMAGE_NAME ghcr.io/NAMESPACE/NEW_IMAGE_NAME:TAG
	```
	Replace `NAMESPACE` with the name of the personal account or organization to which you want the package to be scoped.
	For example:
	```shell
	docker tag 38f737a91f39 ghcr.io/octocat/hello_docker:latest
	```
5. If you haven't already, authenticate to the Container registry. For more information, see [Working with the Container registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-to-the-container-registry).
	```shell
	$ echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin
	> Login Succeeded
	```
6. Push your container image to the Container registry.
	```shell
	docker push ghcr.io/NAMESPACE/IMAGE-NAME:TAG
	```
	For example:
	```shell
	docker push ghcr.io/octocat/hello_docker:latest
	```

## Unlinking a repository from a package on GitHub

1. On GitHub, navigate to the settings page of the Package you'd like to unlink.
2. On the Package settings page, you will see a Repository source section. If this section is not present, then the Package is not currently linked to a repository.
3. Click on the trash icon in the top right corner of the Repository source section.

> It is possible that the Repository source section exists, but there is no trash icon present. This is because a repository source has been defined as part of the packaged code i.e. a `package.json` file, `.gemspec` file, however, it is not actually linked to a repository on GitHub. To link the package to a repository, you will need to follow the steps in the section above.

1. Confirm that you would like to unlink the repository from the package with the dialogue.

## Migrating a package to another repository

If you currently have a package linked to a repository and you would like to link it to a different repository, this can be done by unlinking the package from the current repository and linking it to the new repository.

1. Follow the steps to unlink it, see [Unlinking a repository from a package on GitHub](https://docs.github.com/en/packages/learn-github-packages/connecting-a-repository-to-a-package#unlinking-a-repository-from-a-package-on-github).
2. Follow the steps to link the package to the new repository, see [Connecting a repository to an organization-scoped package on GitHub](https://docs.github.com/en/packages/learn-github-packages/connecting-a-repository-to-a-package#connecting-a-repository-to-an-organization-scoped-package-on-github) or [Connecting a repository to a user-scoped package on GitHub](https://docs.github.com/en/packages/learn-github-packages/connecting-a-repository-to-a-package#connecting-a-repository-to-a-user-scoped-package-on-github).