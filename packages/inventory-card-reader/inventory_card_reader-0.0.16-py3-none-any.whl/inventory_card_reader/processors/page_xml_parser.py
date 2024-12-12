import xml.etree.ElementTree as ET
from glob import glob
from tqdm import tqdm
import os
import yaml

class PageXMLParser:
    def __init__(self, config, xml_folder, custom_header_filters=[], file_skip_markers=[]):
        """
        Initialize the PageXMLParser with a region configuration file and XML folder.
        """
        self.template_regions = self._get_regions(config)
        self.xml_folder = xml_folder
        self.custom_header_filters = custom_header_filters
        self.file_skip_markers = file_skip_markers


    def _get_regions(self, config_yaml):
        """Load regions from the configuration YAML file."""
        with open(config_yaml) as f:
            conf = yaml.safe_load(f)  
        return conf['regions']

    def _get_results_dict(self, xml_path):
        """Initialize a results dictionary to store extracted text data."""
        results_dict = {k: '' for k in self.template_regions.keys()}
        results_dict['source_xml'] = os.path.basename(xml_path)
        return results_dict

    def _is_region_match(self, text_region, template_region, thresh=.8):
        """Check if a text region overlaps sufficiently with a template region."""
        intersection_minx = max(text_region[0], template_region[0])
        intersection_miny = max(text_region[1], template_region[1])
        intersection_maxx = min(text_region[2], template_region[2])
        intersection_maxy = min(text_region[3], template_region[3])

        if intersection_minx > intersection_maxx or intersection_miny > intersection_maxy:
            return False
        intersection_area = (intersection_maxx - intersection_minx) * (intersection_maxy - intersection_miny)
        textbox_area = (text_region[2] - text_region[0]) * (text_region[3] - text_region[1])
        intersection_ratio = intersection_area / textbox_area
        return intersection_ratio > thresh

    def _bbox_from_polygon(self, polygon_string):
        """Convert polygon coordinates to a bounding box."""
        polygon_points = polygon_string.split(' ')
        xs = []
        ys = []
        for point in polygon_points:
            x, y = point.split(',')
            xs.append(int(x))
            ys.append(int(y))
        return [min(xs), min(ys), max(xs), max(ys)]

    def _to_rel_coordinates(self, box, width, height):
        """Convert bounding box coordinates to relative values."""
        x1, y1, x2, y2 = box
        return [x1 / width, y1 / height, x2 / width, y2 / height]

    def _remove_header(self, text, header_name):
        """Remove headers from extracted text."""
        header_variants = [header_name + ':', header_name + ' :', header_name + ' :;', header_name + ':;'] 
        header_variants.extend(self.custom_header_filters)
        header_variants.extend([v.lower() for v in header_variants])
        if text in header_variants or text.lower() in header_variants:
            return None  # text is header only -> discard
        for header_variant in header_variants:
            text = text.replace(header_variant, '')  # remove headers from text
        return text

    def _handle_hyphenation(self, text):
        """Handle hyphenation by removing hyphenation markers."""
        hyphenation_markers = ['- ']
        for hyphenation in hyphenation_markers:
            text = text.replace(hyphenation, '')
        return text

    def _append_safe(self, target_dct, header_name, text):
        """Safely append text to a target dictionary, after removing headers and hyphenation."""
        out_dct = target_dct
        text = self._remove_header(text, header_name)
        if text is None:
            return out_dct
        text = self._handle_hyphenation(text)
        out_dct[header_name] = text
        return out_dct

    def _skip_file(self, xml_path):
        """Check if the file should be skipped based on file name."""
        file_name = os.path.basename(xml_path)
        for skip_marker in self.file_skip_markers:
            if skip_marker in file_name:
                return True
        return False

    def _extract_from_xml(self, xml_path):
        """Extract relevant data from an XML file."""
        results_dict = self._get_results_dict(xml_path)
        tree = ET.parse(xml_path)
        root = tree.getroot()
        ns = {'ns': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15'}

        page_node = root.find('.//ns:Page', ns)
        if not page_node:
            return None
        page_width = int(page_node.get('imageWidth'))
        page_height = int(page_node.get('imageHeight'))

        text_regions = page_node.findall(".//ns:TextRegion", ns)
        for text_region in text_regions:
            region_polygon = text_region.find('ns:Coords', ns).get('points')
            region_box = self._bbox_from_polygon(region_polygon)
            relative_region_box = self._to_rel_coordinates(region_box, page_width, page_height)

            text_nodes = text_region.findall('.//ns:TextLine/ns:TextEquiv/ns:Unicode', ns)
            text_lines = [node.text for node in text_nodes if node.text is not None]
            text = ' '.join(text_lines)

            for column_name, column_box in self.template_regions.items():
                if not self._is_region_match(relative_region_box, column_box):
                    continue
                self._append_safe(results_dict, column_name, text) 
        return results_dict

    def process(self):
        """Process all XML files in the provided folder and output results as CSV."""
        results = []
        xml_files = glob(os.path.join(self.xml_folder, '*.xml'))
        for input_xml in tqdm(xml_files):
            if self._skip_file(input_xml):
                continue
            page_results = self._extract_from_xml(input_xml)
            results.append(page_results)

        return results

