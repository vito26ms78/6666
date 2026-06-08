class OCRHeatMap:

    def __init__(self):
        self.regions = {}

    def hit(self, region_id):

        self.regions[region_id] = (
            self.regions.get(region_id, 0) + 1
        )

    def priority_regions(self):

        return sorted(
            self.regions,
            key=self.regions.get,
            reverse=True
        )
