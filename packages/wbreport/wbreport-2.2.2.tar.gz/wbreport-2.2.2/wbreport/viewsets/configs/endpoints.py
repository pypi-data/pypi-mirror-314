from rest_framework.reverse import reverse
from wbcore.metadata.configs.endpoints import EndpointViewConfig


class ReportVersionEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return None

    def get_list_endpoint(self, **kwargs):
        return reverse("wbreport:reportversion-list", request=self.request)

    def get_instance_endpoint(self):
        return self.get_list_endpoint()


class ReportEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return reverse("wbreport:report-list", request=self.request)


class ReportVersionReportEndpointConfig(EndpointViewConfig):
    def get_list_endpoint(self, **kwargs):
        return reverse("wbreport:report-version-list", args=[self.view.kwargs["report_id"]], request=self.request)
