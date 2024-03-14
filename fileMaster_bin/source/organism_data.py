from pydantic import BaseModel

HG38_ORGANISM = {"organism": "human",
                 "genome_version": "hg38"}

MM10_ORGANISM = {"organism": "mouse",
                 "genome_version": "mm10"}



ORGANISM_DICT = {
    "hg38": HG38_ORGANISM,
    "mm10": MM10_ORGANISM
}

class Organism(BaseModel):
    organism: str
    genome_version: str

