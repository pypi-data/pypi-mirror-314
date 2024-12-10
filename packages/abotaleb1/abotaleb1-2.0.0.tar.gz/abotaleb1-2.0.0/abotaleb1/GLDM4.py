class GLDM4:
    # Model 4 ==> Fourth-order Generalized Least Deviation Method (GLDM)
    def __init__(self):
        print("Initialized Model 4 ==> Fourth-order Generalized Least Deviation Method (GLDM)")
        
    # Model 4 ==>
    def run(self):
        print("Beginning the execution of the Fourth-order Generalized Least Deviation Method (GLDM)....")
        import math
        import numpy as np
        import matplotlib.pyplot as plt
        import statsmodels.api as sm
        import time
        import psutil
        import os
        import sys
        import glob
        case_name='Modelling using Fourth-order (GLDM)'

        class Errors:
            def __init__(self):
                self.E = 0.0
                self.D = 0.0
                self.minFH = 0  # reasonable forecasting horizon

        class Solution:
            def __init__(self):
                self.a = None
                self.z = None
                self.Z = 0.0
                self.py = None

        # Constants
        LARGE = 0x10000

        # Function pointers are represented as elements in a list
        # Expanded to include 14 functions for the fourth-order model
        G = [None] * 15

        # Define G functions for all single variables
        def G1(x1, x2, x3, x4):
            return x1

        def G2(x1, x2, x3, x4):
            return x2

        def G3(x1, x2, x3, x4):
            return x3

        def G4(x1, x2, x3, x4):
            return x4

        # Define G functions for all square terms
        def G5(x1, x2, x3, x4):
            return x1 * x1

        def G6(x1, x2, x3, x4):
            return x2 * x2

        def G7(x1, x2, x3, x4):
            return x3 * x3

        def G8(x1, x2, x3, x4):
            return x4 * x4

        # Define G functions for all two-variable products
        def G9(x1, x2, x3, x4):
            return x1 * x2

        def G10(x1, x2, x3, x4):
            return x1 * x3

        def G11(x1, x2, x3, x4):
            return x1 * x4

        def G12(x1, x2, x3, x4):
            return x2 * x3

        def G13(x1, x2, x3, x4):
            return x2 * x4

        def G14(x1, x2, x3, x4):
            return x3 * x4

        def GForming():
            G[1] = G1
            G[2] = G2
            G[3] = G3
            G[4] = G4
            G[5] = G5
            G[6] = G6
            G[7] = G7
            G[8] = G8
            G[9] = G9
            G[10] = G10
            G[11] = G11
            G[12] = G12
            G[13] = G13
            G[14] = G14

        def SSTForming(_Y):
            _SST = [[0.0 for _ in range(summs_count * 2 + 2)] for _ in range(summs_count + 1)]
            for i in range(1, summs_count + 1):
                for j in range(1, summs_count + 1):
                    for k in range(4, impl_len + 1):
                        _SST[i][j] += G[i](_Y[k - 1], _Y[k - 2], _Y[k - 3], _Y[k - 4]) * \
                                    G[j](_Y[k - 1], _Y[k - 2], _Y[k - 3], _Y[k - 4])
                for j in range(1, summs_count + 1):
                    _SST[i][summs_count + j] = 0.0
                _SST[i][summs_count + i] = 1.0

            print('\nMatrix SST\n')
            for i in range(1, summs_count + 1):
                print('\n', i, '\t', end='')
                for j in range(1, summs_count * 2 + 1):
                    print(_SST[i][j], '\t', end='')
            return _SST

        def JGTransforming(nn, _SST):
            for iter_first in range(1, nn + 1):
                mm = iter_first
                M = abs(_SST[iter_first][iter_first])
                for iter_second in range(iter_first + 1, nn + 1):
                    Mi = abs(_SST[iter_second][iter_first])
                    if Mi > M:
                        mm = iter_second
                        M = Mi
                _SST[iter_first], _SST[mm] = _SST[mm], _SST[iter_first]
                Temp = _SST[iter_first][iter_first]
                for iter_second in range(iter_first, 2 * nn + 1):
                    _SST[iter_first][iter_second] /= Temp
                for iter_second in range(1, iter_first):
                    Temp = _SST[iter_second][iter_first]
                    for iter_third in range(iter_first, 2 * nn + 1):
                        _SST[iter_second][iter_third] -= _SST[iter_first][iter_third] * Temp
                for iter_second in range(iter_first + 1, nn + 1):
                    Temp = _SST[iter_second][iter_first]
                    for iter_third in range(iter_first, 2 * nn + 1):
                        _SST[iter_second][iter_third] -= _SST[iter_first][iter_third] * Temp
                print('\nMatrix SST^-1\n')
                for iter_first in range(1, nn + 1):
                    print('\n', iter_first, '\t', end='')
                    for iter_third in range(1, nn + nn + 1):
                        print(_SST[iter_first][iter_third], '\t', end='')

        def P1Forming(_Y, _SST):
            _P1 = [[0.0 for _ in range(summs_count + 1)] for _ in range(impl_len + 2)]
            for t in range(5, impl_len + 1):
                for j in range(1, summs_count + 1):
                    _P1[t][j] = 0.0
                    for k in range(1, summs_count + 1):
                        _P1[t][j] += G[k](_Y[t - 1], _Y[t - 2], _Y[t - 3], _Y[t - 4]) * _SST[k][summs_count + j]
            print('\nMatrix P1[5:m][1:n]\n')
            for iter_first in range(5, impl_len + 1):
                print('\n', iter_first, '\t', end='')
                for iter_second in range(1, summs_count + 1):
                    print(_P1[iter_first][iter_second], '\t', end='')
            return _P1

        def PForming(_Y, _P1):
            _P = [[0.0 for _ in range(impl_len + 2)] for _ in range(impl_len + 2)]
            for iter_first in range(5, impl_len + 1):
                for iter_second in range(5, impl_len + 1):
                    _P[iter_first][iter_second] = 0.0
                    for iter_third in range(1, summs_count + 1):
                        _P[iter_first][iter_second] -= G[iter_third](_Y[iter_second - 1], _Y[iter_second - 2], _Y[iter_second - 3], _Y[iter_second - 4]) * _P1[iter_first][iter_third]
                    if iter_first == iter_second:
                        _P[iter_first][iter_first] += 1.0
            print('\nMatrix P[5:m][5:m]\n')
            for iter_first in range(5, impl_len + 1):
                print('\n', iter_first, '\t', end='')
                for iter_third in range(5, impl_len + 1):
                    print(_P[iter_first][iter_third], '\t', end='')
            return _P

        def PrGradForming(_Y, _P):
            _Prgrad = [0.0 for _ in range(impl_len + 2)]
            _grad = [0.0 for _ in range(impl_len + 2)]
            for i in range(1, impl_len + 2):
                _grad[i] = _Y[i]
            for iter_first in range(5, impl_len + 1):
                _Prgrad[iter_first] = 0.0
                for iter_second in range(5, impl_len + 1):
                    _Prgrad[iter_first] += _P[iter_first][iter_second] * _grad[iter_second]
            print('\ni   grad[i]   Prgrad[i]    p[i]  \n', end='')
            for iter_first in range(5, impl_len + 1):
                print(f'\n{iter_first}\t{_grad[iter_first]}\t{_Prgrad[iter_first]}\t', end='')
            return _Prgrad

        def DualWLDMSolution(_w, _p, _Prgrad):
            Al = LARGE
            Alc = 0
            for iter_first in range(5, impl_len + 1):
                _w[iter_first] = 0
            iter_first = 5
            while iter_first < impl_len - summs_count - 2:
                Al = LARGE
                for iter_second in range(5, impl_len + 1):
                    if abs(_w[iter_second]) == _p[iter_second]:
                        continue
                    else:
                        if _Prgrad[iter_second] > 0:
                            Alc = (_p[iter_second] - _w[iter_second]) / _Prgrad[iter_second]
                        elif _Prgrad[iter_second] < 0:
                            Alc = (-_p[iter_second] - _w[iter_second]) / _Prgrad[iter_second]
                        if Alc < Al:
                            Al = Alc
                for iter_second in range(5, impl_len + 1):
                    if abs(_w[iter_second]) != _p[iter_second]:
                        _w[iter_second] += Al * _Prgrad[iter_second]
                        if abs(_w[iter_second]) == _p[iter_second]:
                            iter_first += 1

        def PrimalWLDMSolution(_Y, _SST, _w, _p, _a, _z):
            lc_r = [0 for _ in range(summs_count + 1)]
            lc_ri = 0
            for iter_first in range(5, impl_len + 1):
                if abs(_w[iter_first]) != _p[iter_first]:
                    if lc_ri < len(lc_r) - 1:
                        lc_ri += 1
                        lc_r[lc_ri] = iter_first
                    else:
                        print(f"Error: lc_ri ({lc_ri}) exceeded lc_r bounds.")
                        break
            for iter_first in range(1, lc_ri + 1):
                for iter_second in range(1, lc_ri + 1):
                    _SST[iter_first][iter_second] = G[iter_second](_Y[lc_r[iter_first] - 1], _Y[lc_r[iter_first] - 2], _Y[lc_r[iter_first] - 3], _Y[lc_r[iter_first] - 4])
                _SST[iter_first][lc_ri + 1] = _Y[lc_r[iter_first]]
            JGTransforming(lc_ri, _SST)
            for iter_first in range(1, lc_ri + 1):
                _a[iter_first] = _SST[iter_first][lc_ri + 1]
                _z[lc_r[iter_first]] = 0

        def GLDMEstimator(_Y):
            lc_w = [0.0 for _ in range(impl_len + 2)]
            lc_p = [1.0 for _ in range(impl_len + 2)]
            lc_a1 = [0.0 for _ in range(summs_count + 1)]
            lc_a = [0.0 for _ in range(summs_count + 1)]
            lc_z = [0.0 for _ in range(impl_len + 2)]
            lc_SST = SSTForming(_Y)
            JGTransforming(summs_count, lc_SST)
            lc_P1 = P1Forming(_Y, lc_SST)
            lc_P = PForming(_Y, lc_P1)
            lc_Prgrad = PrGradForming(_Y, lc_P)
            Z = d = 0.0
            while True:
                for i in range(1, summs_count + 1):
                    lc_a1[i] = lc_a[i]
                for i in range(1, impl_len + 1):
                    lc_p[i] = 1.0 / (1.0 + lc_z[i] * lc_z[i])
                for i in range(1, impl_len + 1):
                    lc_w[i] = 0.0
                DualWLDMSolution(lc_w, lc_p, lc_Prgrad)
                print("Dual ok")
                PrimalWLDMSolution(_Y, lc_SST, lc_w, lc_p, lc_a, lc_z)
                print("Primal ok")
                Z = lc_z[1] = lc_z[2] = lc_z[3] = lc_z[4] = 0.0
                for i in range(5, impl_len + 1):
                    lc_z[i] = _Y[i]
                    for j in range(1, summs_count + 1):
                        lc_z[i] -= lc_a[j] * G[j](_Y[i - 1], _Y[i - 2], _Y[i - 3], _Y[i - 4])
                    Z += abs(lc_z[i])
                d = max([abs(lc_a[i] - lc_a1[i]) for i in range(1, summs_count + 1)])
                if d < 0.5:
                    break
            Sol = Solution()
            Sol.a = lc_a
            Sol.z = lc_z
            Sol.Z = Z
            return Sol

        def ForecastingEst(Y, Sol):
            PY = [[0.0 for _ in range(len(Y))] for _ in range(len(Y))]
            FH = [0 for _ in range(len(Y))]
            e = Errors()
            for St in range(len(Y) - 4):
                PY[St][0] = Y[St] if St < len(Y) else 0
                PY[St][1] = Y[St + 1] if St + 1 < len(Y) else 0
                PY[St][2] = Y[St + 2] if St + 2 < len(Y) else 0
                PY[St][3] = Y[St + 3] if St + 3 < len(Y) else 0
                t = 4
                while True:
                    if St + t >= len(Y):
                        break
                    py = 0
                    for j in range(1, len(Sol.a)):
                        if t - 4 >= 0:
                            A1 = G[j](PY[St][t - 1], PY[St][t - 2], PY[St][t - 3], PY[St][t - 4])
                            py += Sol.a[j] * A1
                        else:
                            break
                    PY[St][t] = py
                    t += 1
                    if abs(PY[St][t - 1] - Y[St + t - 1]) > Sol.Z:
                        break
                FH[St] = t - 1
            e.minFH = min(FH)
            e.E, e.D = 0, 0
            for St in range(len(Y) - 4):
                for t in range(5, e.minFH + 1):
                    if St + t < len(Y):
                        e.D += abs(Y[St + t] - PY[St][t])
                        e.E += (Y[St + t] - PY[St][t])
            if e.minFH > 0:
                e.E /= e.minFH
                e.D /= e.minFH
            return e

        def calculate_rmse(actual, predicted):
            return np.sqrt(((np.array(actual) - np.array(predicted)) ** 2).mean())

        def calculate_r_squared(actual, predicted):
            correlation_matrix = np.corrcoef(actual, predicted)
            correlation_xy = correlation_matrix[0,1]
            r_squared = correlation_xy**2
            return r_squared

        def calculate_mape(actual, predicted):
            actual, predicted = np.array(actual), np.array(predicted)
            non_zero_actual = actual != 0
            return np.mean(np.abs((actual[non_zero_actual] - predicted[non_zero_actual]) / actual[non_zero_actual])) * 100

        def calculate_mae(actual, predicted):
            return np.mean(np.abs(np.array(actual) - np.array(predicted)))

        def calculate_mse(actual, predicted):
            return np.mean((np.array(actual) - np.array(predicted)) ** 2)

        def calculate_me(actual, predicted):
            return np.mean(np.array(actual) - np.array(predicted))

        def calculate_median_absolute_error(actual, predicted):
            return np.median(np.abs(np.array(actual) - np.array(predicted)))

        def calculate_mase(actual, predicted, seasonal_period=1):
            actual, predicted = np.array(actual), np.array(predicted)
            n = len(actual)
            d = np.abs(np.diff(actual, n=seasonal_period)).sum() / (n - seasonal_period)
            errors = np.mean(np.abs(actual - predicted))
            return errors / d

        def calculate_mbe(actual, predicted):
            return np.mean(np.array(actual) - np.array(predicted))

        def calculate_time_series_values(Y, Sol, length):
            calculated_values = [0.0 for _ in range(length)]
            for i in range(4):
                calculated_values[i] = Y[i]
            for t in range(4, length):
                value = Sol.a[0]
                for i in range(1, len(Sol.a)):
                    value += Sol.a[i] * G[i](Y[t - 1], Y[t - 2], Y[t - 3], Y[t - 4])
                calculated_values[t] = value
            return calculated_values

        def plot_time_series_adjusted(original_data, calculated_data, series_number, save_path):
            plt.figure(figsize=(10, 6))
            if len(original_data) >= 5 and len(calculated_data) >= 5:
                for i in range(5):
                    calculated_data[i] = original_data[i]
            min_length = min(len(original_data), len(calculated_data))
            original_data_adjusted = original_data[1:min_length-1]
            calculated_data_adjusted = calculated_data[1:min_length-1]
            x_axis_range = range(1, min_length - 1)
            plt.plot(x_axis_range, original_data_adjusted, label='Original', color='blue', linewidth=2)
            plt.plot(x_axis_range, calculated_data_adjusted,  label='GLDM Model', color='black', linestyle='dotted', linewidth=2)
            plt.title(f'Time Series {case_name}: Original vs GLDM Model', fontsize=16)
            plt.xlabel('Time', fontsize=14)
            plt.ylabel('Value', fontsize=14)
            plt.legend(loc='best', fontsize=12)
            plt.grid(True, which='both', linestyle='--', linewidth=0.5)
            plt.savefig(save_path, format='png', dpi=300)
            plt.close()

        def main():
            start_time = time.time()
            process = psutil.Process(os.getpid())
            initial_memory_use = process.memory_info().rss / (1024 * 1024)
            with open("input.txt", "r") as f, open("GLDM_Fourth_order_output.txt", "w") as g:       
                lc_c = ''
                while lc_c != ':':
                    lc_c = f.read(1)
                m, ts = map(int, f.readline().split())
                global impl_len
                impl_len = m
                global summs_count
                summs_count = 14  # Updated to 14 for the fourth-order model
                print(f"Length: {m}\nTime series: {ts}\n")
                setnum = 0
                RY = [[] for _ in range(ts)]
                for i in range(ts):
                    RY[i] = [0] * (m + 2)
                while setnum < ts:
                    print("Reading time series", setnum)
                    ic = 1
                    while ic <= m:
                        line = f.readline()
                        s = float(line)
                        RY[setnum][ic] = s
                        ic += 1
                    print("\n Finished reading of time series", setnum)
                    setnum += 1
                GL_RY = RY        
                g.write(f"Number of time series: {ts}\n")
                g.write(f"Length of time series: {impl_len}\n")
                for sn in range(ts):
                    Y = [0] * (m + 2)
                    k = 1
                    for j in range(1, m + 1):
                        Y[j] = RY[sn][j]
                        k += 1
                    GL_Y = GL_RY[sn]
                    lc_SST = np.zeros((summs_count + 1, summs_count * 2 + 2), dtype=float)
                    GForming()
                    print("GForming() OK\n")
                    lc_SST = SSTForming(GL_Y)
                    JGTransforming(summs_count, lc_SST)
                    print("\n JGTransforming() OK\n")
                    Sol = GLDMEstimator(GL_Y)
                    print("GLDMEstimator() OK\n")
                    calculated_ts_values = calculate_time_series_values(GL_Y, Sol, len(GL_Y))
                    original_data_trimmed = GL_Y
                    calculated_data_trimmed = calculated_ts_values [:]
                    start_index = 5
                    min_length = min(len(original_data_trimmed), len(calculated_ts_values))
                    original_data_trimmed = original_data_trimmed[:min_length]
                    calculated_data_trimmed = calculated_ts_values[:min_length]
                    mae = calculate_mae(original_data_trimmed[start_index:-1], calculated_data_trimmed[start_index:-1])
                    mbe = calculate_mbe(original_data_trimmed[start_index:-1], calculated_data_trimmed[start_index:-1])
                    mse = calculate_mse(original_data_trimmed[start_index:-1], calculated_data_trimmed[start_index:-1])
                    rmse = calculate_rmse(original_data_trimmed[start_index:-1], calculated_data_trimmed[start_index:-1])
                    r_squared = calculate_r_squared(original_data_trimmed[start_index:-1], calculated_data_trimmed[start_index:-1])
                    mape = calculate_mape(original_data_trimmed[start_index:-1], calculated_data_trimmed[start_index:-1])
                    me = calculate_me(original_data_trimmed[start_index:-1], calculated_data_trimmed[start_index:-1])
                    median_abs_error = calculate_median_absolute_error(original_data_trimmed[start_index:-1], calculated_data_trimmed[start_index:-1])
                    seasonal_period = 1
                    mase = calculate_mase(original_data_trimmed[start_index:-1], calculated_data_trimmed[start_index:-1], seasonal_period)
                    g.write(f"Error Matrix start from Fifth point to the end of dataset\n")
                    g.write(f"RMSE: {rmse}\n")
                    g.write(f"R-squared: {r_squared}\n")
                    g.write(f"MAPE: {mape}\n")
                    g.write(f"MAE: {mae}\n")
                    g.write(f"MSE: {mse}\n")
                    g.write(f"ME: {me}\n")
                    g.write(f"Median Absolute Error: {median_abs_error}\n")
                    g.write(f"MASE: {mase}\n")
                    g.write(f"MBE: {mbe}\n")
                    g.write(f"{'Original Data':<20}{'Calculated Data':<20}{'Error':<20}\n")
                    for orig, calc in zip(original_data_trimmed, calculated_data_trimmed):
                        error = orig - calc
                        g.write(f"{orig:<20}{calc:<20}{error:<20}\n")
                    ANS = [0] * 25
                    ANS[0] = sn
                    ANS[1] = 0
                    for i in range(summs_count):
                        ANS[i + 2] = Sol.a[i + 1]
                    ANS[21] = Sol.Z
                    e = ForecastingEst(GL_Y, Sol)
                    print("ForecastingEST OK\n")
                    print(e.minFH, "\n", end='')
                    ANS[22] = e.minFH
                    ANS[23] = e.D
                    ANS[24] = e.E
                    g.write(f"Time Series Number: {ANS[0]}\n")
                    g.write("Model Coefficients:\n")
                    for i in range(2, 16):
                        g.write(f"Coefficient a{i-1}: {ANS[i]}\n")
                    g.write(f"Sum of Absolute Differences: {ANS[21]}\n")
                    g.write(f"Minimum Forecasting Horizon: {ANS[22]}\n")
                    g.write(f"Average Absolute Error: {ANS[23]}\n")
                    g.write(f"Average Error: {ANS[24]}\n")
                    g.write("\nG Function Values:\n")
                    if len(Y) >= 4:
                        x1, x2, x3, x4 = Y[-4], Y[-3], Y[-2], Y[-1]
                        for i in range(1, summs_count + 1):
                            g_value = G[i](x1, x2, x3, x4)
                            g.write(f"G{i}({x1}, {x2}, {x3}, {x4}): {g_value}\n")
                    g.write("Original Time Series Data:\n")
                    for j in range(1, m+1):
                        g.write(f"{Y[j]}\n")
                    g.write("original data trimmed:\n")
                    for value in original_data_trimmed[start_index:-1]:
                        g.write(f"{value}\n")
                    col_widths = [25, 25, 25]
                    headers = ["Original Data", "Calculated Data", "Error"]
                    header_line = "".join(f"{header:<{width}}" for header, width in zip(headers, col_widths))
                    g.write(header_line + "\n")
                    g.write("-" * sum(col_widths) + "\n")
                    data_length = min(len(original_data_trimmed) - start_index - 1, len(calculated_data_trimmed) - start_index - 1)
                    for i in range(data_length):
                        original = original_data_trimmed[start_index + i]
                        calculated = calculated_data_trimmed[start_index + i]
                        error = original - calculated
                        original_str = f"{original}"
                        calculated_str = f"{calculated}"
                        error_str = f"{error}"
                        data_line = f"{original_str:<{col_widths[0]}}{calculated_str:<{col_widths[1]}}{error_str:<{col_widths[2]}}"
                        g.write(data_line + "\n")
                    original_data = Y[1:-1]
                    calculated_data = calculate_time_series_values(GL_Y, Sol, len(GL_Y))[1:-1]
                    plot_save_path = f"plot_series_{sn}.png"
                    plot_time_series_adjusted(Y, calculated_ts_values, sn, f'Fourth_order_GLDM{sn}.png')
                    #plot_time_series(original_data, calculated_data, sn, plot_save_path)
                    end_time = time.time()
                    final_memory_use = process.memory_info().rss / (1024 * 1024)
                    total_time = end_time - start_time
                    total_memory_used = final_memory_use - initial_memory_use
                    g.write("\nPerformance Metrics:\n")
                    g.write(f"Total Execution Time: {total_time:.2f} seconds\n")
                    g.write(f"Total Additional Memory Used: {total_memory_used:.2f} MB\n")

        #if __name__ == "__main__":
        main()
        print("Completing the execution of the Fourth-order Generalized Least Deviation Method (GLDM).")