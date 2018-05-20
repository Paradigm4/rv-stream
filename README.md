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
{0} 'var<id:string,
         ref:string,
         alt:string,
         qual:int64,
         flt:string,
         info:string,
         fmt:string,
         gt:string>
        [chrom=0:*:0:1; pos=0:*:0:1; p=1:500:0:500]'

> iquery --afl --query "limit(var, 10)"
{chrom,pos,p} id,ref,alt,qual,flt,info,fmt,gt
{1,1,1} '.','A','G',100,'.','.','GT','0/1'
{1,1,2} '.','A','G',100,'.','.','GT','0/0'
{1,1,3} '.','A','G',100,'.','.','GT','0/0'
{1,1,4} '.','A','G',100,'.','.','GT','1/1'
{1,1,5} '.','A','G',100,'.','.','GT','0/1'
{1,1,6} '.','A','G',100,'.','.','GT','0/0'
{1,1,7} '.','A','G',100,'.','.','GT','0/1'
{1,1,8} '.','A','G',100,'.','.','GT','0/1'
{1,1,9} '.','A','G',100,'.','.','GT','0/0'
{1,1,10} '.','A','G',100,'.','.','GT','0/0'
```

```bash
> iquery --afl --query "show(pheno)"
{i} schema
{0} 'pheno<etc:string> [tuple_no=0:*:0:100000]'

 iquery --afl --query "limit(pheno, 2)"
{tuple_no} etc
{0} 'P1 P1 0 0 0 1.911 -1.465 -0.817 1'
{1} 'P2 P2 0 0 2 2.146 -2.451 -0.178 2'
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
