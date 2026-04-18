---
title: "Open Policy Agent (OPA) | Open Policy Agent"
source: "https://www.openpolicyagent.org/docs"
author:
published:
created: 2026-04-15
description: "The Open Policy Agent (OPA, pronounced \"oh-pa\") is an open source,"
tags:
  - "clippings"
---
The Open Policy Agent (OPA, pronounced "oh-pa") is an open source, general-purpose policy engine that unifies policy enforcement across the stack. OPA provides a high-level declarative language that lets you specify policy as code and simple APIs to offload policy decision-making from your software. You can use OPA to enforce policies in microservices, Kubernetes, CI/CD pipelines, API gateways, and more.

OPA is proud to be a graduated [Cloud Native Computing Foundation (CNCF)](https://www.cncf.io/announcements/2021/02/04/cloud-native-computing-foundation-announces-open-policy-agent-graduation/) project.

This page covers core concepts in OPA's policy language ([Rego](https://www.openpolicyagent.org/docs/policy-language)) as well as how to download and run OPA.

## What is OPA?

OPA [decouples](https://www.openpolicyagent.org/docs/philosophy#policy-decoupling) policy decision-making from policy enforcement. When your software needs to make policy decisions it **queries** OPA and supplies structured data (e.g., JSON) as input. OPA accepts arbitrary structured data as input.

<svg id="mermaid-svg-5045877" width="100%" xmlns="http://www.w3.org/2000/svg" class="flowchart" style="max-width: 587.835693359375px;" viewBox="53.70183563232422 0 587.835693359375 406" role="graphics-document document" aria-roledescription="flowchart-v2"><g><marker id="mermaid-svg-5045877_flowchart-v2-pointEnd" class="marker flowchart-v2" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" class="arrowMarkerPath" style="stroke-width: 1px; stroke-dasharray: 1px, 0px;"></path></marker><marker id="mermaid-svg-5045877_flowchart-v2-pointStart" class="marker flowchart-v2" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" class="arrowMarkerPath" style="stroke-width: 1px; stroke-dasharray: 1px, 0px;"></path></marker><marker id="mermaid-svg-5045877_flowchart-v2-circleEnd" class="marker flowchart-v2" viewBox="0 0 10 10" refX="11" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" class="arrowMarkerPath" style="stroke-width: 1px; stroke-dasharray: 1px, 0px;"></circle></marker><marker id="mermaid-svg-5045877_flowchart-v2-circleStart" class="marker flowchart-v2" viewBox="0 0 10 10" refX="-1" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" class="arrowMarkerPath" style="stroke-width: 1px; stroke-dasharray: 1px, 0px;"></circle></marker><marker id="mermaid-svg-5045877_flowchart-v2-crossEnd" class="marker cross flowchart-v2" viewBox="0 0 11 11" refX="12" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" class="arrowMarkerPath" style="stroke-width: 2px; stroke-dasharray: 1px, 0px;"></path></marker><marker id="mermaid-svg-5045877_flowchart-v2-crossStart" class="marker cross flowchart-v2" viewBox="0 0 11 11" refX="-1" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" class="arrowMarkerPath" style="stroke-width: 2px; stroke-dasharray: 1px, 0px;"></path></marker><g class="root"><g class="clusters"></g><g class="edgePaths"><path d="M145.767,62L145.767,68.167C145.767,74.333,145.767,86.667,145.767,98.333C145.767,110,145.767,121,145.767,126.5L145.767,132" id="L_Client_Service_0" class="edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style="" marker-end="url(#mermaid-svg-5045877_flowchart-v2-pointEnd)"></path><path d="M119.519,190L111.579,198.167C103.64,206.333,87.762,222.667,107.563,242.849C127.364,263.03,182.845,287.061,210.585,299.076L238.325,311.091" id="L_Service_OPA_0" class="edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style="" marker-end="url(#mermaid-svg-5045877_flowchart-v2-pointEnd)"></path><path d="M263.159,288L255.908,279.833C248.656,271.667,234.153,255.333,219.427,239.478C204.701,223.623,189.752,208.245,182.277,200.557L174.803,192.868" id="L_OPA_Service_0" class="edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style="" marker-end="url(#mermaid-svg-5045877_flowchart-v2-pointEnd)"></path><path d="M353.937,190L353.937,198.167C353.937,206.333,353.937,222.667,350.893,238.382C347.849,254.097,341.761,269.194,338.717,276.742L335.673,284.29" id="L_Policy_OPA_0" class="edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style="" marker-end="url(#mermaid-svg-5045877_flowchart-v2-pointEnd)"></path><path d="M557.746,190L557.746,198.167C557.746,206.333,557.746,222.667,529.068,242.97C500.39,263.272,443.035,287.545,414.357,299.681L385.68,311.817" id="L_Data_OPA_0" class="edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style="" marker-end="url(#mermaid-svg-5045877_flowchart-v2-pointEnd)"></path></g><g class="edgeLabels"><g class="edgeLabel" transform="translate(145.76666259765625, 99)"><g class="label" transform="translate(-52.48332977294922, -12)"><foreignObject width="104.96665954589844" height="24"><p></p><p>Request/Event</p></foreignObject></g></g></g></g></g></svg>

Query  
(any JSON Value)

Decision  
(any JSON Value)

Client

Service

![](https://www.openpolicyagent.org/assets/images/logo-92a1aebfb4ea664b7d9c550b29f450a5.png)

Policy (Rego)

Data (JSON)

OPA generates policy decisions by evaluating the query input against policies and data. OPA and Rego are domain-agnostic so you can describe almost any kind of invariant in your policies. For example:

- Which users can access which resources.
- Which subnets egress traffic is allowed to.
- Which clusters a workload must be deployed to.
- Which registries binaries can be downloaded from.
- Which OS capabilities a container can execute with.
- Which times of day the system can be accessed at.

Policy decisions are not limited to simple yes/no or allow/deny answers. Like query inputs, your policies can generate arbitrary structured data as output.

Let's look at an example. Imagine you work for an organization with the following network infrastructure:

<svg id="mermaid-svg-2414272" width="100%" xmlns="http://www.w3.org/2000/svg" class="flowchart" style="max-width: 584.6666870117188px;" viewBox="0 0 584.6666870117188 302" role="graphics-document document" aria-roledescription="flowchart-v2"><g><marker id="mermaid-svg-2414272_flowchart-v2-pointEnd" class="marker flowchart-v2" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" class="arrowMarkerPath" style="stroke-width: 1px; stroke-dasharray: 1px, 0px;"></path></marker><marker id="mermaid-svg-2414272_flowchart-v2-pointStart" class="marker flowchart-v2" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" class="arrowMarkerPath" style="stroke-width: 1px; stroke-dasharray: 1px, 0px;"></path></marker><marker id="mermaid-svg-2414272_flowchart-v2-circleEnd" class="marker flowchart-v2" viewBox="0 0 10 10" refX="11" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" class="arrowMarkerPath" style="stroke-width: 1px; stroke-dasharray: 1px, 0px;"></circle></marker><marker id="mermaid-svg-2414272_flowchart-v2-circleStart" class="marker flowchart-v2" viewBox="0 0 10 10" refX="-1" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" class="arrowMarkerPath" style="stroke-width: 1px; stroke-dasharray: 1px, 0px;"></circle></marker><marker id="mermaid-svg-2414272_flowchart-v2-crossEnd" class="marker cross flowchart-v2" viewBox="0 0 11 11" refX="12" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" class="arrowMarkerPath" style="stroke-width: 2px; stroke-dasharray: 1px, 0px;"></path></marker><marker id="mermaid-svg-2414272_flowchart-v2-crossStart" class="marker cross flowchart-v2" viewBox="0 0 11 11" refX="-1" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" class="arrowMarkerPath" style="stroke-width: 2px; stroke-dasharray: 1px, 0px;"></path></marker><g class="root"><g class="clusters"></g><g class="edgePaths"><path d="M502.633,190L502.633,194.167C502.633,198.333,502.633,206.667,502.633,214.333C502.633,222,502.633,229,502.633,232.5L502.633,236" id="L_n3_Internet_0" class="edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style="" marker-end="url(#mermaid-svg-2414272_flowchart-v2-pointEnd)"></path><path d="M210.645,62L213.881,68.167C217.117,74.333,223.59,86.667,233.208,98.555C242.827,110.443,255.591,121.887,261.973,127.608L268.355,133.33" id="L_sCI_n1_0" class="edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style="" marker-end="url(#mermaid-svg-2414272_flowchart-v2-pointEnd)"></path><path d="M175.524,62L170.738,68.167C165.953,74.333,156.383,86.667,147.221,98.473C138.06,110.28,129.307,121.56,124.93,127.2L120.554,132.84" id="L_sCI_n2_0" class="edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style="" marker-end="url(#mermaid-svg-2414272_flowchart-v2-pointEnd)"></path><path d="M502.633,62L502.633,68.167C502.633,74.333,502.633,86.667,502.633,98.333C502.633,110,502.633,121,502.633,126.5L502.633,132" id="L_sBusy_n3_0" class="edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style="" marker-end="url(#mermaid-svg-2414272_flowchart-v2-pointEnd)"></path><path d="M368.698,62L374.256,68.167C379.813,74.333,390.927,86.667,405.614,98.642C420.302,110.618,438.561,122.235,447.691,128.044L456.821,133.853" id="L_sApp_n3_0" class="edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style="" marker-end="url(#mermaid-svg-2414272_flowchart-v2-pointEnd)"></path><path d="M336.393,62L334.572,68.167C332.751,74.333,329.109,86.667,325.208,98.376C321.307,110.085,317.147,121.17,315.067,126.713L312.987,132.255" id="L_sApp_n1_0" class="edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style="" marker-end="url(#mermaid-svg-2414272_flowchart-v2-pointEnd)"></path><path d="M314.25,62L307.372,68.167C300.493,74.333,286.736,86.667,263.542,98.772C240.348,110.877,207.718,122.755,191.402,128.693L175.087,134.632" id="L_sApp_n2_0" class="edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style="" marker-end="url(#mermaid-svg-2414272_flowchart-v2-pointEnd)"></path><path d="M59.35,62L59.35,68.167C59.35,74.333,59.35,86.667,62.653,98.426C65.956,110.185,72.563,121.371,75.866,126.963L79.169,132.556" id="L_sCache_n2_0" class="edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style="" marker-end="url(#mermaid-svg-2414272_flowchart-v2-pointEnd)"></path></g><g class="edgeLabels"><g class="edgeLabel"><g class="label" transform="translate(0, 0)"></g></g><g class="edgeLabel" transform="translate(230.0625, 99)"><g class="label" transform="translate(-8.900001525878906, -12)"><foreignObject width="17.800003051757812" height="24"><p></p><p>p1</p></foreignObject></g></g></g></g></g></svg>

p2

p1

p1

p2

p3

p3

net1 (private)

net2 (private)

net3 (public)

Internet

ci

busybox

app

cache

There are three kinds of components in the system:

- Servers listen on a range of ports (for different protocols such as `http`, `ssh`, etc.)
- Networks connect servers and can be public or private. Public networks are connected to the Internet.
- Ports attach servers to networks.

All the servers, networks, and ports are provisioned using infrastructure as code. The infrastructure configuration is specified in this JSON representation:

```json
{
  "servers": [
    { "id": "app", "protocols": ["https", "ssh"], "ports": ["p1", "p2", "p3"] },
    { "id": "db", "protocols": ["mysql"], "ports": ["p3"] },
    { "id": "cache", "protocols": ["memcache"], "ports": ["p3"] },
    { "id": "ci", "protocols": ["http"], "ports": ["p1", "p2"] },
    { "id": "busybox", "protocols": ["telnet"], "ports": ["p1"] }
  ],
  "networks": [
    { "id": "net1", "public": false },
    { "id": "net2", "public": false },
    { "id": "net3", "public": true },
    { "id": "net4", "public": true }
  ],
  "ports": [
    { "id": "p1", "network": "net1" },
    { "id": "p2", "network": "net3" },
    { "id": "p3", "network": "net2" }
  ]
}
```
[Edit](#edit)

Your organization has established the following security policy that must be implemented:

> 1. Servers reachable from the Internet must not expose the insecure 'http' protocol.
> 2. Servers are not allowed to expose the 'telnet' protocol.

The policy needs to be enforced when servers, networks, and ports are provisioned and the compliance team wants to periodically audit the system to find servers that violate the policy.

Let's explore how OPA can help implement this policy.

## Writing Policy with Rego

OPA policies are expressed in a high-level declarative language called Rego. Rego (pronounced "ray-go") is purpose-built for expressing policies over complex hierarchical data structures. For detailed information on Rego see the [Policy Language](https://www.openpolicyagent.org/docs/policy-language) documentation.

> [!-success] -success
> tip
> 
> The examples below are interactive! If you edit the input data above containing servers, networks, and ports, the output will change below. Similarly, if you edit the queries or rules in the examples below the output will change. As you read through this section, try changing the input, queries, and rules and observe the difference in output.
> 
> They can also be run locally on your machine using the [`opa eval` command, here are setup instructions.](#running-opa)

> [!-secondary] -secondary
> note
> 
> This section covers the building blocks of writing policies in Rego. You can see how these concepts come together to solve our network security policy in the [Complete Example](#complete-example).

### Basic Syntax

To implement our security policy, we first need to access and examine the infrastructure data. When OPA evaluates policies, it binds data provided in the query to a global variable called `input`. You can refer to specific parts of the input data using the `.` (dot) operator.

```markdown
package servers

output := input.servers
```
[Edit](#edit)

To refer to array elements you can use the familiar square-bracket syntax:

```markdown
package servers

output := input.servers[0].protocols[0]
```
[Edit](#edit)

> [!-success] -success
> tip
> 
> You can use the same square bracket syntax if keys contain other than `[a-zA-Z0-9_]`. E.g., `input["foo~bar"]`.

If you refer to a value that does not exist, OPA returns *undefined*. Undefined means that OPA was not able to find any results.

```markdown
package servers

output := input.foobar
```
[Edit](#edit)

The most simple policy decisions are made by writing expressions that perform logical operations on the input data. For example, we can check if a server has a specific ID using an equality check with `==`.

```markdown
package servers

output := input.servers[0].id == "app"
```
[Edit](#edit)

OPA includes a set of [built-in functions](https://www.openpolicyagent.org/docs/policy-reference/builtins) you can use to perform common operations like string manipulation, regular expression matching, arithmetic, aggregation, and more.

```markdown
package servers

output := count(input.servers[0].protocols) >= 1
```
[Edit](#edit)

For queries to produce results, all of the expressions in the query must be true or defined. You can separate expressions across multiple lines (or optionally join them with `;` - meaning AND, on a single line):

```markdown
package servers

output if {
    input.servers[0].id == "app"
    input.servers[0].protocols[0] == "https"
}
```
[Edit](#edit)

If any of the expressions in the query are not true (or defined) the result is undefined. In the example below, the second expression is false:

```markdown
package servers

output if {
    input.servers[0].id == "app"
    input.servers[0].protocols[0] == "telnet"
}
```
[Edit](#edit)

> [!-secondary] -secondary
> Expressions are joined together with AND only when they are in the same rule body. In this example, the checks against `input.servers` are OR'd since they are in different rule bodies. See [Logical OR](#logical-or) in the Rules section below for more detail.
> 
> ```markdown
> output if {
>     input.servers[0].id == "app"
> }
> 
> output if {
>     input.servers[0].protocols[0] == "telnet"
> }
> ```

You can store values in intermediate variables using the `:=` (assignment) operator to help make more complex rules easier to read. Variables can be referenced just like `input` and are, like `input`, immutable.

```markdown
package servers

output if {
    s := input.servers[0]
    s.id == "app"
    p := s.protocols[0]
    p == "https"
}
```
[Edit](#edit)

When OPA evaluates expressions, it finds values for the variables that make all of the expressions true. If there are no variable assignments that make all of the expressions true, the result is undefined.

```markdown
package servers

output if {
    s := input.servers[0]
    s.id == "app"
    s.protocols[1] == "telnet"
}
```
[Edit](#edit)

Imagine you need to check if any networks are public. Recall that the networks are supplied inside an array:

`[{"id": "net1", "public": false}, {"id": "net2", "public": false}, ...]`

To solve this problem, you might naively first think to test each network individually by checking specific array indices like this:

```markdown
package servers

# if any are true, the result of the exists_public_network is true.

exists_public_network if input.networks[0].public == true
# or
exists_public_network if input.networks[1].public == true
# or
exists_public_network if input.networks[2].public == true
# or
exists_public_network if input.networks[3].public == true
# ...
```
[Edit](#edit)

This approach is problematic, there may be too many networks to list statically, the number of networks may not be known in advance.

Like other declarative languages (e.g., SQL), iteration in Rego happens implicitly when you inject variables into expressions. The solution for this case is to substitute the array index with a variable:

```markdown
package servers

exists_public_network if {
    some i
    input.networks[i].public == true
}
```
[Edit](#edit)

Now the query asks for values of `i` that make the overall expression true. When you substitute variables in references, OPA automatically finds variable assignments that satisfy all of the expressions in the query. Just like intermediate variables, OPA returns the values of the variables.

You can substitute as many variables as you want to do nested iteration. For example, to find out if any servers expose the insecure `"http"` protocol you could write:

```markdown
package servers

http_server if {
    some i, j
    input.servers[i].protocols[j] == "http"
}
```
[Edit](#edit)

If variables appear multiple times the assignments satisfy all of the expressions. For example, to find the ids of ports connected to public networks, you could write:

```markdown
package servers

exposed_ports contains port_id if {
    some i, j
    port_id := input.ports[i].id
    input.ports[i].network == input.networks[j].id
    input.networks[j].public
}
```
[Edit](#edit)

Just like references that refer to non-existent fields or expressions that fail to match, if OPA is unable to find any variable assignments that satisfy all of the expressions, the result is undefined.

```markdown
package servers

ssh_server if {
    some i
    # there is no assignment of i that satisfies the expression
    input.servers[i].protocols[i] == "ssh"
}
```
[Edit](#edit)

#### FOR SOME and FOR ALL

While plain iteration serves as a powerful building block, Rego also features ways to express *FOR SOME* and *FOR ALL* more explicitly.

##### FOR SOME (some)

`some ... in ...` is used to iterate over the collection (its last argument), and will bind its variables (key, value position) to the collection items. It introduces new bindings to the evaluation of the rest of the rule body.

Using `some`, we can express the rules introduced above in different ways:

```markdown
package servers

public_network contains net.id if {
    some net in input.networks # some network exists and..
    net.public                 # it is public.
}

shell_accessible contains server.id if {
    some server in input.servers
    "telnet" in server.protocols
}

shell_accessible contains server.id if {
    some server in input.servers
    "ssh" in server.protocols
}
```
[Edit](#edit)

For details on `some ... in ...`, see [the documentation of the `in` operator](https://www.openpolicyagent.org/docs/policy-language#membership-and-iteration-in).

##### FOR ALL (every)

Expanding on the examples above, `every` allows us to succinctly express that a condition holds for all elements of a domain.

```json
Edit the input to add a 'telnet' protocol to a server{
  "servers": [
    {
      "id": "busybox",
      "protocols": ["http", "ftp"]
    },
    {
      "id": "db",
      "protocols": ["mysql", "ssh"]
    },
    {
      "id": "web",
      "protocols": ["https"]
    }
  ]
}
```
[Edit](#edit)
```markdown
package servers

no_telnet_exposed if {
    every server in input.servers {
        not "telnet" in server.protocols
    }
}
```
[Edit](#edit)

Learn more about the [Every Keyword](https://www.openpolicyagent.org/docs/policy-language#every-keyword).

### Policy Rules

Rego lets you encapsulate and re-use logic with rules. Rules are just if-then logic statements. Rules can either be "complete" or "partial".

#### Complete Rules

Complete rules are if-then statements that assign a single value to a variable. Every rule consists of a head and a body. In Rego we say the rule head is true *if* the rule body is true for some set of variable assignments.

```markdown
package rules

# head
exists_public_network := true if {
    # body
    some net in input.networks # some network exists and..
    net.public                 # it is public.
}
```
[Edit](#edit)

You can query for the value generated by rules just like any other value (such as `input` or your own variables):

```markdown
package rules

exists_public_network := true if {
    some net in input.networks # some network exists and..
    net.public                 # it is public.
}

another_rule := {
    "public_networks": exists_public_network,
}
```
[Edit](#edit)

All values generated by rules can be queried via the global `data` variable from other packages loaded into OPA.

```markdown
package another_package

yet_another_rule := {
    "public_networks": data.rules.exists_public_network,
}
```
[Edit](#edit)

> [!-success] -success
> tip
> 
> You can query the value of any rule loaded into OPA by referring to it with an absolute path. The path of a rule is always: `data.<package-path>.<rule-name>`.

If you omit the `= <value>` part of the rule head the value defaults to `true`. You could rewrite the example above as follows without changing the meaning:

```markdown
exists_public_network if {
    some net in input.networks
    net.public
}
```

To define constants, omit the rule body. When you omit the rule body it defaults to `true`. Since the rule body is true, the rule head is always true/defined.

```markdown
package servers

max_allowed_protocols := 5
```
[Edit](#edit)

Constants defined like this can be queried just like any other values:

```markdown
count(input.servers[0].protocols) < max_allowed_protocols
```

If OPA cannot find variable assignments that satisfy the rule body, we say that the rule is undefined. For example, if the `input` provided to OPA does not include a public network then `exists_public_network` will be undefined (which is not the same as false.) Below, OPA is given a different set of input networks (none of which are public):

```json
{
  "networks": [
    { "id": "n1", "public": false },
    { "id": "n2", "public": false }
  ]
}
```
[Edit](#edit)
```markdown
package rules

exists_public_network if {
    some net in input.networks
    net.public
}
```
[Edit](#edit)

#### Partial Rules

Partial rules are if-then statements that generate a set of values and assign that set to a variable. In the example below `public_network contains net.id` is the rule head and `some net in input.networks; net.public` is the rule body. You can query for the entire set of values just like any other value.

```markdown
package example

# head
public_network contains net.id if {
    # body
    some net in input.networks # some network exists and..
    net.public                 # it is public.
}
```
[Edit](#edit)

Using the `in` keyword we can use this list to test if some other value is in the set defined by `public_network`:

```markdown
package example

allow if "net3" in public_network
```
[Edit](#edit)

You can also iterate over the set of values by referencing the set elements with a variable:

```markdown
package example

allow if {
    some net in public_network
    net == "net3"
}
```
[Edit](#edit)

In addition to partially defining sets, You can also partially define key/value pairs (aka objects). See [Rules](https://www.openpolicyagent.org/docs/latest/policy-language/#rules) in the language guide for more information.

#### Logical OR

When you join multiple expressions together in a query you are expressing logical AND. To express logical OR in Rego you define multiple rules with the same name. Let's look at an example.

Imagine you wanted to know if any servers expose protocols that give clients shell access. To determine this you could define a complete rule that declares `shell_accessible` to be `true` if any servers expose the `"telnet"` or `"ssh"` protocols:

```json
Input with telnet and ssh{
  "servers": [
    {
      "id": "busybox",
      "protocols": ["http", "telnet"]
    },
    {
      "id": "db",
      "protocols": ["mysql", "ssh"]
    },
    {
      "id": "web",
      "protocols": ["https"]
    }
  ]
}
```
[Edit](#edit)
```markdown
package example.logical_or

default shell_accessible := false

shell_accessible if {
    input.servers[_].protocols[_] == "telnet"
}

shell_accessible if {
    input.servers[_].protocols[_] == "ssh"
}
```
[Edit](#edit)

> [!-success] -success
> tip
> 
> The `default` keyword tells OPA to assign a value to the variable if all of the other rules with the same name are undefined.

When you use logical OR with partial rules, each rule definition contributes to the set of values assigned to the variable. For example, the example above could be modified to generate a set of servers that expose `"telnet"` or `"ssh"`.

```markdown
package example.logical_or

shell_accessible contains server.id if {
    server := input.servers[_]
    server.protocols[_] == "telnet"
}

shell_accessible contains server.id if {
    server := input.servers[_]
    server.protocols[_] == "ssh"
}
```
[Edit](#edit)

> [!-success] -success
> tip
> 
> Check out this [blog post](https://www.styra.com/blog/how-to-express-or-in-rego/) that goes into much more detail on this topic showing different methods to express OR in idiomatic Rego for different use cases.

### Complete Example

The sections above explain the core concepts in Rego. To put it all together let's review the desired policy in natural language:

> 1. Servers reachable from the Internet must not expose the insecure 'http' protocol.
> 2. Servers are not allowed to expose the 'telnet' protocol.

At a high-level the policy needs to identify servers that violate some conditions. To implement this policy we could define rules called `violation` that generate a set of servers that are in violation. For example:

```markdown
package example

violation contains message if {   # a server is in the violation set if...
    some server in public_servers # it exists in the 'public_servers' set and...
    "http" in server.protocols    # it contains the insecure "http" protocol.
    message := sprintf("server %s exposes http", [server.id])
}

violation contains message if {  # a server is in the violation set if...
    some server in input.servers # it exists in the input.servers collection and...
    "telnet" in server.protocols # it contains the "telnet" protocol.
    message := sprintf("server %s exposes telnet", [server.id])
}

public_servers contains server if { # a server exists in the public_servers set if...
    some server in input.servers    # it exists in the input.servers collection and...

    some port in server.ports       # it references a port in the input.ports collection and...
    some input_port in input.ports
    port == input_port.id

    # the port references a network in the input.networks collection and...
    some input_network in input.networks
    input_port.network == input_network.id

    # the network is public.
    input_network.public
}
```
[Edit](#edit)

This example demonstrates how we can use Rego to create a clear list of policy violations that can be handed back to the infrastructure as code system to present to the user, making it easy for them to see what's gone wrong.

## Running OPA

This section explains how you can query OPA directly and interact with it on your own machine. If you just want to quickly get a feel for the language without installing anything, check out the [OPA Playground](https://play.openpolicyagent.org/).

### 1\. Download OPA

- macOS
- Linux/Unix
- Windows
- Docker

OPA binaries can be installed on macOS using Homebrew. The formula can be reviewed on [brew.sh](https://formulae.brew.sh/formula/opa). This method supports both ARM64 and AMD64 architectures.

```shell
brew install opa
```

It's also possible to download the OPA binary directly:

- arm64 (Apple Silicon)
- amd64 (Older Intel Macs)

```shell
curl -L -o opa https://openpolicyagent.org/downloads/latest/opa_darwin_arm64
```

After downloading the OPA binary, you must ensure it's executable:

```shell
chmod 755 ./opa
```

It's also recommended to move the OPA binary into a directory in your `PATH` so you can run OPA commands in different directories.

You can verify the installation by running:

```shell
opa version
```

See all available binaries on the [GitHub releases](https://github.com/open-policy-agent/opa/releases). Checksums for all binaries are available in the download path by appending `.sha256` to the binary filename.

For example, verify the macOS arm64 binary checksum:

```shell
BINARY_NAME=opa_darwin_arm64
curl -L -O https://openpolicyagent.org/downloads/latest/$BINARY_NAME
curl -L -O https://openpolicyagent.org/downloads/latest/$BINARY_NAME.sha256
shasum -c $BINARY_NAME.sha256
```

### 2\. Try opa eval

The simplest way to interact with OPA is via the command-line using the [`opa eval` sub-command](https://www.openpolicyagent.org/docs/cli#eval). It is a swiss-army knife that you can use to evaluate arbitrary Rego expressions and policies. `opa eval` supports a large number of options for controlling evaluation. Commonly used flags include:

| Flag | Short | Description |
| --- | --- | --- |
| `--bundle` | `-b` | Load a [bundle file](https://www.openpolicyagent.org/docs/management-bundles#bundle-file-format) or directory into OPA. This flag can be repeated. |
| `--data` | `-d` | Load policy or data files into OPA. This flag can be repeated. |
| `--input` | `-i` | Load a data file and use it as `input`. This flag cannot be repeated. |
| `--format` | `-f` | Set the output format to use. The default is `json` and is intended for programmatic use. The `pretty` format emits more human-readable output. |
| `--fail` | n/a | Exit with a non-zero exit code if the query is undefined. |
| `--fail-defined` | n/a | Exit with a non-zero exit code if the query is not undefined. |

For example:

```json
input.json{
  "servers": [
    { "id": "app", "protocols": ["https", "ssh"], "ports": ["p1", "p2", "p3"] },
    { "id": "db", "protocols": ["mysql"], "ports": ["p3"] },
    { "id": "cache", "protocols": ["memcache"], "ports": ["p3"] },
    { "id": "ci", "protocols": ["http"], "ports": ["p1", "p2"] },
    { "id": "busybox", "protocols": ["telnet"], "ports": ["p1"] }
  ],
  "networks": [
    { "id": "net1", "public": false },
    { "id": "net2", "public": false },
    { "id": "net3", "public": true },
    { "id": "net4", "public": true }
  ],
  "ports": [
    { "id": "p1", "network": "net1" },
    { "id": "p2", "network": "net3" },
    { "id": "p3", "network": "net2" }
  ]
}
```
```markdown
example.regopackage example

default allow := false                              # unless otherwise defined, allow is false

allow if {                                          # allow is true if...
    count(violation) == 0                           # there are zero violations.
}

violation contains server.id if {                   # a server is in the violation set if...
    some server
    public_servers[server]                           # it exists in the 'public_servers' set and...
    server.protocols[_] == "http"                   # it contains the insecure "http" protocol.
}

violation contains server.id if {                   # a server is in the violation set if...
    server := input.servers[_]                      # it exists in the input.servers collection and...
    server.protocols[_] == "telnet"                 # it contains the "telnet" protocol.
}

public_servers contains server if {                  # a server exists in the 'public_servers' set if...
    some i, j
    server := input.servers[_]                      # it exists in the input.servers collection and...
    server.ports[_] == input.ports[i].id            # it references a port in the input.ports collection and...
    input.ports[i].network == input.networks[j].id  # the port references a network in the input.networks collection and...
    input.networks[j].public                        # the network is public.
}
```
```bash
# Evaluate a trivial expression.
./opa eval "1*2+3"

# Evaluate a policy on the command line.
./opa eval -i input.json -d example.rego "data.example.violation[x]"

# Evaluate a policy on the command line and use the exit code.
./opa eval --fail-defined -i input.json -d example.rego "data.example.violation[x]"
echo $?
```

### 3\. Try opa run (interactive)

OPA includes an interactive shell or REPL (Read-Eval-Print-Loop) accessible via the [`opa run` sub-command](https://www.openpolicyagent.org/docs/cli#run). You can use the REPL to experiment with policies and prototype new ones.

To start the REPL just:

```bash
./opa run
```

When you enter statements in the REPL, OPA evaluates them and prints the result.

```markdown
> true
true
> 3.14
3.14
> ["hello", "world"]
[
  "hello",
  "world"
]
```

Most REPLs let you define variables that you can reference later on. OPA allows you to do something similar. For example, you can define a `pi` constant as follows:

```markdown
> pi := 3.14
```

Once `pi` is defined, you query for the value and write expressions in terms of it:

```markdown
> pi
3.14
> pi > 3
true
```

Quit out of the REPL by pressing Control-D or typing `exit`:

```markdown
> exit
```

You can load policy and data files into the REPL by passing them on the command line. By default, JSON and YAML files are rooted under `data`.

```shell
opa run input.json
```

Run a few queries to poke around the data:

```markdown
> data.servers[0].protocols[1]
```
```markdown
> data.servers[i].protocols[j]
```
```markdown
> net := data.networks[_]; net.public
```

To set a data file as the `input` document in the REPL prefix the file path:

```shell
opa run example.rego repl.input:input.json
```
```markdown
> data.example.public_servers[s]
```

> [!-info] -info
> info
> 
> Prefixing file paths with a reference controls where file is loaded under `data`. By convention, the REPL sets the `input` document that queries see by reading `data.repl.input` each time a statement is evaluated. See `help input` for details in the REPL.

Quit out of the REPL by pressing Control-D or typing `exit`:

```markdown
> exit
```

### 4\. Try opa run (server)

To integrate with OPA you can run it as a server and execute queries over HTTP. You can start OPA as a server with `-s` or `--server`:

```bash
./opa run --server ./example.rego
```

By default OPA listens for HTTP connections on `localhost:8181`. See `opa run --help` for a list of options to change the listening address, enable TLS, and more.

Inside of another terminal use `curl` (or a similar tool) to access OPA's HTTP API. When you query the `/v1/data` HTTP API you must wrap input data inside of a JSON object:

```json
{
    "input": <value>
}
```

Create a copy the input file for sending via `curl`:

```markdown
cat <<EOF > v1-data-input.json
{
    "input": $(cat input.json)
}
EOF
```

Execute a few `curl` requests and inspect the output:

```bash
curl localhost:8181/v1/data/example/violation -d @v1-data-input.json -H 'Content-Type: application/json'
curl localhost:8181/v1/data/example/allow -d @v1-data-input.json -H 'Content-Type: application/json'
```

By default `data.system.main` is used to serve policy queries without a path. When you execute queries without providing a path, you do not have to wrap the input. If the `data.system.main` decision is undefined it is treated as an error:

```bash
curl localhost:8181 -i -d @input.json -H 'Content-Type: application/json'
```

You can restart OPA and configure to use any decision as the default decision:

```markdown
./opa run --server --set=default_decision=example/allow ./example.rego
```

Re-run the last `curl` command from above:

```bash
curl localhost:8181 -i -d @input.json -H 'Content-Type: application/json'
```

### 5\. Try OPA as a Go library

OPA can be embedded inside Go programs as a library. The simplest way to embed OPA as a library is to import the `github.com/open-policy-agent/opa/rego` package.

```markdown
import "github.com/open-policy-agent/opa/rego"
```

Call the `rego.New` function to create an object that can be prepared or evaluated:

```markdown
r := rego.New(
    rego.Query("x = data.example.allow"),
    rego.Load([]string{"./example.rego"}, nil))
```

The `rego.Rego` supports several options that let you customize evaluation. See the [GoDoc](https://godoc.org/github.com/open-policy-agent/opa/rego) page for details. After constructing a new `rego.Rego` object you can call `PrepareForEval()` to obtain an executable query. If `PrepareForEval()` fails it indicates one of the options passed to the `rego.New()` call was invalid (e.g., parse error, compile error, etc.)

```markdown
ctx := context.Background()
query, err := r.PrepareForEval(ctx)
if err != nil {
    // handle error
}
```

The prepared query object can be cached in-memory, shared across multiple goroutines, and invoked repeatedly with different inputs. Call `Eval()` to execute the prepared query.

```markdown
bs, err := ioutil.ReadFile("./input.json")
if err != nil {
    // handle error
}

var input any

if err := json.Unmarshal(bs, &input); err != nil {
    // handle error
}

rs, err := query.Eval(ctx, rego.EvalInput(input))
if err != nil {
    // handle error
}
```

The policy decision is contained in the results returned by the `Eval()` call. You can inspect the decision and handle it accordingly:

```markdown
// In this example we expect a single result (stored in the variable 'x').
fmt.Println("Result:", rs[0].Bindings["x"])
```

You can combine the steps above into a simple command-line program that evaluates policies and outputs the result:

```markdown
main.gopackage main

import (
    "context"
    "encoding/json"
    "fmt"
    "log"
    "os"

    "github.com/open-policy-agent/opa/v1/rego"
)

func main() {
    ctx := context.Background()

    // Construct a Rego object that can be prepared or evaluated.
    r := rego.New(
        rego.Query(os.Args[2]),
        rego.Load([]string{os.Args[1]}, nil))

    // Create a prepared query that can be evaluated.
    query, err := r.PrepareForEval(ctx)
    if err != nil {
        log.Fatal(err)
    }

    // Load the input document from stdin.
    var input any
    dec := json.NewDecoder(os.Stdin)
    dec.UseNumber()
    if err := dec.Decode(&input); err != nil {
        log.Fatal(err)
    }

    // Execute the prepared query.
    rs, err := query.Eval(ctx, rego.EvalInput(input))
    if err != nil {
        log.Fatal(err)
    }

    // Do something with the result.
    fmt.Println(rs)
}
```

Run the code above as follows:

```shell
go run main.go example.rego 'data.example.violation' < input.json
```

Congratulations on completing the introduction to OPA. You have learned the core concepts behind OPA's policy language as well as how to get OPA and run it on your own.

If you have more questions about how to write policies in Rego check out:

- The [Policy Reference](https://www.openpolicyagent.org/docs/policy-reference) page for reference documentation on built-in functions.
- The [Policy Language](https://www.openpolicyagent.org/docs/policy-language) page for complete descriptions of all language features.

If you want to try OPA for a specific use case check out:

- The [Ecosystem](https://www.openpolicyagent.org/ecosystem) page which showcases various of OPA integrations.

Some popular tutorials include:

- The [Kubernetes](https://www.openpolicyagent.org/docs/kubernetes) page for how to use OPA as an admission controller in Kubernetes.
- The [Envoy](https://www.openpolicyagent.org/docs/envoy) page for how to use OPA as an external authorizer with Envoy.
- The [Terraform](https://www.openpolicyagent.org/docs/terraform) page for how to use OPA to validate Terraform plans.

Don't forget to install the OPA (Rego) Plugin for your favorite [IDE or Text Editor](https://www.openpolicyagent.org/docs/editor-and-ide-support).