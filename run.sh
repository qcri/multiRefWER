#!/bin/bash -e

# Copyright (C) 2017, Qatar Computing Research Institute, HBKU (author: Ahmed Ali)

# This script shows the usage for the multi reference WER. Results are based on the MGB3 development data

function normalise {
inFile=$1
outFile=$2
cat $inFile | cut -d ' ' -f1 > 1
cat $inFile  | cut -d ' ' -f2- > 2
perl -pe 's/[><|]/A/g;s/p/h/g;s/Y/y/g;' < 2  > 2.norm
paste -d ' ' 1 2.norm > $outFile
rm 1 2 2.norm 
}


# we will use the data where all transcribers marked as non-overlap speech    
awk '{print $1}' data/text_* | sort | uniq -c  | grep " 4 "  | awk '{print $2}'  | sort -u > id$$
for x in  data/{text_*,hyp*}; do
 grep -f id$$ $x > $x.common & 
done
wait

# It is a dialectal speech, and we apply surface normalization; alef, hah, and yah 
for a in data/*.common; do
    normalise $a $a.norm
done

rm id$$ data/*.common

#run the multi-refernce evalaution 
./mrwer.py data/text_noverlap.Ali.common.norm data/text_noverlap.Omar.common.norm data/text_noverlap.Alaa.common.norm \
data/text_noverlap.Mohamed.common.norm data/hyp_chainTDNN_MGB2.QCRI.common.norm > results.brief


## To see all alignmnet results you can use it like this:
./mrwer.py --show-alignment --show-multiple-alignment data/text_noverlap.Ali.common.norm data/text_noverlap.Omar.common.norm \
    data/text_noverlap.Alaa.common.norm data/text_noverlap.Mohamed.common.norm data/hyp_chainTDNN_MGB2.QCRI.common.norm > results.details


echo "Calculate the inter annotation dis-agreemnet:" > inter_annotation_summary
for i in data/text_*.norm; do
    echo $i
    for ii in data/text_*.norm; do
        if [[ $i != $ii ]] ; then 
            compute-wer --text --mode=present ark:${i} ark:${ii} &> del$$; grep WER del$$; rm del$$ # use KALDI for inter annotation dis-agreemnet (assuming you have it in the path)
            #./mrwer.py $i $ii | grep "Overall WER" # you can use also use multi reference script if you don't have KALDI installed  
		fi
    done
    echo "###"
done >> inter_annotation_summary

 
