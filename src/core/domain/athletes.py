from dataclasses import dataclass, asdict, field


@dataclass
class Athlete:
    name: str = field(default="not-found")
    title: str = field(default="not-found")
    location: str = field(default="not-found")
    avatar_url: str = field(default="not-found")

    def dict(self) -> dict[str]:
        return {k: str(v) for k, v in asdict(self).items()}
