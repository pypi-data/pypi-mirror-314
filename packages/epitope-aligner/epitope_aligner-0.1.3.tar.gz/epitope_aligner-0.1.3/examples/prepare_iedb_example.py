"""
Prepare data for IEDB example

Download epitopes
Download sequences the epitopes are in
Align the sequences
"""

import requests
import pandas as pd
import re
import os
from Bio import SeqIO

base_uri = 'https://query-api.iedb.org'
table_name = "tcell_search"
full_url = base_uri + '/' + table_name

search_params = {
    'parent_source_antigen_iri': 'eq.UNIPROT:P03452',
    # 'parent_source_antigen_iri': f'in.({antigens})',
    'structure_type': 'eq.Linear peptide',
    'host_organism_iri': 'eq.NCBITaxon:9606',
    'qualitative_measure': 'neq.Negative',
    # 'mhc_allele_name': f'in.({mhc_alleles})',
}

result = requests.get(full_url, params=search_params)
epitopes = pd.json_normalize(result.json())

# Formatting and tidying the epitope dataframe
epitopes = epitopes.rename(columns={
    "curated_source_antigen.starting_position":"start",
    "curated_source_antigen.ending_position":"end"
})
epitopes['antigen_acc'] = epitopes["curated_source_antigen.iri"].str.split(":", expand=True)[1]
epitopes['antigen_acc'] = epitopes['antigen_acc'].str.replace("\\.\\d+", "", regex=True)
epitopes['antigen_acc'] = epitopes['antigen_acc'].str.replace("_.$", "", regex=True)

epitopes = epitopes.drop_duplicates(subset=["antigen_acc", "linear_sequence"])

epitopes = epitopes.dropna(subset=["start", "end"])
epitopes.start = epitopes.start.astype(int)
epitopes.end = epitopes.end.astype(int)

epitopes['length'] = epitopes.linear_sequence.apply(len)

ontie_mask = epitopes['curated_source_antigen.iri'].str.contains("ONTIE")
epitopes = epitopes[~ontie_mask]

epitopes[[
    "antigen_acc",
    "linear_sequence",
    "start", "end",
    "length"
]].to_csv("examples/epitopes.csv", index=False)

def download_seq(source, acc):
    downloader = _get_downloader(source)
    print(f"Downloading {acc} from {source}")
    seq = downloader(acc)
    return seq


def _download_uniprot(acc:str)->str:
    r = requests.get(f"https://rest.uniprot.org/uniprotkb/{acc}.fasta")
    return r.text


def _download_genpept(acc:str, db:str="protein", rettype:str="fasta")->str:
    db="protein"
    rettype="fasta"
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi/?db={db}&id={acc}&rettype={rettype}"
    r = requests.get(url)
    return r.text


def _download_fail(acc:str)->str:
    return ""


def _get_downloader(source):
    if source == "UNIPROT":
        return _download_uniprot
    elif source == "GENPEPT":
        return _download_genpept
    elif source == "ONTIE":
        return _download_fail
    else:
        raise ValueError(source, "Unknown downloader source type")

antigen_accs = epitopes['curated_source_antigen.iri'].unique()
antigen_accs = [(antigen.split(":")[0],antigen.split(":")[1]) for antigen in antigen_accs]

seqs = [download_seq(aa[0], aa[1]) for aa in antigen_accs]

with open("examples/antigens.fa", "w") as f:
    f.writelines(seqs)

seqs = list(SeqIO.parse("examples/antigens.fa", "fasta"))
def seqid2acc(id):
    """strip seq.id to get accession number"""
    acc = id
    pipes = acc.count("|")
    if pipes == 2:
        parts = acc.split("|")
        acc = parts[1]
        if acc == "":
            acc = parts[2]
    acc = re.sub("\\.\\d+", "", acc)
    return acc

for r in seqs:
    r.id = seqid2acc(r.id)

SeqIO.write(seqs, "examples/antigens.fa", "fasta")

# Align antigens, could use any aligner but mafft is fast
os.system("mafft examples/antigens.fa > examples/antigens_al.fa")
