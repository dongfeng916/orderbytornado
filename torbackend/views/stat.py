from common.libs.helper import getFormatDate,getDictFilterField,selectFilterObj
from models.stat import StatDailyMember,StatDailyFood,StatDailySite
from models.member import Member
from models.food import Food
import datetime
from views.auth import Auth
from tornado.web import RequestHandler
from models import session

class StatIndexHandler(Auth,RequestHandler):
    def get(self, *args, **kwargs):
        now = datetime.datetime.now()
        date_before_30days = now + datetime.timedelta(days=-30)
        default_date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
        default_date_to = getFormatDate(date=now, format="%Y-%m-%d")

        resp_data = {}
        date_from = self.get_argument('date_from',default_date_from)
        date_to = self.get_argument('date_to',default_date_to)
        query = session.query(StatDailySite).filter(StatDailySite.date >= date_from) \
            .filter(StatDailySite.date <= date_to)

        list = query.order_by(StatDailySite.id.desc()).limit(100).all()
        resp_data['list'] = list
        resp_data['current'] = 'index'
        resp_data['search_con'] = {
            'date_from': date_from,
            'date_to': date_to
        }
        self.render("stat/index.html", **resp_data)

class StatFoodHandler(Auth,RequestHandler):
    def get(self, *args, **kwargs):
        now = datetime.datetime.now()
        date_before_30days = now + datetime.timedelta(days=-30)
        default_date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
        default_date_to = getFormatDate(date=now, format="%Y-%m-%d")

        resp_data = {}
        date_from = self.get_argument('date_from',default_date_from)
        date_to = self.get_argument('date_to',default_date_to)
        query = session.query(StatDailyFood).filter(StatDailyFood.date >= date_from) \
            .filter(StatDailyFood.date <= date_to)
        list = query.order_by(StatDailyFood.id.desc()).limit(100).all()
        date_list = []
        if list:
            food_map = getDictFilterField(Food, Food.id, "id", selectFilterObj(list, "food_id"))
            for item in list:
                tmp_food_info = food_map[item.food_id] if item.food_id in food_map else {}
                tmp_data = {
                    "date": item.date,
                    "total_count": item.total_count,
                    "total_pay_money": item.total_pay_money,
                    'food_info': tmp_food_info
                }
                date_list.append(tmp_data)

        resp_data['list'] = date_list
        resp_data['current'] = 'food'
        resp_data['search_con'] = {
            'date_from': date_from,
            'date_to': date_to
        }
        self.render("stat/food.html", **resp_data)

class StatMemberHandler(Auth,RequestHandler):
    def get(self, *args, **kwargs):
        now = datetime.datetime.now()
        date_before_30days = now + datetime.timedelta(days=-30)
        default_date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
        default_date_to = getFormatDate(date=now, format="%Y-%m-%d")

        resp_data = {}
        date_from = self.get_argument('date_from', default_date_from)
        date_to = self.get_argument('date_to',default_date_to)
        query = session.query(StatDailyMember).filter(StatDailyMember.date >= date_from) \
            .filter(StatDailyMember.date <= date_to)
        list = query.order_by(StatDailyMember.id.desc()).limit(100).all()
        date_list = []
        if list:
            member_map = getDictFilterField(Member, Member.id, "id", selectFilterObj(list, "member_id"))
            for item in list:
                tmp_member_info = member_map[item.member_id] if item.member_id in member_map else {}
                tmp_data = {
                    "date": item.date,
                    "total_pay_money": item.total_pay_money,
                    "total_shared_count": item.total_shared_count,
                    'member_info': tmp_member_info
                }
                date_list.append(tmp_data)

        resp_data['list'] = date_list
        resp_data['current'] = 'member'
        resp_data['search_con'] = {
            'date_from': date_from,
            'date_to': date_to
        }
        self.render("stat/member.html", **resp_data)

class StatShareHandler(RequestHandler):
    def get(self, *args, **kwargs):
        now = datetime.datetime.now()
        date_before_30days = now + datetime.timedelta(days=-30)
        default_date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
        default_date_to = getFormatDate(date=now, format="%Y-%m-%d")
        resp_data = {}
        date_from = self.get_argument('date_from', default_date_from)
        date_to = self.get_argument('date_to', default_date_to)
        query = session.query(StatDailySite).filter(StatDailySite.date >= date_from) \
            .filter(StatDailySite.date <= date_to)

        list = query.order_by(StatDailySite.id.desc()).limit(100).all()
        resp_data['list'] = list
        resp_data['current'] = 'share'
        resp_data['search_con'] = {
            'date_from': date_from,
            'date_to': date_to
        }
        self.render("stat/share.html", **resp_data)
