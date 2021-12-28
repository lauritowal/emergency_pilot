from gym_jsbsim.environments.environment import GuidanceEnvContinuos
import ray
from gym_jsbsim.wrappers.normalise_observation import NormalizeObservation
from ray.rllib.agents.ddpg import TD3Trainer, td3
from ray.tune import register_env
import datetime
import os
from ray import tune
from gym_jsbsim.aircraft import Aircraft, cessna172P

from gym_jsbsim.tests.CustomCallbacks import CustomCallbacks

def in_seconds(minutes: int) -> int:
    return minutes * 60

SEED = 7
CHECK_POINT_DIR = "./checkpoints"
JSBSIM_PATH = "../jsbsim"
ENVIRONMENT = "guidance-continuous-v0"

def env_creator(config=None):
    print("config", config)
    return GuidanceEnvContinuos(config)

current_episode = 0
def my_train_fn(config, reporter):
    agent = TD3Trainer(config=config, env=ENVIRONMENT)

    checkpoint_path = f'{CHECK_POINT_DIR}/checkpoint_6001/checkpoint-6001'
    # agent.restore(checkpoint_path)

    for i in range(5000):
        result = agent.train()
        if i % 100 == 0:
            checkpoint = agent.save(checkpoint_dir=f"{checkpoint_dir}/checkpoints")
            print("checkpoint saved at", checkpoint)
    agent.stop()


if __name__ == "__main__":
    ray.init()

    default_config = td3.TD3_DEFAULT_CONFIG.copy()
    # default_config.update({'seed': 3})
    custom_config = {
        "lr": 0.0001, # tune.grid_search([0.01, 0.001, 0.0001]),
        "framework": "torch",
        "callbacks": CustomCallbacks,
        "log_level": "WARN",
        "evaluation_interval": 20,
        "evaluation_num_episodes": 10,
        "num_gpus": 0,
        "num_workers": 1,
        "num_envs_per_worker": 3,
        "seed": SEED,
        "env_config": {
            "jsbsim_path": JSBSIM_PATH,
            "flightgear_path": "",
            "aircraft": cessna172P,
            "agent_interaction_freq": 5,
            "target_radius": 100 / 1000,
            "max_distance_km": 4,
            "max_target_distance_km": 2,
            "max_episode_time_s": 60 * 5,
            "phase": 0,
            "render_progress_image": False,
            "render_progress_image_path": './data',
            "offset": 0,
            "seed": SEED,
            "evaluation": False,
        },
        "evaluation_config": {
            "explore": False
        },
        "evaluation_num_workers": 1,
    }

    config = {**default_config, **custom_config}
    register_env(ENVIRONMENT, lambda config: env_creator(config))
    resources = TD3Trainer.default_resource_request(config).to_json()

    # start training
    now = datetime.datetime.now().strftime("date_%d-%m-%Y_time_%H-%M-%S")
    tune.run(my_train_fn,
             checkpoint_freq=100,
             checkpoint_at_end=True,
             reuse_actors=True,
             # resume=True,
             keep_checkpoints_num=5,
             # restore=f'{checkpoint_dir}/checkpoints/checkpoint_2101/checkpoint-2101',
             name=f"experiment_no_sincos_wind_4_{now}_seed_{SEED}",
             resources_per_trial=resources,
             config=config)