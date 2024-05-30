from c_usda_quick_stats import c_usda_quick_stats
import urllib.parse

parameters = 'source_desc=SURVEY' +  \
             '&sector_desc=CROPS' + \
             '&commodity_desc=SOYBEANS'+ \
             '&statisticcat_desc=YIELD'+ \
             '&unit_desc=' + urllib.parse.quote('BU / ACRE') + \
             '&state_alpha=VA' + \
             '&county_name=ESSEX' +\
             f'&year={year}' + \
             '&format=CSV'

stats = c_usda_quick_stats()
val = stats.get_data(parameters)
print(val)
