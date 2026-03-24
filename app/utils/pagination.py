from django.utils.safestring import mark_safe

class Pagination(object):
    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        page = request.GET.get(page_param, "1")

        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start : self.end]

        total_count = len(queryset)
        total_page_count, div = divmod(total_count, page_size)

        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        # 计算出,显示当前页的前5页和后5页
        if self.total_page_count <= 2 * self.plus + 1:
            # 当queryset中的数据量较少，不足11页数据，无法显示全部页码
            start_page = 1
            end_page = self.total_page_count
        else:
            #数据量足够多，可以显示11页及以上
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 页码
        page_str_list = []

        page_str_list.append('<li><a href="?search_value={{ search_value }}&page={}">首页</a></li>'.format(1))

        #上一页
        if self.page > 1:
            prev = '<li><a href="?search_value={{ search_value }}&page={}">上一页</a></li>'.format(self.page - 1)
        else:
            prev = '<li><a href="?search_value={{ search_value }}&page={}">上一页</a></li>'.format(1)
        page_str_list.append(prev)

        #页面
        for i in range(start_page, end_page + 1):
            if i == self.page:
                ele = '<li class="active"><a href="?search_value={{ search_value }}&page={}">{}</a></li>'.format(i, i)
            else:
                ele = '<li><a href="?search_value={{ search_value }}&page={}">{}</a></li>'.format(i, i)
            page_str_list.append(ele)

        #下一页
        if self.page < self.total_page_count:
            prev = '<li><a href="?search_value={{ search_value }}&page={}">下一页</a></li>'.format(self.page + 1)
        else:
            prev = '<li><a href="?search_value={{ search_value }}&page={}">下一页</a></li>'.format(self.total_page_count)
        page_str_list.append(prev)

        #尾页
        page_str_list.append('<li><a href="?search_value={{ search_value }}&page={}">尾页</a></li>'.format(self.total_page_count))

        search_string = """
            <li>
                <form style="float: left;margin-left: -1px" method="get">
                    <input name="page"
                        style="position: relative;float:left;display:inline-block;width: 80px"
                           type="text" class="form-control" placeholder="页码">
                    <button style="border-radius: 0" class="btn btn-primary" type="submit">跳转</button>
                </form>
            </li>
        """

        page_str_list.append(search_string)

        page_string = mark_safe("".join(page_str_list))

        return page_string