from rest_framework.pagination import PageNumberPagination as __PageNumberPagination


class PageNumberPagination(__PageNumberPagination):
    page_size = 3  # 每页数据条目数
    page_query_param = 'page'  # url中page关键字
    page_query_description = "获取的页码"  # 分页描述
    page_size_query_param = "size"  # url中page_size关键字
    page_size_query_param_description = "每页数据条目数"  # url中page_size描述
    max_page_size = 50  # 最大分页条目数
    invalid_page_message = "无效的页码"
