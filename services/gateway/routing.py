"""Gateway routing configuration placeholder."""


class RouteMap:
    # In a real implementation this would read from config and dynamically map paths
    routes = {}

    @classmethod
    def get_target(cls, path: str):
        return cls.routes.get(path)
