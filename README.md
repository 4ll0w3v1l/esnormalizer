# esnormalizer
Normalize elasticsearch scores with some drawbacks

just use it like this:

normalized_response = EsNormalizer(elasticsearch_response).z_score()

available techniques: minmax(), clip(), log_scale(), z_score()
if you want to set lower threshold for documents, just pass desired threshold in EsNormalizer with doc like this: norm = EsNormalizer(elasticsearch_response, 0)
and after use normalization tecchnique: norm.z_score(); now docs that have z-score less than 0 are filtered out.

response will be the same, except for scores, so that's why known drawbacks are: non-updating argument's stuff, impossible to work with size and from parameters from elasticsearch. Also consider using bigger size parameter, as distribution functions require more data than default 10 rows to work properly.
