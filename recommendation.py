import numpy as np
import torch

from ppo import PPO
from functions.database import get_user_search_restaurant_counts, get_all_restaurant


# def get_user_search_restaurant_counts(user_id):
#     return {'a': 0, 'b': 2, 'c': 1}
#
# def get_all_restaurant():
#     return [{'id': 'b'}, {'id': 'a'}, {'id': 'c'}]


class RecommendationSystem:
    def __init__(self):
        self._obs_size = 50
        self._model = PPO(self._obs_size, 50)
        self._restId2nnId_map = {}
        self._num_restaurants = 0

    def get_obs(self, user_data):
        obs = torch.zeros([1, self._obs_size])
        for k, v in user_data.items():
            obs[:, self._restId2nnId_map[k]] = v
        return obs

    def recommend(self, user_id: int, restaurant_options: dict = {}):
        user_data = get_user_search_restaurant_counts(user_id)

        for k in user_data.keys():
            if self._restId2nnId_map.get(k) is None:
                self._restId2nnId_map[k] = self._num_restaurants
                self._num_restaurants += 1

        restaurants_id = []
        for i, rest in enumerate(get_all_restaurant()):
            ok = 1
            for k, v in restaurant_options.items():
                if rest[k] != v:
                    ok = 0
                    break
            if ok:
                restaurants_id.append(rest['id'])

        restaurants_id = np.array(restaurants_id)

        # sort meal
        preference = torch.Tensor([user_data[i] for i in restaurants_id])
        user_ids = torch.Tensor([user_id]).to(dtype=torch.long)
        obs = self.get_obs(user_data)
        action = self._model.get_action(user_ids, obs).squeeze()
        if self._model.num_epochs > 100:
            preference = torch.Tensor([action[self._restId2nnId_map[i]].item() for i in restaurants_id])
        order_idx = preference.sort(dim=-1, descending=True)[1]
        return list(restaurants_id[order_idx])

    def update_results(self, user_id: int, choice: int):
        user_data = get_user_search_restaurant_counts(user_id)
        env_ids = torch.Tensor([user_id]).to(dtype=torch.long)
        next_obs = self.get_obs(user_data)
        # next_obs = torch.zeros(5)
        choice = torch.Tensor([choice]).to(dtype=torch.long)
        self._model.update_post_datas(env_ids, next_obs, choice)


if __name__ == '__main__':
    rs = RecommendationSystem()
    print(rs.recommend(0))
    rs.update_results(0, 2)
