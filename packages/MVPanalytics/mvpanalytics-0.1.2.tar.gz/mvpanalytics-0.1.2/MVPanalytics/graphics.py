def plot_acf_pacf(data, lags=30):
    import matplotlib.pyplot as plt
    from statsmodels.tsa.stattools import acf, pacf
    """
    Строит графики ACF и PACF для временного ряда.

    Args:
        data: Временной ряд (pandas Series или numpy array).
        lags: Максимальное количество лагов для построения графиков (по умолчанию 30).
    """

    # Вычисляем ACF и PACF
    acf_values = acf(data, nlags=lags)
    pacf_values = pacf(data, nlags=lags)

    # Строим графики
    fig, axs = plt.subplots(2, 1, figsize=(10, 5))

    axs[0].plot(acf_values, marker = 'o')
    axs[0].axhline(y=0, linestyle='--', color='gray')
    axs[0].axhline(y=-1.96/np.sqrt(len(data)), linestyle='--', color='gray')
    axs[0].axhline(y=1.96/np.sqrt(len(data)), linestyle='--', color='gray')
    axs[0].set_title('ACF')
    axs[0].set_xlabel('Lag')

    axs[1].plot(pacf_values, marker = 'o')
    axs[1].axhline(y=0, linestyle='--', color='gray')
    axs[1].axhline(y=-1.96/np.sqrt(len(data)), linestyle='--', color='gray')
    axs[1].axhline(y=1.96/np.sqrt(len(data)), linestyle='--', color='gray')
    axs[1].set_title('PACF')
    axs[1].set_xlabel('Lag')

    plt.tight_layout()
    plt.show()