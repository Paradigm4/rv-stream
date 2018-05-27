# Usage

Paths need to be adjusted in `load.afl`, `stream.afl`, and `stream.py`.

## Load Data

```bash
> iquery --afl --no-fetch --query-file load.afl
Query was executed successfully
Query was executed successfully
Query was executed successfully
Query was executed successfully
```

## Stream Data and Run RVTest

```bash
> iquery --afl --query-file stream.afl
{instance_id,chunk_no,value_no} CHROM,POS,REF,ALT,N_INFORMATIVE,Test,Beta,SE,Pvalue
{0,0,0} 1,2,'A','G',9,'1:2',-0.257571,0.62456,0.680043
{1,0,0} 1,1,'A','G',9,'1:1',0.18075,0.3885,0.641752
{1,1,0} 1,3,'A','G',9,'1:3',0.858,0.783412,0.273425
```

## Filter Variants

Before running RVTest the input variants can be filtered by
chromosome, position, or individual (`P`) using `filter` or `between`:

```bash
stream(
    filter(var, pos = 1),
    ...
```

```bash
stream(
    between(var, null, 1, null,
                 null, 1, null),
    ...
```

Pheno-types can also be filtered by individual (`P`).

# Single-Threaded RVTest

Running `rvtest` on the initial files directly without using SciDB or
`stream` produces the following output:

```bash
> ../executable/rvtest --pheno pheno --inVcf example.vcf --single wald --out out
> cat out.SingleWald.assoc
CHROM	POS	REF	ALT	N_INFORMATIVE	Test	Beta	SE	Pvalue
1	1	A	G	9	1:1	0.18075	0.3885	0.641752
1	2	A	G	9	1:2	-0.257571	0.62456	0.680043
1	3	A	G	9	1:3	0.858	0.783412	0.273425
```

# Arrays Schema

Here are the array schema used:

```bash
> iquery --afl --query "show(var)"
{i} schema
{0} 'var<gt1:int64,
         gt2:int64,
         phase:int64>
        [chrom=1:20:0:10; pos=1:*:0:10000; p=1:500:0:500]

> iquery --afl --query "limit(var, 10)"
{chrom,pos,p} gt1,gt2,phase
{1,1,4} 1,1,0
{1,1,8} 0,1,0
{1,1,9} 0,1,0
{1,1,11} 0,1,0
{1,1,19} 0,1,0
{1,1,20} 0,1,0
{1,1,21} 0,1,0
{1,1,35} 0,1,0
{1,1,40} 1,1,0
{1,1,42} 0,1,0
```

```bash
> iquery --afl --query "show(pheno)"
{i} schema
{0} 'pheno<iid:string,
           fatid:int64,
           matid:int64,
           sex:int64,
           y1:double,
           y2:double,
           y3:double,
           y4:int64>
          [fid=1:500:0:500]'

> iquery --afl --query "limit(pheno, 5)"
{fid} iid,fatid,matid,sex,y1,y2,y3,y4
{1} 'P1',0,0,0,1.911,-1.465,-0.817,1
{2} 'P2',0,0,2,2.146,-2.451,-0.178,2
{3} 'P3',0,0,2,1.086,-1.194,-0.899,1
{4} 'P4',0,0,2,0.704,-1.052,-0.237,1
{5} 'P5',0,0,1,2.512,-3.085,-2.579,1
```

```bash
> iquery --afl --query "show(assoc)"
{i} schema
{0} 'assoc<CHROM:int64,
           POS:int64,
           REF:string,
           ALT:string,
           N_INFORMATIVE:int64,
           Test:string,
           Beta:double,
           SE:double,
           Pvalue:double>
          [instance_id=0:1:0:1; chunk_no=0:*:0:1; value_no=0:*:0:1073741824]'

> iquery --afl --query "limit(assoc, 2)"
{instance_id,chunk_no,value_no} CHROM,POS,REF,ALT,N_INFORMATIVE,Test,Beta,SE,Pvalue
{0,0,0} 1,1,'A','G',9,'1:1',0.18075,0.3885,0.641752
{0,1,0} 1,3,'A','G',9,'1:3',0.858,0.783412,0.273425
```

# Performance Evaluation

We used the `gen.py` script to generate a `200,000` lines variants
file with `500` individuals and a corresponding phenotype file for the
`500` individuals.

```bash
> python gen.py vcf 20 10000
> wc -l gen.vcf
200001 gen.vcf
> ls -lh gen.vcf
.. 387M gen.vcf
> python gen.py pheno
> wc -l gen.pheno
501 gen.pheno
> ls -lh gen.pheno
... 19K gen.pheno
```

We used two SciDB instances running on the same PC. The PC has an
Intel Core i5 processor at `2.50GHz` and `8 GB` RAM.

## Single-Threaded RVTest

```bash
> ./executable/rvtest --noweb --pheno gen.pheno --inVcf gen.vcf --single wald --out out
...
[INFO]	Program version: 20171009
[INFO]	Analysis started at: Sun May 20 19:00:23 2018
[INFO]	Loaded [ 500 ] samples from genotype files
[INFO]	Loaded [ 500 ] sample pheontypes
[INFO]	Loaded 231 male, 209 female and 60 sex-unknonw samples from gen.pheno
[INFO]	Analysis begins with [ 500 ] samples...
[INFO]	Impute missing genotype to mean (by default)
[INFO]	Analysis started
[INFO]	Analyzed [ 200000 ] variants
[INFO]	Analysis ends at: Sun May 20 19:00:49 2018
[INFO]	Analysis took 26 seconds
RVTESTS finished successfully
```

## Load Variants and Phenotypes in SciDB

```bash
> time iquery --afl --no-fetch --query-file load.afl
...
real	2m16.397s
```

## Stream Data and Run RVTest in SciDB

```bash
> time iquery --no-fetch --afl --query-file stream.afl
...
real	0m44.291s
```

## Filter Variants by Chromosome and Position

```bash
> time iquery --afl --query "filter(var, chrom = 5 and pos = 10)" \
  >  /dev/null
...
real	0m1.704s
```

## Load Variants and Phenotypes as-is in SciDB

Using `load.afl` script from [v0.1](../../tree/v0.1):

```bash
> time iquery --afl --no-fetch --query-file load.afl
...
real	0m10.380s
```
