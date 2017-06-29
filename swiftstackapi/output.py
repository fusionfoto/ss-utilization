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

    def write_csv(self):
        writer = csv.DictWriter(self.output_file, self.fields)
        writer.writeheader()
        rows=0
        for k in self.data:
            for p in self.data[k]:
                p['account'] = k
                writer.writerow({field: p.get(field) for field in self.fields})
                rows+=1
        logger.debug('wrote %d rows to %s' % (rows, self.output_file))

    def get_fields(self, data):
        accounts = data.keys()
        fields = ['account'] + data[accounts[0]][0].keys()
        return fields
