#!/bin/bash

group='fermilab'     # as which group the job should be submitted (default will be genie, but for now we use fermilab group as genie does not work yet)
script='runGENIE.sh' # path to the script to submit 
options=''           # possible args for script

usage ()
{
  echo
  echo './submitGENIE.sh [options]'
  echo
  echo '-g group_name [fermilab (default), genie]'
  echo '-s path_to_script'
  echo '-o script_args'
  echo '-x [run offsite]'
  echo
  exit 1
}

while getopts g:s:o:xh OPT
do
  case ${OPT} in
    g) # genie or fermilab
      group=$OPTARG
      ;;
    s) # script to submit
      script=$OPTARG
      ;;
    o) # optional args for script
      options=$OPTARG
      ;;
    x) # use to run offsite
      offsite=true
      ;;
    h)
      usage
      ;;
    *)
      usage
  esac
done

# set up destination folder based on group

if [ "$group" == 'fermilab' ]
then
  out='/pnfs/fermilab/volatile/genie/'
elif [ "$group" == 'genie' ]
then
  out='/pnfs/genie/scratch/users/goran/'
else
  echo  
  echo "ERROR: wrong group"
  echo
  exit 2 
fi

# set up offsite / onsite resources based on offsite flag

if [ "$offsite" = true ]
then
  resource='OFFSITE'
else
  resource='DEDICATED,OPPORTUNISTIC'
fi

# set up jobsub
source /cvmfs/fermilab.opensciencegrid.org/products/common/etc/setups.sh
setup jobsub_client

jobsub_submit -G $group -M --OS=SL6 --resource-provides=usage_model=$resource file://$script $out $options
