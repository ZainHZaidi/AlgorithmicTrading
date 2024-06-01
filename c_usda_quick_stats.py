import urllib.request

class c_usda_quick_stats:

    def __init__(self):

        self.api_key = 'D1CA2087-5817-35BB-B266-2E5853CA5741'

        self.base_url_api_get = 'http://quickstats.nass.usda.gov/api/api_GET/?key=' + self.api_key + '&'

        self.output_file_path = 'D:/'

    def get_data(self, parameters):
        full_url = self.base_url_api_get + parameters
        s_result = urllib.request.urlopen(full_url)
        s_text = s_result.read().decode('utf-8')
        return eval(eval(s_text.split(",")[-2]))
