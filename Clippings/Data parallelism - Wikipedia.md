---
title: "Data parallelism - Wikipedia"
source: "https://en.wikipedia.org/wiki/Data_parallelism"
author:
  - "[[Contributors to Wikimedia projects]]"
published: 2007-02-12
created: 2026-04-13
description:
tags:
  - "clippings"
---
![](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Sequential_vs._Data_Parallel_job_execution.png/500px-Sequential_vs._Data_Parallel_job_execution.png)

Sequential vs. data-parallel job execution

**Data parallelism** is parallelization across multiple processors in [parallel computing](https://en.wikipedia.org/wiki/Parallel_computing "Parallel computing") environments. It focuses on distributing the data across different nodes, which operate on the data in parallel. It can be applied on regular data structures like arrays and matrices by working on each element in parallel. It contrasts to [task parallelism](https://en.wikipedia.org/wiki/Task_parallelism "Task parallelism") as another form of parallelism.

A data parallel job on an array of *n* elements can be divided equally among all the processors. Let us assume we want to sum all the elements of the given array and the time for a single addition operation is Ta time units. In the case of sequential execution, the time taken by the process will be *n* ×Ta time units as it sums up all the elements of an array. On the other hand, if we execute this job as a data parallel job on 4 processors the time taken would reduce to (*n* /4)×Ta + merging overhead time units. Parallel execution results in a speedup of 4 over sequential execution. The [locality of data references](https://en.wikipedia.org/wiki/Locality_of_reference "Locality of reference") plays an important part in evaluating the performance of a data parallel programming model. Locality of data depends on the memory accesses performed by the program as well as the size of the cache.

## History

Exploitation of the concept of data parallelism started in 1960s with the development of the Solomon machine.[^2] The Solomon machine, also called a [vector processor](https://en.wikipedia.org/wiki/Vector_processor "Vector processor"), was developed to expedite the performance of mathematical operations by working on a large data array (operating on multiple data in consecutive time steps). [Concurrency](https://en.wikipedia.org/wiki/Concurrency_\(computer_science\) "Concurrency (computer science)") of data operations was also exploited by operating on multiple data at the same time using a single instruction. These processors were called 'array processors'.[^3] In the 1980s, the term was introduced [^4] to describe this programming style, which was widely used to program [Connection Machines](https://en.wikipedia.org/wiki/Connection_Machine "Connection Machine") in data parallel languages like [C\*](https://en.wikipedia.org/wiki/C* "C*"). Today, data parallelism is best exemplified in [graphics processing units](https://en.wikipedia.org/wiki/Graphics_processing_unit "Graphics processing unit") (GPUs), which use both the techniques of operating on multiple data in space and time using a single instruction.

Most data parallel hardware supports only a fixed number of parallel levels, often only one. This means that within a parallel operation it is not possible to launch more parallel operations recursively, and means that programmers cannot make use of nested hardware parallelism. The programming language [NESL](https://en.wikipedia.org/wiki/NESL "NESL") was an early effort at implementing a nested data-parallel programming model on flat parallel machines, and in particular introduced the [flattening transformation](https://en.wikipedia.org/wiki/Flattening_transformation "Flattening transformation") that transforms nested data parallelism to flat data parallelism. This work was continued by other languages such as [Data Parallel Haskell](https://en.wikipedia.org/w/index.php?title=Data_Parallel_Haskell&action=edit&redlink=1 "Data Parallel Haskell (page does not exist)") and [Futhark](https://en.wikipedia.org/wiki/Futhark_\(programming_language\) "Futhark (programming language)"), although arbitrary nested data parallelism is not widely available in current data-parallel programming languages.

## Description

In a multiprocessor system executing a single set of instructions ([SIMD](https://en.wikipedia.org/wiki/SIMD "SIMD")), data parallelism is achieved when each processor performs the same task on different distributed data. In some situations, a single execution thread controls operations on all the data. In others, different threads control the operation, but they execute the same code.

For instance, consider [matrix multiplication](https://en.wikipedia.org/wiki/Matrix_multiplication "Matrix multiplication") and addition in a sequential manner as discussed in the example.

## Example

Below is the sequential pseudo-code for multiplication and addition of two matrices where the result is stored in the matrix C. The pseudo-code for multiplication calculates the [dot product](https://en.wikipedia.org/wiki/Dot_product "Dot product") of two matrices A, B and stores the result into the output matrix C.

If the following programs were executed sequentially, the time taken to calculate the result would be of the ${\displaystyle O(n^{3})}$ (assuming row lengths and column lengths of both matrices are n) and ${\displaystyle O(n)}$ for multiplication and addition respectively.

```
// Matrix multiplication
for (int i = 0; i < A.rowLength(); i++) {    
    for (int k = 0; k < B.columnLength(); k++) {
        int sum = 0;
        for (int j = 0; j < A.columnLength(); j++) {
            sum += A[i][j] * B[j][k];
        }
        C[i][k] = sum;
    }
}
```

```
// Array addition
for (int i = 0; i < c.size(); i++) {
    c[i] = a[i] + b[i];
}
```

We can exploit data parallelism in the preceding code to execute it faster as the arithmetic is loop independent. Parallelization of the matrix multiplication code is achieved by using [OpenMP](https://en.wikipedia.org/wiki/OpenMP "OpenMP"). An OpenMP directive, "omp parallel for" instructs the compiler to execute the code in the for loop in parallel. For multiplication, we can divide matrix A and B into blocks along rows and columns respectively. This allows us to calculate every element in matrix C individually thereby making the task parallel. For example: *A\[m x n\] dot B \[n x k\]* can be finished in ${\displaystyle O(n)}$ instead of ${\displaystyle O(m*n*k)}$ when executed in parallel using *m\*k* processors.

![](https://upload.wikimedia.org/wikipedia/commons/6/68/Data_Parallelism_in_matrix_multiplication.png)

Data parallelism in matrix multiplication

```
// Matrix multiplication in parallel
#pragma omp parallel for schedule(dynamic,1) collapse(2)
for (int i = 0; i < A.rowLength(); i++) {
    for (int k = 0; k < B.columnLength(); k++) {
        int sum = 0;
        for (int j = 0; j < A.columnLength(); j++) {
            sum += A[i][j] * B[j][k];
        }
        C[i][k] = sum;
    }
}
```

It can be observed from the example that a lot of processors will be required as the matrix sizes keep on increasing. Keeping the execution time low is the priority but as the matrix size increases, we are faced with other constraints like complexity of such a system and its associated costs. Therefore, constraining the number of processors in the system, we can still apply the same principle and divide the data into bigger chunks to calculate the product of two matrices.[^5]

For addition of arrays in a data parallel implementation, let's assume a more modest system with two [central processing units](https://en.wikipedia.org/wiki/Central_processing_unit "Central processing unit") (CPU) A and B, CPU A could add all elements from the top half of the arrays, while CPU B could add all elements from the bottom half of the arrays. Since the two processors work in parallel, the job of performing array addition would take one half the time of performing the same operation in serial using one CPU alone.

The program expressed in [pseudocode](https://en.wikipedia.org/wiki/Pseudocode "Pseudocode") below—which applies some arbitrary operation, `foo`, on every element in the array `d` —illustrates data parallelism:[^1]

```
if CPU = "a" then
    lower_limit := 1
    upper_limit := round(d.length / 2)
else if CPU = "b" then
    lower_limit := round(d.length / 2) + 1
    upper_limit := d.length

for i from lower_limit to upper_limit by 1 do
    foo(d[i])
```

In an [SPMD](https://en.wikipedia.org/wiki/SPMD "SPMD") system executed on 2 processor system, both CPUs will execute the code.

Data parallelism emphasizes the distributed (parallel) nature of the data, as opposed to the processing (task parallelism). Most real programs fall somewhere on a continuum between task parallelism and data parallelism.

## Steps to parallelization

The process of parallelizing a sequential program can be broken down into four discrete steps.[^6]

| Type | Description |
| --- | --- |
| Decomposition | The program is broken down into tasks, the smallest exploitable unit of concurrence. |
| Assignment | Tasks are assigned to processes. |
| Orchestration | Data access, communication, and synchronization of processes. |
| Mapping | Processes are bound to processors. |

## Data parallelism vs. task parallelism

| Data parallelism | Task parallelism |
| --- | --- |
| Same operations are performed on different subsets of same data. | Different operations are performed on the same or different data. |
| Synchronous computation | Asynchronous computation |
| Speedup is more as there is only one execution thread operating on all sets of data. | Speedup is less as each processor will execute a different thread or process on the same or different set of data. |
| Amount of parallelization is proportional to the input data size. | Amount of parallelization is proportional to the number of independent tasks to be performed. |
| Designed for optimum [load balance](https://en.wikipedia.org/wiki/Load_balancing_\(computing\) "Load balancing (computing)") on multi processor system. | Load balancing depends on the availability of the hardware and scheduling algorithms like static and dynamic scheduling. |

## Data parallelism vs. model parallelism

| Data parallelism | Model parallelism |
| --- | --- |
| Same model is used for every thread but the data given to each of them is divided and shared. | Same data is used for every thread, and model is split among threads. |
| It is fast for small networks but very slow for large networks since large amounts of data needs to be transferred between processors all at once. | It is slow for small networks and fast for large networks. |
| Data parallelism is ideally used in array and matrix computations and convolutional neural networks | Model parallelism finds its applications in deep learning |

[^7]

## Mixed data and task parallelism

Data and task parallelism, can be simultaneously implemented by combining them together for the same application. This is called Mixed data and task parallelism. Mixed parallelism requires sophisticated scheduling algorithms and software support. It is the best kind of parallelism when communication is slow and number of processors is large.[^8]

Mixed data and task parallelism has many applications. It is particularly used in the following applications:

1. Mixed data and task parallelism finds applications in the global climate modeling. Large data parallel computations are performed by creating grids of data representing Earth's atmosphere and oceans and task parallelism is employed for simulating the function and model of the physical processes.
2. In timing based [circuit simulation](https://en.wikipedia.org/wiki/Circuit_simulation "Circuit simulation"). The data is divided among different sub-circuits and parallelism is achieved with orchestration from the tasks.

## Data parallel programming environments

A variety of data parallel programming environments are available today, most widely used of which are:

1. [Message Passing Interface](https://en.wikipedia.org/wiki/Message_Passing_Interface "Message Passing Interface"): It is a cross-platform message passing programming interface for parallel computers. It defines the semantics of library functions to allow users to write portable message passing programs in C, C++ and Fortran.
2. [OpenMP](https://en.wikipedia.org/wiki/OpenMP "OpenMP"):[^9] It's an Application Programming Interface (API) which supports [shared memory](https://en.wikipedia.org/wiki/Shared_memory "Shared memory") programming models on multiple platforms of multiprocessor systems. Since version 4.5, OpenMP is also able to target devices other than typical CPUs. It can program FPGAs, DSPs, GPUs and more. It is not confined to GPUs like OpenACC.
3. [CUDA](https://en.wikipedia.org/wiki/CUDA "CUDA") and [OpenACC](https://en.wikipedia.org/wiki/OpenACC "OpenACC"): CUDA and OpenACC (respectively) are parallel computing API platforms designed to allow a software engineer to utilize GPUs' computational units for general purpose processing.
4. [Threading Building Blocks](https://en.wikipedia.org/wiki/Threading_Building_Blocks "Threading Building Blocks") and [RaftLib](https://en.wikipedia.org/wiki/RaftLib "RaftLib"): Both open source programming environments that enable mixed data/task parallelism in C/C++ environments across heterogeneous resources.

## Applications

Data parallelism finds its applications in a variety of fields ranging from physics, chemistry, biology, material sciences to signal processing. Sciences imply data parallelism for simulating models like molecular dynamics,[^10] sequence analysis of genome data [^11] and other physical phenomenon. Driving forces in signal processing for data parallelism are video encoding, image and graphics processing, wireless communications [^12] to name a few.

### Data-intensive computing

[Data-intensive computing](https://en.wikipedia.org/wiki/Data-intensive_computing "Data-intensive computing") is a class of [parallel computing](https://en.wikipedia.org/wiki/Parallel_computing "Parallel computing") applications which use a [data parallel](https://en.wikipedia.org/wiki/Data_parallel "Data parallel") approach to process large volumes of data typically [terabytes](https://en.wikipedia.org/wiki/Terabytes "Terabytes") or [petabytes](https://en.wikipedia.org/wiki/Petabytes "Petabytes") in size and typically referred to as [big data](https://en.wikipedia.org/wiki/Big_data "Big data"). Computing applications that devote most of their execution time to computational requirements are deemed compute-intensive, whereas applications are deemed data-intensive if they require large volumes of data and devote most of their processing time to [input/output](https://en.wikipedia.org/wiki/Input/output "Input/output") and manipulation of data.[^13]

[^1]: Some input data (e.g. when `d.length` evaluates to 1 and `round` rounds towards zero \[this is just an example, there are no requirements on what type of rounding is used\]) will lead to `lower_limit` being greater than `upper_limit`, it's assumed that the loop will exit immediately (i.e. zero iterations will occur) when this happens.

[^2]: ["The Solomon Computer"](https://www.computer.org/csdl/pds/api/csdl/proceedings/download-article/50610097/pdf?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJjc2RsX2FwaSIsImF1ZCI6ImNzZGxfYXBpX2Rvd25sb2FkX3Rva2VuIiwic3ViIjoiYW5vbnltb3VzQGNvbXB1dGVyLm9yZyIsImVtYWlsIjoiYW5vbnltb3VzQGNvbXB1dGVyLm9yZyIsImV4cCI6MTU2NTEwNTAxMX0.AD74lJbBAdGWNvVIpeeTmyF1S7hb4_rUDeSeoDoJ0R4).

[^3]: ["SIMD/Vector/GPU"](https://www.ece.cmu.edu/~ece740/f13/lib/exe/fetch.php%3Fmedia%3Dseth-740-fall13-module5.1-simd-vector-gpu.pdf) (PDF). Retrieved 2016-09-07.

[^4]: [Hillis, W. Daniel](https://en.wikipedia.org/wiki/Daniel_Hillis "Daniel Hillis") and [Steele, Guy L.](https://en.wikipedia.org/wiki/Guy_Steele "Guy Steele"), [Data Parallel Algorithms](https://dx.doi.org/10.1145/7902.7903) [Communications of the ACM](https://en.wikipedia.org/wiki/Communications_of_the_ACM "Communications of the ACM") December 1986

[^5]: Barney, Blaise. ["Introduction to Parallel Computing"](https://web.archive.org/web/20130610122229/https://computing.llnl.gov/tutorials/parallel_comp/). *computing.llnl.gov*. Archived from [the original](https://computing.llnl.gov/tutorials/parallel_comp/) on 2013-06-10. Retrieved 2016-09-07.

[^6]: Solihin, Yan (2016). *Fundamentals of Parallel Architecture*. Boca Raton, FL: CRC Press. [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [978-1-4822-1118-4](https://en.wikipedia.org/wiki/Special:BookSources/978-1-4822-1118-4 "Special:BookSources/978-1-4822-1118-4").

[^7]: ["How to Parallelize Deep Learning on GPUs Part 2/2: Model Parallelism"](http://timdettmers.com/2014/11/09/model-parallelism-deep-learning/). *Tim Dettmers*. 2014-11-09. Retrieved 2016-09-13.

[^8]: ["The Netlib"](http://www.netlib.org/lapack/lawnspdf/lawn97.pdf) (PDF).

[^9]: ["OpenMP.org"](https://web.archive.org/web/20160905232633/http://openmp.org/wp/). *openmp.org*. Archived from [the original](http://openmp.org/wp/) on 2016-09-05. Retrieved 2016-09-07.

[^10]: Boyer, L. L; Pawley, G. S (1988-10-01). "Molecular dynamics of clusters of particles interacting with pairwise forces using a massively parallel computer". *Journal of Computational Physics*. **78** (2): 405–423. [Bibcode](https://en.wikipedia.org/wiki/Bibcode_\(identifier\) "Bibcode (identifier)"):[1988JCoPh..78..405B](https://ui.adsabs.harvard.edu/abs/1988JCoPh..78..405B). [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1016/0021-9991(88)90057-5](https://doi.org/10.1016%2F0021-9991%2888%2990057-5).

[^11]: Yap, T.K.; Frieder, O.; Martino, R.L. (1998). "Parallel computation in biological sequence analysis". *IEEE Transactions on Parallel and Distributed Systems*. **9** (3): 283–294. [Bibcode](https://en.wikipedia.org/wiki/Bibcode_\(identifier\) "Bibcode (identifier)"):[1998ITPDS...9..283Y](https://ui.adsabs.harvard.edu/abs/1998ITPDS...9..283Y). [CiteSeerX](https://en.wikipedia.org/wiki/CiteSeerX_\(identifier\) "CiteSeerX (identifier)") [10.1.1.30.2819](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.30.2819). [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1109/71.674320](https://doi.org/10.1109%2F71.674320).

[^12]: Singh, H.; Lee, Ming-Hau; Lu, Guangming; Kurdahi, F.J.; Bagherzadeh, N.; Filho, E.M. Chaves (2000-06-01). ["MorphoSys: an integrated reconfigurable system for data-parallel and computation-intensive applications"](https://www.researchgate.net/publication/3044209). *IEEE Transactions on Computers*. **49** (5): 465–481. [Bibcode](https://en.wikipedia.org/wiki/Bibcode_\(identifier\) "Bibcode (identifier)"):[2000ITCmp..49..465S](https://ui.adsabs.harvard.edu/abs/2000ITCmp..49..465S). [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1109/12.859540](https://doi.org/10.1109%2F12.859540). [ISSN](https://en.wikipedia.org/wiki/ISSN_\(identifier\) "ISSN (identifier)") [0018-9340](https://search.worldcat.org/issn/0018-9340).

[^13]: [Handbook of Cloud Computing](http://www.cse.fau.edu/~borko/HandbookofCloudComputing.html), "Data-Intensive Technologies for Cloud Computing," by A.M. Middleton. Handbook of Cloud Computing. Springer, 2010.