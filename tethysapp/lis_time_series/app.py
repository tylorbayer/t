from tethys_sdk.base import TethysAppBase, url_map_maker


class LisTimeSeries(TethysAppBase):
    """
    Tethys app class for Lis Time Series.
    """

    name = 'Lis Time Series'
    index = 'lis_time_series:home'
    icon = 'lis_time_series/images/icon.gif'
    package = 'lis_time_series'
    root_url = 'lis-time-series'
    color = '#c0392b'
    description = 'Place a brief description of your app here.'
    tags = ''
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='lis-time-series',
                controller='lis_time_series.controllers.home'
            ),
            UrlMap(
                name='forecast',
                url='lis-time-series/forecast',
                controller='lis_time_series.controllers.forecast'
            )
        )

        return url_maps
