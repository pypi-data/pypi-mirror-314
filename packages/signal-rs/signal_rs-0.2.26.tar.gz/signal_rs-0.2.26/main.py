import signal_rs as sr
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

def main():
    
    sample_data = {
    "run_counter": [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
    "channel": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "data": [0, 5, 100, 500, 150, 1, 0, 4, 80, 450, 140, 2],
    "duration": [0, 250, 500, 750, 1000, 1250, 0, 250, 500, 750, 1000, 1250],
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
    #x = sr.integral_calculation_rust()
    #print(x)
    amv = sr.amvSignalAnalysis(df=df)
    amv.integral_calculation()
    fig = amv.plot_unmodified_signal(mode='lines')
    print(fig)
    pio.write_image(fig, 'fig.png')
    
    
    
    
if __name__ == "__main__":
    main()
    
