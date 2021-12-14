import ray
from ray.rllib.agents.ddpg import TD3Trainer, td3
from ray.tune import register_env
import datetime
from ray import tune

from guidance_flight_env.aircraft import cessna172P
from guidance_flight_env.examples.rllib.rllib_wrapper_env import RllibWrapperEnv

from utils.custom_callbacks import CustomCallbacks

SEED = 1
CHECK_POINT_DIR = "./checkpoints"
JSBSIM_PATH = "../jsbsim"
ENVIRONMENT = "guidance-env-no-wind-v0"

def env_creator(config=None):
    print("config", config)
    return RllibWrapperEnv(config)


def train(config, reporter):
    agent = TD3Trainer(config=config, env=ENVIRONMENT)

    # Uncomment the following two lines and select checkpoint for restoring agent
    # checkpoint_path = f'{CHECK_POINT_DIR}/checkpoint_6001/checkpoint-6001'
    # agent.restore(checkpoint_path)

    for i in range(50000):
        agent.train()
        if i % 100 == 0:
            checkpoint = agent.save(checkpoint_dir=CHECK_POINT_DIR)
            print("checkpoint saved at", checkpoint)
    agent.stop()


if __name__ == "__main__":
    ray.init(ignore_reinit_error=True)

    default_config = td3.TD3_DEFAULT_CONFIG.copy()
    custom_config = {
        "lr": 0.0001, # tune.grid_search([0.01, 0.001, 0.0001]),
        "framework": "torch",
        "callbacks": CustomCallbacks,
        "log_level": "WARN",
        "evaluation_interval": 20,
        "evaluation_num_episodes": 10,
        "num_gpus": 0,
        "num_workers": 10,
        "num_envs_per_worker": 2,
        "seed": SEED,
        "env_config": {
            "jsbsim_path": JSBSIM_PATH,
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
    tune.run(train,
             checkpoint_freq=100,
             checkpoint_at_end=True,
             reuse_actors=True,
             keep_checkpoints_num=5,
             name=f"experiment_{now}_seed_{SEED}",
             resources_per_trial=resources,
             config=config)