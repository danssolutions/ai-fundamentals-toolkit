import numpy as np


def normalize(vector):
    total = sum(vector)
    if total == 0:
        return vector
    return [v / total for v in vector]


def compute_forward(states, start_probability, transition_probability, emission_probability, observations):
    """ Returns the probability of the observation sequence given the model. """
    forward = [{} for _ in range(len(observations))]

    # Initialization
    for state in states:
        forward[0][state] = start_probability[state] * \
            emission_probability[state][observations[0]]

    # Recursion
    for t in range(1, len(observations)):
        for state in states:
            forward[t][state] = sum(
                forward[t - 1][prev_state] *
                transition_probability[prev_state][state] *
                emission_probability[state][observations[t]]
                for prev_state in states
            )

    # Termination
    return sum(forward[-1][state] for state in states)


def compute_viterbi(states, start_probability, transition_probability, emission_probability, observations):
    """ Returns the most probable state path for the observation sequence. """
    viterbi = [{} for _ in range(len(observations))]
    path = {}

    # Initialization
    for state in states:
        viterbi[0][state] = start_probability[state] * \
            emission_probability[state][observations[0]]
        path[state] = [state]

    # Recursion
    for t in range(1, len(observations)):
        new_path = {}
        for state in states:
            (prob, prev_state) = max(
                (viterbi[t - 1][ps] * transition_probability[ps][state] *
                 emission_probability[state][observations[t]], ps)
                for ps in states
            )
            viterbi[t][state] = prob
            new_path[state] = path[prev_state] + [state]
        path = new_path

    # Termination
    n = len(observations) - 1
    (prob, state) = max((viterbi[n][s], s) for s in states)
    return path[state], prob


def run_example():
    states = ['HOT', 'COLD']
    start_p = {'HOT': 0.8, 'COLD': 0.2}
    trans_p = {
        'HOT': {'HOT': 0.7, 'COLD': 0.3},
        'COLD': {'HOT': 0.4, 'COLD': 0.6}
    }
    emit_p = {
        'HOT': {1: 0.2, 2: 0.4, 3: 0.4},
        'COLD': {1: 0.5, 2: 0.4, 3: 0.1}
    }

    obs_seq = [3, 1, 3]

    print("Forward Probability for [3, 1, 3]:")
    forward_prob = compute_forward(states, start_p, trans_p, emit_p, obs_seq)
    print(f"  P(O) = {forward_prob:.6f}")

    print("\nViterbi Path and Probability for [3, 1, 3]:")
    path, prob = compute_viterbi(states, start_p, trans_p, emit_p, obs_seq)
    print(f"  Path = {path}")
    print(f"  P* = {prob:.6f}")

    # Longer sequences
    test_seqs = [
        [3, 3, 1, 1, 2, 2, 3, 1, 3],
        [3, 3, 1, 1, 2, 3, 3, 1, 2]
    ]
    for i, seq in enumerate(test_seqs, start=1):
        print(f"\nSequence {i}: {seq}")
        p = compute_forward(states, start_p, trans_p, emit_p, seq)
        path, vprob = compute_viterbi(states, start_p, trans_p, emit_p, seq)
        print(f"  Forward P(O): {p:.6f}")
        print(f"  Viterbi Path: {path}")
        print(f"  Viterbi P*: {vprob:.6f}")


if __name__ == "__main__":
    run_example()
