from DragonAggregator.connector.Generic import GenericConnector


class SonarQubeConnector(GenericConnector):
    def __init__(self, *args, **kwargs):
        kwargs.update({
            "file_based": False
        })

        super().__init__(*args, **kwargs)

    def pull_raw_vulnerability_data(self):
        pass

    @classmethod
    def parse_vulnerability_data(cls, raw_data):
        pass
