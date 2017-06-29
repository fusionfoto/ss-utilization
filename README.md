# SwiftStack Utilization Scripts

This repository contains scripts for gathering utilization data from SwiftStack
controllers via the SwiftStack API

## Installation

`pip install ss-utilization.tar.gz`

## Usage
```
usage: ss-util [-h] -m CONTROLLER_HOST -c CLUSTER_ID -u SSAPI_USER -k
               SSAPI_KEY -s START_DATETIME -e END_DATETIME -p STORAGE_POLICY
               -o OUTPUT_FILE

optional arguments:
  -h, --help            show this help message and exit

required arguments:
  -m CONTROLLER_HOST, --controller CONTROLLER_HOST
                        Hostname of controller
  -c CLUSTER_ID, --cluster CLUSTER_ID
                        ID of cluster on controller
  -u SSAPI_USER, --user SSAPI_USER
                        SwiftStack API User
  -k SSAPI_KEY, --key SSAPI_KEY
                        SwiftStack API Key
  -s START_DATETIME, --start START_DATETIME
                        Start timestamp for utilization in the format yyyy-mm-
                        ddThh:mm:ss[+/-NNNN] (where NNNN is the timezone
                        offset); e.g.: 2013-08-29T19:24:44-0700
  -e END_DATETIME, --end END_DATETIME
                        End timestamp for utilization in the format yyyy-mm-
                        ddThh:mm:ss[+/-NNNN] (where NNNN is the timezone
                        offset); e.g.: 2013-08-29T19:24:44-0700
  -p STORAGE_POLICY, --policy STORAGE_POLICY
                        Storage Policy in cluster
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        file to output utilization data
```

## Example Output
```
account,object_count,container_count,end,bytes_used,start,pct_complete
AUTH_huda,2306093,3505,2017-04-30 21:00:00Z,2336702843453199,2017-04-30 20:00:00Z,66.66666666666666
AUTH_huda,2306324,3505,2017-04-30 22:00:00Z,2337131193450996,2017-04-30 21:00:00Z,66.66666666666666
AUTH_huda,2306530,3505,2017-04-30 23:00:00Z,2337483561906622,2017-04-30 22:00:00Z,66.66666666666666
AUTH_huda,2306832,3505,2017-05-01 00:00:00Z,2337943744696462,2017-04-30 23:00:00Z,66.66666666666666
AUTH_huda,2307035,3505,2017-05-01 01:00:00Z,2338343847180663,2017-05-01 00:00:00Z,66.66666666666666
AUTH_huda,2307239,3505,2017-05-01 02:00:00Z,2338747379670941,2017-05-01 01:00:00Z,66.66666666666666
AUTH_huda,2307465,3505,2017-05-01 03:00:00Z,2339201611084737,2017-05-01 02:00:00Z,66.66666666666666
AUTH_huda,2307702,3505,2017-05-01 04:00:00Z,2339659029502548,2017-05-01 03:00:00Z,66.66666666666666
AUTH_huda,2307950,3505,2017-05-01 05:00:00Z,2340160083454639,2017-05-01 04:00:00Z,66.66666666666666
```