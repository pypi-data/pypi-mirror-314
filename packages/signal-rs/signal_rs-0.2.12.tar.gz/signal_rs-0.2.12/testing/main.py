from signal_rs import amvParameters, amvSignalAnalysis
import pandas as pd

def main():
    
    sample_data = {
    "run_counter": [1, 1, 1, 1, 1, 1],
    "channel": [1, 1, 1, 1, 1, 1],
    "data": [0, 5, 100, 500, 150, 1],
    "duration": [0, 250, 500, 750, 1000, 1250]
}
    df = pd.DataFrame(sample_data)
    
    amv_params = amvParameters()
    print(amv_params.P0013)
    amv = amvSignalAnalysis(df=df)
    amv.get_baseline()
    
    
    
if __name__ == "__main__":
    main()
    
