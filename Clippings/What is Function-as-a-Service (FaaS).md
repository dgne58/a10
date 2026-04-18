---
title: "What is Function-as-a-Service (FaaS)?"
source: "https://www.cloudflare.com/learning/serverless/glossary/function-as-a-service-faas/"
author:
published:
created: 2026-04-15
description: "FaaS is a serverless backend service allowing developers to write modular pieces of code on the fly that can be executed in response to certain events."
tags:
  - "clippings"
---
Preview Mode

[Documentation](https://staging.mrk.cfdata.org/mrk/redwood-blade-repository/)

FaaS is a serverless backend service allowing developers to write modular pieces of code on the fly that can be executed in response to certain events.

#### Learning Objectives

After reading this article you will be able to:

- Define FaaS
- Explore the advantages and disadvantages of FaaS
- Describe why a large edge network is essential to FaaS application performance

Copy article link

## What is Function-as-a-Service?

Function-as-a-Service (FaaS) is a [serverless](https://www.cloudflare.com/learning/serverless/what-is-serverless/) way to execute modular pieces of code on the edge. FaaS lets developers write and update a piece of code on the fly, which can then be executed in response to an event, such as a user clicking on an element in a web application. This makes it easy to scale code and is a cost-efficient way to implement [microservices](https://www.cloudflare.com/learning/serverless/glossary/serverless-microservice/).

## What are microservices?

If a web application were a work of visual art, using microservice architecture would be like making the art out of a collection of mosaic tiles. The artist can easily add, replace, and repair one tile at a time. Monolithic architecture would be like painting the entire work on a single piece of canvas.

![Microservices vs Monolithic Architecture](https://www.cloudflare.com/img/learning/serverless/glossary/function-as-a-service-faas/monolithic-application-microservice-faas.svg "Microservices vs Monolithic Architecture")

This approach of building an application out of a set of modular components is known as microservice architecture. Dividing an application into microservices is appealing to developers because it means they can create and modify small pieces of code which can be easily implemented into their codebases. This is in contrast to monolithic architecture, in which all the code is interwoven into one large system. With large monolithic systems, even a minor changes to the application requires a hefty deploy process. FaaS eliminates this deploy complexity.

Using serverless code like FaaS, web developers can focus on writing application code, while the serverless provider takes care of server allocation and backend services.

## What are the advantages of using FaaS?

#### Improved developer velocity

With FaaS, developers can spend more time writing application logic and less time worrying about servers and deploys. This typically means a much faster development turnaround.

#### Built-in scalability

Since FaaS code is inherently scalable, developers don’t have to worry about creating contingencies for high traffic or heavy use. The serverless provider will handle all of the scaling concerns.

#### Cost efficiency

Unlike traditional [cloud](https://www.cloudflare.com/learning/cloud/what-is-the-cloud/) providers, serverless FaaS providers do not charge their clients for idle computation time. Because of this, clients only pay for as much computation time as they use, and do not need to waste money over-provisioning cloud resources.

## What are the drawbacks of FaaS?

#### Less system control

Having a third party manage part of the infrastructure makes it tough to understand the whole system and adds debugging challenges.

#### More complexity required for testing

It can be very difficult to incorporate FaaS code into a local testing environment, making thorough testing of an application a more intensive task.

## How to get started with FaaS

Developers must create a relationship with a serverless provider in order to enable FaaS functionality for a web application. Since FaaS integration means some application code will be delivered from the edge, availability and geographical distribution of [edge servers](https://www.cloudflare.com/learning/cdn/glossary/edge-server/) is an important consideration. A user in Italy accessing a site that relies on FaaS edge code served from an overloaded data center in Brazil will encounter the kind of delay that leads to high bounce rates. [Cloudflare Workers](https://www.cloudflare.com/products/cloudflare-workers/) is a FaaS solution that takes advantage of Cloudflare’s global network with data centers in over 330 cities, making it a popular choice.