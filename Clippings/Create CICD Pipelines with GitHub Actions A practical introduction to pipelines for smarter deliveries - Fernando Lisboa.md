---
title: "Create CI/CD Pipelines with GitHub Actions A practical introduction to pipelines for smarter deliveries - Fernando Lisboa"
source: "https://blog.codeminer42.com/create-ci-cd-pipelines-with-github-actions/"
author:
  - "[[Fernando Lisboa]]"
published: 2025-09-02
created: 2026-04-13
description: "Learn what CI/CD pipelines are, why they matter, and how to set up a simple workflow with GitHub Actions."
tags:
  - "clippings"
---
Continuous Integration and Continuous Delivery (or Deployment), better known as **CI/CD Pipelines**, is a pillar of modern software teams. Although it may sound like another buzzword, it’s actually about something very practical: **automating the way code moves from your local enviroment to production**. To illustrate, we’ll use a simple JavaScript/Node.js project, but don’t worry if your stack is different: the same approach applies to other languages like Ruby, Python, Java, Go, or any modern ecosystem.

Regardless of stack or project size, CI/CD helps answer key questions:

- *How can we merge code frequently without breaking things?*
- *How do we release faster, but with less risk?*

In this article, we’ll break down the concepts and set up a simple pipeline using [GitHub Actions](https://github.com/features/actions).

---

## CI vs CD: what’s the difference?

- **Continuous Integration (CI):** every time code is pushed, it’s built and validated. Fast feedback warns developers when something isn’t working.
- **Continuous Delivery (CD):** once code passes CI, it’s automatically prepared for release. The app is always in a deployable state.
- **Continuous Deployment (also CD):** the bold step. If checks pass, code is deployed to production without manual approval.

Put together, these ideas form a **CI/CD pipeline**: an automated path from development to production.

![CI/CD Pipeline Flow](https://d604h6pkko9r0.cloudfront.net/wp-content/uploads/2025/08/28193529/ci-cd-flow-desktop.png.webp)

Reference: https://www.redhat.com/en/topics/devops/what-is-ci-cd

## Why does CI/CD matter?

It comes down to **confidence and efficiency**. You want changes to be checked automatically so bugs are caught early. Once everything passes, you want deployments to happen smoothly with minimal effort.

Without CI/CD, any sort of bugs can slip into production. CI/CD reduces that risk by automating critical tasks like **linting, security audits, and tests**. CD goes further, making deployments more reliable and less error-prone.

In practice, CI/CD means fewer surprises and faster delivery: bugs are caught earlier, fixes arrive quicker, and deployments stop being a manual, risky event. Think of it as a *safety net* and an *accelerator*: fewer bugs reach users, while features arrive faster.

## Anatomy of a pipeline

A basic CI pipeline usually contains three key steps:

1. **Linting** – enforce consistency and catch obvious errors using [ESLint + Prettier](https://blog.codeminer42.com/static-analysis-matters-to-you-linters-vs-formatters/).
2. **Audit** – run security checks with [npm audit](https://docs.npmjs.com/cli/v9/commands/npm-audit/) or [yarn audit](http://classic.yarnpkg.com/lang/en/docs/cli/audit/).
3. **Tests** – make sure automated tests pass before merging.

Even with just these steps, you cover essential aspects of code quality and security. Continuous Delivery then adds build tasks to prepare code for deployment, while Continuous Deployment takes the final step and ships it live.

## GitHub Actions example

If you use GitHub, [Actions](https://github.com/features/actions) is the easiest way to get started. It runs your workflows in response to events in your repository. All you need to do is to commit a file like `.github/workflows/ci.yml`:

```yaml
name: Node.js CI

on:
  push:
    branches: [ "main" ] # set the branch you want to trigger the workflow on push
  pull_request: {} # trigger on pull requests to any branch

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: 'npm'

      - name: Install dependencies
        run: npm ci # use npm ci for clean install in CI environments

      - name: Run linter
        run: npm run lint

      - name: Audit packages
        run: npm audit --audit-level=high

      - name: Run test suite
        run: npm test
```

On each push or pull request, this workflow will:

- **Check out the repo and install Node.js** → makes sure the workflow runs in a clean environment using the Node version you’ve defined. This avoids the classic [“it works on my machine”](https://blog.codeminer42.com/docker-and-containerization/ "“it works on my machine”") problem.
- **Install dependencies in a clean environment** (`npm ci`) → ensures reproducibility by installing exactly what is in `package-lock.json`. Perfect for consistent builds.
- **Run ESLint + Prettier** → validates coding style, catches unused variables or typos early, and enforces a standard across the project. This step improves code quality *before* any functional tests run.
- **Audit dependencies for vulnerabilities** → checks for known security issues. Automated audits mean unsafe libraries are flagged as soon as they’re introduced.
- **Execute your test suite** → runs your tests to confirm core logic still works. If something breaks, you know about it instantly, not after deploy.

Together, these stages build a foundation of quality and security for your project, so every pull request gets validated in the same way. If this pipeline passes, your code is in good shape to merge. And if it fails, you’ll know exactly where and why — making fixes much faster.

## Using the Pipeline in Practice

Once your workflow is in place, every Pull Request against `main` will automatically trigger the CI check, so every new PR becomes a live report card. You can see a first run in [Pull Request #1](https://github.com/fernandollisboa/cicd-blogpost/pull/1).

The feedback loop works like this:

1. You open a PR.
2. GitHub Actions spins up the configured jobs.
3. If something fails, GitHub shows the issue directly in the PR before you merge.

![Example of a PR with failed actions](https://i0.wp.com/d604h6pkko9r0.cloudfront.net/wp-content/uploads/2025/08/28183622/Screenshot-2025-08-28-183409-1024x337.webp?resize=1024%2C337&ssl=1)

By clicking on the failed action, you can inspect detailed logs. In this case, the error was just a linting violation:

![Example of a failed lint workflow run](https://i0.wp.com/d604h6pkko9r0.cloudfront.net/wp-content/uploads/2025/08/28183135/Screenshot-2025-08-28-182615.webp?w=1200&ssl=1)

The fix? Correct the issue, push again, and the pipeline reruns automatically. This time, with all checks passing, the PR displays a green checkmark:

![Pull Request with all tests passing](https://i0.wp.com/d604h6pkko9r0.cloudfront.net/wp-content/uploads/2025/08/28184914/Screenshot-2025-08-28-184858.webp?w=1200&ssl=1)

## Parallelizing the Work

Now, let’s address performance. In the first version of our workflow, **lint, audit, and tests** ran sequentially in a single job. That worked, but the total runtime could get long, especially with multiple PRs in flight.

A simple optimization is to **split these steps into separate jobs** that run in parallel. You can check the change in [Pull Request #2](https://github.com/fernandollisboa/cicd-blogpost/pull/2).

Here’s the updated workflow:

```yaml
name: Node.js CI (Parallel)

on:
  push:
    branches: ['main']
  pull_request: {}

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          cache: 'npm'
      - run: npm ci
      - run: npm run lint

  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: 'npm'
      - run: npm ci
      - run: npm audit --audit-level=high

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: 'npm'
      - run: npm ci
      - run: npm test
```

And here is how it looks when triggered from a PR:

This adjustment sped up the feedback in practice: each check runs independently, so you don’t have to wait for lint to finish before tests start. Failures also show up more clearly because they’re isolated in separate jobs. The result: faster feedback and clearer failures. And for developers, faster feedback means faster progress.

## What About CD?

CI is great, but the full story only comes with CD: Continuous Delivery and Deployment. Once your pipeline goes green, the next step is packaging and releasing your application so that other environments can run it consistently.

For small to medium-sized apps, CD usually means:

- **Deploy to a platform**: services like [Vercel](https://vercel.com/) or [Heroku](https://www.heroku.com/) integrate directly with GitHub. After a merge, they automatically build and redeploy your app. This is the most straightforward way to get started if you don’t need container orchestration.
- **Dockerized deployment**: For more flexibility, you can wrap your app in a [Docker](https://blog.codeminer42.com/docker-and-containerization/) image and push that image to a registry. From there, [Kubernetes](https://kubernetes.io/ "Kubernetes"), [ECS](https://aws.amazon.com/pt/ecs/ "ECS"), or another orchestrator can pick it up and roll it out. Containers are the most common way teams standardize deployments across multiple environments.

With GitHub Actions, adding deployment to your pipeline is simply another job that runs after CI succeeds. Below is an example targeting [Docker Hub](https://hub.docker.com/ "Docker Hub"):

```yaml
deploy:
  needs: [lint, audit, test] # wait for all CI jobs to complete
  runs-on: ubuntu-latest
  if: github.ref == 'refs/heads/main' # only deploy from main branch
  steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Set up QEMU
      uses: docker/setup-qemu-action@v3

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Login to Docker Hub
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_TOKEN }}

    - name: Docker meta
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ secrets.DOCKER_USERNAME }}/cicd-blogpost
        tags: |
          type=sha

    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
```

This deployment job will:

- **Wait for all CI steps (lint, audit, and test) to pass** before running.
- **Trigger only on the `main` branch**, preventing unreviewed code from being deployed.
- **Build a Docker image** from the current source.
- **Tag it with the commit SHA**, giving you immutable, traceable builds.
- **Push the image to the container registry**, where it’s ready for use by staging or production environments

The SHA-based tags matter because they let you promote the *exact same artifact* across environments — no rebuilding required. That way, what you tested in CI is precisely what runs in production.

Even if you don’t set up full CD right away, having CI in place already transforms your development workflow dramatically.

## Best Practices & Key Takeaways

- **Keep pipelines fast:** developers won’t wait 30 minutes for feedback.
- **Start small:** begin with a single job running lint + audit + tests, then add complexity later.
- **Fail early:** let linting or static checks break first before wasting CI minutes.
- **Split jobs when needed:** parallel execution speeds up pipelines and makes debugging clearer.
- **Protect your main branch:** only green builds should be merged.

By exploring GitHub Actions, you get a workflow that not only protects your main branch but also scales well for teams pushing code frequently.

## Other tools you’ll meet

The ecosystem is rich, and you’ll hear about many tools that complement or rival GitHub Actions:

- **[GitLab CI](https://docs.gitlab.com/ci/ "GitLab CI") / [CircleCI](https://circleci.com/ "CircleCI")** – popular managed CI/CD services.
- **[Jenkins](https://www.jenkins.io/ "Jenkins")** – a classic, still widely used.
- **[ArgoCD](https://argo-cd.readthedocs.io/en/stable/ "ArgoCD")** – modern Kubernetes-native deployments.

For most projects you’ll encounter, GitHub Actions (and its Gitlab equilavent) remains one of the simplest and most practical entry points.

## Wrapping up

CI/CD may seem like extra work at first, but it pays off quickly. Automating checks and deployments transforms the old [*“it works on my machine”*](https://blog.codeminer42.com/docker-and-containerization/ "*“it works on my machine”*") culture into a reliable, repeatable process.

Start small: linting, auditing, and testing. Then, when you’re ready, add deployment steps. Whether deploying to Vercel, Docker, or Kubernetes, the principles stay the same: ship faster, with confidence.

The full example code used here is available [on GitHub](https://github.com/fernandollisboa/cicd-blogpost/).

---

## The Miners’ Guide to Code Crafting

> This post is part of our [‘The Miners’ Guide to Code Crafting’](https://blog.codeminer42.com/category/posts/the-miners-guide-to-code-crafting/) series, designed to help aspiring developers learn and grow. Stay tuned for more and continue your coding journey with us! Check out the full summary [here](https://blog.codeminer42.com/the-miners-guide-to-crafting-code-gearing-up/#:~:text=Summary%20of%20Posts%3A%20The%20Miners%E2%80%99%20Guide%20to%20Code%20Crafting).