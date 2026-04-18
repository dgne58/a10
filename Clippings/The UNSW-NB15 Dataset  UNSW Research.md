---
title: "The UNSW-NB15 Dataset | UNSW Research"
source: "https://research.unsw.edu.au/projects/unsw-nb15-dataset"
author:
published:
created: 2026-04-13
description:
tags:
  - "clippings"
---
![](https://research.unsw.edu.au/sites/default/files/images/projects/UNSW-nb15%20dataset.jpg)  

**Faculty:** [UNSW Canberra at ADFA](https://research.unsw.edu.au/researcher?faculty=UNSW%20Canberra%20at%20ADFA)  

**The UNSW-NB15 source files (pcap files, BRO files, Argus Files, CSV files and the reports) can be downloaded from [HERE](https://unsw-my.sharepoint.com/:f:/g/personal/z5025758_ad_unsw_edu_au/EnuQZZn3XuNBjgfcUu4DIVMBLCHyoLHqOswirpOQifr1ag?e=gKWkLS)**. **You can also use our new datasets created the [TON\_IoT](https://unsw-my.sharepoint.com/:f:/g/personal/z5025758_ad_unsw_edu_au/EvBTaetotpdGnW7rJQ8fCvYBh8063CNeY9W33MpRsarJaQ?e=yZlnxW).**

**\----------------------------------------------------------------------------------------------------**

The raw network packets of the UNSW-NB 15 dataset was created by the IXIA PerfectStorm tool in the Cyber Range Lab of UNSW Canberra for generating a hybrid of real modern normal activities and synthetic contemporary attack behaviours. The tcpdump tool was utilised to capture 100 GB of the raw traffic (e.g., Pcap files). This dataset has nine types of attacks, namely, Fuzzers, Analysis, Backdoors, DoS, Exploits, Generic, Reconnaissance, Shellcode and Worms. The Argus, Bro-IDS tools are used and twelve algorithms are developed to generate totally 49 features with the class label. These features are described in the UNSW-NB15\_features.csv file.

- The total number of records is two million and 540,044 which are stored in the four CSV files, namely, UNSW-NB15\_1.csv, UNSW-NB15\_2.csv, UNSW-NB15\_3.csv and UNSW-NB15\_4.csv.
- The ground truth table is named UNSW-NB15\_GT.csv and the list of event file is called UNSW-NB15\_LIST\_EVENTS.csv.
- A partition from this dataset was configured as a training set and testing set, namely, UNSW\_NB15\_training-set.csv and UNSW\_NB15\_testing-set.csv respectively. The number of records in the training set is 175,341 records and the testing set is 82,332 records from the different types, attack and normal.

\-------------------------------------------------------------------------------------------------------

**The details of the UNSW-NB15 dataset were published in following the papers. For the academic/public use of this dataset, the authors have to cities the following papers:**

1. Moustafa, Nour, and Jill Slay. ["UNSW-NB15: a comprehensive data set for network intrusion detection systems (UNSW-NB15 network data set)."](https://ieeexplore.ieee.org/abstract/document/7348942) *Military Communications and Information Systems Conference (MilCIS)*, 2015. IEEE, 2015.
2. Moustafa, Nour, and Jill Slay. ["The evaluation of Network Anomaly Detection Systems: Statistical analysis of the UNSW-NB15 dataset and the comparison with the KDD99 dataset."](https://www.tandfonline.com/doi/abs/10.1080/19393555.2015.1125974) *Information Security Journal: A Global Perspective* (2016): 1-14.
3. Moustafa, Nour, et al[. "Novel geometric area analysis technique for anomaly detection using trapezoidal area estimation on large-scale networks."](https://ieeexplore.ieee.org/abstract/document/7948715) *IEEE Transactions on Big Data (2017).*
4. Moustafa, Nour, et al. ["Big data analytics for intrusion detection system: statistical decision-making using finite dirichlet mixture models."](https://link.springer.com/chapter/10.1007/978-3-319-59439-2_5) *Data Analytics and Decision Support for Cybersecurity. Springer, Cham, 2017.* 127-156.
5. Sarhan, Mohanad, Siamak Layeghy, Nour Moustafa, and Marius Portmann. [NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems.](https://arxiv.org/abs/2011.09144) In [*Big Data Technologies and Applications: 10th EAI International Conference, BDTA 2020, and 13th EAI International Conference on Wireless Internet, WiCON 2020, Virtual Event, December 11, 2020, Proceedings* (p. 117). Springer Nature.](https://link.springer.com/chapter/10.1007/978-3-030-72802-1_9)

\------------------------------------------------------------------------------------------------------

There are some papers published by the authors for developing, Intrusion Detection, Network Forensics, and Privacy-preserving, and Threat Intelligence approaches in different systems, such as Network Systems, Internet of Things (IoT), SCADA, Industrial IoT, and Industry 4.0. **It is preferable to cite the following papers while comparing with your studies:**

- Moustafa, Nour, et al. ["An Ensemble Intrusion Detection Technique based on proposed Statistical Flow Features for Protecting Network Traffic of Internet of Things."](https://ieeexplore.ieee.org/abstract/document/8470090) *IEEE Internet of Things Journal (2018).*
- Koroniotis, Nickolaos, Moustafa, Nour, et al. ["Towards Developing Network Forensic Mechanism for Botnet Activities in the IoT Based on Machine Learning Techniques."](https://books.google.com.au/books?hl=en&lr=&id=8k5aDwAAQBAJ&oi=fnd&pg=PA30&ots=3NR5WEyk1p&sig=0X03DtpQ7U72nF3ixSWjmMdHD_0#v=onepage&q&f=false) *International Conference on Mobile Networks and Management. Springer, Cham, 2017.*
- Moustafa, Nour, et al. ["Generalized Outlier Gaussian Mixture technique based on Automated Association Features for Simulating and Detecting Web Application Attacks."](https://ieeexplore.ieee.org/abstract/document/8298514) *IEEE Transactions on Sustainable Computing (2018).*
- Keshk, Marwa, Moustafa, Nour, et al. ["Privacy preservation intrusion detection technique for SCADA systems."](https://ieeexplore.ieee.org/abstract/document/8190422/) *Military Communications and Information Systems Conference (MilCIS), 2017. IEEE, 2017.*
- Moustafa, Nour, et al. ["A New Threat Intelligence Scheme for Safeguarding Industry 4.0 Systems."](https://ieeexplore.ieee.org/abstract/document/8374422) *IEEE Access (2018).*
- Moustafa, Nour, et al. ["Anomaly Detection System Using Beta Mixture Models and Outlier Detection." *Progress in Computing, Analytics and Networking. Springer, Singapore, 2018.* 125-135.](https://link.springer.com/chapter/10.1007/978-981-10-7871-2_13)
- Moustafa, Nour, et al.["Flow Aggregator Module for Analysing Network Traffic."](https://link.springer.com/chapter/10.1007/978-981-10-7871-2_3) *Progress in Computing, Analytics and Networking. Springer, Singapore, 2018.* 19-29.
- Moustafa, Nour, et al. ["A Network Forensic Scheme Using Correntropy-Variation for Attack Detection."](https://link.springer.com/chapter/10.1007/978-3-319-99277-8_13) *IFIP International Conference on Digital Forensics. Springer, Cham, 2018.*

\---------------------------------------------------------------------------------------------------

**For more information about designing the new algorithms of the features published in the UNSW-NB15 dataset, please cite Dr.Nour Moustafa’s thesis. The details of the algorithms have been published in Chapter 3.**

- Moustafa, Nour. [Designing an online and reliable statistical anomaly detection framework for dealing with large high-speed network traffic.](http://unsworks.unsw.edu.au/fapi/datastream/unsworks:47438/SOURCE02?view=true) Diss. *University of New South Wales, Canberra, Australia, 2017.*

*\--------------------------------------------------------------------------------------------------*

Free use of the UNSW-NB15 dataset for academic research purposes is hereby granted in perpetuity. Use for commercial purposes should be agreed by the authors. Nour Moustafa and Jill Slay have asserted their rights under the Copyright. To whom intend the use of the UNSW-NB15 dataset have to cite the above five papers.

For more information about the datasets, please contact the author, Dr Nour Moustafa, on his email: [nour.moustafa@unsw.edu.au](mailto:nour.moustafa@unsw.edu.au) or n [our.moustafa@ieee.org](mailto:our.moustafa@ieee.org).

More information about Dr Nour Moustafa is available at:

- [https://www.unsw.adfa.edu.au/our-people/dr-nour-moustafa](https://www.unsw.adfa.edu.au/our-people/dr-nour-moustafa)
- [https://research.unsw.edu.au/people/dr-nour-moustafa-abdelhameed-moustafa](https://research.unsw.edu.au/people/dr-nour-moustafa-abdelhameed-moustafa)
- [https://www.linkedin.com/in/nour-moustafa-0a7a7859/](https://www.linkedin.com/in/nour-moustafa-0a7a7859/)

Last Updated: 02 June 2021

![](https://research.unsw.edu.au/sites/default/files/images/projects/UNSW-nb15%20dataset.jpg)

#### Key contact

[Associate Professor Nour Moustafa](https://research.unsw.edu.au/people/associate-professor-nour-moustafa)

**UNSW Canberra**

**+61 416 817 811**

**nour.moustafa@unsw.edu.au**