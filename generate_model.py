from src.data_generator import main as data_generator
from src.train import main as train

def main():
  data_generator()
  train()

if __name__ == "__main__":
  main()
