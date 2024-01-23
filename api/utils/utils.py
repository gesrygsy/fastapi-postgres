from fastapi import Query


username_query = Query(min_length=4, max_length=50)
password_query = Query(min_length=5, max_length=100)
function_query = Query(min_length=3, max_length=100)
