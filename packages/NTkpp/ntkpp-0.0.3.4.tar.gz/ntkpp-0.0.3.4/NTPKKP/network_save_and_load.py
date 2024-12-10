import h5py
import numpy as np

from NTPKKP import NeuralNetwork, ReLU, Sigmoid, Tanh, Softmax, DenseLayer


def save_model(network, file_path):
    """
        Сохраняет обученную модель в H5 файл.

        Параметры:
        network: объект NeuralNetwork, содержащий обученную модель.
        file_path: str, путь к файлу для сохранения.
        """
    with h5py.File(file_path, 'w') as f:
        # Сохраняем скорость обучения
        f.attrs['learning_rate'] = network.learning_rate

        for i, layer in enumerate(network.layers):
            group = f.create_group(f'layer_{i}')
            group.create_dataset('weights', data=layer.weights)
            group.create_dataset('biases', data=layer.biases)
            group.attrs['activation'] = layer.activation_func.__class__.__name__


def load_model(file_path):
    """
        Загружает обученную модель из H5 файла.

        Параметры:
        network_class: класс NeuralNetwork для создания объекта сети.
        layer_class: класс DenseLayer для создания слоев.
        file_path: str, путь к файлу для загрузки.
        activation_mapping: dict, отображение имен активаций в функции активации.

        Возвращает:
        network: объект NeuralNetwork с загруженной моделью.
        """
    with h5py.File(file_path, 'r') as f:
        learning_rate = f.attrs['learning_rate']
        network = NeuralNetwork(learning_rate=learning_rate)
        activation_mapping = {
            'ReLU': ReLU,
            'Sigmoid': Sigmoid,
            'Softmax': Softmax,
            'Tanh': Tanh
        }
        for i in range(len(f.keys())):
            group = f[f'layer_{i}']
            weights = np.array(group['weights'])
            biases = np.array(group['biases'])
            activation_name = group.attrs['activation']

            # Определяем функцию активации
            activation_func = activation_mapping[activation_name]()

            # Создаем слой и добавляем его в сеть
            layer = DenseLayer(weights.shape[0], weights.shape[1], activation_func)
            layer.weights = weights
            layer.biases = biases
            network.add_layer(layer)

    return network
