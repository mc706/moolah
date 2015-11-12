from datetime import timedelta

from rest_framework import views, response
from dateutil.relativedelta import relativedelta, MO

from tracking.models import Rate, Transaction
from moolah.utils import get_timestamp


class SummaryView(views.APIView):
    def get(self, request):
        t = Transaction.objects

        data = {'rate': Rate.objects.total(),
                'day': t.today().total(),
                'week': t.last_week().total(),
                'month': t.last_month().total(),
                'year': t.last_year().total()}

        return response.Response(data)


class DailyTransactionReportView(views.APIView):
    def _get_week_dates(self, weeks=-1):
        today = get_timestamp()
        monday = today + relativedelta(weekday=MO(weeks))
        return [monday + timedelta(days=n)
                for n in range(7)]

    def get(self, request):
        t = Transaction.objects
        labels = ['Monday',
                  'Tuesday',
                  'Wednesday',
                  'Thursday',
                  'Friday',
                  'Saturday',
                  'Sunday']

        this_week = [t.date(d).total()
                     for d in self._get_week_dates()]

        last_week = [t.date(d).total()
                     for d in self._get_week_dates(-2)]

        return response.Response({'labels': labels,
                                  'data': [this_week,
                                           last_week],
                                  'series': ['This Week', 'Last Week']})


class YearlySavingReflectionReportView(views.APIView):
    def get(self, request):
        hundo_days_ago = get_timestamp() + timedelta(days=-20)
        dates = [hundo_days_ago + timedelta(days=n) for n in range(100)]
        data = [Transaction.objects.date(d).total() for d in dates]
        labels = [str(n) for n in range(100, -1, -1)]
        return response.Response({'labels': labels,
                                  'data': [data],
                                  'series': []})
