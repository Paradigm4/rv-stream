import os
import pandas
import tempfile
import scidbstrm
import shutil
import subprocess
import sys


root_path = '/o'
inst_path = tempfile.mkdtemp(dir=root_path)
pheno_path = os.path.join(inst_path, 'pheno')

sys.stderr.write('-- - init - --\n')

pheno_df = scidbstrm.read()

sys.stderr.write('pheno_df: {}\n'.format(len(pheno_df)))
sys.stderr.write('{}\n'.format(pheno_df.dtypes))
sys.stderr.write('{}\n'.format(pheno_df.head()))

pheno_df['fid'] = pheno_df[['fid']].apply(lambda x: 'P{}'.format(x[0]), axis=1)
pheno_df.to_csv(
    path_or_buf=pheno_path,
    columns='fid iid fatid matid sex y1 y2 y3 y4'.split(),
    index=False,
    sep=' ')
scidbstrm.write()


sys.stderr.write('-- - start - --\n')

i = 0
while True:
    # Read DataFrame
    var_df = scidbstrm.read()

    if var_df is None:
        # End of stream
        break

    sys.stderr.write('var_df: {}\n'.format(len(var_df)))
    sys.stderr.write('{}\n'.format(var_df.dtypes))
    sys.stderr.write('{}\n'.format(var_df.head()))

    iter_path = os.path.join(inst_path, '{:03d}'.format(i))
    os.mkdir(iter_path)

    var_path = os.path.join(iter_path, 'var.vcf')
    assoc_path = os.path.join(iter_path, 'out')

    attr_df = var_df[var_df.p == 1].drop(
        columns=['p', 'gt']).set_index(
            ['chrom', 'pos'])

    p_df = var_df[['chrom', 'pos', 'p', 'gt']].set_index(
        ['chrom', 'pos', 'p']).unstack(
            level=-1)

    stack_df = pandas.concat([attr_df, p_df], axis=1, join='inner')
    sys.stderr.write('stack_df: {}\n'.format(len(stack_df)))
    sys.stderr.write('{}\n'.format(stack_df.dtypes[:20]))

    stack_df.to_csv(
        path_or_buf=var_path,
        index_label='#CHROM\tPOS'.split(),
        header='ID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tP1\tP2\tP3\tP4\tP5\tP6\tP7\tP8\tP9\tP10\tP11\tP12\tP13\tP14\tP15\tP16\tP17\tP18\tP19\tP20\tP21\tP22\tP23\tP24\tP25\tP26\tP27\tP28\tP29\tP30\tP31\tP32\tP33\tP34\tP35\tP36\tP37\tP38\tP39\tP40\tP41\tP42\tP43\tP44\tP45\tP46\tP47\tP48\tP49\tP50\tP51\tP52\tP53\tP54\tP55\tP56\tP57\tP58\tP59\tP60\tP61\tP62\tP63\tP64\tP65\tP66\tP67\tP68\tP69\tP70\tP71\tP72\tP73\tP74\tP75\tP76\tP77\tP78\tP79\tP80\tP81\tP82\tP83\tP84\tP85\tP86\tP87\tP88\tP89\tP90\tP91\tP92\tP93\tP94\tP95\tP96\tP97\tP98\tP99\tP100\tP101\tP102\tP103\tP104\tP105\tP106\tP107\tP108\tP109\tP110\tP111\tP112\tP113\tP114\tP115\tP116\tP117\tP118\tP119\tP120\tP121\tP122\tP123\tP124\tP125\tP126\tP127\tP128\tP129\tP130\tP131\tP132\tP133\tP134\tP135\tP136\tP137\tP138\tP139\tP140\tP141\tP142\tP143\tP144\tP145\tP146\tP147\tP148\tP149\tP150\tP151\tP152\tP153\tP154\tP155\tP156\tP157\tP158\tP159\tP160\tP161\tP162\tP163\tP164\tP165\tP166\tP167\tP168\tP169\tP170\tP171\tP172\tP173\tP174\tP175\tP176\tP177\tP178\tP179\tP180\tP181\tP182\tP183\tP184\tP185\tP186\tP187\tP188\tP189\tP190\tP191\tP192\tP193\tP194\tP195\tP196\tP197\tP198\tP199\tP200\tP201\tP202\tP203\tP204\tP205\tP206\tP207\tP208\tP209\tP210\tP211\tP212\tP213\tP214\tP215\tP216\tP217\tP218\tP219\tP220\tP221\tP222\tP223\tP224\tP225\tP226\tP227\tP228\tP229\tP230\tP231\tP232\tP233\tP234\tP235\tP236\tP237\tP238\tP239\tP240\tP241\tP242\tP243\tP244\tP245\tP246\tP247\tP248\tP249\tP250\tP251\tP252\tP253\tP254\tP255\tP256\tP257\tP258\tP259\tP260\tP261\tP262\tP263\tP264\tP265\tP266\tP267\tP268\tP269\tP270\tP271\tP272\tP273\tP274\tP275\tP276\tP277\tP278\tP279\tP280\tP281\tP282\tP283\tP284\tP285\tP286\tP287\tP288\tP289\tP290\tP291\tP292\tP293\tP294\tP295\tP296\tP297\tP298\tP299\tP300\tP301\tP302\tP303\tP304\tP305\tP306\tP307\tP308\tP309\tP310\tP311\tP312\tP313\tP314\tP315\tP316\tP317\tP318\tP319\tP320\tP321\tP322\tP323\tP324\tP325\tP326\tP327\tP328\tP329\tP330\tP331\tP332\tP333\tP334\tP335\tP336\tP337\tP338\tP339\tP340\tP341\tP342\tP343\tP344\tP345\tP346\tP347\tP348\tP349\tP350\tP351\tP352\tP353\tP354\tP355\tP356\tP357\tP358\tP359\tP360\tP361\tP362\tP363\tP364\tP365\tP366\tP367\tP368\tP369\tP370\tP371\tP372\tP373\tP374\tP375\tP376\tP377\tP378\tP379\tP380\tP381\tP382\tP383\tP384\tP385\tP386\tP387\tP388\tP389\tP390\tP391\tP392\tP393\tP394\tP395\tP396\tP397\tP398\tP399\tP400\tP401\tP402\tP403\tP404\tP405\tP406\tP407\tP408\tP409\tP410\tP411\tP412\tP413\tP414\tP415\tP416\tP417\tP418\tP419\tP420\tP421\tP422\tP423\tP424\tP425\tP426\tP427\tP428\tP429\tP430\tP431\tP432\tP433\tP434\tP435\tP436\tP437\tP438\tP439\tP440\tP441\tP442\tP443\tP444\tP445\tP446\tP447\tP448\tP449\tP450\tP451\tP452\tP453\tP454\tP455\tP456\tP457\tP458\tP459\tP460\tP461\tP462\tP463\tP464\tP465\tP466\tP467\tP468\tP469\tP470\tP471\tP472\tP473\tP474\tP475\tP476\tP477\tP478\tP479\tP480\tP481\tP482\tP483\tP484\tP485\tP486\tP487\tP488\tP489\tP490\tP491\tP492\tP493\tP494\tP495\tP496\tP497\tP498\tP499\tP500'.split(),
        sep='\t')

    cmd = ('/a/executable/rvtest',
           '--noweb',
           '--pheno', pheno_path,
           '--inVcf', var_path,
           '--single', 'wald',
           '--out', assoc_path)
    sys.stderr.write('cmd: {}\n'.format(' '.join(cmd)))
    subprocess.call(cmd, stdout=open('/dev/null'))

    assoc_single_path = os.path.join(iter_path, 'out.SingleWald.assoc')
    assoc_df = pandas.read_csv(
        filepath_or_buffer=assoc_single_path,
        sep='\t')
    sys.stderr.write('assoc_df: {}\n'.format(len(assoc_df)))

    # Write DataFrame
    scidbstrm.write(assoc_df)
    i += 1


# Cleanup
# shutil.rmtree(inst_path)

# Write final DataFrame (if any)
sys.stderr.write('-- - stop - --\n')
scidbstrm.write()
