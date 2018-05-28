import gc
import os
import pandas
import tempfile
import scidbstrm
import shutil
import subprocess
import sys


root_path = '/tmp'


sys.stderr.write('-- - init - --\n')
inst_path = tempfile.mkdtemp(dir=root_path)
pheno_path = os.path.join(inst_path, 'pheno')
var_path = os.path.join(inst_path, 'var.vcf')
assoc_path = os.path.join(inst_path, 'out')


pheno_df = scidbstrm.read()
sample = len(pheno_df)

# sys.stderr.write('pheno_df: {}\n'.format(sample))
# sys.stderr.write('{}\n'.format(pheno_df.dtypes))
# sys.stderr.write('{}\n'.format(pheno_df.head()))

pheno_df['fid'] = pheno_df[['fid']].apply(lambda x: 'P{}'.format(x[0]), axis=1)
pheno_df.to_csv(
    path_or_buf=pheno_path,
    columns='fid iid fatid matid sex y1 y2 y3 y4'.split(),
    index=False,
    sep=' ')
del pheno_df

scidbstrm.write()


cnt = 0
while True:
    if cnt % 10 == 0:
        sys.stderr.write('-- - iteration {} - --\n'.format(cnt))

    # Read DataFrame
    var_df = scidbstrm.read()

    if var_df is None:
        # End of stream
        break

    # sys.stderr.write('var_df: {}\n'.format(len(var_df)))
    # sys.stderr.write('{}\n'.format(var_df.dtypes))
    # sys.stderr.write('{}\n'.format(var_df.head()))

    with open(var_path, 'a') as f:
        if cnt == 0:
            f.write(
                '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t{}'.format(
                    '\t'.join('P{}'.format(1 + i) for i in range(sample))) +
                '\n')
        p_lst = sample
        chrom = pos = None
        for line in var_df.itertuples(index=False, name=None):
            if chrom == line[3] and pos == line[4]:

                # Empty values between last value and this value
                p_crt = line[5]
                f.write('\t0/0' * (p_crt - p_lst - 1))
                p_lst = p_crt

                # This value
                f.write('\t{}{}{}'.format(
                    line[0],
                    '/' if line[2] == 0 else '|',
                    line[1]))

            else:
                # End previous row
                if chrom is not None:
                    f.write('\t0/0' * (sample - p_lst))
                    f.write('\n')

                # New row attributes
                f.write('\t'.join(map(str, line[3:5])))
                f.write('\t.\tA\tG\t100\t.\t.\tGT')

                # New row empty values
                p_lst = line[5]
                f.write('\t0/0' * (p_lst - 1))

                # New row first non-empty value
                f.write('\t{}{}{}'.format(
                    line[0],
                    '/' if line[2] == 0 else '|',
                    line[1]))

                chrom = line[3]
                pos = line[4]

        # End last row
        f.write('\t0/0' * (sample - p_lst))
        f.write('\n')
    del var_df
    gc.collect()
    cnt +=1

    # Write DataFrame
    scidbstrm.write()


# Run RVTest
assoc_df = None
if cnt:
    cmd = ('/a/executable/rvtest',
           '--noweb',
           '--pheno', pheno_path,
           '--inVcf', var_path,
           '--single', 'wald',
           '--out', assoc_path)
    # sys.stderr.write('cmd: {}\n'.format(' '.join(cmd)))
    rcode = subprocess.call(cmd, stdout=open('/dev/null'))
    if rcode:
        raise Exception('rvtest execution failed')

    assoc_single_path = os.path.join(inst_path, 'out.SingleWald.assoc')
    assoc_df = pandas.read_csv(filepath_or_buffer=assoc_single_path, sep='\t')
    # sys.stderr.write('assoc_df: {}\n'.format(len(assoc_df)))


# Cleanup
# shutil.rmtree(inst_path)

# Write final DataFrame (if any)
sys.stderr.write('-- - stop {} - --\n'.format(cnt))
if assoc_df is not None:
    scidbstrm.write(assoc_df)
else:
    scidbstrm.write()
