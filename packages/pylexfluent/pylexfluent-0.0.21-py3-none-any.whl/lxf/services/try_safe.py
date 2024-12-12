import asyncio
import logging
async def try_safe_execute_async(logger:logging.Logger,func,**kargs) :
    try:
        result= await func(**kargs)
        return result
    except Exception as ex:
        #logger.exception(f"Exception occured in {func} with kargs={kargs}: {ex} ")
        logger.exception(f"Exception occured in {func} : {ex} ")
        return None

def try_safe_execute(logger,func,**kargs) :
    try:
        result= func(**kargs)
        return result
    except Exception as ex:
        logger.exception(f"Exception occured in {func} with kargs={kargs}: {ex} ")
        return None
    
def try_safe_execute_asyncio(logger,func,**kargs) :
    try:

        result= asyncio.run(func(**kargs))

        return result
    except Exception as ex:
        logger.exception(f"Exception occured in {func} with kargs={kargs}: {ex} ")
        return None