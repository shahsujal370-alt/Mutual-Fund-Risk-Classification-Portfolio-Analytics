from prepare_data import main as prepare
from train_model import main as train
from recommend import recommend
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    prepare(); train()
    for risk in ['Low','Medium','High']:
        recommend(risk,5).to_csv(ROOT/'outputs'/f'recommendations_{risk.lower()}.csv',index=False)
    print('\nPipeline completed. Outputs are in outputs/.')
if __name__=='__main__': main()
