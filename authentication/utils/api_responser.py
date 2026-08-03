from rest_framework.response import Response
from rest_framework import status


class ApiResponseMixin:
    def success_response(
        self, data_title="data", data=None, message="Success", status_code=status.HTTP_200_OK
    ):
        return Response(
            {"success": True, "message": message, data_title: data, "errors": None},
            status=status_code,
        )

    def error_response(
        self, errors=None, message="Error", status_code=status.HTTP_400_BAD_REQUEST
    ):
        return Response(
            {"success": False, "message": message, "data": None, "errors": errors},
            status=status_code,
        )
