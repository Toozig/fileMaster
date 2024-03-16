from pydantic import BaseModel

HG38_ORGANISM = {"organism": "human",
                 "genome_version": "hg38"}

MM10_ORGANISM = {"organism": "mouse",
                 "genome_version": "mm10"}



ORGANISM_DICT = {
    "hg38": HG38_ORGANISM,
    "mm10": MM10_ORGANISM
}


def get_organism_data(genome: str) -> dict:
    if organism in ORGANISM_DICT:
        return ORGANISM_DICT[organism]
    raise ValueError(f"Organism {organism} not found in the organism dictionary.")

class Organism(BaseModel):
    organism: str
    genome_version: str

