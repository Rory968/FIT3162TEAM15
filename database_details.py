# CHANGE THESE VARIABLES TO CONNECT WITH DIFFERENT DB ADDRESSES
# REFERENCED IN INSTRUCTION GUIDELINES.
name = 'raw_data'
client_n = 'localhost'
client_address = 27017


target_variable = 'RATING_INT'
model_dbname = 'models'


drop_features = ['_id', 'optional', target_variable]