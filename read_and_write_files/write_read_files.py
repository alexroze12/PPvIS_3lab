import json


class WriteRead:
    def write(self, to_json):
        with open('../config/score.json', 'w') as f:
            f.write(json.dumps(to_json))

    def write2(self, to_json):
        with open('../config/score_value.json', 'w') as f:
            f.write(json.dumps(to_json))

    def read(self):
        my_file = open('../config/score.json')
        data = json.load(my_file)
        my_file.close()
        return data

    def read2(self):
        my_file = open('../config/score_value.json')
        data = json.load(my_file)
        my_file.close()
        return data


