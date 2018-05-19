# Usage

Paths need to be adjusted in `load.afl`, `stream.afl`, and `stream.py`.

## Load Data

```bash
> iquery --afl --no-fetch --query-file load.afl
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

# Single-Threaded RVTest

This with the output produced by `rvtest` running on the initial
files:

```bash
> ../executable/rvtest --pheno pheno --inVcf example.vcf --single wald --out out
> cat out.SingleWald.assoc
CHROM	POS	REF	ALT	N_INFORMATIVE	Test	Beta	SE	Pvalue
1	1	A	G	9	1:1	0.18075	0.3885	0.641752
1	2	A	G	9	1:2	-0.257571	0.62456	0.680043
1	3	A	G	9	1:3	0.858	0.783412	0.273425
```

# Arrays Schema

Here are the array schemas used:

```bash
> iquery --afl --query "show(var)"
{i} schema
{0} 'var<etc:string> [tuple_no=0:*:0:1]'
```

```bash
> iquery --afl --query "show(pheno)"
{i} schema
{0} 'pheno<etc:string> [tuple_no=0:*:0:100000]'
```

```bash
> iquery --afl --query "show(assoc)"
{i} schema
{0} 'assoc<CHROM:int64,POS:int64,REF:string,ALT:string,N_INFORMATIVE:int64,Test:string,Beta:double,SE:double,Pvalue:double> [instance_id=0:1:0:1; chunk_no=0:*:0:1; value_no=0:*:0:1073741824]'
```
