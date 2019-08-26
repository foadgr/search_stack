CREATE EXTENSION "uuid-ossp";
CREATE SCHEMA api;
CREATE TABLE api.variant_results (
    pkey UUID NOT NULL DEFAULT uuid_generate_v4 (),
    gene TEXT,
    nucleotide_change TEXT,
    protein_change TEXT,
    other_mappings TEXT,
    alias TEXT,
    transcripts TEXT,
    region TEXT,
    reported_classification TEXT,
    inferred_classification TEXT,
    source TEXT,
    last_evaluated DATE,
    last_updated DATE,
    url TEXT,
    submitter_comment TEXT,
    assembly TEXT,
    chr INTEGER,
    genomic_start INTEGER,
    genomic_stop INTEGER,
    ref TEXT,
    alt TEXT,
    accession TEXT,
    reported_ref TEXT,
    reported_alt TEXT,
    PRIMARY KEY (pkey)
);

-- Make a new data store with some filters for cleaner query outputs.
CREATE VIEW api.variants AS (
SELECT * FROM api.variant_results
WHERE gene IS NOT NULL
AND protein_change IS NOT NULL
AND protein_change !~* 'p.\(=\)|p.='
ORDER BY gene ASC, protein_change ASC
);

/* Apply a regular B-Tree index with the varchar_pattern_ops operator
class will help speed up search queries */
CREATE INDEX ON api.variants (substr(gene, 1, 5) varchar_pattern_ops);
