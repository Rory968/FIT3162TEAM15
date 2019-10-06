# CHANGE THESE VARIABLES TO CONNECT WITH DIFFERENT DB ADDRESSES
# REFERENCED IN INSTRUCTION GUIDELINES.
name = 'raw_data'
client_n = 'localhost'
client_address = 27017

# Explicitly for cloud cluster implementation
username = ''
password = ''

# DO NOT CHANGE BELOW THIS POINT
target_variable = 'RATING_INT'
long = 'LONGITUDEDD_NUM'
lat = 'LATITUDEDD_NUM'
model_dbname = 'models'
backlog_dbname = 'backlog'
features_dbname = 'features'
splitter = 'SCIENTIFIC_DISPLAY_NME'

drop_features = ['_id', 'optional', target_variable]

packages = ['sklearn', 'pymongo', 'pandas', 'subprocess', 'time', 'pathlib', 'pickle', 'errno', 'xlrd', 'xlwt']