from dataclasses import dataclass
import datetime


@dataclass
class BaseStructure:
    title: str

    @dataclass
    class OwnerStructure:
        name: str
        dob: datetime.datetime

    owner: OwnerStructure

    @dataclass
    class DatabaseStructure:
        enabled: bool
        ports: list[int]
        data: list[list[str | float]]
        temp_targets: dict[str, float]

    database: DatabaseStructure

    @dataclass
    class ServerStructure:
        ip: str
        role: str

    servers: dict[str, ServerStructure]


EXAMPLE_TOML = """
# This is a TOML document

title = "TOML Example"

[owner]
name = "Tom Preston-Werner"
dob = 1979-05-27T07:32:00-08:00

[database]
enabled = true
ports = [ 8000, 8001, 8002 ]
data = [ ["delta", "phi"], [3.14] ]
temp_targets = { cpu = 79.5, case = 72.0 }

[servers]

[servers.alpha]
ip = "10.0.0.1"
role = "frontend"

[servers.beta]
ip = "10.0.0.2"
role = "backend"
"""


def test_example():
    import tattl
    import tomllib

    data = tattl.unpack(tomllib.loads(EXAMPLE_TOML), BaseStructure)
    print(data)
    assert data == BaseStructure(
        title="TOML Example",
        owner=BaseStructure.OwnerStructure(
            name="Tom Preston-Werner",
            dob=datetime.datetime(
                1979,
                5,
                27,
                7,
                32,
                tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=57600)),
            ),
        ),
        database=BaseStructure.DatabaseStructure(
            enabled=True,
            ports=[8000, 8001, 8002],
            data=[["delta", "phi"], [3.14]],
            temp_targets={"cpu": 79.5, "case": 72.0},
        ),
        servers={
            "alpha": BaseStructure.ServerStructure(ip="10.0.0.1", role="frontend"),
            "beta": BaseStructure.ServerStructure(ip="10.0.0.2", role="backend"),
        },
    )
