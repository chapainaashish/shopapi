
endpoints                               anonymous                   authenticated             admin

collection                              GET                         GET                       GET, POST
collection/pk                           GET                         GET                       GET, PUT, PATCH, DELETE

product                                 GET                         GET, POST                 GET, POST
product/pk                              GET                         GET                       GET, PUT, PATCH, DELETE
product/pk/reviews                      GET                         GET, POST                 GET, POST
product/pk/reviews/pk                   GET                         GET, PATCH, DELETE        GET, PATCH, DELETE

cart                                    -                           GET, POST                 GET, POST
cart/pk                                 -                           GET                       GET
cart/pk/items                           -                           GET, POST                 GET, POST
cart/pk/items/pk                        -                           GET, PATCH, DELETE        GET, PATCH, DELETE

order                                   -                           GET, POST                 GET, POST                           
order/pk                                -                           GET, DELETE               GET, PATCH, DELETE
order/pk/items                          -                           GET                       GET
order/pk/items/pk                       -                           GET, DELETE               GET, DELETE 
order/pk/payment                        -                           GET                       GET, PATCH, DELETE


/address                                -                           GET, POST                 GET, POST
/address/pk                             -                           GET, PUT, PATCH, DELETE   GET, PUT, PATCH, DELETE
/payment                                -                           GET                       GET, PATCH, DELETE
/profile                                -                           GET, POST                 GET, P
