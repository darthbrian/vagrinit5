#!/usr/bin/env python3
# This module generates a vagrant init file based on arguments passed in to the module.
# This version utilitizes Classes and Object Orientation instead of traditional function structures.

if __name__ == "__main__":
    import argparse
    from vagrcreate import VagrantClass
    parser = argparse.ArgumentParser(description = "Create a Vagrant initialization file based on a JSON input file.")
    parser.add_argument("filename", help = "The name of the JSON file to be used as input")
    args = parser.parse_args()
    args_dict = vars(args)
    Vagr = VagrantClass(**args_dict)
    Vagr.VagrantCreate()
