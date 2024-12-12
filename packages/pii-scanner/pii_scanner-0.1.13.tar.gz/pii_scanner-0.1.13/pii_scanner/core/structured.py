import time
import logging
import random
from typing import Dict, List, Optional, Union
from multiprocessing import Pool, cpu_count
from pii_scanner.regex_patterns.data_regex import patterns

logger = logging.getLogger(__name__)

class ScannerForStructuredData:
    """
    NER Scanner using Presidio's AnalyzerEngine with SpaCy and regex patterns.
    """

    SPACY_EN_MODEL = "en_core_web_md"

    def __init__(self):
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Initialize variables for lazy loading
        self.analyzer = None
        self.nlp_engine = None
        self.initialized = False

    def _initialize(self):
        """Lazy initialization of the SpaCy model and Presidio Analyzer."""
        if not self.initialized:
            import spacy
            from presidio_analyzer import AnalyzerEngine, PatternRecognizer
            from presidio_analyzer.nlp_engine.spacy_nlp_engine import SpacyNlpEngine

            try:
                self.nlp_engine = spacy.load(self.SPACY_EN_MODEL)
            except OSError:
                self.logger.warning("Downloading en_core_web_md language model for SpaCy")
                from spacy.cli import download
                download(self.SPACY_EN_MODEL)
                self.nlp_engine = spacy.load(self.SPACY_EN_MODEL)

            models_ = [{"lang_code": "en", "model_name": self.SPACY_EN_MODEL}]
            self.analyzer = AnalyzerEngine(nlp_engine=SpacyNlpEngine(models=models_))

            # Create recognizers with the defined patterns and add them in a single loop
            recognizers = [
                PatternRecognizer(supported_entity=entity, patterns=[pattern])
                for entity, pattern in patterns.items()
            ]
            for recognizer in recognizers:
                self.analyzer.registry.add_recognizer(recognizer)

            self.initialized = True

    def _process_with_analyzer(self, texts: List[str]) -> List[Dict[str, Union[str, List[Dict[str, str]]]]]:
        """
        Process texts using the Presidio Analyzer.
        """
        self._initialize()  # Ensure the analyzer is initialized before processing

        results = []
        for text in texts:
            text = text.strip()
            try:
                analyzer_results = self.analyzer.analyze(text, language="en")
                result = {
                    "text": text,
                    "entity_detected": [{
                        "type": entity.entity_type,
                        "start": entity.start,
                        "end": entity.end,
                        "score": entity.score  # You can include the score if needed
                    } for entity in analyzer_results]
                }
                results.append(result)
            except Exception as exc:
                self.logger.error(f"Error processing text '{text}': {exc}")
                results.append({
                    "text": text,
                    "entity_detected": []
                })

        return results

    def _sample_data(self, sample_data: List[str], sample_size: Union[int, float]) -> List[str]:
        """
        Sample the data based on the sample_size, which can be an integer or a percentage.
        """
        total_data_length = len(sample_data)
        if isinstance(sample_size, float) and 0 < sample_size <= 1:
            sample_size = int(total_data_length * sample_size)
        elif isinstance(sample_size, int) and sample_size < total_data_length:
            sample_size = min(sample_size, total_data_length)
        else:
            sample_size = total_data_length

        return random.sample(sample_data, sample_size)

    # def scan(self, sample_data: List[str], chunk_size: int = 100, sample_size: Optional[Union[int, float]] = None) -> Dict[str, List[Dict[str, Union[str, List[Dict[str, str]]]]]]:
    #     """
    #     Scan the input list of text using the AnalyzerEngine and return results.
    #     Can process only a sample of the data if sample_size is specified.
    #     """
    #     start_time = time.time()

    #     if sample_size:
    #         sample_data = self._sample_data(sample_data, sample_size)

    #     # Split the data into chunks
    #     chunks = [sample_data[i:i + chunk_size]
    #               for i in range(0, len(sample_data), chunk_size)]

    #     # Ensure at least 1 worker is available
    #     num_workers = max(1, min(cpu_count(), len(chunks)))

    #     # Process the chunks in parallel
    #     with Pool(processes=num_workers) as pool:
    #         results = pool.map(self._process_with_analyzer, chunks)

    #     # Combine results from all chunks
    #     combined_results = [item for sublist in results for item in sublist]

    #     end_time = time.time()
    #     processing_time = end_time - start_time
    #     self.logger.info(f"Processing completed in {processing_time:.2f} seconds.")  # Use self.logger

    #     return {
    #         "results": combined_results
    #     }
    def scan(self, sample_data: List[str], chunk_size: int = 100, sample_size: Optional[Union[int, float]] = None) -> Dict[str, List[Dict[str, Union[str, List[Dict[str, str]]]]]]:
        """
        Scan the input list of text using the AnalyzerEngine and return results.
        Can process only a sample of the data if sample_size is specified.
        """
        start_time = time.time()

        if sample_size:
            sample_data = self._sample_data(sample_data, sample_size)

        # Split the data into chunks
        chunks = [sample_data[i:i + chunk_size]
                for i in range(0, len(sample_data), chunk_size)]

        # Process the chunks sequentially
        results = []
        for chunk in chunks:
            chunk_result = self._process_with_analyzer(chunk)
            results.extend(chunk_result)

        # Combine results from all chunks
        combined_results = results

        end_time = time.time()
        processing_time = end_time - start_time
        self.logger.info(f"Processing completed in {processing_time:.2f} seconds.")  # Use self.logger

        return {
            "results": combined_results
        }
