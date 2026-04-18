---
title: "What is serverless computing?"
source: "https://www.cloudflare.com/learning/serverless/what-is-serverless/"
author:
published:
created: 2026-04-15
description: "Learn about what serverless computing is, and how FaaS enables developers to write and deploy code in a serverless architecture."
tags:
  - "clippings"
---
Preview Mode

[Documentation](https://staging.mrk.cfdata.org/mrk/redwood-blade-repository/)

## What is serverless computing? | Serverless definition

Serverless computing is a method of providing backend services on an as-used basis. Servers are still used, but a company that gets backend services from a serverless vendor is charged based on usage, not a fixed amount of bandwidth or number of servers.

#### Learning Objectives

After reading this article you will be able to:

Copy article link

## What is serverless computing?

Serverless computing is a method of providing backend services on an as-used basis. A serverless provider allows users to write and [deploy code](https://www.cloudflare.com/learning/serverless/how-to-deploy-app-or-website/) without the hassle of worrying about the underlying infrastructure. A company that gets backend services from a serverless vendor is charged based on their computation and do not have to reserve and pay for a fixed amount of bandwidth or number of servers, as the service is auto-scaling. Note that despite the name serverless, physical servers are still used but developers do not need to be aware of them.

In the early days of the web, anyone who wanted to build a web application had to own the physical hardware required to run a server, which is a cumbersome and expensive undertaking.

Then came [cloud computing](https://www.cloudflare.com/learning/cloud/what-is-the-cloud/), where fixed numbers of servers or amounts of server space could be rented remotely. Developers and companies who rent these fixed units of server space generally over-purchase to ensure that a spike in traffic or activity will not exceed their monthly limits and break their applications. This means that much of the server space that gets paid for can go to waste. Cloud vendors have introduced auto-scaling models to address the issue, but even with auto-scaling an unwanted spike in activity, such as a [DDoS Attack](https://www.cloudflare.com/learning/ddos/what-is-a-ddos-attack/), could end up being very expensive.

![Benefits of Serverless](https://cf-assets.www.cloudflare.com/slt3lc6tev37/7nyIgiecrfe9W6TfmJRpNh/dfc5434659e31300d1918d4163dfb263/benefits-of-serverless.svg)

Serverless computing allows developers to purchase backend services on a flexible ‘pay-as-you-go’ basis, meaning that developers only have to pay for the services they use. This is like switching from a cell phone data plan with a monthly fixed limit, to one that only charges for each byte of data that actually gets used.

The term ‘serverless’ is somewhat misleading, as there are still servers providing these backend services, but all of the server space and infrastructure concerns are handled by the vendor. Serverless means that the developers can do their work without having to worry about servers at all.

## What are backend services? What’s the difference between frontend and backend?

Application development is generally split into two realms: the frontend and the backend. The frontend is the part of the application that users see and interact with, such as the visual layout. The backend is the part that the user doesn’t see; this includes the server where the application's files live and the database where user data and business logic is persisted.

![Frontend vs Backend of an Application](https://www.cloudflare.com/img/learning/serverless/what-is-serverless/frontend-vs-backend.svg)

For example, let’s imagine a website that sells concert tickets. When a user types a website address into the browser window, the browser sends a request to the backend server, which responds with the website data. The user will then see the frontend of the website, which can include content such as text, images, and form fields for the user to fill out. The user can then interact with one of the form fields on the frontend to search for their favorite musical act. When the user clicks on ‘submit’, this will trigger another request to the backend. The backend code checks its database to see if a performer with this name exists, and if so, when they will be playing next, and how many tickets are available. The backend will then pass that data back to the frontend, and the frontend will display the results in a way that makes sense to the user. Similarly, when the user creates an account and enters financial information to buy the tickets, another back-and-forth communication between the frontend and backend will occur.

## What kind of backend services can serverless computing provide?

Most serverless providers offer database and storage services to their customers, and many also have [Function-as-a-Service (FaaS)](https://www.cloudflare.com/learning/serverless/glossary/function-as-a-service-faas/) platforms, like [Cloudflare Workers](https://www.cloudflare.com/developer-platform/workers/). FaaS allows developers to execute small pieces of code on the [network edge](https://www.cloudflare.com/learning/serverless/glossary/what-is-edge-computing/). With FaaS, developers can build a modular architecture, making a codebase that is more scalable without having to spend resources on maintaining the underlying backend. [Learn more about FaaS >>](https://www.cloudflare.com/learning/serverless/glossary/function-as-a-service-faas/)

## What are the advantages of serverless computing?

- **Lower costs** - Serverless computing is generally very cost-effective, as traditional cloud providers of backend services (server allocation) often result in the user paying for unused space or idle CPU time.
- **Simplified scalability** - Developers using serverless architecture don’t have to worry about policies to scale up their code. The serverless vendor handles all of the scaling on demand.
- **Simplified backend code** - With FaaS, developers can create simple functions that independently perform a single purpose, like making an API call.
- **Quicker turnaround** - Serverless architecture can significantly cut time to market. Instead of needing a complicated deploy process to roll out bug fixes and new features, developers can add and modify code on a piecemeal basis.

Learn more about [the benefits of serverless computing.](https://www.cloudflare.com/learning/serverless/why-use-serverless/)

## How does serverless compare to other cloud backend models?

A couple of technologies that are often conflated with serverless computing are Backend-as-a-Service and Platform-as-a-Service. Although they share similarities, these models do not necessarily meet the requirements of serverless.

**Backend-as-a-service (BaaS)** is a service model where a cloud provider offers backend services such as data storage, so that developers can focus on writing front-end code. But while serverless applications are event-driven and run on the edge, BaaS applications may not meet either of these requirements. [Learn more about BaaS >>](https://www.cloudflare.com/learning/serverless/glossary/backend-as-a-service-baas/)

**Platform-as-a-service (PaaS)** is a model where developers essentially rent all the necessary tools to develop and deploy applications from a cloud provider, including things like operating systems and middleware. However PaaS applications are not as easily scalable as serverless applications. PaaS also don’t necessarily run on the edge and often have a noticeable startup delay that isn’t present in serverless applications. [Learn more about PaaS >>](https://www.cloudflare.com/learning/serverless/glossary/platform-as-a-service-paas/)

**Infrastructure-as-a-service (IaaS)** is a catchall term for cloud vendors hosting infrastructure on behalf of their customers. IaaS providers may offer serverless functionality, but the terms are not synonymous. [Learn more about IaaS >>](https://www.cloudflare.com/learning/cloud/what-is-iaas/)

## What is next for serverless?

Serverless computing continues to evolve as serverless providers come up with solutions to overcome some of its drawbacks. One of these drawbacks is cold starts.

Typically when a particular serverless function has not been called in a while, the provider shuts down the function to save energy and avoid over-provisioning. The next time a user runs an application that calls that function, the serverless provider will have to spin it up fresh and start hosting that function again. This startup time adds significant latency, which is known as a ‘cold start’.

Once the function is up and running it will be served much more rapidly on subsequent requests (warm starts), but if the function is not requested again for a while, the function will once again go dormant. This means the next user to request that function will experience a cold start. Up until fairly recently, cold starts were considered a necessary trade-off of using serverless functions.

Cloudflare Workers has addressed this problem by spinning up serverless functions in advance, during the [TLS handshake](https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake/). Since Workers functions spin up at the edge in a very short amount of time, even shorter than the time required to complete the handshake, the result is an [FaaS platform with zero cold starts](https://blog.cloudflare.com/eliminating-cold-starts-with-cloudflare-workers/). This approach embodies the principle that The Network is the Computer®. To get started with Cloudflare Workers, see our [Developer documentation](https://developers.cloudflare.com/workers/).

As more and more of the drawbacks of using serverless get addressed and the popularity of edge computing grows, we can expect to see serverless architecture becoming more widespread.

## FAQs

#### What does "pay-as-you-go backend services" mean in serverless computing?

Serverless computing uses a pay-as-you-go model, where developers only pay for the backend computational resources they actually use, instead of paying for reserved server space or bandwidth.

#### What is Function-as-a-Service (FaaS)?

Function-as-a-Service (FaaS) is a type of serverless platform that lets developers run small, modular pieces of code in response to events, without managing any underlying infrastructure.

#### What is auto-scaling in a serverless environment?

In serverless computing, auto-scaling means the provider automatically allocates or reduces computational resources as needed, so developers do not have to manage scaling policies themselves.

#### How does serverless computing relate to frontend and backend services?

Serverless computing specifically addresses backend services, handling server-side logic, data processing, and infrastructure management that users do not directly see.

#### How does serverless computing improve cost efficiency?

Serverless computing reduces costs by eliminating the need to pay for idle server space or unused CPU time, since charges are based only on actual usage.

#### What is edge computing and how does it relate to serverless?

Edge computing in serverless means that functions can be deployed closer to end users, reducing latency and improving application performance.

#### What is cold start mitigation in serverless platforms?

Cold start mitigation refers to techniques that reduce the delay when starting dormant serverless functions. Serverless providers with cold start mitigation features in place spin up functions at the edge in advance, helping to eliminate delays in execution.