
endpoints                                   anonymous                   authenticated             admin

store/collection                              GET                         GET                       GET, POST
store/collection/pk                           GET                         GET                       GET, PUT, PATCH, DELETE

store/product                                 GET                         GET                       GET, POST
store/product/pk                              GET                         GET                       GET, PUT, PATCH, DELETE
store/product/pk/reviews                      GET                         GET, POST                 GET, POST
store/product/pk/reviews/pk                   GET                         GET, PATCH, DELETE        GET, PATCH, DELETE


store/cart                                    -                           GET, POST                 GET, POST
store/cart/pk                                 -                           GET                       GET
store/cart/pk/items                           -                           GET, POST                 GET, POST
store/cart/pk/items/pk                        -                           GET, PATCH, DELETE        GET, PATCH, DELETE

store/order                                   -                           GET, POST                 GET, POST                          
store/order/pk                                -                           GET                       GET, PATCH, DELETE
store/order/pk/items                          -                           GET                       GET
store/order/pk/items/pk                       -                           GET                       GET, DELETE


user/address                                  -                           GET, POST                 GET, POST
user/address/pk                               -                           GET, PUT, PATCH, DELETE   GET, PUT, PATCH, DELETE
user/payment                                  -                           GET                       GET, PATCH, DELETE
user/profile                                  -                           GET, POST                 GET, 
