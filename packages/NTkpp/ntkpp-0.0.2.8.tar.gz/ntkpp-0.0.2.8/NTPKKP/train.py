import numpy as np


def train(network, x_train, y_train, loss_func, epochs, batch_size=None, optimizer=None):
    """
    Обучает нейронную сеть на заданных тренировочных данных.

    Параметры:
    network: объект сети, который имеет методы forward и backward для прямого и обратного распространения.
    x_train: ndarray, входные данные для обучения (размерность: [количество образцов, количество признаков]).
    y_train: ndarray, целевые значения (размерность: [количество образцов, количество выходов]).
    loss_func: функция потерь, которая оценивает разницу между предсказаниями сети и целевыми значениями.
    epochs: int, количество эпох для обучения сети.
    batch_size: int или None, размер батча для мини-батч обучения (если None, обучение происходит на всех данных за раз).
    optimizer: объект оптимизатора, который будет использован для обновления весов слоя (может быть None).

    """
    n_samples = x_train.shape[0]  # Количество обучающих образцов

    for epoch in range(epochs):
        print(f"\nЭпоха {epoch + 1}/{epochs}:")

        if batch_size:  # Если указан размер батча, проводим обучение по батчам
            indices = np.arange(n_samples)  # Индексы всех образцов
            np.random.shuffle(indices)  # Перемешиваем индексы для случайной выборки

            x_train, y_train = x_train[indices], y_train[indices]  # Перемешиваем данные

            for start_idx in range(0, n_samples, batch_size):
                end_idx = start_idx + batch_size
                x_batch = x_train[start_idx:end_idx]  # Получаем текущий батч данных
                y_batch = y_train[start_idx:end_idx]  # Получаем текущий батч целевых значений

                # Обратное распространение и обновление весов для текущего батча
                network.backward(x_batch, y_batch, loss_func)

                for layer in network.layers:
                    if hasattr(layer, 'update_weights'):
                        layer.update_weights(network.learning_rate, optimizer=optimizer)  # Обновление весов слоя

                # Вычисляем потери для текущего батча
                batch_loss = (loss_func(y_batch, network.forward(x_batch))) / y_batch.size

                # Вывод ошибки каждый батч
                batch_num = start_idx // batch_size + 1
                if batch_num % batch_size == 0:
                    print(f"  Батч {batch_num}, Потеря: {batch_loss:.4f}")

        else:  # Обучение без разбивки на батчи
            network.backward(x_train, y_train, loss_func)  # Обратное распространение для всех данных

            for layer in network.layers:  # Обновление весов для всех слоев
                if hasattr(layer, 'update_weights'):
                    layer.update_weights(network.learning_rate, optimizer=optimizer)
            # Вычисляем потери эпоху
            epoch_loss = (loss_func(y_train, network.forward(x_train))) / y_train.size
            print(f"Итоговая потеря за эпоху: {epoch_loss:.4f}")