import re
import json
from pathlib import Path

import openpyxl


def get_pmid_list(pmids):
    for pmid in pmids:
        pmid = str(pmid)
        if Path(pmid).exists():
            text = Path(pmid).read_text().strip()
            yield from re.split(r'\s+', text)
        else:
            yield pmid



def save_excel(data, outfile='output.xlsx'):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['PMID', 'Count', 'Cited By PMIDs'])
    for item in data:
        row = [item['pmid'], item['count'], ','.join(item['cited_by_pmids'])]
        ws.append(row)
    
    wb.save(outfile)


def save_csv(data, outfile='output.csv', sep=','):
    with open(outfile, 'w') as out:
        out.write(sep.join(['PMID', 'Count', 'Cited By PMIDs']) + '\n')
        for item in data:
            row = [str(item['pmid']), str(item['count']), '|'.join(item['cited_by_pmids'])]
            out.write(sep.join(row) + '\n')


def save_json(data, outfile='output.json'):
    with open(outfile, 'w') as out:
        json.dump(list(data), out, indent=4, ensure_ascii=False)


def save_jsonlines(data, outfile='output.jl'):
    with open(outfile, 'w') as out:
        for item in data:
            line = json.dumps(item, ensure_ascii=False)
            out.write(line + '\n')


if __name__ == '__main__':
    pmid_list = list(get_pmid_list(['1', '2', '3']))
    print(pmid_list)
