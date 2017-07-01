import logging

import csv

logger = logging.getLogger(__name__)


class CsvUtilizationWriter(object):
    def __init__(self, data, output_file, data_fields=None):
        self.data = data
        self.output_file = output_file
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
        fields = ['account', 'start', 'end', 'bytes_used']
        writer = csv.DictWriter(self.output_file, fields)
        writer.writeheader()
        rows = 0
        summary = self.summarize()
        sorted_accounts = summary.keys()
        sorted_accounts.sort()
        for account in sorted_accounts:
            acct_sum = summary[account]
            acct_sum['account'] = account
            writer.writerow({field: acct_sum.get(field) for field in fields})
            rows += 1
        logger.debug('wrote %d rows to %s' % (rows, self.output_file))

    def summarize(self):
        logger.debug('summarizing raw data')
        summary = {}
        for account in self.data:
            accountsum = float(0)
            for policy in self.data[account]:
                policysum = float(0)
                numhours = len(self.data[account][policy])
                starttime = self.data[account][policy][:1][0]['start']
                endtime = self.data[account][policy][-1:][0]['end']
                for record in self.data[account][policy]:
                    policysum += float(record['bytes_used']) / numhours
                accountsum += policysum
            summary[account] = {'start': starttime,
                                'end': endtime,
                                'bytes_used': int(accountsum)}
        all_sum = sum(int(summary[account]['bytes_used']) for account in summary)
        logger.debug('summarized %d accounts' % len(summary))
        summary['_TOTAL_BYTES'] = {'start': starttime,
                                   'end': endtime,
                                   'bytes_used': all_sum}
        summary['_TOTAL_GBYTES'] = {'start': starttime,
                                   'end': endtime,
                                   'bytes_used': all_sum / 10**9}
        summary['_TOTAL_TBYTES'] = {'start': starttime,
                                   'end': endtime,
                                   'bytes_used': all_sum / 10**12}
        return summary

    def get_fields(self, data):
        accounts = data.keys()
        policies = data[accounts[0]].keys()
        fields = ['account'] + ['policy'] + data[accounts[0]][policies[0]][0].keys()
        return fields
