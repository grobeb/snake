from mc import *                                    
                                
                                                    
def post(message):                                  
    print(message)                                  
    world.postToChat(message)                       

x, y, z = player.getPos()
                                                    
# post('{}, {}, {}'.format(int(x), int(y), int(z)))                                                      

# test = 'test message '                              
                                                    
# message = 'John'                                    
                                                    
# post('my name is ' + message)                       
# post('my name is {}'.format(message))               
# post(f'my name is {message}')                       

# print(list(test))                                   
# print(list(test)[3]) 

# a = post('our names are {} {} {}'.format("john", "jack", "mark"))