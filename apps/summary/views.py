from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from django.contrib.auth.models import User
from rest_framework import permissions

from projects.models import ProjectsModel
from interfaces.models import InterfacesModel
from testcases.models import TestcasesModel
from testsuites.models import TestsuitsModel
from configures.models import ConfiguresModel
from envs.models import EnvsModel
from debugtalks.models import DebugTalksModel
from reports.models import ReportsModel
from users.serializers import UserInforModelSeralizer


class SummaryView(APIView):
    # 鉴权方式
    permission_classes = [permissions.IsAuthenticated]

    def get(self, ruquest, *args, **kwargs):
        # user
        instance = User.objects.get(username=ruquest.user.username)
        userseralizer = UserInforModelSeralizer(instance=instance)
        user = userseralizer.data
        # statistics
        projects_count = ProjectsModel.objects.all().count()
        interfaces_count = InterfacesModel.objects.all().count()
        testcases_count = TestcasesModel.objects.all().count()
        testsuits_count = TestsuitsModel.objects.all().count()
        configures_count = ConfiguresModel.objects.all().count()
        envs_count = EnvsModel.objects.all().count()
        debug_talks_count = DebugTalksModel.objects.all().count()
        reports_count = ReportsModel.objects.all().count()
        reports_case_sum = ReportsModel.objects.all().aggregate(
            Sum("count"))["count__sum"]
        if reports_case_sum:
            reports_success_sum = ReportsModel.objects.all().aggregate(
                Sum("success"))["success__sum"]
            success_rate = round(
                (reports_success_sum / reports_case_sum), 2) * 100
            fail_rate = 100 - success_rate
        else:
            success_rate = 0
            fail_rate = 0

        res = {
            "user": user,
            "statistics": {
                "projects_count": projects_count,
                "interfaces_count": interfaces_count,
                "testcases_count": testcases_count,
                "testsuits_count": testsuits_count,
                "configures_count": configures_count,
                "envs_count": envs_count,
                "debug_talks_count": debug_talks_count,
                "reports_count": reports_count,
                "success_rate": success_rate,
                "fail_rate": fail_rate
            }
        }
        return Response(res)
