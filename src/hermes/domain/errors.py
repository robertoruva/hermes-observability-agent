class DashboardNotFound(Exception):
    def __init__(self, uid: str) -> None:
        super().__init__(f"Dashboard not found: {uid}")
        self.uid = uid
