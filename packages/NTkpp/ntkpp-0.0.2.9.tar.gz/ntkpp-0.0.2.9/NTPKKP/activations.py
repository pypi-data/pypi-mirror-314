import numpy as np


class ReLU:
    """
        Класс для функции активации ReLU (Rectified Linear Unit).
        """

    def __call__(self, z):
        """
        Вычисляет значение функции ReLU для входного массива z.
        ReLU(z) = max(0, z)

        Параметры:
        z (ndarray): Входной массив.

        Возвращает:
        ndarray: Массив после применения функции ReLU.
        """
        return np.maximum(0, z)

    @staticmethod
    def derivative(z):
        """
        Вычисляет производную функции ReLU по входу z.
        Производная равна 1 для z > 0 и 0 для z <= 0.

        Параметры:
        z (ndarray): Входной массив.

        Возвращает:
        ndarray: Массив значений производной функции ReLU.
        """
        derivative = np.ones_like(z)
        derivative[z <= 0] = 0
        return derivative


# Класс для функции активации сигмоиды
class Sigmoid:
    def __call__(self, z):
        """
        Вычисляет значение сигмоидной функции для входного массива z.
        Sigmoid(z) = 1 / (1 + exp(-z))

        Параметры:
        z (ndarray): Входной массив.

        Возвращает:
        ndarray: Массив после применения сигмоиды.
        """
        return 1 / (1 + np.exp(-z))

    @staticmethod
    def derivative(z):
        """
        Вычисляет производную сигмоидной функции по входу z.
        Производная: sigmoid(z) * (1 - sigmoid(z))

        Параметры:
        z (ndarray): Входной массив.

        Возвращает:
        ndarray: Массив значений производной сигмоиды.
        """
        sigmoid = 1 / (1 + np.exp(-z))
        return sigmoid * (1 - sigmoid)


# Класс для функции активации гиперболического тангенса
class Tanh:
    """
       Класс для функции активации Tanh (гиперболический тангенс).
       """

    def __call__(self, z):
        """
        Вычисляет значение функции гиперболического тангенса для z.
        Tanh(z) = tanh(z)

        Параметры:
        z (ndarray): Входной массив.

        Возвращает:
        ndarray: Массив после применения tanh.
        """
        return np.tanh(z)

    @staticmethod
    def derivative(z):
        """
        Вычисляет производную функции гиперболического тангенса по входу z.
        Производная: 1 - tanh(z)^2

        Параметры:
        z (ndarray): Входной массив.

        Возвращает:
        ndarray: Массив значений производной функции tanh.
        """
        return 1 - np.tanh(z) ** 2


# Класс для функции активации Softmax
class Softmax:
    """
       Класс для функции активации Softmax.
       """
    def __call__(self, z):
        """
        Вычисляет значение функции Softmax для входного массива z.
        Softmax(z) = exp(z) / sum(exp(z))

        Параметры:
        z (ndarray): Входной массив.

        Возвращает:
        ndarray: Массив после применения Softmax.
        """
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))  # Нормализация для численной устойчивости
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)

    @staticmethod
    def derivative(z):
        """
        Заглушка для производной Softmax.
        Производная Softmax является более сложной, поэтому здесь она упрощена.
        """
        return 1  # В Softmax производная требует отдельного подхода, который обычно не реализуется прямо
