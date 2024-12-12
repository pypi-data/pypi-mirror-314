print('hello')

def do(body: dict = None):
    if dict is not None:
        print(body['client_assertion'])
        
do({
    'client_assertion': 
    {
        'chair': 'hello'
    }
    })