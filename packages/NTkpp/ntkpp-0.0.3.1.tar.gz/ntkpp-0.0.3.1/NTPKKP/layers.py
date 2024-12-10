import numpy as np


class DenseLayer:
    def __init__(self, input_size, output_size, activation_func, weights_initializer='random', biases_initializer='ones', learning_rate=0.01,
                 decay_rate=0.9, epsilon=1e-7):
        """
        Инициализация слоя нейронной сети.

        Параметры:
        input_size (int): Размер входных данных.
        output_size (int): Размер выходных данных.
        activation_func (object): Функция активации (например, ReLU, Sigmoid, Softmax и т. д.).
        is_last_layer (bool): Указывает, является ли слой последним (по умолчанию False).
        weights_initializer (str): Метод инициализации весов ('random', 'xavier', 'he', 'normal').
        biases_initializer (str): Метод инициализации смещений ('zeros', 'ones', 'normal').
        learning_rate (float): Скорость обучения для обновления весов.
        decay_rate (float): Коэффициент затухания для оптимизаторов, таких как RMSProp и AdaDelta.
        epsilon (float): Малое значение для предотвращения деления на ноль в оптимизаторах.
        """
        self.activation_func = activation_func
        self.learning_rate = learning_rate
        self.decay_rate = decay_rate
        self.epsilon = epsilon

        # Инициализация весов в зависимости от выбранного метода
        if weights_initializer == 'random':
            self.weights = np.random.randn(input_size, output_size) * 0.01
        elif weights_initializer == 'xavier':
            self.weights = np.random.randn(input_size, output_size) * np.sqrt(1 / input_size)
        elif weights_initializer == 'he':
            self.weights = np.random.randn(input_size, output_size) * np.sqrt(2 / input_size)
        elif weights_initializer == 'normal':
            self.weights = np.random.normal(0, 1, (input_size, output_size))
        else:
            raise ValueError(f"Unknown weights initializer: {weights_initializer}")

        # Инициализация смещений в зависимости от выбранного метода
        if biases_initializer == 'zeros':
            self.biases = np.zeros((1, output_size))
        elif biases_initializer == 'ones':
            self.biases = np.ones((1, output_size))
        elif biases_initializer == 'normal':
            self.biases = np.random.normal(0, 1, (1, output_size))
        else:
            raise ValueError(f"Unknown biases initializer: {biases_initializer}")

        # Инициализация переменных для оптимизации
        self.squared_grad_weights = np.zeros_like(self.weights)
        self.squared_grad_biases = np.zeros_like(self.biases)
        self.m_weights = np.zeros_like(self.weights)
        self.v_weights = np.zeros_like(self.weights)
        self.m_biases = np.zeros_like(self.biases)
        self.v_biases = np.zeros_like(self.biases)
        self.beta1 = 0.9
        self.beta2 = 0.999
        self.t = 1

    def forward(self, inputs):
        """
        Прямой проход через слой нейронной сети.

        Параметры:
        inputs (ndarray): Входные данные.

        Возвращает:
        ndarray: Выходные данные после применения весов, смещений и функции активации.
        """
        self.inputs = inputs
        self.z = np.dot(inputs, self.weights) + self.biases  # Линейное преобразование
        self.a = self.activation_func(self.z)  # Применение функции активации
        return self.a

    def backward(self, grad_output):
        """
        Обратный проход через слой нейронной сети для вычисления градиентов.

        Параметры:
        grad_output (ndarray): Градиент ошибки на выходе слоя.

        Возвращает:
        ndarray: Градиент ошибки для входных данных слоя.
        """
        grad_activation = self.activation_func.derivative(self.z)  # Производная функции активации
        grad_input = np.dot(grad_output * grad_activation, self.weights.T)  # Градиент по входным данным
        self.grad_weights = np.dot(self.inputs.T, grad_output)  # Градиент по весам
        self.grad_biases = np.sum(grad_output, axis=0, keepdims=True)  # Градиент по смещениям
        return grad_input

    def update_weights(self, learning_rate, optimizer=None):
        """
        Обновление весов и смещений с использованием выбранного оптимизатора.

        Параметры:
        learning_rate (float): Скорость обучения.
        optimizer (str): Метод оптимизации ('RMSProp', 'AdaGrad', 'Adam', 'AdaDelta', 'SGD').

        Важные оптимизаторы:
        - 'RMSProp', 'AdaGrad', 'Adam' и 'AdaDelta' используют адаптивные шаги обновления для весов и смещений.
        - 'SGD' (Stochastic Gradient Descent) просто обновляет веса и смещения на основе градиента.
        """
        if optimizer == "RMSProp":
            # Обновление с использованием RMSProp
            self.squared_grad_weights = self.decay_rate * self.squared_grad_weights + (1 - self.decay_rate) * (self.grad_weights ** 2)
            self.squared_grad_biases = self.decay_rate * self.squared_grad_biases + (1 - self.decay_rate) * (self.grad_biases ** 2)
            self.weights -= learning_rate * self.grad_weights / (np.sqrt(self.squared_grad_weights) + self.epsilon)
            self.biases -= learning_rate * self.grad_biases / (np.sqrt(self.squared_grad_biases) + self.epsilon)
        elif optimizer == "AdaGrad":
            # Обновление с использованием AdaGrad
            self.squared_grad_weights += self.grad_weights ** 2
            self.squared_grad_biases += self.grad_biases ** 2
            self.weights -= learning_rate * self.grad_weights / (np.sqrt(self.squared_grad_weights) + self.epsilon)
            self.biases -= learning_rate * self.grad_biases / (np.sqrt(self.squared_grad_biases) + self.epsilon)
        elif optimizer == "Adam":
            # Обновление с использованием Adam
            self.m_weights = self.beta1 * self.m_weights + (1 - self.beta1) * self.grad_weights
            self.v_weights = self.beta2 * self.v_weights + (1 - self.beta2) * (self.grad_weights ** 2)
            self.m_biases = self.beta1 * self.m_biases + (1 - self.beta1) * self.grad_biases
            self.v_biases = self.beta2 * self.v_biases + (1 - self.beta2) * (self.grad_biases ** 2)
            m_weights_hat = self.m_weights / (1 - self.beta1 ** self.t)
            v_weights_hat = self.v_weights / (1 - self.beta2 ** self.t)
            m_biases_hat = self.m_biases / (1 - self.beta1 ** self.t)
            v_biases_hat = self.v_biases / (1 - self.beta2 ** self.t)
            self.weights -= learning_rate * m_weights_hat / (np.sqrt(v_weights_hat) + self.epsilon)
            self.biases -= learning_rate * m_biases_hat / (np.sqrt(v_biases_hat) + self.epsilon)
            self.t += 1
        elif optimizer == "AdaDelta":
            # Обновление с использованием AdaDelta
            self.squared_grad_weights = self.decay_rate * self.squared_grad_weights + (1 - self.decay_rate) * (self.grad_weights ** 2)
            self.squared_grad_biases = self.decay_rate * self.squared_grad_biases + (1 - self.decay_rate) * (self.grad_biases ** 2)
            update_weights = -self.grad_weights * (np.sqrt(self.m_weights + self.epsilon) / np.sqrt(self.squared_grad_weights + self.epsilon))
            update_biases = -self.grad_biases * (np.sqrt(self.m_biases + self.epsilon) / np.sqrt(self.squared_grad_biases + self.epsilon))
            self.m_weights = self.decay_rate * self.m_weights + (1 - self.decay_rate) * (update_weights ** 2)
            self.m_biases = self.decay_rate * self.m_biases + (1 - self.decay_rate) * (update_biases ** 2)
            self.weights += update_weights
            self.biases += update_biases
        elif optimizer == "SGD":
            # Обновление с использованием стандартного градиентного спуска
            self.weights -= learning_rate * self.grad_weights
            self.biases -= learning_rate * self.grad_biases
