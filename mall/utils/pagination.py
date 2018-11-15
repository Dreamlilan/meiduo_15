from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    # 每页显示几条数据
    page_size = 2
    # 分页查询参数
    page_size_query_param = 'page_size'
    # 每页最多显示数据
    max_page_size = 20