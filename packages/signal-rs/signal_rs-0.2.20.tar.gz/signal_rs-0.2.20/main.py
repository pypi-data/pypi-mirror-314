import signal_rs as sr
import pandas as pd

def main():
    
    sample_data = {
    "run_counter": [1, 1, 1, 1, 1, 1],
    "channel": [1, 1, 1, 1, 1, 1],
    "data": [0, 5, 100, 500, 150, 1],
    "duration": [0, 250, 500, 750, 1000, 1250]
}
    df = pd.DataFrame(sample_data)
    
    # amv_params = amvParameters()
    # print(amv_params.P0013)
    # amv = amvSignalAnalysis(df=df)
    # df = amv.get_baseline()
    # integral = amv.integral_calculation()
    # print(integral)
    # print(df)
    #sr.amvSignalAnalysis(df=df)
    print(sr.__package__)
    print(sr.__doc__)
    print(sr.__all__)
    x = sr.integral_calculation_rust()
    print(x)
    amv = sr.amvSignalAnalysis(df=df)
    amv.integral_calculation()
    
    
    
if __name__ == "__main__":
    main()
    
