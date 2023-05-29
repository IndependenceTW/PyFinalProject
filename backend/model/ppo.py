import torch
import numpy as np
from torch import nn
from torch import Tensor
from torch.autograd import Variable
from copy import deepcopy


def neglogp(x: Tensor, mean: Tensor, logstd: Tensor):
    return 0.5 * (((x - mean) / torch.exp(logstd)) ** 2).sum(dim=-1) \
        + 0.5 * np.log(2.0 * np.pi) * x.size()[-1] \
        + logstd.sum(dim=-1)


class Actor(nn.Module):
    def __init__(self, num_obs, num_act):
        super().__init__()
        self.mu = nn.Sequential(
            nn.Linear(num_obs, 1024),
            nn.ReLU(),
            nn.Linear(1024, 1024),
            nn.ReLU(),
            nn.Linear(1024, num_act),
        )
        self.logstd = Variable(torch.zeros([num_act]), requires_grad=True)

    def __call__(self, obs):
        return self.mu(obs), self.logstd


class Critic(nn.Module):
    def __init__(self, num_obs):
        super().__init__()
        self.mlp = nn.Sequential(
            nn.Linear(num_obs, 1024),
            nn.ReLU(),
            nn.Linear(1024, 1024),
            nn.ReLU(),
            nn.Linear(1024, 1),
        )

    def __call__(self, obs):
        return self.mlp(obs).squeeze(-1)


class AsyncExperienceBuffer:
    def __init__(self, size, num_obs, num_actions):
        self.size = size
        self.num_actions = num_actions
        self.num_obs = num_obs
        self.tensor_dict = {}
        self.create_buffer()
        self.run_idx = {}

    def get(self, env_ids, key):
        idx = torch.Tensor([self.run_idx[i] for i in env_ids]).to(dtype=torch.long)
        return self.tensor_dict[key][idx]

    def create_buffer(self):
        size = self.size * 2
        self.status = torch.zeros([size], dtype=torch.long)
        self.tensor_dict['obs'] = torch.zeros([size, self.num_obs])
        self.tensor_dict['actions'] = torch.zeros([size, self.num_actions])
        self.tensor_dict['rewards'] = torch.zeros(size)
        self.tensor_dict['log_probs'] = torch.zeros([size])
        self.tensor_dict['next_obs'] = torch.zeros([size, self.num_obs])

    def pre_update_data(self, env_ids, datas: dict):
        idx = (self.status == 0).nonzero().squeeze(-1)[:len(env_ids)]
        for i, v in zip(env_ids, idx.tolist()):
            self.run_idx[i] = v
        for k, v in datas.items():
            self.tensor_dict[k][idx] = v
        self.status[idx] = -1

    def post_update_data(self, env_ids, datas: dict):
        idx = torch.Tensor([self.run_idx.pop(i) for i in env_ids]).to(dtype=torch.long)
        for k, v in datas.items():
            self.tensor_dict[k][idx] = v
        self.status[self.status > 0] += 1
        self.status[idx] = 1

    def full(self):
        return torch.sum(self.status > 0) >= self.size

    def get_data(self):
        if not self.full():
            raise
        idx = self.status.topk(self.size, sorted=False)[1]
        data = {k: v[idx] for k, v in self.tensor_dict.items()}
        self.status[idx] = 0
        return data


class PPO(nn.Module):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.obs_size = input_size
        self.action_size = output_size

        self.lr = 3e-4
        self.tau = 0.95
        self.gamma = 0.95
        self.clip = 0.2
        self.batch_size = 1024

        self.num_epochs = 0

        self.actor = Actor(self.obs_size, self.action_size)
        self.critic = Critic(self.obs_size)
        self.actor_optim = torch.optim.AdamW(self.actor.parameters(), lr=self.lr)
        self.critic_optim = torch.optim.AdamW(self.critic.parameters(), lr=self.lr)

        self.dataset = AsyncExperienceBuffer(self.batch_size, self.obs_size, self.action_size)

    @torch.no_grad()
    def get_action(self, env_ids, obs):
        mean, logstd = self.actor(obs)
        dist = torch.distributions.Normal(mean, logstd.exp())
        actions = dist.sample()
        log_probs = neglogp(actions, mean, logstd)

        datas = dict(obs=obs, actions=actions, log_probs=log_probs)
        self.dataset.pre_update_data(env_ids, datas)
        return torch.softmax(actions, dim=-1)

    def update_post_datas(self, env_ids, next_obs, choice):
        actions = self.dataset.get(env_ids, 'actions')
        prob = torch.softmax(actions, dim=-1)
        rewards = prob[torch.arange(len(env_ids)), choice]
        self.dataset.post_update_data(env_ids, {'rewards': rewards, 'next_obs': next_obs})
        if self.dataset.full():
            self._train_epoch()

    def train(self, mode=True):
        super().train(mode)
        self.actor.train(mode)
        self.critic.train(mode)

    def eval(self):
        super().eval()
        self.actor.eval()
        self.critic.eval()

    def _train_epoch(self):
        self.num_epochs += 1
        self.train()

        datas = self.dataset.get_data()
        obs = datas['obs']
        actions = datas['actions']
        rewards = datas['rewards']
        next_obs = datas['next_obs']
        old_action_log_probs = datas['log_probs']

        # calc return & advantage
        with torch.no_grad():
            values = self.critic(obs)
            next_values = self.critic(next_obs)
            returns = rewards + self.gamma * next_values - values
            advantage = returns - values

        # update critic
        values = self.critic(obs)
        critic_loss = torch.norm(values - returns)
        self.critic_optim.zero_grad()
        critic_loss.backward()
        self.critic_optim.step()

        # update actor
        mean, logstd = self.actor(obs)
        action_log_probs = neglogp(actions, mean, logstd)
        ratio = torch.exp(old_action_log_probs - action_log_probs)
        actor_loss = torch.max(
            - advantage * ratio,
            - advantage * torch.clamp(ratio, 1.0 - self.clip, 1.0 + self.clip)
        ).mean()

        self.actor.zero_grad()
        actor_loss.backward()
        self.actor_optim.step()

        self.eval()

        print(f'Epoch {self.num_epochs}: '
              f'actor_loss={actor_loss.item()}, '
              f'critic_loss={critic_loss.item()}, '
              f'reward={rewards.mean().item()}')


if __name__ == '__main__':
    num_envs = 512
    num_choices = 20
    model = PPO(num_choices, num_choices)
    dist_w = torch.randint(15, [num_envs, num_choices]).exp()
    dist_w = dist_w / dist_w.norm(dim=-1, keepdim=True)
    env_ids = torch.arange(num_envs)

    record = torch.zeros([num_envs, num_choices])

    for steps in range(10000):
        obs = record / steps if steps else record
        action = model.get_action(env_ids.tolist(), obs)
        choice = torch.multinomial(dist_w, 1).squeeze()
        reward = action[env_ids, choice]
        record[env_ids, choice] += 1
        next_obs = record / (steps + 1)
        model.update_post_datas(env_ids.tolist(), next_obs, choice)


