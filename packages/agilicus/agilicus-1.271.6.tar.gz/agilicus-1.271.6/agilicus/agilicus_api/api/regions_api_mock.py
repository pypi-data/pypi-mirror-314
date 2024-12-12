from unittest.mock import MagicMock

class RegionsApiMock:

    def __init__(self):
        self.mock_add_point_of_presence = MagicMock()
        self.mock_delete_point_of_presence = MagicMock()
        self.mock_get_point_of_presence = MagicMock()
        self.mock_list_point_of_presences = MagicMock()
        self.mock_replace_point_of_presence = MagicMock()

    def add_point_of_presence(self, *args, **kwargs):
        """
        This method mocks the original api RegionsApi.add_point_of_presence with MagicMock.
        """
        return self.mock_add_point_of_presence(self, *args, **kwargs)

    def delete_point_of_presence(self, *args, **kwargs):
        """
        This method mocks the original api RegionsApi.delete_point_of_presence with MagicMock.
        """
        return self.mock_delete_point_of_presence(self, *args, **kwargs)

    def get_point_of_presence(self, *args, **kwargs):
        """
        This method mocks the original api RegionsApi.get_point_of_presence with MagicMock.
        """
        return self.mock_get_point_of_presence(self, *args, **kwargs)

    def list_point_of_presences(self, *args, **kwargs):
        """
        This method mocks the original api RegionsApi.list_point_of_presences with MagicMock.
        """
        return self.mock_list_point_of_presences(self, *args, **kwargs)

    def replace_point_of_presence(self, *args, **kwargs):
        """
        This method mocks the original api RegionsApi.replace_point_of_presence with MagicMock.
        """
        return self.mock_replace_point_of_presence(self, *args, **kwargs)

