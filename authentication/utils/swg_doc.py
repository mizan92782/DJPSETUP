from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


def swagger_documentation(
    *,
    title: str,
    description: str,
    request_serializer=None,
    response_serializer=None,
    tags: list[str] | None = None,
    status_code: int = 200,
    method: str | None = None,
    many: bool = False,
    pagination: bool = False,
):
    """
    Advanced reusable swagger decorator
    Supports:
    - ViewSet default actions (list, retrieve, create, update, destroy)
    - @action methods
    - APIView methods
    - Pagination
    - Dynamic request & response serializers
    """

    # 🔹 Handle response schema
    response_schema = None

    if response_serializer:
        if many:
            response_schema = response_serializer(many=True)
        else:
            response_schema = response_serializer

    # 🔹 Pagination support (for list views)
    if pagination and response_serializer:
        response_schema = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "count": openapi.Schema(type=openapi.TYPE_INTEGER),
                "next": openapi.Schema(type=openapi.TYPE_STRING, format="uri", nullable=True),
                "previous": openapi.Schema(type=openapi.TYPE_STRING, format="uri", nullable=True),
                "results": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_OBJECT)
                ),
            },
        )

    # 🔹 Standard responses (Global reusable)
    responses = {
        status_code: openapi.Response(
            description="Success",
            schema=response_schema,
        ),
        400: openapi.Response(description="Bad Request / Validation Error"),
        401: openapi.Response(description="Unauthorized"),
        403: openapi.Response(description="Forbidden"),
        404: openapi.Response(description="Not Found"),
        500: openapi.Response(description="Internal Server Error"),
    }

    kwargs = {
        "operation_summary": title,
        "operation_description": description,
        "responses": responses,
        "tags": tags or [],
    }

    # 🔹 Auto detect write methods
    write_methods = ["post", "put", "patch"]

    if request_serializer:
        if method:
            if method.lower() in write_methods:
                kwargs["request_body"] = request_serializer
        else:
            # For ViewSet create/update automatically
            kwargs["request_body"] = request_serializer

    # 🔹 Add method for @action support
    if method:
        kwargs["method"] = method.lower()

    return swagger_auto_schema(**kwargs)

