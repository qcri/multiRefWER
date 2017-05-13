### Multi-reference WER  for evaluating ASR for languages with no orthographic rules

This code reflects the work described in the ASRU' 2015 paper on MR-WER


### Requirements
* Python (tested with v.2.7.5)

### Sample data: 
* References transcriptions: We provide four different transcriptions for the non-overalp speech in the development set for Arabic MGB-3 task.
* Recognition Transcription: We provide ASR output using TDNN models trained on the 1,200 hours Arabic MGB-2 task.

### Usage:
* ./run.sh shows the usage for the multi refence results 

		./mrwer.py --help
        usage: mrwer.py [-h] [-e] [-ma] [-a] ref [ref ...] hyp
        Multi reference evaluation for ASR against one reference or more.
        positional arguments:
        	ref                   one or more reference transcription
  			hyp                  ASR hypothesis transcription (must be last argument)
		optional arguments:
          -h, --help            show this help message and exit
          -e, --show-errors     Show error per sentence
          -ma, --show-multiple-alignment   Show multi-reference alignment  for each sentence
          -a, --show-alignment   Show alignment  for each sentence


### Citing
The system is described in [this](http://homepages.inf.ed.ac.uk/srenals/ahmed-asru2015.pdf) paper:

    @inproceedings{ali2015multi,
    title={Multi-reference WER for evaluating ASR for languages with no orthographic rules},
    author={Ali, Ahmed and Magdy, Walid and Bell, Peter and Renals, Steve},
    booktitle={Automatic Speech Recognition and Understanding (ASRU), 2015 IEEE Workshop on},
    pages={576--580},
    year={2015},
    organization={IEEE}
    }
    
