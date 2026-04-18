---
title: "n8n: A Guide With Practical Examples"
source: "https://www.datacamp.com/tutorial/n8n-ai"
author:
  - "[[François Aubry]]"
published: 2025-05-06
created: 2026-04-13
description: "Learn how to use n8n to build AI agents that automate email processing and create a retrieval-augmented generation (RAG) agent for document question answering."
tags:
  - "clippings"
---
n8n has emerged as a popular and powerful framework in agentic AI. It allows us to build automated workflows without the need for complex coding.

In this article, I will explain step by step how to make the most of this robust platform to automate two distinct processes:

1. First, I will guide you through setting up an AI agent to automatically process email from Gmail, saving valuable time and reducing manual effort.
2. Then, we will create an intelligent agent that can chat about any given document, providing quick access to information at our fingertips.

We keep our readers updated on the latest in AI by sending out The Median, our free Friday newsletter that breaks down the week’s key stories. Subscribe and stay sharp in just a few minutes a week:

<iframe src="https://dcthemedian.substack.com/embed" width="800" height="400" frameborder="0"></iframe>

## What Is n8n?

n8n is an open-source automation tool that helps us connect various apps and services to create workflows, much like a digital assembly line. It allows users to visually design these workflows with nodes, each representing a different step in the process.

With n8n, we can automate tasks, manage data flow, and even integrate APIs, all without needing extensive programming skills. Here's an example of an automation we'll build in this tutorial:

