from sherlock.sherlock_data.persistence import Log2DB

def getFunctionCalls(db):
    db = Log2DB.instance()
    cursor =  db.getCursor()

    query = f"""
        select * from function_call
        join function on 
        function_call.hash_id = function.hash_id
        where function_call.session_id = {db.getSession()[0]};
    """
    sql = "select * from function_call"
    cursor = db.getCursor()
    for row in cursor.execute(sql):
        print(row)
    breakpoint()