import logging


class FileToRtreeAnalyzerMap:

    def __init__(self):
        self.rtrees_map = {}

    def add_rtree_analyzer(self, name, rtree_analyzer):
        if name in self.rtrees_map:
            logging.info(f"Overwriting RtreeAnalyzer at substring {name} in FileSubsringToRtreAnalyzerMap.\n"
                         f"Probably not an error.")
        self.rtrees_map[name] = rtree_analyzer

    def get_rtree_analyzer(self, name):
        if name not in self.rtrees_map:
            raise KeyError(f"get_rtree_analyzer called for invalid substring key {name} on "
                           f"FileSubstringToRtreeAnalyzerMap.")
        return self.rtrees_map[name]
