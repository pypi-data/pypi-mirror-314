from inventory_card_reader.processors.image_detector import YoloImageDetector
from inventory_card_reader.processors.page_xml_parser import PageXMLParser
from inventory_card_reader.processors.pero_ocr_processor import PeroOCRProcessor
from inventory_card_reader.processors.postprocessor import PostProcessor
import argparse
import shutil
import os
import appdirs
import yaml

def parse_yaml_config(args):
    with open(args.config, 'r') as f:
        config_data = yaml.safe_load(f)
        for k,v in config_data.items():
            setattr(args, k, v)
    return args

def prepare_resources_dir(use_cache):
    resources_path=appdirs.user_data_dir('inventory_card_reader')
    xml_folder = os.path.join(resources_path,'xml')
    if not use_cache and os.path.isdir(xml_folder):
        shutil.rmtree(xml_folder)
    if not os.path.isdir(xml_folder):
        os.makedirs(xml_folder)
    print(f'Using temporary resources dir {resources_path}.')
    return resources_path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='Path to the config yaml file.')
    parser.add_argument('input_folder', help='Path to the folder which containts the inventory card scans to be processed')
    parser.add_argument('--use_cache', action='store_true', help='Use xmls extracted from previous runs. If not set, cache will be emptied at the start of the execution.')

    try:
        args = parser.parse_args()
    except SystemExit:
        parser.print_help()
        exit()
    args = parse_yaml_config(args)

    return args

def main():
    args = parse_args()
    resources_path = prepare_resources_dir(args.use_cache)    
    xml_folder = os.path.join(resources_path,'xml')

    detector = YoloImageDetector(resources_path)
    ocr_processor = PeroOCRProcessor(args.input_folder, resources_path)
    page_xml_processor = PageXMLParser(args.config, xml_folder,
                                       custom_header_filters=args.header_filters,
                                       file_skip_markers=args.file_skip_markers)
    postprocessor = PostProcessor()
    ocr_processor.parse_directory(args.input_folder)
    detector.parse_directory(args.input_folder)
    results = page_xml_processor.process()
    results = postprocessor.postprocess(results, args.custom_header_mappings)
    postprocessor.dump_to_csv(results)

if __name__ == '__main__':
    main()