![n8n example workflow](https://media.datacamp.com/cms/ad_4nxea0y8i_3c6glaweedqzqfu7gk6o6wjdlc51emflw4cpvkbhyszjiqb2ut8c-4bepfcwmoucvi2b3hrahonqv2xd50wgksbmhcrvqptodyepwb6ivmc-_ybyus0-p-_unc3md0f.png)

Without going into details, here’s a description of what this automation does:

1. It accesses our Gmail account to check for new email messages.
2. New emails are sent to ChatGPT for AI processing.
3. The AI identifies the relevant information, which is then saved in a spreadsheet.

## How to Use n8n?

We have two options to use n8n:

1. Use their web interface [here](https://n8n.io/). This requires an account and a paid subscription, but it has a 14-day free trial you can use to follow this tutorial.
2. Because it is open source, we can also run it locally or host it ourselves. This is free and gives access to almost all of its features (a few features are exclusive to their paid cloud or enterprise plans).

Both options let you follow this tutorial at no cost. We’ll run it locally, but if you prefer to use the web interface, the steps are the same.

## n8n Local Setup

[n8n’s official repository](https://github.com/n8n-io/n8n) explains how to set up n8n locally. The simplest way is to:

1. Download and install Node.js from [the official website](https://nodejs.org/en/download).
2. Open a terminal and run the command `npx n8n`.

That's it! After running the command, you should see this in the terminal:

![Running n8n locally](https://media.datacamp.com/cms/ad_4nxeru1msr3eaziequk4awuaae5a1d48zazqzqbcvzaocnucimh0u_zzudsrj94gsziy3zekjpl2yzsag3hzruyoeuibu640xj_w8zwqulttlsccltkb51mgiktyhgbljmebzvxgs.png)

To open the interface, either press "o" on the keyboard or open the localhost URL shown in the terminal—in my case, `http://localhost:5678`.

## Understanding n8n

Before we build our first automation, it's good to understand how n8n works. An n8n workflow consists of a sequence of nodes. It starts with a trigger node that specifies a condition for the workflow to be executed.

![n8n trigger nodes](https://media.datacamp.com/cms/ad_4nxfzalbjepknpogplb-1lzosvrvggezyt2izqj9y6mhxlqkxl8b6yv2zxa5ybw0_eyq3hfltpgdo5g08h0kalfwtpcmi-tsawp3xpb8na7cdb70vum-nc2qz3rivxeuwdodml7jqfw.png)

Nodes connect to move and process data. In this example, the Gmail trigger node connects to an OpenAI node. This means that the email is given to ChatGPT for processing. Finally, the output of ChatGPT is sent to a Google Sheet node, which connects to a Google Sheet in our Google Drive and writes a new line into a spreadsheet.

This particular workflow uses ChatGPT to identify invoices that need to be paid and assigns a line in the sheet with the invoice ID and the price.

![n8n data flow](https://media.datacamp.com/cms/ad_4nxdclv-loatltcg-beddcpqtpia_od-3y7a72bulomxfx9-lx4qbrnbkhtjft5clcfanjqowbdgd_ekjsz9i__j0q---lgnzw3gucjynwbbgk5cqcvvk9wsrlsoxp1rmo0munkbo6g.png)

n8n workflows can be much more complex. n8n supports over 1,047 integrations, so we can't cover all of them in a tutorial. Instead, I'll focus on giving you a general idea of how it works and the necessary background to explore it on your own. If there's a tool you use regularly, chances are that either n8n supports it or you can manually integrate it.

## Example 1: Automating Invoice Processing From Email

In this section, we learn how to build the workflow above.

This is a real use case that I use to manage my rental invoices. I have a house with a few rooms that I rent. The bills are split equally between all tenants. Each time I receive an invoice, I need to add the total to a spreadsheet that is shared with my tenants.

I have a specific email address to which invoices related to house bills are forwarded. This way, I know all emails in that mailbox correspond to an invoice. I send the content of the email to ChatGPT to identify the invoice ID and the total amount to be paid. Then this information is added to a new row in the shared spreadsheet.

### Configuring the email trigger

To start a new workflow, we need to click the "Add first step..." button.

![Starting a n8n workflow](https://media.datacamp.com/cms/ad_4nxercbuuamxzaxztfvnw8lzxbegk_gzayfembpq7obv-ly29dm45rpgsshbid7cjlkha-xphlrwbt4kyybsn0kegs387cbx5xt0xfs0lfrgwm4nkmfubxszr6oqjo6j-0aus2hvy8a.png)

Starting a n8n workflow

Because it's the first node, it must be a trigger, so we're presented with a panel to select a trigger node. A trigger node defines the conditions for the workflow to execute.

![Trigger nodes in n8n](https://media.datacamp.com/cms/ad_4nxfrw136vcpoigsnljge07fr6sepdi_c8ohx52rvws9yh8lb9dmstetj2g4skwifjbns9ljj9x-wrlp8td82ekpqmw-yx4c4kyaxwv4p4qavbpxr4ytyufxfsgdzcweu2zopuymoaa.png)

There's a wide range of possible trigger nodes. Let's select a Gmail trigger node by typing "gmail" in the search box and clicking the Gmail node.

![Selecting a Gmail trigger node in n8n](https://media.datacamp.com/cms/ad_4nxcx-liyqsfvqbrne_zqkj7dvw7n_lgshdgna5a9jb1yemjorigqk9ol_q6skdcv0rfxbkbgz7u7n18axkmoz3rglntaoxfwo-fyetbt2evgy6d9adywph_mcfyvg53zg-limg1s.png)

Then, we choose the only available trigger for Gmail: "On message received".

![On message received trigger node in n8n](https://media.datacamp.com/cms/ad_4nxc3p9jbkv0kvmrdcgawdjth56s9si9jwbcs8xyvv-zn7c7vdj5rzfmga3tukqgvq2kkosmxxlwl7d2reqdqe9flyvgt1gvrdrechkusld7-7fs1qbkcicgor7zputishkdccfgijw.png)

This will open the node configuration panel, where we need to configure our Gmail credentials to allow the n8n workflow to access our Gmail account. To do so, click "New credential". This will open the following window:

![Configuring Google OAuth credentials in n8n](https://media.datacamp.com/cms/ad_4nxen4lq5wxowrsmznj1djd0xrvxeqseifzfnb8mxonrqjq-tlrjmo737sbrhoczr5m57je0-s1j-87giwbftczhniowoy8q39uhvlo-vkl0earjpdgr8z-rlfqzy58yv04c4yzk0bg.png)

On the right-hand side (1), there's a setup guide explaining the steps required to configure the credentials on [Google Cloud](https://console.cloud.google.com/). The guides provided by n8n are quite comprehensive, so we won't repeat the steps here. Make sure to also enable the Gmail API in the Google Cloud Console.

Once it's configured, we need to copy the client ID (2) and client secret (3) from Google Cloud into the credential configuration of n8n.

To make sure everything is correctly configured, we can test the node by clicking "Fetch Test Event."

![Testing a workflow](https://media.datacamp.com/cms/ad_4nxctuxfldznfpwqvhuv4_xqsi_aknspzw25dwrn82wwefqr-efsve1dns8_rc8ayxaabjlldzywblzzl1ebdenpajk4_c_gtll-6xgn4e7ifxannjx9zfgwm6tsrouvszxtksgvooa.png)

Testing a workflow

After the test, we should see the latest email we've received in our inbox in the output section. The content of the email is the `snippet` field.

![](https://media.datacamp.com/cms/ad_4nxdlwzesuw02onacezk2ruajbkg24ghul5l-eb8vuiygnmomi7ikcb7fbyhzdphqhuu0vzcszgxyfxdffvfkblav-lakhp-c-_30c7ej32gogcezco2jws6_roz86gtem-ddkkmsow.png)

The `snippet` field stores the email content. It says that my April internet invoice is available. It provides the invoice ID and total amount to be paid. This is the information we want to add to the spreadsheet.

For testing purposes, I recommend pinning the output by clicking the pin button in the top right corner:

![Pinning a node result in n8n](https://media.datacamp.com/cms/ad_4nxeoqcvdeptujwlztbsgwwjjedo_p9l_k2h_ni5wsfvtm0bq2bolgr2t4zeayi0laicaxfhejxv9dw8awjbxmnzua--mlbwnrvwfa4_ffv8x1yx46is9_ul-kgaou1ogkzytajlleq.png)

Pinning a node result in n8n

This will lock the result to the trigger, meaning that whenever we run this workflow, this same output is used, making it easier to test the workflow because the results won't be affected by any new emails we may receive. We will unpin it once the workflow is properly set up.

At this stage, our workflow should have a single trigger node (we can see it's a trigger node because of the small lightning bolt marker on the left).

![Identifying trigger nodes in n8n](https://media.datacamp.com/cms/ad_4nxcfeyybdrqysa81ed1qpfsptto_3sgviyfew14dvzgx3h7hggezntn7s9bvafcjvso7qlhc9piwgg8r7awcrpqxad2ksfa9h5eszro6f5heyzw3srkqn2npvynjijbs8sxrlyhzdw.png)

Identifying trigger nodes in n8n

Note that, since you likely won't have an email invoice in your mailbox, later on, ChatGPT will likely give you an answer that doesn't make sense. If you want to test this exact workflow, you can send yourself a test e-mail with the following content (or something similar):

```markdown
Dear customer,

Your internet invoice number FT 2025**/****** for April is now available in the attachment.

Amount

€**.**
This invoice must be paid by 19/05/2025.Powered By
```

After you send this, you must unpin the result, re-run the Gmail node, and pin the new result.

### Configuring the ChatGPT node

The next step is to configure the OpenAI node. Start by clicking the "+" button on the right of the Gmail trigger node:

![Connecting nodes in n8n](https://media.datacamp.com/cms/ad_4nxdijqki1gdic53tbut_2zoniyi6yk6njojz9emghhb2-uoproudz15shbufc3uusrvdboxomqq0bqmxjmjxftcrrkfly4drwpx_c0qemryns-9vwmlo__mtf0r1jvowl1dbe2yw.png)

Type "OpenAI" and select the corresponding option from the list.

![Finding OpenAI nodes in n8n](https://media.datacamp.com/cms/ad_4nxfpoi5olbdoi8yu0ttegf3v9upkic1cjs02zfb6rpmqk1qb2s3hhl1kkrwmk47r_l0lpa4vjxn8rzqcwsmqlmo2cy_qc2puj8ly0ny6-cwdzv8fsx23e8djggsqtx9jkah-t3cf.png)

Then, under "Text Actions", select the "Message a model" node. This node is used to message an LLM.

![Creating a "Message a model" node in n8n](https://media.datacamp.com/cms/ad_4nxcz2ygjjxkefmvbfijo5x18sabhr2_y2etcu2ochrsbbaw6yls_zvjktuj8lhewalnc08y95yz5fuvkmtgt-_qzscdthlkr-0pcijezkn-nrxadm2pfpuarggpcj7h-96abpmzvsq.png)

As before, we need to create a credential to access OpenAI. Note that once a credential is created, it can be reused in any workflow. We don't need to set it each time.

For the OpenAI credential, all we need is an API key. If you don't have one, you can create one [here](https://platform.openai.com/api-keys). If you have trouble doing this, n8n also provides a guide for this.

In terms of configuration, we need to select the AI model we want to use and the message we send to the model. For the model, we can use GPT 4.1:

![Selecting the AI model in n8n](https://media.datacamp.com/cms/ad_4nxd7uv4ipy7ama0yk2o8ksfphledz9oy52ya3to6wmvd0i1rfjhksmdlylqnkhs1gxvw5komwwczqxqkll3q0ngf4t9nq7uk2syl8ug5ynntnvy2o1tueax5l8kwr3tlkz-2fnja5a.png)

In the message field, we need to provide the prompt. For this example, we give the model the content of the email and ask it to identify the invoice ID and the total amount to pay. Here's the prompt I used:

![Configuring the agent prompt in n8n](https://media.datacamp.com/cms/ad_4nxf4lf_ytnxqlt8xofapcwyesy7whtlt5uuav-5hipny9eh8ohyqb29qokhenhipvniirzovcnytgu9nvb_k4qfjqsjsgps1hnt9hrurutike2-kdn_0zcvnyndeywzfpn6aqto3qg.png)

The content of the email is provided as `{{ $json.snippet }}`. In n8n, the prompt can contain variables that are populated from the output of previous nodes, the email in our case. The list of available fields can be seen on the left. We can type the field manually or drag and drop it into the prompt.

![](https://media.datacamp.com/cms/ad_4nxezj8xno1svxalp0i2bpmhij7csgobgkvnl42c6et6lqcc3bon76ewqqa010-nuz4fnbmexxcyguqa9xncl1bjhymyl3oooniyn2zwa2gtlw4ohp_8om21pbcfmi4esujli_sbr.png)

To test this, we click the "Test Step" button at the top of the configuration panel. The result is displayed on the right:

![](https://media.datacamp.com/cms/ad_4nxeys7u6s8j5hcpkm2rqjuh2dbuevfszcfx7ryd-s_4q2iy67z1udbtsxqsl2hsiktnjnq3jhdmngsmuuwy00hqu0q-fqz8b4fpfqbcze5gkur9mjtodaxssuv6cknhzzlgdmrj7.png)

The result is a string with the answer from the model. We would like to have the two fields separately, so we don't have to further process the message. We can achieve this by changing the output of the LLM to JSON:

![Configuring the output format in n8n](https://media.datacamp.com/cms/ad_4nxfo9uekgml7tescsgbn_lcngnul1hkv7en21coforfcin55rhmmdktlgmtepqznzlugeg6c0muho9irhuk8lbsbkcmjmm5dkopmycp0s1t99ivmljiasgbtlxifgjqfgffjq-e0.png)

Testing this step again, we get the two fields as JSON data:

![](https://media.datacamp.com/cms/ad_4nxfhugtcn1qhosl6jqqcv9oaxdqts1qukxot80bbmp1titvoslrsgphwiidbaguogonipfpidldpybnlifkliomnny78aury6cwotjxnowgqsyobiszwptf9zthcamvq1zx7x38jvg.png)

### Sending the data to a Google Sheet

The final step in this workflow is to send the invoice ID and price to a new row in a Google Sheet. At this stage, we need to connect the output of the OpenAI node to Google Sheets. We do this as before by clicking the "+" button to the left of the node:

![Adding the final node in n8n](https://media.datacamp.com/cms/ad_4nxdc80g1g9u78any-hionnuclw_uker1rn1tufeajcmgz3mdccg3vvscb3ljvibgc2_z8drfjnyhaehgbcla9b1tsvbdcutwdsh1qbabz-a8siex74v_uut3ppohjhxkyplcrepazg.png)

Here we want to type Google Sheets and select the "Append row in sheet" node:

![Selecting a Google Sheets node in n8n](https://media.datacamp.com/cms/ad_4nxetrp0ompfmwgtlypaakowpxys7cne1svje0wa00vyhs-gey7tyt4i7o8_u3f3pzspckx2y8dmdyftsmkagzy7-30padqyli7rmwr9u30nfj4r9nizw8f6pz186pu2zm5paje4lbg.png)

We can use the same credentials we used for Gmail access. But we need to enable the following API's in the [Google Cloud Console](https://console.cloud.google.com/):

- Google Sheets API
- Google Drive API

To configure the Google Sheets node, we need to select the sheet and select the values to populate the fields. The sheet should be created manually with two columns, one to hold the invoice ID and another for the invoice total.

![Initial state of the speadsheet](https://media.datacamp.com/cms/ad_4nxfuhjt4rsxpx_tpowbvplaot6bto_zrshx9fipbmt-pupzzpzv6sz7xnwxq4zzzmxm09wm9gk3l_roxgrj5sbog_qrxmxtq-m2vjyk8vrd99utdvltb9otjoo6k5blg3qhdgd-ovw.png)

Initial state of the speadsheet

Those values are taken from the output of the OpenAI node. We can drag and drop them into the columns.

![](https://media.datacamp.com/cms/ad_4nxdvfmazn9igb_egz405fgwtb515m3rch67nbzaknwdsgrozaovlvhc6bdklag3hduhm8hepdqjdgsq8v4_ebasgtzo17bqczmm9wr_uukczilzpymc_sn-irvlps7evquku8mhz9g.png)

### Running the workflow

That's it! We have a workflow that will automatically process our invoices into a Google Sheet. We can test it by clicking the "Test workflow" at the bottom:

![Testing the workflow in n8n](https://media.datacamp.com/cms/ad_4nxdgwpp1mfyys3uuk0dueimf2heweowtpep_mpbbxzzcqxvsljx-wbfdga-jmbdaka_yv2fa-fyhqkl-d3ue9uysy4lzxz3mluznqrjbyz1v3am5tk_v7hjo-aobcwi5avnpigd-zq.png)

After running it, if we go to our Google Sheet, we'll see a new row with the data:

![](https://media.datacamp.com/cms/ad_4nxfnuaguuplulo4wdrvj09ivig1d-ghczawjudcpjf35umeiy5bsncaqqavzztpelz73w446alpp1xub_hoe2gu5w6_zz6fqtxreucdaizjip1mjliivulihyy7toy1zwrv3dacx.png)

By default, a workflow will run every minute. Depending on the workflow, we should configure an appropriate frequency for it to run. In this specific example, once a minute is far too frequent. Once a day is a more appropriate frequency.

We can configure that by double-clicking on the trigger node and setting a different value in the "Poll Times" field:

![Changing the execution frequency in n8n workflow](https://media.datacamp.com/cms/ad_4nxczpcypti1vwutuhwoqwg8gw2bmdjuxcltszunhbehbingrr1jdqxaavbnz_p6ucvxpfh5_1tcmosbrssghlk2g6burmmdyojwcdarpn2nda3atozfvsimk0oar_6xi_wgoazb9ra.png)

## Example 2: Building a RAG Agent

In this section, we build a more complex RAG agent workflow. [RAG](https://www.datacamp.com/courses/retrieval-augmented-generation-rag-with-langchain) stands for retrieval-augmented generation, a technique that combines retrieving relevant information from a database or document and then using a language model to generate responses based on the retrieved information.

This is very useful when we have a specific knowledge base, such as a long text document, and want to build an AI agent that is able to answer questions about it.

I like to play board games, but my friends and I often argue about the rules and then spend time searching for the correct rules instead of playing, which can be frustrating. Building a RAG agent based on the rules of the game is a good solution to fix this problem because the next time we have a question, we can simply ask the agent.

To build this agent, we'll do two workflows:

1. One workflow that we'll run only once to upload the data to a Pinecone database.
2. Another that powers the RAG agent and uses the Pinecone database to answer our questions.

[Pinecone](https://www.datacamp.com/courses/vector-databases-for-embeddings-with-pinecone) is a type of database that manages data in the form of vectors. A vector database like Pinecone is great for our RAG agent because it helps the agent quickly look up and understand relevant information, making it more efficient at providing accurate answers.

Since we only need to run this workflow once, we can use a manual trigger node. This is a trigger node used to manually run a workflow.

![Manual trigger node in n8n](https://media.datacamp.com/cms/ad_4nxc_mc6ffn0osbkv-prhxbgyaa7uge7-qhwtj9ibaxneakc8yal-yuclpnw4gl2yanmyo4rdasax_j0pj-uazs_ibkx0kwvaoo33flgqvnqcrin6nqzqqghosnq5zgywzgmsu3_1dw.png)

Connect the manual trigger node to a “Google Drive” node to download the data from Google Drive.

![Google Drive download node in n8n](https://media.datacamp.com/cms/ad_4nxearsfp4leza9feq4chjzirljprwnwoma9yrpbzpvazy4n97pqfwnyujkofjxgdkaduqh9vmyhrwid-cnzrfradwqwf61xssqthksk9tgi4emy3nr9o_i_ldqzr5-ifdpgarheaiq.png)

Use the following configuration:

![Configuring the Google Drive download node in n8n](https://media.datacamp.com/cms/ad_4nxctyx6yghblrdbjswgmwlav_dkfkwtlu7ptrlyd9mcp9pb-bvuwreulwldyx4vbcjkp70ctkswrwkpa5ekfe1qwbahmwwcllhrznnozcbocdon_icej5txco79vwz_dbq9pkmr1eg.png)

I used the publicly available `mtgrules.txt` file with the rules of the trading card game Magic: The Gathering. You can use any file you'd like to ask questions about; the workflow is the same.

To configure Pinecone, log into [Pinecone](https://app.pinecone.io/), copy the API key, and create an index by clicking the "Create index" button. I called my index `rules` and selected the `text-embedding-3-small` model.

![Creating the Pinecone index](https://media.datacamp.com/cms/ad_4nxd_ir5ug7d8sau7jjhp-bzjuwgawavsxvq7jeogedplwwbsobjhb9a-hykfzm1sms9u9jd09lmm8_mejliifc1sarq5-tgyk8d2ip3jsposxlqz0eurbdxjv5txr2kdzpdv57syag.png)

Back to n8n, connect the output of the Google Drive node to a Pinecone Vector Store node for the action "Add documents to vector store":

![Creating the Pinecone node in n8n](https://media.datacamp.com/cms/ad_4nxeqo5m1wbyqq-_gyoajwdueavagjrjrfc-ulkssu1u2fmm7xdntslpdytah0pqzhln8pghj-fp08e28aoq8gzx4jk3014avqirorwdjmtsln7y6-jginzsmk9vtmyvu1-p533y0ja.png)

To configure the node, we need to create a credential by pasting the API key and selecting the Pinecone Index we just created. Below the Pinecone Vector Store node, we see two things we need to configure: an embedding model and a data loader.

![Configuring the Pinecone Vector Store in n8n](https://media.datacamp.com/cms/ad_4nxdqvt9cgzrggo8tymakzz_bhr_8xkscsq5urtbz1uh9rclyhvj1wkf_cxykcyiozkifebgwsdfutvva1mp8gp7dpvzwha49oyczp7zie_jlekxqkfd-hptsrqu32mxxzct9-jo9ma.png)

For the embedding, create an OpenAI Embedding node with the model `text-embedding-3-small`:

![Configuration of the Pinecone embedding](https://media.datacamp.com/cms/ad_4nxddjp9icthqjjdj2ljymso2s2hv18w1zgzzzh0irfew-m-vfw25zi1ge0q0zsyuhpbtuyygfulksbmniagfzictfs1onre1f8s3bcsh0cpmrbzdfdh7y21m-nddmhmnp_drmfjx.png)

For the data loader, we create a Default Data Loader node with a binary data type:

![Configuration of the Pinecone data loader in n8n](https://media.datacamp.com/cms/ad_4nxey8wcnl4uidusjoitmgm4vq5_pahiiuqqqbwmmjbnfm7wqnkg3xb5l1dl5shkgmdp_o8svgdz8x4wdp7qau94lspr-wvo2lew-sdrdlelhirrlpb-u7ldobw1cczivtd8qu5q4vg.png)

Finally, the data loader requires a Text Splitter node, which specifies how the data from the file should be split when creating the vector store. We use the Recursive Character Text Splitter node, which is the recommended node for most applications.

![Adding a text splitter node](https://media.datacamp.com/cms/ad_4nxf2rbbclo6pxulfmz7uvnohyfu1ittsa7enm108_ypc3lhssmsv-qhgwhwuhivatbojn_ddax1f8qykjw89z4dpcsrvgjexapp06dc67vtcwmgalqzt4gztaprdvyuaw0xvij7a5a.png)

We configure it to use a chunk size of 1,000 and a chunk overlap of 200:

![Configuration of the text splitter in n8n](https://media.datacamp.com/cms/ad_4nxd1x3czi-3cs6ytzgijmu5oeiem9yp7fhazohpuzyjmhgctotsvn4kqgb_ds90xdryb_ociln0u4zmmsb0g8vakvzdizgxvzgppegdny_sm4b4t_kfw79yypo1nnxf2v1jq0nnq9w.png)

When choosing the chunk size and chunk overlap, consider using a larger chunk size for lengthy documents to capture adequate content and a smaller overlap to maintain context between segments without redundancy.

This is what the final workflow looks like:

![Final data loading workflow in n8n](https://media.datacamp.com/cms/ad_4nxcakkyjflbrjvpylwnssuowosoqji6vzkbw7osp31ckx6pgtekvjx3yt2lfyoti9zwr4keudipfbk2agw1wfpevilibrvjh00v-mwojjghrcydj8kkffkgxjgpixiddoafouvb71w.png)

We can run it by clicking “Test workflow”, and once it's done, we can verify in Pinecone that the data was loaded.

### Creating a RAG agent

Here's the final schema for the RAG agent:

![Final RAG agent workflow in n8n](https://media.datacamp.com/cms/ad_4nxf1mvfxmkkflnrb9vnpc2uagd6hpejlo9fth9cisys0fewugh8zj0y1lkktpsqa0b44svq9g3i-xkra3qsaz0jqwo3babzs_o2cwnhm9juus5qxuqddpim47kj2yzdolezwirr3.png)

As an exercise, I encourage you to try to understand it and maybe even recreate it yourself locally before reading further.

We start with an "On chat message" trigger node. This is used to create a chat workflow.

![On chat message trigger node in n8n](https://media.datacamp.com/cms/ad_4nxdygwdm0timowy7odjquvkkej7f9zoo6rrcsj7vdwb74eyvpgyvmi5q7v6mnsdvsvefrugwd4pcbaco7ybj5oowlp4ke7c-aujigf4z6ebu7emmc4-wmesd_dd25rxujyqdapmadw.png)

Next, we connect the chat trigger to an "AI Agent" node with the default options.

![AI Agent node in n8n](https://media.datacamp.com/cms/ad_4nxfvbgqbjmrc3yi_celsqthbcnxpyghglhzgjc4v3kpcpuwrzjqhw2riifvdjg7rpzpaayfs3tflk2koiqttdnq1osryljpqffvxmroinfxgf-emcabck-c2tlt4lgpnz8uu6ifn.png)

Below the AI Agent, we see that we can configure three things:

- The AI model used by the agent.
- The memory defines how the agent remembers the conversation context
- The tools the agent has access to. In this case, we'll provide the Pinecone database as a tool so the agent can answer questions about our document.

For the AI model, we select an "OpenAI Chat Model" node and use the `gpt-4.1` model:

![Configuring the AI model in n8n](https://media.datacamp.com/cms/ad_4nxf6m4r6vm4icciij4vxxit4dtyveotsytarjixtk8psquwkkm9iha7rvf44ls9ckaxsuu-kehtupr9bfle4erhrrdnxtjhpnxemq_phmspitjpnr0lfrmjh4dfynu5fdrptu-bl.png)

For the memory, we use a "Simple Memory" node with a context window of length 5. This means that the agent will remember and consider the five previous interactions when answering.

Finally, in the tool, we add a "Pinecone Vector Store" node with the following configuration:

![Configuration of the Pinecone Vector store tool for the AI agent in n8n](https://media.datacamp.com/cms/ad_4nxeyhsg5a1vlqzljdyafkjimcdwdyacsivjazygooch4ja-blknig1vrxn5n1i-np2puyiwlvcwmyjobstjfvosydsjs9u34ibit2k--ofdrklat8siijldirvkpk91lybrvnb1cja.png)

In the description field, it is important to specify when the tools should be used. This is what the agent will use to determine whether it should call the tool.

The last thing we need is to configure the embedding used by the vector store. As before, we use an OpenAI Embedding node with the model `text-embedding-3-small`:

![Embedding configuration in n8n](https://media.datacamp.com/cms/ad_4nxcc7djhxpxu4jjizwek-k3-l0bws00orz3ndevkuzuwec9h-etmo8ffwl0ml47xdjvpnr3y6t50je-gdknyafssddhxpr8txajzujzh2l_9t-d4omu-impkzoxadwop4kyjcyqnwq.png)

The workflow is complete, and we can chat with the agent. Here's an example:

![Chatting with the AI agent in n8n](https://media.datacamp.com/cms/ad_4nxfbb54ilsiamjsspkq1sdlyfxwyvjvs4fs2hs-yhlx8i5njl0tdufq-tnmasigvaxvwczyalqe2e2qwuyihosuvl0xj9ky3zd8x1gxhqcecdxuabhehr5pnvivxqqcbikl_0l2j0g.png)

We can see on the right the steps that the agent took to answer our question. In particular, it accessed the Pinecone database to fetch the relevant rules information.

## n8n Templates

n8n offers a useful feature that can significantly speed up our workflow creation process: [the n8n template library](https://n8n.io/workflows/).

This library is a collection of pre-built workflows, crafted by the community and n8n experts. Whether we're trying to automate simple tasks or more complex processes, chances are that someone has already built a workflow suited for our needs.

Importing a workflow into our n8n setup means we don't always have to start from scratch. Instead, we can take advantage of the creative solutions other users have developed. Once we've imported a workflow, all we need to do is configure it with our credentials and tweak it to fit our exact requirements.

For any task we wish to automate, from email processing to social media management, it’s highly likely that there's a template available in the library.

## Conclusion

n8n offers a vast ecosystem of integrations, allowing us to connect over a thousand services and tools to create AI agents. We've only scratched the surface of what n8n can do in this tutorial. By exploring how to use n8n for building AI agents to automate everyday tasks, we've just begun to tap into its potential.

## Introduction to AI Agents

Learn the fundamentals of AI agents, their components, and real-world use—no coding required.

[Explore Course](https://www.datacamp.com/courses/introduction-to-ai-agents)

Learn AI with these courses!

Track

### Developing AI Applications

21 hr

Learn to create AI-powered applications with the latest AI developer tools, including the OpenAI API, Hugging Face, and LangChain.

Course

### AI Security and Risk Management

2 hr

7.9K

Learn the fundamentals of AI security to protect systems from threats, align security with business goals, and mitigate key risks.

Course

### Introduction to AI Agents

1 hr 30 min

76.9K

Learn the fundamentals of AI agents, their components, and real-world use—no coding required.

[

See More

](https://www.datacamp.com/category/artificial-intelligence)