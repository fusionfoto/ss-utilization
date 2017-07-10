import logging

import csv

logger = logging.getLogger(__name__)


# this needs to be a better "thing" and not just a bunch of methods
class CsvUtilizationWriter(object):
    def __init__(self, data, output_file, data_fields=None):
        self.data = data
        self.output_file = output_file
        self.summary = None
        self.policy_fields = None
        if not data_fields:
            self.fields = self.get_fields(self.data)
        else:
            self.fields = data_fields

    def write_raw_csv(self):
        writer = csv.DictWriter(self.output_file, self.fields)
        writer.writeheader()
        rows = 0
        for account in self.data:
            for policy in self.data[account]:
                for record in self.data[account][policy]:
                    record['account'] = account
                    record['policy'] = policy
                    writer.writerow({field: record.get(field) for field in self.fields})
                    rows += 1
        logger.debug('wrote %d rows to %s' % (rows, self.output_file))

    def write_summary_csv(self):
        if not self.summary:
            self.summarize()

        if not self.policy_fields:
            # try to figure out policy indexes
            firstaccount = [account for account in self.summary][0]
            fields = ['account', 'start', 'end']
            fields += [field for field in self.summary[firstaccount] if field not in fields]
        else:
            fields = ['account', 'start', 'end']
            fields += [policy for policy in self.policy_fields]
            fields += ['bytes_used']

        writer = csv.DictWriter(self.output_file, fields)
        writer.writeheader()
        rows = 0
        sorted_accounts = self.summary.keys()
        sorted_accounts.sort(key=unicode.lower)
        for account in sorted_accounts:
            acct_sum = self.summary[account]
            acct_sum['account'] = account
            writer.writerow({field: acct_sum.get(field) for field in fields})
            rows += 1
        logger.debug('wrote %d rows to %s' % (rows, self.output_file))

    def summarize(self):
        logger.debug('summarizing raw data')
        self.summary = {}
        all_policysums = {}
        for account in self.data:
            accountsum = float(0)
            acctpolicysums = {}
            for policy in self.data[account]:
                policysum = float(0)
                numhours = len(self.data[account][policy])
                starttime = self.data[account][policy][:1][0]['start']
                endtime = self.data[account][policy][-1:][0]['end']
                for record in self.data[account][policy]:
                    policysum += float(record['bytes_used']) / numhours
                accountsum += policysum
                acctpolicysums[policy] = policysum
            self.summary[account] = {'start': starttime,
                                     'end': endtime,
                                     'bytes_used': int(accountsum)}
            for pidx in acctpolicysums:
                self.summary[account][pidx] = int(acctpolicysums[pidx])
                try:
                    all_policysums[pidx] += int(acctpolicysums[pidx])
                except KeyError:
                    all_policysums[pidx] = int(acctpolicysums[pidx])

        all_sum = sum(self.summary[account]['bytes_used'] for account in self.summary)
        logger.debug('summarized %d accounts and %d policies' % (len(self.summary), len(all_policysums)))
        self.summary[u'_TOTAL_BYTES'] = {'start': starttime,
                                         'end': endtime,
                                         'bytes_used': all_sum}
        self.summary[u'_TOTAL_GBYTES'] = {'start': starttime,
                                          'end': endtime,
                                          'bytes_used': float(all_sum) / 10 ** 9}
        self.summary[u'_TOTAL_TBYTES'] = {'start': starttime,
                                          'end': endtime,
                                          'bytes_used': float(all_sum) / 10 ** 12}

        self.policy_fields = all_policysums.keys()
        logger.debug('found %d policy fields in summary: %s' % (len(self.policy_fields),
                                                                self.policy_fields))
        for policy in all_policysums:
            self.summary[u'_TOTAL_BYTES'][policy] = all_policysums[policy]
            self.summary[u'_TOTAL_GBYTES'][policy] = float(all_policysums[policy]) / 10 ** 9
            self.summary[u'_TOTAL_TBYTES'][policy] = float(all_policysums[policy]) / 10 ** 12


    def get_fields(self, data):
        accounts = data.keys()
        policies = data[accounts[0]].keys()
        fields = ['account'] + ['policy'] + data[accounts[0]][policies[0]][0].keys()
        return fields
