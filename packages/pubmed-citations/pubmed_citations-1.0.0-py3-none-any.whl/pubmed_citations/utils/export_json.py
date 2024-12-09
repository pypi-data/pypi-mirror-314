import json


def create_json(texts, outfile='output.json'):
    with open(outfile, 'w') as out:
        json.dump(texts, out, ensure_ascii=False, indent=2)


def create_jsonlines(texts, outfile='output.jl'):
    with open(outfile, 'w') as out:
        for text in texts:
            line = json.dumps(text, ensure_ascii=False)
            out.write(line + '\n')



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
    create_json(texts)
    create_jsonlines(texts)
