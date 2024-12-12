import pandas as pd
import os
from typing import Dict, Any

class PostProcessor:
    def _apply_header_mappings(self, results, mappings):
        headers = list(results[0].keys())
        new_headers = {k: mappings.get(k, k) for k in headers}
        updated_results = []
        for result in results:
            updated_results.append({new_headers[k]: v for k, v in result.items()})

        return updated_results

    def postprocess(self, results: Dict[str, Any], header_mappings: Dict[str, str] = None):
        if header_mappings:
            results = self._apply_header_mappings(results, header_mappings)
        return results

    def dump_to_csv(self, results: Dict[str, Any], out_path='output/results.csv'):
        output_folder = os.path.dirname(out_path)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        df = pd.DataFrame(results)
        df.to_csv(out_path, index=False)
