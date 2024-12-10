from typing import List, Tuple
import remdex.framework as framework

def __empty_function__(*args, **kwargs):
    return None

class Metric(framework.Metric):
    def __init__(self, name: str, value, weight: float = 1) -> None:
        super().__init__(name, value, weight)

class Params(framework.Params):
    def __init__(self, params, weight: float = 1) -> None:
        super().__init__(params, weight)

class Gradients(framework.Gradients):
    def __init__(self, gradients, weight: float = 1) -> None:
        super().__init__(gradients, weight)

class Model(framework.Model):
    def __init__(self, model, name: str) -> None:
        super().__init__(model, name)

class FedAvgClient(framework.FedAvgClient):
    def __init__(self):
        super().__init__()
    def train(self):
        return super().train()
    def batch_generator(self):
        return super().batch_generator()
    def batch_train(self, batch):
        return super().batch_train(batch)
    def evaluate(self) -> List[framework.Metric]:
        return super().evaluate()
    def get_params(self) -> List[framework.Params]:
        return super().get_params()
    def update_params(self, parameters: List[List]):
        return super().update_params(parameters)
    def save(self):
        return super().save()
    def return_models(self) -> List[framework.Model]:
        return super().return_models()
    def start(self, server_address: str):
        return super().start(server_address)
    
class FedAvgClientTrain(framework.FedAvgClient):
    train_executor = __empty_function__
    batch_generator_executor = __empty_function__
    batch_train_executor = __empty_function__
    evaluate_executor = __empty_function__
    get_params_executor = __empty_function__
    update_params_executor = __empty_function__
    return_models_executor = __empty_function__
    def __init__(self):
        super().__init__()
    def train(self):
        return self.train_executor()
    def batch_generator(self):
        return self.batch_generator_executor()
    def batch_train(self, batch):
        return self.batch_train_executor()
    def evaluate(self) -> List[framework.Metric]:
        return self.evaluate_executor()
    def get_params(self) -> List[framework.Params]:
        return self.get_params_executor()
    def update_params(self, parameters: List[List]):
        return self.update_params_executor(parameters)
    def save(self):
        return super().save()
    def return_models(self) -> List[framework.Model]:
        return self.return_models_executor() 
    def start(self, server_address: str):
        return super().start(server_address)
    
class FedAvgTrainer: 
    def __init__(self) -> None:
        self.client_train = FedAvgClientTrain()
    def train(self):
        def __wrapper__(fn):
            self.client_train.train_executor = fn
        return __wrapper__
    def batch_generator(self):
        def __wrapper__(fn):
            self.client_train.batch_generator_executor = fn
        return __wrapper__
    def batch_train(self):
        def __wrapper__(fn):
            self.client_train.batch_train_executor = fn
        return __wrapper__
    def evaluate(self):
        def __wrapper__(fn):
            self.client_train.evaluate_executor = fn
        return __wrapper__
    def get_params(self):
        def __wrapper__(fn):
            self.client_train.get_params_executor = fn
        return __wrapper__
    def update_params(self):
        def __wrapper__(fn):
            self.client_train.update_params_executor = fn
        return __wrapper__
    def return_models(self):
        def __wrapper__(fn):
            self.client_train.return_models_executor = fn
        return __wrapper__
    def start(self, server_address: str):
        self.client_train.start(server_address)

class FedSgdClient(framework.FedSgdClient):
    def __init__(self):
        super().__init__()
    def train(self) -> List[framework.Gradients]:
        return super().train()
    def optimize(self, gradients: List[List]):
        return super().optimize(gradients)
    def batch_generator(self):
        return super().batch_generator()
    def batch_train(self, batch) -> List[framework.Gradients]:
        return super().batch_train(batch)
    def evaluate(self) -> List[framework.Metric]:
        return super().evaluate()
    def save(self):
        return super().save()
    def return_models(self) -> List[framework.Model]:
        return super().return_models()
    def start(self, server_address: str):
        return super().start(server_address)
    
class FedSgdClientTrain(framework.FedSgdClient):
    train_executor = __empty_function__
    optimize_executor = __empty_function__
    batch_generator_executor = __empty_function__
    batch_train_executor = __empty_function__
    evaluate_executor = __empty_function__
    return_models_executor = __empty_function__
    def __init__(self):
        super().__init__()
    def train(self) -> List[framework.Gradients]:
        return self.train_executor()
    def optimize(self, gradients: List[List]):
        return self.optimize_executor(gradients)
    def batch_generator(self):
        return self.batch_generator_executor()
    def batch_train(self, batch) -> List[framework.Gradients]:
        return self.batch_train_executor(batch)
    def evaluate(self) -> List[framework.Metric]:
        return self.evaluate_executor()
    def save(self):
        return super().save()
    def return_models(self) -> List[framework.Model]:
        return self.return_models_executor()
    def start(self, server_address: str):
        return super().start(server_address)
    
class FedSgdTrainer:
    def __init__(self) -> None:
        self.client_train = FedSgdClientTrain()
    def train(self): 
        def __wrapper__(fn):
            self.client_train.train_executor = fn
        return __wrapper__
    def optimize(self): 
        def __wrapper__(fn):
            self.client_train.optimize_executor = fn
        return __wrapper__
    def batch_generator(self): 
        def __wrapper__(fn):
            self.client_train.batch_generator_executor = fn
        return __wrapper__
    def batch_train(self): 
        def __wrapper__(fn):
            self.client_train.batch_train_executor = fn
        return __wrapper__
    def evaluate(self): 
        def __wrapper__(fn):
            self.client_train.evaluate_executor = fn
        return __wrapper__
    def return_models(self): 
        def __wrapper__(fn):
            self.client_train.return_models_executor = fn
        return __wrapper__
    def start(self, server_address: str):
        self.client_train.start(server_address=server_address)
    
class FedAvgServer(framework.FedAvgServer):
    def __init__(self, address: str, epochs: int, num_clients: int, batched=False, init_params: List[List] = None) -> None:
        super().__init__(address, epochs, num_clients, batched, init_params)
    def start(self):
        return super().start()
    
class FedSgdServer(framework.FedSgdServer):
    def __init__(self, address: str, epochs: int, num_clients: int, batched=False, init_params: List[List] = None) -> None:
        super().__init__(address, epochs, num_clients, batched, init_params)
    def start(self):
        return super().start()


