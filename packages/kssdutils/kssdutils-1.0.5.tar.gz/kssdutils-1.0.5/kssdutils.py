import os
import time
import kssdtool


def allowed_file(filename):
    allowed_extensions = ['.fa', '.fa.gz', '.fasta', '.fasta.gz', '.fna', '.fna.gz', '.fastq', '.fastq.gz', '.fq', 'fq.gz']
    return any(filename.endswith(ext) for ext in allowed_extensions)


def create_mat(filename):
    qrys = []
    refs = []
    dists = []
    with open('distout/distance.out', 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.split()
            if '.fq' in parts[0]:
                if '/' in parts[0]:
                    qry = parts[0].split('/')[-1].split('.fq')[0]
                else:
                    qry = parts[0].split('.fq')[0]
            elif '.fastq' in parts[0]:
                if '/' in parts[0]:
                    qry = parts[0].split('/')[-1].split('.fastq')[0]
                else:
                    qry = parts[0].split('.fastq')[0]
            elif '.fq.gz' in parts[0]:
                if '/' in parts[0]:
                    qry = parts[0].split('/')[-1].split('.fq.gz')[0]
                else:
                    qry = parts[0].split('.fq.gz')[0]
            elif '.fastq.gz' in parts[0]:
                if '/' in parts[0]:
                    qry = parts[0].split('/')[-1].split('.fastq.gz')[0]
                else:
                    qry = parts[0].split('.fastq.gz')[0]
            elif '.fa' in parts[0]:
                if '/' in parts[0]:
                    qry = parts[0].split('/')[-1].split('.fa')[0]
                else:
                    qry = parts[0].split('.fa')[0]
            elif '.fasta' in parts[0]:
                if '/' in parts[0]:
                    qry = parts[0].split('/')[-1].split('.fasta')[0]
                else:
                    qry = parts[0].split('.fasta')[0]
            else:
                qry = parts[0]

            if '.fa' in parts[1]:
                if '/' in parts[1]:
                    ref = parts[1].split('/')[-1].split('.fa')[0]
                else:
                    ref = parts[1].split('.fa')[0]
            elif '.fasta' in parts[1]:
                if '/' in parts[1]:
                    ref = parts[1].split('/')[-1].split('.fasta')[0]
                else:
                    ref = parts[1].split('.fasta')[0]
            else:
                ref = parts[1]
            dist = parts[4]
            qrys.append(qry)
            refs.append(ref)
            dists.append(dist)
    qrys = qrys[1:]
    refs = refs[1:]
    dists = dists[1:]
    qrys_set = list(set(qrys))
    refs_set = list(set(refs))
    distance_matrix = {}
    for q in qrys_set:
        distance_matrix[q] = {}
        for r in refs_set:
            distance_matrix[q][r] = None
    for q, r, d in zip(qrys, refs, dists):
        distance_matrix[q][r] = d
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, 'w') as output_file:
        output_file.write("\t".join([""] + refs_set) + "\n")
        for q in qrys_set:
            row = [q] + [distance_matrix[q][r] for r in refs_set]
            output_file.write("\t".join(map(str, row)) + "\n")


def sketch(shuf_file=None, genome_files=None, output=None, set_opt=None):
    if shuf_file is not None and genome_files is not None and output is not None:
        if not os.path.exists(genome_files):
            print('No such file or directory: ', genome_files)
            return False
        if set_opt is None:
            set_opt = False
        if not allowed_file(genome_files):
            for filename in os.listdir(genome_files):
                if not allowed_file(filename):
                    print('Genome format error for file:', filename)
                    return False
        if not os.path.exists(shuf_file):
            print('No such file: ', shuf_file)
            return False
        print('Sketching...')
        start = time.time()
        if set_opt:
            kssdtool.dist_dispatch(shuf_file, genome_files, output, 1, 0, 0, '')
        else:
            kssdtool.dist_dispatch(shuf_file, genome_files, output, 0, 0, 0, '')
        end = time.time()
        print('Sketch spend time：%.2fs' % (end - start))
        print('Sketch finished!')
        return True
    else:
        print('Args error!!!')
        return False


def dist(ref_sketch=None, qry_sketch=None, output=None, metric=None, flag=None):
    if ref_sketch is not None and qry_sketch is not None and output is not None:
        if not os.path.exists(ref_sketch):
            print('No such file or directory: ', ref_sketch)
            return False
        if not os.path.exists(qry_sketch):
            print('No such file or directory: ', qry_sketch)
            return False
        if flag is None:
            flag = 0
        if metric is None:
            metric = 'mash'

        print('Disting...')
        start = time.time()
        if '/' in output:
            output_dir = os.path.dirname(output)
            output_name = output.split('/')[-1]
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                print("Created directory:", output_dir)
        else:
            output_name = output
        if output_name.endswith(".phy") or output_name.endswith(".phylip"):
            if metric not in ['mash', 'aaf']:
                print('Metric type error, only supports mash or aaf distance')
                return False
            else:
                kssdtool.dist_dispatch(ref_sketch, output, qry_sketch, 2, 0, flag, metric)
                end = time.time()
                print('Dist spend time：%.2fs' % (end - start))
                print('Dist finished!')
                if ref_sketch != qry_sketch:
                    os.remove(output)
                    filename = output.split('/')[-1].split('.')[0] + '.mat'
                    create_mat(filename)
                return True
        else:
            print('Output type error, only supports .phylip (.phy) format:', output_name)
            return False
    else:
        print('Args error!!!')
        return False

