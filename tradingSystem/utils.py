from .models import StockInfo, StockComment, UserTable, HistoryTradeTable
from .models import News
from django.db.models import Sum


def get_top10():
    return StockInfo.objects.all().order_by('-change_extent')[:10]


def get_news():
    news_list = News.objects.all().order_by('-news_time')
    return news_list[:8]


def get_stock_comments(stock_id):
    stock = StockInfo.objects.get(stock_id=stock_id)
    return StockComment.objects.filter(stock_id=stock)


def get_buy_in_out(phone_number):
    user = UserTable.objects.get(phone_number=phone_number)
    buy_in_res = HistoryTradeTable.objects.filter(user_id=user, trade_shares__gte=0).aggregate(Sum('trade_shares'))
    sold_out_res = HistoryTradeTable.objects.filter(user_id=user, trade_shares__lte=0).aggregate(Sum('trade_shares'))
    return buy_in_res['trade_shares__sum'], -sold_out_res['trade_shares__sum']

