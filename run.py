import sys
sys.path.insert(0, 'app')

import uvicorn

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
    uvicorn.run('app.main:app', reload=True)