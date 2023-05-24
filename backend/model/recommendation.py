import numpy as np
import torch

from ppo import PPO


class RecommendationSystem:
    def __init__(self, num_labels, database):
        self._database = database
        self._model = PPO(num_labels, 50)

    def recommend(self, user_id: int, restaurant_options: dict = {}, meal_options: dict = {}):
        user_data = self._database.get_user_info(user_id)

        # match restaurants
        restaurants_set = set()
        for meal in self._database.meals:
            restaurants_set.add(self._database.restaurants[meal['restaurant']])
            for k, v in meal_options.items():
                if meal[k] != v:
                    restaurants_set.remove(meal)

        restaurants = []
        restaurants_names = []
        for rest in restaurants_set:
            ok = 1
            for k, v in restaurant_options.items():
                if rest[k] != v:
                    ok = 0
                    break
            if ok:
                restaurants.append(rest['id'])
                restaurants_names.append(rest['name'])

        restaurants_names = np.array(restaurants_names)

        # user_history = [0, 1, 2, 3, 4]
        # restaurants = [1, 2, 3]
        # restaurants_names = np.array(['a', 'b', 'c'])

        # sort meal
        user_ids = torch.Tensor([user_id]).to(dtype=torch.long)
        obs = torch.Tensor([user_data.values()])
        logits = self._model.get_action(user_ids, obs).squeeze()[restaurants]
        order_idx = logits.sort(dim=-1, descending=True)[1]
        return list(restaurants_names[order_idx])

    def update_results(self, user_id: int, choice: int):
        user_data = self._database.get_user_info(user_id)
        env_ids = torch.Tensor([user_id]).to(dtype=torch.long)
        next_obs = torch.Tensor([user_data.values()])
        # next_obs = torch.zeros(5)
        choice = torch.Tensor([choice]).to(dtype=torch.long)
        self._model.update_post_datas(env_ids, next_obs, choice)


if __name__ == '__main__':
    rs = RecommendationSystem(5, None)
    print(rs.recommend(0))
    rs.update_results(0, 2)
