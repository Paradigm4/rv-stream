import pandas
import random
import sys


def vcf(chrom=1, pos=3):
  with open('gen.vcf', 'w') as f:
    f.write('\t'.join('#CHROM POS ID REF ALT QUAL FILTER INFO FORMAT'.split() +
                      ['P{}'.format(1 + i) for i in range(500)]) + '\n')

    for c in range(chrom):
      for p in range(pos):

        ind = []
        for j in range(500):
          v = random.uniform(0, 500)
          if v <= 404:
            ind.append('0/0')
          elif v <= 494:
            ind.append('0/1')
          else:
            ind.append('1/1')

        f.write('\t'.join(str(e) for e in ([1 + c,
                                            1 + p,
                                            '.',
                                            'A',
                                            'G',
                                            100,
                                            '.',
                                            '.',
                                            'GT'] + ind)) + '\n')


def pheno():
  df = pandas.DataFrame(columns='fid iid fatid matid sex y1 y2 y3 y4'.split())

  for i in range(500):

    j = random.uniform(0, 9)
    if j <= 4:
      sex = 1
    elif j <= 8:
      sex = 2
    else:
      sex = 0

    y1 = random.random() * 4
    y2 = random.random() * 6 - 4
    y3 = random.random() * 5 - 3
    y4 = random.randint(1, 2)

    df.loc[i] = ['P{}'.format(1 + i),
                 'P{}'.format(1 + i),
                 0,
                 0,
                 sex,
                 '{:.3f}'.format(y1),
                 '{:.3f}'.format(y2),
                 '{:.3f}'.format(y3),
                 y4]

  df.to_csv('gen.pheno', sep=' ', index=False)


if __name__ == '__main__':
  if sys.argv[1] == 'vcf':
    try:
      chrom = int(sys.argv[2])
    except:
      chrom = 1
    try:
      pos = int(sys.argv[3])
    except:
      pos = 3
    vcf(chrom, pos)
  elif sys.argv[1] == 'pheno':
    pheno()
