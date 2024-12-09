from enum import Enum


class ApiEnv(str, Enum):
    IN_VEHICLE = 'in_vehicle'
    E2E = 'e2e'
    CLI = 'cli'
