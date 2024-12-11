# List of queries that we'd like to do in Vizitig, assuming they have been parsed 

Gene(CAST) -> All SubseqMetadata where type=gene and name=CAST
Gene(CAST, [100:500]) -> All SubseqMetadata where type=gene, name=CAST and stop>100 and start < 500

Transcript(NM_002834230) 
Transcript(\*) and Gene(CAST) 

StartCodong(CAST) 




