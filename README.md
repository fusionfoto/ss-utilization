# SwiftStack Utilization Scripts

This repository contains scripts for gathering utilization data from SwiftStack
controllers via the SwiftStack API

## Installation

`ss-utilization` is distributed as a Python Wheel. You can install this on your system or
create a virtualenv and install in there (recommended).

### Standard Install

1. Install Python 2.7 (for MacOS, see [Homebrew](https://brew.sh/))
2. Download the latest release from the
   [Releases](https://github.com/swiftstack/ss-utilization/releases) section
3. Run the command `pip install ss_utilization-X.Y-py2-none-any.whl` (where `X.Y` is the
   version downloaded in the previous step)

### Virtualenv (recommended)

1. Create a new [Virtualenv](https://virtualenv.pypa.io/en/stable/) by running `virtualenv ss-util`
2. `cd ss-util`
3. `source ./bin/activate`
4. Download the latest release from the
   [Releases](https://github.com/swiftstack/ss-utilization/releases) section
5. Run the command `pip install ss_utilization-X.Y-py2-none-any.whl` (where `X.Y` is the
   version downloaded in the previous step)

Every time you want to run the script, you will need to run the `source ./bin/activate`
command, and then run the `deactivate` command to return to your normal environment.

## Usage

To gather utilization information for a cluster, you need to know the following:

- SwiftStack API user and key
- Hostname of SwiftStack Controller
- ID of the cluster on the controller (the number that appears in the URL e.g. `NNNN` in
  `https://controller/cluster/NNNN`)
- List of Storage Policy indexes deployed on cluster (numbers appearing in the controller
  UI under Cluster -> Manage -> Configure -> Policies)

Once you have this information, you can gather the per-account-per-policy (and summary)
utilization for the cluster by running the following command:

```
$ ss-util --controller controller-hostname \
    --user username \
    --key 1234567890feeddeadbeef1234567890abcde \
    --cluster 1234 \
    --policy 1 2 \
    --start 2017-06-01T00:00:00-0500 \
    --end 2017-06-30T23:59:59-0500 \
    --output customer-2017-06.csv
```

Where the `start` and `end` parameters correspond to the start and end times for the
performance period, and `output` specifies the CSV file to write the summary.

#### Example Summary CSV Output
```
account,start,end,1,2,bytes_used
.logs,2017-05-31 19:00:00Z,2017-06-30 19:00:00Z,28499455112,104888362854,133387817967
.misplaced_objects,2017-05-31 19:00:00Z,2017-06-30 19:00:00Z,0,0,0
.utilization,2017-05-31 19:00:00Z,2017-06-30 19:00:00Z,3746559,0,3746559
_TOTAL_BYTES,2017-05-31 19:00:00Z,2017-06-30 19:00:00Z,651599361473,2668692414899628,2669344014261102
_TOTAL_GBYTES,2017-05-31 19:00:00Z,2017-06-30 19:00:00Z,651.599361473,2668692.414899628,2669344.014261102
_TOTAL_TBYTES,2017-05-31 19:00:00Z,2017-06-30 19:00:00Z,0.651599361473,2668.692414899628,2669.344014261102
AUTH_bkruse,2017-05-31 19:00:00Z,2017-06-30 19:00:00Z,511194433,0,511194433
AUTH_brandon,2017-05-31 19:00:00Z,2017-06-30 19:00:00Z,34034611,118111600639,118145635250
AUTH_gateway,2017-05-31 19:00:00Z,2017-06-30 19:00:00Z,0,9039,9039
AUTH_huda,2017-05-31 19:00:00Z,2017-06-30 19:00:00Z,39,2668456279649119,2668456279649158
AUTH_kmullican,2017-05-31 19:00:00Z,2017-06-30 19:00:00Z,0,43,43
AUTH_pmcnully,2017-05-31 19:00:00Z,2017-06-30 19:00:00Z,0,5106982,5106982
AUTH_standingmandan,2017-05-31 19:00:00Z,2017-06-30 19:00:00Z,0,0,0
AUTH_standingmandan2,2017-05-31 19:00:00Z,2017-06-30 19:00:00Z,622550930719,13130170907,635681101626
AUTH_swiftstack,2017-05-31 19:00:00Z,2017-06-30 19:00:00Z,0,45,45
brandon,2017-05-31 19:00:00Z,2017-06-30 19:00:00Z,0,0,0
standingmandan,2017-05-31 19:00:00Z,2017-06-30 19:00:00Z,0,0,0
```

### Raw Utilizataion Output
If required the `--raw` parameter can be used to get raw account-policy-hourly utilization
information.

#### Example Raw CSV Output
```
account,policy,object_count,container_count,end,bytes_used,start,pct_complete
...
AUTH_huda,1,1,1,2017-06-30 05:00:00Z,39,2017-06-30 04:00:00Z,100.0
AUTH_huda,1,1,1,2017-06-30 06:00:00Z,39,2017-06-30 05:00:00Z,100.0
AUTH_huda,1,1,1,2017-06-30 07:00:00Z,39,2017-06-30 06:00:00Z,100.0
AUTH_huda,1,1,1,2017-06-30 08:00:00Z,39,2017-06-30 07:00:00Z,100.0
AUTH_huda,1,1,1,2017-06-30 09:00:00Z,39,2017-06-30 08:00:00Z,100.0
AUTH_huda,1,1,1,2017-06-30 10:00:00Z,39,2017-06-30 09:00:00Z,100.0
AUTH_huda,1,1,1,2017-06-30 11:00:00Z,39,2017-06-30 10:00:00Z,100.0
AUTH_huda,1,1,1,2017-06-30 12:00:00Z,39,2017-06-30 11:00:00Z,100.0
AUTH_huda,1,1,1,2017-06-30 13:00:00Z,39,2017-06-30 12:00:00Z,100.0
AUTH_huda,1,1,1,2017-06-30 14:00:00Z,39,2017-06-30 13:00:00Z,100.0
AUTH_huda,1,1,1,2017-06-30 15:00:00Z,39,2017-06-30 14:00:00Z,100.0
AUTH_huda,1,1,1,2017-06-30 16:00:00Z,39,2017-06-30 15:00:00Z,100.0
AUTH_huda,1,1,1,2017-06-30 17:00:00Z,39,2017-06-30 16:00:00Z,100.0
AUTH_huda,1,1,1,2017-06-30 18:00:00Z,39,2017-06-30 17:00:00Z,100.0
AUTH_huda,1,1,1,2017-06-30 19:00:00Z,39,2017-06-30 18:00:00Z,100.0
AUTH_huda,2,2452108,3063,2017-05-31 20:00:00Z,2589049571070371,2017-05-31 19:00:00Z,100.0
AUTH_huda,2,2452213,3063,2017-05-31 21:00:00Z,2589228656237796,2017-05-31 20:00:00Z,100.0
AUTH_huda,2,2452309,3063,2017-05-31 22:00:00Z,2589396351126028,2017-05-31 21:00:00Z,100.0
AUTH_huda,2,2452409,3063,2017-05-31 23:00:00Z,2589558274118405,2017-05-31 22:00:00Z,100.0
AUTH_huda,2,2452508,3063,2017-06-01 00:00:00Z,2589734387328758,2017-05-31 23:00:00Z,100.0
AUTH_huda,2,2452620,3063,2017-06-01 01:00:00Z,2589937171316426,2017-06-01 00:00:00Z,100.0
AUTH_huda,2,2452720,3063,2017-06-01 02:00:00Z,2590098126915504,2017-06-01 01:00:00Z,100.0
AUTH_huda,2,2452807,3063,2017-06-01 03:00:00Z,2590243625698271,2017-06-01 02:00:00Z,100.0
AUTH_huda,2,2452909,3063,2017-06-01 04:00:00Z,2590422122047663,2017-06-01 03:00:00Z,100.0
AUTH_huda,2,2453023,3063,2017-06-01 05:00:00Z,2590595392532682,2017-06-01 04:00:00Z,100.0
AUTH_huda,2,2453112,3063,2017-06-01 06:00:00Z,2590745861976116,2017-06-01 05:00:00Z,100.0
AUTH_huda,2,2453215,3063,2017-06-01 07:00:00Z,2590925040198939,2017-06-01 06:00:00Z,100.0
AUTH_huda,2,2453326,3063,2017-06-01 08:00:00Z,2591101721504170,2017-06-01 07:00:00Z,100.0
...
```

### Command-line Parameter Reference
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

# Known Limitations

Currently, it is required to know what timezone the cluster is in (or how the performance
period is defined) and use that in the timestamp offsets in the start and end parameters. The
SwiftStack API will return everything in UTC.

Also, there is currently no way in the SwiftStack API to query what policies are in use on
a particular cluster, so this information must be known.