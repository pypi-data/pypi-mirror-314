class GLDM1:
    # Model 1 ==> First-order Generalized Least Deviation Method (GLDM).
    def __init__(self):
        print("Initialized Model 1 ==> First-order Generalized Least Deviation Method (GLDM).")
    def run(self):
        print("Beginning the execution of the First-order Generalized Least Deviation Method (GLDM)....")

        import math
        import numpy as np
        import matplotlib.pyplot as plt
        import statsmodels.api as sm
        import time
        import psutil
        import os
        import sys
        import glob

        case_name = 'Modelling using First-order (GLDM)'

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
        G = [None, None]  # Array for function pointers, now only for G1 and G2

        def G1(x):
            return x

        def G2(x):
            return x * x

        # Update GForming to include only G1 and G2
        def GForming():
            G[0] = G1
            G[1] = G2

        def SSTForming(_Y):
            _SST = [[0.0 for _ in range(summs_count * 2)] for _ in range(summs_count)]
            for i in range(summs_count):
                for j in range(summs_count):
                    for k in range(2, impl_len + 1):
                        _SST[i][j] += G[i](_Y[k - 1]) * G[j](_Y[k - 1])
                for j in range(summs_count):
                    _SST[i][summs_count + j] = 0.0
                _SST[i][summs_count + i] = 1.0
            return _SST

        def JGTransforming(nn, _SST):
            for iter_first in range(nn):
                # Find Lead Row
                mm = iter_first
                M = abs(_SST[iter_first][iter_first])
                for iter_second in range(iter_first + 1, nn):
                    Mi = abs(_SST[iter_second][iter_first])
                    if Mi > M:
                        mm = iter_second
                        M = Mi
                # Swapping of current N-th and lead mm-th rows
                _SST[iter_first], _SST[mm] = _SST[mm], _SST[iter_first]
                # Normalization of the current row
                Temp = _SST[iter_first][iter_first]
                for iter_second in range(iter_first, 2 * nn):
                    _SST[iter_first][iter_second] /= Temp
                # Orthogonalize the Current Column
                for iter_second in range(nn):
                    if iter_second != iter_first:
                        Temp = _SST[iter_second][iter_first]
                        for iter_third in range(iter_first, 2 * nn):
                            _SST[iter_second][iter_third] -= _SST[iter_first][iter_third] * Temp

        def P1Forming(_Y, _SST):
            _P1 = [[0.0 for _ in range(summs_count)] for _ in range(impl_len + 1)]
            for t in range(2, impl_len + 1):
                for j in range(summs_count):
                    _P1[t][j] = 0.0
                    for k in range(summs_count):
                        _P1[t][j] += G[k](_Y[t - 1]) * _SST[k][summs_count + j]
            return _P1

        def PForming(_Y, _P1):
            _P = [[0.0 for _ in range(impl_len + 1)] for _ in range(impl_len + 1)]
            for iter_first in range(2, impl_len + 1):
                for iter_second in range(2, impl_len + 1):
                    _P[iter_first][iter_second] = 0.0
                    for iter_third in range(summs_count):
                        _P[iter_first][iter_second] -= G[iter_third](_Y[iter_second - 1]) * _P1[iter_first][iter_third]
                    if iter_first == iter_second:
                        _P[iter_first][iter_first] += 1.0
            return _P

        def PrGradForming(_Y, _P):
            # Initialize the _Prgrad array
            _Prgrad = [0.0 for _ in range(impl_len + 1)]
            _grad = [0.0 for _ in range(impl_len + 1)]
            # Copying _Y values to _grad
            for i in range(1, impl_len + 1):
                _grad[i] = _Y[i]
            for iter_first in range(2, impl_len + 1):
                _Prgrad[iter_first] = 0.0
                for iter_second in range(2, impl_len + 1):
                    _Prgrad[iter_first] += _P[iter_first][iter_second] * _grad[iter_second]
            return _Prgrad

        def DualWLDMSolution(_w, _p, _Prgrad):
            Al = LARGE
            Alc = 0
            for iter_first in range(2, impl_len + 1):
                _w[iter_first] = 0
            iter_first = 0
            while iter_first < impl_len - summs_count - 1:
                Al = LARGE
                for iter_second in range(2, impl_len + 1):
                    if abs(_w[iter_second]) == _p[iter_second]:
                        continue
                    else:
                        if _Prgrad[iter_second] > 0:
                            Alc = (_p[iter_second] - _w[iter_second]) / _Prgrad[iter_second]
                        elif _Prgrad[iter_second] < 0:
                            Alc = (-_p[iter_second] - _w[iter_second]) / _Prgrad[iter_second]
                        if Alc < Al:
                            Al = Alc
                for iter_second in range(2, impl_len + 1):
                    if abs(_w[iter_second]) != _p[iter_second]:
                        _w[iter_second] += Al * _Prgrad[iter_second]
                        if abs(_w[iter_second]) == _p[iter_second]:
                            iter_first += 1

        def PrimalWLDMSolution(_Y, _SST, _w, _p, _a, _z):
            lc_r = [0 for _ in range(impl_len + 1)]  # Adjusted size
            lc_ri = 0  # The amount of basic equations of the primal problem
            for iter_first in range(2, impl_len + 1):
                if abs(_w[iter_first]) != _p[iter_first]:
                    lc_ri += 1
                    lc_r[lc_ri] = iter_first
            for iter_first in range(1, lc_ri + 1):
                for iter_second in range(1, summs_count + 1):
                    _SST[iter_first - 1][iter_second - 1] = G[iter_second - 1](_Y[lc_r[iter_first] - 1])
                _SST[iter_first - 1][summs_count] = _Y[lc_r[iter_first]]
            JGTransforming(summs_count, _SST)
            for iter_first in range(summs_count):
                _a[iter_first] = _SST[iter_first][summs_count]
            for i in range(1, impl_len + 1):
                _z[i] = _Y[i]
                for j in range(summs_count):
                    _z[i] -= _a[j] * G[j](_Y[i - 1])

        def GLDMEstimator(_Y):
            lc_w = [0.0 for _ in range(impl_len + 1)]  # WLDM weights
            lc_p = [1.0 for _ in range(impl_len + 1)]  # GLDM weights
            lc_a1 = [0.0 for _ in range(summs_count)]
            lc_a = [0.0 for _ in range(summs_count)]  # Identified parameters
            lc_z = [0.0 for _ in range(impl_len + 1)]  # WLDM approximation errors
            lc_SST = SSTForming(_Y)  # Matrix for J-G transforming
            JGTransforming(summs_count, lc_SST)
            lc_P1 = P1Forming(_Y, lc_SST)  # It is used for P calculation
            lc_P = PForming(_Y, lc_P1)  # Projection matrix
            lc_Prgrad = PrGradForming(_Y, lc_P)  # Projection of the gradient
            Z = d = 0.0
            while True:
                for i in range(summs_count):
                    lc_a1[i] = lc_a[i]
                for i in range(1, impl_len + 1):
                    lc_p[i] = 1.0 / (1.0 + lc_z[i] * lc_z[i])
                for i in range(1, impl_len + 1):
                    lc_w[i] = 0.0
                DualWLDMSolution(lc_w, lc_p, lc_Prgrad)
                PrimalWLDMSolution(_Y, lc_SST, lc_w, lc_p, lc_a, lc_z)
                Z = 0.0
                for i in range(2, impl_len + 1):
                    Z += abs(lc_z[i])
                d = max([abs(lc_a[i] - lc_a1[i]) for i in range(summs_count)])
                if d < 0.5:  # Adjust tolerance as needed
                    break
            Sol = Solution()
            Sol.a = lc_a
            Sol.z = lc_z
            Sol.Z = Z
            return Sol

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
            # Set the first calculated value equal to the first original value
            calculated_values[1] = Y[1]
            # Calculate the rest of the values based on the coefficients
            for t in range(2, length):
                value = 0  # No intercept
                for i in range(len(Sol.a)):
                    value += Sol.a[i] * G[i](Y[t - 1])
                calculated_values[t] = value
            return calculated_values

        def plot_time_series_adjusted(original_data, calculated_data, series_number, save_path):
            plt.figure(figsize=(10, 6))
            # Ensure the first value of calculated_data matches the original_data
            if len(original_data) >= 1 and len(calculated_data) >= 1:
                calculated_data[0] = original_data[0]
            # Adjust lengths if necessary to ensure both lists are of equal length
            min_length = min(len(original_data), len(calculated_data))
            # Exclude the last value from both sets of data
            original_data_adjusted = original_data[:min_length-1]
            calculated_data_adjusted = calculated_data[:min_length-1]
            # Adjust the x-axis range
            x_axis_range = range(1, len(original_data_adjusted) + 1)
            # Plotting the original and calculated data
            plt.plot(x_axis_range, original_data_adjusted, label='Original', color='blue', linewidth=2)
            plt.plot(x_axis_range, calculated_data_adjusted, label='GLDM Model', color='red', linestyle='dotted', linewidth=2)
            # Setting the plot title and labels
            plt.title(f'Time Series: {case_name}: Original vs GLDM Model', fontsize=16)
            plt.xlabel('Time', fontsize=14)
            plt.ylabel('Value', fontsize=14)
            # Adding a legend and grid
            plt.legend(loc='best', fontsize=12)
            plt.grid(True, which='both', linestyle='--', linewidth=0.5)
            # Saving the plot to a file and closing the plot figure
            plt.savefig(save_path, format='png', dpi=300)
            plt.close()

        def main():
            # Start measuring time and resources
            start_time = time.time()
            process = psutil.Process(os.getpid())
            initial_memory_use = process.memory_info().rss / (1024 * 1024)  # Convert bytes to MB

            # Find all .txt files in the current directory
            txt_files = glob.glob("*.txt")

            if not txt_files:
                print("No .txt files found in the current directory.")
                sys.exit(1)

            for input_filename in txt_files:
                print(f"Processing file: {input_filename}")
                try:
                    with open(input_filename, "r") as f, open(f"output_{input_filename}", "w") as g:
                        # Data Input
                        # Reading until ':' is encountered
                        lc_c = ''
                        while lc_c != ':':
                            lc_c = f.read(1)
                        m, ts = map(int, f.readline().split())
                        global impl_len
                        impl_len = m  # Length of time series
                        global summs_count
                        summs_count = 2  # Number of coefficients (a1 and a2)
                        print(f"Length: {m}\nTime series: {ts}\n")
                        # Reading time series data
                        setnum = 0
                        RY = [[] for _ in range(ts)]  # Create the ts arrays for time series
                        for i in range(ts):
                            RY[i] = [0.0] * (m + 2)
                        while setnum < ts:
                            print("Reading time series", setnum)
                            ic = 1
                            while ic <= m:
                                line = f.readline()  # Read the next line
                                if not line:
                                    break  # End of file
                                s = float(line.strip())
                                RY[setnum][ic] = s
                                ic += 1
                            print("\n Finished reading of time series", setnum)
                            setnum += 1
                        GL_RY = RY
                        # Writing results to a file
                        g.write(f"Number of time series: {ts}\n")
                        g.write(f"Length of time series: {impl_len}\n")
                        # Processing each time series
                        for sn in range(ts):
                            Y = [0.0 for _ in range(m + 2)]
                            for j in range(1, m + 1):
                                Y[j] = RY[sn][j]
                            GL_Y = GL_RY[sn]
                            lc_SST = [[0.0 for _ in range(summs_count * 2)] for _ in range(summs_count)]
                            # Solution
                            GForming()
                            print("GForming() OK\n")
                            lc_SST = SSTForming(GL_Y)
                            JGTransforming(summs_count, lc_SST)
                            print("\n JGTransforming() OK\n")
                            Sol = GLDMEstimator(GL_Y)
                            print("GLDMEstimator() OK\n")
                            # Calculate the time series values using the obtained coefficients
                            calculated_ts_values = [0.0 for _ in range(len(GL_Y))]
                            calculated_ts_values = calculate_time_series_values(GL_Y, Sol, len(GL_Y))
                            # Write the calculated time series values to the output file
                            g.write("Calculated Time Series Values:\n")
                            for val in calculated_ts_values[1:]:
                                g.write(f"{val}\n")
                            # Error calculations and table display
                            original_data_trimmed = GL_Y[1:]  # Exclude index 0
                            calculated_data_trimmed = calculated_ts_values[1:]
                            # Ensure the lengths match
                            min_length = min(len(original_data_trimmed), len(calculated_data_trimmed))
                            original_data_trimmed = original_data_trimmed[:min_length-1]  # Exclude last point
                            calculated_data_trimmed = calculated_data_trimmed[:min_length-1]  # Exclude last point
                            # Calculate errors using consistent slicing
                            mae = calculate_mae(original_data_trimmed, calculated_data_trimmed)
                            mbe = calculate_mbe(original_data_trimmed, calculated_data_trimmed)
                            mse = calculate_mse(original_data_trimmed, calculated_data_trimmed)
                            rmse = calculate_rmse(original_data_trimmed, calculated_data_trimmed)
                            r_squared = calculate_r_squared(original_data_trimmed, calculated_data_trimmed)
                            mape = calculate_mape(original_data_trimmed, calculated_data_trimmed)
                            me = calculate_me(original_data_trimmed, calculated_data_trimmed)
                            median_abs_error = calculate_median_absolute_error(original_data_trimmed, calculated_data_trimmed)
                            # Assuming a seasonal period for MASE calculation; adjust as necessary
                            seasonal_period = 1  # This should be set based on your data's seasonality
                            mase = calculate_mase(original_data_trimmed, calculated_data_trimmed, seasonal_period)
                            g.write(f"Error Matrix excluding the last data point\n")
                            # Write the results to the file
                            g.write(f"RMSE: {rmse}\n")
                            g.write(f"R-squared: {r_squared}\n")
                            g.write(f"MAPE: {mape}\n")
                            g.write(f"MAE: {mae}\n")
                            g.write(f"MSE: {mse}\n")
                            g.write(f"ME: {me}\n")
                            g.write(f"Median Absolute Error: {median_abs_error}\n")
                            g.write(f"MASE: {mase}\n")
                            g.write(f"MBE: {mbe}\n")
                            # Prepare and display the table
                            g.write(f"\n{'Original Data':<20}{'Calculated Data':<20}{'Error':<20}\n")
                            for orig, calc in zip(original_data_trimmed, calculated_data_trimmed):
                                error = orig - calc
                                g.write(f"{orig:<20}{calc:<20}{error:<20}\n")
                            # Initialize ANS with 8 elements
                            ANS = [0] * 8
                            ANS[0] = sn  # Time Series Number
                            ANS[1] = 0   # Placeholder for future use or additional data
                            # Assigning model coefficients to ANS.
                            ANS[2] = Sol.a[0]  # Coefficient a1
                            ANS[3] = Sol.a[1]  # Coefficient a2
                            # Writing the results with descriptive labels
                            g.write(f"\nModel Coefficients:\n")
                            g.write(f"Coefficient a1: {ANS[2]}\n")
                            g.write(f"Coefficient a2: {ANS[3]}\n")
                            # Define paths for saving the plots
                            plot_save_path = f"plot_{input_filename}_series_{sn}_adjusted.png"
                            # Make a copy of calculated_ts_values to pass to the adjusted plotting function
                            adjusted_calculated_data = calculated_ts_values.copy()
                            # Call the plotting function with the save path
                            plot_time_series_adjusted(Y[1:], adjusted_calculated_data[1:], sn, plot_save_path)
                            # Stop measuring time and resources
                            end_time = time.time()
                            final_memory_use = process.memory_info().rss / (1024 * 1024)  # Convert bytes to MB
                            # Calculate total time and memory used
                            total_time = end_time - start_time
                            total_memory_used = final_memory_use - initial_memory_use
                            g.write("\nPerformance Metrics:\n")
                            g.write(f"Total Execution Time: {total_time:.2f} seconds\n")
                            g.write(f"Total Additional Memory Used: {total_memory_used:.2f} MB\n")
                    print(f"Finished processing {input_filename}. Output written to output_{input_filename}")
                except FileNotFoundError:
                    print(f"Error: The file '{input_filename}' was not found.")
                    continue
                except Exception as e:
                    print(f"An error occurred while processing {input_filename}: {e}")
                    continue
    # if __name__ == "__main__":
        main()
        print("Completing the execution of the First-order Generalized Least Deviation Method (GLDM).")