class EsNormalizer:

    def __init__(self, es_response, clip_to_min=None):
        self.e = es_response
        self.min = clip_to_min

    def minmax(self, new_max: float, new_min: float):
        x_max = self.e['hits']['hits'][0]['_score']
        x_min = self.e['hits']['hits'][-1]['_score']

        for i in range(len(self.e['hits']['hits'])):
            x = self.e['hits']['hits'][i]['_score']
            x_ = (x - x_min) / (x_max - x_min) * (new_max - new_min) + new_min
            self.e['hits']['hits'][i]['_score'] = x_

        return self.get_max_score()

    def clip(self, min_: float, max_: float):
        for i in range(len(self.e['hits']['hits'])):
            x = self.e['hits']['hits'][i]['_score']
            self.e['hits']['hits'][i]['_score'] = min_ if x < min_ else max_ if x > max_ else x

        return self.get_max_score()

    def log_scale(self, base=10):
        import math

        for i in range(len(self.e['hits']['hits'])):
            x = self.e['hits']['hits'][i]['_score']
            x_ = math.log(x, base)
            self.e['hits']['hits'][i]['_score'] = x_

        return self.get_max_score()

    def z_score(self):
        import numpy as np

        data = [doc['_score'] for doc in self.e['hits']['hits']]
        mean = np.mean(data)
        std = np.std(data)

        for i in range(len(self.e['hits']['hits'])):
            x = self.e['hits']['hits'][i]['_score']
            x_ = (x - mean) / std
            self.e['hits']['hits'][i]['_score'] = x_

        return self.get_max_score()

    def get_max_score(self):
        self.e['hits']['max_score'] = max([doc['_score'] for doc in self.e['hits']['hits']])

        if self.min is not None:
            self.e['hits']['hits'] = [doc for doc in self.e['hits']['hits'] if doc['_score'] > self.min]
            self.e['hits']['total']['value'] = sum([1 for _ in self.e['hits']['hits']])

        return self.e
