from fastapi import APIRouter

# it's a route instead of entire application which will be using in main.py file
router=APIRouter()

@router.get('/auth')
def auth():
    return {"user":"authenticated"}