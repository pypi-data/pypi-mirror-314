import dataclasses


@dataclasses.dataclass
class StatusInfoContents:
    current: str | None = None
    message: str | None = None

    @classmethod
    def from_dict(cls, d):
        self = cls()
        self.current = d.get('current')
        self.message = d.get('message')
        return self


@dataclasses.dataclass
class ApplicationStatus:
    application_status: StatusInfoContents = dataclasses.field(default_factory=StatusInfoContents)

    @classmethod
    def from_dict(cls, d):
        self = cls()
        self.application_status = StatusInfoContents.from_dict(d.get('application-status') or {})
        return self


@dataclasses.dataclass
class Status:
    # TODO: Ideally we can generate the list of fields from the Go source in Juju:
    # cmd/juju/status/formatted.go
    applications: dict[str, ApplicationStatus] = dataclasses.field(default_factory=dict)

    @classmethod
    def from_dict(cls, d):
        self = cls()
        applications = d.get('applications') or {}
        self.applications = {
            name: ApplicationStatus.from_dict(status) for name, status in applications.items()
        }
        return self

    # TODO: helper methods
