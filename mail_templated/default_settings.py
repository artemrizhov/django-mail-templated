# The template for tags that is used to cut the email parts from the rendered
# contents. ``block`` is the name of block, i.e. "subject", "body", "html".
# ``bound`` either "start" or "end".
TAG_FORMAT = '###{bound}_{block}###'

# The template for tag variables that is used to generate the context
# variables for storing the actual email part tags.
TAG_VAR_FORMAT = 'TAG_{BOUND}_{BLOCK}'
