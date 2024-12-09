import openpyxl


def create_excel(texts, outfile='output.xlsx'):
    wb = openpyxl.Workbook()

    ws = wb.active

    ws.append(['PMID', 'Citation'])

    for i, row in enumerate(texts):
        ws.append(row)

    wb.save(outfile)


if __name__ == '__main__':
    pmid = '31171989'
    texts = [
        [
            pmid,
            'Sinha BK, Mason RP. IS METABOLIC ACTIVATION OF TOPOISOMERASE II POISONS IMPORTANT IN THE MECHANISM OF CYTOTOXICITY?. <i>J Drug Metab Toxicol</i>. 2015;6(3):186. doi:10.4172/2157-7609.1000186',
        ],
        [
            pmid,
            'Sinha, B. K., & Mason, R. P. (2015). IS METABOLIC ACTIVATION OF TOPOISOMERASE II POISONS IMPORTANT IN THE MECHANISM OF CYTOTOXICITY?. <i>Journal of drug metabolism & toxicology</i>, <i>6</i>(3), 186. https://doi.org/10.4172/2157-7609.1000186',
        ]
    ]
    create_excel(texts)
