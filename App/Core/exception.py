from fastapi import exceptions,status
from fastapi.responses import JSONResponse
def NotFoundId(exception: exceptions.HTTPException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content='Không tìm thấy id'
    )
def WrongtypeData(exception:exceptions.HTTPException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content = 'Nhập sai kiểu dữ liệu'
    )
def NotAuthorized(exception:exceptions.HTTPException):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content='Bạn không có quyền thực hiện hành động này'
    )