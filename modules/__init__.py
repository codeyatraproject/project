# # modules package 
import warnings

# Silence the pandas FutureWarning about get_group when grouping with a length-1 list-like
warnings.filterwarnings(
    "ignore", 
    message="When grouping with a length-1 list-like, you will need to pass a length-1 tuple to get_group in a future version of pandas",
    category=FutureWarning
) 