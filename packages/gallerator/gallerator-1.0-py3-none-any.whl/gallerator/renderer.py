from pathlib import Path
import argparse

from . import data_types   
    
class Renderer:
    """Abstract base class for renderers to implement"""

    def render(self, template_vars: data_types.TemplateVars):
        """Returns the contents of the index file for template_vars"""
        raise NotImplementedError

    def copy_static(self, gallery_path: Path):
        """Copies any required files to gallery_path"""
        raise NotImplementedError

    def add_argparse_args(self, parser: argparse.ArgumentParser):
        """The renderer can add any command line arguments it supports. Add them
        in an approriately named group."""
        # Default implementation adds no args
        pass
    
    def update_args(self, args: argparse.Namespace):
        """Stores the command line args for use in other methods. Will be called
        immediately after args have been parsed. """
        self.args = args