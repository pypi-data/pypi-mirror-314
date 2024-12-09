import numpy as np
import bisect
from enum import Enum

class NeuralNet:
    def __init__(self, config: object, input_size: int):
        self._input_size = input_size
        self._second_layer = config['second_layer']
        self._third_layer = config['third_layer']

        bias_size = [ self._second_layer, self._third_layer, 1 ]

        self._bias = []
        for i in range(0, 3):
            bias_vec = np.empty([bias_size[i], 1])
            for j in range(0, bias_size[i]):
                bias_vec[j, 0] = config['bias'][i][j]
            self._bias.append(bias_vec)

        weight_size = [
            (self._second_layer, self._input_size),
            (self._third_layer, self._second_layer),
            (1, self._third_layer)
        ]

        self._weight = []
        for i in range(0, 3):
            weight = np.empty([weight_size[i][0], weight_size[i][1]])
            for x in range(0, weight_size[i][0]):
                for y in range(0, weight_size[i][1]):
                    weight[x, y] = config['weight'][i][x][y]
            self._weight.append(weight)

    def activate(self, x):
        len = x.shape[0]
        for i in range(0, len):
            # ReLU activation
            x[i, 0] = max(0.0, x[i, 0])
    
    def run(self, input: list) -> float:
        input_layer = np.empty([self._input_size, 1])
        for i in range(0, self._input_size):
            input_layer[i, 0] = input[i]

        second_layer = np.matmul(self._weight[0], input_layer)
        second_layer += self._bias[0]
        self.activate(second_layer)

        third_layer = np.matmul(self._weight[1], second_layer)
        third_layer += self._bias[1]
        self.activate(third_layer)

        output = np.matmul(self._weight[2], third_layer)
        output += self._bias[2]

        return output[0, 0]

class Normalizer:
    def __init__(self, config: object, input_size: int):
        self._input_size = input_size
        self._mean = []
        self._std = []
        for i in range(0, self._input_size):
            self._mean.append(config['mean'][i])
            self._std.append(config['std'][i])

    def normalize(self, input: list) -> list:
        output = []
        for i in range(0, self._input_size):
            output.append((input[i] - self._mean[i]) / self._std[i])
        return output
    
CalType = Enum('CalType', ['PLATT', 'ISOTONIC'])

class Calibrator:
    def __init__(self, config: object):
        if config['type'] == 'platt':
            self._type = CalType.PLATT
        elif config['type'] == 'isotonic':
            self._type = CalType.ISOTONIC
        else:
            raise Exception('unknown keyword: ' + config['type'])
        
        if self._type == CalType.PLATT:
            self._a = config['a']
            self._b = config['b']
        else:
            size = len(config['score'])
            self._segs = []
            for i in range(0, size):
                self._segs.append(( config['score'][i], config['prob'][i] ))

    def calibrate(self, score: float):
        if self._type == CalType.PLATT:
            pre = self._a * score + self._b

            # sigmoid
            if pre > 0:
                return 1 / (1 + np.exp(-pre))
            else:
                return np.exp(pre) / (1 + np.exp(pre))
        else:
            l = 0
            r = len(self._segs) - 1
            while l < r:
                mid = (l + r) / 2
                if self._segs[mid][0] >= score:
                    r = mid
                else:
                    l = mid + 1

            return self._segs[l][1]
        
class ClassificationModel:
    def __init__(self, config: object):
        self.input_size_ = config['input_dimension']
        self.output_size_ = len(config['induce_label'])

        self.base_ = []
        self.normalizer_ = []
        self.calibrator_ = []
        for i in range(0, self.output_size_):
            state = config['state'][i]

            if config['base_model_type'] == 'forward_network':
                self.base_.append(NeuralNet(state['base'], self.input_size_))
            else:
                raise Exception('unknown keyword: ' + state['base_model_type'])
            self.normalizer_.append(Normalizer(state['normalizer'], self.input_size_))
            self.calibrator_.append(Calibrator(state['calibrator']))

    def run(self, input: list):
        result = []
        for i in range(0, self.output_size_):
            normalized = self.normalizer_[i].normalize(input)
            base_output = self.base_[i].run(normalized)
            calibrated = self.calibrator_[i].calibrate(base_output)
            result.append(calibrated)
        return result
    
class RankingModel:
    def __init__(self, config: object):
        self.input_size_ = config['input_dimension']
        
        state = config['state']
        if config['base_model_type'] == 'forward_network':
            self.base_ = NeuralNet(state['base'], self.input_size_)
        else:
            raise Exception('unknown keyword: ' + state['base_model_type'])
        self.normalizer_ = Normalizer(state['normalizer'], self.input_size_)

        self.percentile_ = state['percentile']
        if config['output'] == 'value':
            self.value_ = state['value']
        else:
            self.value_ = None

    def run(self, input: list):
        normalized = self.normalizer_.normalize(input)
        base_output = self.base_.run(normalized)

        idx = bisect.bisect_left(self.percentile_, base_output)
        if idx != len(self.percentile_):
            if self.value_ == None:
                return float(idx) / len(self.percentile_)
            else:
                return self.value_[idx]
        else:
            if self.value_ == None:
                return 1
            else:
                return self.value_[-1]
