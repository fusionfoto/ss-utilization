# SwiftStack Utilization Scripts

This repository contains scripts for gathering utilization data from SwiftStack
controllers via the SwiftStack API

## Installation

`ss-utilization` is distributed as a Python Wheel. You can install this on your system or
create a virtualenv and install in there (recommended).

### Standard Install

1. Install Python 2.7 (for MacOS, see [Homebrew](https://brew.sh/))
2. Download the latest release from the "releases" section on Github
3. Run the command `pip install ss_utilization-X.Y-py2-none-any.whl`

### Virtualenv (recommended)

1. Create a new [Virtualenv](https://virtualenv.pypa.io/en/stable/) by running `virtualenv ss-util`
2. `cd ss-util`
3. `source ./bin/activate`
4. Download the latest release from the "releases" section on Github to this directory
5. Run the command `pip install ss_utilization-X.Y-py2-none-any.whl`

Every time you want to run the script, you will need to run the `source ./bin/activate`
command, and then run the `deactivate` command to return to your normal environment.

## Usage

### Command-line Parameters
```
usage: ss-util [-h] -m CONTROLLER_HOST -c CLUSTER_ID -u SSAPI_USER -k
               SSAPI_KEY -s START_DATETIME -e END_DATETIME -p STORAGE_POLICY
               [STORAGE_POLICY ...] -o OUTPUT_FILE [--raw] [-V] [-v]

optional arguments:
  -h, --help            show this help message and exit
  --raw                 output raw hourly utilization hours; don't summarize
  -V, --version         print version and exit
  -v, --verbose         verbose log messages

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
  -p STORAGE_POLICY [STORAGE_POLICY ...], --policy STORAGE_POLICY [STORAGE_POLICY ...]
                        Storage policies in cluster (can specify multiple,
                        e.g. '-p 1 2')
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        file to output utilization data
```
## Example Summary CSV Output
```
account,start,end,bytes_used
AUTH_huda,2017-04-30 20:00:00Z,2017-05-31 20:00:00Z,2468423089759610
AUTH_brandon,2017-04-30 20:00:00Z,2017-05-31 20:00:00Z,118111600639
brandon,2017-04-30 20:00:00Z,2017-05-31 20:00:00Z,0
.logs,2017-04-30 20:00:00Z,2017-05-31 20:00:00Z,83688382493
AUTH_pmcnully,2017-04-30 20:00:00Z,2017-05-31 20:00:00Z,5106983
AUTH_kmullican,2017-04-30 20:00:00Z,2017-05-31 20:00:00Z,44
.misplaced_objects,2017-04-30 20:00:00Z,2017-05-31 20:00:00Z,0
AUTH_gateway,2017-04-30 20:00:00Z,2017-05-31 20:00:00Z,9039
.utilization,2017-04-30 20:00:00Z,2017-05-31 20:00:00Z,0
AUTH_swiftstack,2017-04-30 20:00:00Z,2017-05-31 20:00:00Z,44
AUTH_standingmandan,2017-04-30 20:00:00Z,2017-05-31 20:00:00Z,0
AUTH_standingmandan2,2017-04-30 20:00:00Z,2017-05-31 20:00:00Z,13130170906
AUTH_bkruse,2017-04-30 20:00:00Z,2017-05-31 20:00:00Z,0
standingmandan,2017-04-30 20:00:00Z,2017-05-31 20:00:00Z,0
```

## Example Raw CSV Output
```
account,object_count,container_count,end,bytes_used,start,pct_complete,policy
AUTH_huda,2306093,3505,2017-04-30 21:00:00Z,2336702843453199,2017-04-30 20:00:00Z,66.66666666666666,2
AUTH_huda,2306324,3505,2017-04-30 22:00:00Z,2337131193450996,2017-04-30 21:00:00Z,66.66666666666666,2
AUTH_huda,2306530,3505,2017-04-30 23:00:00Z,2337483561906622,2017-04-30 22:00:00Z,66.66666666666666,2
AUTH_huda,2306832,3505,2017-05-01 00:00:00Z,2337943744696462,2017-04-30 23:00:00Z,66.66666666666666,2
AUTH_huda,2307035,3505,2017-05-01 01:00:00Z,2338343847180663,2017-05-01 00:00:00Z,66.66666666666666,2
AUTH_huda,2307239,3505,2017-05-01 02:00:00Z,2338747379670941,2017-05-01 01:00:00Z,66.66666666666666,2
AUTH_huda,2307465,3505,2017-05-01 03:00:00Z,2339201611084737,2017-05-01 02:00:00Z,66.66666666666666,2
AUTH_huda,2307702,3505,2017-05-01 04:00:00Z,2339659029502548,2017-05-01 03:00:00Z,66.66666666666666,2
AUTH_huda,2307950,3505,2017-05-01 05:00:00Z,2340160083454639,2017-05-01 04:00:00Z,66.66666666666666,2
AUTH_huda,2308149,3505,2017-05-01 06:00:00Z,2340560784614972,2017-05-01 05:00:00Z,66.66666666666666,2
AUTH_huda,2308354,3505,2017-05-01 07:00:00Z,2340971136604924,2017-05-01 06:00:00Z,66.66666666666666,2
AUTH_huda,2308565,3505,2017-05-01 08:00:00Z,2341395124924355,2017-05-01 07:00:00Z,66.66666666666666,2
AUTH_huda,2308771,3505,2017-05-01 09:00:00Z,2341809795724938,2017-05-01 08:00:00Z,66.66666666666666,2
AUTH_brandon,5502,2,2017-04-30 21:00:00Z,118111600640,2017-04-30 20:00:00Z,66.66666666666666,2
AUTH_brandon,5502,2,2017-04-30 22:00:00Z,118111600640,2017-04-30 21:00:00Z,66.66666666666666,2
AUTH_brandon,5502,2,2017-04-30 23:00:00Z,118111600640,2017-04-30 22:00:00Z,66.66666666666666,2
AUTH_brandon,5502,2,2017-05-01 00:00:00Z,118111600640,2017-04-30 23:00:00Z,66.66666666666666,2
AUTH_brandon,5502,2,2017-05-01 01:00:00Z,118111600640,2017-05-01 00:00:00Z,66.66666666666666,2
AUTH_brandon,5502,2,2017-05-01 02:00:00Z,118111600640,2017-05-01 01:00:00Z,66.66666666666666,2
...
```