def paginate(query, page = 1, limit =  2):
    offset = (page - 1) * limit

    total = query.count()

    data = query.offset(offset).limit(limit).all()

    return {
        "data": data,
        "page": page,
        "limit": limit,
        "total": total
    }