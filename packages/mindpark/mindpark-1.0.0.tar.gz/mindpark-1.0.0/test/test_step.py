import pytest
import mindpark.step
from mindpark.core import Sequential
from test.mocks import Random
from test.fixtures import *


STEPS = [
    'Identity', 'Maximum', 'Delta', 'Grayscale', 'Subsample', 'Skip',
    'History', 'Normalize', 'ClampReward', 'EpsilonGreedy', 'RandomStart',
    'ActionSample', 'ActionMax', 'Score', 'Image']


@pytest.fixture(params=STEPS)
def step(request):
    return getattr(mindpark.step, request.param)


@pytest.fixture
def policy(task, step):
    policy = Sequential(task)
    print('Step:  ', step.__name__)
    print('Input: ', policy.task.observs)
    policy.add(step)
    print('Output:', policy.task.actions)
    policy.add(Random)
    return policy


class TestStep:

    def test_no_error(self, env, policy):
        observ = env.reset()
        policy.begin_episode(0, True)
        while observ is not None:
            action = policy.observe(observ)
            reward, observ = env.step(action)
            policy.receive(reward, observ is None)
        policy.end_episode()
