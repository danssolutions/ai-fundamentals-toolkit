from enums import States, Location, Action, LocationState

type LocationMap = dict[Location, States]


class EnvironmentClass:
    def __init__(self, current_location: Location, states: LocationMap):
        self.current_location = current_location
        self.states = states


base_environment = EnvironmentClass(
    current_location=Location.A,
    states={
        Location.A: States.DIRTY,
        Location.B: States.DIRTY
    }
)


class Agent:
    def __init__(self, environment: EnvironmentClass):
        self.environment = environment

    def sensor(self) -> LocationState:
        return self.environment.current_location, self.environment.states[self.environment.current_location]

    def actuator(self, action: Action) -> None:
        loc = self.environment.current_location
        if action == Action.SUCK:
            self.environment.states[loc] = States.CLEAN
        elif action == Action.RIGHT and action in loc.allowed_moves():
            self.environment.current_location = Location.B
        elif action == Action.LEFT and action in loc.allowed_moves():
            self.environment.current_location = Location.A

    def evaluate(self) -> Action:
        percept = self.sensor()
        action = self.choose_action(percept)
        self.actuator(action)
        return action

    @staticmethod
    def choose_action(state: LocationState) -> Action:
        # Decision is based only on current percept, no memory used
        if state[1] == States.DIRTY:
            return Action.SUCK
        if state[0] == Location.A:
            return Action.RIGHT
        if state[0] == Location.B:
            return Action.LEFT


def run(n) -> None:
    location_space = 10
    status_space = 8
    action_space = 7
    icon = "-> "

    agent = Agent(base_environment)

    print(f"{'Current':{location_space + status_space + action_space}s}{icon}{'New':8s}")
    print(f"{'location':{location_space}s}{'status':{status_space}s}{'action':{action_space}s}{icon}{'location':{location_space}s}{'status':{status_space}s}")

    for _ in range(n):
        loc, stat = agent.sensor()
        print(f"{loc.name:{location_space}s}{stat.name:{status_space}s}", end='')

        action = agent.evaluate()

        loc, stat = agent.sensor()
        print(f"{action.name:{action_space}s}{icon}{loc.name:{location_space}s}{stat.name:{status_space}s}")


if __name__ == '__main__':
    run(10)
