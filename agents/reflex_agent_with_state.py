from enums_extended import Location, States, Action, LocationState
from typing import Dict

type LocationMap = Dict[Location, States]


class EnvironmentClass:
    def __init__(self, current_location: Location, states: LocationMap):
        self.current_location = current_location
        self.states = states


# Agent starts at A; all squares begin dirty
base_environment = EnvironmentClass(
    current_location=Location.A,
    states={
        Location.A: States.DIRTY,
        Location.B: States.DIRTY,
        Location.C: States.DIRTY,
        Location.D: States.DIRTY,
    }
)


class StatefulReflexAgent:
    def __init__(self):
        self.model: LocationMap = {
            Location.A: States.UNKNOWN,
            Location.B: States.UNKNOWN,
            Location.C: States.UNKNOWN,
            Location.D: States.UNKNOWN,
        }
        self.state: LocationState = (Location.UNKNOWN, States.UNKNOWN)

    def match_rule(self) -> Action:
        loc, status = self.state

        if status == States.DIRTY:
            return Action.SUCK

        if all(val == States.CLEAN for val in self.model.values()):
            return Action.NO_OP

        # Movement based on square layout:
        if loc == Location.A:
            return Action.RIGHT
        if loc == Location.B:
            return Action.DOWN
        if loc == Location.C:
            return Action.LEFT
        if loc == Location.D:
            return Action.UP

        return Action.NO_OP

    def update_state(self, percept: LocationState) -> None:
        location, status = percept
        self.model[location] = status  # Track what was seen

    def sensors(self, environment: EnvironmentClass) -> LocationState:
        return environment.current_location, environment.states[environment.current_location]

    def actuators(self, action: Action, environment: EnvironmentClass) -> None:
        loc = environment.current_location

        if action not in loc.allowed_moves():
            return

        if action == Action.SUCK:
            environment.states[loc] = States.CLEAN
        elif action == Action.RIGHT:
            environment.current_location = Location.B
        elif action == Action.DOWN:
            environment.current_location = Location.C
        elif action == Action.LEFT:
            environment.current_location = Location.D
        elif action == Action.UP:
            environment.current_location = Location.A

    def act(self, environment: EnvironmentClass) -> Action:
        percept = self.sensors(environment)
        self.state = percept
        self.update_state(percept)
        action = self.match_rule()
        self.actuators(action, environment)
        return action


def run(n: int = 20) -> None:
    location_space = 10
    status_space = 8
    action_space = 7
    icon = "-> "

    agent = StatefulReflexAgent()

    print(f"{'Current':{location_space + status_space + action_space}s}{icon}{'New':8s}")
    print(f"{'location':{location_space}s}{'status':{status_space}s}{'action':{action_space}s}{icon}{'location':{location_space}s}{'status':{status_space}s}")

    for _ in range(n):
        loc, stat = agent.sensors(base_environment)
        print(f"{loc.name:{location_space}s}{stat.name:{status_space}s}", end='')

        action = agent.act(base_environment)

        loc, stat = agent.sensors(base_environment)
        print(f"{action.name:{action_space}s}{icon}{loc.name:{location_space}s}{stat.name:{status_space}s}")


if __name__ == '__main__':
    run(20)
