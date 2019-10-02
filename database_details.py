# CHANGE THESE VARIABLES TO CONNECT WITH DIFFERENT DB ADDRESSES
# REFERENCED IN INSTRUCTION GUIDELINES.
name = 'raw_data'
client_n = 'localhost'
client_address = 27017

# DO NOT CHANGE BELOW THIS POINT
target_variable = 'RATING_INT'
model_dbname = 'models'
backlog_dbname = 'backlog'


drop_features = ['_id', 'optional', target_variable]