# Database Model
// FUNCTION NAME
class FunctionName(Base): 
    __tablename__ = ""
    attributes

# Service
- if helper: 
// FUNCTION NAME
def _FunctionName (params) -> data type: 
    validation input
    try{
        query
    }
    catch{
        error log
    }

- if actual service: 
//FUNCTION NAME
def FunctionName (params) -> data type:
    validation input
    try{
        query
    }
    catch{
        error log
    }

# Controller
//FUNCTION NAME
route
async def FunctionName (params):
    try{
        contact service function
        send their result here
    }
    catch{
        error log
    }

# Common Rule
1. backend error log must be displayed at cmd log (if possible) & network debug at website dev view 
