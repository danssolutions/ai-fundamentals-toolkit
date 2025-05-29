from variable import Variable
from bn import BayesianNetwork


def car_diagnosis():
    # Define variables

    Battery = Variable("Battery", ("working", "dead"), {
        (): (0.9, 0.1)
    })

    Ignition = Variable("Ignition", ("on", "off"), {
        ("working",): (0.95, 0.05),
        ("dead",): (0.1, 0.9)
    }, parents=[Battery])

    StarterMotor = Variable("StarterMotor", ("working", "dead"), {
        (): (0.85, 0.15)
    })

    Fuel = Variable("Fuel", ("full", "empty"), {
        (): (0.8, 0.2)
    })

    Noise = Variable("Noise", ("heard", "not heard"), {
        ("on", "working"): (0.9, 0.1),
        ("on", "dead"): (0.1, 0.9),
        ("off", "working"): (0.2, 0.8),
        ("off", "dead"): (0.05, 0.95)
    }, parents=[Ignition, StarterMotor])

    Vibration = Variable("Vibration", ("felt", "not felt"), {
        ("on",): (0.95, 0.05),
        ("off",): (0.1, 0.9)
    }, parents=[Ignition])

    Speed = Variable("Speed", ("moving", "not moving"), {
        ("on", "full"): (0.9, 0.1),
        ("on", "empty"): (0.2, 0.8),
        ("off", "full"): (0.05, 0.95),
        ("off", "empty"): (0.01, 0.99)
    }, parents=[Ignition, Fuel])

    # Set children (optional if not used directly)
    Battery.add_child(Ignition)
    Ignition.add_child(Noise)
    Ignition.add_child(Vibration)
    Ignition.add_child(Speed)
    StarterMotor.add_child(Noise)
    Fuel.add_child(Speed)

    # Build network
    bn = BayesianNetwork()
    for var in [Battery, Ignition, StarterMotor, Fuel, Noise, Vibration, Speed]:
        bn.add_variable(var)

    # Calculate marginals
    bn.calculate_marginal_probabilities()
    print("\nMarginal probabilities:")
    for var in bn.get_variables():
        print(f"  {var.name}")
        for assignment in var.assignments:
            prob = var.get_marginal_probability(assignment)
            print(f"    {assignment}: {prob:.4f}")

    # Run sample joint and conditional queries
    print("\nJoint probability of:")
    joint_event = {
        "Battery": "working",
        "Ignition": "on",
        "StarterMotor": "working",
        "Fuel": "full",
        "Noise": "heard",
        "Vibration": "felt",
        "Speed": "moving"
    }
    jp = bn.get_joint_probability(joint_event)
    print(f"  {joint_event}")
    print(f"  -> {jp:.6f}")

    print("\nConditional probability:")
    query = {"Battery": "working"}
    evidence = {"Noise": "not heard"}
    cp = bn.get_conditional_probability(query, evidence)
    print(f"  P({query} | {evidence}) = {cp:.6f}")


if __name__ == "__main__":
    car_diagnosis()
