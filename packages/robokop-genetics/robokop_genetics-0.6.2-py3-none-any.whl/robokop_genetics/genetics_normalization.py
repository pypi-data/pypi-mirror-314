from robokop_genetics.services.clingen import ClinGenService, ClinGenSynonymizationResult, batchable_variant_curie_prefixes
from robokop_genetics.genetics_cache import GeneticsCache
import robokop_genetics.node_types as node_types
from robokop_genetics.util import LoggingUtil, Text
import logging
import requests
import os


class GeneticsNormalizer(object):
    DEFAULT_EDGE_NORM_ENDPOINT = f'https://biolink-lookup.transltr.io/'

    logger = LoggingUtil.init_logging(__name__,
                                      logging.INFO,
                                      log_file_path=LoggingUtil.get_logging_path())

    def __init__(self, use_cache: bool = False, bl_version: str = "latest"):
        if use_cache:
            self.cache = GeneticsCache()
            self.logger.info('Robokop Genetics Normalizer initialized with cache activated.')
        else:
            self.cache = None
            self.logger.info('Robokop Genetics Normalizer initialized with no cache activated.')

        if 'EDGE_NORMALIZATION_ENDPOINT' in os.environ:
            self.edge_norm_endpoint = os.environ['EDGE_NORMALIZATION_ENDPOINT']
            self.logger.info(f'Using EDGE_NORMALIZATION_ENDPOINT from env var: {self.edge_norm_endpoint}')
        else:
            self.edge_norm_endpoint = self.DEFAULT_EDGE_NORM_ENDPOINT
            self.logger.info(f'Using default EDGE_NORMALIZATION_ENDPOINT: {self.edge_norm_endpoint}')

        self.bl_version = bl_version
        self.sequence_variant_node_types = self.fetch_sequence_variant_node_types()
        self.clingen = ClinGenService()

    def get_sequence_variant_node_types(self):
        """
        Returns a list of all normalized node types for sequence variant nodes
        :return:
        """
        return self.sequence_variant_node_types

    def fetch_sequence_variant_node_types(self):
        bl_url = f"{self.edge_norm_endpoint}bl/{node_types.SEQUENCE_VARIANT}/ancestors?version={self.bl_version}"
        with requests.session() as client:
            response = client.get(bl_url)
            if response.status_code == 200:
                sequence_variant_node_types = list(set(response.json() + [node_types.SEQUENCE_VARIANT]))
            else:
                sequence_variant_node_types = [node_types.NAMED_THING, node_types.SEQUENCE_VARIANT]
                self.logger.error(
                    f'Failed bl-lookup for {node_types.SEQUENCE_VARIANT} ancestor types: (response code: {response.status_code})')
        return sequence_variant_node_types

    def normalize_variants(self, variant_ids):
        """
        Normalize a list of variants in the most efficient way ie. check the cache, then process in batches if possible.
        :param variant_ids: a list of variant curie identifiers
        :return: a dictionary of normalization information, with the provided curie list as keys
        """

        # if there is a cache active, check it for existing results and grab them
        if self.cache:
            all_normalization_results = self.cache.get_batch_normalization(variant_ids)
            variants_that_need_normalizing = [variant_id for variant_id in variant_ids if variant_id not in all_normalization_results]
            self.logger.info(f'Batch normalizing found {len(all_normalization_results)}/{len(variant_ids)} results in the cache.')
        else:
            all_normalization_results = {}
            variants_that_need_normalizing = variant_ids

        # normalize batches of variants with the same curie prefix because that's how clingen accepts them
        for curie_prefix in batchable_variant_curie_prefixes:
            batchable_variant_curies = [v_curie for v_curie in variants_that_need_normalizing if v_curie.startswith(curie_prefix)]
            batched_normalizations = self.get_batch_sequence_variant_normalization(batchable_variant_curies)
            all_normalization_results.update(batched_normalizations)
            if self.cache:
                # cache the results if possible
                self.cache.set_batch_normalization(batched_normalizations)

        # for remaining variants batching is not possible - try to find results one at a time
        unbatchable_variant_ids = [v_curie for v_curie in variants_that_need_normalizing if v_curie not in all_normalization_results]
        unbatchable_norm_results = map(self.get_sequence_variant_normalization, unbatchable_variant_ids)
        # this could probably be done more efficiently, we only create unbatchable_norm_result_map for the cache
        unbatchable_norm_result_map = {}
        for i, result in enumerate(unbatchable_norm_results):
            if self.cache:
                unbatchable_norm_result_map[unbatchable_variant_ids[i]] = result
            all_normalization_results[unbatchable_variant_ids[i]] = result
        if self.cache:
            # cache the results if possible
            self.cache.set_batch_normalization(unbatchable_norm_result_map)
        return all_normalization_results

    # variant_curie: the id of the variant that needs normalizing
    def get_sequence_variant_normalization(self, variant_curie: str):
        normalizations = []
        # Note that clingen.get_synonyms_by_other_id supports variants which may return multiple synonymization results.
        # So here we may create more than one normalized node for each provided variant curie.
        synonymization_results = self.clingen.get_synonyms_by_other_id(variant_curie)
        for synonymization_result in synonymization_results:
            if synonymization_result.success:
                normalization_dict = {
                    "id": synonymization_result.id,
                    "name": synonymization_result.name,
                    "hgvs": synonymization_result.hgvs,
                    "equivalent_identifiers": synonymization_result.equivalent_identifiers,
                    "robokop_variant_id": synonymization_result.robokop_variant_id,
                    "category": self.sequence_variant_node_types
                }
            else:
                normalization_dict = {
                    "error_type": synonymization_result.error_type,
                    "error_message": synonymization_result.error_message,
                }
            normalizations.append(normalization_dict)
        return normalizations

    # Given a list of batchable curies with the same prefix, return a map of corresponding normalization information.
    def get_batch_sequence_variant_normalization(self, curies: list):
        normalization_map = {}
        # Note that for batch normalization clingen only supports variant types which return a single set of synonyms,
        # as opposed to potentially returning multiple sets such as when calling get_synonyms_by_other_id.
        # Here we always only create one normalized node per provided ID.
        synonymization_results = self.clingen.get_batch_of_synonyms(curies)
        for i, synonymization_result in enumerate(synonymization_results):
            if synonymization_result.success:
                normalization_dict = {
                    "id": synonymization_result.id,
                    "name": synonymization_result.name,
                    "hgvs": synonymization_result.hgvs,
                    "equivalent_identifiers": synonymization_result.equivalent_identifiers,
                    "robokop_variant_id": synonymization_result.robokop_variant_id,
                    "category": self.sequence_variant_node_types
                }
            else:
                normalization_dict = {
                    "error_type": synonymization_result.error_type,
                    "error_message": synonymization_result.error_message,
                }
            normalization_map[curies[i]] = [normalization_dict]
        return normalization_map
